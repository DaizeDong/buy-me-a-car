---
name: lease-vs-cash-analyzer
description: Use to compute lease structure (cap cost / money factor / residual / acquisition / disposition), compare lease total cost vs cash purchase, decide lease vs buy given buyer's ownership horizon, and check captive lender early-buyout policy. Triggers include "lease or buy", "lease 数学", "compute lease monthly", "money factor markup", "lease cash incentive", "lease vs cash break-even", and Spanish phrase "leasing o compra al contado".
---

# Lease vs Cash Analyzer

Compare complete written offers on the same vehicle, mileage and ownership
horizon. A low monthly payment alone does not establish a cheaper deal. Preserve
the buyer's chosen financing method and private affordability limits.

## Required inputs

- Agreed vehicle value, gross and adjusted capitalized cost, each incentive and
  cap reduction, and each financed/upfront fee.
- Residual dollar amount and its MSRP base, money factor, term, mileage allowance,
  payment dates, first-payment treatment and total due at signing.
- Applicable lease taxes from current jurisdiction/transaction evidence, with
  upfront, periodic and purchase-option taxes separated.
- Contractual acquisition/disposition/purchase fees, wear/mileage rules, security
  deposit/refund terms, and any incentive restrictions.
- Written cash or loan alternative, comparison horizon, estimated resale range,
  maintenance/insurance differences and an explicit discount-rate assumption.

Do not insert default lender waiting periods, residual percentages, money factors,
fee ranges or state lease-tax classifications. Missing terms remain unverified.

## Standard monthly lease formula

For a conventional level-payment lease, with adjusted cap cost `C`, residual `R`,
money factor `MF`, and `N` months:

```text
depreciation_component = (C-R)/N
rent_component = (C+R)*MF
base_monthly = depreciation_component + rent_component
```

Use the contract's adjusted cap cost, not the vehicle price before fees/credits.
Add taxes according to the actual lease rules; tax is not universally a rate
times the monthly payment. `MF*2400` is an approximate APR-style percentage
display convention, not an exact loan APR or proof of markup.

Check quoted buy-rate evidence for the exact lender, credit tier, vehicle,
region, term, mileage and date before alleging markup. For the same `C` and `R`,
the pre-tax monthly effect of a factor change is `(C+R)*delta_MF`.

## Compare cash flows over the same horizon

Use dated outflows/inflows, not a fixed "lease under three years, buy over six"
rule. Avoid counting the first payment twice when it is included in drive-off.
Include contractually applicable return charges, mileage/wear exposure,
maintenance and insurance differences. At the horizon, an owned vehicle has
resale value and possibly an outstanding payoff; a returned lease does not.

For an explicitly chosen per-period discount rate `d`:

```text
present_cost = sum(outflow_t/(1+d)^t) - sum(inflow_t/(1+d)^t)
```

Use equal periods and the same rate/basis across options. Include resale net of
loan payoff as an ownership inflow when modeling a sale. Show sensitivity to
resale and mileage assumptions; neither is a known future outcome.

## Early purchase and incentives

Request an official dated PURCHASE payoff directly from the lessor or its
authorized process. Early purchase payoff can include outstanding lease balance,
remaining contractual charges and fees. It is not the end-of-term residual.
Verify allowed timing, incentive clawbacks, taxes, purchase fees and title costs.

Compare drive-off, payments already made, official payoff, taxes/fees and any
financing costs against the written cash alternative. Do not subtract lease cash
a second time if it already reduced cap cost/payoff. A fixed incentive amount
does not guarantee savings. No lease or buyout is initiated without authorization.

Verify current incentives against official dated terms. Do not assume an "EV
credit" label proves a federal credit, OEM incentive, buyer eligibility or a
lessor pass-through. Keep claimed government credits separate from actual
contractual discounts until their basis is established.

## Output contract

Give the buyer the written inputs, reconstructed monthly calculation, due-at-signing
reconciliation, tax assumptions, horizon cash flows, uncertainty range and a
conditional verdict when terms are missing. Report early-buyout rules as verified,
unverified or unavailable with source dates. Keep `walk_away` and monthly ceilings
private. Save real worksheets and analysis only through the private runtime resolver.

See `../orchestrator/references/lease_playbook.md` and
`../orchestrator/references/payment_methods.md` for the calculation procedure.
The cash-purchase OTD calculator is not evidence of lease-tax support.

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
