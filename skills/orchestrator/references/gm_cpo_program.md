# GM Certified Pre-Owned Program (Chevrolet / GMC / Buick) (as of 2026-05-18)

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)
> **Data refresh schedule**: state rates / CPO programs / EV incentives / lease parameters should be re-verified annually or upon any user-cited deal that contradicts. The 2026-05-18 timestamp marks last full audit.

GM Certified Pre-Owned covers Chevrolet, GMC, and Buick used vehicles. Cadillac CPO is structurally a separate luxury tier (different coverage levels, different inspection, dedicated CT Certified Pre-Owned program) and is deferred to `cadillac_cpo_program.md` (P3.5 deliverable).

GM CPO is structurally a single-tier mainstream program with moderate powertrain coverage (6yr/100k), shorter than Hyundai/Kia (10/100k) and TCUV (7/100k) but with a strong limited B2B extension and dedicated tiers for Duramax diesel (Silverado HD / Sierra HD) and EV models (Bolt EV / Bolt EUV / Hummer EV / Lyriq EV).

This file mirrors the structure of the prior CPO reference files.

---

## Eligibility Criteria

Per GM Certified Pre-Owned at gmcertified.com:

| Criterion | Threshold |
|-----------|-----------|
| Age from original in-service date | **Max 6 years** (e.g., 2026 program covers 2020-2026 in-service vehicles) |
| Mileage | **Under 75,000 mi** |
| Inspection | Must pass GM's **172-point certified inspection** |
| Dealer | Must be sold by authorized Chevrolet / GMC / Buick dealer |
| Title / history | Clean title; no major accident on CARFAX / AutoCheck; no flood, salvage, fire, or rebuilt branding |

A 2022 Chevrolet Equinox LT with 41,000 mi sold by a Chevrolet dealer in 2026 is fully eligible (4 yr / 41k mi).

A 2020 GMC Sierra 1500 with 72,000 mi in 2026 is at the eligibility edge: 6 yr from in-service if early-2020 build, under 75k mi, eligible.

A 2019 GM vehicle in 2026 is generally NOT GM CPO eligible (>6 years from in-service).

### Single-tier program (Cadillac is separate)

GM CPO for Chevy / GMC / Buick is a single tier. Cadillac has its own CPO program with different terms (extends to ~$2,000+ embedded value, longer B2B, Cadillac-specific concierge), see `cadillac_cpo_program.md`.

---

## Coverage Granted (When Enrolled)

### ICE / Hybrid models

| Coverage | Term |
|----------|------|
| **Powertrain warranty extension** | **6 years / 100,000 miles from original in-service date** |
| **Limited bumper-to-bumper extension** | **12 months / 12,000 miles** added (from CPO purchase date, NOT from original in-service) |
| Deductible | $0 |
| Roadside Assistance | 6 years / 100,000 mi 24/7 included (from in-service date) |
| Transferable | Yes (to subsequent buyers within warranty period) |
| Trip Interruption | $200/day, up to $500 total |
| Rental Car Allowance | $40/day for covered repairs (max 5 days) |
| OnStar trial | 3-month OnStar + Connected Services trial on enrollment |
| Sirius XM trial | 3-month on enrollment |
| Scheduled maintenance | 2 maintenance visits included (1 oil change + 1 tire rotation) |

The 6yr/100k powertrain coverage starts from the **original in-service date**, NOT the CPO purchase date.

### Duramax Diesel models (Silverado 2500HD / 3500HD / Sierra 2500HD / 3500HD)

| Coverage | Term |
|----------|------|
| Standard 6/100k powertrain | Applies |
| **Duramax Diesel coverage** | **5 years / 100,000 miles from in-service**, diesel-specific tier including fuel injectors, high-pressure fuel pump (Bosch CP4 on 2017-2021; updated pump on 2022+), turbo, DEF system, EGR cooler, particulate filter |

Note: Duramax-specific coverage is **5/100k**, shorter than Ford PowerStroke's 7/100k diesel tier on Gold Certified. This is a structural disadvantage for GM HD diesel CPO vs Ford F-250/F-350 Gold.

### EV models (Bolt EV / Bolt EUV / Hummer EV / Cadillac LYRIQ / Chevrolet Blazer EV / Equinox EV / Silverado EV)

EV models get standard 6/100k powertrain PLUS separate HV battery component coverage:

| Coverage | Term |
|----------|------|
| **High-voltage battery component coverage** | **8 years / 100,000 miles from original in-service date** (matches federal EV mandate; in CA-emission states, 10 years / 150,000 miles) |
| Battery degradation threshold | If pack falls below 60% state-of-health on Bolt, 70% on Ultium (Hummer / Lyriq / Blazer EV / Equinox EV / Silverado EV), GM covers replacement |
| Drive motor / inverter / onboard charger | Covered under HV battery component line |
| Public-charging hardware (CCS port) | Covered under B2B |

