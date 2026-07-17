# eval/, objective assertion harness

Pure-stdlib (`unittest`) eval harness for `buy-me-a-car`. **No third-party
dependencies**, no `pytest`, no network. Runs offline.

```bash
bash eval/run.sh        # runs every eval/test_*.py; exits non-zero on any failure
```

`run.sh` auto-detects a Python 3 interpreter (`python3` then `python`), runs
each `test_*.py` in this directory, and exits non-zero if any test fails or
errors.

You can also run a single file directly:

```bash
python eval/test_otd.py -v
python eval/test_data_integrity.py -v
```

## What is tested

### `test_otd.py`, OTD calculator math

Imports `skills/orchestrator/scripts/otd_calculator.py` directly and asserts:

- **Forward OTD to the cent** against frozen golden cases in
  `golden/otd_cases.json` (NJ, CA, TX, MD, OH, NC, NY, MI, VA, WA, FL, IL).
  Every input is sourced from `data/state_fees.json` verified values; the
  combined tax rate is computed as `state_base_rate + local_pct/100`, the same
  path the calculator and CLI use.
- **Reverse round-trip within +/-$0.01**: `reverse_otd(forward(sale)) == sale`
  for every golden case, plus an add-ons case.
- **Trade-in tax-credit semantics** (encoded from the prose formulas in
  `skills/otd-calculator/SKILL.md`, since the shipped calculator has no trade
  parameter):
  - granted states (e.g. NJ): trade reduces the taxable base;
  - **CA / KY / DC**: trade is IGNORED for tax (full price taxed);
  - **MI / IL**: trade credit is CLAMPED at the statutory cap read live from
    `state_fees.json` (`trade_credit.cap`: MI $9,000 for 2025, IL $10,000).
- **Doc-fee cap WARNING** fires from the CLI iff `doc > statutory cap`
  (over-cap warns; at/under-cap silent; no-cap states never warn). Includes an
  explicit MD anchor: MD cap is **$800**, so a $499 doc must NOT warn.

### `test_data_integrity.py`, CORE doc-cap regression net

This is the net that catches "the next MD", a `doc_cap` in
`data/state_fees.json` drifting out of sync with the prose humans/agent read.

Doc-fee caps are written in prose in several places:

| Surface | Where | Asserted how |
|---|---|---|
| (A) **canonical** | `state_fees.md` *All-State Summary Table* | HARD: JSON == (A), all 51 states |
| (B) | `otd-calculator/SKILL.md` "State quick rates" table | HARD: JSON == (B), all capped states present |
| (C) | `state-fee-lookup/SKILL.md` "All-state summary" table | HARD: JSON == (C) |
| (D) | `state_fees.md` detail stubs + cross-state rows (free prose) | NOT line-asserted (see below) |

- `TestCanonicalDocCaps` hard-asserts JSON `doc_cap` == the canonical (A) table
  for all 51 records, with an explicit `MD == $800` anchor.
- `TestSecondaryDocCapTables` hard-asserts the (B) and (C) SKILL.md doc-cap
  **tables** match JSON for every capped state. `IL $347` vs JSON `$347.26` is a
  whole-dollar display of cents and is absorbed by a $1 tolerance (not flagged).
- The free-prose detail stubs / cross-state rows (D) are deliberately **not**
  asserted line-by-line: nearly every such line legitimately cross-references
  *other* states' caps ("no NY $175 doc cap", "VA $599 cap", D8 leak lists), so
  a naive per-line scan is ~100% false positives. The three structured tables
  are the correct, low-noise regression surface.

**Negative control verified**: injecting `MD: doc_cap = 300` into the JSON makes
`test_data_integrity.py` fail with 3 failures (canonical table, MD anchor, both
SKILL.md tables), confirming the net actually bites.

### Pre-existing siblings (run by the same `run.sh`)

`run.sh` also discovers two test files authored alongside this harness:

- `test_routing.py`, skill trigger-conflict / README routing-table assertions.
- `test_rubric.py`, deterministic gates (ASCII-only, ask-count, walk-away,
  line-cap, leak-flag) for the non-deterministic negotiation skills; LLM-judge
  cases are opt-in via `--llm` and skipped offline by default.

## Round 2, doc_cap contradiction worklist

**Status as of 2026-06-22: none.** WI-2 reconciled the entire repo to the
verified MD cap of **$800** (effective 2024-07-01). Every doc-cap surface now
agrees with `data/state_fees.json`:

- (A) `state_fees.md` All-State Summary Table, all 51 states match JSON.
- (B) `otd-calculator/SKILL.md` quick-rates table, MD $800; all capped states match.
- (C) `state-fee-lookup/SKILL.md` summary table, MD $800; all capped states match.
- (D) `state_fees.md` MD detail stub, cross-state rows, quirks list, and the
  "MD = low-doc sweet spot" framing have all been updated to $800 (now correctly
  described as the *highest* cap in the DC corridor, above VA's $599).

The earlier known divergence (canonical table fixed to $800 while SKILL.md
tables and the detail stub still said $300/$499/$500) has since been fully
resolved across all files; the integrity test passes against the current tree.

If a future verification flips any `doc_cap` in the JSON, the (A)/(B)/(C)
hard assertions will fail until the corresponding tables are updated in lockstep
, that is the intended behavior. Any *new* contradiction surfaced by a later
run should be listed here for the next reconciliation round.

## Regenerating golden cases

`golden/otd_cases.json` is a **frozen baseline**, not a derived value, it
exists so a silent change in the calculator math or a JSON state value is
caught. Regenerate it deliberately only when such a change is intended:

```bash
python - <<'PY'
import sys, json
sys.path.insert(0, "skills/orchestrator/scripts")
import otd_calculator as o
specs = [("NJ",25000,499,0),("CA",25000,85,1.5),("TX",25000,150,0),
         ("MD",31000,800,0),("OH",24500,250,2.25),("NC",26000,129,0),
         ("NY",30000,175,4.5),("MI",28000,230,0),("VA",33000,599,0),
         ("WA",35000,200,4.05),("FL",32500,500,1),("IL",40000,347.26,1.25)]
fwd = []
for st, sale, doc, local in specs:
    rate = o.STATE_TAX_RATES[st] + local/100.0   # MUST match test path
    title, reg = o.STATE_DEFAULT_TITLE[st], o.STATE_DEFAULT_REG[st]
    r = o.compute_otd(sale, doc, rate, title, reg)
    fwd.append({"state":st,"sale":sale,"doc":doc,"local_pct":local,
                "title":title,"reg":reg,
                "expected_tax":round(r["tax"],2),"expected_otd":round(r["otd"],2)})
print(json.dumps(fwd, indent=2))
PY
```

Paste the result into the `"forward"` array of `golden/otd_cases.json`. Do NOT
add a pre-rounded combined `tax_rate` field back into the golden: rounding the
rate to e.g. `0.085` shifts half-cent boundary cases (NY, TX) by a cent. The
test derives the rate live from `base + local_pct/100`.
