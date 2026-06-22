# Non-State Data Source Ledger

> **purpose**: Single audit trail for every *non-state* hard number the skill quotes as fact —
> CPO program limits, IRS / federal credit figures, manufacturer warranty terms, fee thresholds,
> etc. State-level tax / doc-cap / title / reg numbers live in `data/state_fees.json` (structured)
> and are audited separately by `scripts/check_freshness.py`; do NOT duplicate state rows here.
>
> **scope rule**: if a number is a *claim about the world that can go stale* (a dollar cap, a
> mileage limit, a rate, a date threshold) and it is **not** state-specific, it belongs here.
> Soft heuristics ("launch-year discount is typically $500-1,500") do NOT belong here — only
> verifiable, citeable figures.
>
> **Round 1 (this commit)**: schema + table headers only — NO data rows. Populate in Round 2.
> **Round 2**: fill the Brand / CPO and Federal-Credit tables row by row, each with a real
> statute citation or source URL and a `verified_date`. A row with no source MUST NOT be added.

## Ledger schema (one fact per row)

Every row in every table below uses the same three load-bearing columns:

| column | meaning |
|---|---|
| **value** | the exact figure as quoted (include units / currency / the year it applies to) |
| **statute \| URL** | authoritative source: a statute / IRS publication cite, OR a stable source URL. Prefer primary (gov / OEM) over secondary. |
| **verified_date** | ISO `YYYY-MM-DD` the value was last web-confirmed against the cited source |

Conventions:
- One fact per row. Do not pack a range and a cap into one row — split them.
- `value` must be self-describing out of context (e.g. `7yr/100k mi from original in-service date`, not just `100k`).
- If a figure is CPI-indexed or scheduled to change, note the next change in `value` (e.g. `$9,000 (2025; +$1k/yr to uncapped 2029)`).
- A fact that becomes stale stays in the table; bump its `verified_date` and `value` on re-confirm rather than deleting history-bearing context.
- Freshness target: re-verify each row at least every 12 months (same window as the state dataset). Rows whose `verified_date` is older than that should be re-checked before being quoted in a live deal.

---

## 1. Brand CPO Programs (non-state)

Coverage terms, age/mileage eligibility caps, and deductible figures per OEM CPO program.
Cross-reference the per-brand reference files (`*_cpo_program.md`) — this table is the
quick-audit ledger of the *hard numbers* in those files.

| brand / program | fact | value | statute \| URL | verified_date |
|---|---|---|---|---|
| <!-- e.g. Toyota TCUV | powertrain warranty | 7yr/100k mi from original in-service date | toyotacertified.com/... | YYYY-MM-DD --> | | | |

> R1: headers only. R2: one row per CPO hard number (eligibility age cap, mileage cap,
> comprehensive-warranty term, powertrain term, deductible, roadside term) for each brand
> already documented in the `*_cpo_program.md` references.

## 2. Federal & IRS Figures (credits, deductions, thresholds)

EV/clean-vehicle credits, MSRP caps, income (MAGI) limits, and any other federal dollar
thresholds the skill cites. These change by tax year — pin the year in `value`.

| program | fact | value | statute \| URL | verified_date |
|---|---|---|---|---|
| <!-- e.g. Clean Vehicle Credit (new) | max credit | $7,500 (2025 tax year) | IRC §30D / irs.gov/... | YYYY-MM-DD --> | | | |
| <!-- e.g. Used Clean Vehicle Credit | sale-price cap | $25,000 (2025) | IRC §25E / irs.gov/... | YYYY-MM-DD --> | | | |

> R1: headers only. R2: populate from the EV buyer playbook (`ev_buyer_playbook.md`) — new-credit
> amount, used-credit amount, MSRP caps (car vs SUV/truck), MAGI limits (single / HoH / MFJ),
> point-of-sale transfer rules, and any sunset dates.

## 3. Other Non-State Hard Numbers

Catch-all for citeable figures that are neither state-specific nor brand-CPO nor federal-credit:
e.g. nationally-standard fee structures, federal safety-recall lookup thresholds, lender/finance
regulatory limits, manufacturer base-warranty terms (bumper-to-bumper / powertrain) quoted as fact.

| topic | fact | value | statute \| URL | verified_date |
|---|---|---|---|---|
| <!-- e.g. New-car base warranty (Hyundai) | powertrain | 10yr/100k mi | hyundaiusa.com/... | YYYY-MM-DD --> | | | |

> R1: headers only. R2: populate only as the skill begins quoting specific non-state figures
> elsewhere; keep this table lean — promote a fact here only when it is actually cited as ground truth.

---

## Maintenance

- Audited alongside the state dataset on the annual refresh cadence (see `data/state_fees.json` `_meta`
  and `scripts/check_freshness.py`).
- When you add or re-verify a row, set `verified_date` to the date you confirmed it against the cited
  source — not the date you copied it from another doc.
- If you cannot find a primary source for a number, do not add it; flag it for verification instead.
