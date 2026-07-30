# Scenario 3: Used Honda CR-V, SF Bay Area CA, cash plus a trade-in

## The buyer

The buyer is a software architect in the SF Bay Area (<ZIP>). He is
a third-time buyer and knows cars. He test-drove a CR-V EX-L at a local
Honda dealer last weekend and confirmed the trim preference.

## The target

A 2020-2023 Honda CR-V EX or EX-L, under 50,000 miles. Color flexible
(no white). AWD preferred for winter mountain driving; he will accept
FWD if the savings clear $1,500. Must-haves: heated front seats, Honda
Sensing, Apple CarPlay, sunroof (standard on EX-L).

## The constraints

- Budget: $24,000 to $28,000 OTD. Walk-away ceiling: $29,500 hard stop.
- Geographic radius: 80 miles of <ZIP>, covers the SF Bay Area + adjacent CA metros.
- Payment: cash, cashier's check.
- **Trade-in: 2018 Honda Civic LX Sedan**, 67,000 miles, clean title in
  hand (no loan, no lien), all keys present, minor curb rash on 2 wheels.
  - KBB Instant Offer: $11,200.
  - KBB Trade-In Fair: ~$11,800-$12,500.
  - KBB Private Party: $13,500-$14,500.
  - Manheim wholesale floor: ~$10,500-$10,800.
  - The buyer expects $12,000 trade allowance from the dealer.
- Timeline: three weeks (close by 2026-06-09).

## The ask

The buyer wants the workflow to:

1. Capture the trade structurally, not as a single "expected trade value"
   number, but as the four-anchor valuation matrix (Manheim wholesale /
   KBB Instant / KBB Trade-In / KBB Private Party) plus a walk-floor
   (the $11,200 KBB Instant Offer is his outside option).
2. Apply the California trade-in tax credit correctly. California taxes
   the sale **minus** the trade allowance, that's a ~$1,100 savings at
   the buyer's CA county 9.25% combined rate on a $12k trade.
3. Catch the **shell-game trade**: when a dealer offers $12,000 trade but
   raises the CR-V sale price by $1,200 vs their original quote, the
   "extra" trade value is fake. Separate the two transactions
   structurally.
4. Surface Honda True Certified eligibility, 2022 CR-V EX-L with 28k
   miles is cleanly in the Honda Certified+ premium tier (4yr/48k limit).
   Embedded value $1,200-$1,800.

## What makes this scenario interesting

- This is the **first trade-in case**. The skill's trade-in capture before
  this scenario was a 6-field inline placeholder. Stress-testing surfaced
  three structural gaps: no KBB-vs-private-party tension capture, no
  state-specific trade-tax-credit field, no ACV-vs-trade-allowance
  distinction.
- California has the highest combined sales tax rates in the U.S. (Alameda
  9.25%, LA 9.5%) and California **does grant a trade-in tax credit**,
  this is the load-bearing fact that drives ~$1,100 of OTD math.
- High-supply state: California has thousands of CR-V listings within 80
  miles. Phase 3 filtering must be aggressive (AWD-only, sub-50k miles,
  no salvage / no rebuilt, EX-L trim, certified eligible).
- Honda CPO at this point in the skill's evolution had **zero reference
  depth** (Subaru CPO had full depth from scenario 1). Forced creation of
  the Honda CPO reference file.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md), Phases 1, 2, 6.
- [trade-in-valuator](../skills/trade-in-valuator/SKILL.md), four-anchor
  valuation cascade, ACV-vs-allowance separation, separate-the-negotiation
  protocol.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md), CA detail
  stub (county rates, $85 doc cap, $25 title, VLF-based reg) plus CA→NV /
  CA→OR / CA→AZ cross-state rows.
- [cpo-eligibility](../skills/cpo-eligibility/SKILL.md), Honda True
  Certified + Certified+ tiering.
- [otd-calculator](../skills/otd-calculator/SKILL.md), California math
  with trade-credit applied to sale-minus-trade.
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md), counter
  with three independent asks (sale price / trade allowance / tax credit).

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1, fired the trade-in branch of the buyer-type
   router. Captured 12 fields (vehicle / miles / condition / payoff /
   keys / four-anchor valuation / state credit flag / cosmetic deductions /
   ACV-vs-allowance / walk-floor / cascade ladder).
