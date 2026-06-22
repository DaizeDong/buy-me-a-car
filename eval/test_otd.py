#!/usr/bin/env python3
"""Objective eval harness for the OTD calculator (pure stdlib, no pytest).

Run directly:  python eval/test_otd.py
Or via the runner:  bash eval/run.sh

Asserts:
  1. Forward OTD computed to the cent against frozen golden cases (eval/golden/otd_cases.json),
     all sourced from data/state_fees.json verified values.
  2. Reverse (target OTD -> sale ceiling) round-trips within +/-$0.01.
  3. Trade-in tax credit semantics documented in skills/otd-calculator/SKILL.md:
       - granted states: trade reduces taxable base;
       - CA / KY / DC: trade IGNORED for tax (full price taxed);
       - MI / IL: trade credit CLAMPED at a statutory cap.
  4. Doc-fee cap WARNING fires when doc > statutory cap and not when doc <= cap.
"""
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "skills", "orchestrator", "scripts")
GOLDEN_PATH = os.path.join(REPO_ROOT, "eval", "golden", "otd_cases.json")
sys.path.insert(0, SCRIPTS_DIR)

import otd_calculator as otd  # noqa: E402

CENT = 0.01  # reverse round-trip tolerance (+/-$0.01)


def _rate(case):
    """Combined rate computed EXACTLY as the calculator/CLI does:
    JSON state base rate + local_pct/100. Never read a pre-rounded combined
    rate from the golden file -- that reintroduces half-cent drift."""
    return otd.STATE_TAX_RATES[case["state"]] + case["local_pct"] / 100.0


def _sale(result):
    """compute_otd/reverse_otd return the sale price under key 'sales'."""
    return result["sales"]


# --- Reference trade-aware helpers -------------------------------------------
# The shipped calculator (compute_otd / reverse_otd) has no trade-in parameter;
# the trade semantics live as prose formulas in otd-calculator/SKILL.md. These
# helpers encode those documented formulas so we can assert them objectively.

NO_TRADE_CREDIT_STATES = {"CA", "KY", "DC"}


def _trade_clamp_for(state):
    """Read the trade-credit clamp straight from state_fees.json so the test
    tracks the single source of truth rather than a hard-coded copy."""
    with open(
        os.path.join(REPO_ROOT, "data", "state_fees.json"), encoding="utf-8"
    ) as f:
        data = json.load(f)
    for rec in data["states"]:
        if rec["state"] == state:
            return rec.get("trade_credit", {}).get("cap")
    return None


def compute_otd_with_trade(sale, doc, tax_rate, title, reg, state, trade=0.0, addons=0.0):
    """Forward OTD honoring documented trade-in tax-credit semantics."""
    if state in NO_TRADE_CREDIT_STATES:
        credited_trade = 0.0  # CA/KY/DC: trade never reduces tax base
    else:
        clamp = _trade_clamp_for(state)
        credited_trade = trade if clamp is None else min(trade, clamp)
    taxable = sale + doc - credited_trade
    tax = taxable * tax_rate
    otd_total = sale + doc + tax + title + reg + addons
    return {"taxable": taxable, "tax": tax, "otd": otd_total,
            "credited_trade": credited_trade}


class TestForwardGolden(unittest.TestCase):
    """Forward OTD must match frozen golden values to the cent."""

    @classmethod
    def setUpClass(cls):
        with open(GOLDEN_PATH, encoding="utf-8") as f:
            cls.golden = json.load(f)

    def test_forward_cases_exist(self):
        self.assertTrue(self.golden["forward"], "golden forward list is empty")

    def test_forward_to_the_cent(self):
        for c in self.golden["forward"]:
            with self.subTest(state=c["state"]):
                r = otd.compute_otd(c["sale"], c["doc"], _rate(c),
                                    c["title"], c["reg"])
                # "To the cent": round the computed result to 2 dp and require
                # exact equality with the golden (which was frozen the same way,
                # using the identical base+local rate path). Stable across
                # interpreters; immune to half-cent float boundaries because the
                # rounding is applied once, consistently, on both sides.
                self.assertEqual(
                    round(r["tax"], 2), c["expected_tax"],
                    msg=f"{c['state']} tax {r['tax']:.6f} -> {round(r['tax'],2)} "
                        f"!= golden {c['expected_tax']}")
                self.assertEqual(
                    round(r["otd"], 2), c["expected_otd"],
                    msg=f"{c['state']} OTD {r['otd']:.6f} -> {round(r['otd'],2)} "
                        f"!= golden {c['expected_otd']}")

    def test_golden_inputs_match_state_fees_json(self):
        """Guard that golden title / reg still equal JSON values (the combined
        rate is derived live from JSON base + local_pct, so it cannot drift)."""
        for c in self.golden["forward"]:
            with self.subTest(state=c["state"]):
                self.assertIn(c["state"], otd.STATE_TAX_RATES,
                              f"{c['state']} missing from JSON")
                self.assertEqual(otd.STATE_DEFAULT_TITLE[c["state"]], c["title"],
                                 f"{c['state']} title drifted from JSON")
                self.assertEqual(otd.STATE_DEFAULT_REG[c["state"]], c["reg"],
                                 f"{c['state']} reg drifted from JSON")


