# Lease Structure Playbook

Use a complete written worksheet and current contract terms. This reference
defines the calculation; it does not supply current lender programs, state tax
rules or a promise that leasing saves money.

## 1. Reconcile the quote

Collect the agreed vehicle value, itemized gross capitalized cost, each rebate/
cap reduction, adjusted cap cost, residual dollars and MSRP base, money factor,
term, mileage, monthly payment, tax method and due-at-signing breakdown.

```text
gross_cap_cost = agreed_vehicle_value + capitalized_fees_taxes_and_other_amounts
adjusted_cap_cost = gross_cap_cost - itemized_cap_reductions
```

Cash cap reduction, trade equity and manufacturer incentives are different
sources. Confirm which are conditional and which are already included. Do not
count a payment, tax, acquisition fee or incentive both upfront and in cap cost.
The contractual residual is a purchase-option input, not a guaranteed resale value.

## 2. Rebuild the standard payment

For a conventional level-payment money-factor lease:

```text
C = adjusted_cap_cost
R = contractual_residual
N = term_months
depreciation = (C-R)/N
rent = (C+R)*money_factor
base_monthly = depreciation + rent
```

Check the contract's rounding and payment dates. One-pay, irregular-payment or
other nonstandard leases may use different calculations; obtain the actual
schedule instead of forcing this formula onto them.

`money_factor*2400` expresses an approximate APR-style percentage convention.
It is not the actuarial APR of an equivalent loan. Compare the quoted factor
with verified current buy-rate terms for this exact program before alleging
markup. For fixed `C` and `R`, changing the factor by `delta_MF` changes pre-tax
monthly rent by `(C+R)*delta_MF`; include tax effects where applicable.

## 3. Verify tax and fee treatment

Lease taxation depends on jurisdiction, residency, transaction structure,
upfront payments, capitalized taxes and any later buyout. Do not infer it from
the cash-purchase rate or an old state table. Obtain current official guidance
and the lessor's itemized implementation. Keep unresolved discrepancies visible.

Separate acquisition, documentation, title/registration, periodic taxes,
security deposits, purchase-option fees, disposition and potential mileage/wear
charges. Ask whether a fee is paid upfront, financed, refundable or contingent.
Never assume a fee is waived, first payment is included, or a purchase option
eliminates every return-related charge without reading the contract.

## 4. Compare against purchase

Use the same vehicle, mileage and evaluation horizon. List every dated payment
for each option. If drive-off includes the first monthly payment, count only the
remaining payments separately. Include security-deposit refunds and applicable
return charges. For an owned vehicle at the horizon, use a resale range net of
any remaining loan payoff. Do not compare a lease return with a purchase that
ignores the asset still owned.

For a stated per-period discount rate `d` and matching time index `t`:

```text
present_cost = sum(outflows_t/(1+d)^t) - sum(inflows_t/(1+d)^t)
```

If using a zero discount rate, label the result undiscounted cash cost. Keep
maintenance, insurance and resale assumptions consistent. Do not separately add
"opportunity cost" after discounting if that double counts the same assumption.
Show how the conclusion changes under plausible resale/mileage ranges.

## 5. Early purchase payoff

Before recommending lease-then-buyout, obtain the current lessor's purchase
eligibility, required process and official dated purchase payoff. This differs
from an early-termination quote and from the residual payable at scheduled end.
The early payoff may contain outstanding depreciation, remaining contractual
charges, taxes and fees. Never assume that one payment makes the car purchasable
for the residual alone.

Compare:

```text
lease_to_purchase_cost = drive_off_paid + subsequent_lease_payments_paid
                         + official_purchase_payoff + additional_required_costs
                         - confirmed_refunds
```

Add later financing cash flows if the payoff will be borrowed. Include only
costs not already inside the payoff. Do not subtract a lease incentive again
when it already reduced cap cost or the balance. Obtain the alternative cash
purchase quote before making a savings claim; there is no universal minimum
incentive that makes the strategy worthwhile.

## 6. Program and risk checks

Verify incentive eligibility and source, expiration, stacking, loyalty, credit
tier and any clawback. A worksheet's "EV credit" label is not proof of a federal
credit or mandatory pass-through. Record government incentives and contractual
discounts separately until their legal/program basis is established.

For mileage purchases, security deposits, lease transfers, insurance/GAP and
total-loss terms, read the actual program and contract. Do not rely on brand-wide
fee/holding-period tables. A cash cap reduction and a refundable security deposit
have different loss and liquidity treatment.

## 7. Deliver and act

Return the reconciled worksheet, source dates, formulas, cash-flow comparison,
uncertainty ranges and missing terms. Missing payoff/tax evidence means the
lease-buyout recommendation is incomplete. Do not call the cash OTD calculator
for an unsupported lease branch and present its output as verified lease tax.

Retain the buyer's authorization boundaries for credit applications, signing,
payments and external messages. Keep maximum budget/monthly limits private;
outward offers use the separate approved-offer workflow. All real documents and
calculations belong under the private companion data resolver.