Note: GM matches the federal floor (8/100k) for the HV battery, shorter than Hyundai/Kia EV CPO (10/100k). In CA-emission states, the 10/150k applies for the HV pack but this is regulatory, not GM-program-specific.

### Bolt EV Recall Note (2017-2022)

The 2017-2022 Bolt EV / Bolt EUV had a major LG Chem battery recall. Any 2017-2022 Bolt sold as GM CPO MUST have the recall remedy documented (battery module replacement OR software-update + diagnostic confirmation). Verify the recall remedy at CPO close, see `ev_buyer_playbook.md` § Bolt-specific section for protocol.

---

## Embedded Value

Compare GM CPO to third-party extended powertrain warranties:

| Coverage Source | Cost |
|-----------------|------|
| GM CPO (built-in) | Already in dealer price |
| GM Protection Plan / GMPP (separate, post-CPO) | $1,500-$2,800 layered on top |
| Third-party (CARCHEX, Endurance, Olive) | $1,800-$2,800 for equivalent 6/100k powertrain |
| Third-party diesel-inclusive coverage | $2,800-$4,200 |
| Third-party EV-battery-inclusive coverage | $3,500-$5,500 |

**GM CPO is functionally a $1,500-$2,500 embedded value for ICE models** when the dealer enrolls it. For Duramax diesel, embedded value rises to **$2,500-$3,500**. For EVs (Bolt, Hummer, Lyriq, Blazer EV, Equinox EV, Silverado EV), embedded value is **$2,000-$3,200** (lower than Hyundai/Kia EV CPO due to shorter HV battery term).

**Market premium typical**: **$800-$1,500 over identical non-CPO same VIN** at typical US GM dealers. Duramax CPO premium often runs an additional $300-$800.

So buyer often nets **+$500 to +$1,200 of value** (ICE) or **+$1,500 to +$2,500** (Duramax diesel / EV) after paying the CPO premium.

---

## What GM CPO Does NOT Cover

- Wear items (tires, brake pads, wiper blades, 12V battery)
- Accident damage (not warranty work)
- Cosmetic items (paint chips, interior wear, scratched alloys, bed liner wear on pickups)
- Items modified or altered by aftermarket parts (tunes, lifts, non-GM audio, non-GM turbos)
- Routine maintenance beyond the 2-visit included term (oil changes, filter services)
- Pre-existing conditions documented at time of CPO inspection
- 12V auxiliary battery on EVs (only HV traction pack is covered)
- SuperCruise hardware on older models without a current OnStar subscription (SuperCruise requires active subscription to function; OnStar is included only as 3-month trial under CPO)

---

## CPO vs Non-CPO Math (worked example, Silverado Duramax)

For a 2022 Silverado 2500HD LT Duramax 4WD 52k mi:

| Scenario | Effective Cost |
|----------|---------------|
| **GM CPO included** in dealer sale at $54,990 | $54,990 OTD basis (CPO + 6/100k powertrain + 12/12 B2B + 5/100k diesel tier embedded) |
| Non-CPO same VIN at $53,490 (-$1,500) + buy GMPP Major Guard $3,000 + diesel rider $1,200 | $57,690 effective |
| Non-CPO same VIN at $53,490 + third-party 6/100k powertrain only $2,200 (no diesel-specific) | $55,690 effective with diesel risk uncovered ($4,500-$10,000 expected-value exposure on CP4 / injectors) |
| Non-CPO same VIN at $53,490 + self-insure | $53,490 net cost, accept ~$6,000-$10,000 expected-value risk on diesel-specific components |

For Duramax diesel HD pickups, GM CPO is hard to beat with self-insure math, the CP4 fuel pump risk on 2017-2021 Duramax is particularly load-bearing.

---

## Negotiating GM CPO (Phase 6 play)

If a GM vehicle is CPO-eligible but the dealer has not enrolled it:

> Could you enroll this vehicle in the GM Certified Pre-Owned program as part of the sale? This adds the 6yr/100k powertrain warranty extension, 12mo/12k limited B2B, and (for Duramax models) the diesel-specific component coverage. Standard GM-authorized dealer offering for sub-75k mi cars under 6 years from in-service.

Dealers can enroll a qualifying car for **~$500-$800 internal cost** (172-point inspection + program enrollment fee). They may accept this as part of the deal at no additional charge if OTD ask has been reduced elsewhere.

