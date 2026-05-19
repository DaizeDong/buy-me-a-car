# PDF Review Checklist

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

When dealers send PDFs, open them with the Read tool and extract specific signals. Three common PDF types:

## CARFAX Vehicle History Report

Located in dealer email as a PDF attachment, usually titled with the VIN.

### Strong Positive Signals

- "CARFAX 1-Owner Vehicle" badge
- "No Accidents Reported"
- "No Total Loss"
- "No Structural Damage"
- "No Airbag Deployment"
- "No Odometer Rollback"
- "Personal Vehicle" (not fleet/rental)
- "Last Owned in {State}" matching buyer's state (no out-of-state title hassle)
- "Reliability Forecast: Good" or "Great"
- Annual mileage under 12,000-15,000 mi/year average

### Concerning Signals

- Multiple owners (especially within first 3 years)
- "Accident Reported" (any severity)
- Salvage / Junk / Rebuilt / Lemon title brand
- Flood / Hail / Fire damage history
- "Not Actual Mileage" or "Exceeds Mechanical Limits"
- "Total Loss" reported
- Open recalls listed under "Manufacturer Recall"
- Rental fleet history (heavy use, multiple unknown drivers)
- Out-of-state purchase requiring cross-state title transfer (NJ has specific MVC requirements)

### Service Record Gaps

Even on a 1-owner / no-accident car, CARFAX often shows only registration renewals and emissions checks, not actual service work. This is a gap, not a problem — many owners use independent shops that don't report to CARFAX.

Ask the dealer for dealership-internal service records as a follow-up. See `pdf_review_checklist.md` section "Service Records PDF" below.

### Reading Strategy

Page 1 has the summary badges (1-Owner / Accidents / Title Brands / Mileage check). If all green, proceed to Page 2 for detailed history. Look for:

