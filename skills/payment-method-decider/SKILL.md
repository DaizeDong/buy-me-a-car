---
name: Payment Method Decider
description: Use to choose the right payment method (cashier's check, debit, credit card, financing, lease) for a car purchase given buyer's specific situation (card rewards, dealer POS limits, financing pre-approval, captive vs CU). Triggers include "cash or CC for car", "Visa for $30k purchase", "crypto cashback card rewards", "dealer POS limit", "Chase Sapphire car purchase", "支付方式", "买车用刷卡还是支票", and Spanish phrases "metodo de pago para el carro", "pago el carro con tarjeta o con cheque de caja".
---

# Payment Method Decider

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 3B sub-skill split from orchestrator)

Narrow helper for picking the payment instrument at close. Use when buyer asks "should I pay by X" or when dealer pushes a specific payment channel. Payment method is load-bearing for OTD math and CANNOT be silently swapped.

## When To Use

- Buyer asks "should I use credit card vs cashier's check"
- Card-rewards math (3% crypto-backed cashback, Amex, CSR, Citi DC) vs dealer surcharge
- Dealer claims POS card limit, buyer wants to push back
- Captive financing rebate vs credit union APR comparator
- Binding-constraint check on monthly cap vs OTD ceiling
- Lease cash / lease cap cost reduction routing

## When NOT To Use

- General OTD math without payment-method dimension - use `otd-calculator`
- Lease structure end-to-end - use `lease_playbook.md` first
- After purchase paperwork - use `close-day-checklist`

## Critical Rule

Payment method is LOAD-BEARING. Do NOT recommend financing to a cash buyer, or cashier's check to a buyer who wants card rewards. The buyer's chosen channel constrains:
- Dealer fees (some channels attach convenience fee)
- Effective OTD
- Negotiation leverage (cash often weaker than financing for back-end)
- Reward capture timing

If buyer's stated channel doesn't match the deal math, FLAG explicitly in heads-up.

## Decision Matrix (Base Costs)

| Method | Cost | Clearing | Dealer Pref | Notes |
|--------|------|----------|-------------|-------|
| Cashier's check | $0-15 | 1-3 days | High | Buyer-side mint at credit union |
| Personal check | $0 | 5-10 days | Low | Often rejected for >$5k |
| Debit card | $0 | Instant | Medium | Daily limit usually $5-10k; call bank to lift |
| Credit card | 2-3% surcharge >$5k | Instant | Low-Medium | See card math below |
| ACH (bank wire push) | $0-25 | 1-3 days | Medium | Buyer-friendly |
| Wire transfer | $25-50 | Same day | High | Best for time-critical close |
| Cash | $0 | Instant | Lowest | IRS Form 8300 over $10k |

## Card-Specific Math (Top Cards in Circulation)

Surcharge baseline = 3% (dealer-typical above $5k).

| Card | Earn Rate | Effective Value | Net vs 3% Surcharge |
|------|-----------|------------------|---------------------|
| Crypto-backed cashback, high tier | 3% cashback all cats | 3.0% | BREAK EVEN |
| Crypto-backed cashback, mid tier | 2% cashback all cats | 2.0% | NET LOSS 1% |
| Amex Platinum | 1x non-bonused | ~1.0% (best redemption) | NET LOSS 2% |
| Chase Sapphire Reserve | 1x non-bonused | 1.5-2.25% (transfer partner) | NET LOSS 0.75-1.5% |
| Citi Double Cash | 2% flat | 2.0% | NET LOSS 1% |
| Bilt Mastercard | 1x non-bonused | ~1.25% | NET LOSS 1.75% |
| Capital One Venture X | 2x | ~2.0% | NET LOSS 1% |

### When CC Actually Wins

- Dealer offers card with NO surcharge AND has high POS limit (rare, volume dealers)
- Buyer holds a 3% cashback card AND dealer surcharge is exactly 3% (true break-even with float + sign-up bonus value)
- Buyer is chasing a sign-up bonus minimum spend (e.g., $4k MSR for $750 bonus = 18.75% effective on that portion, easily worth 3% surcharge)

### When CC Loses

- Any card with <3% effective rewards vs 3% surcharge
- Dealer surcharge >3% (e.g., 3.5-4% common at independents)
- Buyer cannot pay statement in full (interest eats reward)

## Dealer POS Limit Reality

- Standard PCI-compliance default: $5,000 max single CC transaction
- Volume franchise (Toyota/Honda/Ford): $10,000-25,000 with GM approval
- Full-price CC: rare, usually requires GM override + auto-attached surcharge
- "Split" trick: some buyers split across 2 cards or 2 transactions; dealer may allow if total still under their absolute cap

