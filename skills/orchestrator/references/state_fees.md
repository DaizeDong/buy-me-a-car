# State-Specific Fees and Taxes — All 50 States + DC

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)
> **Data refresh schedule**: state rates / CPO programs / EV incentives / lease parameters should be re-verified annually or upon any user-cited deal that contradicts. The 2026-05-18 timestamp marks last full audit.

This reference covers the four major fee components for car purchases across all US states:

- Sales tax rate (state-level; some states add local county/city tax)
- Doc fee (legal cap or typical industry range)
- Title fee (one-time)
- Registration fee (typical for sedan/SUV — varies by weight)

Verify exact current rates with the state DMV or seller dealer before each transaction; rates and laws change.

## OTD Formula (Generic)

```
OTD = (Sales price + Doc fee) × (1 + sales_tax_rate)
    + Title fee
    + Registration fee
    + Tire/Battery/Environmental fees (if any)
    + Add-ons
```

States vary on whether sales tax applies to the doc fee (most do), whether trade-ins reduce taxable amount (most do), and whether local tax stacks on state tax (about 35 states have local tax).

## All-State Summary Table

| State | Tax (state%) | Local Tax Typical | Doc Fee Cap | Doc Fee Typical | Title Fee | Trade-In Tax Credit |
|-------|--------------|-------------------|-------------|-----------------|-----------|---------------------|
| AL    | 2%           | 2-4%              | None        | $599-799        | $20       | Yes |
| AK    | 0%           | 0-7.5%            | None        | $499-799        | $15       | N/A (no state tax) |
| AZ    | 5.6%         | 1-5%              | None        | $499-799        | $4        | Yes |
| AR    | 6.5%         | 1-5%              | None        | $499-899        | $10       | Yes |
| CA    | 7.25%        | 1-2%              | $85         | $85 (capped low)| $25       | No (CA does not allow trade-in credit) |
| CO    | 2.9%         | 1-5%              | None        | $499-799        | $7.20     | Yes |
| CT    | 6.35% (7.75% if >$50k) | 0% | None | $499-699 | $25 | Yes |
| DE    | 0% (4.25% doc fee) | 0% | N/A — fee structure | N/A | $35 | N/A |
| FL    | 6%           | 0.5-2% on first $5k only | None  | $799-1,499      | $77.25/$85.25 | Yes (see FL detail stub) |
| GA    | TAVT 6.6% one-time (no traditional sales tax) | N/A | None | $599-799 | $18 | Yes on TAVT (see GA detail stub) |
| HI    | 4% (GET)     | 0-0.5%            | None        | $399-499        | $5        | Yes |
| ID    | 6%           | 0-3%              | None        | $499-799        | $14       | Yes |
| IL    | 6.25%        | 0-4.75%           | $347.26 (2025) | $347.26 (legal max) | $155 | Yes (capped) |
| IN    | 7%           | 0%                | None        | $199-399        | $15       | Yes |
| IA    | 6%           | 0-1%              | None        | $499-180 (cap by some counties) | $25 | Yes |
| KS    | 6.5%         | 0-4%              | None        | $499-799        | $10       | Yes |
| KY    | 6%           | 0%                | None        | $499-799        | $9        | No |
| LA    | 4.45%        | 1-5%              | $200        | $200 (capped)   | $68.50    | Yes |
| ME    | 5.5%         | 0%                | None        | $499            | $33       | Yes |
| MD    | 6%           | 0%                | $300 (raised Nov 2024 from $200) | $300 (capped) | $50      | Yes (see MD detail stub) |
| MA    | 6.25%        | 0%                | None        | $499-799        | $75       | Yes |
| MI    | 6%           | 0%                | $230        | $230 (capped low) | $15     | Yes BUT capped at first $9k (2025; rises $1k/yr to uncapped 2029) — see MI detail stub |
| MN    | 6.5%         | 0-1.5%            | $125        | $125 (capped low) | $11     | Yes |
| MS    | 7% (5% trucks) | 0%             | None        | $499-799        | $9        | Yes |
| MO    | 4.225%       | 0-5.5%            | $599 (statutory cap as of 2024) | $499-599 | $11 | Yes |
| MT    | 0%           | 0%                | None        | $299-499        | $10.30    | N/A |
| NE    | 5.5%         | 0-2%              | None        | $499-799        | $10       | Yes |
| NV    | 6.85%        | 0-1.5%            | None        | $499-799        | $29       | Yes |
| NH    | 0%           | 0%                | None        | $399-599        | $25       | N/A |
| **NJ** | **6.625%** | 0%                | **$799 (legal cap)** | $499-799 | $60-85 | Yes |
| NM    | 4% (motor vehicle excise) | 0% | None | $399-499      | $5        | Yes |
| NY    | 4%           | 4-4.875%          | $175 (legal cap) | $175 (capped low) | $50 | Yes |
| NC    | 3% Highway Use Tax (NO traditional sales tax) | 0% | $129 (statutory cap) | $129 (capped) | $52 | Yes on HUT (see NC detail stub) |
| ND    | 5%           | 0-3%              | None        | $399-499        | $5        | Yes |
| OH    | 5.75%        | 0.25-2.25%        | $250 (statutory cap) | $250 (capped low) | $15 | Yes (see OH detail stub) |
| OK    | 4.5% (excise 3.25%) | 0-7%      | None        | $499-799        | $11       | Partial |
| OR    | 0%           | 0%                | None        | $115 (CAT applies for new) | $122 | N/A |
| PA    | 6%           | 1-2% (Philly/Allegheny) | None  | $499-999        | $58       | Yes |
| RI    | 7%           | 0%                | $250        | $250 (capped low) | $52    | Yes |
| SC    | 5% IMF (capped $500 / vehicle) | 0% | None | $399-499 | $15 | Yes |
| SD    | 4.5% (excise)| 0-2%              | None        | $399-499        | $10       | Yes |
| TN    | 7%           | 1.5-2.75%         | None        | $499-899        | $11       | Yes |
| TX    | 6.25% (motor vehicle sales tax) | 0% | $150 (legal cap) | $150 | $33 | Yes |
| UT    | 4.85%        | 1-3%              | None        | $499-799        | $6        | Yes |
| VT    | 6%           | 0%                | None        | $599 (typical)  | $35       | Yes |
| VA    | 4.15% (motor vehicle SUT, min $75) | 0-1% local | $599 (statutory cap) | $599 (capped) | $15 | **NO** (VA does NOT grant trade credit — see VA detail stub) |
| WA    | 6.5% (MVET 0.3% extra) | 0.5-3.5% | $200        | $200 (capped low) | $15    | Yes (see WA detail stub) |
| WV    | 6% (privilege tax)| 0%             | $199        | $199 (capped low) | $15    | Yes |
| WI    | 5%           | 0-0.5%            | None        | $399-499        | $164.50   | Yes |
| WY    | 4%           | 0-2%              | None        | $399-499        | $15       | Yes |
| DC    | 6-9% excise by weight class on first $40k MSRP, higher tier above | 0% | None | $599-899 | $26 | Yes (see DC detail stub) |

Notes:
- **Doc Fee Cap "None"** means no statutory cap. Dealers can charge whatever, but $499-899 is typical industry range.
- **Trade-In Tax Credit** indicates whether sales tax applies to the net price after trade-in deduction. Most states allow this credit; CA, KY, DC are notable exceptions.
- **CA Doc Fee Capped at $85** is one of the strongest consumer protections in the US.
- **NY Doc Fee Capped at $175** is the second strongest.
- **DE has no sales tax** but charges a 4.25% "document fee" on the purchase price plus title — functionally similar to sales tax.
- **OR, MT, NH have no state sales tax.** AK has no state tax but most boroughs charge local sales tax.

## Sub-State Tax Stacking

In states with local sales tax (CA, CO, IL, KS, LA, NV, NY, OH, OK, TN, TX (none), UT, WA, etc.), the combined rate is:

```
Combined rate = State rate + County rate + City rate (optional) + Special district (optional)
```

Example: California state 7.25% + Alameda County 1% + Oakland 0.5% = 8.75% combined.

For OTD math, use the **combined rate at the buyer's residence ZIP code**, not the dealer's location. The state collects tax based on where the vehicle is titled and registered.

## High-Tax States to Watch

| State | Combined Rate (typical) | Notes |
|-------|-------------------------|-------|
| LA    | 9-10%                   | State 4.45% + local up to 5% |
| TN    | 9-10%                   | State 7% + local 2.5-2.75% |
| AR    | 9-10%                   | State 6.5% + local |
| NY    | 8-9%                    | State 4% + local 4-5% |
| WA    | 9-10%                   | State 6.5% + MVET + local |
| NV    | 8-9%                    | State 6.85% + local |
| IL    | 8-9%                    | State 6.25% + local up to 4.75% |