- First title issue date and state
- Loan/lien reported (needs release confirmation before purchase)
- Inspection records (NJ MVI every 2 years for older cars)
- Registration gap years (could indicate storage / non-use period)
- Last reported odometer reading (should match dealer's listed mileage)

## Dealer Service Records PDF

Some dealers (especially when they sold the car originally) have full internal service history. These are gold — they reveal what was actually maintained.

### Check For

- **Oil change frequency** — every 5-7k miles synthetic is good
- **CVT fluid change** — Subaru spec 60k mi for severe service, 100k for normal. Critical for XT turbo variants
- **Spark plugs** — 60k mi typical interval (60k-100k depending on plug type)
- **Coolant flush** — 100k mi typical
- **Brake fluid flush** — every 2-3 years
- **Brake pads/rotors** — wear-based, look for replacement records
- **Tires** — replacement records, tire brand consistency
- **Battery** — replacement records, especially for cars 4+ years old in cold climates
- **Transmission diff fluid** — 60k mi typical for AWD
- **Spark plugs** — 60k-100k mi typical

### Red Flag Patterns

- Battery flagged 2-3 times but never replaced (still original old battery — high failure risk)
- CVT fluid never serviced past 60k mi (expensive failure if not maintained)
- Oil changes inconsistent (long gaps suggest skipped maintenance)
- Recurring same issue (e.g., "customer states X" multiple times)
- "Customer concern" notes without resolution

### Service Code Decoding (Subaru example)

- PDI = Pre-Delivery Inspection (first sale prep)
- SAS = Subaru Added Security (maintenance plan service)
- INTS = Intermediate service (oil + filter + inspection)
- LOFS = Lube Oil and Filter Service
- CDR = Charging system / battery test
- COR = Check for Open Recalls
- MB4T = Mount and Balance 4 Tires

## OTD Proposal PDF

Dealers send a 1-page "proposal" document with the final OTD numbers. Format varies but usually includes:

### What to Verify

- **VIN match** with listed car
- **Stock #** for internal dealer tracking
- **Mileage** matches what was discussed
- **Sales price** vs the asking price (any reduction?)
- **NJ tax** computed correctly (6.625% on sales + doc fee)
- **Doc fee** within reasonable range ($499-799 NJ)
- **Title fee** ~$60-100 NJ
- **Registration fee** ~$46-84 NJ (varies by car weight)
- **No surprise add-ons** (paint, fabric, nitrogen, etching)
- **Balance Due** matches the breakdown sum

### Common Tricks

- Doc fee at NJ max ($799) without negotiation room
- "Market Value Selling Price" label that does not match actual market
- "Internet Price" footnote requiring lead form unlock (you already did this)
- Add-ons buried at subtotal level

### Math Check

If the dealer's "total" doesn't match: sales + doc + tax + title + reg + add-ons, something is wrong. Ask for itemized clarification.

## CARFAX from Dealer vs Self-Pulled

Some dealers attach the CARFAX PDF, others provide a CARFAX-hosted URL link. Both are equally valid. The PDF is preferred for archival in `dealer_pdfs/` folder.

If the dealer provides only a link, save it; also recommend the user click and save-as-PDF for their records.

## Cross-Reference With Tracker

After PDF analysis, update `dealer_outreach_tracker.md` with:

- 1-owner / multi-owner finding
- Accident history (or absence)
- Specific service records gaps (e.g., "no CVT fluid in records")
- Open recalls (specific to this VIN)
- Any inherited maintenance costs the buyer will face post-sale
- Notable cosmetic notes (e.g., "louie rear bumper" = small paint touch-up done by dealer's in-house painter)

This converts the buyer's hidden risk into known cost. A vehicle with a $500 inherited CVT service due is effectively $500 more expensive than its listed OTD.

## OTD Proposal Add-On Anti-Pattern Detection

Dealer proposal PDFs frequently bury 3-7 F&I (Finance & Insurance) add-on lines in fine print, footnotes, or "Protection Package" bundles that obscure individual costs. Total dollar value of buried add-ons is typically **$1,500-$4,000** per deal — large enough to overshoot the buyer's walk-away ceiling silently. **Every proposal PDF MUST be scanned for these line names verbatim before any OTD is accepted.**

### Add-On Kill List — Scan Routine

For every proposal PDF, search (Ctrl-F equivalent during Read) for each of the following line names. Flag every hit, regardless of dollar amount. The dealer cannot add ANY of these without explicit buyer consent.

| Add-On Line Name (Variants) | Typical Dealer Charge | Cost To Dealer / Fair-Market Alternative | Default Action |
|---|---|---|---|
| **GAP Insurance** (Guaranteed Asset Protection) | $695-$995 | $200-$500 from buyer's auto-insurance carrier or credit union | Decline if cash buyer; if financing, source from CU/insurance instead |
| **VSC / Vehicle Service Contract / Extended Warranty** (also: Platinum Coverage, Premium Care, Honda Care, Toyota Platinum VSA, Subaru Added Security) | $1,495-$3,500 | $800-$2,500 from manufacturer direct or third-party (Endurance, CARCHEX) | Defer to post-other-terms; negotiate separately; verify hybrid/EV component coverage explicitly per `references/toyota_cpo_program.md` / `ev_buyer_playbook.md` |
| **Tire & Wheel Protection** (also: Road Hazard, T&W Coverage) | $495-$895 | $150-$300 from tire-shop direct; many credit cards include road hazard | Decline |
| **Paint Protection / Paint Sealant** (also: Diamond Coat, Ceramic Coating, Permaplate) | $399-$899 | $0 — modern clear-coat paint does not need it; cosmetic-only | **Refuse outright** (Phase 6 add-on refusal list) |
| **Fabric / Interior Protection** (also: Scotchgard, Interior Sealant, Stain Guard) | $299-$599 | $20-$50 retail can of Scotchgard | **Refuse outright** |
| **Key Replacement** (also: Key Fob Insurance, Smart Key Coverage) | $299-$499 | $0 — most modern fobs covered under 3yr/36k B2B factory warranty | Decline |
| **Theft / VIN Etching** (also: Window Etch, Anti-Theft Identification, GlassEtch) | $199-$499 | $0-$25 DIY kit; insurance discount $20-$50/yr only if itemized | **Refuse outright** |
| **Nitrogen Tire Fill** (also: N2 Fill, Premium Air, Green Air) | $49-$199 | $5-$15 actual cost; air has been free since 1903 | **Refuse outright** |
| **LoJack / Clifford / Compustar Alarm** | $599-$1,295 | $200-$500 retail aftermarket; insurance discount $5-$20/mo | Decline unless buyer wants stolen-vehicle recovery |
| **Mop-and-Glo / Undercoating / Rust Proofing** | $399-$899 | $0 — modern OEM undercoating is sufficient on every 2010+ vehicle | **Refuse outright** |
| **Dealer Prep / Vehicle Prep Fee** (also: Make-Ready, Pre-Delivery Service) | $299-$799 | $0 — already covered in MSRP / Internet Price | **Refuse outright** (this is fee theater, not a service) |
| **EV-Specific: EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup / High-Voltage Inspection** | $495-$1,995 | $0 — covered in OEM PDI; double-billing | **Refuse outright** per gotcha D9 (ADM-equivalent on EVs); see `ev_buyer_playbook.md` § 8 |

### "Protection Package" Bundle Detection

Dealers increasingly bundle 4-6 of the above into a single "Total Protection Package" or "Premium Protection Plan" line item for $1,995-$3,995. Bundling obscures individual line costs and removes per-line negotiation.

**Action when bundle is detected**: Demand itemization in writing. "Please re-issue the OTD with each Protection Package component on its own line — GAP $X, VSC $Y, Tire & Wheel $Z, etc. I cannot accept an aggregated line." Once itemized, apply the kill list above per line.

### Math-Check Routine

After scanning for add-on lines, verify the proposal's bottom-line OTD against the canonical formula (from `references/negotiation_playbook.md` § OTD Math):

```
OTD = (Sale + Doc) * (1 + StateRate) + Title + Reg + Other
```

Compare to the dealer's "Balance Due" / "Total Out The Door". Any positive delta is buried fees or arithmetic that needs to be challenged. Typical pattern:

| Buyer-Verbal-Agreement OTD | Proposal Bottom-Line OTD | Delta | Cause (90%+ of cases) |
|---|---|---|---|
| $31,500 | $35,328 | +$3,828 | Buried add-ons (the kill list above) |
| $28,000 | $28,650 | +$650 | Doc fee uncapped (PA / TX) or fee-template leak (gotcha D8) |
| $42,000 | $43,495 | +$1,495 | ADM line item (gotcha D9) on a new car |

### Paste-Ready Buyer Challenge Language

When ANY kill-list add-on is detected, the first counter must demand removal of every flagged line as a precondition. Do NOT negotiate price-down on add-ons; demand removal. Paste-ready:

> *"The proposal includes [list each flagged add-on line + amount]. Per my Phase 1 OTD ceiling these were not part of our agreement. Please re-issue the OTD with all of these removed. If they remain, OTD walks above my ceiling and this unit cannot win."*

If buyer explicitly wants VSC or GAP (financing buyer who didn't pre-source from CU), defer those two lines to a separate post-other-terms negotiation per `payment_methods.md` § Captive-vs-CU. The remaining lines (paint, fabric, nitrogen, etch, key, undercoating, prep, EV-prep) are non-negotiable refusals.

### Cross-References

- Gotcha D7 (`SKILL.md`): dealer-attached `proposal.pdf` hides actual OTD numbers — open the PDF or demand inline paste
- Gotcha D9 (`SKILL.md`): ADM kill list — same pattern as add-on kill list but for new-car sale-price-side markups; both routines apply on new-car proposals (one scan upstream of MSRP for ADM, one scan downstream of subtotal for F&I add-ons)
- `references/payment_methods.md` § Captive-vs-CU rebate playbook — GAP and VSC sourcing alternatives
- `references/ev_buyer_playbook.md` § 8 — EV-specific dealer tactics including the EV add-on variant of this kill list
- `references/negotiation_playbook.md` § OTD Math — state-parameterized formula for the math check above

## CARFAX Accident Detail Extraction Template

A single "Accident Reported" badge collapses 5-7 load-bearing sub-fields into one bullet. Buyer downstream decisions (renegotiate $1k-$3k / request body-shop docs / walk) depend on the sub-field detail. **Every CARFAX with an accident flag MUST be expanded into the structured template below before Phase 6 counter is sent.**

### 7-Field Extraction Template

| Field | Source In PDF | Typical Values | Buyer-Side Impact |
|---|---|---|---|
| **Accident Date** | Damage / Accident History section, dated entry | YYYY-MM-DD | Age of damage: <1 yr = fresh, repair quality unknown; 2-5 yr = settled, inspect; >5 yr = depreciated already |
| **Severity** | Same entry, narrative line ("Minor damage", "Moderate damage", "Severe damage", "Damage reported") | Minor / Moderate / Severe / Unspecified | Minor: -$500-$1,500 negotiation; Moderate: -$1,500-$3,500 + PPI scope expansion; Severe / unspecified: walk-strong-consider |
| **Impact Zones** | Same entry, sub-line ("Front", "Rear", "Left Side", "Right Side", "Left Front Corner", etc.) | 1-4 zones | Front-only = bumper/cooling/headlight; rear-only = bumper/trunk/exhaust; side = door + frame possible; corner = suspension + alignment risk; multi-zone = total-loss territory |
| **Repair Facility** | Service History section, post-accident date | Original OEM dealer body shop / Chain (Maaco, Caliber, Gerber) / Independent / Unknown | OEM dealer body shop: best parts + ADAS recal; Chain: highest miss rate for ADAS recal (Honda Sensing / EyeSight / Toyota Safety Sense / SmartSense / SuperCruise); Independent: variable; Unknown = ask dealer for body-shop invoice |
| **Photos Available** | CARFAX Damage section sometimes embeds 1-3 image thumbnails | Yes (with thumbnails) / No | Photos give visual severity check; no-photos = ask dealer for body-shop photos |
| **Structural Damage Flag** | Title Brands + Damage Summary | Yes / No / "No structural damage reported" | Yes = walk; No = inspect anyway (CARFAX missed reports ~15-25% of time per industry studies) |
| **Airbag Deployment Flag** | Damage Summary | Yes / No / "No airbags deployed" | Yes = moderate-to-severe impact + airbag replacement done? + sensors recalibrated?; No = lower severity ceiling |
| **Post-Accident Inspection Done?** | Cross-reference Service History entries dated within 60 days post-accident | Yes (alignment + body inspection + ADAS recal) / Partial / No / Unknown | No / Partial = ask dealer for alignment spec sheet + ADAS recal documentation; if not available, $200-$600 inherited cost |

### ADAS Recalibration By Brand — Cross-Reference Table

If accident involved front impact zone AND vehicle is equipped with forward-facing camera / radar (most 2018+ vehicles), ADAS calibration is required after windshield / bumper / camera-housing repair. Chain body shops miss this ~40-60% of the time. Recalibration not performed = $200-$600 inherited cost AND functional safety system degradation.

| Brand | ADAS Suite Name | Calibration Required After | Typical Cost To Recalibrate |
|---|---|---|---|
| Subaru | EyeSight | Windshield, front bumper, OEM camera replacement | $250-$500 at Subaru dealer |
| Honda / Acura | Honda Sensing / AcuraWatch | Windshield, front bumper, grille, camera | $300-$600 at Honda dealer |
| Toyota / Lexus | Toyota Safety Sense (TSS 2.0 / 2.5+) / Lexus Safety System | Windshield, front bumper, grille, mm-wave radar | $400-$800 at Toyota dealer |
| Hyundai / Kia / Genesis | Hyundai SmartSense / Kia Drive Wise / Genesis Active Safety | Windshield, front bumper, camera, sometimes side radar | $300-$600 at Hyundai/Kia dealer |
| Ford / Lincoln | Co-Pilot360 | Windshield, front bumper, camera, ACC radar | $350-$700 at Ford dealer |
| GM (Chevy / GMC / Buick / Cadillac) | Driver Assistance (varies); SuperCruise on premium | Windshield, front bumper, camera, lidar (SuperCruise) | $400-$1,500 at GM dealer (SuperCruise highest) |
| Mazda | i-Activsense | Windshield, front bumper, camera | $300-$500 at Mazda dealer |
| Nissan / Infiniti | ProPILOT Assist / Safety Shield 360 | Windshield, front bumper, camera, radar | $350-$650 at Nissan/Infiniti dealer |
| Tesla | Autopilot / Full Self-Driving | Front bumper, camera array, all 8 cameras must be in spec | $500-$1,200 at Tesla service center (no third-party option) |
| VW / Audi | Travel Assist / Audi pre sense | Windshield, front bumper, camera, radar | $400-$800 at VW/Audi dealer |

### Paste-Ready Buyer-Side Ask (Post-Extraction)

After populating the 7-field template, send to dealer:

> *"CARFAX shows [date] accident with [severity] damage to [impact zones], repaired at [facility]. Before I move forward I need: (1) the body-shop invoice / repair order, (2) confirmation of [BRAND ADAS NAME] recalibration if camera/radar systems were touched, (3) post-repair alignment spec sheet, (4) any photos the body shop has on file. If recalibration was not performed, I'm requesting it be completed at dealer cost before delivery OR a $[recal cost] price reduction."*

### Cross-References

- Gotcha V1 (`SKILL.md`): CARFAX 1-owner is necessary but not sufficient — service records reveal maintenance
- Gotcha V2 (`SKILL.md`): require dealer-provided full CARFAX PDF or live URL — verbal "clean" has real failure rate; <Dealer C> incident hid an earlier date minor damage event with front + left + right impact zones
- `references/ppi_booking.md` — mobile PPI scope expansion when severity is Moderate or higher
- `references/negotiation_playbook.md` — accident-finding negotiation lever sizing ($500-$3,500 per the severity table above)

## Service Record Gap Detection — Per-Brand Expected Service Table

Skill compares service record PDFs against expected services per brand at 30k / 60k / 90k / 120k mile bands. Missing services = inherited cost the buyer pays after close. **Quantify each gap as a dollar figure and aggregate as total inherited maintenance cost for use as Phase 6 negotiation leverage.**

### Expected Service Schedule By Brand And Mileage

Severe-service schedules listed (normal-service intervals extend by ~30-50%). For tri-state buyers (NJ/NY/CT/PA), severe is the realistic default due to short-trip + cold-weather usage.

#### Subaru (Forester, Outback, Crosstrek, Ascent, Impreza, Legacy)

| Mileage | Required Services | Typical Cost (if missed) |
|---|---|---|
| 30k | Oil + filter; tire rotation; brake fluid flush; cabin air filter; engine air filter; multi-point inspection | $200-$400 |
| 60k | All 30k items; **CVT fluid drain + fill** (critical, esp. XT turbo); spark plugs (some models); coolant inspection; differential fluid (AWD models) | $400-$700 |
| 90k | All 30k items; brake fluid flush; differential fluid; transmission inspection | $250-$450 |
| 120k | All 30k items; **CVT fluid drain + fill (2nd time)**; spark plugs (if not done at 60k); coolant flush; serpentine belt inspection; PCV valve | $500-$900 |

**Subaru-specific red flags**: CVT fluid never serviced past 60k = $300-$400 inherited + $4,000-$6,000 catastrophic-failure risk if missed long-term; head-gasket history on 2.5L NA pre-2013 (now 13+ yr old, less common); turbo seal leaks on FA20 XT engines.

#### Toyota (RAV4, Camry, Corolla, Highlander, 4Runner, Tacoma, Tundra, Sienna, Prius)

| Mileage | Required Services | Typical Cost (if missed) |
|---|---|---|
| 30k | Oil + filter; tire rotation; engine air filter; cabin air filter; brake inspection | $150-$300 |
| 60k | All 30k items; brake fluid flush; coolant inspection; transmission fluid inspection (non-CVT models) | $300-$500 |
| 90k | All 30k items; spark plugs (Iridium 120k spec but inspect at 90k); coolant flush; **Hybrid-only: hybrid battery inspection** | $250-$500 ICE / $300-$600 Hybrid |
| 120k | All 30k items; spark plugs (replace); coolant flush if not at 90k; transmission fluid drain + fill (non-CVT); timing belt if applicable (most modern Toyotas have timing chain — verify) | $500-$900 |

**Toyota-specific red flags**: Camry / Corolla / RAV4 ICE models have very long maintenance intervals (Iridium plugs 120k, conventional AT not CVT) so gaps are less expensive than Subaru / Honda; Hybrid models add inverter coolant flush at 100k ($150-$300) — frequently missed; Tundra / 4Runner V8 (5.7L) timing belt is replaced by timing chain in 2010+ models; pre-2010 5.7L = 90-100k timing belt $600-$1,000 inherited.

#### Honda / Acura (Civic, Accord, CR-V, Pilot, Odyssey, Passport, Ridgeline, TLX, MDX, RDX)

| Mileage | Required Services | Typical Cost (if missed) |
|---|---|---|
| 30k | Oil + filter; tire rotation; engine + cabin air filter; brake inspection | $150-$300 |
| 60k | All 30k items; brake fluid flush; transmission fluid drain + fill (Honda CVT spec — different from drain-only on AT); rear differential fluid (AWD) | $250-$450 |
| 90k | All 30k items; coolant inspection; spark plugs (NGK Iridium 100k typical) | $200-$400 |
| 120k | All 30k items; spark plugs (replace if not at 90k); **2nd CVT fluid drain + fill (CVT models)**; coolant flush; valve adjustment (Honda Civic 1.5L turbo + select Accord 2.0L turbo) | $400-$800 (+$200-$400 valve adjust on turbo models) |

**Honda-specific red flags**: Honda CVT requires drain + fill (NOT flush — flushing damages CVT — verify dealer did drain + fill); 1.5L turbo (Civic / CR-V / Accord) has known oil-dilution issue 2017-2019 (check oil level + smell for gas contamination); valve adjustment on 1.5T / 2.0T is real maintenance every 100k+ that many owners + dealers skip — $200-$400 inherited.

#### Ford / Lincoln (F-150, Explorer, Escape, Edge, Bronco Sport, Mustang, Ranger)

| Mileage | Required Services | Typical Cost (if missed) |
|---|---|---|
| 30k | Oil + filter; tire rotation; engine + cabin air filter | $150-$300 |
| 60k | All 30k items; brake fluid flush; transfer case fluid (4x4); rear differential fluid | $300-$500 |
| 90k | All 30k items; **spark plugs (EcoBoost 60-100k spec — check carbon buildup)**; coolant inspection; transmission fluid drain (10R80 trans on F-150) | $400-$700 |
| 120k | All 30k items; spark plugs (replace if not at 90k); coolant flush; **2nd transmission fluid service (10R80)**; **turbo seal inspection (EcoBoost)** | $500-$1,200 (+$1,500-$3,000 if turbo seal repair needed) |

**Ford-specific red flags**: EcoBoost engines (1.5L / 2.0L / 2.3L / 2.7L / 3.5L) have turbo seal failure 100-150k = $1,500-$3,000 repair; intercooler condensation buildup causes misfires (track-mode drain procedure); 5.0L V8 in F-150 / Mustang has known exhaust manifold cracks 80-120k = $500-$1,500 ($800-$1,500 on F-150 SCrew); 10R80 trans (2017+) has known shudder issues — flush + new fluid often helps; spark plug intervals are SHORTER on EcoBoost (60-80k) vs naturally aspirated (100k+).

#### Mazda (CX-5, CX-30, CX-50, CX-9, Mazda3, Mazda6, MX-5)

| Mileage | Required Services | Typical Cost (if missed) |
|---|---|---|
| 30k | Oil + filter (Mazda spec is shorter — 5k mi for SkyActiv-G); tire rotation; engine + cabin air filter | $150-$300 |
| 60k | All 30k items; brake fluid flush; rear differential fluid (AWD); transfer case fluid (AWD) | $300-$500 |
| 90k | All 30k items; coolant inspection; spark plugs (NGK Platinum 80-100k spec) | $250-$450 |
| 120k | All 30k items; spark plugs (replace); coolant flush; transmission fluid drain + fill (Mazda 6-speed AT — verify dealer used SkyActiv ATF spec) | $400-$700 |

**Mazda-specific red flags**: SkyActiv-G engines have known carbon buildup on intake valves (direct injection) — walnut blast at 90-120k = $400-$800 if owner / dealer never addressed; some 2014-2017 CX-5 have water-pump weep at 80-100k = $400-$700.

### Gap Detection Output Format

For every service record PDF, produce this structured output for the buyer:

```
Vehicle: [Year Make Model], [Current Mileage] mi
Service records reviewed: [date range, source dealer/independent]

Expected services at [current mileage band]:
- [Service 1]: [YES present / NO missing] — last performed at [X] mi
- [Service 2]: [YES / NO]
- [Service 3]: [YES / NO]
...

MISSING services (inherited cost):
- [Service A] not performed — estimated cost $[X-Y]
- [Service B] not performed — estimated cost $[X-Y]

TOTAL INHERITED MAINTENANCE COST: $[low]-$[high]

Negotiation lever: ask sale price reduction of $[low] (the floor of the inherited range) to compensate.
```

### Paste-Ready Buyer-Side Ask (Post-Gap-Detection)

> *"Service records show [last documented service date + mileage]. Per [Brand] severe-service schedule for [year model] at [current mileage] mi, the following services are missing: [list with estimated costs]. Total inherited maintenance: $[X-Y]. To compensate, I'm asking for a $[X] reduction in sale price, OR have the dealer complete these services at their cost before delivery. Please confirm in writing which option you prefer."*

### Cross-References

- Gotcha V1 (`SKILL.md`): CARFAX 1-owner is necessary but not sufficient — service records reveal maintenance; missing CVT fluid service at 60k is $300-$400 inherited cost
- `references/subaru_cpo_program.md`, `references/honda_cpo_program.md`, `references/toyota_cpo_program.md` — CPO programs include some of these expected services pre-sale; CPO premium may be net-zero if it includes the missed 60k/90k major service
- `references/vertical_playbooks.md#part-1--pickup-truck-specifics` § 4 — pickup-specific PPI items add to this list for F-150 / Silverado / Ram / Tundra / Tacoma (frame, hitch, V8 exhaust manifold, EcoBoost turbo, Hemi MDS lifters)
- `references/negotiation_playbook.md` — inherited-cost figure feeds Phase 6 counter as a quantified anchor ("PPI + service record gaps total $X — sale price needs to drop $X to neutralize")
