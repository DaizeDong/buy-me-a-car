# Non-State Data Source Ledger

> **purpose**: Single audit trail for every *non-state* hard number the skill quotes as fact ,
> CPO program limits, IRS / federal credit figures, manufacturer warranty terms, fee thresholds,
> etc. State-level tax / doc-cap / title / reg numbers live in `data/state_fees.json` (structured)
> and are audited separately by `scripts/check_freshness.py`; do NOT duplicate state rows here.
>
> **scope rule**: if a number is a *claim about the world that can go stale* (a dollar cap, a
> mileage limit, a rate, a date threshold) and it is **not** state-specific, it belongs here.
> Soft heuristics ("launch-year discount is typically $500-1,500") do NOT belong here, only
> verifiable, citeable figures.
>
> **Round 1 (this commit)**: schema + table headers only, NO data rows. Populate in Round 2.
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
- One fact per row. Do not pack a range and a cap into one row, split them.
- `value` must be self-describing out of context (e.g. `7yr/100k mi from original in-service date`, not just `100k`).
- If a figure is CPI-indexed or scheduled to change, note the next change in `value` (e.g. `$9,000 (2025; +$1k/yr to uncapped 2029)`).
- A fact that becomes stale stays in the table; bump its `verified_date` and `value` on re-confirm rather than deleting history-bearing context.
- Freshness target: re-verify each row at least every 12 months (same window as the state dataset). Rows whose `verified_date` is older than that should be re-checked before being quoted in a live deal.

---

## 1. Brand CPO Programs (non-state)

Coverage terms, age/mileage eligibility caps, and deductible figures per OEM CPO program.
Cross-reference the per-brand reference files (`*_cpo_program.md`), this table is the
quick-audit ledger of the *hard numbers* in those files.

