# Scenario 4: New Hyundai Ioniq 5 EV, central Texas, cash with $7,500 POS credit

## The buyer

The buyer is a mechanical engineer in central Texas (<ZIP>). They are
EV-curious and a first-time EV buyer. Their current car is a 2019 Mazda3
which they plan to keep as backup — no trade.

## The target

A **new** 2025 Hyundai Ioniq 5, SEL or Limited trim. AWD strongly preferred
(320 hp dual motor, 260-mile range vs 303 for the RWD SEL — the buyer accepts
the 43-mile range cost). Colors: Atlas White, Cyber Gray, or Phantom Black.
Must-haves: heated seats, V2L (vehicle-to-load) outlet, Hyundai SmartSense
suite, and 800V charging architecture (DC fast charge 10→80% in under 18
minutes).

## The constraints

- Budget: $42,000 to $48,000 OTD **after** the federal $7,500 EV credit at
  point of sale (so effective gross OTD up to ~$55,500).
- Walk-away ceiling: $50,000 OTD post-credit hard stop.
- Geographic radius: 100 miles of <ZIP> — the Austin-San Antonio corridor.
- Payment: cash, cashier's check. The buyer **intends to take
  the $7,500 as a point-of-sale rebate** transferred to the dealer (the
  dealer must be IRS-registered for this to work).
- Timeline: six weeks (close by 2026-06-29).
- Charging: 240V/40A home charger pre-installed by Qmerit, $1,200 (paid).

## The ask

The buyer wants the workflow to:

1. Confirm dealer eligibility for the $7,500 POS transfer — the dealer must
   be registered on IRS Energy Credits Online **before** the buyer signs.
   Verification in writing, not verbal.
2. Map the EV incentive stack: federal $7,500 (§30D) + state (Texas has no
   state EV credit + a $200/yr EV registration premium) + utility (local
   utility charger rebate $1,200 retroactive possibility) + manufacturer
   (Hyundai Customer Cash, typically $1,500-$3,000).
3. Catch "EV Prep Fee" / "Battery Conditioning Fee" / "Charge Cable Fee" /
   "EV Delivery Setup" — these are ADM-equivalent line names that need to
   be killed mechanically.
4. Flag the NACS-vs-CCS1 transition: mid-MY 2025 Ioniq 5 switched to native
   NACS; pre-switchover VINs need a Hyundai-supplied adapter for Tesla
   Supercharger access.
5. Acknowledge that the buyer, as a cash buyer, cannot use the Section 45W
   commercial-vehicle credit that captive lessors pass through on leases —
   it is a structural disadvantage of the cash path on EVs.

## What makes this scenario interesting

- This is the **first EV case**. The skill's Phase 1 EV gate was a 3-field
  placeholder before this scenario. Stress-testing surfaced that a real EV
  branch needs 6 structured fields, not 3.
- Federal §30D mechanics are intricate: vehicle assembly location, MSRP
  cap ($80k for SUVs / $55k for cars — Ioniq 5 classified as SUV), buyer
  MAGI cap ($150k single / $300k joint), POS transfer mechanic, dealer IRS
  registration, recapture risk if MAGI exceeds the cap.
- Texas is one of the cleanest fee structures in the U.S. (6.25% state
  only, no local stacking, $150 doc cap) but EVs add a $200/yr registration
  premium under SB 505.
- Lease-vs-cash creates a structural cash-buyer disadvantage on EVs that
  has no easy fix — captive lessors capture the Section 45W $7,500
  commercial-vehicle credit on leases regardless of MSRP cap and MAGI cap,
  while cash buyers are gated by both.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md) — Phases 1, 2, 6.
- [ev-buyer-helper](../skills/ev-buyer-helper/SKILL.md) — §30D mechanics,
  POS transfer, IRS registration check, NACS-vs-CCS1, range planning,
  used-EV SoH thresholds, EV-specific dealer tactics.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md) — Texas detail
  stub (6.25% state-only, $150 doc cap, $33 title, $200/yr EV premium).
- [lease-vs-cash-analyzer](../skills/lease-vs-cash-analyzer/SKILL.md) —
  Section 45W commercial-credit gap on the cash path.
- [otd-calculator](../skills/otd-calculator/SKILL.md) — gross + net
  post-credit math.
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md) —
  counter with the EV-specific ADM kill list.

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1 — fired the EV branch of the buyer-type router.
   Captured 6 structured fields (home L2 charging + amperage / federal
   $7,500 eligibility incl. assembly + MSRP cap + MAGI + POS transfer +
   dealer IRS reg + recapture risk / state-utility rebate / range minimum /
   DC fast charge + NACS-vs-CCS1 + adapter for the VIN / used-EV SoH).
2. **ev-buyer-helper** — produced the §30D walkthrough including the
   dealer-IRS-registration must-do as a Phase 6 pre-deposit gate.
3. **state-fee-lookup** — Texas detail (6.25% state-only, $150 doc cap,
   $33 title, $200/yr EV registration premium under SB 505, 2025
   inspection elimination for non-commercial vehicles).
4. **lease-vs-cash-analyzer** — flagged the Section 45W structural gap:
   captive lessors capture $7,500 commercial credit on leases regardless
   of MSRP and MAGI caps; cash buyer cannot.
5. **orchestrator** Phase 2 — baseline produced with REAL/SYNTHESIZED
   provenance; trim MSRP ladder synthesized pending live Build & Price
   pull.
6. **dealer-reply-drafter** — counter to a synthetic sales rep at a
   local Hyundai dealer. Quote contained $895 "EV Prep Fee" (ADM-equivalent).

### Artifacts produced

- `criteria.md` with the 6-field EV sub-block + heads-up trio (EV Prep
  Fee detection / AWD inventory tighter than RWD / 6-week timeline
  comfortable).
- `ioniq5-tx-baseline.md` with trim MSRP ladder, Hyundai Q2 2026 incentive
  stack, federal $7,500 mechanics, TX fee structure, worked OTD ($45,353
  net post-credit on SEL AWD inside $42-48k target).
- `p6_counter_to_carlos.md` — paste-ready counter, EV Prep Fee killed
  with one anchored sentence; IRS registration verified in writing as a
  separate ask.

### Gotchas and Critical Rules that fired

- **Critical Rule #7** — all baseline rows marked SYNTHESIZED for this
  test run; would be REAL with a live hyundaiusa.com Build & Price pull
  before send.
- **Gotcha D9 (ADM kill list) with EV-specific line names** — fired on
  "EV Prep Fee" $895. Counter sentence: "Please remove the EV Prep Fee;
  Hyundai PDI covers battery conditioning, charge cable, and delivery
  setup. The competitor in our radius at MSRP-or-below confirms this is
  not market." Sub-rule applied: single ask, single round, no coupling.
- **§30D dealer registration gate** — flagged before deposit. If the
  dealer cannot produce an IRS Energy Credits Online registration ID in
  writing, walk to one of the 15+ alternate dealers in radius.
- **Texas state-fee leak audit** — clean. No local stacking, no tire
  fee, no battery fee, no NJ-style supplemental titling, no NY MCTD.
  Doc at $150 already at statutory cap.

### What this scenario surfaced for the skill

Three concrete deltas landed (the EV branch was previously the largest
single gap in the skill):

- **`ev_buyer_playbook.md` (NEW reference file)** — 10 sections covering
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
- **EV-specific ADM line names added to `outreach_strategy.md`** — EV
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
EVs, the federal §30D detail will feel dense — skim the outcome and
move on. If you do buy EVs, this scenario surfaced the §30D POS
transfer mechanics gap that became the entire `ev-buyer-helper` skill.
Read after scenario 3.
