# Scenario 4: New Hyundai Ioniq 5 EV, central Texas, cash (federal $7,500 POS credit, HISTORICAL)

> ## ⚠️ CRITICAL, FEDERAL EV CREDITS HAVE ENDED (as of 2026-06)
>
> This scenario was authored when the federal $7,500 §30D point-of-sale credit was
> live. The One Big Beautiful Bill Act (OBBBA / Public Law 119-21, signed 2025-07-04)
> **terminated all three federal clean-vehicle credits** (§30D $7,500 new, §25E $4,000
> used, §45W $7,500 commercial/lease pass-through) for any vehicle **acquired after
> 2025-09-30**. The buyer here closes 2026-06-29, so **none of the federal credit
> applies**: there is no $7,500 POS transfer, no "net post-credit" OTD, and no §45W
> lease arbitrage. The federal lines below are retained as **HISTORICAL reference** and
> must NOT be counted in OTD / net-price math. The only live incentive layer for a 2026
> purchase is **state/local rebates** (where still funded) and manufacturer cash, and
> Texas has no state EV rebate, so this buyer's 2026 net OTD equals the gross OTD.
>
> Sources: [IRS FAQ Fact Sheet 2025-05 (modification of §§25C/25D/25E/30C/30D/45L/45W/179D under OBBB)](https://www.irs.gov/newsroom/faqs-for-modification-of-sections-25c-25d-25e-30c-30d-45l-45w-and-179d-under-public-law-119-21-139-stat-72-july-4-2025-commonly-known-as-the-one-big-beautiful-bill-obbb);
> [IRS, accelerated termination of energy provisions under OBBB](https://www.irs.gov/newsroom/treasury-irs-issue-faqs-to-address-the-accelerated-termination-of-several-energy-provisions-under-obbb).

## The buyer

The buyer is a mechanical engineer in central Texas (<ZIP>). They are
EV-curious and a first-time EV buyer. Their current car is a 2019 Mazda3
which they plan to keep as backup, no trade.

## The target

A **new** 2025 Hyundai Ioniq 5, SEL or Limited trim. AWD strongly preferred
(320 hp dual motor, 260-mile range vs 303 for the RWD SEL, the buyer accepts
the 43-mile range cost). Colors: Atlas White, Cyber Gray, or Phantom Black.
Must-haves: heated seats, V2L (vehicle-to-load) outlet, Hyundai SmartSense
suite, and 800V charging architecture (DC fast charge 10→80% in under 18
minutes).

## The constraints

- Budget: $42,000 to $48,000 OTD. (As originally authored this was "after the
  federal $7,500 POS credit"; that credit is TERMINATED for a 2026 purchase, so
  the budget is now a straight gross-OTD figure with no federal offset.)
- Walk-away ceiling: $50,000 OTD hard stop. (Originally "post-credit"; no federal
  credit applies in 2026, so this is a plain gross-OTD ceiling.)
- Geographic radius: 100 miles of <ZIP>, the Austin-San Antonio corridor.
- Payment: cash, cashier's check. (HISTORICAL: the buyer originally intended to
  take the $7,500 as a point-of-sale rebate transferred to an IRS-registered
  dealer. §30D is terminated for vehicles acquired after 2025-09-30, so for this
  2026 close there is no POS transfer and no dealer-registration requirement.)
- Timeline: six weeks (close by 2026-06-29).
- Charging: 240V/40A home charger pre-installed by Qmerit, $1,200 (paid).

## The ask

The buyer wants the workflow to:

1. (HISTORICAL, no longer applicable in 2026.) Originally: confirm dealer
   eligibility for the $7,500 POS transfer, with IRS Energy Credits Online
   registration verified in writing before signing. §30D is terminated for
   vehicles acquired after 2025-09-30, so there is no POS transfer to confirm
   for this 2026 close.
2. Map the EV incentive stack for 2026: the federal $7,500 (§30D) layer is
   TERMINATED and contributes $0. Texas has no state EV rebate (and adds a
   $200/yr EV registration premium). The only live offsets are utility (local
   utility charger rebate $1,200 retroactive possibility) + manufacturer
   (Hyundai Customer Cash, typically $1,500-$3,000).
3. Catch "EV Prep Fee" / "Battery Conditioning Fee" / "Charge Cable Fee" /
   "EV Delivery Setup", these are ADM-equivalent line names that need to
   be killed mechanically.
4. Flag the NACS-vs-CCS1 transition: mid-MY 2025 Ioniq 5 switched to native
   NACS; pre-switchover VINs need a Hyundai-supplied adapter for Tesla
   Supercharger access.
5. (HISTORICAL.) Originally: acknowledge that the buyer, as a cash buyer,
   could not use the Section 45W commercial-vehicle credit that captive lessors
   passed through on leases, a structural disadvantage of the cash path on EVs.
   §45W is now terminated for vehicles acquired after 2025-09-30, so the lease
   pass-through no longer exists and this cash-vs-lease gap is closed.

## What makes this scenario interesting

- This is the **first EV case**. The skill's Phase 1 EV gate was a 3-field
  placeholder before this scenario. Stress-testing surfaced that a real EV
  branch needs 6 structured fields, not 3.
- Federal §30D mechanics were intricate (HISTORICAL, credit terminated
  2025-09-30, does not apply to this 2026 close): vehicle assembly location, MSRP
  cap ($80k for SUVs / $55k for cars, Ioniq 5 classified as SUV), buyer
  MAGI cap ($150k single / $300k joint), POS transfer mechanic, dealer IRS
  registration, recapture risk if MAGI exceeds the cap.
- Texas is one of the cleanest fee structures in the U.S. (6.25% state
  only, no local stacking, $150 doc cap) but EVs add a $200/yr registration
  premium under SB 505.
- Lease-vs-cash used to create a structural cash-buyer disadvantage on EVs
  (HISTORICAL, §45W terminated 2025-09-30): captive lessors captured the Section
  45W $7,500 commercial-vehicle credit on leases regardless of MSRP cap and MAGI
  cap, while cash buyers were gated by both. With §45W gone, that gap no longer
  exists for a 2026 purchase.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md), Phases 1, 2, 6.