| brand / program | fact | value | statute \| URL | verified_date |
|---|---|---|---|---|
| Stellantis SPOTiCAR | top-tier age cap | 5 model years or newer | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | top-tier mileage cap | under 75,000 mi | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | CPO Go age range | 6 to 10 model years old | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | CPO Go mileage range | 75,001-120,000 mi | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | program outer age bound | no more than 10 model years old | https://www.fcacertified.com/ (corroborated: kbb.com/cpo/stellantis-certified-pre-owned-program/) | 2026-06-22 |
| Stellantis SPOTiCAR | program outer mileage bound | maximum 120,000 mi | https://www.fcacertified.com/ (corroborated: kbb.com/cpo/stellantis-certified-pre-owned-program/) | 2026-06-22 |
| Stellantis SPOTiCAR | inspection | 125-point certified inspection | https://www.spoticar.com/ (corroborated: kbb.com/cpo/stellantis-certified-pre-owned-program/) | 2026-06-22 |
| Stellantis SPOTiCAR | powertrain warranty term | 7yr/100k mi from original in-service date | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | comprehensive (Maximum Care) layer | 3 months / 3,000 mi from CPO sale or factory-basic expiry (whichever more beneficial) | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | powertrain deductible | $0 | https://www.kbb.com/cpo/ram-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | roadside / towing benefit | $100 per occurrence (overage buyer's cost), 24hr | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | car rental allowance (Stellantis/KBB) | up to $45/day, $225 max per occurrence | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | car rental allowance (Ram-brand variant) | up to $35/day, $175 max per occurrence | https://www.kbb.com/cpo/ram-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | powertrain warranty transfer fee | $150, one-time transfer to subsequent owner | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | warranty-upgrade mileage gate | <=74,999 mi to add a Certified Upgrade plan | https://www.kbb.com/cpo/stellantis-certified-pre-owned-program/ | 2026-06-22 |
| Stellantis SPOTiCAR | embedded value, top-tier unit | ~$1,000-$1,800 (derived from Mopar/FlexCare quote data, NOT an OEM list figure) | https://www.consumeraffairs.com/automotive/mopar-extended-warranty.html | 2026-06-22 |
| Stellantis SPOTiCAR | embedded value, CPO Go unit | ~$300-$800 (powertrain largely consumed by age/mileage) | https://www.consumeraffairs.com/automotive/jeep-grand-cherokee-extended-warranty.html | 2026-06-22 |
| Stellantis SPOTiCAR | Mopar/FlexCare Maximum Care separate-buy cost | ~$1,500-$2,900 typical; up to ~$5,000 max term/mileage (8yr/125k) | https://www.buymoparwarranty.com/blog/mopar-max-care-warranty-review-coverage-cost-and-common-questions/ | 2026-06-22 |
| Stellantis SPOTiCAR | Mopar Vehicle Protection eligibility ceiling | not available at 80,001+ mi (hard ceiling for OEM extended warranty) | https://www.consumeraffairs.com/automotive/mopar-extended-warranty.html | 2026-06-22 |
| Lexus L/Certified | eligibility age cap | max 6 model years (current MY + 6 prior) | https://www.kbb.com/cpo/lexus-certified-pre-owned-program/ | 2026-06-22 |
| Lexus L/Certified | eligibility mileage cap | under 80,000 mi | https://www.kbb.com/cpo/lexus-certified-pre-owned-program/ | 2026-06-22 |
| Lexus L/Certified | inspection | 161-point certified inspection | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus L/Certified | comprehensive warranty term | 2yr/unlimited mi from later of (factory 4yr/50k basic expiry) or (L/Certified purchase date) | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus L/Certified | total stacked coverage | up to 6yr/unlimited mi (4yr/50k factory + 2yr/unlimited L/Certified) | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus L/Certified | deductible | $0 | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus L/Certified | complimentary maintenance | 4 factory-recommended services over 2yr/20,000 mi from purchase | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus L/Certified | trip interruption | up to 3 nights @ $200/night + rental $50/day up to 5 days | https://www.lexus.com/lcertified/certification-warranty | 2026-06-22 |
| Lexus Extra Care Platinum VSA (embedded-$ benchmark) | 6yr/100k discount-dealer price | approx $1,955 ($0 deductible; $2,800-$4,450 at finance office) | https://www.consumeraffairs.com/automotive/lexus-extended-warranty.html | 2026-06-22 |
| Lexus L/Certified | embedded value (vs Lexus Platinum VSA benchmark) | approx $1,500-$2,500 (Lexus-specific; NOT cross-applied) | https://www.lexusfinancial.com/content/dam/tmcc-webcommons/lexusfinancial/documents/vehicle-protection-plan/vehicle-service-agreement/19-010%20LFS%20VSA%20Platinum%20eBrochure%20(v7).pdf | 2026-06-22 |
| Genesis CPO | eligibility age cap | 5 model years or newer (2026 program: MY2022-2026) | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | eligibility mileage cap | fewer than 60,000 mi | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | inspection | 191-point mechanical/safety/appearance inspection | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | comprehensive (limited) warranty | 6yr/75,000 mi from original in-service date (+1yr/15k over factory 5yr/60k B2B) | https://www.kbb.com/cpo/genesis-certified-pre-owned-program/ | 2026-06-22 |
| Genesis CPO | powertrain warranty | 10yr/100,000 mi from original in-service date (reinstated for CPO/2nd owner) | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | powertrain deductible | $50 per repair visit | https://www.genesis.com/content/dam/genesis/us/pdf/GenesisCertified_Limited-Warranty-Form.pdf | 2026-06-22 |
| Genesis CPO | roadside assistance term | 10yr / unlimited mileage, 24/7/365 | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | rental car reimbursement | up to $50/day for up to 10 days (incl. 1st-day rental) | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | trip interruption | up to $100/day, up to $500/occurrence (breakdown 150+ mi from home) | https://www.genesis.com/us/en/certified | 2026-06-22 |
| Genesis CPO | transferability | both comprehensive + powertrain transfer to next private owner | https://www.kbb.com/cpo/genesis-certified-pre-owned-program/ | 2026-06-22 |
| Genesis CPO | embedded value (est.) | ~$2,500-$3,500 (anchored to Genesis Protection Plan VSC factory extension ~$2,600 GV80 example + luxury 2x-4x repair multiplier; Genesis-specific, NOT borrowed) | https://www.consumeraffairs.com/automotive/genesis-extended-warranty.html | 2026-06-22 |
| Genesis CPO | 2nd-owner non-CPO powertrain haircut | non-CPO used Genesis powertrain drops to 5yr/60k (CPO reinstates 10yr/100k) | https://www.consumeraffairs.com/automotive/genesis-extended-warranty.html | 2026-06-22 |
| Acura Precision Certified | eligibility age cap | 6 yr from original in-service date | https://www.acuracertified.com/certified-preowned-benefits | 2026-06-22 |
| Acura Precision Certified | eligibility mileage cap | under 80,000 mi at delivery | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Precision Certified | inspection | 182-point certified inspection | https://www.acuracertified.com/certified-preowned-benefits | 2026-06-22 |
| Acura Precision Certified | powertrain warranty | 7 yr / 100,000 mi from original in-service date | https://www.acuracertified.com/certified-preowned-benefits | 2026-06-22 |
| Acura Precision Certified | limited (B2B) warranty | 2 yr / 100,000 mi (from NVLW expiry or sale date) | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Precision Certified | roadside assistance | 2 yr from purchase / 100,000 mi | https://www.acuracertified.com/certified-preowned-benefits | 2026-06-22 |
| Acura Precision Certified | deductible | $0 | https://www.acuracertified.com/certified-preowned-benefits | 2026-06-22 |
| Acura Precision Certified | first scheduled maintenance | free, within 1 yr / 12,000 mi | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Precision Used | eligibility age cap | 10 yr from original in-service date | https://acuranews.com/en-US/releases/release-77dfefa32c6016754f9052f7ef0131b9-new-acura-precision-used-expands-availability-of-certified-used-vehicles-to-up-to-10-years-old | 2026-06-22 |
| Acura Precision Used | eligibility mileage cap | none (no mileage restriction) | https://acuranews.com/en-US/releases/release-77dfefa32c6016754f9052f7ef0131b9-new-acura-precision-used-expands-availability-of-certified-used-vehicles-to-up-to-10-years-old | 2026-06-22 |
| Acura Precision Used | inspection | 112-point certified inspection | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Precision Used | limited + powertrain warranty | 6 mo / 7,500 mi (whichever first) | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Precision Used | roadside assistance | 1 yr / 12,000 mi | https://acuranews.com/en-US/releases/release-77dfefa32c6016754f9052f7ef0131b9-new-acura-precision-used-expands-availability-of-certified-used-vehicles-to-up-to-10-years-old | 2026-06-22 |
| Acura Precision Used | transferable | No (not transferable) | https://www.kbb.com/cpo/acura-certified-pre-owned-program/ | 2026-06-22 |
| Acura Care VSC (separate) | list price range | $1,500-$3,500+ (varies by model/mileage/deductible); exclusionary coverage | https://www.consumeraffairs.com/automotive/acura-extended-warranty.html | 2026-06-22 |
| Acura Care Certified Additional Coverage | max B2B extension | up to 9 yr / 150,000 mi | https://www.consumeraffairs.com/automotive/acura-extended-warranty.html | 2026-06-22 |

