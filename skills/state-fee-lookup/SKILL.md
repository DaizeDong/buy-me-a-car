---
name: state-fee-lookup
description: Look up reviewed tax rates, doc-fee limits, title fees, registration rules and trade credit for US states and DC, with explicit unknown fields and source verification. Triggers include "what's the doc fee in X", "NJ sales tax rate", "Texas DMV fees", "州的税率", "doc fee cap", "trade-in credit", and "cual es la tasa de impuesto del estado".
---

# State Fee Lookup

The public dataset covers 50 states and DC as a research index. Coverage does not mean all fields are verified or every tax mechanism is implemented. Do not answer from a legacy numeric value whose `field_provenance.status` is `unverified`.

## Lookup procedure

1. Resolve the vehicle's registration state and applicable transaction jurisdiction. Identify purchase versus lease, dealer versus private seller, vehicle/powertrain class, date, trade eligibility, exemptions and rebates.
2. Read the exact field in `data/state_fees.json` together with its provenance. For a reviewed field, verify that the saved value matches the cited source value, the source is official, the review date is not stale/future, and the transaction is within the recorded effective scope.
3. If the field is unverified, follow the official agency/statute link and verify that field. Record the actual date of review, the applicable effective period if known, and the narrow transaction scope. Never copy an old record's verification date into a new review.
4. For doc fees, distinguish a maximum from a disclosure rule, a finance-contract safe harbor, a filing fee or a typical dealer charge. Null plus unverified provenance means unknown. It does not mean unlimited.
5. For registration, quote the actual class/weight/term/locality/plate/powertrain formula or obtain the transaction-specific fee. The calculator requires explicit title and registration values.
6. Use the state calculator only when its profile supports the transaction and all required field evidence passes. Otherwise request an itemized dealer/DMV calculation.

`check_freshness.py` is a gate by default. `--report-only` allows a report containing unverified fields; malformed and empty data still fail. `--calculator` checks the enabled profiles' required tax fields. `--state XX` narrows the report. A passing profile check does not verify all other fields in that state.

## Reviewed field table

This table is generated from the JSON by `render_state_data.py --write-references`. `--check` detects drift across all three tax reference surfaces. Reviewed dates and applicability live with each field in JSON. Unverified legacy rates/fees are deliberately not printed here.

<!-- state-data:start -->
| State | Reviewed tax rate | Doc cap | Title | Registration | Trade credit | Calculator profile |
|---|---|---|---|---|---|---|
| AK | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AL | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AR | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| AZ | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CO | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| CT | 6.35%; 7.75% over $50,000 | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| DC | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| DE | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| FL | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| GA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| HI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| IA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| ID | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| IL | Unverified | Unverified | Unverified | Unverified | Full eligible allowance | unsupported |
| IN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| KS | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| KY | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| LA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MD | 6.5% | $800 | $200 | Unverified | Full eligible allowance | supported |
| ME | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MI | 6% | Unverified | Unverified | Unverified | Up to $12,000 (2026); annual schedule | supported |
| MN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MO | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MS | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| MT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NC | 3% | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| ND | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NE | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NH | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NJ | 6.625% | Unverified | Unverified | Unverified | Full eligible allowance | supported (used only) |
| NM | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NV | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| NY | 4% + supplied local rate | $175 | Unverified | Unverified | Full eligible allowance | supported |
| OH | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| OK | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| OR | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| PA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| RI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| SC | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| SD | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| TN | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| TX | 6.25% | Unverified | Unverified | Unverified | Full eligible allowance | supported |
| UT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| VA | 4.15% | Unverified | Unverified | Unverified | No tax credit | supported |
| VT | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WA | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WI | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WV | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
| WY | Unverified | Unverified | Unverified | Unverified | Unverified | unsupported |
<!-- state-data:end -->

## Source and calculation boundaries

Maryland's 6.5% rate and $200 standard title took effect July 1, 2025. The $800 processing-charge limit took effect July 1, 2024. Those are separate fields with separate statutes or official notices.

Illinois restored full eligible trade credit January 1, 2022. Michigan's credit cap changes by year: $12,000 in 2026 under its statutory schedule. Do not retain the old Illinois $10,000 or Michigan $9,000 constants.

New Jersey's supported profile is used-only until the separate new-vehicle surcharge is encoded. New York's tax-exempt doc treatment applies only to the qualifying separately stated registration/title service, at most $175; the local tax percentage must come from the purchaser's residence. Connecticut's $50,000 threshold applies before trade, and service/extended warranties retain the 6.35% rate. A warranty-only crossing of that threshold needs a separate review. These restrictions are calculation inputs, not optional footnotes.

The old Virginia $599, New Jersey $799 and North Carolina $129 doc caps had no supporting official field evidence and were removed. Cited rules require disclosure or itemization, but the review does not claim to have proved the absence of every potentially applicable limit. These fields remain unverified until that question is resolved.

[State reference and official sources](../orchestrator/references/state_fees.md) · [OTD calculator](../otd-calculator/SKILL.md).

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
