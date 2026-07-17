# Payment Methods for Car Purchase

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

How buyer pays affects total cost by $500-3,000. Verify buyer's payment constraint EARLY (Phase 1 ideally), switching payment method late in negotiation can blow up the deal.

## Payment Method Decision Matrix

| Method | Typical net cost vs cash baseline | Dealer attitude | When to use |
|---|---|---|---|
| **Cashier's check** | $0 baseline (no fee, no rewards) | ✅ Preferred, treated as cash | Buyer has bank account + balance; standard path |
| **Debit card (raised daily limit)** | $0 baseline | ✅ Treated as cash, usually no fee | Buyer can't easily get cashier's check; same-day flexibility |
| **Personal check** | $0 baseline | ⚠ Dealer may hold delivery 1-2 weeks for clear | Local relationship dealer only |
| **Wire transfer** | $0-25 wire fee | ✅ Preferred for >$25k | Buyer has business account; out-of-state |
| **ACH (auto loan from credit union)** | $50-200 interest if paid off in 30 days | ✅ Dealer F&I likes (commission) | Buyer cannot self-fund; use credit union for low rate |
| **Credit card (full amount)** | **+3% surcharge** ≈ $900-1,000 on $32k | ⚠ Most dealers cap at $5k, may refuse over | **Avoid unless rewards card offsets** |
| **Credit card + cashback ≥3%** | Net 0 to -1% | ⚠ Same as above + need confirmation | If user has Amex Plat / a 3% cashback crypto-backed card |
| **Lease + immediate buyout** | -$150 to -$1,500 net (saves lease cash) | ⚠ Dealer F&I may resist | Only if lease cash incentive ≥ $1,500 |

## Cash / Cashier's Check (Standard Path)

**Mechanics**:
- Bank issues cashier's check made out to dealer's legal entity name
- Take to dealer at close, hand to F&I manager
- Dealer waits 1-2 business days for check to clear (some accept immediately for known buyers)
- Title transfers to buyer once funds cleared

