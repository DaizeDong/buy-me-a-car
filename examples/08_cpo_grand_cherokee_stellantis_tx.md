# Scenario 8: CPO Jeep Grand Cherokee (Stellantis SPOTiCAR), Texas, cash

## The buyer

The buyer is an oil-and-gas field engineer in central Texas (<ZIP>).
Second car, growing family, wants a three-row-capable SUV with real
warranty backing. They are specifically shopping the dealer's
**certified pre-owned** inventory because they want an OEM-backed
warranty on a used vehicle. Cash via cashier's check. No trade, no
financing, no lease.

## The target

A Stellantis CPO (SPOTiCAR) **Jeep Grand Cherokee**, Limited or Overland
trim, 2021-2023 model year, under 60,000 miles. 4x4 strongly preferred.
Colors: Bright White, Diamond Black, or Velvet Red. Must-haves: leather,
Uconnect 5, blind-spot monitoring, backup camera, and, the whole point
of the scenario, **active SPOTiCAR certification** with the
7yr/100k powertrain warranty intact. The buyer is at a CJDR
(Chrysler-Jeep-Dodge-Ram) dealer's used lot, so SPOTiCAR enrollment is
available.

## The constraints

- Budget: $30,000 to $36,000 **out-the-door**.
- Walk-away ceiling: $37,500 OTD, OR any "CPO" claim the dealer cannot
  back with a certificate at close.
- Geographic radius: 75 miles of <ZIP>, covers multiple CJDR parent
  groups in the central-Texas corridor.
- Payment: cash, cashier's check.
- Timeline: three to four weeks.

## The ask

The buyer wants the buy-me-a-car workflow to:

1. Run **Stellantis-specific CPO eligibility** (not Subaru/Honda
   cross-applied): confirm the target falls inside the top-tier
   "Certified" window (5 model years or newer, under 75,000 mi) versus the
   lower "CPO Go" tier (6-10 MY, 75k-120k mi), per the SPOTiCAR two-tier
   structure.
2. Compute the **Stellantis embedded value correctly**, it is
   **age-sensitive** because the powertrain clock runs from the
   **original in-service date**, not the CPO purchase date. Do NOT
   cross-apply the Subaru ($2,000-$2,500) or Honda ($1,200-$1,800)
   embedded value.
3. Verify the **in-service date** and compute remaining powertrain term,
   the load-bearing check on Stellantis CPO. A 2021 unit certified in
   2026 may have far less powertrain coverage left than the "7yr/100k"
   label implies.
4. Build a Texas OTD with the **real TX doc-cap truth ($225)** and the
   rest of the TX fee stack, no invented line items.
5. Counter a synthetic dealer quote that prices a meaningful "CPO
   premium" on the unit, anchoring on the Stellantis embedded-value range
   rather than accepting the dealer's CPO markup at face value.

## What makes this scenario interesting

- This is the **first Stellantis CPO scenario** and the first to exercise
  `stellantis_cpo_program.md`. SPOTiCAR is a single multi-brand program
  (Chrysler / Jeep / Dodge / Ram / Fiat) with a **two-tier** structure
  and the **most age-sensitive embedded value** of any CPO program in the
  refs, because the powertrain term runs from in-service date.
- The **in-service-date trap** is the program's biggest value trap:
  it is "entirely possible to buy a CPO unit that only has the
  3-month/3,000-mile Maximum Care comprehensive layer remaining." The
  remaining-powertrain-term computation is mandatory before treating the
  warranty as a real benefit.
- SPOTiCAR has the **widest eligibility window** (10 MY / 120k mi outer
  bound) but the **weakest comprehensive layer** (only 3mo/3k Maximum
  Care vs Honda's 1-2 yr), so the embedded-value leverage is materially
  lower than Subaru/Honda and must not be over-claimed.
- Texas has one of the cleanest fee structures in the U.S., and the
  scenario pins the **real 2024 doc-cap truth of $225** (raised from
  $150, effective 2024-07-11) so the OTD math uses the current safe-harbor
  amount, not the stale $150.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md), Phases 1, 2, 6.
- [cpo-eligibility](../skills/cpo-eligibility/SKILL.md), Stellantis
  SPOTiCAR two-tier eligibility, age-sensitive embedded value, in-service
  date / remaining-powertrain-term computation (delegates to
  `stellantis_cpo_program.md`).
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md), Texas detail
  (6.25% state, **$225 doc cap**, $33 title, $51 reg).
- [otd-calculator](../skills/otd-calculator/SKILL.md), TX OTD with the
  real doc-cap value.
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md),
  counter anchoring on the Stellantis embedded-value range against a
  dealer CPO premium.

> **Not exercised (deliberately):** `lease-vs-cash-analyzer` (cash),
> `trade-in-valuator` (no trade), `payment-method-decider` (cash, no
> financing), `ev-buyer-helper` (ICE).

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1, captured the 9-field core with the
   CPO-required sub-fields (target is CPO-only; certification must be
   active and certificate-backed at close).
2. **state-fee-lookup**, Texas detail from `data/state_fees.json`:
   state tax **6.25%** (`tax_state: 0.0625`), **doc cap $225**
   (`doc_cap: 225`, `doc_cap_effective_date: 2024-07-11`), **title $33**
   (`title: 33`), **reg/yr $51** (`reg_1yr: 51`). Confirmed TX
   `verified: true` with `source_url` to the Texas Comptroller + OCCC.
   `does_not_have` row confirmed no state income tax, no local stacking
   above 1.75%, no TAVT/HUT.
