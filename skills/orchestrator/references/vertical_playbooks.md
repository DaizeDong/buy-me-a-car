# Vertical Buyer Playbooks (Pickup / Heavy / Luxury)

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

This file combines two niche buyer-type playbooks that extend the mainstream-light-vehicle workflow. **Part 1 — Pickup Truck Specifics** covers 1/2-ton and mid-size pickups (F-150, Ram 1500, Silverado/Sierra 1500, Tundra, Tacoma, Ranger, Frontier, Colorado/Canyon) — tow rating, payload, factory vs aftermarket distinction, pickup-specific PPI items, and dealer tactics. **Part 2 — Heavy / Commercial / Luxury** covers HD pickups (F-250+, 2500+, 3500+), commercial vans / box trucks / fleet vehicles, and the luxury European / Japanese / American luxury brands (BMW / MB / Audi / Lexus / Genesis / Acura / Infiniti / Cadillac / Lincoln / Porsche).

## Part 1 — Pickup Truck Specifics

## Pickup Truck Specifics

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

Comprehensive reference for buying used full-size and mid-size pickups (F-150, Silverado/Sierra 1500, Ram 1500, Tundra, Tacoma, Ranger, Frontier, Colorado/Canyon). Covers:

1. Tow rating dependency (engine × axle × cab × package = real capacity)
2. Factory tow package vs aftermarket distinction
3. Payload dependency (separate from tow capacity)
4. Pickup-specific PPI items (frame, suspension, towing wear, body mounts, exhaust)
5. Used-pickup depreciation patterns
6. Pickup-specific dealer tactics

Loaded when buyer's vehicle target is any 1500-class or mid-size pickup (Phase 1 router gate fires on truck make/model).

---

### 1. Tow Rating Dependency Table — DO NOT trust the listing

Pickup tow ratings vary wildly within the SAME nameplate based on **engine × axle ratio × cab config × bed length × tow package**. A "2022 F-150 with tow package" can mean anywhere from 8,000 lb to 14,000 lb depending on the actual configuration. Buyers are routinely sold the wrong truck because the dealer's listing only says "tow package" without the configuration detail.

#### Ford F-150 2021-2023 Tow Capacity (SuperCrew 4x4 5.5' or 6.5' bed)

| Engine | Axle Ratio | Tow Package | Real Tow Capacity |
|---|---|---|---|
| 2.7L EcoBoost V6 | 3.55 | Std Trailer Tow | 9,000-9,800 lb |
| 3.3L V6 (base) | 3.55 | Std | 7,700 lb |
| 5.0L V8 | 3.31 | Std | 9,300 lb |
| 5.0L V8 | 3.55 | Max Trailer Tow Pkg | 11,300 lb |
| 3.5L EcoBoost V6 | 3.55 | Std | 11,300 lb |
| **3.5L EcoBoost V6** | **3.55 or 3.73** | **Max Trailer Tow Pkg** | **13,000 lb** |
| 3.5L EcoBoost HO (Raptor) | 4.10 | Std | 8,200 lb (lower; Raptor is off-road tuned) |
| PowerBoost Hybrid 3.5L | 3.73 | Max | 12,700 lb |
| 3.0L Power Stroke diesel | 3.55 | Max | 12,100 lb |

#### Ram 1500 2019-2024 Tow Capacity (Crew Cab 4x4 5.7' bed)

| Engine | Axle | Tow Pkg | Capacity |
|---|---|---|---|
| 3.6L Pentastar V6 | 3.21 | Std | 7,500-7,730 lb |
| 5.7L Hemi V8 | 3.21 | Std | 8,500 lb |
| 5.7L Hemi V8 | 3.92 | Max Tow Pkg | 11,540 lb (12,750 w/ light-weight options) |
| 5.7L eTorque mild hybrid | 3.92 | Max | 12,750 lb |
| 3.0L EcoDiesel V6 | 3.92 | Max | 12,560 lb |
| TRX (6.2L supercharged Hemi) | 4.10 | Std | 8,100 lb (TRX is off-road, not tow-tuned) |

#### Chevy Silverado / GMC Sierra 1500 2021-2024 (Crew Cab 4x4)

| Engine | Axle | Tow Pkg | Capacity |
|---|---|---|---|
| 2.7L Turbo I4 | 3.42 | Std | 9,500-9,800 lb |
| 5.3L V8 | 3.23 | Std | 9,500 lb |
| 5.3L V8 | 3.42 | Max Trailering | 11,400 lb |
| 6.2L V8 | 3.23 | Std | 11,800 lb |
| 6.2L V8 | 3.42 | Max | 13,300 lb |
| 3.0L Duramax diesel | 3.42 | Max | 13,200 lb |

#### Toyota Tundra 2022-2024 (Crew Cab 4x4)

| Engine | Tow Pkg | Capacity |
|---|---|---|
| 3.5L Twin-Turbo V6 | Std | 11,120 lb |
| 3.5L Twin-Turbo V6 | Tow Tech | 12,000 lb |
| 3.5L Hybrid (i-Force MAX) | Tow Tech | 11,450 lb |

#### Reading the Window Sticker / VIN for Tow Config

Buyer must verify the SPECIFIC truck's tow rating, not the trim's max-possible rating:

1. **Door-jamb sticker** has GVWR + GAWR + tire spec. Real tow capacity is derived from (GCWR − GVWR), not advertised.
2. **VIN decode** via Ford / Ram / GM official decoders shows installed option codes:
   - **Ford F-150 Max Trailer Tow Pkg = option code 53A or 53B** (depending on year)
   - **Ford F-150 Std tow = code 535** (most common; just hitch + 7-pin + 4-pin)
   - **Ram Max Tow = option code AHT** (with 3.92 axle electronic)
   - **Chevy Max Trailering = code NHT** (with 3.42 axle)
3. **Build sheet** (some dealers can pull from OEM) shows complete option list
4. **Trailer hitch receiver class** stamped on hitch:
   - Class III: 6,000 lb
   - Class IV: 10,000 lb
   - Class V: 16,000-20,000 lb (rare on factory 1500-class; common on HD trucks)
   Factory Max Tow on F-150/Silverado/Sierra/Ram typically Class IV

#### Tow-Capacity Negotiation Lever

