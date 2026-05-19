---
name: EV Buyer Helper
description: Use when the buyer is purchasing an EV (battery electric or plug-in hybrid) and needs federal $7,500 credit mechanics, state EV rebates, NACS adapter info, home charging guidance, used-EV battery State-of-Health rules, or any EV-specific dealer behavior knowledge. Triggers include "EV federal credit", "$7,500 POS transfer", "Ioniq 5 incentives", "NACS adapter", "EV charging at home", "买电车", "电车补贴", "EV battery health".
---

# EV Buyer Helper

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 3B sub-skill split from orchestrator)

Narrow helper for EV-only buying scenarios: federal/state incentives, charging hardware transition, used-EV battery diligence. Use when buyer has already chosen an EV powertrain and needs the EV-specific layer on top of the standard OTD/negotiation flow.

## When To Use

- Buyer is purchasing a BEV or PHEV (new or used)
- Need to compute net price after federal + state EV incentives
- Question about NACS vs CCS1 adapter compatibility
- Home charging install (L1 vs L2, panel, installer cost)
- Used-EV battery State-of-Health (SoH) verification before purchase
- Lease vs purchase decision driven by §45W commercial credit pass-through

## When NOT To Use

- ICE / hybrid (non-plug-in) buyer - skip this skill
- General OTD math - delegate to `otd-calculator`
- CPO eligibility - delegate to `cpo-eligibility` (then return here for §EV)
- Lease structuring - delegate to `lease_playbook.md` § EV first

## Federal §30D New EV Credit (Purchase)

- Max credit: $7,500 (split $3,750 critical minerals + $3,750 battery components)
- Vehicle MSRP cap: $80,000 SUV/truck/van, $55,000 car
- Buyer AGI cap: single $150k, HoH $225k, MFJ $300k
- Vehicle must be on fueleconomy.gov tax-credit eligible list
- Final assembly in North America required

### Point-of-Sale (POS) Transfer (since 2024)

- Dealer MUST be IRS-registered (Energy Credits Online portal)
- Buyer signs IRS Form 8936-A at signing
- Dealer applies $7,500 directly to sale price (acts as down payment)
- Buyer gets time-of-sale report; still must file Form 8936 with return
- If dealer NOT IRS-registered: credit claimed on tax filing only (worse cash flow, 6-15 month delay)
- Recapture risk: if buyer AGI exceeds cap in purchase year OR prior year (lookback), buyer owes IRS back the $7,500

### Pre-Purchase Verification Checklist

1. Confirm dealer is IRS-registered (ask for confirmation, or check via dealer)
2. Confirm vehicle VIN is on fueleconomy.gov eligible list
3. Confirm MSRP under cap
4. Confirm buyer AGI under cap (current OR prior year)
5. Get time-of-sale report copy at signing

## Federal §25E Used EV Credit

- Max credit: $4,000 OR 30% of sale price, whichever lower
- Vehicle sale price cap: $25,000
- Buyer AGI cap: single $75k, HoH $112.5k, MFJ $150k
- Vehicle: 2+ model years old (e.g. 2026 buyer needs 2024 or older)
- Must be first transfer after Dec 31 2022 (1-owner-since-IRA-passed check)
- One §25E credit per buyer every 3 years
- Same POS transfer mechanism available

## State EV Rebate Matrix (Top 8 States)

| State | Program | BEV | PHEV | Notes |
|-------|---------|-----|------|-------|
| CA | CVRP | suspended 2024 | suspended | Check current CCVRP status |
| CO | Innovative Motor Vehicle Credit | $5,000 | $1,500 | State income tax credit |
| IL | IEPA EV Rebate | $4,000 | n/a | First-come funding |
| NJ | Charge Up NJ | up to $4,000 | up to $4,000 | MSRP cap $55k |
| NY | Drive Clean Rebate | $2,000 | $500-1,000 | At point of sale |
| TX | none | $0 | $0 | Discontinued 2024 |
| OH | none | $0 | $0 | n/a |
| MI | none | $0 | $0 | n/a |
| PA | none currently | $0 | $0 | Check AFV program status |

## Stack Worked Example

Ioniq 5 SEL AWD in NJ:
- MSRP $51,400 (under $80k SUV cap)
- Federal §30D POS: -$7,500
- NJ Charge Up: -$4,000
- Net before negotiation: $39,900
- Stack value: $11,500 off sticker

## NACS / CCS1 Charging Transition

NACS = SAE J3400 (Tesla connector standardized).