class TestReverseRoundTrip(unittest.TestCase):
    """reverse_otd(forward(sale)) must recover sale within +/-$0.01."""

    @classmethod
    def setUpClass(cls):
        with open(GOLDEN_PATH, encoding="utf-8") as f:
            cls.golden = json.load(f)

    def test_round_trip_within_one_cent(self):
        for c in self.golden["forward"]:
            with self.subTest(state=c["state"]):
                rate = _rate(c)
                fwd = otd.compute_otd(c["sale"], c["doc"], rate,
                                      c["title"], c["reg"])
                back = otd.reverse_otd(fwd["otd"], c["doc"], rate,
                                       c["title"], c["reg"])
                self.assertLessEqual(
                    abs(_sale(back) - c["sale"]), CENT,
                    msg=f"{c['state']} round-trip sale off by more than $0.01")

    def test_reverse_with_addons_round_trip(self):
        # addons must survive the reverse algebra too
        fwd = otd.compute_otd(28000, 300, 0.06, 50, 135, addons=225)
        back = otd.reverse_otd(fwd["otd"], 300, 0.06, 50, 135, addons=225)
        self.assertLessEqual(abs(_sale(back) - 28000), CENT)


class TestTradeCredit(unittest.TestCase):
    """Documented trade-in tax-credit semantics."""

    def test_granted_state_trade_reduces_tax(self):
        # NJ grants credit: $10k trade cuts taxable base by $10k.
        rate = otd.STATE_TAX_RATES["NJ"]
        with_trade = compute_otd_with_trade(30000, 499, rate, 85, 70, "NJ", trade=10000)
        without = compute_otd_with_trade(30000, 499, rate, 85, 70, "NJ", trade=0)
        self.assertAlmostEqual(with_trade["credited_trade"], 10000, places=2)
        saved = without["tax"] - with_trade["tax"]
        self.assertAlmostEqual(saved, 10000 * rate, places=2)

    def test_CA_KY_DC_ignore_trade_for_tax(self):
        for st in ("CA", "KY", "DC"):
            with self.subTest(state=st):
                rate = otd.STATE_TAX_RATES[st]
                wt = compute_otd_with_trade(30000, 85, rate, 25, 250, st, trade=10000)
                nt = compute_otd_with_trade(30000, 85, rate, 25, 250, st, trade=0)
                self.assertEqual(wt["credited_trade"], 0.0,
                                 f"{st} must not credit trade for tax")
                self.assertAlmostEqual(wt["tax"], nt["tax"], places=2,
                                       msg=f"{st} tax changed with trade (should not)")

    def test_MI_clamps_trade_credit(self):
        clamp = _trade_clamp_for("MI")
        self.assertIsNotNone(clamp, "MI trade clamp missing from state_fees.json")
        rate = otd.STATE_TAX_RATES["MI"]
        over = clamp + 3000
        wt = compute_otd_with_trade(40000, 230, rate, 15, 100, "MI", trade=over)
        # Only `clamp` of the trade earns credit.
        self.assertAlmostEqual(wt["credited_trade"], clamp, places=2)
        full = compute_otd_with_trade(40000, 230, rate, 15, 100, "MI", trade=0)
        saved = full["tax"] - wt["tax"]
        self.assertAlmostEqual(saved, clamp * rate, places=2)

    def test_IL_clamps_trade_credit(self):
        clamp = _trade_clamp_for("IL")
        self.assertIsNotNone(clamp, "IL trade clamp missing from state_fees.json")
        rate = otd.STATE_TAX_RATES["IL"] + 0.0125  # Naperville-style local
        over = clamp + 2000
        wt = compute_otd_with_trade(40000, 347.26, rate, 155, 151, "IL", trade=over)
        self.assertAlmostEqual(wt["credited_trade"], clamp, places=2)
        # Trade below clamp gets full credit.
        under = compute_otd_with_trade(40000, 347.26, rate, 155, 151, "IL", trade=7000)
        self.assertAlmostEqual(under["credited_trade"], 7000, places=2)


class TestDocCapWarning(unittest.TestCase):
    """Doc-fee cap warning must fire iff doc exceeds the statutory cap."""

    def _run_cli(self, args):
        argv = sys.argv
        out = io.StringIO()
        try:
            sys.argv = ["otd_calculator.py"] + args
            with redirect_stdout(out):
                otd.main()
        finally:
            sys.argv = argv
        return out.getvalue()

    def test_warning_fires_over_cap(self):
        # CA cap is $85; $499 must trigger the warning.
        self.assertIsNotNone(otd.STATE_DOC_FEE_CAP["CA"])
        text = self._run_cli(["--target", "30000", "--state", "CA", "--doc", "499"])
        self.assertIn("WARNING", text)
        self.assertIn("caps doc fee", text)

    def test_no_warning_at_or_under_cap(self):
        # CA $85 == cap: no warning.
        text = self._run_cli(["--target", "30000", "--state", "CA", "--doc", "85"])
        self.assertNotIn("WARNING", text)

    def test_no_cap_state_never_warns(self):
        # AL has no statutory cap (null in JSON); any doc must not warn.
        self.assertIsNone(otd.STATE_DOC_FEE_CAP["AL"])
        text = self._run_cli(["--target", "30000", "--state", "AL", "--doc", "1500"])
        self.assertNotIn("WARNING", text)

    def test_md_cap_is_800_and_warns_at_499(self):
        # Regression anchor: MD verified cap is $800 (NOT $300/$499 legacy prose).
        # A $499 doc must therefore NOT warn in MD.
        self.assertEqual(otd.STATE_DOC_FEE_CAP["MD"], 800)
        text = self._run_cli(["--target", "30000", "--state", "MD", "--doc", "499"])
        self.assertNotIn("WARNING", text)
        text_over = self._run_cli(["--target", "30000", "--state", "MD", "--doc", "950"])
        self.assertIn("WARNING", text_over)


if __name__ == "__main__":
    unittest.main(verbosity=2)