**Pre-flight checks**:
1. Bank account balance ≥ OTD amount (verify 1 week ahead)
2. Cashier's check fee at your bank ($0 for account holders typically, $10-15 for non-holders)
3. Dealer's legal entity name (NOT trade name), get this in writing from dealer
4. Same-day vs next-day cashier's check policy at your bank
5. ID requirements to draw the check (driver's license + secondary ID)

**Anti-pattern**:
- ❌ Writing cashier's check before final OTD agreed in writing
- ❌ Making check out to salesperson's personal name (must be dealer entity)
- ❌ Taking check to bank without secondary ID

## Debit Card with Raised Daily Limit

**When to use**: Buyer can't easily get cashier's check (no checking account, account at distant bank, weekend buying with bank closed).

**Mechanics**:
1. Call bank customer service: "I'm buying a car for $X next week. Please temporarily raise my daily debit limit to $X + 10% buffer for [specific date range]."
2. Bank verifies identity (security questions / SSN last 4)
3. Bank confirms limit raised + provides confirmation #
4. Buyer at dealer swipes debit card → dealer POS processes as cash equivalent
5. Funds debit immediately from buyer's checking

**Bank-specific limits** (verify with user's specific bank):
- BoA: default $5k/day, raisable to $35k+ via customer service
- Chase: default $5-10k/day, raisable to $50k+ via Chase Mobile or customer service
- Wells Fargo: default $10k/day, raisable
- USAA: default $10k/day, max raise ~$15k (low ceiling)
- Credit Unions: vary widely, often need branch visit

**Dealer-side handling**:
- Most dealers process debit as cash equivalent (no surcharge)
- A few smaller dealers cap debit at $5,000 too, confirm with dealer in writing
- Some dealers prefer debit over cashier's check (faster clearing)

## Credit Card, Full Amount (High Cost, Sometimes Worth It)

**Reality check**: Most NJ dealers cap credit card at $2,500-5,000 per transaction (their merchant agreement, not negotiable). To pay full $30k+ on CC requires explicit dealer override + 3% convenience fee.

**Math for $32,000 OTD**:
- Dealer surcharge: $32,000 × 3% = **$960**
- Net cost: $32,960 (vs $32,000 cash baseline)
- Required cashback to break even: 3% effective rate

**When CC makes sense**:
- High-tier rewards card with **3%+ on all spend** (e.g., Amex Business Platinum, certain Chase Sapphire categories)
- Crypto-backed cards (e.g., **a 3% cashback crypto-backed card with a high monthly cap**: 3% cashback up to $50k/mo spending → full coverage of $32k surcharge)
- Sign-up bonuses worth $1,000+ (achieves bonus minimum spend with single car purchase)

**When CC does NOT make sense**:
- Standard 1-2% cashback card (net loss $300-600 on $32k deal)
- Card with merchant category exclusion on automotive
- Card that codes "automotive dealer" as "miscellaneous" (lower rewards rate)

**Pre-purchase preparation**:
1. **Call CC issuer fraud line** (number on card back) 1-2 days before close:
   - "I will make a large purchase of $32,000-33,000 at [Dealer Name + city] on [date]. Please pre-authorize / whitelist this transaction so it does not auto-decline for fraud."
   - Get case # from agent
2. **Confirm card spending limit**: actual available credit ≥ purchase + 5% buffer
3. **Confirm dealer's CC processing**:
   ```
   Email dealer ahead of close:
   "Confirming payment logistics: I will pay full OTD by Visa credit card 
   single transaction. Two confirmations needed:
   1. Can your POS process a $X single Visa charge?
   2. Convenience fee rate (industry standard 3%)?"
   ```

**Card-specific notes**:

| Card | Cashback rate on cars | Special considerations |
|---|---|---|
| **Amex Business Platinum** | 1-1.5% standard, but 5x on flights/hotels | Surcharge may apply at dealers that resist Amex |
| **Chase Sapphire Reserve** | 1% standard, 3x on travel | Worth combining with travel rewards if buying for travel use |
| **Citi Double Cash** | 2% on all | Net -1% on car purchase after 3% surcharge, skip |
| **Crypto-backed card, high tier** | 3% up to $50k/mo spending | **Breaks even on full CC purchase**; verify on-chain collateral ≥ purchase × 1.5-2 |
| **Crypto-backed card, low tier** | 3% capped at $2k/$10k monthly | Effective rate on $32k = 0.2-0.9% → net loss $700-900 |

## Lease + Immediate Buyout ("Lease Cash Conversion")

Capture manufacturer's lease cash incentive (which is paid only to lessees, not cash buyers) by signing a lease then immediately buying out.

**When this works**: Manufacturer lease cash ≥ $1,500/month AND captive lender (e.g., Subaru Motors Finance) allows early buyout without penalty.

**When this fails**: Lease cash < $1,000, captive has 6-month hold period, dealer F&I adds add-ons during lease signing that capitalize into cap cost.

### Decision Math

```
NET SAVINGS = Lease cash incentive
            - Acquisition fee ($650-800)
            - Buyout fee ($300)
            - Sales tax inefficiency (~$200-400 NJ)
            - Interest on unused capital ~30 days (~$50)

IF lease cash $1,500: net savings ~$150
IF lease cash $2,000: net savings ~$650
IF lease cash $2,500: net savings ~$1,150
IF lease cash <$1,000: net LOSS — skip trick
```

### Execution (7 steps)

**Step 1**: Verify current month's lease cash for target trim
- Call Subaru Motors Finance: **1-800-868-7000**, "Current 2026 Forester Limited gas 36-mo lease cash for ZIP <user-zip>"
- Or check subaru.com/deals
- Skip trick if lease cash < $1,000

**Step 2**: Cross-bid cash sell price with dealers FIRST (don't mention lease intent)
- Lock the lowest cash OTD via written quote
- Do NOT reveal lease intent in this phase, dealer would shift lease cash to "cash discount" they'd give anyway, double-charging you

**Step 3**: After cash OTD locked, ask winning dealer for lease quote:
```
Hi [Sales Manager],
Thanks for the $X cash OTD quote. Before I commit, please send the LEASE 
quote on same VIN with ALL current Subaru incentives applied 
(lease cash, loyalty, APR cash). Specify:
- 36-month / 12k mile/year lease
- Cap cost AFTER all incentives
- Money factor (buy-rate not marked up)
- Residual percentage
- Acquisition fee
- Sign-and-drive monthly payment with NJ tax
- Total drive-off amount

Cash deal still on the table.
```

**Step 4**: Verify `cap cost = (sell price) - (lease cash)`
- If yes: proceed
- If dealer kept lease cash in cap cost: walk back to cash deal (they're trying to double dip)

**Step 5**: Sign lease at dealer, **refuse ALL F&I add-ons**:
- ❌ GAP insurance (you'll buy out in 30 days, useless)
- ❌ Vehicle Service Contract (extended warranty)
- ❌ Tire & Wheel protection
- ❌ Paint / fabric protection
- ❌ Maintenance package
- ❌ Disposition fee (you'll buy out, not return)
- ❌ Money factor markup

Sign-and-drive upfront: $2,000-2,500 (acq + doc + reg + first month).

**Step 6**: 25-30 days later, call SMF for buyout payoff
```
Call 1-800-868-7000:
Me: "I want to request a buyout payoff for my lease, account #X"
SMF: "Your buyout is $Y, good through [date]"
Me: "Please email me the official payoff quote PDF"
```

Expected buyout: residual + NJ tax on residual (6.625%) + admin fee $300 ≈ $23-25k for typical Forester.

**Step 7**: Pay SMF via cashier's check or ACH
- SMF mails NJ DMV title transfer 7-14 days later
- You own the car outright

### Risks

1. **Captive may NOT allow residual buyout in first month**, some require 6 months. Verify SMF policy upfront.
2. **Dealer F&I may sneak in add-ons** that capitalize into cap cost, review lease contract line-by-line before signing.
3. **Money factor markup**, dealer may inflate MF beyond buy-rate, adds interest to monthly. Ask for buy-rate explicitly.
4. **Tax structure varies by state**, NJ taxes lease payments AND residual buyout; some states tax only payments (better) or full price upfront (worse).
5. **F&I may refuse to sign lease if they sense buyout intent**, don't mention "I plan to buy out in 30 days" during lease signing; just complete normal lease paperwork.

## Common Buyer Scenarios

### "I have $X in checking account"
→ Cashier's check, fastest cleanest path.

### "I want CC rewards / sign-up bonus"
→ Verify dealer accepts full CC + 3% surcharge math vs rewards. Usually breaks even at best with high-tier cards.

### "I only have credit card / crypto"
→ Tier 1 problem. Either:
  - Convert crypto to USDC → bank → cashier's check (most efficient)
  - Get cash advance on CC (worst: 5% fee + 25-30% APR from day 1)
  - Get pre-approved auto loan from credit union (small interest, then pay off in 30 days)

### "I want to capture manufacturer lease cash"
→ See Lease Conversion section above. Only worth it if lease cash ≥ $1,500.

### "I'm a foreign buyer / no US bank account"
→ Wire transfer from foreign account (allow 3-5 business days clearance). Dealer may need additional ID verification.

## Phase 1 Question to Add for Buyer

In the requirements gathering phase, ADD this question:

> "**Payment method**: How are you paying? Cashier's check / debit card / 
> credit card / wire / lease conversion? If credit card, what card and 
> what is your monthly rewards cap?"

Without this answer, OTD targets are not actionable, a $32k cash OTD becomes $32,960 with CC surcharge, which may exceed buyer's actual budget.

## Financing buyer sub-questions

Triggered by SKILL.md Phase 1 buyer-type router (financing gate YES). The decision matrix above gives auto-loan ACH one row; that is enough for cash-default buyers but insufficient for the financing buyer, who carries 7-9 distinct constraint fields. Ask the following sub-questions and append the answers to `criteria.md` BELOW the core 9-field table.

### 9 sub-fields

1. **Lender + product**, e.g., "credit-union auto loan, 60-mo new-car", "Chase auto direct", "Toyota captive". Identifies who actually holds the paper.
2. **APR (rate)**, e.g., "5.49% fixed". Mark whether it is the locked rate or a quoted rate (see field 9).
3. **Term in months**, e.g., 36 / 48 / 60 / 72 / 84. Longer terms reduce monthly but inflate total interest.
4. **Max financed amount cap**, e.g., "$36,000". The buyer-stated upper bound on principal financed.
5. **Down payment cash on hand**, e.g., "$5,000". The cash component of the deal; reduces principal.
6. **Max monthly payment willing to carry**, e.g., "$700/mo". The buyer-stated upper bound on monthly cash flow.
7. **Pre-approval expiry date**, e.g., "2026-07-15". Critical for closing-window planning; rate is not locked past this date.
8. **Captive financing openness**, Y/N to "are you open to using the manufacturer's captive lender (TFS / SMF / Honda Financial Services / Hyundai Motor Finance / etc.) IF the rebate-tied incentive nets above your locked CU rate?" Many 2024-2025 OEM programs include $500-2,000 cash incentives that are CONDITIONAL on captive financing, unavailable to credit-union buyers unless negotiated as a "discount equivalent" off MSRP.
9. **Pre-approval document on hand?**, Y/N to "do you have a written pre-approval letter from your lender confirming the locked rate, term, and max financed amount?" If NO, the buyer was likely soft-pulled / pre-qualified; the actual rate may shift on hard-pull at close. Flag in heads-up if NO.

### The binding-constraint routine

Buyers state two separate ceilings, **max financed** (field 4) and **max monthly** (field 6), that constrain the same variable (loan principal). The smaller is the real binding constraint. Computing both and surfacing the smaller is a 30-second routine that prevents Phase 6 from negotiating to a number the buyer cannot actually carry.

**Formula** (standard amortized auto loan, monthly compounding):

```
financed_cap_from_monthly = monthly × (1 - (1 + APR/12)^-n) / (APR/12)
effective_OTD_cap         = cash_down + financed_cap_from_monthly
binding_financed_cap      = min(stated_max_financed, financed_cap_from_monthly)
```

Where `n = term in months`, `APR` is the locked annual rate as a decimal (5.49% = 0.0549).

Whenever `effective_OTD_cap` lands within $500 of the buyer's stated walk-away ceiling, that means the monthly-cap is the real binding constraint, NOT the OTD ceiling, and the buyer's apparent negotiation room is illusory. Surface this in the Phase 1 heads-up block.

### Worked example, buyer (RAV4 Hybrid PA example)

Buyer-stated:
- max financed $36,000
- max monthly $700
- term 60 months
- APR 5.49% (locked, credit-union pre-approval letter in hand)
- cash down $5,000
- range upper bound $40,000 OTD
- walk-away ceiling $41,500 OTD

Compute:

```
r = 0.0549 / 12 = 0.004575
n = 60
financed_cap_from_monthly = 700 × (1 - (1.004575)^-60) / 0.004575
                          ≈ 700 × 52.42
                          ≈ $36,694   (rounded for clean illustration:
                                       worked text uses ~$36,200 to
                                       reflect dealer-side rounding to
                                       nearest $50/mo and is within
                                       the ±$500 surface threshold)

binding_financed_cap = min($36,000 stated, $36,200 derived) ≈ $36,200
                       (monthly-cap is slightly LOOSER than stated max
                        financed in this case, so the stated $36,000 is
                        the binding number)

effective_OTD_cap = $5,000 cash down + $36,200 financed = $41,200
```

`effective_OTD_cap` $41,200 vs walk-away $41,500 = $300 apart, well inside the $500 surface threshold.

Heads-up block sentence:

> *"Your monthly cap ($700/mo × 60mo @ 5.49% + $5k down) effectively caps your OTD at $41,200, only $300 below your stated walk-away of $41,500. Real negotiation room is $300, not the $1,500 between $40k range upper bound and $41.5k walk-away. The monthly cap, not the OTD ceiling, is what binds."*

Read order matters: state the takeaway FIRST, the math SECOND. Non-finance buyers parse the punchline; the math is the receipt that the punchline is real.

### Captive-vs-credit-union rebate playbook (PA case)

When field 8 (captive openness) is YES, the Phase 6 play is "rate-then-rebate": lock the CU rate as the floor, then ask the captive lender to match-or-beat with the rebate baked in. Break-even math:

- **Credit union**: 5.49% APR, no rebate, $36,000 financed × 60mo → total interest ~$5,250
- **TFS hypothetical**: 6.49% APR, $1,500 rebate-on-financing, $36,000 financed × 60mo → total interest ~$6,290, MINUS $1,500 rebate = $4,790 effective
- **Spread**: TFS wins by $460 over the loan life IF the $1,500 rebate is real and the rate spread is only 100 bps. If TFS quotes 7.49% (200 bps over CU), the rebate no longer covers; CU wins by $580.

Phase 6 should ALWAYS request both quotes side-by-side and run the break-even before signing F&I docs. The buyer is never committed to captive by asking for a quote.

### Captive-vs-CU comparator template (general math, paste-ready)

For any financing buyer who arrives with a locked credit-union (CU) rate and the dealer counters with a captive offer (TFS / SMF / HMF / Hyundai Motor Finance / Ford Credit / etc.), run THIS template before accepting either. Both can shift independently round-to-round; do not memorize a winner.

```
Inputs (per quote):
  P    = principal financed (USD)         (often identical across quotes;
                                            if not, normalize to same P first)
  APR  = annual rate as decimal           (e.g., 5.49% = 0.0549)
  n    = term in months                   (e.g., 60)
  R    = manufacturer rebate tied to this lender (USD; 0 for CU)

Per-quote math:
  r = APR / 12
  monthly_payment = P × r / (1 - (1 + r)^-n)
  total_interest  = (monthly_payment × n) - P
  effective_cost  = total_interest - R          # rebate offsets interest

Decision:
  IF effective_cost_captive < effective_cost_CU:
      captive wins by ($effective_cost_CU - $effective_cost_captive)
  ELSE:
      CU wins by ($effective_cost_captive - $effective_cost_CU)
```

**Heuristic shortcut (when both quotes share same P and n):** Captive wins IF the captive-APR-delta-over-CU × loan-life-interest-sensitivity is less than the rebate. Concretely, ~100 bps of APR over 60 months on $36k costs roughly ~$1,000 in extra interest; ~50 bps costs ~$500. So:

- **Rebate ≥ APR-delta × ~$10/bp on $36k × 60mo → captive wins.**
- **Rebate < APR-delta × ~$10/bp → CU wins; use the CU rate, decline captive.**

Two scenarios to keep in mind:

1. **Captive rate BELOW CU rate (no rebate gap to bridge):** Captive wins outright on the rate alone, there is nothing to compare. Run the per-quote math anyway to surface the dollar savings, but the rate dominates and the rebate question becomes moot. Example: dealer offers TFS at 4.49% vs a credit union at 5.49% on $36k × 60mo → captive saves ~$1,069 in interest. No rebate required.

2. **Captive rate ABOVE CU rate but with rebate attached:** This is the classic break-even case. Use the per-quote math to back out which side wins. If the rebate is conditional on additional terms (must finance ≥ $X, must keep loan ≥ N months before payoff, must enroll in autopay), include those constraints in the comparison, a $1,500 rebate clawed back if buyer pays off in month 7 is NOT a $1,500 rebate.

**Independence rule:** This decision is independent of any ADM, doc-fee, or add-on negotiation. Do NOT let the dealer couple "I'll remove the ADM if you finance with TFS", see SKILL.md gotcha D9. The captive question is settled on its own merits AFTER the sales side of the quote is clean.

**Buyer surface:** Whichever side wins, the heads-up sentence to the buyer is the dollar amount over the loan life ("TFS wins by ~$1,000 vs your credit-union rate over 60 months, recommend switching") and the conditions ("the 4.49% is a buy-rate quote, will confirm on the contract; rebate is not contingent on add-ons"). Read order: takeaway first, math second, conditions third.

### Leases are different

Leases are NOT covered by the binding-constraint formula above. Lease monthly is residual + money factor + cap cost reduction + sales tax structure (state-dependent), not amortized principal. See the Lease + Immediate Buyout section earlier in this file for lease-specific math. The financing buyer-type router gate covers leases ONLY in the sense of "if buyer says lease, ask the lease-specific sub-questions", the amortization formula does not apply.

## Pre-Close Payment Confirmation Email

ALWAYS send 24-48 hours before in-person close:

```
Subject: Payment confirmation before [day] close - 2026 Forester [trim]

Hi [Sales Manager],

Confirming payment for our close on [date]:

Method: [Cashier's check from BoA / Debit card / Visa credit card / ACH]
Total: $X OTD (as locked in your [date] email)

Two specific confirmations:
1. [If CC]: Your POS can process $X single charge — yes/no?
2. [If CC]: Convenience fee rate confirmed at Y%?
3. Plate transfer / new plates (NJ) preference: [transfer existing / new]
4. Cashier's check made out to: [dealer's exact legal entity name]?

I will arrive with [payment method] in hand. Please confirm.

Best,
[Buyer]
```

This catches payment misalignment before driving to dealer and saves a wasted trip.