- [ev-buyer-helper](../skills/ev-buyer-helper/SKILL.md), §30D mechanics,
  POS transfer, IRS registration check, NACS-vs-CCS1, range planning,
  used-EV SoH thresholds, EV-specific dealer tactics.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md), Texas detail
  stub (6.25% state-only, $150 doc cap, $33 title, $200/yr EV premium).
- [lease-vs-cash-analyzer](../skills/lease-vs-cash-analyzer/SKILL.md) ,
  Section 45W commercial-credit gap on the cash path (HISTORICAL; §45W terminated
  2025-09-30, gap no longer exists).
- [otd-calculator](../skills/otd-calculator/SKILL.md), gross + net
  post-credit math (HISTORICAL; in 2026 net OTD equals gross OTD, no federal credit).
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md) ,
  counter with the EV-specific ADM kill list.

---

## Outcome

> The Outcome below records the ORIGINAL run, authored while §30D/§25E/§45W were
> live. All federal-credit figures (the "$7,500 POS", "net post-credit" OTD, and
> the "$45,353 net" worked number) are HISTORICAL and must not be reused: for a
> 2026 TX close the federal offset is $0 and net OTD equals gross OTD.

### Skill firing order

1. **orchestrator** Phase 1, fired the EV branch of the buyer-type router.
   Captured 6 structured fields (home L2 charging + amperage / federal
   $7,500 eligibility incl. assembly + MSRP cap + MAGI + POS transfer +
   dealer IRS reg + recapture risk / state-utility rebate / range minimum /
   DC fast charge + NACS-vs-CCS1 + adapter for the VIN / used-EV SoH).
2. **ev-buyer-helper**, produced the §30D walkthrough including the
   dealer-IRS-registration must-do as a Phase 6 pre-deposit gate.
3. **state-fee-lookup**, Texas detail (6.25% state-only, $150 doc cap,
   $33 title, $200/yr EV registration premium under SB 505, 2025
   inspection elimination for non-commercial vehicles).
4. **lease-vs-cash-analyzer**, flagged the Section 45W structural gap:
   captive lessors capture $7,500 commercial credit on leases regardless
   of MSRP and MAGI caps; cash buyer cannot.
5. **orchestrator** Phase 2, baseline produced with REAL/SYNTHESIZED
   provenance; trim MSRP ladder synthesized pending live Build & Price
   pull.
