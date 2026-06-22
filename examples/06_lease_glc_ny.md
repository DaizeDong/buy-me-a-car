# Scenario 6: New Mercedes-Benz GLC 300 lease, New York, 36-month / 12k

## The buyer

The buyer is a hospital administrator in the New York City suburbs
(<ZIP>). They have leased twice before (both Audi) and want to lease
again rather than buy. They turn cars over every three years, drive
about 11,000 miles a year, and want the option to walk away at lease
end. Tier 1+ credit. No trade, no EV interest, no financing of a
purchase.

## The target

A **new** 2026 Mercedes-Benz GLC 300 4MATIC, Premium trim with the
heated-seats / panoramic-roof / Burmester package. Colors: Polar White,
Selenite Grey, or Obsidian Black. Must-haves: 4MATIC AWD (NY winters),
MBUX, blind-spot assist, and the heated front seats. The GLC is the
volume luxury compact SUV in this segment and the buyer cross-shopped
the Audi Q5 and BMW X3, but lease economics on the GLC pencil out
because Mercedes-Benz Financial Services is running lease cash this
quarter.

## The constraints

- Budget: target effective monthly **$520-$580 all-in** (tax included),
  drive-off under $3,000.
- Walk-away ceiling: $620/mo all-in hard stop, OR any quote where the
  dealer refuses to disclose the buy-rate money factor.
- Geographic radius: 40 miles of <ZIP> — sweeps three MB dealer parent
  groups across NY and into NJ.
- Payment: **lease** through Mercedes-Benz Financial Services (MBFS).
  - Term: 36 months.
  - Mileage: 12k/yr (11k actual, small cushion).
  - Down: $0 cap-cost reduction beyond drive-off (per lease playbook
    section 11 default).
- Timeline: four weeks, close by month-end.

## The ask

The buyer wants the buy-me-a-car workflow to:

1. Confirm this is a lease (not finance, not cash) at Phase 1 and capture
   the six lease-specific sub-fields (annual miles / term / plan-after /
   down-payment posture / conversion-eligible? / pre-purchase miles?).
2. Score the lease on the five core fields (Cap Cost, Residual, Money
   Factor, Term, Mileage) and reject any quote missing one of them.
3. Handle the **New York lease tax mechanic correctly**: NY taxes the
   full sum-of-all-payments **up front at signing**, not per-monthly like
   NJ/CA. This is the single most-muffed lease number for a NY buyer and
   changes drive-off materially.
4. Demand the buy-rate money factor and cite the MBFS markup ceiling so
   the dealer cannot bury reserve in the MF.
5. Confirm the MBFS acquisition and disposition fees are at captive
   standard, not dealer-marked-up.

## What makes this scenario interesting

- This is the **first lease scenario** in the example set. Leasing was
  "already supported" by `lease-vs-cash-analyzer` and the
  `lease_playbook.md` reference, but had **zero worked end-to-end
  fixture** — this scenario closes that gap and gives the lease path a
  regression anchor.
- NY lease tax (lump-sum on sum-of-payments at signing) is structurally
  different from the NJ/CA tax-on-monthly default that the other examples
  implicitly assume. A workflow that silently applies tax-on-monthly to a
  NY lease understates drive-off by over a thousand dollars.
- The OTD-calculator is the **wrong tool** for a lease and must be
  suppressed — lease cost is depreciation + rent + tax, not
  sale + doc + title + reg + dealer fees. The orchestrator has to route
  to the lease monthly-payment formula instead.
- Mercedes-Benz Financial Services has a relatively high acquisition fee
  and the **highest disposition fee** among mainstream/luxury captives,
  so the lease-end cost posture matters at signing.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md) — Phases 1, 2, 6.
- [lease-vs-cash-analyzer](../skills/lease-vs-cash-analyzer/SKILL.md) —
  five-core-field scoring, MBFS captive rules, NY lease tax mechanic,
  buy-rate MF counter (delegates to `lease_playbook.md`).
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md) — New York
  detail (4% state base, $175 doc cap, $50 title, $100 reg) plus the
  NY-vs-NJ lease-tax-timing contrast for the cross-radius NJ dealers.
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md) — the
  lease-specific Phase 6 counter (buy-rate MF demand + cap-cost
  composition + acq/disposition verification).

> **Not exercised (deliberately):** `otd-calculator` (lease has no OTD
> stack — suppressed), `cpo-eligibility` (new car), `trade-in-valuator`
> (no trade), `ev-buyer-helper` (ICE).

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1 — fired the financing branch, then the
   "loan or lease?" sub-router resolved to **lease**. Captured the
   standard 9 fields + the 6 lease sub-fields (annual miles 12k / term
   36 / plan-after = return / down = $0 beyond drive-off /
   conversion-eligible = no (ICE) / pre-purchase miles = no, 11k actual
   under the 12k allowance).
