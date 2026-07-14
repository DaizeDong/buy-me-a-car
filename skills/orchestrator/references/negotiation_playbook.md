# OTD Negotiation Playbook

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

## The Three Anchoring Approaches

### Anchor 1: Internal Dealer Inventory

When the same dealer offers two comparable cars at different prices, derive the implied fair price for the target car using the spread.

Example: Dealer offers 2024 Forester Standard 10k mi @ $25,000 sales / $26,900 OTD and 2024 Forester Limited 20k mi @ $30,000 sales / $32,200 OTD.

The $5,000 sales spread should equal:
- + Limited trim premium over Standard ($2,000-3,000 typical for used)
- − Mileage delta penalty (+10k mi × $0.10-0.15/mi = $1,000-1,500)
- = Net fair spread $1,000-2,000

So Limited fair sales = $25,000 + $1,500 = $26,500. Asking $30,000 is overpriced by $3,500.

This is the strongest anchor because it uses the dealer's own pricing data against them. They cannot dispute their own listings.

### Anchor 2: Regional Market Comp

Pull aggregate data from AutoTrader / Edmunds / CarGurus for the exact year/make/model in the buyer's region. CarGurus publishes deal ratings ("Great Deal" / "Good Price" / "Fair Price" / "Overpriced") that correspond to specific price thresholds.

Search query template: "{Year} {Make} {Model} {Trim} {City} {State} used average price"

Save the data points: regional median price, range, sample size, deal-rating thresholds.

Example: AutoTrader regional NJ search shows ~263 listings of 2024 Forester, avg $28,177, range $23,498-32,042. A "Great Deal" at this region threshold is ~$26,500 selling price.

### Anchor 3: Competing Concurrent Offers

When the buyer has 2-4 confirmed written OTD quotes from other dealers for similar vehicles, share these in negotiation. Format as:

> For reference, my current best offers:
> - {Year Make Model Trim} {miles} mi at ${OTD_1} OTD from {Dealer Name and City}
> - {Year Make Model Trim} {miles} mi at ${OTD_2} OTD from {Dealer Name and City}

Be specific (dealer name, mileage, OTD). Dealers know the regional market and can verify these are real numbers.

## Round 1 Cold Open (1 bid in hand, 0 competing OTDs)

The most common starting state of any negotiation cycle: the buyer has ONE dealer quote in hand, ZERO competing written OTDs, and no internal-spread comparable in the dealer's own inventory. Anchor 3 is not yet available; Anchor 1 may not be available; Critical Rule #7 forbids inventing competitor numbers. The Cold Open recipe codifies what to do in this state so the executor does not improvise.

Use these 5 elements, in this order, in a ~10 line counter:

1. **Regional anchor — 1 real Edmunds/CarGurus citation by name.** One named-source data point with city/region scope (e.g., "Edmunds Hartford CT 2023 Outback average list $26,151"). Stronger than "national average." Must be REAL-tagged per Critical Rule #7; cite source by name so dealer can verify or refute.

2. **Named single-comp listing — another dealer's same-trim listing.** One specific competing listing by dealer name + ask price (e.g., "Hoffman Honda has a comparable 2023 Outback Limited at $27,900 ask"). This is a public listing, not a written OTD, so it does not violate Critical Rule #7. Stronger than the regional aggregate alone because it has a name.

3. **In-flight signal — preserve Critical Rule #7.** Reference the cross-bid effort transparently WITHOUT naming dealers or inventing numbers: e.g., "I am actively cross-bidding written OTDs with 2-3 more dealers in the region this week; I expect responses by Wednesday." This is true (you do have outreach in flight) and primes the dealer for a tighter close window without fabricating data.

4. **Soft ceiling at round 1 — range, not precise number.** State the walk-away as a RANGE (e.g., "low-$30k OTD, hard cap") rather than the exact dollar number. Preserves commitment-device value while denying the dealer a precise +$250/+$400 fishing target. Reserve precise-number disclosure for round 2-3 once the ZOPA is mapped.

5. **Close-window deadline — specific, near, plausible.** Name a close date that is short enough to apply pressure but credible given cash/funding posture (e.g., "I can close Thursday or Friday with a cashier's check pending PPI"). Avoid vague "this month."