### UNVERIFIED CPO rows (flagged, do NOT quote as fact in a live deal until confirmed)

| brand / program | fact | status | note |
|---|---|---|---|
| Stellantis SPOTiCAR | canonical OEM "MSRP value of CPO" dollar figure | UNVERIFIED | Stellantis does not publish one; embedded-value ranges above are derived from Mopar/FlexCare quotes, not an OEM list price |
| Stellantis SPOTiCAR | CPO market premium (asking-price delta vs non-CPO same VIN) | UNVERIFIED | no reliable Stellantis-specific hard number found; use embedded-value range as anchor |
| Stellantis SPOTiCAR | exact rental allowance for Ram brand specifically | UNVERIFIED (conflicting) | $45/$225 (KBB Stellantis) vs $35/$175 (Ram-brand pages), confirm per VIN/brand at close |
| Lexus L/Certified | dedicated L/Certified hybrid-component term | UNVERIFIED | not confirmed on OEM page; federal/CA hybrid-battery warranty (8yr/100k base, 10yr/150k CA) applies separately on in-service date |
| Lexus L/Certified | fixed market premium over non-CPO same-VIN | UNVERIFIED | no citeable pin (anecdotally ~$1,000-$2,500); negotiation variable, not a ledger fact |
| Genesis CPO | CPO market price premium (CPO vs same-VIN non-CPO) | UNVERIFIED | KBB editorial says negotiate "below ~$1,000"; no published national program figure |
| Genesis CPO | separate EV HV-battery CPO coverage line | UNVERIFIED | not documented whether CPO reinstates a standalone 10yr/100k HV battery line for 2nd owner; do NOT assume Hyundai/Kia EV-CPO parity |
| Acura Precision Certified | embedded $ value | UNVERIFIED (analyst est.) | ~$1,800-$2,800 derived from Acura Care VSC pricing, NOT an OEM-published number; Acura-specific estimate |
| Acura Precision Used | embedded $ value | UNVERIFIED (analyst est.) | ~$300-$700 analyst estimate |
| Acura (both tiers) | market asking-price premium | UNVERIFIED (heuristic) | $1,000-$2,000 (Certified) / $300-$700 (Used) soft heuristic |

> R2: one row per CPO hard number (eligibility age cap, mileage cap,
> comprehensive-warranty term, powertrain term, deductible, roadside term) for each brand
> already documented in the `*_cpo_program.md` references.

## 2. Federal & IRS Figures (credits, deductions, thresholds)

EV/clean-vehicle credits, MSRP caps, income (MAGI) limits, and any other federal dollar
thresholds the skill cites. These change by tax year, pin the year in `value`.

| program | fact | value | statute \| URL | verified_date |
|---|---|---|---|---|
| <!-- e.g. Clean Vehicle Credit (new) | max credit | $7,500 (2025 tax year) | IRC §30D / irs.gov/... | YYYY-MM-DD --> | | | |
| <!-- e.g. Used Clean Vehicle Credit | sale-price cap | $25,000 (2025) | IRC §25E / irs.gov/... | YYYY-MM-DD --> | | | |

> R1: headers only. R2: populate from the EV buyer playbook (`ev_buyer_playbook.md`), new-credit
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
> elsewhere; keep this table lean, promote a fact here only when it is actually cited as ground truth.

---

## Maintenance

- Audited alongside the state dataset on the annual refresh cadence (see `data/state_fees.json` `_meta`
  and `scripts/check_freshness.py`).
- When you add or re-verify a row, set `verified_date` to the date you confirmed it against the cited
  source, not the date you copied it from another doc.
- If you cannot find a primary source for a number, do not add it; flag it for verification instead.