In high-tax states, a $30,000 sales price can incur $2,700-3,000 in tax alone. Cross-state buying (titling in a lower-tax state if you genuinely reside there) can save thousands but requires legitimate residency and is not a tax evasion strategy for ordinary buyers.

## Low-Tax / No-Tax States

| State | Notes |
|-------|-------|
| OR    | No state sales tax; CAT applies on new car dealers, not buyers |
| MT    | No state sales tax; favorable LLC residency for some out-of-state buyers (controversial) |
| NH    | No state sales tax; pay only registration ~$25-100 |
| DE    | "Document fee" 4.25% but no separate sales tax |
| AK    | No state sales tax; some boroughs add local 0-7.5% |

## Cross-State Titling Math

For a buyer in State A buying from a dealer in State B:

- **Sales tax** is paid based on where the vehicle will be registered (State A), not where the dealer is located (State B). Out-of-state dealers should NOT charge their own state's sales tax for cars going out of state.
- **Doc fee** is charged by the dealer; depends on the dealer's state laws.
- **Title fee** is charged at registration in State A.
- **Registration fee** is paid to State A's DMV.
- **Cross-state title transfer fees** may apply (~$150-300) for out-of-state titles being titled fresh in the buyer's state.

Common cross-state buying patterns and their tax implications:

| Buyer State | Dealer State | Tax Paid | Doc Fee | Notes |
|-------------|--------------|----------|---------|-------|
| NJ          | NY (Manhattan) | NJ 6.625% | NY $175 (capped) | Save on doc fee, pay NJ tax |
| NJ          | PA           | NJ 6.625% | PA no cap (typ $499-999) | PA dealer should not charge PA tax |
| PA (19010 Montgomery County, flat 6%) | NJ (Cherry Hill / Marlton) | PA 6% (paid at PennDOT, not collected by NJ dealer) | NJ ≤ $799 (legal cap) | NJ dealer should NOT charge NJ 6.625%. Net advantage: lower-capped NJ doc fee vs PA's uncapped doc. |
| PA (19010) | DE (Wilmington / Newark) | PA 6% (paid at PennDOT) | DE typically $299-499 (DE has no statutory cap but DE dealers run low) | DE has no state sales tax; the DE 4.25% "document fee" applies to DE residents only. PA buyer pays only PA 6% at PennDOT. **DE = doc-fee sweet spot for PA buyers**: DE doc commonly $200-500 cheaper than equivalent PA dealer. |
| PA (19010) | MD (edge of Philly metro) | PA 6% (paid at PennDOT) | MD ≤ $499 (legal cap as of Nov 2024) | MD dealer should NOT charge MD 6% tax. Strongest doc protection in the PA radius. |
| CA          | NV           | CA combined (typ 8.75-9.5%) | NV $499-799 | NV dealer often shifts to CA tax |
| TX          | OK           | TX 6.25%  | OK $499-799      | Save on doc fee, pay TX tax |
| FL          | GA (Atlanta) | FL 6%     | GA $499-799      | GA TAVT 6.6% does NOT apply to out-of-state buyers |

## Common Hidden Add-Ons (Universal)

These should be refused or itemized separately, regardless of state:

- "Paint protection" / "Permaplate" / "Diamond Coat" — $500-2,000
- "Fabric/leather protection" — $200-500
- "Nitrogen-filled tires" — $100-200
- "Window etching" / "VIN etching" — $200-400
- "Theft deterrent / anti-theft package" — $300-1,000
- "Lojack / Skylink" — $400-700
- "Dealer prep" over $200 — non-negotiable should be ≤$200
- "Compliance fee" — vague, refuse
- "Reconditioning fee" — should be in sales price, not separate

## OTD Math Examples by State

### NJ Example (Mid-tax with doc fee cap)

Sales $25,000, Doc $499, NJ tax 6.625%:

```
Taxable = $25,000 + $499 = $25,499
Tax = $25,499 × 0.06625 = $1,689.31
Title = $85
Reg = $70
OTD = $25,000 + $499 + $1,689.31 + $85 + $70 = $27,343.31
```

### CA Example (High tax, low doc fee cap)

Sales $25,000, Doc $85 (CA cap), CA tax 8.75% (Bay Area combined):

```
Taxable = $25,000 + $85 = $25,085
Tax = $25,085 × 0.0875 = $2,194.94
Title = $25
Reg = $250
OTD = $25,000 + $85 + $2,194.94 + $25 + $250 = $27,554.94
```

CA's higher tax mostly offsets its lower doc fee cap. Total OTD is similar to NJ.

### OR Example (No state tax)

Sales $25,000, Doc $115:

```
Tax = $0
Title = $122
Reg = $100 (assume)
OTD = $25,000 + $115 + $0 + $122 + $100 = $25,337
```

OR has the cleanest OTD math.

### TX Example (Mid-tax with strong doc fee cap)

Sales $25,000, Doc $150 (TX cap), TX tax 6.25%:

```
Taxable = $25,000 + $150 = $25,150
Tax = $25,150 × 0.0625 = $1,571.88
Title = $33
Reg = $50 (assume)
OTD = $25,000 + $150 + $1,571.88 + $33 + $50 = $26,804.88
```

TX is one of the most buyer-friendly states for OTD: low doc fee, mid-range tax.

## Trade-In Tax Credit Math

In states allowing trade-in credit (most), trade-in value is subtracted from sales price BEFORE tax:

```
Taxable = (Sales price - Trade-in value) + Doc fee
```

Example NJ: Sales $30,000, Trade-in $10,000, Doc $499:

```
Taxable = ($30,000 - $10,000) + $499 = $20,499
Tax = $20,499 × 0.06625 = $1,358.06  (saves $662.50 vs no-trade)
```

In CA, KY, DC (no trade-in credit), the full sales price is taxed regardless of trade-in.

## Tri-State Detail Stubs (NJ / NY / PA)

Quick-reference stubs for the NJ tri-state core. The "Does NOT have" subsection lists fees that dealer CRM templates from OTHER states often try to slip in; absence of these in the registering state is grounds to demand a full re-quote (see SKILL.md gotcha D8).

### NJ — New Jersey
- **Sales tax**: 6.625% flat (no local-rate stacking on motor vehicles).
- **Doc fee cap**: **$799 (legal cap)**. Typical range $499-799.
- **Title fee**: $60-85. **Registration**: typical $60-120 first year, weight-based.
- **Trade-in tax credit**: Yes.
- **Has**: Supplemental titling fee on some financed transactions; tire fee $1.50/tire (rare on used retail dealer sales, sometimes appears as a $7.50 line for 5 tires incl. spare).
- **Does NOT have**: per-battery fee, environmental impact fee on used vehicles, CA-style smog fee, RI-style cap on doc, NY $175 doc cap.

### NY — New York
- **Sales tax**: 4% state + 4-4.875% local (NYC combined 8.875%).
- **Doc fee cap**: **$175 (legal cap — second strongest in US).** Typical $175.
- **Title fee**: $50. **Registration**: weight-based, typical $26-140 for 2-year passenger.
- **Trade-in tax credit**: Yes.
- **Has**: MCTD (Metropolitan Commuter Transportation District) $50 fee for NYC area registrations; tire recycling fee on new tires only ($2.50/tire) — not normally on used vehicle retail sales.
- **Does NOT have**: NJ-style supplemental titling fee, NJ $799 doc, CT luxury 7.75% tier, RI $250 doc cap, FL $77 title.

### PA — Pennsylvania
- **Sales tax**: 6% state base. **Local-rate disambiguation by ZIP**: Allegheny County (Pittsburgh metro, 150XX-152XX ZIPs) adds +1% (total 7%); Philadelphia (City + County, 191XX ZIPs) adds +2% (total 8%); **all other PA counties = flat 6%** (e.g., Bryn Mawr 19010 is Montgomery County, flat 6%; King of Prussia 19406 is Montgomery, flat 6%; West Chester 19380 is Chester, flat 6%). Confirm the buyer's registration ZIP is NOT in the 191XX or 150XX-152XX bands before defaulting to 6%.
- **Doc fee cap**: **No statutory cap.** Typical industry range $499-999 — **PA dealers run high** versus NJ's $799 cap or NY's $175 cap. Treat any PA doc above $899 as negotiable.
- **Title fee**: $58. **Registration**: $45/year typical for passenger vehicles (annual, not biennial).
- **Trade-in tax credit**: Yes — trade-in value is subtracted from sales price BEFORE 6% (or 7% / 8%) tax applies.
- **Has**: Public Transportation Assistance Fund tire fee $1/tire on NEW tires sold (not normally a line on used vehicle OTD); $5 lien fee if financed (auto loan recorded against title); $26 lien recording add-on at PennDOT.
- **Does NOT have**: NJ-style supplemental titling fee, CT luxury 7.75% tier, NY $175 doc cap, RI $250 doc cap, MD $499 doc cap, environmental impact fee, per-battery fee, CA-style smog fee. Any of these appearing on a PA-buyer quote is a state-template leak — see SKILL.md gotcha D8.