### Worked example (CT cold open, used 2023 Outback Limited)

Dealer's opening: $28,990 sale / $31,560 OTD with an NJ-tire-fee leak on a CT quote. Buyer has no written competing OTDs yet, walk-away ceiling $30,000 OTD.

> Hi Tony, thanks for the breakdown. Three items:
> 1) The $7.50 tire fee on the quote is an NJ line item; CT has no per-tire fee. Please re-quote OTD without it.
> 2) CT 2-year passenger reg is ~$120, not $80; please correct.
> 3) For the sale price, Edmunds shows the Hartford CT 2023 Outback average list at $26,151, and Hoffman Honda has a comparable Limited at $27,900 ask. I am actively cross-bidding written OTDs with 2-3 more CT/MA dealers this week; responses expected by Wednesday. My budget caps in the low-$30k OTD range, hard.
> Cash buyer, cashier's check, ready to close Thursday or Friday pending PPI. Please send the revised written OTD when you have it.

5 elements present: regional anchor (Edmunds Hartford), named single comp (Hoffman $27,900), in-flight signal (no names, just timing), soft ceiling (range "low-$30k", not "$30,000"), close window (Thu/Fri). 10 content lines. Dealer can answer each numbered item without re-reading.

## OTD Math (State-Parameterized)

Generic formula — works for any registering state. Pull `StateRate` (combined state + local), `Doc`, `Title`, `Reg`, `Other` line-items from `references/state_fees.md` for the specific state and ZIP.

```
OTD = (Sale + Doc) × (1 + StateRate) + Title + Reg + Other
```

Where:
- **Sale** = agreed sales price
- **Doc** = dealer doc fee (subject to state cap if any; see state_fees.md)
- **StateRate** = combined sales-tax rate at registering ZIP (state + county + city + special-district)
- **Title + Reg** = state-fixed (or weight/value-formulated)
- **Other** = state-specific add-ons that are LEGITIMATE for the registering state (NY MCTD, TX EV reg premium, CA smog/TIF, etc. — see state_fees.md "Has" lists). Line items appearing on a quote but NOT in the registering state's "Has" list are state-template leaks (gotcha D8).

To reverse-engineer the maximum sales price for a target OTD:

```
Sale = (TargetOTD - Title - Reg - Other) / (1 + StateRate) - Doc
```

If trade-in applies AND state grants trade-in tax credit (state_fees.md "Trade-In Tax Credit" column), Sale tax base becomes `(Sale + Doc - Trade)`; see § Trade-In Tax Credit Math in state_fees.md and `references/trade_in.md` § 3 for the per-state matrix.

### Worked example 1 — NJ (example county, no local stacking)

StateRate = 6.625% flat; Doc cap = $799; Title = $85; Reg = $70; Other = $0.

Sale $25,000, Doc $499:
```
OTD = ($25,000 + $499) × 1.06625 + $85 + $70 + $0
    = $25,499 × 1.06625 + $155
    = $27,188.31 + $155
    = $27,343.31
```

Reverse, Target OTD $30,000:
```
Sale = ($30,000 - $85 - $70 - $0) / 1.06625 - $499
     = $29,845 / 1.06625 - $499
     = $27,991.55 - $499
     = $27,492.55
```

### Worked example 2 — CT (Hartford, no local stacking, watch luxury tier)

StateRate = 6.35% standard (7.75% if Sale > $50,000); Doc cap = none, $499-699 typical; Title = $25; Reg ≈ $120 (2-year passenger); Other = $0 (no per-tire, no battery fee — see CT "Does NOT have" list).

Sale $25,000, Doc $599:
```
OTD = ($25,000 + $599) × 1.0635 + $25 + $120 + $0
    = $25,599 × 1.0635 + $145
    = $27,224.71 + $145
    = $27,369.71
```

If a CT quote contains an NJ-style $7.50 tire fee or NJ supplemental titling, demand full re-quote per gotcha D8 — these are not legitimate CT line-items.

### Worked example 3 — CA (Alameda County, ZIP-stacked combined rate, low doc cap)

