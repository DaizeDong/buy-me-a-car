---
name: Insurance Shopper
description: Use when the buyer needs to set up or compare auto insurance before close day, especially for first-time drivers, cash buyers, or cross-state moves. Handles NJ/NY/PA/CT/MA state minimums, full-coverage recommendations, new-driver rate shocks, NJM/Geico/Progressive/State Farm quote sequence, and the "insurance ID card before dealer release" pre-close gate. Triggers include "set up insurance", "上保", "car insurance quote", "new driver insurance", "保险报价", "ID card before pickup".
---

# Insurance Shopper

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state minimums / carrier rates / discount stacking against current sources before binding a policy. Not insurance, tax, legal, or financial advice.
> last_verified: 2026-05-19
> Scope: narrow pre-close insurance shopping + bind workflow. For full close-day flow see `../close-day-checklist/SKILL.md`. For per-state fee specifics see `../state-fee-lookup/SKILL.md`.

Narrow helper for setting up auto insurance BEFORE the F&I appointment, with new-driver and cash-buyer edge cases handled. Use when buyer says "I need insurance for the new car" or when close day is < 7 days out and no policy exists yet.

## When To Use

- Buyer asks "how do I set up insurance for the new car"
- First-time driver (license < 12 months) needs a quote
- Cash buyer asking "do I even need full coverage"
- Cross-state move (NJ resident buying in PA, etc.) and unclear which state's policy
- Close-day countdown started, no ID card secured yet
- Triggers: "set up insurance", "car insurance quote", "new driver insurance", "上保", "保险报价", "ID card before pickup", "lender requires insurance"

## When NOT To Use

- Policy review for existing policyholder with no new vehicle - use a licensed agent
- Claims handling after an accident - use the carrier's claims line
- Commercial / fleet / rideshare insurance - out of scope
- Health / life / homeowners / umbrella - out of scope
- General OTD math - use `../otd-calculator/SKILL.md`

## The Pre-Close Gate

```
+--------------------------------------------------------+
| BLOCKER: Dealer will NOT release the vehicle without   |
| an active insurance ID card showing the buyer + VIN.   |
| Bind insurance BEFORE the F&I appointment, NOT during. |
| Walking in without coverage = dealer-controlled scramble|
| and worst-case overnight delay.                        |
+--------------------------------------------------------+
```

Target state: ID card PDF on phone, 1 paper copy in folder, before walking into F&I.

## NJ State Minimums (Tri-State Anchor)

| Coverage | NJ legal min | Recommended ($33k cash buyer) |
|---|---|---|
| Bodily Injury Liability | 15/30 | 100/300 |
| Property Damage Liability | $5k | $100k |
| PIP (Personal Injury Protection) | $15k | $250k (NJ no-fault) |
| UM/UIM | matched to BI | matched to BI |
| Comprehensive | not required | $500 deductible |
| Collision | not required | $500 deductible |

NJ is a no-fault state - PIP is load-bearing on medical exposure.

### Neighboring state minimums (BI / PD / PIP or equivalent)

| State | BI min | PD min | PIP / MedPay | Notes |
|-------|--------|--------|--------------|-------|
| NY | 25/50 | $10k | $50k PIP | No-fault; SUM (UM) required |
| PA | 15/30 | $5k | $5k MedPay | Choice no-fault; "limited tort" trap |
| CT | 25/50 | $25k | none required | Tort state; UM required |
| MA | 20/40 | $5k | $8k PIP | No-fault; compulsory PIP |

Whatever the state minimum is, on a new $33k vehicle the BI / PD floors are catastrophically low. Always recommend 100/300/100k as the practical floor.

## Driver-Profile Capture (7 fields)

Before any quote, collect:

```
1. Garaging ZIP             : NNNNN
2. DOB (year-month)         : YYYY-MM
3. License-issue date       : YYYY-MM-DD
4. Annual miles             : N,NNN (commute + pleasure)
5. Marital                  : single / married / domestic partner
6. Education                : high school / some college / bachelor / graduate
7. Prior insurance Y/N      : YES <months continuous> / NO
```

**New-driver flag**: license_issue_date < 12 months ago. Flips quote workflow into new-driver mode (see below).

**Continuous insurance**: most carriers reward 12+ months continuous; new drivers start at 0 and have to build the clock.

## Carrier Shortlist By State

Quote at least 3 carriers. Order matters - slowest/best-rate first.