## New England States — Detail Stubs

Quick-reference stubs for CT, MA, RI, NH, ME, VT. Full breakdowns (registration formulas, county quirks, dealer-typical practices) to be filled by later iterations as actual buying cycles surface specifics. "Does NOT have" lines exist to catch dealer CRM template leaks from other states (see SKILL.md gotcha D8).

### CT — Connecticut
- **Sales tax**: 6.35% standard; **7.75%** on vehicles with sales price > $50,000 (luxury threshold).
- **Doc fee cap**: No statutory cap. Typical industry range $499-699.
- **Title fee**: $25. **Registration**: ~$120 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, NY MCTD fee, RI $250 doc cap. Any of these appearing on a CT quote indicates a state-template leak — demand full re-quote.

### MA — Massachusetts
- **Sales tax**: 6.25% flat. No local sales tax on vehicles.
- **Doc fee cap**: No statutory cap. Typical industry range $499-799.
- **Title fee**: $75. **Registration**: ~$60 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, NY MCTD fee, CT luxury 7.75% tier, local-rate stacking.

### RI — Rhode Island
- **Sales tax**: 7% flat.
- **Doc fee cap**: **$250** (capped low — strong buyer protection).
- **Title fee**: $52.50. **Registration**: ~$30-90 depending on weight.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, doc fee over $250 (cap is binding), NY MCTD fee.

### NH — New Hampshire
- **Sales tax**: **0% — no state sales tax on vehicles.** This is a structural advantage; an NH-resident buyer titling in NH pays no sales tax regardless of dealer state.
- **Doc fee cap**: No statutory cap. Typical industry range $399-599.
- **Title fee**: $25. **Registration**: town-based, formula on MSRP × age factor; typical $200-500 first year for newer vehicles.
- **Trade-in tax credit**: N/A (no sales tax).
- **Does NOT have**: any sales tax line at all (any sales-tax-rate appearing on an NH quote is a flat template leak), per-tire fee, NJ supplemental titling fee.

### ME — Maine
- **Sales tax**: 5.5% flat.
- **Doc fee cap**: No statutory cap. Typical industry range ~$499.
- **Title fee**: $33. **Registration**: ~$35 plus excise tax (mil rate × MSRP, declining with age) collected by town.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, local sales tax stacking, NY MCTD fee.

### VT — Vermont
- **Sales tax**: 6% flat (Purchase & Use Tax).
- **Doc fee cap**: No statutory cap. Typical industry range ~$599.
- **Title fee**: $35. **Registration**: ~$76 (1-year) / $140 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, local sales tax stacking, NY MCTD fee, CT luxury 7.75% tier.

## IL — Illinois (Detail Stub at CT/CA/TX Depth)

- **Sales tax**: 6.25% state base. **Local-rate stacking by ZIP** — IL has the most complex local stacking in the US after CA:
  - **Naperville (60540, DuPage County)**: 6.25% state + 1.25% DuPage = **7.5% combined**
  - **Chicago (606XX, Cook County)**: 6.25% state + 2.75% county + 1.25% city + RTA fees = **up to 10.25% combined** (highest large-city combined rate in the US)
  - **Suburban Cook County**: 6.25% state + 1.75% county + 0.5-1% city = 8-9% combined
  - **DuPage County (Naperville, Aurora, Wheaton)**: flat 7.5% combined
  - **Will County (Joliet, Bolingbrook, Plainfield 60544)**: 7-7.25% combined
  - **Kane County (St. Charles, Geneva, Aurora-Kane portion)**: 7-7.5% combined
  - **Lake County (Waukegan, Libertyville)**: 7-8% combined
  - Always confirm the buyer's registration ZIP combined rate before defaulting — DuPage (60540) != Cook (606XX).