StateRate = 9.25% combined (CA 7.25% + Alameda 2.00%); Doc cap = $85 (Vehicle Code § 4456.5, capped low); Title = $25; Reg ≈ $250 (VLF + base + TIF + county components on a ~$25k value vehicle); Other = $0-25 (smog transfer ≈ $9; tire fee ≈ $1.75/tire).

Sale $25,000, Doc $85:
```
OTD = ($25,000 + $85) × 1.0925 + $25 + $250 + $0
    = $25,085 × 1.0925 + $275
    = $27,405.36 + $275
    = $27,680.36
```

Notes for CA: (a) CA does NOT grant state-level trade-in tax credit (sales tax applies to gross sale; see state_fees.md All-State Summary CA row and § Trade-In Tax Credit Math). (b) Pull the buyer's ZIP-specific combined rate from state_fees.md CA stub — Alameda 9.25%, LA 9.5%, SF 8.625%, Santa Clara 9.125%, Sacramento 8.75%, Solano 7.375% (lowest in state), San Diego/Orange 7.75%.

### Worked example 4 — TX (state-only, no local stacking, EV reg premium)

StateRate = 6.25% flat (TX is state-only — NO local stacking, unique among large states; see TX detail stub in state_fees.md); Doc cap = $150 (statutory, TX Occ Code § 2301); Title = $33; Reg ≈ $67 (~$56.50 base + ~$11 county). Other = +$200/yr if BEV (TX Transp Code § 502.360, SB 505 effective Sept 2023; BEV only, hybrid exempt).

Sale $25,000, Doc $150, ICE vehicle:
```
OTD = ($25,000 + $150) × 1.0625 + $33 + $67 + $0
    = $25,150 × 1.0625 + $100
    = $26,721.88 + $100
    = $26,821.88
```

Same scenario, BEV (Ioniq 5, Mach-E, etc.):
```
OTD = ($25,000 + $150) × 1.0625 + $33 + $67 + $200
    = $26,721.88 + $300
    = $27,021.88
```

The federal §30D $7,500 New Clean Vehicle Credit is **TERMINATED** for any vehicle acquired after 2025-09-30 (OBBBA / Public Law 119-21; see IRS FAQ Fact Sheet 2025-05). For any 2026 purchase there is NO federal $7,500 credit — do NOT subtract it from net cash or OTD. The BEV case net cash out-of-pocket is the full OTD ($27,021.88), unless a still-funded **state/local rebate** applies (see `ev_buyer_playbook.md` state EV rebate matrix, the only live federal/state incentive layer). HISTORICAL: for a vehicle acquired on or before 2025-09-30 the §30D credit was a buyer-side POS or tax-filing credit ($27,021.88 − $7,500 = $19,521.88); that window is now closed.

### Quick state-rate lookup (most-common registering states)

| State | StateRate (combined typical) | Doc cap | Notes |
|---|---|---|---|
| NJ | 6.625% (flat, no local) | $799 | Trade credit Yes |
| NY | 8.875% (NYC); 8.0% (Westchester); 4.0% (no local) | $175 | + MCTD $50 in NYC area |
| PA | 6% / 7% Allegheny 150-152XX / 8% Philly 191XX | none | Verify ZIP before defaulting |
| CT | 6.35%; 7.75% if Sale > $50k | none, $499-699 | Watch luxury tier |
| MA | 6.25% (flat, no local) | none | |
| RI | 7% (flat) | $250 | Strong protection |
| CA | 7.25% base; 7.375%-10.5% combined by ZIP | $85 | No trade credit |
| TX | 6.25% (flat, NO local stacking) | $150 | +$200/yr BEV reg |
| IL | 6.25% + 0-4% local | $347.26 | Trade credit capped at $10k |
| FL | 6% + 0.5-1.5% local | none, $799-1,000+ | Trade credit Yes |

For other states, pull from state_fees.md All-State Summary Table + relevant detail stub.

### Special structures

Enterprise / CarMax / Carvana no-haggle ($0 doc, fixed DMV fee):
```
OTD = Sale × (1 + StateRate) + Title + Reg + FixedDMV
```

DE (no state tax, but 4.25% "doc fee" on purchase price for DE residents):
```
OTD = Sale × 1.0425 + Title + Reg     // DE-residents-only
```
For PA/NJ buyers titling at home, DE = doc-fee sweet spot (avoid DE doc fee, pay home-state tax instead; see state_fees.md PA→DE row).