| State | Carriers (rank order) | Why |
|-------|----------------------|-----|
| NJ | NJM, Geico, Progressive, State Farm | NJM is mutual, NJ-only, best rates for clean NJ resident; Geico + Progressive online instant |
| NY | Geico, Progressive, Allstate, NYCM | NYCM strong upstate; Geico/Progressive baseline; Allstate for bundling |
| PA | Erie, Geico, Progressive | Erie is agent-only but consistently 15-25% under online carriers in PA |
| CT | Amica, Geico, Progressive, State Farm | Amica mutual w/ dividend; State Farm strong agent network |
| MA | Plymouth Rock, Geico, MAPFRE, Arbella | MA has unique carriers; national carriers often not cheapest here |
| CA | Mercury, Geico, AAA | Mercury CA-strong; AAA bundles well; CA bans credit-based rating |
| TX | USAA (military), State Farm, Geico | USAA unbeatable if eligible; TX is competitive |
| FL | Geico, Progressive, State Farm | FL is expensive across the board; shop hard |

NJM requires NJ residence at quote time - confirm garaging address is NJ before wasting 25 min on the phone.

## Cash Buyer vs Financed vs Leased Matrix

| Buyer type | Comp+Collision | Deductible cap | GAP needed | Other |
|------------|----------------|----------------|------------|-------|
| Cash | Optional (recommended on new car) | Your choice | NO | Free to drop comp+coll on old beater later |
| Financed | REQUIRED by lender | Often $1,000 max | Often required first 1-3 yrs | Lender named as loss-payee |
| Leased | REQUIRED + higher limits | Often $500 max | Sometimes folded into lease | Lessor named as loss-payee + additional insured |

Cash buyer with $33k new vehicle: comp+collision is "optional" but skipping it on a new car is a self-insurance decision against $33k. Recommended unless buyer can write that check tomorrow.

Lender / lessor requirements vary - read the loan docs. Common: "100/300 BI, $100k PD, $500 deductible max, comp+collision required."

## New-Driver Section (license < 12 months)

This is the most expensive / most landmine-laden case.

### Rate impact

- First-year rate is typically **2-3x adult average** for the same coverage
- Examples (NJ, 100/300/100k + $500 comp+coll on a $33k Subaru):
  - 30-year-old clean driver: $1,200-1,600 / 6 months
  - 22-year-old new driver standalone: $2,800-4,500 / 6 months
  - Same 22yo added to parents' policy: $900-1,800 / 6 months

### Parents'-policy option (the big lever)

If parents have a clean record and a policy in the same household, three ways to attach:

| Status | What it means | Rate impact |
|--------|----------------|-------------|
| "Added driver" | New driver listed on parents' policy, drives any household car | Cuts new-driver rate 30-60% vs standalone |
| "Named driver" | New driver named but pegged to specific vehicle | Mid-tier discount |
| "Principal driver" | The vehicle's PRIMARY driver - rate calculated to this driver | Highest cost on this vehicle but household discount applies |

Most carriers require same garaging address. If the new driver titles their own vehicle in their own name but lives at the parents' address, "added driver" is the usual path - they own the car, parents' policy covers it, household discount stacks.

### Defensive driving course discount

- 5-10% off liability premium for 3 years
- NJ MVC-approved courses: AARP Driver Safety, AAA, I Drive Safely, National Safety Council
- Online completion ~$25-40, 6-8 hours, no in-person required for most
- Stack with good-student if under 25

### Continuous-insurance start