If a listing claims "tow package" but the VIN decode shows std tow only, the buyer has leverage:
- Real tow capacity is 1,500-3,000 lb below advertised
- A truck advertised at "12,000 lb tow" that actually does 9,500 lb has a value drop of $1,500-$3,000
- Counter: "VIN decode shows std tow option 535, not Max Tow 53A. Listing says 'tow package' which is technically true but misleading on capacity. I'm asking for a $2,000 sale-price reduction to compensate."

This is a frequent pickup-listing mismatch — surface it in Phase 6 routinely on any pickup-trade.

---

### 2. Factory Tow Package vs Aftermarket Distinction

A truck with **only an aftermarket hitch** is functionally a "no tow package" truck. The list of equipment that comes with FACTORY tow (and is absent with aftermarket) is load-bearing:

| Equipment | Factory Max Tow Includes | Factory Std Tow | Aftermarket Hitch Only |
|---|---|---|---|
| Hitch receiver (welded to frame) | Yes Class IV/V | Yes Class III/IV | Bolt-on or weld-on; quality varies |
| 7-pin OEM trailer connector wired | Yes | Yes | Sometimes wired aftermarket — voltage/ground can be flaky |
| 4-pin trailer connector | Yes | Yes | Sometimes |
| Integrated Trailer Brake Controller (dash) | Yes (Ford from 2009+; GM 2015+; Ram 2019+) | No (or optional add-on) | No — must add aftermarket Tekonsha/Curt under-dash |
| Trailer sway control software | Yes (integrated with stability control) | Maybe (varies) | No |
| Heavier rear axle gearing (3.55+ Ford / 3.92 Ram / 3.42 GM) | Yes | Maybe | No (whatever came with the truck) |
| Transmission cooler (auxiliary or upgraded) | Yes | Yes (smaller) | No |
| Engine oil cooler upgrade | Yes (some) | Maybe | No |
| Larger radiator | Yes (some) | Maybe | No |
| 36-gal extended fuel tank (Ford F-150 Max Tow only) | Yes | No | No |
| Higher rated rear shocks / leaf packs | Yes (some Heavy Duty Payload variants) | No | No |
| Rear axle pumpkin / diff size upgrade | Yes (Ford Heavy Duty 9.75" vs std 8.8") | No | No |
| 7- or 4-pin OEM wiring harness back through chassis | Yes | Yes | Sometimes (cheap installs run wire under floor mat) |
| Towing display in instrument cluster | Yes | Yes (some) | No |
| Pro Trailer Backup Assist (Ford) | Yes | Maybe | No |
| Class IV vs Class III hitch rating | Class IV (10k lb) or V | Class III (6-7.5k lb) | Varies; many aftermarket hitches are Class III only |

#### Aftermarket hitch effective capacity