**Phase 6 negotiation play for Duramax**: When a non-CPO Duramax 2500HD/3500HD is priced within $2,000 of a CPO same-model same-mileage comp, ask the non-CPO dealer to enroll CPO at their cost. The diesel-specific component coverage delta (CP4 fuel pump on 2017-2021 specifically) makes this the highest-leverage margin give on GM HD diesel pickup negotiations.

**Phase 6 negotiation play for Bolt EV (2017-2022)**: Always verify the LG Chem battery recall remedy was performed before considering CPO. If the recall remedy is NOT documented, CPO is suspect, walk or demand documentation. See `ev_buyer_playbook.md` § Bolt recall protocol.

---

## For Out-of-CPO Cars (Over 6 Years or 75k+ mi)

A 2019 GM vehicle or any GM with 80k+ mi is ineligible for GM CPO. Options:

1. **GM Protection Plan (GMPP)**, GM's separately-sold extended warranty. Tiers: Major Guard (top, comprehensive), Smart Care (mid), Powertrain (entry). Available 5/60k through 8/125k from time of purchase. Duramax-specific tiers available.
   Typical GM dealer GMPP pricing for an out-of-CPO 2018 Silverado 1500 (~85k mi at purchase):
   - Major Guard comprehensive: approximately $2,800-$3,800
   - Powertrain only: approximately $1,700-$2,400
   - Duramax-specific rider (HD only): +$700-$1,200
2. **Third-party extended warranty**, buy elsewhere. For Duramax, verify the plan explicitly covers CP4 fuel pump (or its replacement on 2022+), injectors, turbo, DPF.
3. **Self-insure**, GM reliability is bimodal: 5.3L / 6.2L L8X V8 NA models are statistically reliable; 2.7L Tri-Power Turbo (2019+) has lower mileage track record; Duramax CP4 era (2017-2021) has notable failure risk. Self-insure is defensible for L83/L84/L8X V8 on 1500-series with clean maintenance.

For out-of-CPO ICE GM, expect price to be ~$1,200 lower than a comparable CPO. For Duramax out-of-CPO, expect ~$2,500-$4,000 lower.

---

## CPO Verification at Close

Confirm CPO status before signing:

- [ ] **GM Certified Pre-Owned Certificate** (PDF) with VIN, vehicle data, in-service date
- [ ] **172-point inspection report** (signed by GM-certified tech, dated)
- [ ] Verify warranty start date matches original in-service date for powertrain (B2B starts from CPO purchase date)
- [ ] Confirm transferability documentation
- [ ] For Duramax: verify 5yr/100k diesel-specific coverage is explicitly noted on certificate
- [ ] For EV models: verify 8yr/100k HV battery coverage (or 10/150k if CA-emission state)
- [ ] For 2017-2022 Bolt EV: verify LG Chem battery recall remedy documentation
- [ ] Verify SuperCruise hardware (if equipped) is functional; OnStar subscription status disclosed
- [ ] If dealer says "this is CPO" but cannot produce certificate at close: walk or demand documentation

---

## Brand-Specific Model Notes

### Silverado 1500 (5th gen 2019-2024 / 6th gen 2025+) / GMC Sierra 1500
- Most common GM pickup on used market
- Powertrains: 2.7L Turbo / 5.3L V8 / 6.2L V8 / 3.0L Duramax Diesel inline-6 (light-duty diesel)
- Light-duty 3.0L Duramax diesel on 1500-series qualifies for the 5/100k diesel tier
- AT4 (Sierra) / Trail Boss (Silverado) are off-road trims; ZR2 (Silverado 2023+) is most off-road capable
- See `vertical_playbooks.md#part-1-pickup-truck-specifics` § 4 for tow rating verification by engine x axle x package

### Silverado HD 2500/3500 / Sierra HD 2500/3500 (4th gen 2020-2024 / 5th gen 2025+)
- Heavy-duty pickups; 6.6L Duramax Diesel V8 is the high-value engine
- CP4 fuel pump on 2017-2021 Duramax HD; updated pump on 2022+
- Allison 10-speed automatic on diesel; GM 10L80/10L90 on gas

### Suburban / Tahoe (5th gen 2021+) / Yukon / Yukon XL (5th gen 2021+) / Escalade (5th gen 2021+)
- Full-size SUVs; 5.3L / 6.2L V8 / 3.0L Duramax diesel (Tahoe/Yukon/Suburban/Escalade)
- Escalade is Cadillac, separate Cadillac CPO program (deferred to P3.5)

