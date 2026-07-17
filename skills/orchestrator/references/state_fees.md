# State-Specific Fees and Taxes, All 50 States + DC

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)
> **Data refresh schedule**: state rates / CPO programs / EV incentives / lease parameters should be re-verified annually or upon any user-cited deal that contradicts. The 2026-05-18 timestamp marks last full audit.

This reference covers the four major fee components for car purchases across all US states:

- Sales tax rate (state-level; some states add local county/city tax)
- Doc fee (legal cap or typical industry range)
- Title fee (one-time)
- Registration fee (typical for sedan/SUV, varies by weight)

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
| DE    | 0% (4.25% doc fee) | 0% | N/A, fee structure | N/A | $35 | N/A |
| FL    | 6%           | 0.5-2% on first $5k only | None  | $799-1,499      | $77.25/$85.25 | Yes (see FL detail stub) |
| GA    | TAVT 6.6% one-time (no traditional sales tax) | N/A | None | $599-799 | $18 | Yes on TAVT (see GA detail stub) |
| HI    | 4% (GET)     | 0-0.5%            | None        | $399-499        | $5        | Yes |
| ID    | 6%           | 0-3%              | None        | $499-799        | $14       | Yes |
| IL    | 6.25%        | 0-4.75%           | $347.26 (2025) | $347.26 (legal max) | $155 | Yes (capped) |
| IN    | 7%           | 0%                | $251.05 (2025, CPI-indexed) | $251.05 (legal max) | $15       | Yes |
| IA    | 6%           | 0-1%              | None        | $499-180 (cap by some counties) | $25 | Yes |
| KS    | 6.5%         | 0-4%              | None        | $499-799        | $10       | Yes |
| KY    | 6%           | 0%                | None        | $499-799        | $9        | No |
| LA    | 4.45%        | 1-5%              | $436 (2025, CPI-indexed) | $436 (capped)   | $68.50    | Yes |
| ME    | 5.5%         | 0%                | None        | $499            | $33       | Yes |
| MD    | 6%           | 0%                | $800 (raised eff. July 1 2024 from $500) | $499-799 | $50      | Yes (see MD detail stub) |
| MA    | 6.25%        | 0%                | None        | $499-799        | $75       | Yes |
| MI    | 6%           | 0%                | $230        | $230 (capped low) | $15     | Yes BUT capped at first $9k (2025; rises $1k/yr to uncapped 2029), see MI detail stub |
| MN    | 6.875%       | 0-1.5%            | $350 (eff. July 1 2025, raised from $125) | $350 (capped) | $11     | Yes |
| MS    | 7% (5% trucks) | 0%             | None        | $499-799        | $9        | Yes |
| MO    | 4.225%       | 0-5.5%            | $604.47 (2025, CPI-indexed) | $604.47 (legal max) | $11 | Yes |
| MT    | 0%           | 0%                | None        | $299-499        | $10.30    | N/A |
| NE    | 5.5%         | 0-2%              | None        | $499-799        | $10       | Yes |
| NV    | 6.85%        | 0-1.5%            | None        | $499-799        | $29       | Yes |
| NH    | 0%           | 0%                | $27 (state doc/title fee only; dealer admin fees uncapped) | $399-599 (dealer admin) | $25       | N/A |
| **NJ** | **6.625%** | 0%                | **$799 (legal cap)** | $499-799 | $60-85 | Yes |
| NM    | 4% (motor vehicle excise) | 0% | None | $399-499      | $5        | Yes |
| NY    | 4%           | 4-4.875%          | $175 (legal cap) | $175 (capped low) | $50 | Yes |
| NC    | 3% Highway Use Tax (NO traditional sales tax) | 0% | $129 (statutory cap) | $129 (capped) | $52 | Yes on HUT (see NC detail stub) |
| ND    | 5%           | 0-3%              | None        | $399-499        | $5        | Yes |
| OH    | 5.75%        | 0.25-2.25%        | $250 (statutory cap) | $250 (capped low) | $15 | Yes (see OH detail stub) |
| OK    | 4.5% (excise 3.25%) | 0-7%      | None        | $499-799        | $11       | Partial |
| OR    | 0% (0.5% privilege tax on new) | 0% | $250 (integrator) / $200 (eff. 2025-09-26) | $200-250 | $122 | N/A |
| PA    | 6%           | 1-2% (Philly/Allegheny) | None  | $499-999        | $58       | Yes |
| RI    | 7%           | 0%                | $250        | $250 (capped low) | $52    | Yes |
| SC    | 5% IMF (capped $500 / vehicle) | 0% | None | $399-499 | $15 | Yes |
| SD    | 4.5% (excise)| 0-2%              | None        | $399-499        | $10       | Yes |
| TN    | 7%           | 1.5-2.75%         | None        | $499-899        | $11       | Yes |
| TX    | 6.25% (motor vehicle sales tax) | 0% | $225 (OCCC safe-harbor, eff. 2024-07-11) | $225 | $33 | Yes |
| UT    | 4.85%        | 1-3%              | None        | $499-799        | $6        | Yes |
| VT    | 6%           | 0%                | None        | $599 (typical)  | $35       | Yes |
| VA    | 4.15% (motor vehicle SUT, min $75) | 0-1% local | $599 (statutory cap) | $599 (capped) | $15 | **NO** (VA does NOT grant trade credit, see VA detail stub) |
| WA    | 6.5% (MVET 0.3% extra) | 0.5-3.5% | $200        | $200 (capped low) | $15    | Yes (see WA detail stub) |
| WV    | 6% (privilege tax)| 0%             | $575 (eff. July 1 2024, CPI-indexed) | $575 (capped) | $15    | Yes |
| WI    | 5%           | 0-0.5%            | None        | $399-499        | $164.50   | Yes |
| WY    | 4%           | 0-2%              | None        | $399-499        | $15       | Yes |
| DC    | 6-9% excise by weight class on first $40k MSRP, higher tier above | 0% | None | $599-899 | $26 | Yes (see DC detail stub) |

Notes:
- **Doc Fee Cap "None"** means no statutory cap. Dealers can charge whatever, but $499-899 is typical industry range.
- **Trade-In Tax Credit** indicates whether sales tax applies to the net price after trade-in deduction. Most states allow this credit; CA, KY, DC are notable exceptions.
- **CA Doc Fee Capped at $85** is the lowest binding doc-fee cap in the US, the strongest consumer protection.
- **NC ($129), NY ($175), WA ($200), TX ($225 OCCC safe-harbor), MI ($230)** round out the next-lowest caps after CA. (NH's $27 is a state-title-fee cap only; NH dealer admin fees are uncapped.)
- **DE has no sales tax** but charges a 5.25% "document fee" (raised from 4.25% eff. 2025-10-01) on the purchase price plus title, functionally similar to sales tax. This is a state title document fee, not a dealer doc fee (DE does not cap dealer processing fees).
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
| PA (19010) | MD (edge of Philly metro) | PA 6% (paid at PennDOT) | MD ≤ $800 (legal cap eff. July 1 2024) | MD dealer should NOT charge MD 6% tax. No doc advantage, MD's $800 cap is high (above PA's typical $499-999 low end). |
| CA          | NV           | CA combined (typ 8.75-9.5%) | NV $499-799 | NV dealer often shifts to CA tax |
| TX          | OK           | TX 6.25%  | OK $499-799      | Save on doc fee, pay TX tax |
| FL          | GA (Atlanta) | FL 6%     | GA $499-799      | GA TAVT 6.6% does NOT apply to out-of-state buyers |

## Common Hidden Add-Ons (Universal)

These should be refused or itemized separately, regardless of state:

- "Paint protection" / "Permaplate" / "Diamond Coat", $500-2,000
- "Fabric/leather protection", $200-500
- "Nitrogen-filled tires", $100-200
- "Window etching" / "VIN etching", $200-400
- "Theft deterrent / anti-theft package", $300-1,000
- "Lojack / Skylink", $400-700
- "Dealer prep" over $200, non-negotiable should be ≤$200
- "Compliance fee", vague, refuse
- "Reconditioning fee", should be in sales price, not separate

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

### TX Example (Mid-tax with OCCC doc-fee safe harbor)

Sales $25,000, Doc $225 (TX OCCC safe-harbor, eff. 2024-07-11), TX tax 6.25%:

```
Taxable = $25,000 + $225 = $25,225
Tax = $25,225 × 0.0625 = $1,576.56
Title = $33
Reg = $50 (assume)
OTD = $25,000 + $225 + $1,576.56 + $33 + $50 = $26,884.56
```

TX is buyer-friendly for OTD: mid-range tax and a low presumed-reasonable doc amount ($225, OCCC safe-harbor, not a hard cap; above $225 requires an OCCC cost-justification filing). The widely-cited "$150 TX doc limit" is outdated.

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

### NJ, New Jersey
- **Sales tax**: 6.625% flat (no local-rate stacking on motor vehicles).
- **Doc fee cap**: **$799 (legal cap)**. Typical range $499-799.
- **Title fee**: $60-85. **Registration**: typical $60-120 first year, weight-based.
- **Trade-in tax credit**: Yes.
- **Has**: Supplemental titling fee on some financed transactions; tire fee $1.50/tire (rare on used retail dealer sales, sometimes appears as a $7.50 line for 5 tires incl. spare).
- **Does NOT have**: per-battery fee, environmental impact fee on used vehicles, CA-style smog fee, RI-style cap on doc, NY $175 doc cap.

### NY, New York
- **Sales tax**: 4% state + 4-4.875% local (NYC combined 8.875%).
- **Doc fee cap**: **$175 (legal cap, third-strongest in US, after CA $85 and NC $129).** Typical $175.
- **Title fee**: $50. **Registration**: weight-based, typical $26-140 for 2-year passenger.
- **Trade-in tax credit**: Yes.
- **Has**: MCTD (Metropolitan Commuter Transportation District) $50 fee for NYC area registrations; tire recycling fee on new tires only ($2.50/tire), not normally on used vehicle retail sales.
- **Does NOT have**: NJ-style supplemental titling fee, NJ $799 doc, CT luxury 7.75% tier, RI $250 doc cap, FL $77 title.

### PA, Pennsylvania
- **Sales tax**: 6% state base. **Local-rate disambiguation by ZIP**: Allegheny County (Pittsburgh metro, 150XX-152XX ZIPs) adds +1% (total 7%); Philadelphia (City + County, 191XX ZIPs) adds +2% (total 8%); **all other PA counties = flat 6%** (e.g., Bryn Mawr 19010 is Montgomery County, flat 6%; King of Prussia 19406 is Montgomery, flat 6%; West Chester 19380 is Chester, flat 6%). Confirm the buyer's registration ZIP is NOT in the 191XX or 150XX-152XX bands before defaulting to 6%.
- **Doc fee cap**: **No statutory cap.** Typical industry range $499-999, **PA dealers run high** versus NJ's $799 cap or NY's $175 cap. Treat any PA doc above $899 as negotiable.
- **Title fee**: $58. **Registration**: $45/year typical for passenger vehicles (annual, not biennial).
- **Trade-in tax credit**: Yes, trade-in value is subtracted from sales price BEFORE 6% (or 7% / 8%) tax applies.
- **Has**: Public Transportation Assistance Fund tire fee $1/tire on NEW tires sold (not normally a line on used vehicle OTD); $5 lien fee if financed (auto loan recorded against title); $26 lien recording add-on at PennDOT.
- **Does NOT have**: NJ-style supplemental titling fee, CT luxury 7.75% tier, NY $175 doc cap, RI $250 doc cap, environmental impact fee, per-battery fee, CA-style smog fee. Any of these appearing on a PA-buyer quote is a state-template leak, see SKILL.md gotcha D8.

## New England States, Detail Stubs

Quick-reference stubs for CT, MA, RI, NH, ME, VT. Full breakdowns (registration formulas, county quirks, dealer-typical practices) to be filled by later iterations as actual buying cycles surface specifics. "Does NOT have" lines exist to catch dealer CRM template leaks from other states (see SKILL.md gotcha D8).

### CT, Connecticut
- **Sales tax**: 6.35% standard; **7.75%** on vehicles with sales price > $50,000 (luxury threshold).
- **Doc fee cap**: No statutory cap. Typical industry range $499-699.
- **Title fee**: $25. **Registration**: ~$120 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, NY MCTD fee, RI $250 doc cap. Any of these appearing on a CT quote indicates a state-template leak, demand full re-quote.

### MA, Massachusetts
- **Sales tax**: 6.25% flat. No local sales tax on vehicles.
- **Doc fee cap**: No statutory cap. Typical industry range $499-799.
- **Title fee**: $75. **Registration**: ~$60 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, NY MCTD fee, CT luxury 7.75% tier, local-rate stacking.

### RI, Rhode Island
- **Sales tax**: 7% flat.
- **Doc fee cap**: **$250** (capped low, strong buyer protection).
- **Title fee**: $52.50. **Registration**: ~$30-90 depending on weight.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, doc fee over $250 (cap is binding), NY MCTD fee.

### NH, New Hampshire
- **Sales tax**: **0%, no state sales tax on vehicles.** This is a structural advantage; an NH-resident buyer titling in NH pays no sales tax regardless of dealer state.
- **Doc fee cap**: **$27 state document/title fee cap only** (NH RSA 261:171-a, $25 title + $2 agent). Dealer "administrative/documentary" fees are NOT capped (commonly $300-$495). The JSON `doc_cap=27` records the statutory state fee; treat dealer admin fees as uncapped negotiation targets. (verified 2026-06-22)
- **Title fee**: $25. **Registration**: town-based, formula on MSRP × age factor; typical $200-500 first year for newer vehicles.
- **Trade-in tax credit**: N/A (no sales tax).
- **Does NOT have**: any sales tax line at all (any sales-tax-rate appearing on an NH quote is a flat template leak), per-tire fee, NJ supplemental titling fee, statutory cap on dealer administrative fees.

### ME, Maine
- **Sales tax**: 5.5% flat.
- **Doc fee cap**: No statutory cap. Typical industry range ~$499.
- **Title fee**: $33. **Registration**: ~$35 plus excise tax (mil rate × MSRP, declining with age) collected by town.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, local sales tax stacking, NY MCTD fee.

### VT, Vermont
- **Sales tax**: 6% flat (Purchase & Use Tax).
- **Doc fee cap**: No statutory cap. Typical industry range ~$599.
- **Title fee**: $35. **Registration**: ~$76 (1-year) / $140 (2-year) for passenger vehicles.
- **Trade-in tax credit**: Yes.
- **Does NOT have**: per-tire fee, battery fee, NJ-style supplemental titling fee, local sales tax stacking, NY MCTD fee, CT luxury 7.75% tier.

## IL, Illinois (Detail Stub at CT/CA/TX Depth)

- **Sales tax**: 6.25% state base. **Local-rate stacking by ZIP**, IL has the most complex local stacking in the US after CA:
  - **Naperville (60540, DuPage County)**: 6.25% state + 1.25% DuPage = **7.5% combined**
  - **Chicago (606XX, Cook County)**: 6.25% state + 2.75% county + 1.25% city + RTA fees = **up to 10.25% combined** (highest large-city combined rate in the US)
  - **Suburban Cook County**: 6.25% state + 1.75% county + 0.5-1% city = 8-9% combined
  - **DuPage County (Naperville, Aurora, Wheaton)**: flat 7.5% combined
  - **Will County (Joliet, Bolingbrook, Plainfield 60544)**: 7-7.25% combined
  - **Kane County (St. Charles, Geneva, Aurora-Kane portion)**: 7-7.5% combined
  - **Lake County (Waukegan, Libertyville)**: 7-8% combined
  - Always confirm the buyer's registration ZIP combined rate before defaulting, DuPage (60540) != Cook (606XX).
