#!/usr/bin/env python3
"""CORE regression net: keep data/state_fees.json doc-fee caps consistent with
the prose that humans and the agent actually read.

Pure stdlib (no pytest). Run:  python eval/test_data_integrity.py

Design / why MD passes now
--------------------------
There are several places a per-state doc-fee cap is written in prose:

  (A) state_fees.md  ->  "All-State Summary Table"   == the CANONICAL prose table.
  (B) skills/otd-calculator/SKILL.md     "State quick rates" table.
  (C) skills/state-fee-lookup/SKILL.md   "All-state summary" table.
  (D) state_fees.md detail stubs + cross-state rows (free prose).

Round 1 (WI-2) reconciled the JSON cap with the CANONICAL table (A) for every
state, including MD ($800). So the HARD assertion below — JSON (A) — passes now
and will fail the instant the JSON cap and the canonical table diverge again.
That is the regression net that catches "the next MD".

As of this Round-1 pass, WI-2 also reconciled the secondary doc-cap TABLES in
(B) and (C) to $800 for MD (and they agree with JSON for every other capped
state too), so `scan_secondary_doc_mentions()` returns []. That scan therefore
runs as a HARD guard: any future drift in a SKILL.md doc-cap table (the most
likely place "the next MD" reappears) fails the suite. IL $347 vs $347.26 is a
pure whole-dollar display of cents and is absorbed by a $1 tolerance, not
flagged.

The free-prose detail stubs / cross-state rows (D) are intentionally NOT
asserted line-by-line: every such line legitimately cross-references OTHER
states' caps ("no NY $175 doc cap", "VA $599 cap", leak lists), so a naive
line scan is all false positives. The three structured tables are the correct
regression surface; see eval/README.md.
"""
import json
import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(REPO_ROOT, "data", "state_fees.json")
STATE_FEES_MD = os.path.join(REPO_ROOT, "skills", "orchestrator", "references", "state_fees.md")
OTD_SKILL_MD = os.path.join(REPO_ROOT, "skills", "otd-calculator", "SKILL.md")
SFL_SKILL_MD = os.path.join(REPO_ROOT, "skills", "state-fee-lookup", "SKILL.md")

STATE_RE = re.compile(r"^[A-Z]{2}$")
DOLLAR_RE = re.compile(r"\$([0-9][0-9,]*(?:\.[0-9]+)?)")
NONE_RE = re.compile(r"\bnone\b|no\s*cap|n/?a", re.IGNORECASE)


def load_json_caps():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {r["state"]: r.get("doc_cap") for r in data["states"]}


def _cell_to_cap(cell):
    """Map a doc-cap table cell to a numeric cap, None (no cap), or 'UNKNOWN'."""
    m = DOLLAR_RE.search(cell)
    if m:
        return float(m.group(1).replace(",", ""))
    if NONE_RE.search(cell):
        return None
    return "UNKNOWN"


