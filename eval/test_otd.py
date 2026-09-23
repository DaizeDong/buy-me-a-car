"""Production calculator tests against independently authored synthetic oracles."""
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/orchestrator/scripts/otd_calculator.py"
sys.path.insert(0, str(SCRIPT.parent))
import otd_calculator as otd

GOLDEN = json.loads((ROOT / "eval/golden/otd_cases.json").read_text(encoding="utf-8"))
REVIEW_DATE = dt.date.fromisoformat(GOLDEN["_meta"]["as_of"])


def arguments(case):
    return {key: case[key] for key in ("sales", "doc", "state", "title", "reg", "trade", "trade_payoff", "condition", "local_rate", "warranty") if key in case}


class ProductionStateTests(unittest.TestCase):
    def test_supported_forward_cases(self):
        self.assertGreaterEqual(len(GOLDEN["forward"]), 8)
        for case in GOLDEN["forward"]:
            with self.subTest(case=case["name"]):
                result = otd.compute_state_otd(**arguments(case), today=REVIEW_DATE)
                for key in ("tax", "otd", "balance_due"):
                    self.assertEqual(result[key], Decimal(case[key]))
                self.assertEqual(result["status"], "estimate")
                self.assertEqual(result["tax_rule_evidence"], "verified")

    def test_reverse_is_maximum_cent_within_budget(self):
        for case in GOLDEN["forward"]:
            with self.subTest(case=case["name"]):
                args = arguments(case)
                sales = Decimal(args.pop("sales"))
                result = otd.reverse_state_otd(case["otd"], **args, today=REVIEW_DATE)
                self.assertEqual(result["sales"], sales)
                self.assertLessEqual(result["otd"], Decimal(case["otd"]))
                above = otd.compute_state_otd(result["sales"] + otd.CENT, **args, today=REVIEW_DATE)
                self.assertGreater(above["otd"], Decimal(case["otd"]))

    def test_actual_production_trade_rules(self):
        for case in GOLDEN["trade_rules"]:
            with self.subTest(case=case):
                result = otd.trade_credit_for_state(case["state"], case["trade"], as_of=case["as_of"], today=REVIEW_DATE)
                self.assertEqual(result, Decimal(case["credit"]))

    def test_unsupported_mechanism_cannot_use_headline_rate(self):
        for state in ("GA", "DC", "OR", "DE", "CA"):
            with self.subTest(state=state), self.assertRaisesRegex(ValueError, "unsupported"):
                otd.compute_state_otd(30000, 100, state, 50, 100, today=REVIEW_DATE)

    def test_alaska_zero_state_rate_does_not_support_an_otd(self):
        for local_rate in (None, "0", "0.05"):
            for calculate in (otd.compute_state_otd, otd.reverse_state_otd):
                with self.subTest(local_rate=local_rate, calculation=calculate.__name__):
                    with self.assertRaisesRegex(ValueError, "AK calculation unsupported"):
                        calculate(30000, 100, "AK", 50, 100,
                                  local_rate=local_rate, today=REVIEW_DATE)

    def test_variable_fees_must_be_explicit(self):
        with self.assertRaisesRegex(ValueError, "--title and --reg"):
            otd.compute_state_otd(30000, 800, "MD", today=REVIEW_DATE)

    def test_unsupported_transaction_classes_are_rejected(self):
        for kwargs in ({"transaction": "lease"}, {"transaction": "private_sale"}, {"vehicle": "ev"}, {"vehicle": "commercial"}):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, "Only ordinary"):
                otd.compute_state_otd(30000, 800, "MD", 200, 100, today=REVIEW_DATE, **kwargs)

    def test_md_low_residual_value_needs_separate_review(self):
        with self.assertRaisesRegex(ValueError, "valuation/minimum"):
            otd.compute_state_otd(30000, 0, "MD", 200, 100, trade=30000, today=REVIEW_DATE)

    def test_md_fee_above_verified_cap_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "statutory cap"):
            otd.compute_state_otd(30000, 801, "MD", 200, 100, today=REVIEW_DATE)

    def test_local_tax_not_blindly_added(self):
        with self.assertRaisesRegex(ValueError, "local sales-tax stack"):
                otd.compute_state_otd(30000, 225, "TX", 33, 100, local_rate="0.01", today=REVIEW_DATE)

    def test_nj_requires_used_condition_until_new_vehicle_surcharge_encoded(self):
        for condition in (None, "new"):
            with self.subTest(condition=condition), self.assertRaisesRegex(ValueError, "condition.*used"):
                otd.compute_state_otd(30000, 500, "NJ", 85, 100, condition=condition, today=REVIEW_DATE)

    def test_ny_local_rate_and_qualifying_doc_are_required(self):
        with self.assertRaisesRegex(ValueError, "--local"):
            otd.compute_state_otd(30000, 175, "NY", 50, 100, today=REVIEW_DATE)
        with self.assertRaisesRegex(ValueError, "cap"):
            otd.compute_state_otd(30000, 176, "NY", 50, 100, local_rate="0.04", today=REVIEW_DATE)

    def test_ct_reverse_budget_in_luxury_tax_jump(self):
        result = otd.reverse_state_otd(53500, 500, "CT", 25, 100, today=REVIEW_DATE)
        self.assertEqual(result["sales"], Decimal("49500.00"))
        self.assertEqual(result["budget_remaining"], Decimal("200.00"))
        self.assertGreater(otd.compute_state_otd("49500.01", 500, "CT", 25, 100, today=REVIEW_DATE)["otd"], Decimal("53500"))

    def test_warranty_cannot_silently_use_unencoded_state_treatment(self):
        with self.assertRaisesRegex(ValueError, "warranty"):
            otd.compute_state_otd(30000, 0, "MD", 200, 100, warranty=1000, today=REVIEW_DATE)

    def test_ct_warranty_only_threshold_crossing_requires_review(self):
        with self.assertRaisesRegex(ValueError, "warranty.*threshold"):
            otd.compute_state_otd(50000, 0, "CT", 25, 100, warranty=1000, today=REVIEW_DATE)
        result = otd.reverse_state_otd(54000, 0, "CT", 25, 100, warranty=1000, today=REVIEW_DATE)
        self.assertEqual(result["sales"], Decimal("49000.00"))

    def test_payoff_does_not_change_tax(self):
        args = dict(sales=30000, doc=200, state="TX", title=33, reg=100, trade=10000, today=REVIEW_DATE)
        cash = otd.compute_state_otd(**args)
        lien = otd.compute_state_otd(**args, trade_payoff=12000)
        self.assertEqual(cash["tax"], lien["tax"])
        self.assertEqual(lien["balance_due"] - cash["balance_due"], Decimal("12000"))

    def test_addon_tax_classification_changes_tax(self):
        args = dict(sales=30000, doc=200, state="TX", title=33, reg=100, today=REVIEW_DATE)
        taxable = otd.compute_state_otd(**args, taxable_addons=100)
        exempt = otd.compute_state_otd(**args, addons=100)
        self.assertEqual(taxable["tax"] - exempt["tax"], Decimal("6.25"))