If dealer cites $5,000 and buyer wants more: push for written confirmation BEFORE signing other docs. Common dealer move: agree verbally, then refuse at finance office.

## Captive Financing vs Credit Union Comparator

Scenario: captive APR > CU APR, but $1,000-2,500 customer cash rebate available ONLY with captive financing.

### Math

```
extra_interest = (captive_APR - CU_APR) * loan_amount * (term_yr / 2)
                 [approximation; use amortization for precision]

If rebate >= extra_interest: captive wins
Else: CU wins, take rebate's value as opportunity cost
```

### Quick Heuristic

On $36k / 60 month loan:
- $10 of rebate offsets ~1 bp of APR delta
- So $2,000 rebate offsets ~200 bp (2.0%) of APR delta
- If captive is 7.49% vs CU 5.49% (200 bp gap) with $2k rebate: BREAK EVEN; pick by other factors
- If captive is 6.49% vs CU 5.49% (100 bp gap) with $2k rebate: CAPTIVE wins by ~$1k

### Refinance Escape

Take captive financing to capture rebate; refinance with CU after 60-90 days. Verify:
- No prepayment penalty in captive contract
- CU will refi same-day-old loans (most do)
- Captive doesn't have "rebate clawback" clause for early payoff (rare but exists)

## Binding-Constraint Math

When buyer states BOTH a monthly cap AND OTD ceiling, check which actually binds:

```
max_financeable = (max_monthly - 0) * (1 - (1 + APR/12)^(-n)) / (APR/12)
effective_OTD_ceiling = max_financeable + down_payment
```

Compare against buyer's stated OTD ceiling. If within $500, FLAG in heads-up: "monthly cap is the real binding constraint, not OTD ceiling."

### Worked Example

Buyer: $700/mo max, $5k down, OTD ceiling $42k, 60mo @ 5.49% APR.
- max_financeable = $700 * (1 - (1.004575)^-60) / 0.004575 = ~$36,200
- effective_OTD_ceiling = $36,200 + $5,000 = $41,200
- Buyer's stated $42k ceiling is NOT the binding constraint - $700/mo is.
- Must negotiate to OTD $41,200 or lower, OR raise monthly cap, OR extend term.

## Lease Cash / Lease Cap Cost Reduction

Some manufacturers offer $1,000-3,000 lease cash that flows through ONLY as cap cost reduction (not as down payment, not as rebate to buyer).

- If lessor captures §45W $7,500 commercial credit: monthly drops ~$104 over 60mo lease, ~$208 over 36mo
- Verify on lease worksheet: "EV lease credit" or "cap cost reduction - manufacturer"
- Do NOT let dealer pocket the $7,500 - it must show as cap reduction line

See `../orchestrator/references/lease_playbook.md` for full lease structuring.

## Heuristic Flowchart

1. Cash buyer, no rewards play -> cashier's check from CU
2. Cash buyer with 3% cashback card + 3% dealer surcharge -> CC up to dealer cap, cashier's check for remainder
3. Cash buyer chasing sign-up MSR -> CC for the MSR portion, cashier's check for rest
4. Financing buyer, manufacturer rebate available -> captive (with refi escape plan)
5. Financing buyer, no rebate, CU pre-approved at lower APR -> CU outright
6. Lease buyer -> follow lease_playbook.md, verify §45W pass-through

## Cross-References

- `../orchestrator/references/payment_methods.md` - full reference
- `../orchestrator/references/lease_playbook.md` § captive rules
- orchestrator Phase 1 Critical Rule: "Payment method is load-bearing"
- `otd-calculator` skill - for downstream OTD recomputation after method change

## Worked Example

A buyer wanting single-transaction Visa for ~$33k at a dealer.
- Action item 1: confirm dealer POS limit for single transaction (likely $5-10k cap, needs GM override for $30k+)
- Action item 2: confirm convenience fee rate (3% typical = ~+$1k on a $33k purchase)
- If 3% fee AND buyer holds a 3% cashback card: BREAK EVEN, deal goes through net-neutral on payment method
- If fee >3% OR card is not 3% cashback tier: split into card portion + cashier's check, or all cashier's check

## Voice Note

Do NOT silently change payment method between Phase 6 negotiation and Phase 9 close. If buyer said "cash" in Phase 1 and dealer pushes financing in Phase 9, FLAG as load-bearing change - rerun OTD with new assumptions.