- **Doc fee cap**: **$347.26 (legal cap as of 2025)**. **Highest doc-fee cap in the US.** Updated annually for inflation (Illinois Vehicle Code 625 ILCS 5/5-101.1; CPI-linked). PA dealers run $499-999 uncapped; IL dealers are statute-bound. Treat any IL quote with doc above $347.26 as a leak — flat illegal under IL law.
- **Title fee**: $155 (one of higher US title fees). **Registration**: $151/yr passenger vehicle. **Plate transfer**: ~$26 (transfer from trade vehicle to new vehicle — cheaper than new-plate issuance).
- **License + Emissions inspection ("LE")**: $20 for emissions-test counties (Cook, DuPage, Kane, Lake, Will, McHenry, Madison, Monroe, St. Clair). Other counties exempt.
- **Trade-in tax credit**: **YES BUT CAPPED at first $10,000 of trade allowance** (Illinois Vehicle Code; was uncapped pre-2020, capped 2020-2024 per Rivian-vs-Ford SB-690 lobbying compromise, **kept at $10k cap** through 2025+ — verify current legislation). A $12,000 trade allowance in IL only gets credit on $10,000 × combined rate. A $5,800 trade (the buyer's Ram) gets full credit ($5,800 × 7.5% = $435 tax savings in the buyer's Illinois county).
- **Has**: state Use Tax separately if buying from out-of-state dealer (IL Form RUT-25); county-level tax stacking per ZIP (5+ rate tiers in IL); plate transfer option ($26) vs new plate ($151 included in reg); LE/emissions inspection $20 in non-exempt counties.
- **Does NOT have**: NJ-style supplemental titling fee, NY MCTD fee, CT $50k luxury tier, RI $250 doc cap (IL's cap is $347.26), MD $499 cap, TX $200/yr EV reg premium, PA's uncapped doc tier, per-tire fee on retail used dealer sales, battery fee, CA-style smog fee, NC HUT, OK excise tax separate from sales tax. Any of these appearing on an IL-buyer quote is a state-template leak — demand full re-quote per gotcha D8.

### IL Worked OTD Example (no trade, Naperville 7.5%)

Sales $40,495 (post-counter), doc $347.26, IL Naperville 7.5%:

```
Taxable = $40,495 + $347.26 = $40,842.26
Tax     = $40,842.26 × 0.075 = $3,063.17
Title   = $155
Reg     = $151
LE      = $20
OTD     = $40,495 + $347.26 + $3,063.17 + $155 + $151 + $20 = $44,231.43
```

### IL Worked OTD Example (with $7,000 trade, $2,800 lien)

```
Sale price (locked):    $40,495
Doc:                    $347.26
Trade credit applied:   -$7,000 (full credit, below $10k cap)
Taxable base:           $40,495 + $347.26 - $7,000 = $33,842.26
Tax (7.5%):             $33,842.26 × 0.075 = $2,538.17
Title:                  $155
Reg:                    $151
LE:                     $20
OTD before trade-net:   $40,495 + $347.26 + $2,538.17 + $155 + $151 + $20 = $43,706.43

Trade allowance:        -$7,000 (applied to OTD reduction)
Lien payoff (Ally):     +$2,800 (dealer cuts check; routed from trade allowance)
Net trade equity:       $7,000 - $2,800 = $4,200

Cash out-the-door:      $43,706.43 - $4,200 (net trade equity) = $39,506.43

Tax savings from IL trade-tax credit: $7,000 × 7.5% = $525
```

If trade allowance had been $12,000 instead of $7,000:
- IL trade credit applies only to first $10,000 → $10,000 × 7.5% = $750 max tax saving
- Remaining $2,000 of trade allowance receives no tax credit (capped)

### IL Cross-State Titling Rows

| Buyer State | Dealer State | Tax Paid | Doc Fee | Notes |
|---|---|---|---|---|
| IL (60540 Naperville, DuPage 7.5%) | IN (Munster / Highland / Hammond, 46XXX) | IL 7.5% (paid at IL SOS) | IN typ $279-399 (IN doc cap $199 statutory but many IN dealers add fees) | IN dealer should NOT charge IN 7% tax; IL buyer pays IL 7.5% at IL SOS titling. **IN doc cap $279 vs IL $347.26**: IN doc is $68 cheaper. Cross-state IL→IN small advantage. |
| IL (60540) | WI (Kenosha / Pleasant Prairie, 53XXX) | IL 7.5% (paid at IL SOS) | WI no statutory doc cap (typ $399-499) | WI dealer should NOT charge WI 5% tax. **WI doc typ $399-499 = $50-150 more than IL $347.26 cap**. Cross-state IL→WI net advantage flips negative on doc; net effect: nil for IL buyer (tax same, doc slightly more). |
| IL (60540) | MO (border zones — IL→MO uncommon for Chicagoland) | IL 7.5% (paid at IL SOS) | MO doc cap $599 statutory | MO doc cap $599 > IL $347.26. No advantage. |
| IL (60540) | IA (Quad Cities border, 522XX→527XX) | IL 7.5% (paid at IL SOS) | IA doc typ $499 | No advantage. |
| IL (606XX Chicago, 10.25%) | IN (Lake County / Hammond) | IL 10.25% (paid at IL SOS) | IN doc cap $279 | Chicago buyers face the highest combined US tax (10.25%) — cross-state buys don't reduce tax burden because IL SOS collects IL tax regardless of dealer location. The cross-state move only saves $68 on doc. |

**IL has no structural cross-state arbitrage advantage** — IL's combined tax stacking is high enough that even no-tax-state dealers (DE, NH, OR) far from Chicagoland would lose to local IL on the doc cap. The exception is IL→IN ($68 doc savings), which is too small to drive cross-state buying decisions on its own; only relevant when an IN dealer happens to have the exact specific VIN at a price advantage.

## High-Population State Detail Stubs — FL / OH / NC / GA / MI / VA / WA + DC / MD

Quick-reference stubs for 7 high-population states plus DC and MD (commuter-corridor coverage paired with VA). Pattern matches CT / CA / TX / IL depth: tax + doc fee + title + reg + trade-in credit + "Does NOT have" leak list + cross-state rows + 2 worked OTD examples. last_verified: 2026-05-18

### FL — Florida

- **Sales tax**: 6% state + **county discretionary surtax** 0.5-2% applied **only to first $5,000** of taxable price (max $5,000 × 2% = $100 county surtax cap per vehicle). Combined effective: most counties land 6.5-8% on the first $5k then drop to flat 6% for the remaining sale price (e.g., Pinellas 7%, Miami-Dade 7%, Hillsborough 7.5%, Orange 6.5%, Broward 7%, Duval 7.5%). The **$5,000 surtax ceiling** is a structural FL quirk: a $40,000 sale taxed at Pinellas 7% county doesn't pay 7% on $40k, it pays 6% × $40,000 + 1% × $5,000 = $2,450 (effective 6.125%), not $2,800. Always apply the FL ceiling math at OTD calculation.
- **Doc fee cap**: **No statutory cap.** Typical industry range $799-1,499 — **FL dealers run high**, often the highest in the US. Treat any FL doc above $999 as negotiable and any above $1,299 as a Phase 6 first-counter demand-removal item per gotcha D8/D9 pattern.
- **Title fee**: $77.25 new title / $85.25 with lien recording (high vs typical $15-50). **Registration**: weight-based, $46-95 first year + tag fee, then $46-72 renewal.
- **Trade-in tax credit**: **YES** — sale price minus trade allowance is the tax base (with FL surtax ceiling applied to net taxable, not gross).
- **Has**: title surcharge for "initial registration fee" $225 first-time FL registrations (out-of-state buyers transferring to FL hit this — counts as a one-time-only fee for the first FL registration of any vehicle in the buyer's name); lemon law fee $2/vehicle; battery fee $1.50/battery (rare on used retail).
- **Does NOT have**: no state income tax (this drives FL as destination state for retirees + out-of-state buyers); no NY MCTD fee; no CA-style luxury tier; no CA smog inspection; no IL emissions inspection requirement statewide (some counties test); no NC highway use tax; no MI trade-in cap; no PA Philly/Allegheny local stacking; no doc fee cap (this is a leak vector in the OPPOSITE direction — FL has no cap so high doc fees are legal, just negotiable).

#### FL Worked OTD Example (no trade, Pinellas County 7% on first $5k)

Sales $32,500, doc $1,199 (negotiated down from $1,499 quote), Pinellas 6% state + 1% county on first $5k:

```
Taxable                     = $32,500 + $1,199 = $33,699
State tax (6%)              = $33,699 × 0.06 = $2,021.94
County surtax (1% × $5,000) = $50.00
Title (new with lien)       = $85.25
Reg                         = $72
Initial reg fee             = $225 (first FL reg)
OTD = $32,500 + $1,199 + $2,021.94 + $50 + $85.25 + $72 + $225 = $36,153.19
```

#### FL Worked OTD Example (with $8,000 trade, Miami-Dade 7%)

Sales $35,000, doc $999, trade $8,000, Miami-Dade 6% state + 1% county on first $5k of net taxable:

```
Net sale before doc         = $35,000 - $8,000 trade = $27,000
Taxable                     = $27,000 + $999 = $27,999
State tax (6%)              = $27,999 × 0.06 = $1,679.94
County surtax (1% × $5,000) = $50.00
Title                       = $77.25
Reg                         = $60
OTD before trade-net        = $35,000 + $999 + $1,679.94 + $50 + $77.25 + $60 = $37,866.19
Trade allowance applied     = -$8,000
Cash OTD                    = $29,866.19
Tax savings from trade credit: $8,000 × 6% (state only, surtax already capped) = $480
```

### OH — Ohio

- **Sales tax**: 5.75% state base + county/transit district 0.25%-2.25% (typical combined 6.5-8%). Cuyahoga (Cleveland 44XXX) 8%, Franklin (Columbus 432XX) 7.5%, Hamilton (Cincinnati 452XX) 7.8%, Summit (Akron 443XX) 6.75%, Montgomery (Dayton 454XX) 7.5%, Lucas (Toledo 436XX) 7.75%. Confirm buyer's registration ZIP combined rate.
- **Doc fee cap**: **$250 (statutory cap)** — among the lowest in the US (only IL $347, RI $250, MI $230, WA $200, TX $150, NY $175, CA $85 are comparable or lower). OH doc-fee compliance is mechanically enforced; treat any OH quote with doc above $250 as a flat illegal leak.
- **Title fee**: $15 + $5 lien recording if financed = $20 with lien. **Registration**: $35 base + $3-91 by axle/weight (passenger sedan typical $50-65/yr).
- **Trade-in tax credit**: **YES** — full trade allowance subtracted from sales price before tax.
- **Has**: $5 lien fee (financed sales only); axle-based commercial vehicle surcharge.
- **Does NOT have**: no CA-style smog inspection (Ohio has e-check emissions in 6 Cleveland-area counties only — Cuyahoga, Lake, Lorain, Geauga, Medina, Portage; rest of state exempt); no NJ supplemental titling; no NY MCTD; no IL emissions $20 add-on; no FL initial registration fee; no NC highway use tax; no PA Philly local stacking; no MI trade-in cap.

#### OH Worked OTD Example (Cleveland Cuyahoga 8%, no trade)

Sales $24,500, doc $250 (OH cap), Cuyahoga 8%:

```
Taxable = $24,500 + $250 = $24,750
Tax     = $24,750 × 0.08 = $1,980.00
Title   = $20 (with lien)
Reg     = $55
OTD     = $24,500 + $250 + $1,980 + $20 + $55 = $26,805
```

#### OH Worked OTD Example (Columbus Franklin 7.5%, $6,500 trade)

Sales $28,000, doc $250, trade $6,500, Franklin 7.5%:

```
Net taxable price = $28,000 - $6,500 = $21,500
Taxable           = $21,500 + $250 = $21,750
Tax               = $21,750 × 0.075 = $1,631.25
Title             = $15
Reg               = $50
OTD before trade  = $28,000 + $250 + $1,631.25 + $15 + $50 = $29,946.25
Trade applied     = -$6,500
Cash OTD          = $23,446.25
Tax savings       = $6,500 × 7.5% = $487.50
```

### NC — North Carolina

- **NC has NO traditional sales tax on motor vehicles.** Instead, NC applies a **Highway Use Tax (HUT) of 3%** on the purchase price (or fair market value if higher than purchase price) at title issuance. This is the structural NC quirk — agents must explicitly use "HUT 3%" not "sales tax 3%" in communications, and dealer CRM templates that try to apply 5-7% "sales tax" are a flat error (gotcha D8 leak — demand full re-quote).
- **HUT cap**: $250 for commercial vehicles only (not passenger); passenger vehicles pay full 3% with no upper cap.
- **Doc fee cap**: **$129 (statutory cap, NCGS § 20-101.1)** — second-lowest in the US after CA $85. NC doc-fee leaks are common from out-of-state CRM templates (FL, GA, VA dealers in border zones often charge their own state's $599-799 doc on NC buyers). Treat any NC doc above $129 as a flat illegal leak.
- **Title fee**: $52 (new title). **Registration**: $36-89/yr by vehicle class (passenger sedan typical $38.75).
- **Trade-in tax credit**: **YES on HUT** — full trade allowance subtracted from sale price before 3% HUT.
- **Has**: $20 plate transfer fee (if transferring from previous NC vehicle); $40 inspection fee (annual safety + emissions in 19 counties — Mecklenburg, Wake, Durham, Guilford, etc.).
- **Does NOT have**: no traditional sales tax on cars at all (any "sales tax" line on an NC quote is a leak); no NY MCTD; no NJ supplemental titling; no FL initial registration fee; no PA local stacking; no CA luxury tier; no IL emissions $20; no GA TAVT (NC's HUT replaces both); no VA SUT (different mechanism, different rate); no MI trade-in cap.

#### NC Worked OTD Example (Charlotte Mecklenburg, no trade)

Sales $26,000, doc $129 (NC cap), HUT 3%:

```
Taxable = $26,000 + $129 = $26,129
HUT     = $26,129 × 0.03 = $783.87
Title   = $52
Reg     = $38.75
Inspect = $40
OTD     = $26,000 + $129 + $783.87 + $52 + $38.75 + $40 = $27,043.62
```

NC HUT 3% on a $26k vehicle = $783.87 vs FL 6% same vehicle ~$1,560 = **$776 NC structural advantage** purely from the tax rate, before doc-fee savings.

#### NC Worked OTD Example (Raleigh Wake, $9,000 trade)

Sales $32,000, doc $129, trade $9,000, HUT 3%:

```
Net sale     = $32,000 - $9,000 = $23,000
Taxable      = $23,000 + $129 = $23,129
HUT          = $23,129 × 0.03 = $693.87
Title        = $52
Reg          = $40
Inspect      = $40
OTD bef trade = $32,000 + $129 + $693.87 + $52 + $40 + $40 = $32,954.87
Trade        = -$9,000
Cash OTD     = $23,954.87
HUT savings  = $9,000 × 3% = $270
```

### GA — Georgia

- **Sales tax**: **GA does NOT use traditional sales tax on most vehicle purchases.** Instead, GA applies a **Title Ad Valorem Tax (TAVT) of 6.6% one-time** at vehicle registration, calculated on the fair market value (typically the GA DOR's Motor Vehicle Assessment Manual value, not the sale price — this is a structural quirk that can cut both ways: GA DOR FMV can be HIGHER than sale price for distressed/high-mileage cars, costing buyer; or LOWER for premium-trim/low-mileage cars, saving buyer). TAVT replaced GA's annual ad valorem ("birthday tax") in 2013 for vehicles purchased after March 1, 2013 — Georgia residents pay TAVT once at purchase, then $20/yr renewal with no annual ad valorem.
- **TAVT base value rule**: GA DOR FMV from Motor Vehicle Assessment Manual; if no FMV available, sale price is used. Agents must check DOR FMV vs sale price at Phase 2 — if FMV materially exceeds sale, the TAVT bill will be higher than the buyer expects.
- **Doc fee cap**: **No statutory cap.** Typical industry range $599-799 (typical GA dealers run mid-range vs FL's high $999-1,499). Treat above $899 as negotiable.
- **Title fee**: $18. **Registration**: $20/yr base + $76 emissions in metro Atlanta 13-county zone (Cherokee, Clayton, Cobb, Coweta, DeKalb, Douglas, Fayette, Forsyth, Fulton, Gwinnett, Henry, Paulding, Rockdale).
- **Trade-in tax credit**: **YES on TAVT** — trade allowance subtracted from sale price/FMV before 6.6% TAVT.
- **Has**: $1 lien fee; "ad valorem" line item ONLY for vehicles purchased pre-2013 still on annual ad valorem (irrelevant for new buyers); GA Power Combat Veteran exemption ($0 TAVT for qualifying); $200 alternative fuel vehicle fee for EVs/hybrids replacing fuel tax.
- **Does NOT have**: no traditional sales tax on titled vehicles (any "sales tax 4%" line is a leak — GA's general 4% sales tax applies to most retail but NOT to vehicle purchases that get TAVT); no annual ad valorem on 2013+ vehicles; no NY MCTD; no NJ supplemental titling; no FL surtax ceiling; no MI trade-in cap; no IL emissions $20 (GA has its own $76 emissions in 13 metro counties only).

#### GA Worked OTD Example (Atlanta Fulton County, no trade)

Sales $29,500 (matches DOR FMV), doc $699, TAVT 6.6%:

```
TAVT base       = $29,500 + $699 = $30,199 (TAVT applies to total)
TAVT (6.6%)     = $30,199 × 0.066 = $1,993.13
Title           = $18
Reg + emissions = $20 + $76 = $96
Alt-fuel fee    = $0 (non-EV)
OTD = $29,500 + $699 + $1,993.13 + $18 + $96 = $32,306.13
```

#### GA Worked OTD Example (Savannah Chatham County, $10,000 trade)

Sales $36,000 (DOR FMV $34,500 — sale price is HIGHER, but TAVT uses sale price since dealer transaction), doc $799, trade $10,000, TAVT 6.6%:

```
Net sale  = $36,000 - $10,000 = $26,000
TAVT base = $26,000 + $799 = $26,799
TAVT      = $26,799 × 0.066 = $1,768.73
Title     = $18
Reg       = $20 (Chatham not in 13-county emissions zone)
OTD bef trade = $36,000 + $799 + $1,768.73 + $18 + $20 = $38,605.73
Trade     = -$10,000
Cash OTD  = $28,605.73
TAVT savings: $10,000 × 6.6% = $660
```

### MI — Michigan

- **Sales tax**: 6% flat state, **no local stacking on motor vehicles** (Michigan is one of the cleanest tax structures — same 6% statewide for vehicles).
- **Doc fee cap**: **$230 (statutory cap, MCL 257.217e)** — among lowest in US (parallels OH $250, RI $250, MI $230, WA $200, NY $175, CA $85, IL $347.26). Treat any MI doc above $230 as flat illegal leak.
- **Title fee**: $15. **Registration**: ad-valorem by MSRP, declining annually (typical $30-200/yr for passenger; high-trim trucks/SUVs hit $200+).
- **Trade-in tax credit**: **YES BUT CAPPED.** Michigan caps trade-in credit at **first $9,000 of trade value (2025; rises $1,000/year until uncapped by 2029)**. Above $9k trade allowance receives no tax credit. This is the MI quirk: a $20,000 trade in MI gets credit only on $9,000 × 6% = $540 max tax savings, vs uncapped states like NJ/OH/CA where $20k × 6%+ would save $1,200+. Verify current-year cap (2025 = $9k; 2026 = $10k; 2027 = $11k; 2028 = $12k; 2029 = uncapped per Public Act 1 of 2018 phase-in).
- **Has**: $5 lien recording; transfer fee $9 (plate transfer when bringing existing plate); $100 EV registration surcharge + $30 hybrid surcharge (replacing gas-tax shortfall).
- **Does NOT have**: no local sales tax stacking on vehicles; no NY $175 doc cap (MI's $230 is similar bracket); no NY MCTD; no NJ supplemental titling; no IL emissions $20; no CA smog; no FL surtax ceiling; no GA TAVT system; no NC HUT; no PA Philly local stacking; no VA "no-trade-credit" rule (MI grants credit, just capped).

#### MI Worked OTD Example (Detroit Wayne, no trade)

Sales $28,000, doc $230 (MI cap), MI 6%:

```
Taxable = $28,000 + $230 = $28,230
Tax     = $28,230 × 0.06 = $1,693.80
Title   = $15
Reg     = $120 (ad-valorem on $28k MSRP)
OTD     = $28,000 + $230 + $1,693.80 + $15 + $120 = $30,058.80
```

#### MI Worked OTD Example (Grand Rapids Kent, $12,000 trade — exceeds 2025 cap)

Sales $34,000, doc $230, trade $12,000 (cap = $9,000 in 2025), MI 6%:

```
Capped trade credit applied = $9,000 (not full $12,000)
Net taxable                  = $34,000 - $9,000 = $25,000
Taxable                      = $25,000 + $230 = $25,230
Tax                          = $25,230 × 0.06 = $1,513.80
Title                        = $15
Reg                          = $150
OTD before trade             = $34,000 + $230 + $1,513.80 + $15 + $150 = $35,908.80
Trade applied (full)         = -$12,000
Cash OTD                     = $23,908.80
Tax savings (capped)         = $9,000 × 6% = $540 (not $720 if uncapped)
MI cap penalty               = ($12,000 - $9,000) × 6% = $180 lost vs uncapped state
```

If buyer trades $12k in 2027 instead, cap = $11k → tax savings $660 (better but still $60 below uncapped).

### VA — Virginia (DC commuter corridor)

- **Sales tax**: 4.15% state Motor Vehicle SUT (Sales and Use Tax) + 1% local in some localities (combined effective 4.15-5.15%; most VA buyers pay flat 4.15%). **Minimum SUT $75** — for very low-price purchases (<$1,800), VA charges a $75 floor.
- **Doc fee cap**: **$599 (statutory cap, VA Code § 46.2-1530.1).** Treat any VA quote with doc above $599 as flat illegal leak.
- **Title fee**: $15 (new title). **Registration**: $35-46/yr by weight class (passenger sedan typical $40.75/yr).
- **Trade-in tax credit**: **NO. VA does NOT grant trade-in tax credit on the 4.15% SUT.** This is the VA quirk — unique among DC-area neighbors (DC = yes, MD = yes, VA = no). A $10,000 trade in VA saves $0 in tax; same trade in MD saves $600. VA buyers should NOT structure deals as "trade reduces taxable price" — full sale price is taxed regardless of trade.
- **Has**: $64.50/yr Hybrid + EV registration fee; $40.75/yr personal property tax assessed by city/county (Fairfax, Arlington, Loudoun rates vary 3.5-4.57% of NADA value/year — separate from purchase SUT, but a recurring cost VA buyers must plan for); inspection $20/yr.
- **Does NOT have**: NO trade-in tax credit (the structural quirk); no NY MCTD; no NJ supplemental titling; no DC excise weight scaling; no MD doc cap $300 (VA's is $599 — higher than MD); no NC HUT (VA has SUT, different mechanism); no GA TAVT; no IL emissions $20; no FL surtax ceiling; no MI trade-in cap (because VA has no trade credit at all); no PA Philly local stacking.

#### VA Worked OTD Example (Arlington 22203, DC commuter, no trade)

Sales $33,000, doc $599 (VA cap), VA SUT 4.15%:

```
Taxable = $33,000 + $599 = $33,599
SUT     = $33,599 × 0.0415 = $1,394.36 (above $75 minimum)
Title   = $15
Reg     = $40.75
Inspect = $20
OTD     = $33,000 + $599 + $1,394.36 + $15 + $40.75 + $20 = $35,069.11
```

Note: Arlington personal property tax of ~4.4% × NADA value will hit at Oct/Nov each year separately from this OTD.

#### VA Worked OTD Example (Fairfax 22030, $8,000 trade — NO credit benefit)

Sales $30,000, doc $599, trade $8,000, VA SUT 4.15%:

```
Net sale (cash)   = $30,000 - $8,000 = $22,000
Taxable           = $30,000 + $599 = $30,599 (TRADE NOT DEDUCTED — VA quirk)
SUT               = $30,599 × 0.0415 = $1,269.86
Title             = $15
Reg               = $40.75
OTD before trade  = $30,000 + $599 + $1,269.86 + $15 + $40.75 = $31,924.61
Trade applied     = -$8,000 (cash reduction, not tax base reduction)
Cash OTD          = $23,924.61
Tax savings       = $0 (VA does not grant trade credit)
Compare same deal in MD: $8,000 × 6% = $480 tax savings missed by being in VA.
```

### WA — Washington

- **Sales tax**: 6.5% state + 0.5-3.5% local (combined 8.5-10.4%; Seattle 10.25%, Tacoma 10.3%, Bellevue 10.1%, Spokane 8.9%, Olympia 9.4%). **Plus MVET 0.3%** (Motor Vehicle Excise Tax) on top of sales tax = effective 8.8-10.7% combined for the registering ZIP.
- **Doc fee cap**: **$200 (statutory cap, RCW 46.12.555).** Treat any WA quote with doc above $200 as flat illegal leak.
- **Title fee**: $15. **Registration**: ad-valorem by vehicle value, typical $50-200/yr for passenger; high-value vehicles can hit $300-500/yr due to MVET surcharge component.
- **Trade-in tax credit**: **YES** — full trade allowance subtracted before sales tax (and MVET).
- **Has**: $75 EV registration surcharge + $30 electric motorcycle; $30 transportation electrification fee on EVs; $1.50/tire fee on new tires (rare on used retail); $7 ferry surcharge for puget sound counties.
- **Does NOT have**: no state income tax (WA structural advantage — but vehicle ad-valorem reg makes the differential smaller than buyers expect); no smog inspection (WA discontinued state emissions program 2020); no NY MCTD; no NJ supplemental titling; no GA TAVT; no NC HUT; no FL initial registration fee; no MI trade-in cap; no IL emissions $20; no CA luxury tier; no PA Philly local stacking; no VA "no-trade-credit" rule.

#### WA Worked OTD Example (Seattle King 10.25%, no trade)

Sales $35,000, doc $200 (WA cap), Seattle combined 10.25% + MVET 0.3% = 10.55%:

```
Taxable = $35,000 + $200 = $35,200
Tax     = $35,200 × 0.1055 = $3,713.60
Title   = $15
Reg     = $130 (ad-valorem on $35k value)
OTD     = $35,000 + $200 + $3,713.60 + $15 + $130 = $39,058.60
```

WA Seattle 10.55% on $35k = $3,713 vs OR same vehicle (no tax) ~$0 = **$3,713 OR structural advantage** — drives the WA→OR cross-state magnet pattern below.

#### WA Worked OTD Example (Spokane 8.9%, $7,000 trade)

Sales $26,000, doc $200, trade $7,000, Spokane 8.9% + MVET 0.3% = 9.2%:

```
Net sale  = $26,000 - $7,000 = $19,000
Taxable   = $19,000 + $200 = $19,200
Tax       = $19,200 × 0.092 = $1,766.40
Title     = $15
Reg       = $80
OTD bef tr = $26,000 + $200 + $1,766.40 + $15 + $80 = $28,061.40
Trade     = -$7,000
Cash OTD  = $21,061.40
Tax savings: $7,000 × 9.2% = $644
```

### DC — District of Columbia

- **Sales tax / excise structure**: DC does NOT use traditional sales tax on vehicles. Instead, DC applies an **excise tax by vehicle weight class on first $40,000 of MSRP**, then a higher tier above $40k. Current rates (2026):
  - Class I (≤3,499 lbs): 6% on first $40k MSRP, 7% above $40k
  - Class II (3,500-4,999 lbs): 7% on first $40k MSRP, 8% above $40k
  - Class III (5,000-5,999 lbs): 8% on first $40k MSRP, 9% above $40k
  - Class IV (≥6,000 lbs): 8% on first $40k MSRP, 9% above $40k
  - EV exemption: alternative-fuel vehicles get $0 excise on first $40k (then standard above)
- **Doc fee cap**: **No statutory cap.** Typical DC dealer industry range $599-899; DC has only ~12 dealerships total, most are luxury-tier (Mercedes / BMW / Audi / Tesla Georgetown / Capitol Cadillac). Most DC residents register vehicles bought at VA / MD dealers.
- **Title fee**: $26 standard / by weight class. **Registration**: $72/yr biennial (paid every 2 years = $144 total for 2-year period; passenger).
- **Trade-in tax credit**: **YES** — sale price minus trade is the excise base.
- **Has**: $26 lien recording; $25 reflective plate fee; $100 EV charging infrastructure fee; emissions inspection biennial ($35).
- **Does NOT have**: no traditional sales tax (DC's excise structure is unique among US jurisdictions — closest analog is GA TAVT but DC scales by weight); no county stacking (DC = single jurisdiction, no sub-jurisdiction layering); no MD $300 doc cap (DC has no cap); no VA "no-trade-credit" rule; no NY MCTD; no NJ supplemental titling; no NC HUT; no FL surtax ceiling; no MI trade-in cap; no CA luxury tier; no IL emissions $20.

#### DC Worked OTD Example (Class II 4,200 lb Honda CR-V, $32,000 MSRP, no trade)

Sales $32,000 (under $40k MSRP threshold, all at 7%), doc $799, DC 7%:

```
Taxable = $32,000 + $799 = $32,799
Excise  = $32,799 × 0.07 = $2,295.93
Title   = $26
Reg     = $72 (annualized; $144 paid biennially)
Plate   = $25
OTD     = $32,000 + $799 + $2,295.93 + $26 + $72 + $25 = $35,217.93
```

#### DC Worked OTD Example (Class III 5,400 lb F-150, $52,000 MSRP, $9,000 trade)

Sales $52,000 (above $40k MSRP — tiered), doc $799, trade $9,000, DC Class III 8% on first $40k + 9% above:

```
Net sale          = $52,000 - $9,000 = $43,000 (taxable base after trade)
First $40k @ 8%   = $40,000 × 0.08 = $3,200.00
Above $40k @ 9%   = ($43,000 + $799 - $40,000) × 0.09 = $3,799 × 0.09 = $341.91
                    (doc fee taxable; pushes the above-$40k portion higher)
Total excise      = $3,200 + $341.91 = $3,541.91
Title             = $40 (heavier vehicle class)
Reg               = $72
Plate             = $25
OTD bef trade     = $52,000 + $799 + $3,541.91 + $40 + $72 + $25 = $56,477.91
Trade applied     = -$9,000
Cash OTD          = $47,477.91
Tax savings       = $9,000 × ~8.5% blended = ~$765
```

### MD — Maryland

- **Sales tax**: 6% flat state, **no local stacking** (MD is one of the cleanest tax structures — same 6% statewide for vehicles, parallel to MI).
- **Doc fee cap**: **$300 (statutory cap, MD Transportation § 15-311.1 raised from $200 in Nov 2024).** Treat any MD doc above $300 as flat illegal leak. **MD has the second-strongest doc-fee protection in the DC corridor** (DC no cap, VA $599, MD $300, PA no cap).
- **Title fee**: $50 (titling tax separately, not a fee). **Registration**: **$135 every 2 years** (biennial — passenger 3,700 lbs+; smaller cars $108 biennial). This is high vs typical $35-50/yr.
- **Trade-in tax credit**: **YES** — sale price minus trade is the taxable base.
- **Has**: $20 lien recording; $14 title-search fee; biennial vehicle safety inspection at sale only ($65-100 at certified station — required before title transfer for used cars sold by dealers; no annual recurring inspection like VA); $100 EV registration surcharge.
- **Does NOT have**: no local sales tax stacking; no VA "no-trade-credit" rule (MD grants credit — this is the structural MD advantage over VA for traded buyers in the DC commuter corridor); no DC excise weight scaling; no NY MCTD; no NJ supplemental titling; no PA Philly local stacking; no GA TAVT; no NC HUT; no FL surtax ceiling; no MI trade-in cap; no IL emissions $20 (MD has its own VEIP biennial emissions on most counties — Anne Arundel, Baltimore, Calvert, Carroll, Cecil, Charles, Frederick, Harford, Howard, Montgomery, Prince George's, Queen Anne's — $14); no CA luxury tier.

#### MD Worked OTD Example (Montgomery County 20850, DC commuter, no trade)

Sales $31,000, doc $300 (MD cap), MD 6%:

```
Taxable = $31,000 + $300 = $31,300
Tax     = $31,300 × 0.06 = $1,878.00
Title   = $50
Lien    = $20
Reg (biennial annualized) = $67.50/yr ($135/2yr)
VEIP    = $14
OTD     = $31,000 + $300 + $1,878 + $50 + $20 + $67.50 + $14 = $33,329.50
```

#### MD Worked OTD Example (Baltimore County 21204, $10,000 trade)

Sales $34,000, doc $300, trade $10,000, MD 6%:

```
Net sale          = $34,000 - $10,000 = $24,000
Taxable           = $24,000 + $300 = $24,300
Tax               = $24,300 × 0.06 = $1,458.00
Title             = $50
Reg (biennial)    = $135 (paid in full at registration)
VEIP              = $14
OTD before trade  = $34,000 + $300 + $1,458 + $50 + $135 + $14 = $35,957
Trade applied     = -$10,000
Cash OTD          = $25,957
Tax savings       = $10,000 × 6% = $600 (vs $0 in VA — the DC-corridor structural MD advantage)
```

### Cross-State Titling Rows — High-Pop States + DC Corridor

| Buyer State | Dealer State | Tax Paid | Doc Fee | Notes |
|---|---|---|---|---|
| FL (Pinellas 33701, 7% w/ surtax ceiling) | GA (Atlanta Fulton) | FL 6% + $50 county surtax cap | GA $599-799 (no cap) | GA TAVT 6.6% does NOT apply to out-of-state buyers; FL buyer pays only FL effective rate at FL DOR titling. GA doc typ $100-300 cheaper than FL $999-1,499 typical — small doc-fee advantage but FL initial reg fee $225 still applies if first FL registration. |
| FL (Miami-Dade 33101, 7% w/ ceiling) | AL (Mobile) | FL 6% + surtax | AL no cap (typ $599-799) | AL dealer should NOT charge AL 2% sales tax. AL doc similar to GA. Net: small advantage on doc, FL still pays $225 initial reg fee. |
| OH (Cleveland Cuyahoga 8%) | PA (Pittsburgh Allegheny 7%) | OH 8% (paid at OH BMV) | PA no cap (typ $499-999) | PA dealer should NOT charge PA 7%. PA doc typ $499-999 vs OH $250 cap. Net DISADVANTAGE on doc ($250-750 more in PA), no advantage on tax. OH→PA only worth it for specific VIN scarcity. |
| OH (Toledo Lucas 7.75%) | MI (Detroit Wayne 6%) | OH 7.75% (paid at OH BMV) | MI $230 cap | MI dealer should NOT charge MI 6%. MI doc $230 = $20 cheaper than OH $250 cap. Tax same buyer-state rate. Net: $20 advantage. |
| OH (Cincinnati Hamilton 7.8%) | IN (Indianapolis Marion) | OH 7.8% | IN typ $279-399 | IN dealer should NOT charge IN 7%. IN doc $30-150 more than OH $250 cap. Net disadvantage on doc. |
| OH (border 43XXX) | WV (Wheeling Ohio County) | OH 5.75-8% | WV $199 cap | WV doc $51 cheaper than OH cap. Tax same. Net: small advantage IF WV dealer has the VIN. |
| NC (Charlotte Mecklenburg) | VA (Bristol/Roanoke) | NC HUT 3% | VA $599 cap | VA dealer should NOT charge VA 4.15% SUT. NC HUT 3% is the buyer's rate. VA doc $599 = $470 MORE than NC $129. Net major doc disadvantage. NC buyers should stay in-state for doc savings; only cross-state for specific VIN scarcity. |
| NC (Raleigh Wake) | SC (Greenville Anderson) | NC HUT 3% | SC IMF capped $500/vehicle + doc typ $399-499 | SC has unique 5% Infrastructure Maintenance Fee (IMF) capped $500/vehicle in lieu of sales tax for out-of-state titles; SC dealer should NOT apply IMF to NC buyer. NC HUT applies. SC doc $270-370 MORE than NC $129. |
| NC (Asheville Buncombe) | TN (Knoxville Knox) | NC HUT 3% | TN no cap (typ $499-899) | TN dealer should NOT charge TN 9.25%. NC HUT applies. TN doc $370-770 MORE than NC $129. NC buyers cross-state to TN ONLY for specific VIN. |
| GA (Atlanta Fulton) | FL (Jacksonville Duval) | GA TAVT 6.6% (on FMV at GA registration) | FL $999-1,499 typ | FL dealer should NOT charge FL 6%. GA buyer pays TAVT at GA registration; FL doc 200-700 MORE than GA typical. Net disadvantage on doc. |
| GA (Savannah Chatham) | AL (Birmingham Jefferson) | GA TAVT 6.6% | AL similar to GA | AL dealer should NOT charge AL 2%. TAVT applies. Doc similar. |
| GA (Augusta Richmond) | SC (Aiken) | GA TAVT 6.6% | SC IMF capped $500 + doc $399-499 | SC IMF does NOT apply to GA buyer (out-of-state). GA TAVT applies at GA DOR. SC doc $200-300 LESS than GA typ $599-799 — small advantage if SC dealer has the VIN. |
| GA (Columbus Muscogee) | TN (Chattanooga Hamilton) | GA TAVT 6.6% | TN typ $499-899 | TN doc $100-300 more than GA typical. No advantage. |
| MI (Detroit Wayne) | OH (Toledo Lucas) | MI 6% (paid at MI SOS) | OH $250 cap | OH doc $20 cheaper than MI $230 cap. Tax same. Net: $20 advantage. |
| MI (Grand Rapids Kent) | IN (South Bend St. Joseph) | MI 6% | IN typ $279-399 | IN doc $49-169 MORE than MI cap. Net disadvantage. |
| VA (Arlington 22203, DC commuter) | DC (Georgetown) | VA 4.15% SUT, NO trade credit | DC no cap (typ $599-899) | DC dealer should NOT charge DC excise to VA buyer. VA SUT applies at VA DMV titling. DC doc typ $200-300 MORE than VA $599 cap. Trade-in: if buyer has trade, MD/DC sales would grant credit but VA registration does NOT — buyer pays full SUT regardless of dealer state. **VA buyers with trades: this is the structural disadvantage; consider relocating before purchase if trade is large.** |
| VA (Fairfax 22030) | MD (Bethesda Montgomery) | VA 4.15% SUT, NO trade credit | MD $300 cap | MD dealer should NOT charge MD 6%. VA SUT applies. MD doc $299 LESS than VA $599 cap — **MD = doc-fee sweet spot for VA buyers** (parallel to DE for PA buyers). Trade credit lost at VA DMV regardless of MD origin. |
| VA (Loudoun 20176) | WV (Charles Town Jefferson) | VA 4.15% SUT, NO trade credit | WV $199 cap | WV doc $400 LESS than VA $599 cap — even bigger doc savings than MD. WV dealer should NOT charge WV 6%. |
| VA (Norfolk 23508) | NC (Raleigh Wake) | VA 4.15% SUT | NC $129 cap | NC doc $470 LESS than VA $599 cap — best doc-fee cross-state from VA. NC dealer should NOT charge NC HUT to VA buyer. |
| DC (Capitol Hill 20003) | VA (Arlington) | DC excise by weight class | VA $599 cap | VA dealer should NOT charge VA 4.15%. DC excise applies at DC DMV. VA doc cheaper than DC's uncapped. **VA = doc-fee sweet spot for DC buyers** (parallel to DE for PA, MD for VA). |
| DC (Adams Morgan 20009) | MD (Silver Spring Montgomery) | DC excise | MD $300 cap | MD dealer should NOT charge MD 6%. DC excise applies. **MD doc $300 = lowest in DC corridor** — strongest doc protection. Net major advantage. |
| MD (Bethesda Montgomery) | VA (Tysons Corner Fairfax) | MD 6% (paid at MD MVA) | VA $599 cap | VA dealer should NOT charge VA 4.15%. MD 6% applies at MD MVA. VA doc $299 MORE than MD $300 cap. Net disadvantage on doc; tax depends on net trade-credit-adjusted comparison. |
| MD (Silver Spring Montgomery) | DC (Georgetown) | MD 6% | DC no cap | DC doc typically MORE than MD cap. No advantage. |
| MD (Baltimore County) | PA (border Harrisburg/York 17XXX) | MD 6% | PA no cap (typ $499-999) | PA doc typically $200-700 MORE than MD $300 cap. No advantage. |
| MD (Cecil County 219XX) | DE (Wilmington/Newark) | MD 6% | DE no cap (typ $299-499) | DE has no state sales tax but 4.25% doc fee for DE residents only — does NOT apply to MD buyer. MD 6% at MD MVA. DE doc $300-200 LESS than MD $300 cap effectively (or similar). **DE = doc-fee parity zone for MD buyers.** |
| WA (Seattle King 10.55%) | OR (Portland Multnomah) | WA 10.55% (paid at WA DOL) | OR typ $115 (CAT applies for new) | OR has NO state sales tax. OR dealer should NOT charge anything tax-side to WA buyer (but per WA-OR reciprocity rules, WA tax IS due at WA DOL titling — buyers attempting to register OR-purchased cars in WA cannot escape WA 10.55%). **WA→OR is a magnet for residency arbitrage (buying + registering in OR if buyer maintains OR address) but NOT for WA-residents who try to register in OR — WA DOL audits cross-border title transfers.** Doc: OR $115 vs WA $200 cap = $85 OR doc savings; minimal. |
| WA (Spokane 9.2%) | ID (Coeur d'Alene Kootenai) | WA 9.2% | ID no cap (typ $299-499) | ID dealer should NOT charge ID 6%. WA tax applies. ID doc $99-299 MORE than WA $200 cap. Net disadvantage on doc. |

### Cross-Corridor Structural Summary (DC Commuter)

The DC + VA + MD commuter corridor has 3 distinct doc-fee zones:

- **MD $300 cap** — strongest doc protection (parallels NY $175, IL $347, TX $150)
- **VA $599 cap** — moderate
- **DC no cap** — weakest but small dealer count limits impact

For a buyer with trade-in optionality across the corridor, the math:

- MD-registered: full trade credit at 6% — **structural winner** for traded buyers
- DC-registered: full trade credit at 6-9% weight-class — variable based on vehicle weight
- VA-registered: NO trade credit — **structural loser** for traded buyers regardless of dealer state

For a buyer with NO trade:

- VA 4.15% SUT — **structural winner** by tax rate (vs MD 6%, DC 6-9%)
- MD 6% flat
- DC 6-9% by weight class

Phase 1 buyer-type router should surface the trade-vs-no-trade DC-corridor split when buyer's ZIP is in 22XXX (VA) / 200XX-209XX (DC) / 207XX-219XX (MD).

## State-Specific Quirks

- **MD doc fee cap $300** (raised from $200 in November 2024 — second-strongest doc protection in DC corridor)
- **FL has no state income tax + no doc fee cap** — FL is a destination state for retirees/out-of-state buyers but FL dealers charge among the highest doc fees in the US ($999-1,499 typical, no statutory ceiling)
- **FL surtax ceiling on first $5,000** — county discretionary surtax (0.5-2%) only applies to first $5k of price, so total surtax is capped at ~$100 per vehicle regardless of sale price
- **FL first-time registration fee $225** — out-of-state buyers transferring to FL hit this one-time fee at first FL title issuance
- **OH doc fee cap $250** — among the strongest US protections (only TX $150, NY $175, CA $85 lower)
- **NC uses Highway Use Tax 3% (NOT sales tax)** — any "sales tax" line on an NC quote is a flat error; NC doc fee cap $129 is second-lowest in US (after CA $85)
- **GA uses TAVT 6.6% one-time at registration** — replaced annual ad valorem in 2013 for vehicles purchased after March 1, 2013; TAVT base is GA DOR FMV (Motor Vehicle Assessment Manual) OR sale price, whichever applies — agents must verify FMV at Phase 2 since FMV can be higher OR lower than sale price
- **MI trade-in tax credit capped at $9,000 (2025)** — rises $1k/year to uncapped by 2029 per Public Act 1 of 2018 phase-in
- **VA does NOT grant trade-in tax credit** — unique among DC-corridor states (DC=yes, MD=yes, VA=no); a $10k trade in VA saves $0 in tax vs $600 in MD same trade
- **DC excise tax by vehicle weight class** — not traditional sales tax; 4 weight tiers each with 2 brackets (first $40k MSRP vs above $40k); EV exemption on first $40k
- **WA combined tax can exceed 10.5% in Seattle** — state 6.5% + local up to 3.5% + MVET 0.3% = up to 10.55% Seattle; drives WA→OR residency arbitrage attempts (audited by WA DOL)
- **IL doc fee $347.26** is statutorily capped; updated annually for inflation. **Highest cap in US.**
- **IL trade-in tax credit capped at first $10,000** (Rivian-vs-Ford SB-690 outcome, in effect since 2020). Above $10k of trade allowance gets no tax credit.
- **IL combined local-rate stacking ranges from 6.25% (rural counties) to 10.25% (Chicago Cook City).** ZIP-by-ZIP variance is the largest in the US after CA.
- **NC uses "Highway Use Tax" 3%** instead of sales tax — much lower than typical
- **OK uses "excise tax" 3.25%** on vehicles, separate from local sales tax
- **VA minimum SUT $75** — small purchases have a floor
- **CT $50k threshold** — luxury cars above $50,000 face 7.75% instead of 6.35%

## When to Verify

Always verify state-specific fees with the dealer in writing before signing. Get an itemized OTD breakdown that matches the formula above. Reject any line items that do not fit the standard structure.
