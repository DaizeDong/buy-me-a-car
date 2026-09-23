---
name: otd-calculator
description: Compute an out-the-door (OTD) estimate or reverse a target OTD into a sales-price ceiling using verified, explicitly supported state rules. Triggers include "compute OTD", "OTD math", "what's my OTD", "reverse OTD to sale price", "算 OTD", "算总价", "calcula el precio final del carro", and "calcula el precio total con impuestos y cargos".
---

# OTD Calculator

Use the installed orchestrator's `../orchestrator/scripts/otd_calculator.py`. It resolves the real repository path through Windows junctions. State fees and tax rules come from `data/state_fees.json`; each reviewed field has its own source and effective scope.

The result is an **estimate** with explicit fee inputs. A successful calculation does not confirm a dealer offer or the legality/completeness of every fee. Ordinary in-state resident dealer purchases of passenger ICE vehicles are the supported transaction class. Check the current profile table below; an unsupported profile must produce an actionable refusal.

## Required inputs and gate

1. Confirm the state, transaction date, in-state dealer/resident context, passenger ICE vehicle, and whether this is an ordinary purchase. Lease, private-party, EV, commercial, exemption, rebate and new-resident branches need their own official calculation.
2. Obtain itemized sales price, separately stated doc charge, title and registration amounts. Include applicable plate/inspection/local fees, and classify their tax treatment before putting them in `--reg`; Michigan temporary-registration and electronic-filing charges belong in taxable additions. No average registration fee is assumed.
3. Classify additional charges explicitly: `--taxable-addons` versus `--addons` for independently verified nontaxable charges. Connecticut service and extended warranties must use `--warranty` because their rate is separate. Do not infer that warranties, accessories or dealer packages share one tax treatment.
4. Run the calculator. It validates the dataset, field sources, source-value consistency, dates and a three-month review window before using an enabled state profile. Missing or stale evidence stops calculation.
5. Keep gross OTD separate from the trade settlement. A trade allowance can change the tax base, while payoff changes the balance due. Neither cash down nor financing terms changes gross OTD.

Use `--sales PRICE --forward` for a forward estimate, or `--target TARGET` for a cent-safe sales-price ceiling. Supply `--state STATE --doc DOC --title TITLE --reg REG` in both modes. `--sale-price` is an alias of `--sales`. Use `--trade ALLOWANCE --trade-payoff PAYOFF` for a buyer-owned motor vehicle transferred to the same dealer in the same transaction. The allowance is the vehicle's gross value, not equity after payoff.

All amounts must be finite, nonnegative and have at most two decimal places. Reverse calculation returns the highest supported whole-cent sales price that stays within the target after tax rounding. If a higher price falls into an unresolved classification interval, the result says so. `--json` returns monetary values as decimal strings.

## State differences that must survive the calculation

- Maryland: 6.5% from July 1, 2025; doc charge is taxable and eligible trade reduces the base. Standard title is $200, and the verified dealer processing cap is $800. The dealer profile refuses residual tax bases below $640 because valuation/minimum rules need separate review. A universal minimum is not inferred from the fee-summary page.
- Texas: 6.25% motor vehicle tax with eligible trade credit. A separately stated documentary charge is excluded from this tax. Do not add a local general-sales-tax rate. The historical $225 figure is not represented as an unconditional statutory cap.
- Virginia: 4.15% of sales plus doc, minimum tax $75, no trade-in tax credit. The former $599 cap claim was unsupported.
- North Carolina: 3% highway-use tax includes the dealer administrative charge and eligible trade credit. The $2,000 commercial/RV maximum is not applied to an ordinary passenger car. The former $129 doc cap claim was unsupported.
- Illinois: the $10,000 trade limit applied in 2020 and 2021; full eligible trade credit returned January 1, 2022. The production trade-rule helper covers that rule, while the complete OTD profile remains unavailable until all necessary jurisdiction rules are encoded.
- Michigan: 6% includes doc charges and eligible trade credit capped at $12,000 in 2026. The statutory annual schedule is $5,000 in 2019 plus $1,000 per year; the limit ends in 2029. Temporary-registration and electronic-filing charges are taxable additions. The old fixed $230 doc cap is unverified and was removed.
- New Jersey: 6.625% includes doc charges and eligible trade credit. The profile requires `--condition used`; new vehicles need a separate Luxury and Fuel-Inefficient Vehicle Surcharge calculation and are refused.
- New York: 4% plus an explicitly supplied `--local` percentage for the purchaser's residence, including MCTD tax where applicable. Eligible trade is deductible. The `doc` input is only the separately stated reasonable title/registration application service, up to $175, which is exempt. A larger or differently described charge needs an itemized review.
- Connecticut: 6.35%, or 7.75% when vehicle price including doc and taxable vehicle additions exceeds $50,000 **before trade**. Service/extended warranties are separately entered with `--warranty`, remain taxable at 6.35%, and do not go in sales or taxable vehicle additions. If a warranty alone pushes the combined price over $50,000, the profile requires an itemized tax review because the reviewed sources do not explicitly resolve that classification. Reverse calculation respects the tax jump and excludes this review interval.

## Coverage table

“Unverified” means the stored legacy value must not be quoted as current fact. “Supported” refers to the scoped tax profile and still requires explicit fees and the runtime freshness gate. Reviewed fields carry their actual verification dates in JSON; a whole-state boolean is not evidence.

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

## Explicit custom arithmetic

An unsupported state must not fall back to generic arithmetic automatically. A user who specifically wants an estimate from externally supplied assumptions can use `--estimate --tax-rate PERCENT --doc-taxable yes|no --title TITLE --reg REG`. The output is labelled `unverified_custom_estimate`. This mode does not infer trade credits or apply state defaults.

The low-level Python functions `compute_otd(sales, doc, tax_rate, title, reg, addons=0)` and `reverse_otd(...)` preserve their argument signatures and return Decimal amounts. They implement generic sales-plus-doc algebra only. Production state work must use `compute_state_otd` / `reverse_state_otd`.

## Verification and sources

Run `python tools/make_fixtures.py --check` and `python -m unittest discover -s eval -p "test_*tax*.py"`, plus `eval/test_otd.py`, for deterministic validation. The generated [OTD cases](../../eval/golden/otd_cases.json) contain synthetic inputs and independent expected totals. Tests call production calculation and trade functions.

See [state fees and source evidence](../orchestrator/references/state_fees.md) and [state fee lookup](../state-fee-lookup/SKILL.md).

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