| OEM | 2024 and earlier | 2025+ |
|-----|------------------|-------|
| Hyundai/Kia | CCS1 + adapter | NACS native (some 2025 still CCS1) |
| Ford | CCS1 + adapter | NACS native MY2025 |
| GM | CCS1 + adapter | NACS native MY2025 |
| Tesla | NACS native | NACS native |
| Rivian | CCS1 + adapter | NACS native MY2025 |

### Adapter Reality

- OEM-supplied NACS-to-CCS1 adapter: $200-400 (Ford/GM/Hyundai bundle one for some MY2024 owners)
- Tesla Supercharger access: NACS-native plugs in direct; CCS1 + adapter works only at V3 Superchargers (V2 incompatible for most non-Tesla)
- Magic Dock stations: limited rollout, can serve CCS1 without adapter

## Home Charging Install

| Level | Spec | Speed | Use Case | Install Cost |
|-------|------|-------|----------|--------------|
| L1 | 120V/12A standard outlet | 4-5 mi/hr | <40 mi/day commute | $0 |
| L2 | 240V/40A | 25-30 mi/hr | Daily driver | $1,000-2,000 |
| L2 (high) | 240V/48A hardwired | 35-40 mi/hr | Multi-EV household | $1,500-3,000 |

Common installer: Qmerit (OEM-blessed network).

Prerequisites for L2:
- Electrical panel capacity check (200A panel ideal; 100A may need load management)
- HOA approval if condo/townhome
- Permit pull by electrician

## Range Decision Matrix

| Use Case | EPA Range Minimum |
|----------|-------------------|
| City commute only | 100-150 mi |
| Mixed daily + occasional road trip | 200-250 mi |
| Frequent road trips | 270-320 mi |
| Cold climate (subtract 30%) | add 30% to above |

## Used-EV Battery State-of-Health (SoH)

CRITICAL pre-purchase step. Battery degradation:
- Healthy: 2-3% per year capacity loss
- Concerning: 5%+ per year = heat damage / abuse / frequent DCFC
- Cliff: sudden drop = cell failure imminent

### How to Get SoH

- Tesla: visible in service mode; ask seller to screenshot
- Hyundai/Kia: dealer scan tool (request explicitly)
- GM Bolt: dealer Tech 2 scan
- Nissan Leaf: LeafSpy app + OBD dongle ($30 buyer-side check)
- Ford Mach-E / F-150 Lightning: FordPass / dealer scan

### Out-of-Warranty Battery Replacement Cost

| Brand | Pack Cost (parts + labor) |
|-------|---------------------------|
| Hyundai/Kia | $15,000-22,000 |
| GM Bolt | $12,000-18,000 |
| Nissan Leaf | $10,000-15,000 |
| Tesla Model 3 | $13,000-20,000 |
| Ford Mach-E | $18,000-25,000 |

## EV Warranty (Federal Floor)

- Federal mandate: 8 years / 100,000 miles on battery + drive unit
- Voluntary extended (notable):
  - Hyundai/Kia: 10 years / 100,000 miles (original owner only - check transferability)
  - Tesla Model 3 SR: 8/100k; Long Range: 8/120k
  - Ford: 8/100k
  - GM: 8/100k

## Lease + §45W Pass-Through

If lessor (captive finance) captures the $7,500 commercial clean vehicle credit (§45W) and passes through:
- Monthly drops ~$104 over 60mo (or ~$208 over 36mo lease)
- No buyer AGI cap, no MSRP cap on §45W
- Loophole used heavily for ineligible-under-§30D vehicles (foreign-assembled, over MSRP cap)
- Verify on lease worksheet: look for "EV lease credit" or "$7,500 cap cost reduction"

See `../orchestrator/references/lease_playbook.md` § EV for full mechanics.

## Cross-References

- `../orchestrator/references/ev_buyer_playbook.md` - full deep-dive
- `../orchestrator/references/hyundai_cpo_program.md` § EV
- `../orchestrator/references/kia_cpo_program.md` § EV
- `../orchestrator/references/lease_playbook.md` § EV §45W
- `../orchestrator/references/payment_methods.md` - for paying remaining balance after credit

## Worked Example (Current Iter)

The buyer in central Texas, Ioniq 5 SEL AWD:
- Sale price negotiated: $46,800
- Dealer fees + TTL: $1,356
- Pre-credit OTD: $48,156
- §30D POS via IRS-registered local Hyundai dealer: -$7,500
- TX state rebate: $0 (discontinued)
- Net OTD: $40,656
- L2 home install (Qmerit): +$1,400 (separate line)