def parse_doc_cap_table(path, header_match):
    """Parse the first markdown table whose header row satisfies header_match.

    Returns {state_code: raw_cap_cell_string} for rows keyed by a 2-letter code.
    The doc-cap column is located by header text containing 'doc'.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        if not header_match(line):
            continue
        header = [c.strip() for c in line.strip().strip("|").split("|")]
        doc_cols = [j for j, h in enumerate(header) if "doc" in h.lower()]
        if not doc_cols:
            continue
        ci = doc_cols[0]
        rows = {}
        for ln in lines[i + 2:]:  # skip the |---|---| separator row
            if not ln.strip().startswith("|"):
                break
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) <= ci:
                continue
            st = cells[0].replace("*", "").strip()
            if STATE_RE.match(st):
                rows[st] = cells[ci]
        return rows
    raise AssertionError(f"no doc-cap table found in {path}")


def canonical_summary_table():
    """(A) state_fees.md All-State Summary Table: header has 'Doc Fee Cap'."""
    return parse_doc_cap_table(STATE_FEES_MD, lambda l: "Doc Fee Cap" in l)


def _caps_equal(json_cap, prose_cap, dollars_tolerance=0.0):
    if prose_cap == "UNKNOWN":
        return False
    if json_cap is None or prose_cap is None:
        return json_cap == prose_cap
    return abs(float(json_cap) - float(prose_cap)) <= dollars_tolerance


def scan_secondary_doc_mentions():
    """Collect (surface, state, json_cap, prose_cap) mismatches on the secondary
    surfaces (B)+(C). IL $347 vs $347.26 is a pure display rounding and is NOT
    reported (tolerance $1). Returns a list of dict rows for the Round-2 list."""
    surfaces = {
        "otd-calculator/SKILL.md": parse_doc_cap_table(
            OTD_SKILL_MD, lambda l: "Doc cap" in l),
        "state-fee-lookup/SKILL.md": parse_doc_cap_table(
            SFL_SKILL_MD, lambda l: "Doc cap" in l),
    }
    json_caps = load_json_caps()
    out = []
    for surface, table in surfaces.items():
        for st, cell in table.items():
            jc = json_caps.get(st)
            prose = _cell_to_cap(cell)
            # $1 tolerance absorbs whole-dollar display of cents (IL 347.26->347)
            if not _caps_equal(jc, prose, dollars_tolerance=1.0):
                out.append({"surface": surface, "state": st,
                            "json_cap": jc, "prose_cap": prose,
                            "raw_cell": cell})
    return out


class TestCanonicalDocCaps(unittest.TestCase):
    """HARD net: JSON doc_cap == canonical state_fees.md summary table, all states."""

    @classmethod
    def setUpClass(cls):
        cls.json_caps = load_json_caps()
        cls.table = canonical_summary_table()

    def test_all_51_states_present_in_table(self):
        self.assertEqual(len(self.json_caps), 51, "JSON should hold 51 records")
        missing = [s for s in self.json_caps if s not in self.table]
        self.assertFalse(
            missing, f"states missing from canonical summary table: {missing}")

    def test_doc_cap_matches_canonical_table(self):
        mismatches = []
        for st, jc in self.json_caps.items():
            prose = _cell_to_cap(self.table[st])
            if not _caps_equal(jc, prose):
                mismatches.append((st, jc, prose, self.table[st]))
        self.assertFalse(
            mismatches,
            "JSON doc_cap disagrees with state_fees.md All-State Summary Table:\n"
            + "\n".join(
                f"  {s}: JSON={j!r} table={p!r} (cell={c!r})"
                for s, j, p, c in mismatches))

    def test_md_cap_is_eight_hundred_everywhere_canonical(self):
        """Explicit MD anchor — the bug class this whole file exists to catch."""
        self.assertEqual(self.json_caps["MD"], 800)
        self.assertEqual(_cell_to_cap(self.table["MD"]), 800,
                         "canonical MD summary-table cap drifted off $800")


class TestSecondaryDocCapTables(unittest.TestCase):
    """HARD guard on the SKILL.md doc-cap tables (otd-calculator, state-fee-lookup).

    These agreed with JSON after Round-1/WI-2, so the expected drift set is empty.
    If a SKILL.md table later drifts from JSON (the next 'MD'), this fails.
    """

    def test_skill_doc_cap_tables_match_json(self):
        drift = scan_secondary_doc_mentions()
        self.assertEqual(
            drift, [],
            "SKILL.md doc-cap table(s) disagree with state_fees.json:\n"
            + "\n".join(
                f"  {d['surface']} {d['state']}: JSON={d['json_cap']!r} "
                f"prose={d['prose_cap']!r} (cell={d['raw_cell']!r})"
                for d in drift))

    def test_skill_tables_agree_on_md_800(self):
        otd_tbl = parse_doc_cap_table(OTD_SKILL_MD, lambda l: "Doc cap" in l)
        sfl_tbl = parse_doc_cap_table(SFL_SKILL_MD, lambda l: "Doc cap" in l)
        self.assertEqual(_cell_to_cap(otd_tbl["MD"]), 800,
                         "otd-calculator SKILL.md MD doc cap not $800")
        self.assertEqual(_cell_to_cap(sfl_tbl["MD"]), 800,
                         "state-fee-lookup SKILL.md MD doc cap not $800")


if __name__ == "__main__":
    unittest.main(verbosity=2)