6. **dealer-reply-drafter**, counter to a synthetic sales rep at a
   local Hyundai dealer. Quote contained $895 "EV Prep Fee" (ADM-equivalent).

### Artifacts produced

- `criteria.md` with the 6-field EV sub-block + heads-up trio (EV Prep
  Fee detection / AWD inventory tighter than RWD / 6-week timeline
  comfortable).
- `ioniq5-tx-baseline.md` with trim MSRP ladder, Hyundai Q2 2026 incentive
  stack, federal $7,500 mechanics (HISTORICAL, terminated 2025-09-30), TX fee
  structure, worked OTD ($45,353 net post-credit on SEL AWD, HISTORICAL; with
  no federal credit in 2026 the SEL AWD net OTD equals its gross OTD of ~$52,853).
- `p6_counter_to_carlos.md`, paste-ready counter, EV Prep Fee killed
  with one anchored sentence; IRS registration verified in writing as a
  separate ask.

### Gotchas and Critical Rules that fired

- **Critical Rule #7**, all baseline rows marked SYNTHESIZED for this
  test run; would be REAL with a live hyundaiusa.com Build & Price pull
  before send.
- **Gotcha D9 (ADM kill list) with EV-specific line names**, fired on
  "EV Prep Fee" $895. Counter sentence: "Please remove the EV Prep Fee;
  Hyundai PDI covers battery conditioning, charge cable, and delivery
  setup. The competitor in our radius at MSRP-or-below confirms this is
  not market." Sub-rule applied: single ask, single round, no coupling.
- **§30D dealer registration gate** (HISTORICAL, no longer fires in 2026) ,
  originally flagged before deposit; if the dealer could not produce an IRS Energy
  Credits Online registration ID in writing, walk to one of the 15+ alternate
  dealers in radius. With §30D terminated, there is no POS transfer and thus no
  dealer-registration gate for a current purchase.
- **Texas state-fee leak audit**, clean. No local stacking, no tire
  fee, no battery fee, no NJ-style supplemental titling, no NY MCTD.
  Doc at $150 already at statutory cap.

### What this scenario surfaced for the skill

Three concrete deltas landed (the EV branch was previously the largest
single gap in the skill):

- **`ev_buyer_playbook.md` (NEW reference file)**, 10 sections covering
  federal §30D credit, federal §25E used-EV credit, state and local EV
  rebate matrix (CA / NY / NJ / CO / IL / MA / CT / OR / TX / PA / MD /
  WA / VT / DE / RI with Nov 2025 funding posture), charging
  considerations (home L2, NACS vs CCS1, public DC fast-charge network
  comparison, 800V vs 400V), range planning (EPA vs real-world delta,
  AWD-vs-RWD trade-off), battery health for used EVs (SoH thresholds +
  warranty standards), EV depreciation patterns, EV-specific dealer
  tactics (EV Prep Fee / Battery Conditioning Fee / Charge Cable Fee /
  EV Delivery Setup Fee + Section 45W lease-vs-cash + IRS registration
  as leverage point + "EV in transit" stall), EV-specific Phase 6
  checklist, EV-specific walk conditions.
- **EV-specific ADM line names added to `outreach_strategy.md`**, EV
  Prep Fee / Battery Conditioning Fee / Charge Cable Fee / EV Delivery
  Setup Fee / High-Voltage Inspection Fee / EV Activation Fee. Combines
  with the ICE/hybrid kill list (Market Adjustment / Hybrid Premium /
  Allocation Fee / Protection Plus).
- **Texas detail stub** at CT/CA depth (6.25% state-only, $150 doc cap,
  $33 title, base reg + $200/yr EV premium under TX Transportation
  Code § 502.360, 2025 inspection elimination). Plus TX→OK / TX→LA /
  TX→NM cross-state titling rows; Texas has no structural cross-state
  arbitrage advantage (already among the cleanest in the U.S.).

### Reading takeaway

This scenario is the most domain-heavy of the five. If you do not buy
EVs, the federal §30D detail will feel dense, skim the outcome and
move on. If you do buy EVs, this scenario surfaced the §30D POS
transfer mechanics gap that became the entire `ev-buyer-helper` skill.
Read after scenario 3.
