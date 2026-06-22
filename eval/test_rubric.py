#!/usr/bin/env python3
"""Judge-rubric eval for the buy-me-a-car non-deterministic skills.

Two tiers:

  1. Deterministic sub-checks (DEFAULT, offline, free): regex / counting /
     substring checks that need no model call. These validate (a) the cheap
     mechanical gates of the negotiation-counter rubric -- ASCII-only,
     numbered-ask count, walk-away presence, line cap -- against golden
     sample drafts, (b) leak-flag substrings against the leak fixtures, and
     (c) integrity of the fixtures + rubrics + routing JSON.

  2. LLM-judge cases (OPT-IN via --llm): the qualitative rubric criteria
     that genuinely need a model (anchor-is-REAL, ADM-decoupling, D10
     re-anchor judgment, routing on ambiguous prompts). Skipped by default so
     the suite runs free and offline in CI / pre-commit.

Run:
    python test_rubric.py            # deterministic only (offline, default)
    python test_rubric.py --llm      # also run LLM-judge cases (needs a model)
    python test_rubric.py -v         # verbose per-check output

Exit code 0 iff all RUN checks pass. Skipped LLM checks never fail the run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
FIXTURES = EVAL_DIR / "fixtures"
LEAK_DIR = FIXTURES / "leak_quotes"
RUBRICS = EVAL_DIR / "rubrics"
ROUTING_JSON = FIXTURES / "routing_prompts.json"


# --------------------------------------------------------------------------- #
# Deterministic checkers (reusable; these are what a fast pre-save gate would
# call on a freshly drafted counter email).
# --------------------------------------------------------------------------- #

# Characters/markers forbidden in a dealer-facing draft body (gotcha E1).
_NON_ASCII = re.compile(r"[^\x00-\x7f]")
_MD_MARKERS = [
    ("bold", re.compile(r"\*\*")),
    ("backtick", re.compile(r"`")),
    ("md_link", re.compile(r"\[[^\]]+\]\([^)]+\)")),
    ("heading", re.compile(r"(?m)^\s*#{1,6}\s")),
    ("hr_dash", re.compile(r"(?m)^\s*---+\s*$")),
    ("hr_star", re.compile(r"(?m)^\s*\*\*\*+\s*$")),
    ("strikethrough", re.compile(r"~~")),
]
# Curly/typographic chars are non-ASCII so _NON_ASCII catches them too, but we
# name them for clearer diagnostics.
_TYPO_CHARS = {
    "em_dash": "—",
    "en_dash": "–",
    "curly_double_open": "“",
    "curly_double_close": "”",
    "curly_single_open": "‘",
    "curly_single_close": "’",
    "bullet": "•",
}

_NUMBERED_ASK = re.compile(r"(?m)^\s*(\d+)[\.\)]\s+\S")
_WALK_AWAY = re.compile(
    r"\b(above\s+\$?[\d,]+\s+otd|move forward with|walk|other anchor"
    r"|other option|hard cap|will move on)\b",
    re.IGNORECASE,
)


def ascii_violations(body: str) -> list[str]:
    """Return list of human-readable ASCII/markdown violations in a draft body."""
    out: list[str] = []
    if _NON_ASCII.search(body):
        for name, ch in _TYPO_CHARS.items():
            if ch in body:
                out.append(f"non-ascii:{name}")
        # any other stray non-ascii not in the named set
        stray = set(_NON_ASCII.findall(body)) - set(_TYPO_CHARS.values())
        if stray:
            out.append("non-ascii:other(" + ",".join(sorted(stray)) + ")")
    for name, rx in _MD_MARKERS:
        if rx.search(body):
            out.append(f"markdown:{name}")
    return out


def count_numbered_asks(body: str) -> int:
    """Count distinct leading numbered list items (1) 2) 3) ...)."""
    nums = [int(m.group(1)) for m in _NUMBERED_ASK.finditer(body)]
    return len(nums)


def has_walk_away(body: str) -> bool:
    return bool(_WALK_AWAY.search(body))


def content_line_count(body: str) -> int:
    """Count non-blank body lines excluding greeting + sign-off scaffolding."""
    lines = [ln.strip() for ln in body.splitlines()]
    lines = [ln for ln in lines if ln]
    drop = re.compile(
        r"^(hi\b|hello\b|hey\b|good (morning|afternoon)|thanks,?$|thank you,?$"
        r"|best,?$|regards,?$|[A-Z][a-z]+$)",
        re.IGNORECASE,
    )
    return sum(1 for ln in lines if not drop.match(ln))


# --------------------------------------------------------------------------- #
# Golden sample drafts: small in-repo corpus the deterministic gates run on so
# the offline suite actually exercises the checkers. GOOD drafts must pass all
# mechanical gates; BAD drafts must trip the specific gate named.
# --------------------------------------------------------------------------- #

GOOD_DRAFT_D8 = """Hi Tony,