- **Doc fee cap**: **$347.26 (legal cap as of 2025)**. **Highest cap among the low-tier (sub-$400) capped states, NOT the highest cap in the US** (MD $800, NJ $799, MO $604.47, VA $599, WV $575, LA $436, MN $350 all exceed it). Updated annually for inflation (Illinois Vehicle Code 625 ILCS 5/5-101.1; CPI-linked). PA dealers run $499-999 uncapped; IL dealers are statute-bound. Treat any IL quote with doc above $347.26 as a leak, flat illegal under IL law.
- **Title fee**: $155 (one of higher US title fees). **Registration**: $151/yr passenger vehicle. **Plate transfer**: ~$26 (transfer from trade vehicle to new vehicle, cheaper than new-plate issuance).
- **License + Emissions inspection ("LE")**: $20 for emissions-test counties (Cook, DuPage, Kane, Lake, Will, McHenry, Madison, Monroe, St. Clair). Other counties exempt.
- **Trade-in tax credit**: **YES BUT CAPPED at first $10,000 of trade allowance** (Illinois Vehicle Code; was uncapped pre-2020, capped 2020-2024 per Rivian-vs-Ford SB-690 lobbying compromise, **kept at $10k cap** through 2025+, verify current legislation). A $12,000 trade allowance in IL only gets credit on $10,000 × combined rate. A $5,800 trade (the buyer's Ram) gets full credit ($5,800 × 7.5% = $435 tax savings in the buyer's Illinois county).
- **Has**: state Use Tax separately if buying from out-of-state dealer (IL Form RUT-25); county-level tax stacking per ZIP (5+ rate tiers in IL); plate transfer option ($26) vs new plate ($151 included in reg); LE/emissions inspection $20 in non-exempt counties.
- **Does NOT have**: NJ-style supplemental titling fee, NY MCTD fee, CT $50k luxury tier, RI $250 doc cap (IL's cap is $347.26), TX $200/yr EV reg premium, PA's uncapped doc tier, per-tire fee on retail used dealer sales, battery fee, CA-style smog fee, NC HUT, OK excise tax separate from sales tax. Any of these appearing on an IL-buyer quote is a state-template leak, demand full re-quote per gotcha D8.

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
| IL (60540 Naperville, DuPage 7.5%) | IN (Munster / Highland / Hammond, 46XXX) | IL 7.5% (paid at IL SOS) | IN $251.05 (statutory cap, CPI-indexed) | IN dealer should NOT charge IN 7% tax; IL buyer pays IL 7.5% at IL SOS titling. **IN cap $251.05 vs IL $347.26**: IN doc is ~$96 cheaper. Cross-state IL→IN small advantage. |
| IL (60540) | WI (Kenosha / Pleasant Prairie, 53XXX) | IL 7.5% (paid at IL SOS) | WI no statutory doc cap (typ $399-499) | WI dealer should NOT charge WI 5% tax. **WI doc typ $399-499 = $50-150 more than IL $347.26 cap**. Cross-state IL→WI net advantage flips negative on doc; net effect: nil for IL buyer (tax same, doc slightly more). |
| IL (60540) | MO (border zones, IL→MO uncommon for Chicagoland) | IL 7.5% (paid at IL SOS) | MO doc cap $599 statutory | MO doc cap $599 > IL $347.26. No advantage. |
| IL (60540) | IA (Quad Cities border, 522XX→527XX) | IL 7.5% (paid at IL SOS) | IA doc typ $499 | No advantage. |
| IL (606XX Chicago, 10.25%) | IN (Lake County / Hammond) | IL 10.25% (paid at IL SOS) | IN $251.05 (statutory cap) | Chicago buyers face the highest combined US tax (10.25%), cross-state buys don't reduce tax burden because IL SOS collects IL tax regardless of dealer location. The cross-state move only saves ~$96 on doc (IN $251.05 vs IL $347.26). |

**IL has no structural cross-state arbitrage advantage**, IL's combined tax stacking is high enough that even no-tax-state dealers (DE, NH, OR) far from Chicagoland would lose to local IL on the doc cap. The exception is IL→IN (~$96 doc savings: IN $251.05 cap vs IL $347.26 cap), which is too small to drive cross-state buying decisions on its own; only relevant when an IN dealer happens to have the exact specific VIN at a price advantage.

## High-Population State Detail Stubs, FL / OH / NC / GA / MI / VA / WA + DC / MD

Quick-reference stubs for 7 high-population states plus DC and MD (commuter-corridor coverage paired with VA). Pattern matches CT / CA / TX / IL depth: tax + doc fee + title + reg + trade-in credit + "Does NOT have" leak list + cross-state rows + 2 worked OTD examples. last_verified: 2026-05-18

### FL, Florida

- **Sales tax**: 6% state + **county discretionary surtax** 0.5-2% applied **only to first $5,000** of taxable price (max $5,000 × 2% = $100 county surtax cap per vehicle). Combined effective: most counties land 6.5-8% on the first $5k then drop to flat 6% for the remaining sale price (e.g., Pinellas 7%, Miami-Dade 7%, Hillsborough 7.5%, Orange 6.5%, Broward 7%, Duval 7.5%). The **$5,000 surtax ceiling** is a structural FL quirk: a $40,000 sale taxed at Pinellas 7% county doesn't pay 7% on $40k, it pays 6% × $40,000 + 1% × $5,000 = $2,450 (effective 6.125%), not $2,800. Always apply the FL ceiling math at OTD calculation.
- **Doc fee cap**: **No statutory cap.** Typical industry range $799-1,499, **FL dealers run high**, often the highest in the US. Treat any FL doc above $999 as negotiable and any above $1,299 as a Phase 6 first-counter demand-removal item per gotcha D8/D9 pattern.
- **Title fee**: $77.25 new title / $85.25 with lien recording (high vs typical $15-50). **Registration**: weight-based, $46-95 first year + tag fee, then $46-72 renewal.
- **Trade-in tax credit**: **YES**, sale price minus trade allowance is the tax base (with FL surtax ceiling applied to net taxable, not gross).
- **Has**: title surcharge for "initial registration fee" $225 first-time FL registrations (out-of-state buyers transferring to FL hit this, counts as a one-time-only fee for the first FL registration of any vehicle in the buyer's name); lemon law fee $2/vehicle; battery fee $1.50/battery (rare on used retail).
- **Does NOT have**: no state income tax (this drives FL as destination state for retirees + out-of-state buyers); no NY MCTD fee; no CA-style luxury tier; no CA smog inspection; no IL emissions inspection requirement statewide (some counties test); no NC highway use tax; no MI trade-in cap; no PA Philly/Allegheny local stacking; no doc fee cap (this is a leak vector in the OPPOSITE direction, FL has no cap so high doc fees are legal, just negotiable).

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

### OH, Ohio

- **Sales tax**: 5.75% state base + county/transit district 0.25%-2.25% (typical combined 6.5-8%). Cuyahoga (Cleveland 44XXX) 8%, Franklin (Columbus 432XX) 7.5%, Hamilton (Cincinnati 452XX) 7.8%, Summit (Akron 443XX) 6.75%, Montgomery (Dayton 454XX) 7.5%, Lucas (Toledo 436XX) 7.75%. Confirm buyer's registration ZIP combined rate.
- **Doc fee cap**: **$250 (statutory cap)**, among the lowest in the US (only CA $85, NC $129, NY $175, WA $200, TX $225 safe-harbor, MI $230 are lower; RI $250 and OR $250 tie). OH doc-fee compliance is mechanically enforced; treat any OH quote with doc above $250 as a flat illegal leak.
- **Title fee**: $15 + $5 lien recording if financed = $20 with lien. **Registration**: $35 base + $3-91 by axle/weight (passenger sedan typical $50-65/yr).
- **Trade-in tax credit**: **YES**, full trade allowance subtracted from sales price before tax.
- **Has**: $5 lien fee (financed sales only); axle-based commercial vehicle surcharge.
- **Does NOT have**: no CA-style smog inspection (Ohio has e-check emissions in 6 Cleveland-area counties only, Cuyahoga, Lake, Lorain, Geauga, Medina, Portage; rest of state exempt); no NJ supplemental titling; no NY MCTD; no IL emissions $20 add-on; no FL initial registration fee; no NC highway use tax; no PA Philly local stacking; no MI trade-in cap.

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

### NC, North Carolina

- **NC has NO traditional sales tax on motor vehicles.** Instead, NC applies a **Highway Use Tax (HUT) of 3%** on the purchase price (or fair market value if higher than purchase price) at title issuance. This is the structural NC quirk, agents must explicitly use "HUT 3%" not "sales tax 3%" in communications, and dealer CRM templates that try to apply 5-7% "sales tax" are a flat error (gotcha D8 leak, demand full re-quote).
- **HUT cap**: $250 for commercial vehicles only (not passenger); passenger vehicles pay full 3% with no upper cap.
- **Doc fee cap**: **$129 (statutory cap, NCGS § 20-101.1)**, second-lowest in the US after CA $85. NC doc-fee leaks are common from out-of-state CRM templates (FL, GA, VA dealers in border zones often charge their own state's $599-799 doc on NC buyers). Treat any NC doc above $129 as a flat illegal leak.
- **Title fee**: $52 (new title). **Registration**: $36-89/yr by vehicle class (passenger sedan typical $38.75).
- **Trade-in tax credit**: **YES on HUT**, full trade allowance subtracted from sale price before 3% HUT.
- **Has**: $20 plate transfer fee (if transferring from previous NC vehicle); $40 inspection fee (annual safety + emissions in 19 counties, Mecklenburg, Wake, Durham, Guilford, etc.).
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

### GA, Georgia

- **Sales tax**: **GA does NOT use traditional sales tax on most vehicle purchases.** Instead, GA applies a **Title Ad Valorem Tax (TAVT) of 6.6% one-time** at vehicle registration, calculated on the fair market value (typically the GA DOR's Motor Vehicle Assessment Manual value, not the sale price, this is a structural quirk that can cut both ways: GA DOR FMV can be HIGHER than sale price for distressed/high-mileage cars, costing buyer; or LOWER for premium-trim/low-mileage cars, saving buyer). TAVT replaced GA's annual ad valorem ("birthday tax") in 2013 for vehicles purchased after March 1, 2013, Georgia residents pay TAVT once at purchase, then $20/yr renewal with no annual ad valorem.
- **TAVT base value rule**: GA DOR FMV from Motor Vehicle Assessment Manual; if no FMV available, sale price is used. Agents must check DOR FMV vs sale price at Phase 2, if FMV materially exceeds sale, the TAVT bill will be higher than the buyer expects.
- **Doc fee cap**: **No statutory cap.** Typical industry range $599-799 (typical GA dealers run mid-range vs FL's high $999-1,499). Treat above $899 as negotiable.
- **Title fee**: $18. **Registration**: $20/yr base + $76 emissions in metro Atlanta 13-county zone (Cherokee, Clayton, Cobb, Coweta, DeKalb, Douglas, Fayette, Forsyth, Fulton, Gwinnett, Henry, Paulding, Rockdale).
- **Trade-in tax credit**: **YES on TAVT**, trade allowance subtracted from sale price/FMV before 6.6% TAVT.
- **Has**: $1 lien fee; "ad valorem" line item ONLY for vehicles purchased pre-2013 still on annual ad valorem (irrelevant for new buyers); GA Power Combat Veteran exemption ($0 TAVT for qualifying); $200 alternative fuel vehicle fee for EVs/hybrids replacing fuel tax.
- **Does NOT have**: no traditional sales tax on titled vehicles (any "sales tax 4%" line is a leak, GA's general 4% sales tax applies to most retail but NOT to vehicle purchases that get TAVT); no annual ad valorem on 2013+ vehicles; no NY MCTD; no NJ supplemental titling; no FL surtax ceiling; no MI trade-in cap; no IL emissions $20 (GA has its own $76 emissions in 13 metro counties only).

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

Sales $36,000 (DOR FMV $34,500, sale price is HIGHER, but TAVT uses sale price since dealer transaction), doc $799, trade $10,000, TAVT 6.6%:

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

### MI, Michigan

- **Sales tax**: 6% flat state, **no local stacking on motor vehicles** (Michigan is one of the cleanest tax structures, same 6% statewide for vehicles).
- **Doc fee cap**: **$230 (statutory cap, MCL 257.217e)**, among lowest in US (parallels OH $250, RI $250, MI $230, WA $200, NY $175, CA $85, IL $347.26). Treat any MI doc above $230 as flat illegal leak.
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

#### MI Worked OTD Example (Grand Rapids Kent, $12,000 trade, exceeds 2025 cap)

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

### VA, Virginia (DC commuter corridor)

- **Sales tax**: 4.15% state Motor Vehicle SUT (Sales and Use Tax) + 1% local in some localities (combined effective 4.15-5.15%; most VA buyers pay flat 4.15%). **Minimum SUT $75**, for very low-price purchases (<$1,800), VA charges a $75 floor.
- **Doc fee cap**: **$599 (statutory cap, VA Code § 46.2-1530.1).** Treat any VA quote with doc above $599 as flat illegal leak.
- **Title fee**: $15 (new title). **Registration**: $35-46/yr by weight class (passenger sedan typical $40.75/yr).
- **Trade-in tax credit**: **NO. VA does NOT grant trade-in tax credit on the 4.15% SUT.** This is the VA quirk, unique among DC-area neighbors (DC = yes, MD = yes, VA = no). A $10,000 trade in VA saves $0 in tax; same trade in MD saves $600. VA buyers should NOT structure deals as "trade reduces taxable price", full sale price is taxed regardless of trade.
- **Has**: $64.50/yr Hybrid + EV registration fee; $40.75/yr personal property tax assessed by city/county (Fairfax, Arlington, Loudoun rates vary 3.5-4.57% of NADA value/year, separate from purchase SUT, but a recurring cost VA buyers must plan for); inspection $20/yr.
- **Does NOT have**: NO trade-in tax credit (the structural quirk); no NY MCTD; no NJ supplemental titling; no DC excise weight scaling; VA's $599 doc cap is LOWER than MD's $800 cap (VA = doc-fee sweet spot in the corridor, not MD); no NC HUT (VA has SUT, different mechanism); no GA TAVT; no IL emissions $20; no FL surtax ceiling; no MI trade-in cap (because VA has no trade credit at all); no PA Philly local stacking.

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

#### VA Worked OTD Example (Fairfax 22030, $8,000 trade, NO credit benefit)

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

### WA, Washington

- **Sales tax**: 6.5% state + 0.5-3.5% local (combined 8.5-10.4%; Seattle 10.25%, Tacoma 10.3%, Bellevue 10.1%, Spokane 8.9%, Olympia 9.4%). **Plus MVET 0.3%** (Motor Vehicle Excise Tax) on top of sales tax = effective 8.8-10.7% combined for the registering ZIP.
- **Doc fee cap**: **$200 (statutory cap, RCW 46.12.555).** Treat any WA quote with doc above $200 as flat illegal leak.
- **Title fee**: $15. **Registration**: ad-valorem by vehicle value, typical $50-200/yr for passenger; high-value vehicles can hit $300-500/yr due to MVET surcharge component.
- **Trade-in tax credit**: **YES**, full trade allowance subtracted before sales tax (and MVET).
- **Has**: $75 EV registration surcharge + $30 electric motorcycle; $30 transportation electrification fee on EVs; $1.50/tire fee on new tires (rare on used retail); $7 ferry surcharge for puget sound counties.
- **Does NOT have**: no state income tax (WA structural advantage, but vehicle ad-valorem reg makes the differential smaller than buyers expect); no smog inspection (WA discontinued state emissions program 2020); no NY MCTD; no NJ supplemental titling; no GA TAVT; no NC HUT; no FL initial registration fee; no MI trade-in cap; no IL emissions $20; no CA luxury tier; no PA Philly local stacking; no VA "no-trade-credit" rule.

#### WA Worked OTD Example (Seattle King 10.25%, no trade)

Sales $35,000, doc $200 (WA cap), Seattle combined 10.25% + MVET 0.3% = 10.55%:

```
Taxable = $35,000 + $200 = $35,200
Tax     = $35,200 × 0.1055 = $3,713.60
Title   = $15
Reg     = $130 (ad-valorem on $35k value)
OTD     = $35,000 + $200 + $3,713.60 + $15 + $130 = $39,058.60
```

WA Seattle 10.55% on $35k = $3,713 vs OR same vehicle (no tax) ~$0 = **$3,713 OR structural advantage**, drives the WA→OR cross-state magnet pattern below.

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

### DC, District of Columbia

- **Sales tax / excise structure**: DC does NOT use traditional sales tax on vehicles. Instead, DC applies an **excise tax by vehicle weight class on first $40,000 of MSRP**, then a higher tier above $40k. Current rates (2026):
  - Class I (≤3,499 lbs): 6% on first $40k MSRP, 7% above $40k
  - Class II (3,500-4,999 lbs): 7% on first $40k MSRP, 8% above $40k
  - Class III (5,000-5,999 lbs): 8% on first $40k MSRP, 9% above $40k
  - Class IV (≥6,000 lbs): 8% on first $40k MSRP, 9% above $40k
  - EV exemption: alternative-fuel vehicles get $0 excise on first $40k (then standard above)
- **Doc fee cap**: **No statutory cap.** Typical DC dealer industry range $599-899; DC has only ~12 dealerships total, most are luxury-tier (Mercedes / BMW / Audi / Tesla Georgetown / Capitol Cadillac). Most DC residents register vehicles bought at VA / MD dealers.
- **Title fee**: $26 standard / by weight class. **Registration**: $72/yr biennial (paid every 2 years = $144 total for 2-year period; passenger).
- **Trade-in tax credit**: **YES**, sale price minus trade is the excise base.
- **Has**: $26 lien recording; $25 reflective plate fee; $100 EV charging infrastructure fee; emissions inspection biennial ($35).
- **Does NOT have**: no traditional sales tax (DC's excise structure is unique among US jurisdictions, closest analog is GA TAVT but DC scales by weight); no county stacking (DC = single jurisdiction, no sub-jurisdiction layering); no MD $800 doc cap (DC has no cap); no VA "no-trade-credit" rule; no NY MCTD; no NJ supplemental titling; no NC HUT; no FL surtax ceiling; no MI trade-in cap; no CA luxury tier; no IL emissions $20.

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

Sales $52,000 (above $40k MSRP, tiered), doc $799, trade $9,000, DC Class III 8% on first $40k + 9% above:

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

### MD, Maryland

- **Sales tax**: 6% flat state, **no local stacking** (MD is one of the cleanest tax structures, same 6% statewide for vehicles, parallel to MI).
- **Doc fee cap**: **$800 (statutory cap, MD Transportation § 15-311.1, effective July 1 2024, raised from $500).** Cap history: $200 → $300 (2014) → $500 (2020) → $800 (2024). Treat any MD doc above $800 as flat illegal leak. **MD doc protection is now WEAK, its $800 cap is HIGHER than VA's $599 cap**, inverting the old "MD = low-doc sweet spot" claim. In the DC corridor MD now has the highest statutory doc cap (DC no cap, MD $800, VA $599); VA is the doc-fee sweet spot, not MD.
- **Title fee**: $50 (titling tax separately, not a fee). **Registration**: **$135 every 2 years** (biennial, passenger 3,700 lbs+; smaller cars $108 biennial). This is high vs typical $35-50/yr.
- **Trade-in tax credit**: **YES**, sale price minus trade is the taxable base.
- **Has**: $20 lien recording; $14 title-search fee; biennial vehicle safety inspection at sale only ($65-100 at certified station, required before title transfer for used cars sold by dealers; no annual recurring inspection like VA); $100 EV registration surcharge.
- **Does NOT have**: no local sales tax stacking; no VA "no-trade-credit" rule (MD grants credit, this is the structural MD advantage over VA for traded buyers in the DC commuter corridor); no DC excise weight scaling; no NY MCTD; no NJ supplemental titling; no PA Philly local stacking; no GA TAVT; no NC HUT; no FL surtax ceiling; no MI trade-in cap; no IL emissions $20 (MD has its own VEIP biennial emissions on most counties, Anne Arundel, Baltimore, Calvert, Carroll, Cecil, Charles, Frederick, Harford, Howard, Montgomery, Prince George's, Queen Anne's, $14); no CA luxury tier.

#### MD Worked OTD Example (Montgomery County 20850, DC commuter, no trade)

Sales $31,000, doc $800 (MD cap), MD 6%:

```
Taxable = $31,000 + $800 = $31,800
Tax     = $31,800 × 0.06 = $1,908.00
Title   = $50
Lien    = $20
Reg (biennial annualized) = $67.50/yr ($135/2yr)
VEIP    = $14
OTD     = $31,000 + $800 + $1,908 + $50 + $20 + $67.50 + $14 = $33,859.50
```

#### MD Worked OTD Example (Baltimore County 21204, $10,000 trade)

Sales $34,000, doc $800, trade $10,000, MD 6%:

```
Net sale          = $34,000 - $10,000 = $24,000
Taxable           = $24,000 + $800 = $24,800
Tax               = $24,800 × 0.06 = $1,488.00
Title             = $50
Reg (biennial)    = $135 (paid in full at registration)
VEIP              = $14
OTD before trade  = $34,000 + $800 + $1,488 + $50 + $135 + $14 = $36,487
Trade applied     = -$10,000
Cash OTD          = $26,487
Tax savings       = $10,000 × 6% = $600 (vs $0 in VA — the DC-corridor structural MD trade-credit advantage)
```

### Cross-State Titling Rows, High-Pop States + DC Corridor

| Buyer State | Dealer State | Tax Paid | Doc Fee | Notes |
|---|---|---|---|---|
| FL (Pinellas 33701, 7% w/ surtax ceiling) | GA (Atlanta Fulton) | FL 6% + $50 county surtax cap | GA $599-799 (no cap) | GA TAVT 6.6% does NOT apply to out-of-state buyers; FL buyer pays only FL effective rate at FL DOR titling. GA doc typ $100-300 cheaper than FL $999-1,499 typical, small doc-fee advantage but FL initial reg fee $225 still applies if first FL registration. |
| FL (Miami-Dade 33101, 7% w/ ceiling) | AL (Mobile) | FL 6% + surtax | AL no cap (typ $599-799) | AL dealer should NOT charge AL 2% sales tax. AL doc similar to GA. Net: small advantage on doc, FL still pays $225 initial reg fee. |
| OH (Cleveland Cuyahoga 8%) | PA (Pittsburgh Allegheny 7%) | OH 8% (paid at OH BMV) | PA no cap (typ $499-999) | PA dealer should NOT charge PA 7%. PA doc typ $499-999 vs OH $250 cap. Net DISADVANTAGE on doc ($250-750 more in PA), no advantage on tax. OH→PA only worth it for specific VIN scarcity. |
| OH (Toledo Lucas 7.75%) | MI (Detroit Wayne 6%) | OH 7.75% (paid at OH BMV) | MI $230 cap | MI dealer should NOT charge MI 6%. MI doc $230 = $20 cheaper than OH $250 cap. Tax same buyer-state rate. Net: $20 advantage. |
| OH (Cincinnati Hamilton 7.8%) | IN (Indianapolis Marion) | OH 7.8% | IN $251.05 cap | IN dealer should NOT charge IN 7%. IN cap $251.05 ≈ OH $250 cap (~$1 apart). Net: doc-neutral, no advantage. |
| OH (border 43XXX) | WV (Wheeling Ohio County) | OH 5.75-8% | WV $575 cap | WV cap $575 is $325 ABOVE OH $250 cap. Tax same. Net DISADVANTAGE on doc, OH buyers should stay in-state; only cross for specific VIN. |
| NC (Charlotte Mecklenburg) | VA (Bristol/Roanoke) | NC HUT 3% | VA $599 cap | VA dealer should NOT charge VA 4.15% SUT. NC HUT 3% is the buyer's rate. VA doc $599 = $470 MORE than NC $129. Net major doc disadvantage. NC buyers should stay in-state for doc savings; only cross-state for specific VIN scarcity. |
| NC (Raleigh Wake) | SC (Greenville Anderson) | NC HUT 3% | SC IMF capped $500/vehicle + doc typ $399-499 | SC has unique 5% Infrastructure Maintenance Fee (IMF) capped $500/vehicle in lieu of sales tax for out-of-state titles; SC dealer should NOT apply IMF to NC buyer. NC HUT applies. SC doc $270-370 MORE than NC $129. |
| NC (Asheville Buncombe) | TN (Knoxville Knox) | NC HUT 3% | TN no cap (typ $499-899) | TN dealer should NOT charge TN 9.25%. NC HUT applies. TN doc $370-770 MORE than NC $129. NC buyers cross-state to TN ONLY for specific VIN. |
| GA (Atlanta Fulton) | FL (Jacksonville Duval) | GA TAVT 6.6% (on FMV at GA registration) | FL $999-1,499 typ | FL dealer should NOT charge FL 6%. GA buyer pays TAVT at GA registration; FL doc 200-700 MORE than GA typical. Net disadvantage on doc. |
| GA (Savannah Chatham) | AL (Birmingham Jefferson) | GA TAVT 6.6% | AL similar to GA | AL dealer should NOT charge AL 2%. TAVT applies. Doc similar. |
| GA (Augusta Richmond) | SC (Aiken) | GA TAVT 6.6% | SC IMF capped $500 + doc $399-499 | SC IMF does NOT apply to GA buyer (out-of-state). GA TAVT applies at GA DOR. SC doc $200-300 LESS than GA typ $599-799, small advantage if SC dealer has the VIN. |
| GA (Columbus Muscogee) | TN (Chattanooga Hamilton) | GA TAVT 6.6% | TN typ $499-899 | TN doc $100-300 more than GA typical. No advantage. |
| MI (Detroit Wayne) | OH (Toledo Lucas) | MI 6% (paid at MI SOS) | OH $250 cap | OH doc $20 cheaper than MI $230 cap. Tax same. Net: $20 advantage. |
| MI (Grand Rapids Kent) | IN (South Bend St. Joseph) | MI 6% | IN $251.05 cap | IN cap $251.05 is ~$21 MORE than MI $230 cap. Net minor disadvantage on doc. |
| VA (Arlington 22203, DC commuter) | DC (Georgetown) | VA 4.15% SUT, NO trade credit | DC no cap (typ $599-899) | DC dealer should NOT charge DC excise to VA buyer. VA SUT applies at VA DMV titling. DC doc typ $200-300 MORE than VA $599 cap. Trade-in: if buyer has trade, MD/DC sales would grant credit but VA registration does NOT, buyer pays full SUT regardless of dealer state. **VA buyers with trades: this is the structural disadvantage; consider relocating before purchase if trade is large.** |
| VA (Fairfax 22030) | MD (Bethesda Montgomery) | VA 4.15% SUT, NO trade credit | MD $800 cap | MD dealer should NOT charge MD 6%. VA SUT applies. MD's $800 cap is $201 HIGHER than VA's $599 cap, **no doc advantage crossing to MD; MD is now the high-doc state in this pair.** Trade credit lost at VA DMV regardless of MD origin. |
| VA (Loudoun 20176) | WV (Charles Town Jefferson) | VA 4.15% SUT, NO trade credit | WV $575 cap | WV cap $575 is only ~$24 below VA $599 cap, marginal doc savings, not the large gap once claimed. WV dealer should NOT charge WV 6%. For real doc savings from VA, cross to NC ($129) instead. |
| VA (Norfolk 23508) | NC (Raleigh Wake) | VA 4.15% SUT | NC $129 cap | NC doc $470 LESS than VA $599 cap, best doc-fee cross-state from VA. NC dealer should NOT charge NC HUT to VA buyer. |
| DC (Capitol Hill 20003) | VA (Arlington) | DC excise by weight class | VA $599 cap | VA dealer should NOT charge VA 4.15%. DC excise applies at DC DMV. VA doc cheaper than DC's uncapped. **VA = doc-fee sweet spot for DC buyers** (parallel to DE for PA, MD for VA). |
| DC (Adams Morgan 20009) | MD (Silver Spring Montgomery) | DC excise | MD $800 cap | MD dealer should NOT charge MD 6%. DC excise applies. **MD's $800 cap is the highest in the DC corridor**, weak doc protection. For doc savings a DC buyer should cross to VA ($599 cap), not MD. |
| MD (Bethesda Montgomery) | VA (Tysons Corner Fairfax) | MD 6% (paid at MD MVA) | VA $599 cap | VA dealer should NOT charge VA 4.15%. MD 6% applies at MD MVA. VA's $599 cap is $201 LESS than MD's $800 cap, **doc advantage crossing to VA**; tax depends on net trade-credit-adjusted comparison. |
| MD (Silver Spring Montgomery) | DC (Georgetown) | MD 6% | DC no cap | DC is uncapped (typ $599-899), comparable to MD's $800 cap. No reliable doc advantage either way. |
| MD (Baltimore County) | PA (border Harrisburg/York 17XXX) | MD 6% | PA no cap (typ $499-999) | PA doc ($499-999) is comparable to MD's $800 cap, PA low end is cheaper, high end pricier. No reliable doc advantage. |
| MD (Cecil County 219XX) | DE (Wilmington/Newark) | MD 6% | DE no cap (typ $299-499) | DE has no state sales tax but 4.25% doc fee for DE residents only, does NOT apply to MD buyer. MD 6% at MD MVA. DE doc ($299-499) is $300-500 LESS than MD's $800 cap. **DE = doc-fee savings zone for MD buyers.** |
| WA (Seattle King 10.55%) | OR (Portland Multnomah) | WA 10.55% (paid at WA DOL) | OR typ $115 (CAT applies for new) | OR has NO state sales tax. OR dealer should NOT charge anything tax-side to WA buyer (but per WA-OR reciprocity rules, WA tax IS due at WA DOL titling, buyers attempting to register OR-purchased cars in WA cannot escape WA 10.55%). **WA→OR is a magnet for residency arbitrage (buying + registering in OR if buyer maintains OR address) but NOT for WA-residents who try to register in OR, WA DOL audits cross-border title transfers.** Doc: OR $115 vs WA $200 cap = $85 OR doc savings; minimal. |
| WA (Spokane 9.2%) | ID (Coeur d'Alene Kootenai) | WA 9.2% | ID no cap (typ $299-499) | ID dealer should NOT charge ID 6%. WA tax applies. ID doc $99-299 MORE than WA $200 cap. Net disadvantage on doc. |

### Cross-Corridor Structural Summary (DC Commuter)

The DC + VA + MD commuter corridor has 3 distinct doc-fee zones:

- **VA $599 cap**, strongest doc protection in the corridor
- **MD $800 cap**, weak (raised to $800 eff. July 1 2024; now the HIGHEST statutory cap in the corridor, above VA)
- **DC no cap**, uncapped but small dealer count limits impact

For a buyer with trade-in optionality across the corridor, the math:

- MD-registered: full trade credit at 6%, **structural winner** for traded buyers
- DC-registered: full trade credit at 6-9% weight-class, variable based on vehicle weight
- VA-registered: NO trade credit, **structural loser** for traded buyers regardless of dealer state

For a buyer with NO trade:

- VA 4.15% SUT, **structural winner** by tax rate (vs MD 6%, DC 6-9%)
- MD 6% flat
- DC 6-9% by weight class

Phase 1 buyer-type router should surface the trade-vs-no-trade DC-corridor split when buyer's ZIP is in 22XXX (VA) / 200XX-209XX (DC) / 207XX-219XX (MD).

## Round 2 Verified State Detail Stubs

Web-verified detail stubs (source_url + source_verified_date in `data/state_fees.json`, `verified:true`). Doc-fee caps here are the single source of truth reconciled with the All-State Summary Table and the JSON. "Does NOT have" lines catch dealer CRM template leaks from other states. NH's verified stub lives in the New England section above. last_verified: 2026-06-22

### AK, Alaska

- **Sales tax**: **No state sales tax.** Boroughs/cities impose local sales tax 0-7.5% (Anchorage & Fairbanks 0%, Juneau 5%); many jurisdictions cap tax per transaction (e.g., Wasilla taxes only first $500; Kodiak caps taxable at $3,000), drastically reducing tax on a vehicle. A local use tax applies if you buy outside your taxing jurisdiction.
- **Doc fee cap**: **No statutory cap** (secondary-sourced). Typical doc fee ~$80, usually non-negotiable.
- **Title fee**: $15 (lien recording $15/lien). **Registration**: biennial, ~$100 for a standard passenger vehicle (≈$50/yr), paid every two years. A locally-imposed Motor Vehicle Registration Tax (MVRT) adds $10-$221 depending on borough and vehicle age; Fairbanks and Kenai Peninsula charge no MVRT.
- **Trade-in tax credit**: N/A at the state level, governed by local ordinance where local tax applies.
- **Does NOT have**: state sales tax; doc-fee statutory cap; a statewide trade-in credit rule; emissions inspection in most boroughs.

#### AK Worked OTD Example (Anchorage, 0% local, no trade)

Sales $30,000, doc $80, Anchorage 0% local tax:

```
Tax        = $0 (Anchorage has no local sales tax)
Doc        = $80
Title      = $15
Reg (2 yr) = $100 (annualize ~$50/yr)
OTD        = $30,000 + $80 + $15 + $100 = $30,195
```

(Same purchase in Juneau at 5% local with no per-transaction cap would add ~$1,500 in tax.)

verified: 2026-06-22 | source: LegalClarity Alaska vehicle sales tax + FindTheBestCarPrice (AK) + AK DMV title/reg fee schedule | by: orchestrator-S7

---

### AL, Alabama

- **Sales tax**: **2% state** automotive sales tax (notably below Alabama's 4% general rate; applies to new, used, and private-party sales). **Heavily local-ZIP-driven**: counties add 0.3-2.5% and cities 0-4%, each as a **separate, usually lower automotive rate**, so the combined vehicle rate at the buyer's locale typically runs ~2.3-5% and occasionally higher. There is **no uniform statewide local rate**, the real rate is entirely a function of the buyer's county+city.
- **Doc fee cap**: **No statutory cap.** Doc/"clerical/processing" fees are dealer-set and, unusually, **taxable at the automotive rate** (so a $499 doc adds tax on top). AL average is ~$485. With no ceiling, treat the doc line as fully negotiable; there is no statute to cite against an inflated number.
- **Title fee**: $18 ($15 certificate of title, Code of Ala. §§ 32-8-1 et seq., + ~$3 processing). **Registration**: ~$23/yr standard passenger (plus value-based ad valorem property tax collected at registration under Code of Ala. § 40-8-1, assessed at 15% of market value, a separate annual property charge, not a one-time purchase fee).
- **Trade-in tax credit**: **YES** on **dealer** purchases, the trade-in value is deducted from the taxable price (state level; some sources note local taxes may not always honor it). **No trade credit on private-party sales** (full agreed price is taxed), and **rebates do NOT reduce** the tax base.
- **Has**: separate county + city automotive rates stacked on the 2% state; **EV registration surcharge $200/yr BEV, $100/yr PHEV** (Rebuild Alabama Act, 2019 Act 2019-2); annual ad valorem property tax on the vehicle at registration; taxable doc fee.
- **Does NOT have**: a statutory doc-fee cap; a uniform statewide local vehicle rate; TAVT; highway-use tax; IMF; a Texas-style SPV minimum-value floor; trade-in credit on private-party sales; rebate tax reduction.

#### AL Worked OTD Example (Huntsville / Madison Co., ~3.25% combined automotive, no trade)

Sales $30,000, doc $485, AL 2% state + 1.25% local automotive = 3.25%:

```
Taxable = $30,000 + $485 = $30,485   # doc fee is taxable in AL
Tax     = $30,485 × 0.0325 = $990.76
Title   = $18
Reg     = $23 (annual; excludes value-based ad valorem property tax)
OTD     = $30,000 + $485 + $990.76 + $18 + $23 = $31,516.76
```

#### AL Worked OTD Example (Huntsville / Madison Co., ~3.25%, $7,000 trade, dealer sale)

Sales $30,000, doc $485, trade $7,000, AL 3.25%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $23,000 + $485 = $23,485   # trade credited (dealer sale); doc still taxable
Tax        = $23,485 × 0.0325 = $763.26
Title      = $18
Reg        = $23
Cash OTD   = $23,000 + $485 + $763.26 + $18 + $23 = $24,289.26
Tax savings on trade = $7,000 × 0.0325 = $227.50   (dealer sale only; $0 on private-party)
```

verified: 2026-06-22 | source: AL Dept. of Revenue Automotive Sales/Use/Lease Tax Guide (2% rate, taxable doc, trade credit) + SalesTaxHandbook AL vehicles (no doc cap, local stacking) + ADOR Memo 2023-002 / Rebuild Alabama Act 2019-2 (EV $200 / PHEV $100) | by: orchestrator-S3

---

### AR, Arkansas

- **Sales tax**: 6.5% state sales tax; + 1-5% local at buyer's address (combined typically ~9.5-11.5%). Buyer pays tax to the DFA at registration, not to the dealer at point of sale. Note a 2025 used-vehicle relief tier (SB49, effective ~2025-10-01): used vehicles under $10,000 are exempt, $10,000-$14,999 taxed at a reduced 3.5%, $15,000+ at the full 6.5%.
- **Doc fee cap**: **No statutory cap.** Typical industry range $110-395. A "$125 cap" figure appears on some calculator sites but is NOT supported by Arkansas statute or DFA guidance, treat it as unverified folklore and treat anything above ~$395 as a leak.
- **Title fee**: $10. **Registration**: ~$25/yr (weight-based, passenger baseline).
- **Trade-in tax credit**: **YES**, taxable base is sale price minus trade. Arkansas is unusually generous: under Ark. Code § 26-53-126 you can even claim a private-sale credit if you sell your old vehicle privately and buy a replacement of greater value within 60 days (bill of sale required at registration).
- **Has**: EV annual registration surcharge $200 (BEV) / $100 (PHEV) / $50 (HEV), per Ark. Code 27-24 / AFDC, on top of standard registration.
- **Does NOT have**: statutory doc fee cap; no trade-in credit denial (full trade credit allowed).

#### AR Worked OTD Example (Pulaski County ~9.5%, $30,000 new, no trade)

```
Taxable = $30,000 + $200 doc = $30,200
Tax     = $30,200 x 0.095 = $2,869.00   (6.5% state + ~3% local)
Title   = $10
Reg     = $25
OTD     = 30,200 + 2,869 + 10 + 25 = $33,104.00
```

verified: 2026-06-22 | source: Ark. Code § 26-53-126 (trade/private-sale credit) + AR DFA used-vehicle tax credit page + AFDC law 12182 (EV fee) | by: agent-S5

---

### AZ, Arizona

- **Sales tax**: 5.6% state Transaction Privilege Tax (TPT), legally on the dealer, passed to buyer like a sales tax; + county/city stacking at buyer ZIP (combined typically ~7.7%, up to 11.2% in Pinal County). Manufacturer rebates are NOT deducted from the taxable base; trade-in IS.
- **Doc fee cap**: **No statutory dollar cap.** A.R.S. requires only that the fee be "reasonable." Typical AZ doc fee runs $395-499 (median ~$499); some dealers quote $500-700. Treat anything above ~$500 as a negotiation target / potential leak, there is no ceiling protecting you, so push it down at the OTD line.
- **Title fee**: $4. **Registration**: ~$50/year fixed fees ($8 reg + $5 plate + $1.50 air quality + small compliance), PLUS the annual Vehicle License Tax (VLT) assessed on 60% of base MSRP at $2.80/$100 new ($2.89/$100 used), the VLT is the big recurring number, not the flat fees.
- **Trade-in tax credit**: **YES**, taxable base is sale price minus trade-in value. You save 5.6%+ on the trade amount.
- **Has**: 5.6% state TPT + local stacking; VLT on the value of the vehicle each year; $4 title; standard reg fees.
- **Does NOT have**: statutory doc fee cap; tax on private/casual sales (private-party purchases are untaxed in AZ); rebate deduction from the tax base; a flat EV registration surcharge (EVs ride the VLT formula, historically at a reduced assessment basis).

#### AZ Worked OTD Example (Maricopa County ~8.0% combined, no trade)

Sales $30,000, doc $499, AZ 8.0% combined:

```
Taxable = $30,000 + $499 = $30,499
Tax     = $30,499 × 0.08 = $2,439.92
Title   = $4
Reg     = ~$50 flat fees (VLT billed separately on value)
OTD     = $30,499 + $2,439.92 + $4 + $50 = $32,992.92
```

#### AZ Worked OTD Example (Maricopa County ~8.0% combined, $5,000 trade)

Sales $30,000, doc $499, trade $5,000, AZ 8.0% combined:

```
Net sale = $30,000 - $5,000 = $25,000
Taxable  = $25,000 + $499 = $25,499
Tax      = $25,499 × 0.08 = $2,039.92
Title    = $4
Reg      = ~$50 flat fees
Cash OTD = $25,499 + $2,039.92 + $4 + $50 = $27,592.92
Tax savings on trade = $5,000 × 0.08 = $400
```

verified: 2026-06-22 | source: azdor.gov Motor Vehicle Sales (TPT 5.6%, trade-in deduction, $4 title) + SalesTaxHandbook AZ (combined rate range, no doc cap) | by: orchestrator-S2

---

### CA, California

- **Sales tax**: 7.25% statewide base (the highest state base rate in the US), levied as sales/use tax; **+ district (local) tax 0.10-2.00%** added at the buyer's registration ZIP, so the combined rate runs ~7.75-10.75%. The taxable rate is keyed to where the vehicle will be primarily kept/registered, not where the dealer sits (CDTFA). Use tax on private-party buys is collected by DMV at registration.
- **Doc fee cap**: **$85 statutory cap** for dealers that are DMV business partners under Veh. Code § 1685, and **$70** for non-partner dealers (CA Vehicle Code §§ 11713.1(g) and 4456.5; charge must be itemized and disclosed per Civ. Code § 2982, the Automobile Sales Finance Act). This is by far the lowest doc-fee ceiling in the country. **SB 791 (2025)** would have raised it to the lesser of 1% of price or $260, but **Governor Newsom vetoed it in October 2025**, so the $85/$70 caps remain in force. Treat any doc/"DPC" line above $85 as a leak.
- **Title fee**: $15 (basic title transfer). **Registration**: ~$250 first-year cash all-in (base reg ~$74 + CHP $32 + value-based Transportation Improvement Fee $27-$192 by vehicle value under SB 1 + 0.65% Vehicle License Fee); annualized.
- **Trade-in tax credit**: **NO.** California taxes the full negotiated sale price; a trade-in (and manufacturer rebates) do NOT reduce the taxable base. This is California's structural disadvantage versus trade-credit states like Texas, on a $7k trade you lose ~$540 of tax savings you'd get next door.
- **Has**: district transaction tax at buyer ZIP; CHP fee $32; Vehicle License Fee 0.65% of value; Transportation Improvement Fee (value-tiered); **ZEV / EV Road Improvement Fee $118/yr** on 2020-and-newer zero-emission vehicles at renewal; smog/emissions transfer fee on many used sales.
- **Does NOT have**: trade-in tax credit; rebate tax credit; arbitrary local-rate stacking beyond the published district tax; Texas-style SPV minimum-value tax floor; GA TAVT; NC highway-use tax; an MD-style high doc cap.

#### CA Worked OTD Example (Los Angeles County, 9.50% combined, no trade)

Sales $30,000, doc $85, CA 9.50% (7.25% state + 2.25% LA district):

```
Taxable = $30,000 + $85 = $30,085   # doc is taxable; no trade reduction
Tax     = $30,085 × 0.0950 = $2,858.08
Title   = $15
Reg     = $250 (first-year all-in, annualized)
OTD     = $30,000 + $85 + $2,858.08 + $15 + $250 = $33,208.08
```

#### CA Worked OTD Example (Los Angeles County, 9.50%, $7,000 trade)

Sales $30,000, doc $85, trade $7,000, CA 9.50%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $30,085   # FULL price + doc — CA gives NO trade credit, trade does not reduce tax
Tax        = $30,085 × 0.0950 = $2,858.08
Title      = $15
Reg        = $250
Cash OTD   = $23,000 + $85 + $2,858.08 + $15 + $250 = $26,208.08
Tax savings on trade = $0  (California does not credit trade-ins — called out)
```

verified: 2026-06-22 | source: CA Vehicle Code §§ 11713.1 & 4456.5 (doc cap) + CA DMV VIRP manual 3.030 + CDTFA tax-rate FAQ (7.25% + district) | by: orchestrator-S1

---

### CO, Colorado

- **Sales tax**: 2.9% state (the lowest state rate in the US) + county (up to 5%) + city/special district. At Denver and Boulder ZIPs the combined rate is ~8.85%. Use the buyer's exact ZIP, Colorado is heavily home-rule, so two addresses a mile apart can differ. Trade-in reduces the base at dealers; rebates/incentives do NOT.
- **Doc fee cap**: **No statutory cap.** Often labeled "dealer handling fee" on CO paperwork. Typical $400-700, with Denver-metro dealers commonly at the high end. No legal ceiling, negotiate to the OTD number.
- **Title fee**: ~$7 ($4 state + $3.20 county clerk). **Registration**: ~$67/year (road safety $23 + bridge safety $32 + license $6 + small clerk/EMS), plus the annual Specific Ownership Tax (SOT) on 85% of original MSRP, declining by vehicle age (2.10% yr1 down to ~$3 flat by yr10). A $29 Keep Colorado Wild Pass is added by default (opt-out available).
- **Trade-in tax credit**: **YES at a dealer**, taxable base is price minus trade. **Caveat**: this applies only to dealer sales; private-party buyers get no trade deduction.
- **Has**: 2.9% state + home-rule local stacking; SOT each year on MSRP basis; ~$7 title; ~$67 reg; $73/year EV fee (BEV); Keep Colorado Wild Pass $29; $40 lien filing fee on financed vehicles (eff 2025-07-01).
- **Does NOT have**: statutory doc fee cap; rebate deduction from the tax base; trade-in credit on private-party sales.

Home-rule note: Denver (80202 etc.) and Boulder (80301 etc.) ZIPs land near 8.85% combined; always price at the delivery ZIP, not the state rate.

#### CO Worked OTD Example (Denver 80202, ~8.81% combined, no trade)

Sales $30,000, doc $600, CO ~8.81% combined:

```
Taxable = $30,000 + $600 = $30,600
Tax     = $30,600 × 0.0881 = $2,695.86
Title   = $7
Reg     = ~$67 (+ $29 Wild Pass, opt-out; SOT billed on MSRP basis)
OTD     = $30,600 + $2,695.86 + $7 + $67 = $33,369.86
```

#### CO Worked OTD Example (Denver 80202, ~8.81% combined, $5,000 trade)

Sales $30,000, doc $600, trade $5,000, CO ~8.81% combined:

```
Net sale = $30,000 - $5,000 = $25,000
Taxable  = $25,000 + $600 = $25,600
Tax      = $25,600 × 0.0881 = $2,255.36
Title    = $7
Reg      = ~$67
Cash OTD = $25,600 + $2,255.36 + $7 + $67 = $27,929.36
Tax savings on trade = $5,000 × 0.0881 = $440.50
```

verified: 2026-06-22 | source: dmv.colorado.gov Taxes and Fees (2.9% state, trade-in deduction, $4+$3.20 title, EV fee) + SalesTaxHandbook CO (combined rate / Denver-Boulder 8.85%, no doc cap) | by: orchestrator-S2

---

### DE, Delaware

- **Sales tax**: **None.** Delaware levies a state **document fee in lieu of sales tax**: **5.25%** of the greater of purchase price or NADA trade-in value, paid once at titling. (Rate increased from 4.25% to 5.25% effective **2025-10-01**.) Revenue goes to the Transportation Trust Fund. No local sales tax exists in DE.
- **Doc fee cap**: The 5.25% figure is the *state title document fee* (the tax mechanism), not a dealer processing fee. Delaware does **not cap** a separate dealer doc/processing fee. Do not confuse the 5.25% state doc fee with a dealer add-on.
- **Title fee**: ~$35 (cash/clean title; ~$55 if financed/lien). **Registration**: $40/yr (registrable up to 5 years).
- **Trade-in tax credit**: **N/A, no sales tax.** However, a trade-in (or qualifying private sale within 60 days) *does* reduce the 5.25% document-fee base; manufacturer rebates do not.
- **Does NOT have**: traditional sales tax; local sales tax stacking; a separate sales-tax-based trade credit (the doc fee is the only purchase tax).

#### DE Worked OTD Example (Wilmington, no trade)

Sales $30,000, doc fee 5.25%:

```
Doc fee = max($30,000, NADA) × 0.0525 = $30,000 × 0.0525 = $1,575
Title   = $35
Reg     = $40
OTD     = $1,575 + $35 + $40 + $30,000 = $31,650
```

#### DE Worked OTD Example (Wilmington, $8,000 trade)

Sales $30,000, trade $8,000, doc fee 5.25%:

```
Net base = $30,000 - $8,000 = $22,000   (trade reduces the doc-fee base)
Doc fee  = $22,000 × 0.0525 = $1,155
Title    = $35
Reg      = $40
Cash OTD = $1,155 + $35 + $40 + $22,000 = $23,230
Doc-fee savings on trade = $8,000 × 0.0525 = $420
```

verified: 2026-06-22 | source: https://news.delaware.gov/2025/09/30/dmv-fees-increase-in-october-2025/ + https://dmv.de.gov/Common/DMVFees/index.shtml | by: orchestrator-S4

---

### HI, Hawaii

- **Sales tax**: No traditional sales tax, Hawaii uses the **General Excise Tax (GET)**, 4.0% statewide, plus a **0.5% county surcharge now in effect in all four counties** (Honolulu, Kauai, Maui, Hawaii Island) = **4.5%** on vehicle purchases. Because GET is a tax on the seller, dealers may pass on a "tax-on-tax" rate up to **4.712%** (incl. surcharge).
- **Doc fee cap**: **No statutory cap identified** (secondary-sourced; no HRS provision found). UNVERIFIED as a hard statutory fact, flag any unusually high doc fee.
- **Title fee**: $10 (HRS § 286-41). **Registration**: ~$66.50 base first year (state $46 per HRS § 249-3 + county $20 + highway beautification $7 + emblem $0.50 + plate $5 - example), PLUS a state weight tax (1.75¢/lb up to 4,000 lb, HRS § 249-33) and a county weight tax that varies sharply by island.
- **Trade-in tax credit**: **NO**, trade-ins do not reduce the GET base; only dealer discounts do. This is the opposite of most mainland states and a structural disadvantage.
- **EV surcharge**: $50/yr (HRS § 249-3.5); HiRUC road-usage option may substitute.
- **Does NOT have**: traditional retail sales tax (uses GET); trade-in tax credit; doc-fee statutory cap.

#### HI Worked OTD Example (Honolulu, no trade)

Sales $30,000, doc $300, GET pass-on 4.712%:

```
GET (pass-on) = $30,000 x 0.04712 = $1,413.60
Doc           = $300
Title         = $10
Reg + weight  = ~$66.50 base + ~$58 state weight (3,300 lb) = ~$125
OTD           = $30,000 + $1,413.60 + $300 + $10 + $125 = ~$31,848.60
```

verified: 2026-06-22 | source: tax.hawaii.gov County Surcharge + GET pages (HRS §§ 237/238) + HRS §§ 249-3/249-3.5/286-41 via comparemechanic | by: orchestrator-S7

---

### IA, Iowa

- **Sales tax**: **None** in the traditional sense. Iowa charges a **5% "Fee for New Registration"** (Iowa Code § 321.105A) in lieu of sales tax on every vehicle transfer (new/used, dealer/private). No local stacking. Formula: $10 + (Net Purchase Price × 0.05).
- **Doc fee cap**: **No statutory cap.** Iowa law does not limit dealer doc fees; typical ~$135.
- **Title fee**: ~$25. **Registration**: ~$100/yr (annual fee is a separate weight + list-price declining-rate formula, Iowa Code §§ 321.109 to 321.124).
- **Trade-in tax credit**: **YES**, Net Purchase Price = Purchase Price − Trade-In − Rebate, so both trade-in and rebates reduce the 5% fee base.
- **EV surcharge**: $130/yr full EV (BEV); $65 PHEV; $9 electric motorcycle. Statute Iowa Code § 321.116 (HF 767), fully phased in since CY2022.
- **Does NOT have**: traditional sales tax (5% Fee for New Registration applies instead); local sales tax stacking; statutory doc fee cap.

#### IA Worked OTD Example (Polk County / Des Moines, no trade)

Sales $30,000, doc $135, IA 5% Fee for New Registration:

```
Net price = $30,000
Fee for New Reg = $10 + ($30,000 × 0.05) = $10 + $1,500 = $1,510
Title   = $25
Annual reg = $100 (weight + list-price formula; declines with age)
Doc     = $135
OTD     = $1,510 + $25 + $100 + $135 + $30,000 = $31,770
```

#### IA Worked OTD Example (Polk County / Des Moines, $8,000 trade)

Sales $30,000, trade $8,000, IA 5%:

```
Net price = $30,000 - $8,000 = $22,000
Fee for New Reg = $10 + ($22,000 × 0.05) = $10 + $1,100 = $1,110
Title   = $25
Annual reg = $100
Cash OTD = $1,110 + $25 + $100 + $22,000 = $23,235
Tax savings on trade = $8,000 × 0.05 = $400
```

verified: 2026-06-22 | source: https://www.legis.iowa.gov/docs/code/321.105A.pdf + https://www.legis.iowa.gov/docs/code/321.116.pdf | by: orchestrator-S4

<!-- Batch S5 detail-stubs: AR, KS, MS, NM, UT. lite stub depth. All verified 2026-06-22 against 2 authoritative sources each. -->

---

### ID, Idaho

- **Sales tax**: flat 6% state sales tax on vehicles; **no local add-on** on motor vehicle sales (Idaho restricts local-option sales tax from applying to motor vehicles even in resort areas). Taxable base is reduced by trade-in; NOT reduced by rebates (Idaho taxes before rebates).
- **Doc fee cap**: **No statutory cap**, must be disclosed but is uncapped; median ~$265, dealer ranges to ~$399. Doc fee is NOT taxable and does not reduce the taxable amount.
- **Title fee**: $14. **Registration**: base ~$69/yr (age-tiered) + county admin fee $3-$14; example total ~$78.50/yr (Ada County, mid-age vehicle).
- **Trade-in tax credit**: **YES**, trade-in value is deducted from the taxable price.
- **Has**: EV registration fee $140/yr and plug-in hybrid fee $75/yr, in addition to standard registration, under Idaho Code § 49-457.
- **Does NOT have**: statutory doc fee cap; local sales tax stacking on vehicles; NY MCTD fee; NJ supplemental titling fee; GA TAVT; NC highway use tax.

#### ID Worked OTD Example (Ada County / Boise, no trade)

Sales $30,000, doc $299, ID 6% (doc not taxable):

```
Taxable = $30,000
Tax     = $30,000 x 0.06 = $1,800
Title   = $14
Reg     = ~$78.50 (base + county admin)
Doc     = $299
OTD     ~ $32,191.50
```

#### ID Worked OTD Example (Boise, $8,000 trade)

Sales $30,000, trade $8,000, doc $299, ID 6%:

```
Net sale = $30,000 - $8,000 = $22,000
Tax      = $22,000 x 0.06 = $1,320
Title    = $14
Reg      = ~$78.50
Doc      = $299
Cash OTD ~ $23,711.50; tax savings on trade = $480
```

verified: 2026-06-22 | source: Idaho State Tax Commission Sales & Use Tax Guide for Vehicle Transactions (tax.idaho.gov); Idaho Code § 49-457 (legislature.idaho.gov); SalesTaxHandbook ID | by: orchestrator/S6

<!-- Batch S7 detail-stubs: MT, OR, NH, AK, HI, WY. Lite stubs to round out the 50+DC set. -->

---

### IN, Indiana

- **Sales tax**: 7% flat statewide. Indiana has **no local or county sales tax** on vehicles, you pay 7% no matter where in the state you buy. Trade-in reduces the base; manufacturer rebates do NOT.
- **Doc fee cap**: **$251.05** (effective 2025-07-01), the document preparation fee under **IC 9-32-13-7**. The statutory base is $200, CPI-indexed annually; the SOS Auto Dealer Services Division publishes the no-enforcement threshold ($237.51 in 2023, $251.05 from 2025-07-01). Charging above the published figure or hiding the fee is an unfair practice (civil penalty up to $10,000/violation). This is a real, enforced cap, among the tighter ones in this batch.
- **Title fee**: $15. **Registration**: ~$40/year ($15 BMV base + annual excise tax on MSRP/age basis + county fee, most counties +$7.50).
- **Trade-in tax credit**: **YES**, taxable base is price minus trade-in value.
- **Has**: 7% flat state tax; $15 title; BMV reg + MSRP-based excise + county fee; **EV supplemental registration fee** (statutory base $150 under IC 9-18.1-5-12, fuel-index-adjusted to ~$230 currently); hybrid supplemental ~$77 (base $50).
- **Does NOT have**: local/county sales tax stacking (flat 7% everywhere); rebate deduction from the tax base.

EV note: the JSON uses $230 (the current fuel-index-adjusted figure per DOE/AFDC and IRP); the statutory base in IC 9-18.1-5-12 is $150. If a dealer/BMV quote shows $150 it is the un-indexed base, confirm the current-year amount with the BMV Fee Chart.

#### IN Worked OTD Example (statewide 7%, no trade)

Sales $30,000, doc $251.05 (at cap), IN 7%:

```
Taxable = $30,000 + $251.05 = $30,251.05
Tax     = $30,251.05 × 0.07 = $2,117.57
Title   = $15
Reg     = ~$40 (BMV base + excise + county)
OTD     = $30,251.05 + $2,117.57 + $15 + $40 = $32,423.62
```

#### IN Worked OTD Example (statewide 7%, $5,000 trade)

Sales $30,000, doc $251.05, trade $5,000, IN 7%:

```
Net sale = $30,000 - $5,000 = $25,000
Taxable  = $25,000 + $251.05 = $25,251.05
Tax      = $25,251.05 × 0.07 = $1,767.57
Title    = $15
Reg      = ~$40
Cash OTD = $25,251.05 + $1,767.57 + $15 + $40 = $27,073.62
Tax savings on trade = $5,000 × 0.07 = $350
```

verified: 2026-06-22 | source: IN SOS Auto Dealer Services "Doc Fees in 2025" PDF + IC 9-32-13-7 ($251.05 cap eff 2025-07-01) + IC 9-18.1-5-12 / DOE-AFDC (EV supplemental) + SalesTaxHandbook IN (flat 7%, trade-in deduction) | by: orchestrator-S2

---

### KS, Kansas

- **Sales tax**: 6.5% state sales tax; + 0-4% local at the buyer's county of residence (combined can reach ~11.5%). Rate is the buyer's home county rate, not the seller/treasurer location.
- **Doc fee cap**: **No statutory cap.** Dealer-set, typical ~$285. Note the doc fee is itself part of taxable gross receipts under KS Dept. of Revenue Pub. KS-1526, it is taxed.
- **Title fee**: $10. **Registration**: ~$40/yr (passenger baseline; weight-based).
- **Trade-in tax credit**: **YES**, tax applies to the net trade difference. Credit is capped at the value of the vehicle received (a trade worth more than the purchased vehicle zeroes the tax but does not refund). Manufacturer rebates paid to the purchaser remain taxable per KS-1526.
- **Has**: EV annual registration fee $100 (BEV) / $50 (PHEV/HEV). Per KS legislative research, the Kansas EV fee is structured *in lieu of* (replacing) other registration fees, unlike most states which add it on top.
- **Does NOT have**: statutory doc fee cap; no trade-in credit denial.

#### KS Worked OTD Example (Sedgwick County ~7.5%, $26,000 new, $6,300 trade)

```
Net sale = $26,000 - $6,300 = $19,700
Taxable  = $19,700 + $285 doc = $19,985
Tax      = $19,985 x 0.075 = $1,498.88
Title    = $10
Reg      = $40
OTD      = 19,985 + 1,498.88 + 10 + 40 = $21,533.88
Tax savings on trade = $6,300 x 0.075 = $472.50
```

verified: 2026-06-22 | source: KS Dept. of Revenue Pub. KS-1526 (tax/trade/doc) + SalesTaxHandbook KS vehicles + AFDC law 12182 (EV fee) | by: agent-S5

---

### KY, Kentucky

- **Sales tax**: 6% **motor vehicle usage tax** (in lieu of property tax at purchase), flat statewide; **no local usage tax stacking**, 6% is the most you pay.
- **Doc fee cap**: **No statutory cap.** Dealer doc fees are set by dealers; Kentucky does not legislate a ceiling.
- **Title fee**: $9. **Registration**: $21/yr (passenger). (Note: the seed value of $65 was stale; current KY passenger base registration is $21.)
- **Trade-in tax credit**: **YES (new vehicles)**, per KY DOR, since 2014-07-01 trade-in allowance is granted on the usage-tax base for new-vehicle purchases. For **used** vehicles a trade-in also reduces the base, but a "50% floor" rule applies and both vehicles must have been previously KY-registered. NOTE: the S4 batch brief described KY as "no trade credit"; the authoritative DOR page contradicts that, so this stub follows DOR (posture = yes).
- **EV surcharge**: $120/yr full EV; $60 hybrid/electric motorcycle. Statute KRS 138.475, annually CPI-adjusted (max +5%/yr), in effect since 2024.
- **Does NOT have**: local sales/usage tax stacking; statutory doc fee cap.

#### KY Worked OTD Example (Louisville, no trade)

Sales $30,000, KY usage tax 6%:

```
Taxable = $30,000
Usage tax = $30,000 × 0.06 = $1,800
Title   = $9
Reg     = $21
OTD     = $1,800 + $9 + $21 + $30,000 = $31,830
```

#### KY Worked OTD Example (Louisville, $8,000 trade, new vehicle)

Sales $30,000, trade $8,000, KY usage tax 6%:

```
Net taxable = $30,000 - $8,000 = $22,000   (new-vehicle trade credit)
Usage tax   = $22,000 × 0.06 = $1,320
Title       = $9
Reg         = $21
Cash OTD    = $1,320 + $9 + $21 + $22,000 = $23,350
Tax savings on trade = $8,000 × 0.06 = $480
```

verified: 2026-06-22 | source: https://revenue.ky.gov/Property/Motor-Vehicles/Pages/Motor-Vehicle-Usage-Tax.aspx + https://drive.ky.gov/Pages/EV-HV-Fee.aspx | by: orchestrator-S4

---

### LA, Louisiana

- **Sales tax**: **5% state** sales/use tax on vehicles (raised from 4.45% to 5% effective **2025-01-01** under 2024 HB10 / Act 11; scheduled to step down to 4.75% on 2030-01-01), the old 4.45% figure is **outdated**. **Plus parish/municipal local tax of roughly 4-7%**, so the combined rate at the buyer's registration parish/ZIP commonly lands in the **~9-10%** band and can reach ~12.95% in the highest-rate locales. The taxable rate follows the buyer's parish of registration, not the dealer's.
- **Doc fee cap**: **~$436**, CPI-indexed (max 3%/yr increase, published annually by the LA Motor Vehicle Commission) under **La. R.S. 6:969.18(A)(2)**, with the current figure effective **2025-07-04** (Acts 2025 No. 502). This replaced the prior $200 cap the seed carried, that **$200 figure is outdated**. The cap has climbed $35 -> $200 -> $425 (2020 SB144) -> ~$436. Confirm the exact published number against the LMVC site for a given year; treat a doc/compliance fee materially above the published cap as a leak.
- **Title fee**: $68.50 (La. R.S. 32:728) plus an $8 handling fee per transaction. **Registration**: value-based at 0.1% of vehicle value, issued for 2-year periods (min $20/2yr on a $10,000-floor value); the ~$25/yr figure reflects a typical annualized passenger plate.
- **Trade-in tax credit**: **YES**, taxable base is sale price minus trade-in allowance.
- **Has**: 5% state + parish/municipal local tax (~9-10% combined); EV/hybrid **road-usage fee $110/yr EV, $60/yr hybrid** (per LA OMV); $8 handling fee; optional Public Tag Agent convenience fee up to $23.
- **Does NOT have**: IMF; TAVT; highway-use tax; a Texas-style SPV minimum-value floor; a trade-in tax disadvantage.

#### LA Worked OTD Example (East Baton Rouge Parish, ~9.95% combined, no trade)

Sales $30,000, doc $436, LA 5% state + 4.95% parish = 9.95%:

```
Taxable = $30,000   # LA vehicle tax is on the sale price (trade-adjusted); doc is not in the tax base
Tax     = $30,000 × 0.0995 = $2,985.00
Title   = $68.50
Handling= $8.00
Reg     = $25 (annualized passenger plate)
Doc     = $436 (current CPI-indexed cap)
OTD     = $30,000 + $436 + $2,985.00 + $68.50 + $8.00 + $25 = $33,522.50
```

#### LA Worked OTD Example (East Baton Rouge Parish, ~9.95%, $7,000 trade)

Sales $30,000, doc $436, trade $7,000, LA 9.95%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $23,000   # trade credited against the taxable base
Tax        = $23,000 × 0.0995 = $2,288.50
Title      = $68.50
Handling   = $8.00
Reg        = $25
Doc        = $436
Cash OTD   = $23,000 + $436 + $2,288.50 + $68.50 + $8.00 + $25 = $25,826.00
Tax savings on trade = $7,000 × 0.0995 = $696.50
```

verified: 2026-06-22 | source: La. R.S. 6:969.18 (doc cap ~$436, eff 2025-07-04) + Sales Tax Institute / 2024 HB10 Act 11 (state 5%, eff 2025-01-01) + LA OMV fee schedule (title $68.50, EV $110) | by: orchestrator-S3

---

### MN, Minnesota

- **Sales tax**: 6.875% Motor Vehicle Sales Tax (MVST) on the taxable sale price; rate rose from 6.5% to **6.875% effective 2023-07-01** (Minn. Stat. § 297B). **No general local sales tax stacks on vehicles**, MVST is the whole tax. A few counties/cities (e.g., metro transit-improvement jurisdictions) add a flat **$20 vehicle excise tax** per sale, but it is a fixed dollar amount, not a percentage, so the combined "rate" stays 6.875%.
- **Doc fee cap**: **$350 statutory cap** (the lesser of $350 or 10% of sale value; the 10% prong only matters on vehicles at or under $3,499), under **Minn. Stat. § 168.27 subd. 31**, effective **2025-07-01** (HF1513). This replaced Minnesota's long-standing very-low caps ($75, then $125), the old "$125 MN doc cap" you may see cited is **outdated**. Treat any doc/"document administration" line above $350 as a leak.
- **Title fee**: $11 (transfer). **Registration**: MSRP/value-based, roughly 1.285-1.575% of the depreciating base value plus a $10 flat, so first-year tabs on a ~$30-35k car run ~$400-560 and fall each year to a $20 floor after year 11. The ~$100 figure is a rough mid-life annualized placeholder; real first-year cost is materially higher and value-driven.
- **Trade-in tax credit**: **YES**, the taxable price is sale price minus the trade-in allowance (and minus rebates), confirmed by MN Dept. of Revenue. Exception: trading in an off-road vehicle (ATV/watercraft/snowmobile) does NOT reduce the base.
- **Has**: $20 flat county/city vehicle excise tax in some jurisdictions; **$75/yr EV registration surcharge** on all-electric vehicles (Minn. Stat. § 168.013 subd. 1m), note this rises to a $150 minimum EV / $75 PHEV (MSRP-scaled) **beginning 2026-01-01**, but for current-year purposes the surcharge is $75; rebate amounts are not taxed (rebates DO reduce the base in MN, unlike most states).
- **Does NOT have**: percentage local sales-tax stacking on vehicles; TAVT; highway-use tax; IMF; a Texas-style SPV minimum-value floor; GA TAVT; NC HUT.

#### MN Worked OTD Example (Hennepin County, no trade)

Sales $30,000, doc $350, MN 6.875% MVST + $20 county excise:

```
Taxable = $30,000   # MN MVST is on the vehicle sale price; doc fee is not in the MVST base
Tax     = $30,000 × 0.06875 = $2,062.50
Excise  = $20 (flat county vehicle excise)
Title   = $11
Reg     = $100 (mid-life annualized placeholder; first-year value-based is higher)
Doc     = $350 (statutory cap)
OTD     = $30,000 + $350 + $2,062.50 + $20 + $11 + $100 = $32,543.50
```

#### MN Worked OTD Example (Hennepin County, $7,000 trade)

Sales $30,000, doc $350, trade $7,000, MN 6.875%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $23,000   # MN credits the trade-in against the MVST base
Tax        = $23,000 × 0.06875 = $1,581.25
Excise     = $20
Title      = $11
Reg        = $100
Doc        = $350
Cash OTD   = $23,000 + $350 + $1,581.25 + $20 + $11 + $100 = $25,062.25
Tax savings on trade = $7,000 × 0.06875 = $481.25
```

verified: 2026-06-22 | source: MN Dept. of Revenue Motor Vehicle Sales guide (6.875% + trade credit) + Minn. Stat. § 168.013 (EV $75) + Minn. Stat. § 168.27 subd. 31 / HF1513 + MADA (doc cap $350, eff 2025-07-01) | by: orchestrator-S3

---

### MO, Missouri

- **Sales tax**: 4.225% state + county/city/special district stacking (0-5.5% at buyer ZIP). Use the buyer's home address, MO taxes the vehicle at the purchaser's domicile rate, not the dealer's. Trade-in reduces the base.
- **Doc fee cap**: **$604.47** for the 2025 licensure year (rule effective 2025-08-17), the dealer "administrative fee" under **RSMo § 301.558**, with the dollar table in **12 CSR 10-26.231**. Base $500 (2021), CPI-indexed annually: $523.50 (2022), $565.38 (2023), $587.43 (2024), $604.47 (2025). Two wrinkles: the dealer must remit 10% of every administrative fee collected to the MV Administration Technology Fund, and must charge a single uniform declared fee to all retail buyers for the license period. Capped, but the cap is high (~$604), one of the most generous in this batch.
- **Title fee**: $11 (plus $8.50 processing in practice). **Registration**: ~$50/year (varies by horsepower/weight).
- **Trade-in tax credit**: **YES**, taxable base is price minus trade-in value.
- **Has**: 4.225% state + local stacking at buyer ZIP; CPI-indexed administrative fee up to $604.47; $11 title; HP/weight-based reg.
- **Does NOT have**: an uncapped doc fee (it is capped, just generously); tax on the trade-in value.

#### MO Worked OTD Example (St. Louis County ~8.0% combined, no trade)

Sales $30,000, admin fee $604.47 (at cap), MO ~8.0% combined:

```
Taxable = $30,000 + $604.47 = $30,604.47
Tax     = $30,604.47 × 0.08 = $2,448.36
Title   = $11
Reg     = ~$50
OTD     = $30,604.47 + $2,448.36 + $11 + $50 = $33,113.83
```

#### MO Worked OTD Example (St. Louis County ~8.0% combined, $5,000 trade)

Sales $30,000, admin fee $604.47, trade $5,000, MO ~8.0% combined:

```
Net sale = $30,000 - $5,000 = $25,000
Taxable  = $25,000 + $604.47 = $25,604.47
Tax      = $25,604.47 × 0.08 = $2,048.36
Title    = $11
Reg      = ~$50
Cash OTD = $25,604.47 + $2,048.36 + $11 + $50 = $27,713.83
Tax savings on trade = $5,000 × 0.08 = $400
```

verified: 2026-06-22 | source: RSMo § 301.558 (revisor.mo.gov) + 12 CSR 10-26.231 ($604.47 max 2025, eff 2025-08-17, via Cornell LII) + SalesTaxHandbook MO (4.225% state, local stacking, trade-in deduction) | by: orchestrator-S2

---

### MS, Mississippi

- **Sales tax**: 5% state sales tax on cars/light trucks <=10,000 lb GVW (3% for carriers of property / trucks over 10,000 lb), per Miss. Code § 27-65-201. No local sales-tax stacking on the purchase, but counties levy an ad valorem (property) tax at registration that dominates total Mississippi registration cost.
- **Doc fee cap**: **No statewide statutory cap.** Dealer-set, typical ~$230.
- **Title fee**: $9. **Registration**: ~$25/yr base tag (plus county ad valorem, value-based, separate).
- **Trade-in tax credit**: **YES**, tax on net difference (new vehicle true value minus trade allowance), per § 27-65-201. Manufacturer rebates do NOT reduce the taxable base; dealer discounts do.
- **Has**: EV annual registration surcharge $150 (BEV) / $75 (PHEV/HEV), Miss. Code §§ 27-19-21/23, indexed for inflation annually since 2021-07-01. County ad valorem tax at registration (with 5% legislative tag credit).
- **Does NOT have**: statutory doc fee cap; no trade-in credit denial; no local sales-tax stacking on the 5% purchase tax.

#### MS Worked OTD Example (Hinds County, $30,000 new, $10,000 trade, gas car)

```
Net sale = $30,000 - $10,000 = $20,000
Taxable  = $20,000 + $230 doc = $20,230
Tax      = $20,230 x 0.05 = $1,011.50
Title    = $9
Reg      = $25 (base tag; county ad valorem billed separately, value-based)
OTD      = 20,230 + 1,011.50 + 9 + 25 = $21,275.50
Tax savings on trade = $10,000 x 0.05 = $500.00
```

verified: 2026-06-22 | source: Miss. Code § 27-65-201 (5% tax + net-difference trade) + AFDC ELEC MS (EV $150/$75, §§ 27-19-21/23) + SalesTaxHandbook MS vehicles | by: agent-S5

---

### MT, Montana

- **Sales tax**: 0%, Montana is one of five no-sales-tax states. No state or local *sales* tax on vehicles, so trade-ins are tax-irrelevant. Caveat: 45 of 56 counties levy a separate **county option tax** (~0.3-0.5% of depreciated MSRP, per § 61-3-503 MCA) collected with registration, not a sales tax, but a real recurring cost.
- **Doc fee cap**: **No statutory cap.** Typical industry doc fee ~$224. Treat anything well above that as a leak.
- **Title fee**: $10.30 (this is the *replacement* title fee, incl. 3% admin per § 61-3-111 MCA; a new title is bundled into registration). **Registration**: $217/yr for vehicles 0-4 yrs, $87 for 5-10 yrs, $28 for 11+ yrs (age-based flat fee, § 61-3-321(2)(d) MCA, incl. 3% admin). A $150k+ MSRP vehicle ≤10 yrs adds an $825/yr luxury surcharge.
- **Trade-in tax credit**: N/A, no sales tax to offset.
- **Does NOT have**: state sales tax; trade-in tax credit (moot); doc-fee cap; emissions/safety inspection at sale.

#### MT Worked OTD Example (Gallatin County, 0-4 yr vehicle, no trade)

Sales $30,000, doc $224, MT 0% sales tax:

```
Taxable    = n/a (no sales tax)
Tax        = $0
Doc        = $224
Title      = $0 (bundled into reg; replacement title would be $10.30)
Reg        = $217 (age 0-4 yr, incl 3% admin)
County opt = ~$45 (0.5% of ~$9,000 depreciated MSRP — varies by county/age)
OTD        = $30,000 + $224 + $217 + ~$45 = ~$30,486
```

verified: 2026-06-22 | source: mvdmt.gov Light Vehicle Registration & Fees + § 61-3-321 MCA + SalesTaxHandbook (MT) | by: orchestrator-S7

---

### ND, North Dakota

- **Sales tax**: 5% motor vehicle **excise tax** (NDCC ch. 57-40.3), in lieu of general sales tax; **no local stacking** on motor vehicles. Calculated on net purchase price after trade-in.
- **Doc fee cap**: **No statutory cap**, North Dakota does not regulate a dealer doc fee ceiling. Title, registration, license, and doc fees are excluded from the excise-taxable price.
- **Title fee**: $5. **Registration**: weight-and-age based, base passenger fee ~$49/yr ranging up to ~$274/yr (annual). $1.50 abandoned-vehicle disposal fee on first ND titling.
- **Trade-in tax credit**: **YES**, 5% excise applies to purchase price minus trade-in allowance.
- **Has**: EV road-use surcharge $120/yr (all-electric); plug-in hybrid $50/yr, added at registration.
- **Does NOT have**: statutory doc fee cap; traditional sales tax on motor vehicles; local sales tax stacking on vehicles; safety/emissions inspection at sale; NY MCTD fee.

#### ND Worked OTD Example (Bismarck, no trade)

Sales $30,000, doc $200, ND 5% excise (doc NOT in excise base):

```
Taxable = $30,000 (doc fee excluded from excise base)
Excise  = $30,000 x 0.05 = $1,500
Title   = $5
Reg     = ~$49 (base passenger; scales by weight/age)
Doc     = $200
OTD     ~ $31,754
```

#### ND Worked OTD Example (Bismarck, $8,000 trade)

Sales $30,000, trade $8,000, ND 5% excise:

```
Net sale = $30,000 - $8,000 = $22,000
Excise   = $22,000 x 0.05 = $1,100
Title    = $5
Reg      = ~$49
Doc      = $200
Cash OTD ~ $21,354 + financed balance basis; tax savings on trade = $400
```

verified: 2026-06-22 | source: ND Motor Vehicle Excise Tax Guideline (tax.nd.gov); NDCC ch. 57-40.3 (ndlegis.gov); SalesTaxHandbook ND | by: orchestrator/S6

---

### NE, Nebraska

- **Sales tax**: 5.5% state sales tax; local stacking 0-2% at buyer ZIP (combined up to ~7.5%). Applied to sale price minus trade-in, after rebates.
- **Doc fee cap**: **No statutory cap**, typical industry doc fee is ~$280; treat anything materially above ~$350 as a leak and negotiate. Nebraska law requires disclosure but does not limit the amount.
- **Title fee**: $10. **Registration**: ~$30/yr base (annual), plus a separate MSRP-based Motor Vehicle Tax and Motor Vehicle Fee that scale by value/age, and ~$5.50 in fixed statutory surcharges (EMS, DMV cash, recreation, county) per year.
- **Trade-in tax credit**: **YES**, taxable base is sale price minus trade-in value.
- **Has**: EV/alternative-fuel registration surcharge of $150/yr on electric and hydrogen vehicles ($75 for plug-in hybrid / motorcycle), effective 2025-01-01 under Neb. Rev. Stat. § 60-3,191 (raised from $75).
- **Does NOT have**: statutory doc fee cap; NY MCTD fee; NJ supplemental titling fee; GA TAVT; NC highway use tax.

#### NE Worked OTD Example (Lincoln, ~7.0% combined, no trade)

Sales $30,000, doc $280, NE 7.0%:

```
Taxable = $30,000 + $280 = $30,280
Tax     = $30,280 x 0.07 = $2,119.60
Title   = $10
Reg     = ~$30 (base; MSRP-based MV tax/fee additional)
OTD     ~ $32,239.60 + value-based MV tax/fee
```

verified: 2026-06-22 | source: Nebraska DMV Registration Fees & Taxes (dmv.nebraska.gov); Neb. Rev. Stat. § 60-3,191; SalesTaxHandbook NE | by: orchestrator/S6

---

### NM, New Mexico

- **Sales tax**: Vehicles are NOT subject to ordinary retail gross-receipts/sales tax. Instead a flat **4% Motor Vehicle Excise Tax (MVET)**, uniform statewide (no local component), per NMSA § 7-14-4 (raised from 3% to 4% effective 2019-07-01). (The canonical JSON previously labeled this `sales_tax`; the verified mechanism is the MVET excise.)
- **Doc fee cap**: **No statutory cap.** A dealer transfer/document service fee is a separate add-on subject to gross-receipts tax and is explicitly NOT part of the MVET "price paid" base, so doc fees do not get MVET-taxed.
- **Title fee**: $5. **Registration**: $27-$62 for one year ($54-$124 biennial), by weight and model year, annualize the biennial figure; ~$35/yr is a representative passenger value.
- **Trade-in tax credit**: **YES**, trade-in allowances are deducted from "price paid" before the 4% MVET, per § 7-14-4. Contractually-guaranteed manufacturer rebates also reduce the base. A trade worth more than the purchase zeroes the MVET.
- **Has**: 50% MVET penalty if title not applied for within 90 days (effectively 6%). Out-of-state tax credit against MVET.
- **Does NOT have**: statutory doc fee cap; no traditional retail sales tax on vehicles (4% MVET excise instead); no trade-in credit denial; **no enacted statewide EV registration surcharge**, an EV fee (HB 145 / a 2025 DOT proposal) passed the House 65-0 but did NOT become law as of this verification, so ev_reg_surcharge is null.

#### NM Worked OTD Example (statewide 4% MVET, $40,000 new, $10,000 trade)

```
Net sale = $40,000 - $10,000 = $30,000   # "price paid" reduced by trade
Taxable  = $30,000  (doc fee is GRT-taxed separately, NOT in MVET base)
MVET     = $30,000 x 0.04 = $1,200.00
Title    = $5
Reg      = $35 (passenger, annualized from biennial)
OTD      = 30,000 + 1,200 + 5 + 35 = $31,240.00 (+ separately quoted doc fee + GRT on it)
Tax savings on trade = $10,000 x 0.04 = $400.00
```

verified: 2026-06-22 | source: NMSA § 7-14-4 (4% MVET, trade deduction) + NM Taxation & Revenue Motor Vehicle Excise Tax page | by: agent-S5

---

### NV, Nevada

- **Sales tax**: 4.6% state base + mandatory county add-ons; **minimum combined 6.85%**, average ~7.96%, max 8.375%, at buyer's county. Sales/use tax applies to dealer sales only, private-party transfers are exempt.
- **Governmental Services Tax (GST)**: a separate value-based annual reg charge = 4% of the depreciated DMV valuation (35% of original MSRP, depreciating), $16 minimum; Clark/Churchill counties add a Supplemental GST.
- **Doc fee cap**: **No statutory cap.** Dealer doc fees are unregulated by amount.
- **Title fee**: $28.25 (first-time). **Registration**: $33/yr base (passenger), plus GST/SGST above.
- **Trade-in tax credit**: **YES**, taxable base is sale price minus trade. Dealer rebates also reduce the base; manufacturer rebates do not.
- **EV surcharge**: **None**, Nevada has no statewide EV registration surcharge as of 2026.
- **Does NOT have**: EV registration surcharge; statutory doc fee cap; sales tax on private-party transfers.

#### NV Worked OTD Example (Clark County / Las Vegas, no trade)

Sales $30,000, doc $499, NV 8.375% (Clark combined):

```
Taxable = $30,000 + $499 = $30,499   (NV taxes doc fee)
Tax     = $30,499 × 0.08375 = $2,554
Title   = $28.25
Reg     = $33 (base; GST/SGST additional, value-based)
OTD     = $2,554 + $28.25 + $33 + $30,499 = $33,114.25
```

verified: 2026-06-22 | source: https://dmv.nv.gov/regfees.htm + https://www.salestaxhandbook.com/nevada/sales-tax-vehicles | by: orchestrator-S4

---

### OK, Oklahoma

- **Sales tax**: 3.25% flat **excise tax** in lieu of sales tax (47/68 O.S.); no state or local sales tax stacks on a titled vehicle. New vehicles taxed at 3.25% of price; used vehicles $20 on first $1,500 + 3.25% above. As of HB 1183 (effective 2026-07-01) excise is based on actual sales price, removing the +/-20% NADA-value band.
- **Doc fee cap**: **No statutory cap.** Title 47 / ONMVC advertising rules govern *disclosure* of the documentary fee, not its amount. Typical OK doc fee runs ~$300-$785 (avg ~$549), treat anything well above that as a leak.
- **Title fee**: $11. **Registration**: ~$96/yr (declining by vehicle age under 47 O.S. § 1132).
- **Trade-in tax credit**: **YES**, under SB 1619 the trade-in value is subtracted from purchase price before the 3.25% excise is computed.
- **EV surcharge**: $110/yr for full EVs (Class 1, gross weight <6,000 lbs); $82 PHEV. Statute 68 O.S. § 6511 (HB 1014X, in effect since 2024).
- **Does NOT have**: traditional state/local sales tax on titled vehicles; statutory doc fee cap; local tax stacking on the excise.

#### OK Worked OTD Example (Oklahoma City, no trade)

Sales $30,000, doc $549, OK excise 3.25%:

```
Taxable = $30,000 (excise on price; doc fee not part of excise base)
Excise  = $30,000 × 0.0325 = $975
Title   = $11
Reg     = $96
Doc     = $549
OTD     = $975 + $11 + $96 + $549 + $30,000 = $31,631
```

verified: 2026-06-22 | source: https://oklahoma.gov/service/all-services/auto-vehicle/fees.html + https://www.salestaxhandbook.com/oklahoma/sales-tax-vehicles + 68 O.S. § 6511 | by: orchestrator-S4

---

### OR, Oregon

- **Sales tax**: No general sales tax, BUT a **0.5% vehicle privilege tax** applies to dealer sales of new vehicles (2018+, <7,500 mi, never OR-titled), and a **0.5% use tax** on out-of-state purchases titled in OR. Dealers may pass the privilege tax to the buyer. No county sales-tax stacking.
- **Doc fee cap**: **$250** if the dealer uses an integrator, **$200** if not, capped by **ORS 822.043(4)** (amended 2025 c.415 §20; raised from the prior $150/$115). Negotiable; over-collection must be refunded within 5 business days.
- **Title fee**: ~$101. **Registration**: biennial, ~$126-$316 for two years depending on MPG class (≈$63-$158/yr); EV biennial surcharge ~$128 (≈$64/yr). Local/transit district fees may stack in some counties.
- **Trade-in tax credit**: **NO**, trade-in value does *not* reduce the 0.5% privilege-tax base; only manufacturer rebates/dealer discounts do. (Privilege tax is small, so impact is minor.)
- **Does NOT have**: general retail sales tax; trade-in credit against privilege tax; county sales-tax stacking.

#### OR Worked OTD Example (Multnomah County, new vehicle, no trade)

Sales $30,000, doc $250 (integrator), OR 0.5% privilege tax:

```
Privilege tax = $30,000 x 0.005 = $150
Doc           = $250
Title         = $101
Reg (2 yr)    = $254 (annualize ~$127/yr)
OTD           = $30,000 + $150 + $250 + $101 + $254 = $30,755
```

verified: 2026-06-22 | source: ORS 822.043 (oregon.public.law) + oregon.gov/odot/dmv fees + OR DOR Vehicle Privilege Tax | by: orchestrator-S7

---

### SC, South Carolina

- **Sales tax**: SC does **not** charge a traditional sales tax on titled vehicles. Instead it imposes a **5% Infrastructure Maintenance Fee (IMF)**, **capped at $500 per vehicle** (S.C. Code Ann. § 56-3-627). Because the IMF replaces sales/use tax, there is **no county/local rate stacking** on the vehicle. New residents titling an out-of-state car pay a flat **$250 IMF**.
- **$500 IMF cap, VERIFIED**: confirmed at 5% with a hard $500 ceiling under § 56-3-627. It was set at $500 effective **2017-07-01** (2017 Act 40, raising the prior $300 sales-tax cap), with the collection/titling mechanics amended by 2021 Act 70. On any vehicle priced above $10,000 the buyer hits the $500 cap.
- **Doc / "closing" fee cap**: **No hard dollar cap.** Under **S.C. Code Ann. § 37-2-307**, a dealer may set its own closing fee but must file an annual written notice with DOR/DMV (with a $10 filing fee). A closing fee **above $225** triggers a DOR "reasonableness" review; at or below $225 no review occurs. So $225 is a practical soft threshold, not a statutory maximum, treat a closing fee well above $225 as a flag worth questioning.
- **Title fee**: $15. **Registration**: ~$40/yr for a standard passenger vehicle (biennial $80 option also offered; annualized).
- **Trade-in tax credit**: **YES**, the trade-in allowance reduces the IMF base, and because of the $500 cap a trade-in can keep an otherwise-capped buyer under $500. SCDMV examples: $12,000 sale with $7,000 trade => IMF on $5,000 = $250; equal-value trade => $0 IMF. Rebates do NOT reduce the base.
- **Has**: 5% IMF (capped $500); dealer closing fee (uncapped, >$225 reviewable); standard title/reg. No EV registration surcharge currently in the structured data (none confirmed in this pass).
- **Does NOT have**: traditional state/local sales tax on titled vehicles; percentage local-rate stacking; a hard statutory doc/closing-fee dollar cap; TAVT; NC highway-use tax; a Texas-style SPV minimum-value floor.

#### SC Worked OTD Example (Richland County, $35k car, no trade, IMF capped)

Sales $35,000, closing fee $225, SC 5% IMF (capped $500):

```
IMF base = $35,000
IMF (5%) = $35,000 × 0.05 = $1,750  ->  CAPPED at $500
Title    = $15
Reg      = $40 (annualized)
Closing  = $225 (no-review threshold)
OTD      = $35,000 + $225 + $500 + $15 + $40 = $35,780.00
```

#### SC Worked OTD Example (Richland County, $35k car, $7,000 trade)

Sales $35,000, closing fee $225, trade $7,000, SC 5% IMF:

```
Net sale = $35,000 - $7,000 = $28,000
IMF base = $28,000   # trade credited against IMF base
IMF (5%) = $28,000 × 0.05 = $1,400  ->  still CAPPED at $500
Title    = $15
Reg      = $40
Closing  = $225
Cash OTD = $28,000 + $225 + $500 + $15 + $40 = $28,780.00
IMF savings on trade = $0 here (both pre- and post-trade IMF exceed the $500 cap, so the cap, not the trade, governs)
```

verified: 2026-06-22 | source: S.C. Code Ann. § 56-3-627 (5% IMF, $500 cap, eff 2017-07-01) + S.C. Code Ann. § 37-2-307 (closing fee, $225 review threshold) + SC DOR Chapter 10 Maximum Tax Items | by: orchestrator-S3

---

### SD, South Dakota

- **Sales tax**: 4% motor vehicle **excise tax** in lieu of sales/use tax; **no local stacking** on vehicles. Calculated on purchase price minus verified trade-in (rebates do NOT reduce base).
- **Doc fee cap**: **No statutory cap**, typical doc fee ~$115. Note: the doc fee IS part of the 4% excise-taxable purchase price in SD (along with rebates, extended warranties, GAP).
- **Title fee**: $10. **Registration**: weight-based, ~$36-$144+/yr by shipping weight; vehicles 10+ years old get a 30% reduction. Counties may add a wheel tax up to $5/wheel ($60 max).
- **Trade-in tax credit**: **YES**, trade-in deducted from purchase price if verified by VIN on contract and titled to the applicant.
- **Has**: EV surcharge $50/yr (mandatory state fee). 45-day titling window; penalties after.
- **Does NOT have**: statutory doc fee cap; traditional sales tax on motor vehicles; local sales tax stacking on vehicles; NY MCTD fee; GA TAVT.

#### SD Worked OTD Example (Sioux Falls, no trade)

Sales $30,000, doc $115, SD 4% excise (doc IS in base):

```
Taxable = $30,000 + $115 = $30,115
Excise  = $30,115 x 0.04 = $1,204.60
Title   = $10
Reg     = ~$60 (weight-based passenger)
OTD     ~ $31,389.60
```

#### SD Worked OTD Example (Sioux Falls, $10,000 trade)

Sales $30,000, trade $10,000, doc $115, SD 4% excise:

```
Net sale = $30,000 - $10,000 = $20,000
Taxable  = $20,000 + $115 = $20,115
Excise   = $20,115 x 0.04 = $804.60
Title    = $10
Reg      = ~$60
Cash OTD ~ $20,989.60; tax savings on trade = $400
```

verified: 2026-06-22 | source: SD DOR Motor Vehicle - Title, Fees & Registration (dor.sd.gov); SD DOR Motor Vehicle page; SalesTaxHandbook SD | by: orchestrator/S6

---

### TN, Tennessee

- **Sales tax**: 7% flat state rate on the full taxable amount. Local option tax (2.00-2.75% by county) applies only to the first $1,600 (max ~$36), then a state-level 2.75% "single-article" tax applies to the slice from $1,600 to $3,200 (max ~$44). The local portion is capped, TN does NOT stack uncapped local rates on the whole price. Trade-in reduces the base; rebates do NOT.
- **Doc fee cap**: **No statutory dollar cap.** T.C.A. § 55-17-114 authorizes the fee but voids it if the dealer represents it as a government charge. Typical TN doc fee ~$495-499. No ceiling, negotiate at OTD.
- **Title fee**: ~$11 ($5.50 + $8.50; +$11 lien notation if financed). **Registration**: ~$24-26.50 state base, plus a local wheel tax that varies $0 to $75+ by county (annual renewal can run $29 to $100+).
- **Trade-in tax credit**: **YES**, taxable base is price minus trade-in value.
- **Has**: 7% state + capped local + single-article tax; $11 title; state reg + county wheel tax; **$200/year EV registration surcharge** (all-electric, T.C.A. § 55-4-116, $200 for 2024-2026, rising to $274 in 2027); separate $100/year hybrid fee.
- **Does NOT have**: statutory doc fee cap; uncapped local sales tax (local is limited to the first $1,600); rebate deduction from the tax base.

#### TN Worked OTD Example (Knox County, 2.25% local, no trade)

Sales $30,000, doc $499, TN 7% + capped local + single-article:

```
Taxable          = $30,000 + $499 = $30,499
State tax        = $30,499 × 0.07 = $2,134.93
Local (first $1,600 × 2.25%)        = $36.00
Single-article ($1,600 × 2.75%)     = $44.00
Title            = $11
Reg              = ~$26.50 (+ county wheel tax, varies)
OTD              = $30,499 + $2,134.93 + $36 + $44 + $11 + $26.50 = $32,751.43
```

#### TN Worked OTD Example (Knox County, 2.25% local, $5,000 trade)

Sales $30,000, doc $499, trade $5,000, TN 7% + capped local + single-article:

```
Net sale         = $30,000 - $5,000 = $25,000
Taxable          = $25,000 + $499 = $25,499
State tax        = $25,499 × 0.07 = $1,784.93
Local (first $1,600 × 2.25%)        = $36.00
Single-article ($1,600 × 2.75%)     = $44.00
Title            = $11
Reg              = ~$26.50
Cash OTD         = $25,499 + $1,784.93 + $36 + $44 + $11 + $26.50 = $27,401.43
Tax savings on trade = $5,000 × 0.07 = $350 (state portion; local/single-article already maxed)
```

verified: 2026-06-22 | source: TN Dept of Revenue VTR-34 (7% state, trade-in deduction, local $1,600 cap, single-article) + VR-5 / T.C.A. § 55-4-116 ($200 EV fee 2024-2026) + SalesTaxHandbook TN | by: orchestrator-S2

---

### TX, Texas

- **Sales tax**: 6.25% state motor-vehicle sales/use tax; **+ up to 1.75% local** (combined max 8.00%). For dealer sales the base is sale price minus trade-in allowance. For **private-party** used buys, tax is the greater of actual price or 80% of the vehicle's **Standard Presumptive Value (SPV)** set by TxDMV, a minimum-value floor unique among the big states; a certified appraisal within 20 working days can override it.
- **Doc fee cap**: **$225 presumed-reasonable amount, NOT a hard statutory cap** (Tex. Finance Code § 348.006(f); OCCC rule 7 TAC § 84.205). Effective **2024-07-11** the OCCC "safe harbor" rose from $150 (set 2016) to $225; a dealer may charge above $225 only after filing a cost justification with the OCCC. The widely-cited "$150 Texas doc limit" is **outdated**, do not use it. Treat doc above $225 as a flag (legal but requires OCCC justification).
- **Title fee**: $33 (county application fee; $28 in some counties). **Registration**: ~$51/yr ($50.75 base passenger + small county add-ons + $7.50/$16.75 Inspection Program Replacement Fee since safety inspections were dropped 2025-01-01).
- **Trade-in tax credit**: **YES**, taxable base is sale price minus the trade-in vehicle's value (vehicle-for-vehicle only; boats/livestock don't count), but **only on licensed-dealer purchases**. No trade credit on private-party deals, and trade-downs incur no tax.
- **Has**: $200/yr EV registration surcharge ($400 at new-vehicle initial 2-year registration) on full-electric vehicles ≤10,000 lb under SB 505, effective 2023-09-01 (hybrids exempt); SPV minimum-value tax on private-party used buys; Inspection Program Replacement Fee; metal plate at point of sale (HB 718, 2025-07-01).
- **Does NOT have**: state income tax; local-rate stacking above 1.75%; CA-style district tax; CA's no-trade-credit rule; GA TAVT; NC highway-use tax; an MD-style high doc cap; trade-in credit on private-party sales.

#### TX Worked OTD Example (Harris County, 8.25% combined, no trade)

Sales $30,000, doc $225, TX 6.25% state + 2.00% local = 8.25% (Harris combined typ. ~8.25%):

```
Taxable = $30,000   # TX motor-vehicle tax is on sale price; doc fee is not part of the 6.25% base
Tax     = $30,000 × 0.0825 = $2,475.00
Title   = $33
Reg     = $51 (annualized)
Doc     = $225 (capped/presumed-reasonable)
OTD     = $30,000 + $225 + $2,475.00 + $33 + $51 = $32,784.00
```

#### TX Worked OTD Example (Harris County, 8.25%, $7,000 dealer trade)

Sales $30,000, doc $225, trade $7,000, TX 8.25%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $23,000   # TX credits the trade-in at a licensed dealer
Tax        = $23,000 × 0.0825 = $1,897.50
Title      = $33
Reg        = $51
Doc        = $225
Cash OTD   = $23,000 + $225 + $1,897.50 + $33 + $51 = $25,206.50
Tax savings on trade = $7,000 × 0.0825 = $577.50  (vs $0 in California)
```

verified: 2026-06-22 | source: Texas Comptroller Motor Vehicle Sales & Use Tax (6.25% + trade credit + SPV) + OCCC final doc-fee rule adoption 7 TAC § 84.205 / Fin. Code § 348.006 ($225 eff. 2024-07-11) + TxDMV SB 505 EV fee release ($200) | by: orchestrator-S1

---

### UT, Utah

- **Sales tax**: 4.85% state sales tax; + 1-3% local (combined typically ~6.1-9.05%, e.g. Park City/Summit ~9.05%, Wayne County ~6.1%). Rate is the dealer location, or the registration locality for private/out-of-area.
- **Doc fee cap**: **No statutory cap**, the Utah DMV confirms no limit. Utah Admin Code R877-23V-14 imposes a *disclosure* requirement (posted sign with the fee amount) but no dollar ceiling. Dealer-set, typical $300-500. HB 194 (2023) bars dealers from adding mandatory fees beyond the negotiated price other than legally-required fees, the doc service fee, and certain heavy-truck manufacturer increases.
- **Title fee**: $6. **Registration**: ~$44/yr (age/weight-based) + a $10 county highway/corridor fee in some counties.
- **Trade-in tax credit**: **YES**, the trade-in value is excluded from the taxable price, but only for a true vehicle-to-vehicle trade documented in the *same* transaction at the same dealer; the credit applies to sales tax only (not title/reg). Manufacturer rebates also reduce the taxable amount.
- **Has**: EV/alt-fuel annual registration surcharge ~$138.50 (BEV) / ~$56.50 (PHEV) / lower (HEV), inflation-adjusted, set as of 2025-04-01; drivers may instead opt into UDOT's Road Usage Charge (~$0.0111/mile, capped at the flat fee).
- **Does NOT have**: statutory doc fee cap; no trade-in credit denial.

#### UT Worked OTD Example (Salt Lake County ~7.75%, $35,000 new, $8,000 trade)

```
Net sale = $35,000 - $8,000 = $27,000
Taxable  = $27,000 + $400 doc = $27,400
Tax      = $27,400 x 0.0775 = $2,123.50
Title    = $6
Reg      = $44 (passenger, annualized)
OTD      = 27,400 + 2,123.50 + 6 + 44 = $29,573.50
Tax savings on trade = $8,000 x 0.0775 = $620.00
```

verified: 2026-06-22 | source: UT DMV dealer sales FAQ + Utah Admin Code R877-23V-14 (doc disclosure) + AFDC ELEC UT (EV fee) + SalesTaxHandbook UT vehicles | by: agent-S5

---

### WI, Wisconsin

- **Sales tax**: 5% state sales/use tax; **+0.5% county** in most counties (0% in Waukesha and Winnebago; Milwaukee County 0.9%, and the **City of Milwaukee** adds a further 2% from 2024-01-01, the only municipal vehicle sales tax in the state). Combined is 5.5% in the typical county, up to ~7.9% inside Milwaukee city. Manitowoc Co. added 0.5% (Jan 2025) and Racine Co. 0.5% (Apr 2025).
- **Doc fee cap**: **No statutory cap.** The "service/document/title-prep" fee is dealer-set and **taxable**; the Wisconsin average is only ~$190 and some dealers add an optional ~$99 service fee. Because there is no ceiling, treat an unusually high doc line as negotiable rather than statutorily-limited, Wisconsin sits among the low-doc-fee states despite having no cap.
- **Title fee**: **$214.50** ($207 base + $7.50 supplemental, Wis. Stat. § 342.14), increased from $164.50 effective **2025-10-01** under 2025 WI **Act 15** (the biennial budget), now the highest title fee in the US. Spouse/partner transfers are $0. **Registration**: $85/yr for a standard passenger auto; some counties/municipalities add a $15-$35 "wheel tax."
- **Trade-in tax credit**: **YES**, subtract the trade-in allowance from the sale price before applying the rate (Wis. DOR Pub. 202). Rebates/incentives do NOT reduce the base (you still pay tax on rebate amounts).
- **Has**: $0.5-0.9% county tax + Milwaukee city 2%; **$175/yr EV registration surcharge** and **$75/yr hybrid surcharge** (Wis. Stat. § 341.25(1)(L), added by 2017 Act 4) on top of the $85 base reg; optional local wheel tax $15-$35; taxable doc fee.
- **Does NOT have**: a statutory doc-fee cap; a city-level vehicle sales tax anywhere except Milwaukee; TAVT; highway-use tax; IMF; a Texas-style SPV minimum-value floor.

#### WI Worked OTD Example (Dane County, 5.5% combined, no trade)

Sales $30,000, doc $190, WI 5% state + 0.5% county = 5.5%:

```
Taxable = $30,000 + $190 = $30,190   # doc fee is taxable in WI
Tax     = $30,190 × 0.055 = $1,660.45
Title   = $214.50 (post-2025-10-01)
Reg     = $85 (annual; before any wheel tax)
OTD     = $30,000 + $190 + $1,660.45 + $214.50 + $85 = $32,149.95
```

#### WI Worked OTD Example (Dane County, 5.5%, $7,000 trade)

Sales $30,000, doc $190, trade $7,000, WI 5.5%:

```
Net sale   = $30,000 - $7,000 = $23,000
Taxable    = $23,000 + $190 = $23,190   # trade credited, doc still taxable
Tax        = $23,190 × 0.055 = $1,275.45
Title      = $214.50
Reg        = $85
Cash OTD   = $23,000 + $190 + $1,275.45 + $214.50 + $85 = $24,764.95
Tax savings on trade = $7,000 × 0.055 = $385.00
```

verified: 2026-06-22 | source: WI DOR Pub. 202 (5% + 0.5% county + trade credit) + Wis. Stat. § 342.14 / 2025 Act 15 (title $214.50, eff 2025-10-01) + Wis. Stat. § 341.25(1)(L) (EV $175 / hybrid $75) | by: orchestrator-S3

---

### WV, West Virginia

- **Sales tax**: 5% motor vehicle title privilege/sales tax on vehicles (WV general rate is 6%, but the vehicle title privilege tax rate is 5%); **no local stacking** on vehicles. Applied to net price after trade-in.
- **Doc fee cap**: **$575** statutory/regulatory cap, effective **2024-07-01** (raised from $499), set by the DMV Dealer Advisory Board under WV Code 17A-6A-8a; **CPI-indexed annually beginning 2025-07-01**. NOTE: the $199 figure carried in the seed is INCORRECT (that is closer to Missouri's $199.99 cap), corrected here.
- **Title fee**: $15. **Registration**: ~$51.50/yr passenger (annual).
- **Trade-in tax credit**: **YES**, privilege tax applies to price minus trade-in.
- **Has**: EV registration surcharge ~$200/yr (alternative-fuel annual fee).
- **Does NOT have**: local sales tax stacking on vehicles; NY MCTD fee; NJ supplemental titling fee; GA TAVT; NC highway use tax.

#### WV Worked OTD Example (Charleston, no trade)

Sales $30,000, doc $575 (at cap), WV 5% (doc not in tax base):

```
Taxable = $30,000
Tax     = $30,000 x 0.05 = $1,500
Title   = $15
Reg     = ~$51.50
Doc     = $575
OTD     ~ $32,141.50
```

#### WV Worked OTD Example (Charleston, $8,000 trade)

Sales $30,000, trade $8,000, doc $575, WV 5%:

```
Net sale = $30,000 - $8,000 = $22,000
Tax      = $22,000 x 0.05 = $1,100
Title    = $15
Reg      = ~$51.50
Doc      = $575
Cash OTD ~ $23,741.50; tax savings on trade = $400
```

verified: 2026-06-22 | source: WVADA / DMV Dealer Advisory Board (doc cap $575 eff. 2024-07-01, CPI-indexed); WV Code 17A-6A-8a (code.wvlegislature.gov); SalesTaxHandbook WV (5% vehicle tax) | by: orchestrator/S6

---

### WY, Wyoming

- **Sales tax**: 4% state + 0-2% county (typical combined 5-6%); rate is set by the buyer's **county of residence**, not the point of sale. The doc fee is itself taxable as part of the sales price. Private-party sales are taxed on Fair Market Value regardless of negotiated price.
- **Doc fee cap**: **No statutory cap.** Typical $100-$495. Because it is folded into the taxable base, a high doc fee costs extra tax too.
- **Title fee**: $15 (Wyo. Stat. §§ 31-2-101 et seq.; lien recording $20). **Registration**: state fee $30 for a passenger car, PLUS a county fee = factory-cost (original MSRP) x age-based depreciation % x 3% (e.g., a 6th-year $35k-MSRP car = $35,000 x 15% x 3% = $157.50). Out-of-state vehicles pay a $10 VIN inspection.
- **Trade-in tax credit**: **YES** on dealer sales, taxable base = purchase price minus gross trade-in allowance (and minus dealer-assigned rebates). Not available on private sales (taxed at FMV).
- **EV surcharge**: $200/yr (all registered EVs, with annual renewal).
- **Does NOT have**: doc-fee statutory cap; emissions/safety inspection; trade-credit on private FMV-taxed sales.

#### WY Worked OTD Example (Laramie County 6%, no trade)

Sales $30,000, doc $400 (taxable), WY 6%:

```
Taxable = $30,000 + $400 = $30,400
Tax     = $30,400 x 0.06 = $1,824
Title   = $15
Reg     = $30 state + ~$157.50 county fee (factory MSRP x depr x 3%) = ~$187.50
OTD     = $30,000 + $400 + $1,824 + $15 + $187.50 = $32,426.50
```

#### WY Worked OTD Example (Laramie County 6%, $8,000 trade, dealer sale)

```
Net sale = $30,000 - $8,000 = $22,000
Taxable  = $22,000 + $400 doc = $22,400
Tax      = $22,400 x 0.06 = $1,344
Title    = $15
Reg      = ~$187.50
Cash OTD = $22,000 + $400 + $1,344 + $15 + $187.50 = $23,946.50
Tax savings on trade = $8,000 x 0.06 = $480
```

verified: 2026-06-22 | source: SalesTaxHandbook (WY vehicles) + Laramie County Treasurer Vehicle Sales & Use Tax + Wyo. Stat. Title 31/39 | by: orchestrator-S7

## State-Specific Quirks

- **MD doc fee cap $800** (effective July 1 2024; cap history $200 → $300 [2014] → $500 [2020] → $800 [2024] per MD Transportation § 15-311.1, now the HIGHEST statutory doc cap in the DC corridor, above VA's $599; the old "MD = low-doc sweet spot" framing is obsolete)
- **FL has no state income tax + no doc fee cap**, FL is a destination state for retirees/out-of-state buyers but FL dealers charge among the highest doc fees in the US ($999-1,499 typical, no statutory ceiling)
- **FL surtax ceiling on first $5,000**, county discretionary surtax (0.5-2%) only applies to first $5k of price, so total surtax is capped at ~$100 per vehicle regardless of sale price
- **FL first-time registration fee $225**, out-of-state buyers transferring to FL hit this one-time fee at first FL title issuance
- **OH doc fee cap $250**, among the strongest US protections (only CA $85, NC $129, NY $175, WA $200, TX $225 safe-harbor, MI $230 lower; ties RI $250 and OR $250)
- **Verified low-doc-cap ranking (states WITH a statutory cap, lowest first)**: CA $85 (lowest binding cap) < NC $129 < NY $175 < WA $200 < TX $225 (OCCC safe-harbor, not a hard cap) < MI $230 < OH $250 = RI $250 = OR $250 (integrator) < IN $251.05 < IL $347.26 < MN $350 < LA $436 < WV $575 < VA $599 < MO $604.47 < NJ $799 < MD $800 (highest). NH $27 is a state-title-fee cap only, dealer admin fees are uncapped, so NH is NOT a low-doc state in practice. All other states have NO statutory cap. **MD $800 is the single highest statutory doc cap in the country and is decisively NOT low-doc.**
- **NC uses Highway Use Tax 3% (NOT sales tax)**, any "sales tax" line on an NC quote is a flat error; NC doc fee cap $129 is second-lowest in US (after CA $85)
- **GA uses TAVT 6.6% one-time at registration**, replaced annual ad valorem in 2013 for vehicles purchased after March 1, 2013; TAVT base is GA DOR FMV (Motor Vehicle Assessment Manual) OR sale price, whichever applies, agents must verify FMV at Phase 2 since FMV can be higher OR lower than sale price
- **MI trade-in tax credit capped at $9,000 (2025)**, rises $1k/year to uncapped by 2029 per Public Act 1 of 2018 phase-in
- **VA does NOT grant trade-in tax credit**, unique among DC-corridor states (DC=yes, MD=yes, VA=no); a $10k trade in VA saves $0 in tax vs $600 in MD same trade
- **DC excise tax by vehicle weight class**, not traditional sales tax; 4 weight tiers each with 2 brackets (first $40k MSRP vs above $40k); EV exemption on first $40k
- **WA combined tax can exceed 10.5% in Seattle**, state 6.5% + local up to 3.5% + MVET 0.3% = up to 10.55% Seattle; drives WA→OR residency arbitrage attempts (audited by WA DOL)
- **IL doc fee $347.26** is statutorily capped; CPI-indexed annually. It is the highest cap among the *low-tier* (sub-$400) capped states, but NOT the highest cap in the US, MD $800, NJ $799, MO $604.47, VA $599, WV $575, LA $436, and MN $350 all exceed it. (The old "highest cap in US" claim was based on an outdated read and is wrong.)
- **IL trade-in tax credit capped at first $10,000** (Rivian-vs-Ford SB-690 outcome, in effect since 2020). Above $10k of trade allowance gets no tax credit.
- **IL combined local-rate stacking ranges from 6.25% (rural counties) to 10.25% (Chicago Cook City).** ZIP-by-ZIP variance is the largest in the US after CA.
- **NC uses "Highway Use Tax" 3%** instead of sales tax, much lower than typical
- **OK uses "excise tax" 3.25%** on vehicles, separate from local sales tax
- **VA minimum SUT $75**, small purchases have a floor
- **CT $50k threshold**, luxury cars above $50,000 face 7.75% instead of 6.35%

## When to Verify

Always verify state-specific fees with the dealer in writing before signing. Get an itemized OTD breakdown that matches the formula above. Reject any line items that do not fit the standard structure.