- Even 1 month of any prior coverage (a rental policy, a non-owner policy, a parents'-policy line item) starts the continuous-insurance clock
- For a true first-time buyer with zero prior coverage: lock in the 6-month policy NOW, even if pickup is 2 weeks out, to start the clock for renewal
- Carriers vary, but most reward "12+ months continuous" with a 5-15% discount at renewal

### Recommended starting coverage for new driver

- Liability: 100/300 BI + $100k PD (do NOT take state minimums on a $33k vehicle)
- PIP: $250k in NJ; state-required elsewhere
- UM/UIM: matched to BI
- Comp + Collision: $500 deductible (the $250 deductible upcharge is usually not worth it for a new driver - claims frequency is higher and any single claim already shifts you to surcharge territory)
- New Vehicle Replacement rider: ASK (see G5 below)

## Quote Sequence Playbook

Step-by-step. Total time: 60-90 min for a thorough multi-carrier shop.

1. **Pull driver-profile data sheet** (the 7 fields above). Have driver's license + VIN + lienholder info (if financed) ready.
2. **NJM first** (~25 min, requires phone for new drivers in many cases - NJM sometimes won't fully quote online for under-12-months license). Get the rate, hold it.
3. **Geico online** (~10 min, fully online for new drivers). Save the quote ID.
4. **Progressive online** (~10 min). Save the quote ID.
5. **Optionally State Farm** (~30 min, agent contact, slower) or **Erie** (PA only, agent-only).
6. **Compare 6-month total premiums apples-to-apples**. Lock the coverage spec FIRST (e.g. 100/300/100k + $500 comp+coll + $250k PIP + NVR rider), then compare same-spec totals across carriers. Never compare on monthly premium - compare 6-month totals to avoid pay-period gotchas.
7. **Pick winner. Bind with effective date = close-day morning.** Don't bind effective 2 weeks early unless you're already driving the current vehicle and want continuity.
8. **Get ID card PDF emailed** within minutes of bind. Save to phone. Print 1 paper copy for the F&I folder. Verify VIN, buyer name, effective date all correct.

## Common Discounts (5-15% each, stack)

| Discount | Typical rate | Notes |
|----------|--------------|-------|
| Paid-in-full | 5-10% | Pay 6 months up front instead of monthly |
| 6-month vs 12-month | n/a | 6-month gives re-shop flexibility; 12-month sometimes locks rate but reduces leverage |
| Continuous insurance | 5-15% | 12+ months prior with no lapse |
| Defensive driving course | 5-10% | 3-year discount window |
| Good student | 5-15% | Under 25 + B+ GPA / Dean's list |
| Bundle | 5-15% | Renters + auto, or homeowners + auto |
| Anti-theft device | 1-5% | Most new cars qualify (factory immobilizer) |
| Vehicle safety features | n/a | EyeSight, AEB, etc. - usually baked into base rate, NOT a separate discount |
| Auto-pay / paperless | 1-3% | Small but free |

Stack everything that applies. Discounts are multiplicative-ish but capped per carrier.

## 5 Gotchas

**G1: Online new-driver coverage caps.** New-driver online quote tools sometimes silently CAP coverage selections at lower limits (e.g., dropdown won't show 250/500 even though it exists). Always verify the bound declarations page shows the limits you requested. Common at Geico online for under-21 drivers.

**G2: NJ "Basic Policy" trap.** NJ has a legal "Basic Policy" tier at $300-500/yr - DO NOT pick this. Medical-bills and BI exposure on Basic is catastrophic on a new $33k vehicle. It exists for low-income drivers with no assets to protect; on a financed new car it's a felony-of-judgment waiting to happen. The Standard Policy is the baseline.

**G3: "Automatic new-vehicle coverage" only works for ADDS.** The 14-30 day grace period for adding a new vehicle ASSUMES an existing policy you're adding to. For first-time buyers with NO existing policy: this does NOT exist. You MUST bind a new policy before pickup. Dealer F&I sometimes mis-states this - verify.

**G4: Quoted rate vs bound rate vs 90-day surcharge.** Progressive (sometimes Allstate) will quote LOW initially then surcharge after 90 days when they pull MVR or credit. Always:
  - Verify "no rate change in first 6 months" in writing
  - Get the binding rate confirmed AFTER they've pulled MVR + credit (not before)
  - Walk away if the carrier won't commit to the quoted rate for the full policy term

**G5: New Vehicle Replacement rider.** For brand-new $33k vehicle in first 1-3 years, ALWAYS include New Vehicle Replacement (NVR) coverage - typically $5-15/mo. Pays full replacement cost (new car of same trim, NOT depreciated ACV) if totaled. Most carriers don't push this - you must ASK. Without NVR, totaling a 6-month-old car gets you the depreciated value (~$26-28k on a $33k car), leaving you short.

## Output Contract

When the skill completes a shopping pass, return:

```
Insurance shopping pass - <YYYY-MM-DD HH:MM>
  Driver profile     : <new-driver / experienced>
  State              : <NJ / NY / PA / etc>
  Garaging ZIP       : <NNNNN>
  Carriers quoted    : <N>
  Coverage spec      : <e.g. 100/300/100k + $500 comp+coll + $250k PIP + NVR>
  Best 6-month total : $<X> via <carrier>
  Runner-up          : $<Y> via <carrier> (delta +$<Z>)
  ID card status     : <pending bind / bound / received>
  Effective date     : <YYYY-MM-DD>
  Pre-close blocker  : <YES resolved / NO not yet>
  Next action        : <bind by <date> / send ID card to F&I / etc>
```

## Cross-References

- `../orchestrator/SKILL.md` Phase 9 close-day gate (ID card is a blocker)
- `../close-day-checklist/SKILL.md` - cross-references the insurance ID card requirement
- `../state-fee-lookup/SKILL.md` - for per-state fee/registration detail (insurance is a separate axis but often shopped together)
- `../payment-method-decider/SKILL.md` - if financed, lender insurance requirements feed back into payment-method choice

## Voice Note

Insurance is a pre-close blocker, not a post-close cleanup. If the buyer pushes "I'll deal with it at the dealer" - push back. Dealer F&I will sell a panicked uninsured buyer a bad first-day policy + financing tie-in, and re-shopping after the fact is harder than shopping clean once.
