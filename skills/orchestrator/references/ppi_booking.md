# Pre-Purchase Inspection (PPI) Booking Guide

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

This reference covers PPI booking when the buyer has 1-4 final candidates and a same-week close deadline.

## When to Engage PPI

- Immediately after dealer commits to written OTD AND CARFAX is clean AND warranty + service history check out.
- Before transferring cashier's check.
- Required on every used purchase regardless of CPO status — CPO 152-point is dealer self-inspection and does not replace independent PPI.

## Mobile PPI vs Drop-Off PPI

**Mobile PPI is the preferred default** because:
- Inspector goes to dealer location (or buyer-chosen meeting point)
- Eliminates car-transport coordination with dealer
- Saves buyer 1-2 hours of round-trip drive
- Same comprehensive inspection as shop-based

**Drop-Off PPI** (buyer drives car to mechanic) is acceptable when:
- Mobile services don't service the area
- Dealer happens to be 2-5 minutes from buyer-preferred mechanic
- Buyer wants to inspect car personally during PPI

## Recommended Mobile PPI Services (NY/NJ/CT region)

| Service | Cost | Coverage | Inspection Depth | Phone |
|---------|------|----------|------------------|-------|
| **Lemon Protector** | $139+ | NY/NJ/CT | 450-point + lift + phone consult | (516) 983-3800 / (718) 229-7594 |
| **YourMechanic** | $137-234 | National | 50-point or full diagnostic | 1-844-997-3624 |
| **Pep Boys Mobile** | $99-149 | National chain | 120-point | Local Pep Boys |

Lemon Protector specializes in PPI, 25+ years experience, includes a phone consultation with the actual inspector. Best fit for time-sensitive buying cycles.

## Parallel-Booking Strategy (2-4 final candidates)

When the buyer has 2-4 dealers in final consideration and a same-week close, book PPI slots for ALL of them in parallel.

**Why**: The dealer choice may not be finalized until 8-10 AM the day of PPI. Booking only one slot risks delays if that dealer falls through.

**How to book in parallel without confusing the service**:

1. **Stagger times** so the inspector knows they only need to do one. Example: 9 AM / 10 AM / 11 AM / 12 PM.
2. **NOTES field for each booking**: "BOOKING X OF N - TENTATIVE. I am finalizing my dealer choice by [DAY] [TIME] AM ET and will cancel the unused slots. This booking: [vehicle details]. Dealer: [name + address]. Salesperson: [name + phone]. Cash buyer ready to close same day if PPI is clean."
3. **Same email + phone** across all bookings so service can quickly link them.
4. **Cancel within 24 hours** of scheduled time to avoid no-show fees. Call service phone, reference confirmation number.

**Example parallel-booking cycle** (4 in-radius dealers, staggered slots the night before PPI day):
- 9 AM <Dealer A> (2024 Limited)
- 10 AM <Dealer B> (2023 Touring)
- 11 AM <Dealer C> (2023 Touring)
- 12 PM <Dealer D> (2025 Limited)

Service may proactively call to confirm before dispatching — answer with "I'm finalizing tonight, will confirm by 9 AM Thursday."

## Online Form Quirks (Lemon Protector and similar)

- **YEAR dropdown** caps at current year - 1 (currently 2023 max). For 2024/2025 vehicles, put actual MY in MODEL field or NOTES: "Forester Limited (note actual MY is 2025)".
- **DATE input** is HTML5 `<input type="date">` requiring **ISO format YYYY-MM-DD** (not MM/DD/YYYY). Playwright `fill_form` with MM/DD/YYYY will throw "Malformed value" error.
- **VEHICLE LOCATION STATE** defaults to NY (Lemon Protector HQ). Must manually change to NJ for NJ dealer.
- **SELLER PHONE TYPE** defaults to "Cell". Change to "Work" for dealership main line.
- **TIME** dropdown defaults to "Select" (not a real selection). Must explicitly pick.
- Always re-snapshot after `fill_form` to verify state before clicking Submit.

## Subaru-Specific PPI Checklist

Print and hand to inspector:

**Engine (FB25 2.5L H4)**:
- Compression test all 4 cylinders (variance ≤10%)
- Oil leaks (FB25 is much improved over EJ25 head gasket, but check)
- Coolant level + condition
- PCV valve operation
- Engine mounts

**Transmission (CVT)** — Subaru's known wear point:
- CVT fluid condition + level
- Test drive 25/45/65 mph — any judder/vibration is RED FLAG
- Cold start behavior
- TCM no DTCs

**AWD System (Subaru Symmetrical AWD)**:
- Center differential coupling check
- Front + rear differential fluid
- CV joint inspection (both sides)
- 4-tire tread depth must be within 2/32" of each other or AWD will be damaged

**Brakes**:
- Pad thickness (mm): front ≥5mm OK, <3mm = $400 replacement
- Rotor thickness + warping
- Brake fluid moisture content
- Parking brake operation

**Tires**:
- Tread depth all 4 (≥4/32" OK)
- DOT date codes (4 digits — within 5 years)
- Sidewall integrity
- Tire matching for AWD

**Suspension**:
- Strut/shock bounce test
- Bushings (control arm, sway bar end links)
- Ball joints
- Wheel bearings

**Electrical / Safety**:
- All dash warning lights clear after engine warm
- EyeSight cameras alignment (CRITICAL on Forester)
- Battery health (CCA test)
- A/C output ≤45°F at vents
- All accessory functions

**Body / Frame**:
- Paint thickness gauge (front fenders, doors, hood — check for repaint)
- Undercarriage rust (NJ/Northeast salt corrosion)
- Frame straightness visual
- Panel gap consistency

**Documentation cross-check**:
- Mileage matches CARFAX last report
- VIN tag (dashboard + door jamb) matches paperwork
- No visible accident repair / panel replacement
- Service records align with CARFAX timeline

## PPI Cost vs Walk-Away Math

PPI cost: $139-200
Cost of buying a car with hidden issues: $1,000-6,000 typical repair ranges (CVT $4-5k, head gasket $2-3k, frame $5-8k, EyeSight calibration $800).

PPI ROI: 5-30× return on investment. Never skip.

## PPI Result Decision Matrix

| PPI Result | Action |
|------------|--------|
| Clean — no significant issues | Proceed to close, cashier's check, drive home |
| Minor issues ($300-1,000 total) | Counter dealer for repair-credit OR have dealer fix BEFORE delivery |
| Major issues ($1,000+) — CVT judder, frame damage, hidden accident, oil consumption | **Walk away**, deposit refunded per hold mechanism |
| Anything not disclosed by dealer pre-PPI | Trust score down — even if minor, reconsider |

## Cashier's Check Timing

Plan bank visit BEFORE PPI:
- US banks typically have 9-10 AM business day cut-off for same-day cashier's checks
- Have check made out to dealer (per dealer's exact legal name from earlier email) for OTD amount
- Bring secondary ID + small contingency cash for unexpected fees ($50-100)
- If PPI fails, return check to bank for refund/reissue (most banks allow within 90 days)

## Walk-Away Email Template (Losing Dealers)

After committing with the winning dealer, send each losing dealer a 5-line walk-away:

```
Hi [name],

Quick note to close out our conversation. I have committed to a different unit
this week, but I appreciate your responsiveness and the [specific positive thing,
e.g. clean OTD breakdown / quick reply / good CARFAX disclosure].

I will keep you in mind for future Subaru needs and may refer family / friends.

Best,
{{BUYER_NAME}}
```

Preserves relationship + leaves channel open.

## Coordination Email to Winning Dealer

After PPI confirmation, send winning dealer a 8-line logistics email:

```
Hi [name],

PPI is booked for Friday 5/15 [time] with [inspector service name],
phone [service number]. Inspector will arrive at your dealership.

I will arrive shortly after with cashier's check ready for $[OTD amount].

If everything is clean, I plan to close same afternoon.

Please confirm:
1. Inspector will be welcomed on premises
2. Hold/deposit terms (if any) for the morning before close

Thanks,
{{BUYER_NAME}}
[phone]
```