## Counter-Offer Tactics

### Direct Counter

Lead with target OTD and provide 2-3 structural paths so dealer can pick which to give:

> My target OTD is $30,000. Possible structures:
> 1. Sales $27,950 + Doc $0 + Tax + $200 Reg
> 2. Sales $27,471 + Doc $499 + Tax + $200 Reg
> 3. Any combination that lands at $30,000 OTD

This gives the dealer flexibility on how to make their numbers work internally (margin on doc fee, etc.).

### Soft Counter with Walk-Away Line

Include an explicit "If $X does not pencil out, I will move forward with my other offer." This creates urgency without aggression and shows the buyer is not bluffing.

### Add-On Refusal

Reject any of these line items with: "Please remove the [item] add-on. I am not interested in dealer-installed accessories."

- Paint protection / sealant
- Fabric guard
- Nitrogen tires
- Window etching / VIN etching
- Theft deterrent / anti-theft package
- Dealer prep fee over $200
- Doc fee over $799 (NJ legal cap)
- Compliance fee (vague)

## Walk-Away Lines

The clearest signals to walk away from a dealer:

- Won't send OTD by email ("come in and discuss pricing")
- Doc fee at NJ max ($799) AND sales price at MSRP (no discount)
- Mandatory add-ons that can't be removed
- "Best price upfront, no negotiation" combined with above-market pricing
- Refuses to share CARFAX or maintenance records
- Refuses independent PPI
- Pressures with "this car will be gone today" repeatedly

Walk gracefully:

> Understood, and I respect the policy. For my needs and budget, the numbers do not pencil out versus my comparable offers. If anything changes (price adjustment, a similar unit at a more competitive number), please reach back out. Wishing you the best on the sale.

This keeps the door open without conceding leverage.

## Cash Buyer Leverage