2. **state-fee-lookup** — New York detail from `data/state_fees.json`:
   state base **4%** (`tax_state: 0.04`), local 4-4.875% on top, **doc
   cap $175** (`doc_cap: 175`), **title $50** (`title: 50`), **reg/yr
   $100** (`reg_1yr: 100`), **no EV reg surcharge**
   (`ev_reg_surcharge: null`). Flagged NY's `does_not_have` row "CT
   luxury 7.75% tier" and "NJ-style supplemental titling fee" against the
   cross-radius NJ dealers.
3. **lease-vs-cash-analyzer** — applied the NY lease-tax mechanic
   (`lease_playbook.md` section 3.1): NY taxes the **sum of all payments
   up front at signing**, not per-monthly. Worked the monthly-payment
   formula (depreciation + rent + tax) and scored the quote on the five
   core fields. Pulled the MBFS captive row: acquisition fee in the
   ~$795-$925 band, **disposition fee $595** (highest among mainstream
   captives), MF markup ceiling **0.00040**, GAP included.
4. **dealer-reply-drafter** — lease-specific Phase 6 counter against a
   synthetic MB sales manager whose quote omitted the money factor and
   stated "Cap Cost = MSRP."

### Artifacts produced

- `criteria.md` — Phase 1 core 9 fields + the 6-field lease sub-block
  under the Financing block, with the "is this monthly figure tax-in or
  tax-out?" clarifier and a NY-lease-tax heads-up row.
- `glc-ny-lease-baseline.md` — trim MSRP ladder, MBFS Q-current lease
  cash, residual % from Edmunds Lease Forum (REAL/SYNTHESIZED tagged),
  worked monthly on the five core fields, and the NY drive-off built with
  **tax on sum-of-payments computed up front** (not tax-on-monthly).
- `p6_lease_counter.md` — paste-ready lease counter under 12 lines:
  demand buy-rate MF (cite MBFS 0.00040 markup ceiling), reject
  "Cap Cost = MSRP," confirm acquisition fee at captive standard, confirm
  disposition fee $595 is the captive figure not a dealer add.

### Numbers and their provenance

Every dollar figure traces to a truth source — no invented fees:

- NY state tax 4%, doc cap $175, title $50, reg $100, no EV surcharge:
  `data/state_fees.json` -> states[] -> NY (`tax_state` 0.04,
  `doc_cap` 175, `title` 50, `reg_1yr` 100, `ev_reg_surcharge` null).
  **Provenance caveat:** the NY record is `verified: false` (no
  `source_url`, `source_verified_date` null) — these are seed values
  pending Round 2 web confirmation, so they are usable as the fixture
  truth but must be re-verified before quoting a live NY buyer.
- NY lease tax = lump-sum on sum-of-payments at signing:
  `lease_playbook.md` section 3.1 NY row.
- MBFS acquisition $795-$925 band, disposition $595, MF markup ceiling
  0.00040, GAP included: `lease_playbook.md` section 2 (acq fee bands),
  section 4.1 (MF markup ceiling table), section 6 (captive-lender rules
  table).
- Lease monthly formula (depreciation + rent + tax): `lease_playbook.md`
  section 3.

### Gotchas and Critical Rules that fired

- **Critical Rule #1 (plain ASCII)** — lease counter contains no
  em-dashes, no smart quotes, no markdown bold.
- **OTD-calculator suppression** — the orchestrator did NOT run the OTD
  stack; a lease has no doc/title/reg/dealer-fee OTD build. Routed to the
  lease monthly formula instead. (This is the load-bearing routing
  decision the fixture verifies.)
- **NY lease-tax timing** — drive-off built on tax-on-sum-of-payments at
  signing, NOT tax-on-monthly. Catching this is the scenario's core
  regression check.
- **"Cap Cost = MSRP" rejection** (`lease_playbook.md` section 13 Phase 6
  item 3) — the synthetic quote opened with Cap Cost = MSRP; the counter
  rejects it outright and demands Cap Cost = MSRP minus discount minus
  lease cash.
- **Buy-rate MF demand** (`lease_playbook.md` section 4) — counter cites
  the MBFS 0.00040 markup ceiling so reserve cannot hide in the MF.

### What this scenario surfaced for the skill

The lease path existed in reference form but had never been exercised
end-to-end. This fixture pins:

- The Phase 1 "loan or lease?" sub-router and the 6-field lease sub-block
  as a required capture, not an optional aside.
- The **OTD-calculator-suppression** routing rule for leases as an
  explicit, testable branch (the most common way a generic car-buying
  agent gets a lease wrong is by running OTD math on it).
- The NY lump-sum-at-signing lease tax as the canonical contrast against
  the NJ/CA tax-on-monthly default.
- The MBFS captive row (high acq, highest disposition $595, 0.00040 MF
  ceiling) as a worked negotiation anchor.

### Reading takeaway

Read this after scenario 4. It is the first lease in the set and the
only one where the OTD calculator is deliberately turned off. If your
local copy runs an OTD stack on this scenario instead of the lease
monthly formula, that is a routing regression. The NY tax-at-signing
mechanic is the second thing to verify — getting drive-off right on a NY
lease depends on it.
