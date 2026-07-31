---
name: ppi-scheduler
description: Use to book a pre-purchase mechanical inspection (PPI) before finalizing a used-car purchase, especially when juggling 2-4 final candidates. Triggers include "book PPI", "mobile inspector NJ", "pre-purchase inspection", "Lemon Protector", "YourMechanic", "Pep Boys mobile inspection", "提车前检车", and Spanish phrase "agendar inspeccion pre-compra antes de comprar el auto usado".
---

# PPI Scheduler

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 3C sub-skill split from orchestrator)

Narrow helper: book a mobile PPI on one or more final candidates before
signing. Defers the full inspector directory + form-field gotchas to
`../orchestrator/references/ppi_booking.md`.

## When To Use

- Buyer has 1-4 used-car final candidates and wants mechanical sign-off
- Buyer asks for a mobile inspector recommendation by region
- Need PARALLEL booking strategy across 2-4 dealers same day
- Need brand-specific PPI scope (Subaru CVT, Toyota hybrid, etc.)
- Post-PPI walk vs proceed decision

## When NOT To Use

- New car off the truck under factory bumper-to-bumper - PPI is rarely
  cost-justified; skip
- CARFAX history review only (no mechanical) - delegate to `carfax-pdf-review`
- General CPO benefits eligibility - delegate to `cpo-eligibility`

## Mobile PPI Services by Region

| Region | Service | Price | Notes |
|---|---|---|---|
| NY / NJ / CT | Lemon Protector | $139+ | lemonprotector.com, dispatched tri-state |
| CA / Bay Area | YourMechanic | $150-200 | App-based, ASE-certified |
| CA / SoCal | Lemon Squad | $175 | Mobile, fast scheduling |
| Multi-state | Pep Boys Mobile | $150 | Variable quality by region |
| Multi-state | Carchex Mobile Inspection | $190 | Insurance-grade reports |
| Local fallback | Yelp top-rated ASE shop | $100-200 | Best for brand specialists |

For Subaru / Toyota / Honda hybrid powertrains: prefer brand-specialist shop
over generic mobile when one is within 15 miles. Specialists catch CVT
seepage, head gasket weep, inverter coolant level that generic miss.

## Parallel Booking Strategy (2-4 Candidates Same Day)

Per orchestrator gotcha P1: when there are 2-4 final candidates and the buyer
plans to commit within 24-48 hours, stagger PPIs on a SINGLE day to compress
the decision window.

| Slot | Time | Note in booking form |
|---|---|---|
| 1 | 9:00 AM | "BOOKING 1 of N - tentative, finalizing by 11 AM" |
| 2 | 10:30 AM | "BOOKING 2 of N - tentative, finalizing by 11 AM" |
| 3 | 12:00 PM | "BOOKING 3 of N - tentative, finalizing by 11 AM" |
| 4 | 1:30 PM | "BOOKING 4 of N - tentative, finalizing by 11 AM" |

Cancel the unused slots no later than 24 h before the scheduled time to avoid
the service's no-show fee (typically half the inspection cost).

Inspector dispatch needs (collect BEFORE filling the form):

- Dealer phone number (NOT cell - dealers route mobile inspectors via the
  service desk)