### Equinox (3rd gen 2018-2024 / 4th gen 2025+) / Traverse (2nd gen 2018-2023 / 3rd gen 2024+) / Blazer (3rd gen 2019+)
- Mid-size crossovers; standard CPO coverage
- Equinox EV (2024+) is BEV variant, gets EV CPO line
- Blazer EV (2024+) is BEV variant, gets EV CPO line

### Bolt EV / Bolt EUV (2017-2023)
- Compact EV / subcompact crossover EV
- 2017-2022 had LG Chem battery recall, verify recall remedy before CPO acceptance
- 2023 redesigned pack, fewer recall issues
- Bolt production ended 2023; 2025+ Bolt returns on Ultium platform (new generation)

### Hummer EV (2022+) / Lyriq EV (Cadillac, 2023+), Ultium platform
- Hummer EV: 3-motor or 2-motor configurations; massive battery pack (~205 kWh)
- Lyriq: Cadillac luxury EV, separate Cadillac CPO (deferred to P3.5)
- See `ev_buyer_playbook.md` for Ultium-specific SoH and NACS adapter notes

### Buick lineup
- Enclave (3-row SUV) / Encore GX / Envista, all standard CPO ICE
- Buick is being phased out at the corporate strategy level; expect declining new-vehicle inventory through 2027

### Camaro / Corvette (2014-2024 / 2020+ C8 Corvette)
- Camaro production ended 2024 model year; final units circulating on used market
- C8 Corvette (2020+) qualifies for standard GM CPO; Z06 / E-Ray hybrid (2024+) verify trim-specific items

---

## Related GM Programs

- **GM Protection Plan (GMPP)**, GM's separately-sold extended warranty. Different from CPO.
- **GM Family First / Friends & Family**, employee/family discount program
- **GM Military / First Responder / Educator**, $500-$1,000 off new
- **OnStar / Connected Services**, subscription-based connectivity
- **SuperCruise**, hands-free highway driving (requires active OnStar subscription)
- **GM Card**, Mastercard with auto purchase rewards

Most of these apply to NEW GM purchases. Used GM CPO is its own thing.

---

## GM CPO vs Other CPO Programs, Quick Comparison

| Feature | GM CPO (Chevy / GMC / Buick) | Ford Gold | Toyota TCUV | Hyundai CPO | Kia CPO |
|---|---|---|---|---|---|
| Age cap | 6 yr from in-service | 6 yr | 6 yr | 7 yr | 5 yr |
| Mileage cap | 75k mi | 80k mi | 85k mi | 80k mi | 60k mi |
| Inspection | 172-point | 172-point | 160-point | 173-point | 165-point |
| Powertrain extension | **6 yr / 100k from in-service** | 7 yr / 100k | 7 yr / 100k | 10 yr / 100k | 10 yr / 100k |
| Limited B2B post-factory | 12 mo / 12k (from CPO date) | 12 mo / 12k (from CPO date) | 1 yr / 12k | 1 yr / 12k | 1 yr / 12k |
| **Diesel-specific coverage** | **Yes, 5/100k diesel (Duramax)** | **Yes, 7/100k diesel (PowerStroke)** | n/a | n/a | n/a |
| EV HV battery coverage | 8 yr / 100k (10/150k in CA-emission states) | 8 yr / 100k | n/a | 10 yr / 100k | 10 yr / 100k |
| Deductible | $0 | $100/visit | $0 | $0 | $50 B2B / $0 powertrain |
| Included maintenance | **2 visits (oil + tire rotation)** | None | Limited (regional) | None | None |
| Embedded value (ICE) | $1,500-$2,500 | $1,500-$2,500 | $1,000-$2,000 | $1,500-$2,500 | $1,200-$2,000 |
| Embedded value (diesel) | $2,500-$3,500 | $2,500-$4,000 | n/a | n/a | n/a |
| Embedded value (EV) | $2,000-$3,200 | $2,000-$3,500 | n/a | $3,000-$4,500 | $2,800-$4,200 |
| Market premium typical | $800-$1,500 | $1,000-$1,800 | $1,000-$2,000 | $800-$1,500 | $700-$1,500 |

**Key structural differences**: GM CPO's powertrain term (6/100k) is the SHORTEST among major non-luxury programs. The 2-visit included maintenance is a unique feature (no other listed program includes scheduled maintenance under CPO). The Duramax diesel coverage at 5/100k is shorter than Ford PowerStroke 7/100k. For Bolt EV buyers, the LG Chem recall remedy verification is the unique CPO-validity gate. For Silverado / Sierra 1500 ICE buyers, GM CPO is competitive with Ford Gold but shorter on powertrain term, favoring Ford Gold on equivalent buyer profiles.
