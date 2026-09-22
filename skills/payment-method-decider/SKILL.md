---
name: payment-method-decider
description: Use to choose the right payment method (cashier's check, debit, credit card, financing, lease) for a car purchase given buyer's specific situation (card rewards, dealer POS limits, financing pre-approval, captive vs CU). Triggers include "cash or CC for car", "Visa for $30k purchase", "crypto cashback card rewards", "dealer POS limit", "Chase Sapphire car purchase", "支付方式", "买车用刷卡还是支票", and Spanish phrases "metodo de pago para el carro", "pago el carro con tarjeta o con cheque de caja".
---

# Payment Method Decider

Compare the buyer's authorized payment options using written dealer and issuer
terms. Payment method can change price, incentives, fees and borrowing costs.
Retain the buyer's preference; do not switch to financing or a lease silently.
Keep internal `walk_away`, maximum monthly payment and account details private.

## Inputs

Use known information first and obtain only missing terms:

- Complete same-vehicle OTD for each payment method, with conditional incentives.
- Dealer's accepted instruments, aggregate and per-transaction card limits,
  surcharge/fixed fees, settlement requirements and verified payee details.
- Issuer's actual eligible purchase categories, reward rate, remaining cap,
  treatment of surcharges, attainable redemption value and exclusions.
- Available credit/funds, statement/grace-period terms and ability to pay in full.
- For borrowing: principal, down payment, note interest rate, disclosed APR,
  payment schedule, term, fees, prepayment terms and dated payoff conditions.

There is no universal PCI card transaction cap, dealer surcharge or card-brand
reward rate. A car intended for travel does not become travel-category spending.
ACH is a transfer method, distinct from a wire and from an auto loan.

## Card comparison

For the eligible card portion, let `C` be the amount before the card surcharge,
`S` the actual surcharge and `R` the attainable incremental reward. Compare:

```text
incremental_cost = S + card_interest + other_incremental_costs
                   - R - incremental_bonus - avoided_baseline_payment_fee
```

`R` must use the issuer's actual eligible base and remaining cap. If an uncapped
flat rate `r` applies only to `C`, then `R = r*C`. If the entire charged total
earns rewards, `R = r*(C+S)`. For a pure surcharge `S=s*C`, break-even rewards are
`r=s` in the first case and `r=s/(1+s)` in the second. Equal headline rates are
therefore not automatically break-even. Fixed fees, caps, exclusions, financing
interest and reward valuation can change the answer.

Count only a bonus caused by this purchase that the buyer would otherwise miss.
Do not value all points at an optimistic transfer redemption or assume reward
eligibility from a card name. A collateral-backed reward product also requires
its actual fees, liquidity and collateral risks in the comparison.

## Financing comparison

Use the actual lender schedule whenever available. For a fixed-rate, level-payment,
fully amortizing monthly loan with principal `P`, contractual monthly rate `i`
and `n` payments, the unrounded payment is:

```text
M = P*i / (1 - (1+i)^(-n))      when i > 0
M = P/n                       when i = 0
```

This assumes regular monthly periods. Use the note rate for `i`, not a disclosed
APR that already includes fees. Daily-simple-interest contracts, irregular first
periods, balloon amounts and cents rounding require the actual schedule/payoff.

Compare each option's down payment, unfinanced fees and scheduled payments at the
same ownership horizon. A rebate already deducted from the principal must not be
subtracted again. There is no fixed conversion from a rebate dollar amount to
basis points. A refinancing plan is conditional on actual future approval, fees,
payoff, rate availability and any rebate clawback; never assume a waiting period.

## Affordability and choice

At a fixed `i` and `n`, the principal supported by a private monthly limit `Mmax` is
`Mmax*(1-(1+i)^(-n))/i`, or `Mmax*n` at zero interest. Reconcile down payment,
net trade equity and other financed amounts to the full OTD. Compare that private
limit with the buyer's private OTD maximum; a lower monthly payment from a longer
term does not by itself make the vehicle cheaper.

Recommend an option only when the written terms make its cost and feasibility
clear. If terms are missing, return a conditional comparison with the missing
inputs. Do not initiate a loan, credit-limit change, wire, card transaction or
external communication without the user's authorization.

Use `../orchestrator/references/payment_methods.md` for cash-flow accounting and
`../lease-vs-cash-analyzer/SKILL.md` for lease comparisons. The purchase OTD
calculator does not establish lender terms or lease tax treatment. Store real
quotes, account details and calculations only in private companion data through
`tools/runtime_paths.py`.

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