2. **state-fee-lookup**, pulled the California detail stub with county-
   level rate tables and the **YES** on trade-in tax credit (cross-checked
   against CDTFA Reg 1610).
3. **trade-in-valuator**, produced the cascade: >=$12.5k excellent,
   $11.2-$11.8k matches Instant-Offer tier, <$10.5k walk to KBB direct.
4. **cpo-eligibility**, Honda True Certified+ eligibility for the 2022
   EX-L 28k mi target; embedded value $1,200-$1,800.
5. **orchestrator** Phase 2, baseline produced (regional median $26,100
   sale / $29,000 gross OTD with no trade).
6. **dealer-reply-drafter**, counter to a synthetic sales-rep quote (sale
   $26,990, trade offer $10,500 sight-unseen, CA trade credit not applied).

### Artifacts produced

- `criteria.md` with the 12-field trade-in sub-block.
- `crv-ca-baseline.md` with four-anchor trade valuation matrix.
- `p6_counter_to_sarah.md`, three independent asks:
  - Sale price $26,990 → $26,400 (regional comps + mileage adjust).
  - Trade allowance $10,500 → $12,000 (KBB Instant Offer outside option +
    KBB Trade-In mid + private-party reality).
  - California trade-in tax credit (not applied in dealer quote) → applied
    per state_fees.md.
  - Cash out-of-pocket $19,750 → ~$16,225 (a $3,525 swing).

### Gotchas and Critical Rules that fired

- **Critical Rule #7**, one REAL anchor (the buyer's KBB Instant Offer
  screenshot at $11,200); all regional comps SYNTHESIZED with explicit
  placeholders for pre-send REAL pull.
- **Gotcha D8**, state-fee leak audit on the sales rep's quote: clean (CA doc
  $85 at statutory cap, 9.25% buyer's CA county combined correct, $25 title, $375
  reg). Leverage was on prices and trade, not fees.
- **ACV-vs-allowance shell-game detection**, if the sales rep raises the sale
  price by $1,200 to fund a $1,500 trade bump, the buyer nets +$300, not
  +$1,500. Counter asked for both transactions separately.
- **Separate-the-negotiation 5-round protocol**, counter framed the sale
  and the trade as independent transactions; dealer can walk on one without
  walking on both.

### What this scenario surfaced for the skill

Three concrete deltas landed (high leverage per delta):

- **`trade_in.md` (NEW reference file)**, 12-section playbook covering
  four-anchor valuation, ACV-vs-allowance distinction, state trade-tax-
  credit matrix, payoff handling (positive / negative / washed equity),
  lien release timing, key-count check, cosmetic deduction reference,
  separate-the-negotiation 5-round protocol, KBB Instant Offer as BATNA,
  state-specific quirks (CA, IL trade-credit cap, NJ, NY, KY/DC no-credit),
  documentation at close, and when NOT to trade.
- **California state stub at CT-depth**, county rates (Alameda 9.25%, LA
  9.5%, SF 8.625%, Santa Clara 9.125%, Contra Costa 8.75%), $85 doc cap,
  $25 title, VLF-based reg, **trade-in credit YES** with line-item
  enforcement note, full "Has" / "Does NOT have" leak lists, two worked
  OTD examples (no trade + with trade), CA→NV / CA→OR / CA→AZ cross-state
  rows.
- **`honda_cpo_program.md` (NEW reference file)**, at Subaru CPO depth.
  Honda True Certified vs Certified+ tier table, 6-year-from-in-service
  eligibility cap, embedded value $1,200-$1,800 (lower than Subaru's
  $2,000-$2,500 because Honda's factory powertrain warranty is shorter),
  market premium $800-$1,500 Bay Area, paste-ready negotiation ask,
  Honda Care VSC out-of-CPO option, CPO-vs-Subaru side-by-side.

### Reading takeaway

This scenario unlocks the trade-in path. Read after scenario 2. The four-
anchor valuation cascade and the separate-the-negotiation protocol are
the load-bearing patterns to internalize, they reappear in scenario 5.