Cash buyers reduce dealer transaction risk:
- No financing approval delay (typical 3-7 day wait)
- No trade appraisal contingency
- Same-day funding (cashier's check)
- Simpler paperwork
- Predictable close timeline

Use this explicitly in opening message and any counter:

> I am a cash buyer in {City} {State}, ready to close this week pending PPI. No trade, no financing.

Dealers should price this at ~$500-1,000 of value vs a typical financed-with-trade customer. Don't expect them to advertise this discount — but use it as a reason for them to meet your number.

## CPO Embedded Value Math

Subaru CPO (and similar OEM CPO programs):
- 7-year/100,000-mile powertrain warranty from original in-service date
- $0 deductible
- Transferable
- 152-point inspection
- Roadside assistance 24/7

Equivalent third-party extended powertrain warranty: $2,000-2,500 for same coverage.

So if a sub-60k mi car is CPO-eligible but not enrolled at point of sale, asking the dealer to enroll it (often at dealer cost ~$500-800) captures ~$1,500-2,000 of additional value.

For out-of-CPO cars (over 5 years old or 80k+ mi), this avenue closes. Factor in $2,000 missing value when comparing.

## Mileage Adjustments

Standard industry adjustments (Black Book / Manheim):

- Compact/Midsize sedan: $0.07-0.10/mi
- SUV (Forester / Outback / CR-V): $0.10-0.15/mi
- Luxury / Performance: $0.15-0.25/mi

So a 73k mi Subaru vs a 50k mi Subaru is $0.10 × 23,000 = $2,300 lower fair value (using low-end adjustment).

## Test Drive Negotiation Pivot

After a successful test drive, walk through this sequence:

1. Confirm interest verbally but without committing to a number
2. Ask the dealer for THEIR best price (do not anchor first)
3. If their number is at or below your target → accept happily
4. If their number is above your target → use anchor logic to counter
5. If they refuse to move → invoke walk-away line + leave door open
6. Avoid going below "Walk away OTD" in the prep file

## Sequential Dealer Pricing Disclosure

Save a competing OTD quote (lower than your target) for late-stage leverage:

- Round 1: Ask dealer for OTD (don't share competition)
- Round 2: If OTD too high, reveal one or two competitive offers
- Round 3: If still too high, reveal additional offers + state walk-away line
- Round 4: Walk

Each disclosure increases urgency without committing to walk.

## Escalation Ladder When Dealer Delays ("Let Me Check With My Manager" Tactic)

A common stall tactic: dealer rep says "let me check with my manager" or "I'll get back to you tomorrow" repeatedly across multiple touches. The intent is to burn the buyer's clock — pre-approval letters expire (typically 30 days), insurance binders expire, other anchor dealers go cold, and the buyer becomes positionally weaker the longer the cycle drags. Without an escalation ladder, the dealer controls cadence and the buyer loses leverage by attrition.

Codified ladder — start the clock at the first "let me check" without a same-day reply:

### T+24h — Polite reminder with explicit EOD-tomorrow deadline

Reply in the existing thread (do NOT start a new thread — breaks the dealer's CRM context and re-starts the cadence). Keep it ~6 lines, plain ASCII.

```
Hi {REP_NAME},

Following up on my {DATE} question about {VEHICLE / OTD ASK}.

To keep the cycle moving, I need an answer by EOD tomorrow,
{T+48H_DATE}. After that, my other anchors firm up and this
unit loses position in the queue.

Thanks,

{BUYER_NAME}
```

### T+48h — Firm walk-away signal with the locked competitor anchor

If no response by T+48h, escalate. Cite the locked competitor OTD by dollar amount (per gotcha N1 anchor-disclosure rule). This is the last realistic chance for the delaying dealer to win.

```
Hi {REP_NAME},

I have not heard back since my {DATE} note. My locked benchmark
is now {COMPETITOR_DEALER} at ${COMPETITOR_OTD} OTD on a
comparable unit.

I am proceeding with {COMPETITOR_DEALER} unless I have a written
OTD from you by {T+72H_DATE} EOD. Final chance.

Thanks,

{BUYER_NAME}
```

### T+72h — Silent walk-away + tracker log

If still no response, do NOT send another follow-up — additional pings past T+72h signal desperation and reduce leverage on the next outreach cycle (dealers remember). Log the dealer as cold in `dealer_outreach_tracker.md`:

```
[timestamp] | {Dealer} | {Rep} | COLD | last_contact_attempt=T+48h |
  walked silently per escalation ladder | re-engage only if {Rep}
  initiates contact OR inventory situation changes materially
```

Do NOT delete the dealer from the tracker — they may re-engage in 1-2 weeks with a "are you still looking?" ping, at which point the cold-warm transition reopens. Keep the row for that future signal.

### Special cases

- **Out-of-Office detected mid-cycle.** If the rep's silence coincides with an OOO autoresponder (per `references/cron_monitoring.md` § OOO autoresponder detection), do NOT advance the ladder. Hold the cycle until the parsed `oo_return_date` passes, then re-baseline at T+0 from the return date. OOO is a legitimate pause, not a delay tactic.
- **"Let me check with my manager" as opening move on a same-day reply.** Not a delay yet. Apply the ladder only after the rep has said this AND failed to return with the manager's answer by EOD same day OR T+24h.
- **Buyer-side timeline compression.** If the buyer's stated close date is within T+72h of the first ping (timeline already at minimum per Phase 1 dependency-chain check), tighten the ladder: T+12h reminder, T+24h walk-signal, T+36h cold-log. Short cycles cannot afford the 72h standard cadence.
- **Multi-rep parallel push.** If the original rep is unresponsive but the dealership has multiple Internet Sales reps, after T+48h with no response from the original rep, send the T+48h walk-signal email to the dealership's general Internet Sales mailbox (often `internet@example-dealer.com` or `sales@example-dealer.com`) with the original rep CC'd. This sometimes surfaces a more responsive rep at the same store without burning the bridge with the first rep.

### Why this ladder exists

Without it, a dealer can stall a buyer for 5-10 days while the buyer's pre-approval, anchors, and patience all decay. With it, the buyer controls the cadence: the dealer either responds within 72h or loses position permanently, and the buyer's other anchors stay warm because the buyer is not waiting on this one dealer past T+72h to confirm them. The ladder is also a Critical Rule #7-safe pattern: every claim in the T+24h and T+48h emails is real (the deadline IS real because the buyer has set it; the competitor OTD IS real because it's a locked benchmark).