3. **cpo-eligibility** -> **Stellantis SPOTiCAR** branch
   (`stellantis_cpo_program.md`): a 2021-2023 Grand Cherokee under 60k mi
   is **top-tier "Certified"** (5 MY or newer AND under 75k mi). Computed
   embedded value at the Stellantis top-tier range **~$1,000-$1,800**
   (NOT the Subaru/Honda figures). Flagged the in-service-date check as a
   Phase 9 pre-deposit gate.
4. **otd-calculator**, gross TX OTD on a ~$33,000 CPO sale: sale +
   6.25% TX tax + $225 doc + $33 title + $51 reg, inside the $36k ceiling.
5. **dealer-reply-drafter**, counter to a synthetic CJDR sales rep whose
   quote tacked a "$2,400 CPO Certification Premium" on top of the
   non-CPO comp.

### Artifacts produced

- `criteria.md`, Phase 1 core 9 fields + a CPO sub-block (active
  certification required, in-service-date verification gate, tier
  confirmation, certificate-at-close walk condition).
- `grand-cherokee-tx-cpo-baseline.md`, trim ladder, regional CPO vs
  non-CPO asking spreads (REAL/SYNTHESIZED tagged), the Stellantis
  top-tier embedded-value anchor ($1,000-$1,800), and the worked TX OTD.
- `p6_cpo_counter.md`, paste-ready counter under 12 lines: the
  $2,400 CPO premium exceeds the Stellantis top-tier embedded value of
  $1,000-$1,800; counter demands the premium be reset into that band,
  the in-service date in writing, and the SPOTiCAR certificate +
  125-point inspection report at close.

### Numbers and their provenance

Every dollar figure traces to a truth source, no invented fees:

- TX state tax 6.25%, doc cap $225, title $33, reg $51:
  `data/state_fees.json` -> states[] -> TX (`tax_state` 0.0625,
  `doc_cap` 225, `title` 33, `reg_1yr` 51). TX is
  `verified: true` with `source_url`
  (comptroller.texas.gov + occc.texas.gov) and
  `source_verified_date: 2026-06-22`, this is a ground-truth-verified
  record, the strongest provenance in the fixture set.
- TX doc cap $225 effective 2024-07-11 (raised from $150), OCCC
  presumed-reasonable safe-harbor not a hard statutory ceiling:
  `data/state_fees.json` TX `doc_cap_effective_date`,
  `doc_cap_statute`, `doc_cap_history`.
- Stellantis top-tier embedded value $1,000-$1,800 (and CPO Go
  $300-$800), powertrain 7yr/100k from in-service, 3mo/3k Maximum Care,
  $0 powertrain deductible, $150 transfer fee, two-tier age/mileage
  thresholds (top tier 5 MY / 75k mi; outer bound 10 MY / 120k mi):
  `stellantis_cpo_program.md` (Eligibility Criteria, Coverage Granted,
  Embedded Value sections).

> **CPO embedded value is a range, not a published OEM figure:**
> `stellantis_cpo_program.md` flags as UNVERIFIED that Stellantis
> publishes any single canonical "MSRP value of CPO." The $1,000-$1,800
> top-tier figure is derived from Mopar/FlexCare quote data, used as a
> negotiating anchor, not invented and not presented as an OEM list price.

### Gotchas and Critical Rules that fired

- **Critical Rule #1 (plain ASCII)**, counter contains no em-dashes,
  no smart quotes, no markdown bold.
- **Critical Rule #7 (REAL-tagged citations only)**, counter cites only
  REAL CPO-vs-non-CPO asking comps by URL + timestamp; synthesized rows
  stay internal.
- **Stellantis embedded value NOT cross-applied**, the workflow used the
  Stellantis-specific $1,000-$1,800 top-tier range, explicitly NOT the
  Subaru $2,000-$2,500 or Honda $1,200-$1,800 figures. (Load-bearing
  check the fixture verifies.)
- **In-service-date gate**, remaining-powertrain-term computed from the
  in-service date before treating the 7yr/100k warranty as a real
  benefit; certificate + 125-point inspection report demanded at close.
- **CPO-premium-exceeds-embedded-value counter**, the synthetic
  $2,400 premium is above the top-tier embedded-value band, so the
  counter demands it be reset into the $1,000-$1,800 range rather than
  meeting in the middle.
- **TX doc-cap currency**, OTD used the current $225 safe-harbor, not
  the stale $150; an old-cap quote would be a state-fee-leak leverage
  point.

### What this scenario surfaced for the skill

The Stellantis CPO program existed as a reference file but had no
end-to-end fixture. This scenario pins:

- The `cpo-eligibility` -> Stellantis branch as an explicit, testable
  route distinct from the Subaru/Honda branches.
- The **age-sensitive embedded value** computation (in-service-date
  clock) as the load-bearing Stellantis CPO check, the most common way a
  generic agent over-values Stellantis CPO is by cross-applying a
  Subaru/Honda figure or ignoring the in-service date.
- The **two-tier (Certified vs CPO Go)** eligibility test against real
  5MY/75k and 10MY/120k thresholds.
- The **TX $225 doc-cap truth** (verified record) as the OTD anchor,
  guarding against stale-$150 quotes.

### Reading takeaway

Read this after scenario 3 (the Honda CPO baseline) for the cleanest
cross-program contrast: Honda CPO embedded value is fairly uniform, while
Stellantis CPO is sharply age-sensitive because the powertrain clock runs
from in-service date. If your local copy quotes a Subaru/Honda embedded
value on a Stellantis unit, or skips the in-service-date computation,
that is a CPO regression. The TX OTD here is also the cleanest
verified-data fee build in the set.
