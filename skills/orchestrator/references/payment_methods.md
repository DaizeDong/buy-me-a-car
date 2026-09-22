# Payment Methods for Car Purchase

Choose among the buyer's authorized options using current written prices and
terms. There is no fixed savings range from changing payment method. Keep private
budget, account and financing-capacity information out of dealer-facing material.

## Instrument and settlement checks

| Method | Confirm before close |
|---|---|
| Cashier's check | Bank issuance fee/timing, exact legal payee, amount and dealer acceptance |
| Personal check | Dealer acceptance, clearance/delivery policy and funds availability |
| Debit card | Issuer authorization limits, dealer aggregate limit and applicable fee rules |
| Credit card | Accepted network, total permitted charge, surcharge, issuer eligibility and available credit |
| ACH | Transfer direction, bank/dealer support, settlement timing and account verification |
| Wire | Verified instructions through a trusted channel, fees, cutoff and receipt procedure |
| Loan | Written loan terms, approved vehicle, funding conditions, incentive eligibility and payoff terms |
| Lease | Complete lease worksheet, contract conditions and the buyer's authorized ownership plan |

Do not assume a card transaction limit is a PCI requirement. Do not split payments
to bypass a dealer's aggregate limit. A notice to an issuer is not a guarantee of
approval. Never describe an ACH transfer as a wire or assume it implies borrowing.
Check surcharge legality and network rules for the instrument and jurisdiction.
Do not recommend cash advances or a new financing obligation as a routine workaround
for a missing checkbook.

## Credit-card cost and rewards

Let `C` be the card-funded portion before card fees. Determine the actual surcharge
`S`, any additional fixed charge, whether the fee is added to the card charge,
and which parts earn rewards. Use the remaining reward cap, not the advertised
annual/monthly cap before existing spending.

For a single uncapped reward rate `r`:

```text
R = r*C          if only the purchase amount earns
R = r*(C+S)      if the full charged amount earns, including surcharge
```

For a capped/tiered program, calculate each eligible band separately and value its
actual redemption. For a points program, use a buyer-attainable cash-equivalent
value and disclose that assumption. Merchant coding is determined by the actual
transaction, not by what the buyer plans to use the car for.

Relative to the same purchase paid through the baseline method:

```text
delta = surcharge + card_interest + other_incremental_costs
        - incremental_rewards - incremental_bonus - avoided_baseline_payment_fee
```

Negative `delta` favors the card on cost; it does not prove acceptance or liquidity.
With a surcharge rate `s` and no other costs, break-even is `r=s` when fees earn
no rewards, and `r=s/(1+s)` when the full charge earns. If `r=s` and fees earn
rewards, the arithmetic reward on the surcharge creates a small nominal gain;
caps, fees, timing and exclusions can erase it. Do not label equal headline
rates automatically neutral.

Count a signup bonus only to the extent it is incremental, attainable and not
displaced from other planned spending. Include interest if the balance will not
qualify for a full grace-period payoff. Evaluate collateral-backed reward products
using their actual borrowing, collateral, conversion and redemption costs.

## Cash versus financed acquisition

Collect each complete offer independently: negotiated vehicle price, taxes,
fees, down payment, net trade equity, financed extras, lender principal, note
rate, disclosed APR, term, payment schedule and conditional rebates. A lower
APR with a different price is not automatically cheaper.

For a standard monthly fully amortizing loan, let `i` be the contractual monthly
interest rate, `P` principal and `n` number of payments:

```text
payment = P*i/(1-(1+i)^(-n))    for i > 0
payment = P/n                 for i = 0
unrounded_total_interest = n*payment - P
```

For a nominal annual note rate quoted as a decimal with monthly accrual, `i` is
that rate divided by 12. Disclosed APR can incorporate fees and is not necessarily
the rate used in this payment equation. Use the lender's actual schedule to
account for daily accrual, irregular periods, rounded payments and final payoff.

Over the full loan term, compare down payment plus unfinanced costs plus all
scheduled payments. Over a shorter horizon, include the remaining dated payoff
and the same resale/ownership assumption for each option. Rebate credited in
the purchase price or financed principal is already counted; do not subtract it
again. There is no universal dollar-to-basis-point rebate conversion.

Refinancing needs an official payoff, eligibility, new fees, actual new rate and
payment schedule. A dealer's reserve preference is distinct from a buyer's
contractual early-payoff or rebate-clawback obligation. Do not invent a required
holding period or treat future refinancing approval as guaranteed.

## Private affordability

For an equal-payment loan, the principal allowed by monthly limit `Mmax` is:

```text
Pmax = Mmax*(1-(1+i)^(-n))/i    for i > 0
Pmax = Mmax*n                 for i = 0
```

Translate principal to OTD using the actual down payment, net trade equity and
other financed amounts. If `OTD` excludes optional financed products and trade
settlement, the reconciliation is:

```text
principal = OTD - down_payment - net_trade_equity + other_financed_amounts
```

Check the contract's definitions before using this identity. Negative trade
equity increases the loan. The supported OTD limit and `walk_away` remain private;
only a separate user-authorized offer may be proposed externally.

## Lease then buyout

Use `lease_playbook.md`. Early purchase payoff is NOT automatically the residual.
Get a dated lessor purchase quote, allowed timing and all taxes/fees first.
Compare total outflows already paid plus the official payoff and remaining
costs with a written cash-purchase alternative. Incentives already reflected
in adjusted cap cost must not be counted again. There is no fixed lease-cash
threshold that guarantees this path saves money.

## Deliverable and authorization

Return a cost comparison with source dates, missing terms, timing assumptions,
and the buyer's chosen method. A method change requires an explicit decision;
do not quietly replace a cash plan with financing. Analysis does not authorize
money movement, credit applications or contact with banks/dealers. Keep all real
records under private companion data resolved by `tools/runtime_paths.py`.