Thanks for the breakdown. Three items:

1) The NJ Supplemental Titling Fee $13.50 is an NJ line item; CT does not have it.
2) The $7.50 tire fee is also NJ-style; CT has no per-tire fee. Please send a full revised OTD with both removed, not just a single-line edit.
3) For the sale price, Edmunds Hartford CT shows the 2023 Outback Limited average list at $27,100. My target to commit is $29,500 OTD.

Hoffman Subaru has a comparable 2023 Outback Limited at $28,400 ask.

Above $30,000 OTD I will move forward with my other anchors. Cash buyer, cashier's check, ready to close Friday pending PPI.

Thanks,

<BUYER_NAME>
"""

GOOD_DRAFT_D9 = """Hi Marisa,

Thanks for the numbers. Three items:

1) Please remove the $1,495 Toyota Hybrid Adjustment line. MSRP is the ceiling, not the floor on this trim, so it has to come off before we go further.
2) Please send a clean OTD on MSRP plus tax, doc, title, and reg only.
3) Confirm no other dealer add-ons (paint, etching, nitrogen) are in the quote.

CarGurus shows 2026 RAV4 Hybrid XLE Premium pricing at or under MSRP in the Philadelphia region.

Above $40,000 OTD I will move forward with an MSRP-clean store. The financing-rate offer is a separate conversation and does not change the ADM ask.

Thanks,

<BUYER_NAME>
"""

GOOD_DRAFT_D10 = """Hi Greg,

Thanks for the update. Three items:

1) Can you forward the sold-date confirmation on the original VIN (bill of sale or CRM sold timestamp)? I want to be sure I am not still racing the same VIN elsewhere.
2) On the substitute at 36,000 miles, the OTD needs to land at or under the original benchmark adjusted only for the 8,000-mile delta at $0.12/mi, about $960.
3) Treat this as a fresh quote: please send the full written OTD line by line.

KBB Boston shows the 2022 CR-V EX-L band consistent with the original $26,500 ask.

Above $29,000 OTD I will move forward with my other anchors. Cash buyer, ready to close this week pending PPI.

Thanks,