class GenericAndCliTests(unittest.TestCase):
    def test_alaska_cli_refuses_a_state_total_with_explicit_zero_local_tax(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--sales", "30000", "--forward",
             "--state", "AK", "--local", "0", "--title", "50", "--reg", "100", "--json"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AK calculation unsupported", result.stderr)
        self.assertEqual(result.stdout.strip(), "")
        self.assertNotIn("Traceback", result.stderr)

    def test_generic_reverse_rounding_cannot_overspend(self):
        result = otd.reverse_otd("100.01", "1.99", "0.06625", 1, 1)
        self.assertLessEqual(result["otd"], Decimal("100.01"))
        higher = otd.compute_otd(result["sales"] + otd.CENT, "1.99", "0.06625", 1, 1)
        self.assertGreater(higher["otd"], Decimal("100.01"))

    def test_cli_invalid_numbers_fail_without_traceback(self):
        for value in ("NaN", "Infinity", "-1", "100.001"):
            result = subprocess.run([sys.executable, str(SCRIPT), "--sales", value, "--forward", "--estimate", "--tax-rate", "6", "--doc-taxable", "yes", "--title", "1", "--reg", "1"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)

    def test_custom_estimate_is_explicit_and_labelled(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--sale-price", "100", "--forward", "--state", "GA", "--estimate", "--tax-rate", "7", "--doc-taxable", "no", "--doc", "10", "--title", "1", "--reg", "1", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "unverified_custom_estimate")
        self.assertEqual(data["tax"], "7.00")


if __name__ == "__main__":
    unittest.main()