A 2021 Lariat 5.0L V8 with aftermarket hitch + 7-pin and NO factory tow package:
- Bumper-mounted vs frame-mounted hitch matters (frame-mount > bumper)
- Even Class IV aftermarket hitch (10,000 lb rated) is **derated by the truck's GCWR** without factory rear axle/cooling upgrades
- Real safe tow capacity: **8,000-9,000 lb** for a 9,300-lb-rated truck with aftermarket gear, due to:
  - No transmission cooler upgrade (transmission overheats above 8,500 lb sustained)
  - No integrated TBC (aftermarket Tekonsha is functional but adjustment requires user calibration; factory integrated is auto-calibrated)
  - No rear axle upgrade (8.8" axle saturates above ~9,000 lb sustained on V8)
  - No trailer sway integration

Counter language for aftermarket-tow listing: "Listing says 'tow package' but VIN decode + door-jamb show no factory tow option (no 53A / 535 / NHT / AHT code). The aftermarket hitch is rated to 10,000 lb but real safe sustained tow on this truck is closer to 8,500 lb without factory cooling and TBC. For my use case (13,000 lb travel-trailer) this truck does not meet the requirement and I'm passing."

---

### 3. Payload Capacity (Separate From Tow Capacity)

Payload = max weight inside the cab + bed + passengers + fuel + factory accessories. Payload is **separate** from tow capacity and can be the binding constraint:

| Truck | Typical Payload | Notes |
|---|---|---|
| F-150 SuperCrew 5.5' bed XLT 4x4 EcoBoost std | 1,640-1,780 lb | Crew cab + 4x4 + EB = lowest payload |
| F-150 SuperCrew 6.5' bed Heavy Duty Payload Pkg | 2,200-2,400 lb | HDPP option, separate from Max Tow |
| Ram 1500 Crew Cab 4x4 Hemi std | 1,700-1,800 lb | |
| Ram 1500 Crew Cab 4x4 Hemi Max Tow | 1,500-1,600 lb (Max Tow REDUCES payload due to heavier driveline) | Counter-intuitive trade-off |
| Silverado 1500 Crew 4x4 5.3L std | 1,750-1,900 lb | |
| Tundra Crew 4x4 i-Force std | 1,940-2,030 lb | Tundra has best stock payload |
| Tacoma Crew 4x4 V6 std | 1,140-1,280 lb (mid-size) | |

**Tongue weight on bumper hitch:** 10-15% of trailer weight. A 13,000 lb trailer = 1,300-1,950 lb tongue weight. Plus 2 passengers (350 lb) + gear (200 lb) = 1,850-2,500 lb on the truck → many F-150 SCrew 4x4 EB configs **exceed payload capacity before tow capacity matters**.

This is the #1 pickup-buyer mistake. Verify payload before tow-rating optimization.

---

### 4. Pickup-Specific PPI Items (Distinct From Sedan/SUV PPI)

Standard sedan PPI (CARFAX + service records + brake/tire/fluids) misses pickup-specific failure points. Add these to the inspection:

#### Frame inspection

- Rear frame rust around spare-tire well (water collects)
- Rear cross-member rust (especially Toyota Tacoma 2005-2010 — class-action) and (Ford F-150 1997-2003 — separate class-action). **2015-2024 trucks generally OK** but inspect anyway in rust-belt states (IL, OH, PA, MI, NY, NJ, NE).
- Frame cracks around hitch mount points — sign of regular over-tow use
- Hidden surface rust under bedliner (drop-in liners hold moisture)
- Frame paint condition (factory paint = original; recent paint = damage repair)
- Body-mount bushings (12 mounts on F-150; cracked/missing rubber = corrosion access to frame and body misalignment)

#### Suspension under-load test

- Eyeball spring sag with truck on level ground — rear should sit 0-1" higher than front (raked stance); equal or rear-sagging = worn springs
- Bump-stop wear pattern — visible rubber contact marks = regular bottoming-out from over-tow or off-road
- Shock dust boots intact (torn boots = early shock failure)
- Sway bar end-link rubber bushings (worn = clunk on washboard roads)
- Rear leaf-spring stack alignment (off-center = previous accident or curb-hit)
- Steering rack play (rare on modern trucks but check)

#### Hitch + Towing wear pattern

- **Hitch receiver wear** — regular tow use leaves chrome wear inside the receiver; sliding pattern indicates frequent insertion/removal
- **Tongue weight ball wear** — flattened ball top = regular heavy tow; gouged = improper coupler match
- **Hitch pin hole wear** — elongation = regular use
- **7-pin connector wear** — corroded pins = exposure; bent pins = forced connection; replacement (new chrome) = damage repair
- **Trailer brake controller test** — must function in gain test (dash knob 1-10); LED indicator goes from amber-no-trailer to green-trailer-connected; aftermarket Tekonsha installs often have wrong wire splice

#### Transmission cooler

- Front of radiator stack — look for separate auxiliary cooler with 2-3 lines running to transmission
- Inspect cooler fins for road-debris damage
- No fluid weeping at cooler joints
- Transmission fluid color from dipstick (or via service records if sealed) — clean amber/red = OK; dark brown = overdue change; metallic-grey = internal damage

#### Differential (rear)

- Rear axle fluid color via fill-plug inspection — clean amber = OK; metallic = bearing wear
- 4x4 trucks: front axle fluid same check
- Pinion-yoke wear (touch test) — loose = U-joint or pinion bearing failure

#### Exhaust

- **V8 trucks**: exhaust manifold cracks (Ford 5.0L, Chevy 5.3L/6.2L, Ram 5.7L Hemi prone after 100k mi with work-truck stress) — listen for ticking on cold start
- **Hemi 5.7L specifically**: lifter tick (MDS lifter failure) audible cold; cylinder deactivation = wear pattern check
- **EcoBoost 3.5L specifically**: turbo seal leak (smoke on cold start = turbo seal); intercooler condensation collection (causes misfires); spark plug condition critical
- Cat health (passes IL emissions in DuPage County)

#### Bed condition

- Bedliner: drop-in plastic = pop out and inspect bed for rust/dents
- Spray-in bedliner: tap test for hollow spots (rust trapped beneath cheap spray)
- Bed-mount rust at corners (water collection)
- Tailgate handle + latch function (handle wear from frequent use)
- Tailgate cable condition (rusted/frayed cables on 10+ year trucks)
- Bedside dents (snow piles, plow flicks)

#### Cab

- Floor pan rust under carpet (rear footwell especially)
- Drain plugs functional
- Roof rust spots above headliner
- Door-hinge wear (regular work-truck use = sag on driver door)

#### Drivetrain heat indicators

- Transfer case (4x4 trucks) — heat marks on case
- Transmission pan — heat marks or fluid weeping
- Engine oil pan — heat marks (overheating history)

#### Plow-truck flags

If truck has plow brackets installed or hooks at front bumper:
- Frame stress at plow mount points
- Body mount cracking
- Front suspension wear (plows beat front springs)
- Cooling system upgrade signs (plow trucks add coolers)
- Premium-rate insurance flag (some insurers raise rates for ex-plow vehicles)
- Highly negotiable — ex-plow trucks usually $1,500-$3,000 below clean comp

---

### 5. Used-Pickup Depreciation Patterns

Trucks depreciate differently from sedans:

| Year | Typical Retained Value (full-size 1500) | Notes |
|---|---|---|
| Year 1 (~12 mo) | 75-80% of MSRP | Steeper than sedan year-1 |
| Year 2 | 65-70% | Pickup market reset; CPO program targets here |
| Year 3 | 55-60% | Sweet spot for used buyers |
| Year 4-5 | 50-55% | Plateau begins |
| Year 6-8 | 45-50% | Slow decline if low miles |
| Year 9-10 | 35-45% | Mileage-dominated |
| Year 11+ | Floor-priced by maintenance backlog (frame rust, suspension overhaul, transmission) |

**The buyer's reference**: 2022 F-150 XLT EcoBoost SCrew 4x4 with MSRP ~$52,000 (Max Tow + Iconic Silver). At year 3 expected retained value: 55-60% × $52,000 = $28,600-$31,200 wholesale, $32-36k dealer retail. Currie's $41,995 ask is at the **retail premium tier** (not deal-floor); $38-40k is the deal-floor zone for this configuration.

#### Comparison to ICE sedan depreciation

| | Year 3 retained (sedan) | Year 3 retained (full-size pickup) |
|---|---|---|
| Premium German sedan | 50-55% | n/a |
| Mainstream Japanese sedan | 65-70% | n/a |
| Mainstream truck (F-150, Silverado, Ram) | n/a | 55-60% (steeper) |
| Tundra (Toyota truck premium) | n/a | 65-70% (Japanese-truck retention) |
| Tacoma (mid-size) | n/a | 70-75% (legendary retention) |

**Tacoma is the depreciation exception** — holds value better than any other US truck due to legendary durability rep. Tundra second. Domestic full-size (F-150, Silverado, Ram) cluster around 55-60% year-3.

#### Trim premium (used)

- XLT vs Lariat used premium: $2,500-$4,500 (Lariat has heated/cooled leather seats, larger nav, BLIS standard)
- Lariat vs King Ranch / Limited / Platinum: $3,000-$6,000 (luxury packages, real wood, panoramic roof, 360 cam)
- Sport Trim Package premium (XLT Sport / Lariat Sport): $500-$1,200 (cosmetic + black grille)

---

### 6. Pickup-Specific Dealer Tactics

#### "Tow ready" / "tow package" listing language

Most common pickup-listing deception. "Tow package" can mean factory Max Tow, factory Std Tow, or aftermarket hitch only. Counter: demand VIN decode + option code verification (53A/535/NHT/AHT) in writing before any deposit.

#### "Plow prep" or "winter package"

Code for ex-fleet / ex-plow truck. Front-end stress + cooling system upgrades are positives, but insurance rates and frame-stress are real risks. Negotiate $1,500-$3,000 below clean comp.

#### "Work truck" / "fleet" history on CARFAX

CARFAX reports fleet usage as "rental fleet" or "commercial fleet." Commercial fleet = construction/utility truck; expect higher engine hours, hitched usage, but also more consistent maintenance (commercial fleets typically follow OEM service schedules). Negotiate $1,000-$2,000 below clean private-owner comp.

#### Aftermarket lift kit

Common on Ram and F-150 in rural/red-state markets. Issues:
- Voids OEM driveline warranty (CV joint angles increased)
- Reduces tow capacity (geometry change)
- Insurance flag (some insurers refuse to cover aftermarket lifts)
- Negotiate $1,000-$3,000 below clean OEM comp; demand stock-suspension photos if dealer can't show lift documentation

#### Aftermarket wheels / oversized tires

- 35" tires on F-150 = -2 mpg, -1,500 lb tow, speedometer error
- 33" tires = -1 mpg, -500 lb tow
- Negotiate to restore stock wheels/tires OR get a $1,000-$2,000 price reduction

#### "Pickup truck premium" — current market context

2022-2024 used pickup pricing was elevated (~10-15% over historical norm) due to 2021-2022 chip shortage. By 2026 the premium has compressed but used full-size pickups still trade at 5-10% above pre-2021 historical norm. Build this into baseline target.

#### F&I "Tow service plan" / "RV-prep package"

$1,500-$2,500 add-on offered at close. Most factory tow packages already cover trailer brake controller calibration and 7-pin troubleshooting via OEM warranty. Decline.

---

### 7. Pickup-Specific Phase 6 Checklist

Before sending an OTD counter on a used pickup:

- [ ] VIN decode confirms engine + axle + tow package option codes (53A/535/NHT/AHT)
- [ ] Real tow capacity verified against buyer's actual needs (the buyer: 13,000 lb → requires factory Max Tow only)
- [ ] Payload capacity NOT exceeded by buyer's actual use (passengers + tongue weight + bed cargo)
- [ ] Factory vs aftermarket hitch distinction confirmed
- [ ] Listing claims of "tow ready" verified by VIN decode (not just listing text)
- [ ] Frame inspection booked into PPI scope
- [ ] If V8: exhaust manifold + lifter tick check booked
- [ ] If EcoBoost: turbo seal + intercooler check booked
- [ ] Ex-plow / ex-fleet posture asked of dealer in writing
- [ ] Lift kit / oversized tires inspected for warranty + insurance impact

### 8. Pickup-Specific Walk Conditions

- VIN decode reveals std tow option (535) but listing claimed Max Tow → either renegotiate -$2k or walk
- Aftermarket lift kit without documented installation + alignment specs → walk
- Frame rust visible in spare-tire well or rear crossmember → walk in rust-belt states
- Multiple owners + commercial fleet history + over-tow signs → walk
- Tongue-weight + passenger + gear math exceeds payload capacity → walk; truck is wrong for buyer use case
- Integrated TBC test fails (no green LED when connected to trailer) → renegotiate $300-$500 OR walk

### Cross-References

- `references/pdf_review_checklist.md` — CARFAX patterns; pickup-specific is additive to sedan checklist
- `references/trade_in.md` — pickup as trade-in (lien handling + Hemi/EcoBoost specific resale)
- `references/state_fees.md` — IL/PA/TX/OH/MI rust-belt states have higher frame-rust risk for cross-state purchases
- SKILL.md Phase 3 — pickup inventory dispatch should add tow-config column
- SKILL.md Phase 9 — pickup-specific close-day walk-around checklist (factory tow option verification at delivery, integrated TBC functional test)

## Part 2 — Heavy / Commercial / Luxury

## Heavy-Duty / Commercial / Luxury Axes

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

Buyer-type extensions beyond the core mainstream-light-vehicle workflow. Covers heavy-duty pickups (HD trucks), commercial vehicles (cargo vans / box / fleet), and luxury (BMW / MB / Audi / Lexus / Genesis / Acura / Infiniti / Cadillac / Lincoln). Each axis has structurally different negotiation, financing, lease, and ownership patterns that the standard SKILL.md flow does not handle out-of-the-box.

Cross-references: Part 1 above (1/2-ton pickups — F-150, RAM 1500, Silverado 1500, Tundra, Tacoma), `lease_playbook.md` (luxury lease arbitrage), `ev_buyer_playbook.md` (Cadillac LYRIQ, Lincoln Star EVs, electric Sprinter).

### 1. Heavy-Duty Pickups (F-250 / F-350 / RAM 2500 / RAM 3500 / GM 2500HD / 3500HD)

HD pickups are 3/4-ton (250 / 2500 class) and 1-ton (350 / 3500 class) trucks designed for heavy towing, payload, and commercial use. Different from the light-duty 1/2-ton pickups covered in Part 1 of this file.

#### 1.1 Spec axes the buyer MUST capture at Phase 1

| Field | Why load-bearing |
|---|---|
| **GCWR (Gross Combined Weight Rating)** | Total weight of truck + trailer + cargo + passengers. Federal CDL trigger at 26,001 lbs GCWR; below that, no CDL needed. Many F-450 / RAM 3500 dually combos exceed 26,000 GCWR with a loaded fifth-wheel — CDL required. |
| **Tow rating (5th-wheel / gooseneck vs conventional)** | 5th-wheel and gooseneck tow ratings are dramatically higher than conventional bumper-pull (e.g., F-350 SRW conventional 16,500 lbs vs 5th-wheel 24,800 lbs vs gooseneck 32,500 lbs). Buyer's trailer type determines which rating matters. |
| **Engine (gas vs diesel)** | Diesel: Ford PowerStroke 6.7L, Ram Cummins 6.7L I6, GM Duramax 6.6L V8. Gas: Ford 7.3L "Godzilla" V8, Ram 6.4L Hemi V8, GM 6.6L Gas V8. Diesel: $9k-$11k premium, 22-28 MPG towing-loaded, $90k+ engine repairs at high mileage. Gas: $0 premium, 14-18 MPG loaded, $25k engine. |
| **Axle ratio** | 3.55, 3.73, 4.10, 4.30 (Ford / GM) or 3.42 / 3.92 / 4.10 (Ram). Lower numerical = better fuel economy, lower tow. Higher = more tow capacity, worse MPG. |
| **Cab configuration** | Regular cab (work truck, cheapest), Extended/SuperCab (4-door but rear suicide-style, less back room), Crew Cab (full 4-door, most common for retail). |
| **Bed length** | 6.5 ft (standard, fits most setups) vs 8 ft (heavy-duty work, dually pairing). |
| **Dually (DRW) vs SRW** | DRW = Dual Rear Wheel, 4 rear tires, only on 1-ton (350/3500). Higher payload (5,000-7,500 lbs vs SRW 3,500-4,500). Required for gooseneck-fifth-wheel combos over 25k lbs. Wider rear track — limits parking / urban use. |
| **Trim (Tradesman/XL vs King Ranch/Platinum/Limited/Longhorn)** | XL/Work Truck: vinyl floors, manual everything, $50-$65k. Lariat/SLT: leather, navigation, $65-$80k. King Ranch / Platinum / Limited / Longhorn: $80-$110k. Dual-tank diesel King Ranch is the volume HD trim across all 3 makes. |

#### 1.2 EPA emissions warnings — CRITICAL

**DELETED EMISSIONS / EGR / DPF SYSTEMS ON DIESEL TRUCKS ARE FEDERALLY ILLEGAL** under the Clean Air Act § 203. EPA pursues violators aggressively as of 2023-2026.

- DEF (Diesel Exhaust Fluid) delete: ILLEGAL.
- EGR (Exhaust Gas Recirculation) delete: ILLEGAL.
- DPF (Diesel Particulate Filter) delete: ILLEGAL.
- "Tuned for performance" with emissions still intact: legal.
- "Deleted by previous owner": federal liability transfers to current owner once a violation is identified. Buyer can be fined $4,500-$45,000 per violation.

Used-HD-diesel buyer MUST check at Phase 7 / PPI:

1. Visual check of DEF tank (still present, not bypassed).
2. Visual check of DPF (still present in exhaust line).
3. OBD-II scan for cleared / deleted ECU codes (delete tunes leave fingerprints).
4. Smoke output under load — black smoke = no DPF, likely deleted.

If deleted, walk regardless of price discount. Re-installing OEM emissions on a deleted truck costs $8,000-$15,000 plus parts wait-list (6+ months for some PowerStroke parts). Insurance also drops coverage on emissions-modified trucks.

#### 1.3 Commercial registration vs personal

Heavy-duty trucks can register as **personal** or **commercial**. Mechanics:

| Registration type | Cost | Restrictions |
|---|---|---|
| **Personal** | Standard reg + fuel-type fees | Cannot use commercially (cannot rent, cannot deduct as business expense on Schedule C, may not pull commercial trailers in some states). |
| **Commercial** | Higher reg (state-specific; $200-$1,200/yr); subject to weight tax (some states); commercial plates required | Allows business use, mileage deductions, IFTA fuel tax (interstate-commerce), commercial insurance. Some states require DOT number even for non-CDL trucks if commercial-registered. |

**Heads-up for Phase 1**: Buyer says "I'll use my truck for my landscaping business" — commercial registration may be legally required. Defer to CPA or commercial insurance broker if buyer is registering for business use.

#### 1.4 HD pickup Phase 9 close-day items (in addition to standard pickup checklist)

- [ ] DEF tank filled at delivery (DEF refills $15-$30 every 5k-10k miles thereafter)
- [ ] 5th-wheel hitch prep package verified if buyer needs it (factory option $750-$1,800 plus install $400-$800)
- [ ] Brake controller verified (integrated factory on all 2017+ HDs; aftermarket adds $300-$500)
- [ ] Diesel pre-conditioning explanation if buyer is new to diesel (glow plug warm-up, regen cycles, DEF system requirements)
- [ ] Insurance pre-quoted at commercial rate if commercial use planned (commercial coverage 1.5-2x personal rate)
- [ ] Emissions inspection / DEF certification at delivery (proof the truck is not deleted)

### 2. Commercial Vehicles (Cargo Vans / Box Trucks / Work Trucks)

Commercial vehicles are passenger-deficient utility vehicles built for fleet, contractor, delivery, and shuttle use. Different sales process, different financing, different incentives.

#### 2.1 Common models

| Model | Class | Use case |
|---|---|---|
| **Ford Transit** (Cargo, Crew, Passenger) | Class 1-3 van | Most popular US commercial van; cargo conversions for trades, plumbers, electricians; 130/148/164 inch wheelbases; gas 3.5L EcoBoost or 3.5L PFI; AWD optional |
| **Mercedes-Benz Sprinter** (also Freightliner branded) | Class 2-3 van | Most luxurious commercial van; "wedding shuttles", "tour buses", high-end upfit market; gas 2.0L turbo I4 or diesel 3.0L V6 (V6 now retired in some markets); legendary durability 400k+ mi reported |
| **RAM ProMaster** | Class 2-3 van | Italian-made (Fiat Ducato platform); FWD layout = unique cargo floor height; lowest entry price in segment; gas 3.6L V6 only since 2024 |
| **Chevrolet Express / GMC Savana** | Class 2-3 van | Holdovers from 2003 era — solid axle rear, body-on-frame; outdated cab but bombproof for fleet; gas 4.3L V6 / 6.6L V8 / 2.8L Duramax I4 diesel |
| **Ford E-Transit (electric)** | Class 2 BEV van | Electric Transit; 126 mi range; commercial-only purchase incentive ($7,500 § 45W per unit) |
| **Mercedes eSprinter (electric)** | Class 2 BEV van | Same as E-Transit, 71 kWh battery; § 45W eligible |

#### 2.2 Section 179 + Bonus Depreciation — Tax Strategy

The IRS § 179 deduction allows businesses to deduct the full purchase price of qualifying vehicles in the year of purchase, up to a vehicle limit:

| Tax year | § 179 vehicle limit | Bonus depreciation |
|---|---|---|
| 2024 | $30,500 (passenger) / $1.16M (heavy van) | 60% additional |
| 2025 | $30,500 (passenger) / $1.21M (heavy van) | 40% additional |
| 2026 | $30,500 (passenger) / TBD (heavy van) | 20% additional (phasing out) |

**Heavy van exception**: Vehicles over 6,000 lbs GVWR (Ford Transit 250/350 HD, Sprinter 2500/3500, ProMaster 2500/3500) qualify for FULL § 179 deduction without the $30,500 cap — up to the annual aggregate limit (~$1.2M).

**Buyer strategy at Phase 1**: If buyer is purchasing commercially, run the tax-deduction math at Phase 2 baseline. A $60k Transit 350 HD bought December 31 with § 179 + bonus can save $25k-$33k in same-year taxes (35% marginal bracket business).

#### 2.3 Upfit allowances

Commercial vans are often delivered "white cargo" (empty cargo space) and customized post-purchase:

- **Shelving / racking** (Adrian Steel, Ranger Design, Kargo Master): $2,500-$7,000 installed.
- **Ladder racks**: $500-$1,500.
- **Interior lighting**: $200-$800.
- **Vehicle wraps / signage**: $1,800-$4,500 (vinyl wrap full coverage).
- **Aftermarket cold-weather / heated cargo**: $2,500-$5,000.

**Manufacturer upfitter programs**: Ford QVM (Qualified Vehicle Modifier), Mercedes MasterUpfitter, RAM ProMaster Authorized Upfitter. Buyer can specify upfit at order time; dealer coordinates with upfitter; total rolled into financing.

#### 2.4 Fleet pricing — separate negotiation

Commercial dealers run a "fleet" desk distinct from retail. Fleet pricing is:

- **Volume-discount based** — fleet of 5+ units negotiates as a single deal; 2-4% off retail invoice typical.
- **Manufacturer-direct rebates** — Ford FCSD (Fleet, Commercial, Service Department), GM Onstar Business, Mercedes Pro: $500-$2,500/unit cash on order.
- **Financing terms** — TFS Business / Ford Credit Commercial / GM Commercial Credit offer non-recourse business financing; rates 50-100bps above personal auto.
- **Less negotiation back-and-forth** — fleet desks are volume-focused; one round of negotiation typical (vs 3-5 rounds retail).

Phase 4 outreach for commercial buyer: contact dealer's fleet manager directly (NOT internet sales). Email subject "Fleet quote, [N] units [Model], [Use Case]". Get fleet pricing in writing.

#### 2.5 Commercial vs personal plate decision

- **Commercial plates**: Required if vehicle used in commerce; allows business deduction; higher reg fees; restricts personal use in some states (cannot park overnight in residential zones in NJ, NY).
- **Personal plates**: Cannot claim business deduction unless detailed mileage log; cannot legally serve passengers for hire; insurance reverts to personal rate.

Defer to CPA. Document at Phase 1 if commercial use confirmed.

### 3. Luxury Cars

Luxury covers BMW / Mercedes-Benz / Audi / Lexus / Genesis / Acura / Infiniti / Cadillac / Lincoln. Volvo and Jaguar / Land Rover are luxury-adjacent (volume too small to address separately here — apply general luxury rules with Volvo skewing toward Honda-tier financing and JLR / Range Rover toward MB-tier).

#### 3.1 Lease penetration — luxury default

| Brand | Lease share of US sales | Implication |
|---|---|---|
| **BMW** | 60-67% | Lease is the default; CPO purchase second; cash purchase 3rd |
| **Mercedes-Benz** | 60-65% | Same |
| **Audi** | 55-62% | Same |
| **Lexus** | 45-55% | Slightly more purchase-balanced |
| **Genesis** | 40-50% | Newer brand, lease incentives aggressive |
| **Acura** | 35-45% | Mid-tier |
| **Infiniti** | 35-45% | Mid-tier |
| **Cadillac CT (CT4 / CT5)** | 50-60% | Sedan = lease default |
| **Cadillac SUV (XT4 / XT5 / XT6 / Escalade)** | 40-50% | SUV = balanced |
| **Lincoln** | 35-45% | Mid-tier |
| **Mainstream comparison (Honda / Toyota / Subaru)** | 18-28% | Reference baseline |

**Implication**: For luxury, Phase 1 buyer-type router should usually fire BOTH the financing gate (if not cash) AND prompt for lease vs loan. Default to lease unless buyer specifies otherwise. See `lease_playbook.md` for lease structure.

#### 3.2 Service plans typically included

Luxury OEMs include scheduled maintenance for the first 3-4 years on most new cars. Quick reference:

| Brand | Included maintenance | Roadside |
|---|---|---|
| **BMW** | BMW Ultimate Care: 3 yr / 36k mi covers brake fluid, micro filter, oil/filter, wiper inserts. Optional "Ultimate Care+" extends to 6 yr / 60k mi for ~$1,800 | 4 yr included |
| **Mercedes-Benz** | First service free (10k mi or 1 yr); subsequent services discounted via "Star Service" plans pre-paid at signing | Unlimited mileage roadside 4 yr |
| **Audi** | Audi Care: 5 yr / 50k mi pre-paid for $750-$1,200 (NOT included by default; sales tactic to add at signing — buyer should compare to cash-pay) | 4 yr |
| **Lexus** | Lexus Plus: 2 yr / 20k mi free; "Lexus Service Tradition" loaner | 4 yr |
| **Genesis** | Genesis Connected Services: 3 yr / 36k mi maintenance + valet pickup | 5 yr included |
| **Acura** | None on most; "AcuraCare" extended service optional add-on | Roadside 4 yr included |
| **Infiniti** | None; INFINITI Premium Care optional | Roadside 4 yr |
| **Cadillac** | 5 yr / 75k mi free maintenance "Premium Care Maintenance" | 6 yr roadside |
| **Lincoln** | "Lincoln Way" first 4 services free | 4 yr roadside |

**Tactic**: Cadillac (5 yr / 75k mi) and Genesis (3 yr / 36k mi + valet) are the most generous included maintenance among luxury brands. BMW / Mercedes / Audi require buyer to pay or add a plan. Compute the value at Phase 1 — Cadillac Premium Care saves $1,800-$3,000 over the included period; that's a hidden incentive equal to BMW / MB cash discount.

#### 3.3 Performance trim premium

Luxury performance variants (AMG, M, RS, F-Sport / TRD, S-Line, Type S, NISMO) carry significant premium over base luxury trims:

| Variant | Examples | Premium over standard trim |
|---|---|---|
| **BMW M** (M2, M3, M4, M5, X3M, X4M, X5M, X6M, XM) | $80k-$185k | $25k-$70k over base 2-Series, 3-Series, 5-Series, X3, X5, X6 |
| **Mercedes AMG** (AMG 35 → AMG 53 → AMG 63 → AMG 73 SE) | $60k-$220k | $20k-$80k over base |
| **Audi RS / S** (RS3, RS5, RS6, RS7, S4, S5, S6, S7) | $55k-$160k | $20k-$50k over base |
| **Lexus F-Sport / F** (IS-F, RC-F, LC-F, F-Sport handling) | $5k-$30k F-Sport package vs $10k-$25k F variant | Less premium than German rivals |
| **Cadillac V / V-Series** (CT4-V, CT5-V, CT5-V Blackwing) | $50k-$95k Blackwing | $15k-$30k over base |
| **Genesis Sport / Sport+** (G70 Sport, G80 Sport, GV70 Sport, GV80 Sport) | $5k-$15k premium | Modest |

**Implication**: Phase 6 negotiation on performance variants is structurally tougher — these run lower discount, lower allocation, dealer-side margin is fatter. Buyer should expect MSRP - 2-4% discount typical (vs MSRP - 6-10% on base luxury cars). Performance trims often have ADM (Additional Dealer Markup) on top of MSRP — see gotcha D9.

#### 3.4 Exclusive concierge networks

Luxury brands operate parallel customer experience programs:

- **BMW Genius** — dedicated product specialists at each dealer; one-on-one delivery + tech walkthrough; 90-day post-delivery follow-up calls. Standard on most BMWs.
- **Mercedes Concierge** — VIP white-glove pickup-and-delivery for service; loaner is same-class or up; 24/7 roadside hotline.
- **Lexus PLUS** — service loaner and valet pickup standard at all dealers; 2-yr free maintenance.
- **Audi DTL (Driver Tech Library)** — virtual tech support post-purchase.
- **Cadillac Concierge** — service pickup-and-delivery available, included on V models.

**Buyer-side value**: $500-$1,500/yr equivalent value in service convenience. Cadillac and Lexus offer the most under standard pricing; BMW / MB / Audi tend to include only on top trims or via service plan upgrades.

#### 3.5 Depreciation patterns — luxury 1st-3yr cliff then plateau

Luxury cars depreciate steeply in years 1-3 (40-50% loss) then plateau (3-5% per year after).

| Brand | 3-year retention | 5-year retention |
|---|---|---|
| **Porsche** | 65-75% | 50-60% (best in luxury) |
| **Lexus** | 60-70% | 50-58% |
| **Toyota / Honda (mainstream)** | 60-67% | 55-62% |
| **BMW** | 50-60% | 38-45% |
| **Mercedes-Benz** | 48-58% | 35-43% |
| **Audi** | 48-58% | 35-43% |
| **Acura / Infiniti** | 50-60% | 40-48% |
| **Cadillac** | 42-52% | 30-38% |
| **Lincoln** | 42-52% | 30-38% |
| **Genesis** | 45-55% | 35-45% (improving) |
| **Range Rover / Land Rover** | 38-48% | 25-32% (weakest mainstream luxury — known issues compound depreciation) |
| **Maserati** | 30-40% | 20-28% (sub-luxury depreciation cliff) |

**Practical implication**: Used 3-year-old luxury cars at 40-50% off MSRP are the value sweet spot — the buyer captures the steep first-cliff loss from the original lessee. This is why luxury CPO is critical.

#### 3.6 CPO — critical for luxury used

Luxury CPO programs are structurally more important than mainstream CPO:

| Brand | CPO program | Coverage |
|---|---|---|
| **BMW** | BMW Certified | 1 yr unlimited mi B2B + 1 yr unlimited mi powertrain (BMW extends factory warranty) |
| **Mercedes-Benz** | MB Certified Pre-Owned | 1 yr unlimited mi B2B + powertrain extension; eligible vehicles must be under 6 yrs / 75k mi |
| **Audi** | Audi Certified plus | 1 yr / unlimited mi from cert date OR remainder of 4 yr / 50k mi factory, whichever longer |
| **Lexus** | Lexus Certified Pre-Owned | 2 yr / unlimited mi from cert date + 6 yr / 100k mi from in-service (longest in luxury) |
| **Porsche** | Porsche Approved | 1 yr / unlimited mi + remainder of factory; extends to 2 yr if vehicle <6 yrs / 100k mi |
| **Cadillac** | Cadillac Certified | 1 yr / 12k mi B2B + 6 yr / 100k mi powertrain |
| **Genesis** | Genesis Certified | 5 yr / 60k mi from cert date (transferable, longest in luxury after Lexus) |
| **Acura** | Acura Certified | 1 yr / 12k mi B2B + 7 yr / 100k mi powertrain |
| **Infiniti** | Infiniti Certified | 1 yr / unlimited mi B2B + 6 yr / 100k mi powertrain |
| **Lincoln** | Lincoln Certified | 1 yr / 12k mi B2B + 6 yr / 100k mi powertrain |

**Differentiation from independent shop "Certified"**: An independent used dealer selling a 4-year-old BMW with a sticker labeled "Certified" is NOT BMW Certified unless the inspection was done at an authorized BMW dealer with the factory's 200-point checklist. The independent sticker is dealer-internal marketing only. Buyer must verify:

- Inspection done at authorized brand dealer (request inspection report with dealer letterhead).
- CPO certificate from BMW USA / MBUSA / etc. (not a dealer-printed sheet).
- Warranty registered to buyer's name in the brand's CRM (BMW account, MBO account).
- Vehicle eligible (under brand's age/mileage thresholds when certified).

The fake-CPO label is the most common dealer trap on used luxury — see gotcha (m) in SKILL.md heads-up block.

#### 3.7 Pricing dynamics — luxury negotiation

Luxury dealers operate differently from mainstream:

- **Sticker rarely budges much** — dealers see MSRP - 4-7% on most volume luxury vehicles, MSRP - 0-3% on performance variants and limited allocations.
- **Lease incentives are MORE aggressive than purchase incentives** — captive lease cash $2,500-$7,500 typical on volume luxury (BMW 3-series, MB GLC, Audi Q5); purchase cash often $500-$2,000. The captive prefers to retain customer for next lease (60-65% lease share = future customer).
- **First-time-buyer programs** — College Grad ($500-$1,500), Military ($500-$1,500), Loyalty / Conquest ($500-$2,000). These stack with lease cash.
- **MSDs (Multiple Security Deposits)** — BMW / Mercedes / Audi all offer; can drop effective MF by 0.00040-0.00080 (~ 1% APR equivalent). See `lease_playbook.md` § 6.
- **Service plan negotiation** — Audi Care ($750-$1,200), BMW Ultimate Care+ ($1,800), MB Star Service plans — all are negotiable at signing; never pay sticker on a service plan.

**Phase 6 luxury counter approach**: Focus on lease incentive stack + MSDs + loyalty stack, NOT on sticker discount. The path to lower OTD on luxury is through captive lease incentives, not through direct sticker discount.

#### 3.8 Entry-luxury / "halo" models with high markup

Mercedes CLA / GLA, Audi A3 / Q3, BMW 2-Series / X1, Lexus IS / NX / UX, Acura ILX / RDX, Infiniti Q50 / QX50, Cadillac CT4 / XT4, Lincoln Corsair / Nautilus, Genesis G70 / GV70 — these are designed as "first luxury car" hooks with high invoice-to-MSRP margin to feed the captive's future lease pipeline.

- Dealer margin: 8-12% on these (vs 4-6% on volume models)
- Lease cash on entry-luxury: aggressive ($2,000-$3,500)
- Conversion-to-mid-luxury at end of first lease: 30-40% upgrade rate
- Buyer-side trap: leaving with a $48k OTD on a $42k MSRP entry-luxury sedan because of high dealer-side margin + add-ons stack

Phase 6 counter for entry-luxury: aggressive cross-bid (4+ dealers); MSRP - 8% target reasonable.

### 4. Sub-Axes — Ultra-Luxury / Exotic / High-End Performance

These tiers require separate playbooks not covered here in depth. Documented for routing only.

#### 4.1 Ultra-luxury (>$200k MSRP segment)

- **Porsche** (911, Cayenne S/Turbo, Panamera Turbo, Taycan) — base Porsche near luxury (Macan / 718 = pure luxury); top-trim Porsches (Cayenne Turbo GT, Taycan Turbo GT, 911 Turbo S, 911 GT3 RS) are ultra-luxury. Demand >> supply on allocations; ADM common.
- **Maserati** (Quattroporte, Levante, Granturismo) — heavy depreciation; mostly used market.
- **Bentley** (Continental, Bentayga, Flying Spur) — ultra-luxury entry $250k+; lease 60-70% of sales.
- **Rolls-Royce** (Ghost, Phantom, Cullinan, Spectre) — $400k-$600k+; bespoke / commission model.
- **Aston Martin** (DB12, DBX, Vantage) — $190k-$285k; treated as luxury+.
- **McLaren** (most are exotic, GT4 is GT-touring on lease).
- **Lamborghini Urus** (only Lamborghini SUV; $230k-$300k+ MSRP, $400k+ with options).

**Skill workflow modifications**: Allocations matter more than negotiation. Phase 3 routing prioritizes dealers with confirmed in-bound allocations, not just inventory. Phase 6 negotiation often = "what's available" + flat MSRP, no discount; counter on options package only.

#### 4.2 Exotic (out of scope)

- Ferrari (all models) — not sold via standard dealer process; allocation by relationship; cannot order one without prior Ferrari ownership for many models.
- Lamborghini (Huracán, Revuelto) — limited dealer network; allocation by relationship.
- McLaren (720S, P1) — limited.

For these, the standard skill workflow does NOT apply. Buyer should engage a marque specialist / brand ambassador. Do NOT attempt to cross-bid Ferrari dealers.

#### 4.3 High-end performance (gray area)

- Corvette (Stingray, Z06, ZR1, E-Ray) — $70k-$160k MSRP; often ADM'd; allocation-driven on Z06 / ZR1.
- Nissan GT-R (R35 last MY 2024) — out of production; used market only.
- Ford Mustang Dark Horse / GT500 — performance variants, sometimes ADM.
- Camaro ZL1 / SS / SS 1LE — discontinued 2024; used market.
- Cadillac CT5-V Blackwing / CT4-V Blackwing — performance V variants; limited allocation.
- Dodge Challenger Hellcat / Demon / SRT — discontinued 2024 ICE; used market only.
- Toyota GR Corolla / GR86 / Supra — performance Toyota; volume-limited, often near MSRP.

**Skill workflow modifications**: Cross-bid 2-3 dealers max in radius (limited allocation = less to bid against); accept MSRP-clean = win; ADM-laden = walk to next allocation. Patience often wins (allocations refresh quarterly).

### 5. Phase 1 Heads-Up for HD / Commercial / Luxury Buyers

When buyer's Phase 1 input includes:

- **HD pickup** (F-250+, RAM 2500+, GM 2500HD+): surface diesel-emissions-check heads-up + CDL/GCWR check + commercial-vs-personal registration question.
- **Commercial van**: surface § 179 deduction availability + fleet desk vs internet sales routing + upfit requirements.
- **Luxury car**: surface lease-vs-purchase default + service plan included status (Cadillac / Genesis vs BMW / MB / Audi) + fake-CPO label warning if used.
- **Ultra-luxury / exotic**: surface allocation-not-negotiation context + flag that ADM is structural in this tier + suggest brand specialist not standard workflow.

### 6. Quick Reference — Phase 9 Close-Day Routing

| Buyer type | Add to standard cash/financing/trade close-day sub-checklist |
|---|---|
| **HD pickup buyer** | DEF tank, emissions verification, 5th-wheel prep, brake controller, commercial-vs-personal plate decision |
| **Commercial van buyer** | Upfit timeline confirmation, commercial plates ordered, § 179 paperwork (CPA copy), fleet manager handoff to service desk |
| **Luxury car buyer (loan/cash)** | Service plan locked-in (not add-on at close), tech walkthrough scheduled (Genius / Concierge), CPO certificate received if used, brand app pre-installed and activated |
| **Luxury car buyer (lease)** | MSDs paid (refundable; track in records), GAP confirmed included, mileage allowance matches buyer's actual driving estimate (`lease_playbook.md` § 10), MF buy-rate verified one final time |
| **Ultra-luxury buyer** | Brand specialist handoff at delivery; allocation paperwork verified; PPI on used not via standard mobile inspector (use marque specialist instead) |

### 7. References and Cross-Links

- Part 1 above — light-duty pickups (F-150, RAM 1500, Silverado 1500, Tundra, Tacoma).
- `lease_playbook.md` — luxury lease arbitrage details, MSDs, MF markup.
- `ev_buyer_playbook.md` — Cadillac LYRIQ, Lincoln Star EVs, electric Sprinter, electric F-150 Lightning HD use case.
- `negotiation_playbook.md` — counter math (general).
- `outreach_strategy.md` — Phase 4 fleet-desk routing for commercial buyers.
- `state_fees.md` — state-specific commercial / HD plate fee math.

last_verified: 2026-05-18