- VIN (17 chars)
- Dealer street address + ZIP
- Service-bay confirmation (call dealer day before: "your service bay is
  expecting a Lemon Protector inspector at <time> for VIN <last 6>")

## Online Booking Form Quirks

Per orchestrator gotcha P2: every mobile-PPI booking form has the same 5
gotchas. Snapshot the page before each step.

| Quirk | Symptom | Fix |
|---|---|---|
| Year dropdown caps at current/-1 year | 2026 vehicle on a form that maxes at 2025 | Pick 2025, put true year in NOTES |
| Date input ISO format | "12/30/2026" rejected | Use YYYY-MM-DD: "2026-12-30" |
| State default = service HQ state | Form pre-fills NJ when buyer is in NY | Manually pick buyer's state |
| Phone TYPE default "Cell" | Dealer phone routed wrong | Change to "Work" for dealer number |
| Multi-page form stale state | Form resets fields between pages | Re-snapshot after each `fill_form`, before Submit |

## Standard PPI Scope (50-pt mechanical)

The default checklist every mobile PPI runs:

- Cold start + idle vibration (engine NOT warmed up - critical for head
  gasket / lifter detection)
- Test drive: 55-65 mph highway + city stop-and-go + parking-lot tight turns
- Brake feel + ABS function under firm stop
- Suspension under load (uneven road, speed bumps at low speed)
- Transmission shift quality (CVT smoothness for Subaru, 10-speed downshift
  for Ford, DCT clutch for VW/Audi)
- Exhaust leak check (visual + sound)
- Underbody inspection: frame condition, rust if Northeast / Rust Belt
- Battery health + alternator output
- Air conditioning function (cold + heat + defrost)
- All electronics: infotainment, ADAS calibration, power features

## Brand-Specific PPI Additions

| Brand | Extra check |
|---|---|
| Subaru | CVT fluid color (should be red), head gasket weep, AWD coupling engagement |
| Toyota Hybrid | Inverter coolant level, hybrid battery scan via Techstream |
| Honda 1.5T | Oil dilution check (smell + level), valve adjustment due? |
| Ford EcoBoost | Turbo wastegate function, 5.0L manifold/exhaust |
| Mazda SkyActiv | Carbon buildup symptom check on intake valves |
| Pickup (HD) | Tow hitch wear, transmission cooler clean, 5th wheel rail wear |
| Pickup (light) | Bed wear, hitch wiring integrity, 4WD engagement |

For pickup-specific scope see `../orchestrator/references/vertical_playbooks.md#part-1-pickup-truck-specifics` § 4.

## Post-PPI Walk-Decision Matrix

| PPI finding | Action |
|---|---|
| Clean PPI + dealer-revealed CARFAX matches | PROCEED |
| < $500 inherited cost (e.g. minor scuff, light bulb) | PROCEED; ask dealer to address pre-close |
| $500-$2,000 inherited cost (e.g. brake pads + rotors, tires) | COUNTER: ask $1-2k OTD reduction |
| > $2,000 OR structural (frame rust, head gasket weep, transmission slip) | WALK |
| PPI report disagrees with CARFAX (undisclosed accident damage found) | WALK + report to state AG if egregious |

Get the report in writing (PDF) - some dealers ask to see it and offer to
"fix" issues for free. Politely decline unless they put the fix on the
buyer's order in writing.

## Cross-References

- `../orchestrator/references/ppi_booking.md` - full inspector directory,
  state-by-state pricing, booking form screenshots
- `../orchestrator/references/vertical_playbooks.md#part-1-pickup-truck-specifics` § 4 - pickup
  PPI scope additions
- `../orchestrator/SKILL.md` gotcha V1 - CARFAX vs PPI evidence priority
- `../orchestrator/SKILL.md` gotcha V2 - dealer "we already inspected" trick
- `../orchestrator/SKILL.md` gotcha P1 - parallel booking strategy
- `../orchestrator/SKILL.md` gotcha P2 - form field gotchas

## Output Contract

After every PPI scheduling pass, return to the operator:

```
PPI scheduling pass - <timestamp>
  Candidates: N
  Bookings made:
    1. <service> at <time> for <year make model> @ <dealer>, $<fee>
    2. <service> at <time> for ...
  Booking IDs (for cancel): [list]
  Cancel deadline (T-24h): <date time>
  Dealer service desk calls due: <date>
  Brand-specific scope added: <yes/no, which brand>
```

After PPI completes, return:

```
PPI result pass - <timestamp>
  Vehicle: <year make model VIN>
  Verdict bucket: PROCEED / COUNTER $<n> / WALK
  Inherited cost estimate: $<n>
  Report PDF on disk: <path>
```