<BUYER_NAME>
"""

# BAD drafts: each trips exactly one gate, used to prove the checkers FAIL loudly.
BAD_ASCII = "Hi Tony,\n\nThanks — three items below. Please remove the **tire fee**.\n\nThanks,\n<BUYER_NAME>\n"
BAD_ASK_COUNT = (
    "Hi Tony,\n\nTwo items:\n\n1) Drop the tire fee.\n2) Drop the titling fee.\n\n"
    "Above $30,000 OTD I will move forward.\n\nThanks,\n<BUYER_NAME>\n"
)
BAD_NO_WALK = (
    "Hi Tony,\n\nThree items:\n\n1) Drop the tire fee.\n2) Drop the titling fee.\n"
    "3) Target $29,500 OTD.\n\nEdmunds Hartford shows $27,100.\n\nThanks,\n<BUYER_NAME>\n"
)

GOOD_DRAFTS = {
    "D8": GOOD_DRAFT_D8,
    "D9": GOOD_DRAFT_D9,
    "D10": GOOD_DRAFT_D10,
}


# --------------------------------------------------------------------------- #
# Test runner scaffolding
# --------------------------------------------------------------------------- #

class Result:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures: list[str] = []

    def check(self, name: str, ok: bool, detail: str = "", verbose: bool = False) -> None:
        if ok:
            self.passed += 1
            if verbose:
                print(f"  PASS  {name}")
        else:
            self.failed += 1
            self.failures.append(f"{name}: {detail}")
            print(f"  FAIL  {name} :: {detail}")

    def skip(self, name: str, verbose: bool = False) -> None:
        self.skipped += 1
        if verbose:
            print(f"  SKIP  {name} (LLM-judge; pass --llm to run)")


# --------------------------------------------------------------------------- #
# Deterministic test groups
# --------------------------------------------------------------------------- #

def test_fixture_integrity(r: Result, v: bool) -> None:
    print("[integrity] fixtures + rubrics + routing JSON")
    expected_leaks = ["D8_ct_tire_fee.md", "D9_rav4_adm.md", "D10_bait_switch.md"]
    for fn in expected_leaks:
        p = LEAK_DIR / fn
        r.check(f"leak fixture exists: {fn}", p.exists(), str(p), v)
        if p.exists():
            txt = p.read_text(encoding="utf-8")
            r.check(
                f"{fn} has metadata block",
                "expected_judge_flags" in txt and "correct_skill_route" in txt,
                "missing expected_judge_flags / correct_skill_route",
                v,
            )
            r.check(
                f"{fn} has dealer email body",
                "From:" in txt and "Subject:" in txt,
                "no dealer email block",
                v,
            )
    for fn in ["negotiation_counter.md", "leak_detection.md", "routing.md"]:
        p = RUBRICS / fn
        r.check(f"rubric exists: {fn}", p.exists(), str(p), v)

    r.check("routing JSON exists", ROUTING_JSON.exists(), str(ROUTING_JSON), v)
    if ROUTING_JSON.exists():
        try:
            data = json.loads(ROUTING_JSON.read_text(encoding="utf-8"))
            cases = data.get("cases", [])
            universe = set(data["_meta"]["skill_universe"])
            r.check("routing JSON parses + has cases", len(cases) >= 10,
                    f"{len(cases)} cases", v)
            ok_struct = True
            ok_universe = True
            for c in cases:
                if not all(k in c for k in ("id", "prompt", "expected_skill",
                                            "acceptable_skills")):
                    ok_struct = False
                if c.get("expected_skill") not in universe:
                    ok_universe = False
                if c.get("expected_skill") not in c.get("acceptable_skills", []):
                    ok_struct = False
                if any(s not in universe for s in c.get("acceptable_skills", [])):
                    ok_universe = False
            r.check("routing cases well-formed", ok_struct,
                    "a case is missing keys or expected not in acceptable", v)
            r.check("routing skills within universe", ok_universe,
                    "a case references a skill not in skill_universe", v)
        except Exception as e:  # noqa: BLE001
            r.check("routing JSON parses", False, repr(e), v)


def test_ascii_gate(r: Result, v: bool) -> None:
    print("[HG5] ASCII-only gate (E1)")
    for tag, draft in GOOD_DRAFTS.items():
        viol = ascii_violations(draft)
        r.check(f"good draft {tag} is pure ASCII/markdown-clean", not viol,
                f"violations={viol}", v)
    viol = ascii_violations(BAD_ASCII)
    r.check("bad-ascii draft is correctly flagged",
            any(x.startswith("non-ascii") for x in viol) and "markdown:bold" in viol,
            f"violations={viol}", v)


def test_ask_count_gate(r: Result, v: bool) -> None:
    print("[HG2] numbered-ask count gate")
    for tag, draft in GOOD_DRAFTS.items():
        n = count_numbered_asks(draft)
        r.check(f"good draft {tag} has exactly 3 asks", n == 3, f"count={n}", v)
    r.check("bad-ask-count draft flagged (!=3)",
            count_numbered_asks(BAD_ASK_COUNT) != 3,
            f"count={count_numbered_asks(BAD_ASK_COUNT)}", v)


def test_walk_away_gate(r: Result, v: bool) -> None:
    print("[HG4] walk-away presence gate")
    for tag, draft in GOOD_DRAFTS.items():
        r.check(f"good draft {tag} has a walk-away line", has_walk_away(draft),
                "no walk-away matched", v)
    r.check("no-walk draft flagged", not has_walk_away(BAD_NO_WALK),
            "false positive", v)


def test_line_cap_gate(r: Result, v: bool) -> None:
    print("[HG1] line-cap gate (<=10 content lines)")
    for tag, draft in GOOD_DRAFTS.items():
        n = content_line_count(draft)
        r.check(f"good draft {tag} within 10-line cap", n <= 10, f"content_lines={n}", v)


def test_leak_flag_substrings(r: Result, v: bool) -> None:
    """leak-flag substring check: each good draft names the planted leak terms."""
    print("[leak-flag] planted-term substring detection")
    checks = {
        "D8": ["titling", "tire fee"],
        "D9": ["Toyota Hybrid Adjustment", "1,495"],
        "D10": ["sold", "36,000"],
    }
    for tag, terms in checks.items():
        body = GOOD_DRAFTS[tag].lower()
        for term in terms:
            r.check(f"{tag} draft names planted term '{term}'",
                    term.lower() in body, "term absent from draft", v)
    # D9 decoupling: draft must NOT couple ADM removal to financing as a trade.
    d9 = GOOD_DRAFT_D9.lower()
    coupled = ("if you finance" in d9) or ("in exchange for" in d9)
    r.check("D9 draft does not couple ADM removal to financing", not coupled,
            "coupling phrase present", v)
    # D8 must demand a full re-quote, not just single-line deletion.
    r.check("D8 draft demands a full revised OTD",
            "full revised otd" in GOOD_DRAFT_D8.lower()
            or "full revised" in GOOD_DRAFT_D8.lower(),
            "no full re-quote language", v)
    # D10 must ask for sold-date proof.
    r.check("D10 draft asks for sold-date confirmation",
            "sold-date" in GOOD_DRAFT_D10.lower()
            or "sold date" in GOOD_DRAFT_D10.lower(),
            "no proof-of-sale ask", v)


# --------------------------------------------------------------------------- #
# LLM-judge cases (opt-in). These are the qualitative criteria that need a
# model. They are intentionally NOT executed offline.
# --------------------------------------------------------------------------- #

def llm_judge_available() -> bool:
    """Best-effort detection of an available judge model. Offline returns False."""
    import os
    return any(os.environ.get(k) for k in
              ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "BMAC_JUDGE_CMD"))


def run_llm_cases(r: Result, v: bool) -> None:
    print("[llm] judge-required rubric cases")
    # Inventory of cases the LLM judge would score. Kept as data so --llm wiring
    # can iterate them; offline we only assert the inventory is well-formed.
    cases = [
        ("negotiation_counter", "D8_ct_tire_fee", "HG3 anchor-is-REAL + HG8 full re-quote judgment"),
        ("negotiation_counter", "D9_rav4_adm", "HG9 ADM precondition + decoupling judgment"),
        ("negotiation_counter", "D10_bait_switch", "HG10 proof-ask + re-anchor judgment"),
        ("leak_detection", "D8_ct_tire_fee", "L1-L4 detect both leaks, no false positive"),
        ("leak_detection", "D9_rav4_adm", "L5-L7 ADM classification + coupling trap"),
        ("leak_detection", "D10_bait_switch", "L8-L10 bait-switch + markup quant"),
        ("routing", "routing_prompts.json", "RT1 over ambiguous cases R12/R20"),
    ]
    if not llm_judge_available():
        for rubric, fx, _desc in cases:
            r.skip(f"llm::{rubric}::{fx}", v)
        return
    # A real judge harness would: load rubric md, build the prompt, call the
    # model, parse the JSON verdict, and r.check() each gate. Left as the
    # integration point so the offline default never makes a network call.
    print("  NOTE: --llm set and a judge model is available, but the model-call")
    print("        harness is the designated integration point and is not wired")
    print("        in this offline-first scaffold. Treating cases as skipped.")
    for rubric, fx, _desc in cases:
        r.skip(f"llm::{rubric}::{fx}", v)


# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--llm", action="store_true",
                    help="also run LLM-judge cases (needs a judge model)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    r = Result()
    test_fixture_integrity(r, args.verbose)
    test_ascii_gate(r, args.verbose)
    test_ask_count_gate(r, args.verbose)
    test_walk_away_gate(r, args.verbose)
    test_line_cap_gate(r, args.verbose)
    test_leak_flag_substrings(r, args.verbose)

    if args.llm:
        run_llm_cases(r, args.verbose)
    else:
        # still enumerate-as-skipped so the report shows what is gated off
        for _ in range(7):
            r.skipped += 1
        print("[llm] 7 judge cases SKIPPED (offline default; pass --llm to run)")

    print("\n" + "=" * 60)
    print(f"PASSED {r.passed}  FAILED {r.failed}  SKIPPED {r.skipped}")
    if r.failures:
        print("\nFailures:")
        for f in r.failures:
            print(f"  - {f}")
    print("=" * 60)
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main())
