# OTD Negotiation Playbook

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

Example: AutoTrader <NJ town> shows 263 listings of 2024 Forester, avg $28,177, range $23,498-32,042. A "Great Deal" at this region threshold is ~$26,500 selling price.

### Anchor 3: Competing Concurrent Offers

When the buyer has 2-4 confirmed written OTD quotes from other dealers for similar vehicles, share these in negotiation. Format as:

> For reference, my current best offers:
> - {Year Make Model Trim} {miles} mi at ${OTD_1} OTD from {Dealer Name and City}
> - {Year Make Model Trim} {miles} mi at ${OTD_2} OTD from {Dealer Name and City}

Be specific (dealer name, mileage, OTD). Dealers know the regional market and can verify these are real numbers.

## OTD Math (NJ)

Reverse-engineer from target OTD to acceptable sales price:

```
Target OTD = (Sales + Doc) × 1.06625 + Title + Reg + Add-ons

If Doc = $499, Title = $85, Reg = $100, Add-ons = $0:
Target $30,000 = (Sales + $499) × 1.06625 + $185
Sales = ($30,000 - $185) / 1.06625 - $499 = $27,470
```

For dealers with $0 doc fee (rare; some independent dealers absorb doc fee into selling price):
```
Target $30,000 = Sales × 1.06625 + $200 reg
Sales = ($30,000 - $200) / 1.06625 = $27,950
```

For Enterprise no-haggle structure ($250 flat DMV, no doc):
```
OTD $20,348 = Sales × 1.06625 + $250
Sales = ($20,348 - $250) / 1.06625 = $18,851
```

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

> Understood, and I respect the policy. For my needs and budget, the numbers do not pencil out versus my comparable offers. If anything changes — price adjustment, a similar unit at a more competitive number — please reach back out. Wishing you the best on the sale.

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
