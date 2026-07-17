---
name: Carfax & PDF Review
description: Use to analyze a dealer-attached PDF, CARFAX vehicle history report, service records, or OTD proposal, and extract accident detail, service gaps, F&I add-on hidden costs. Triggers include "review this CARFAX", "analyze service records", "what's in this proposal PDF", "did dealer hide add-ons", "看下 CARFAX", "审 PDF", "F&I add-on detection", and Spanish phrases "revisar este CARFAX", "analizar el historial del vehiculo en este PDF".
---

# Carfax & PDF Review

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 2C sub-skill split from orchestrator)

Structured extraction from three common dealer-attached PDFs: CARFAX vehicle history, dealership service records, and OTD/financing proposals. Output is a typed red-flag report the buyer can act on.

## When To Use

- Dealer email attaches a CARFAX PDF and buyer wants accident/owner/title verification
- Dealer attaches service records PDF and buyer wants completeness check
- Dealer attaches OTD proposal / financing worksheet and buyer wants F&I add-ons surfaced
- Buyer wants to verify dealer's verbal claims against the written PDF

## When NOT To Use

- No PDF attached - skill cannot proceed; tell user to request the file from dealer
- PDF is text-extracted poorly (scanned image with no OCR) - flag to user, do not invent content
- Generic listing screenshot, not a PDF - hand off to inventory research in `../orchestrator`

## Critical Gotchas Up Front

- **V1**: CARFAX 1-Owner is necessary but NOT sufficient. A 1-owner car can still have unreported body damage or missing scheduled service. Always cross-check service records.
- **V2**: Read the PDF yourself with the Read tool. Never trust dealer's verbal summary. ("Just a fender bender" has masked $8k structural repairs.)
- **D7**: Dealer proposal PDFs sometimes render as image-only or with hidden text layers that Claude cannot see. If extraction fails, ask buyer to (a) open the PDF locally and paste the line items inline, OR (b) ask dealer to paste the OTD breakdown into email body as plain text.

Full gotcha list: `../orchestrator/references/pdf_review_checklist.md`.

## 3-Section Workflow

### Section 1 - CARFAX Analysis

1. **VIN match**: confirm VIN on PDF matches VIN in dealer listing and buyer's notes. Mismatch = stop and re-confirm.
2. **Owner count**: 1-owner is gold; 2-owner is fine if both held >2 years; 3+ owners in <5 years is a flip-warning.
3. **Accident detail extraction** (use template below): impact zones, repair shop name, structural damage flag, airbag deployment flag, estimated ADAS recalibration cost (see ADAS table below).
4. **Service record completeness**: count service entries vs vehicle age; flag gaps >18 months.
5. **Title brand**: Salvage / Junk / Rebuilt / Lemon / Flood = walk away immediately.
6. **Odometer audit**: last reported reading should match dealer's listed mileage within 500 mi.
7. **Open recalls**: list each recall ID; demand written confirmation that all are resolved before purchase.

### Section 2 - Service Records PDF

1. **Brand-specific service expectations**:

| Brand | Oil Interval | Major Service | CVT/Trans Service | Spark Plugs |
|-------|--------------|---------------|-------------------|-------------|
| Toyota | 10k / 12 mo | 30k inspection | 60k (Atkinson hybrid) | 120k iridium |
| Subaru | 6k / 6 mo | 30k inspection | 30k CVT fluid (post-2015) | 60k |
| Honda | 5-7.5k (oil minder) | 30k inspection | 30k ATF / CVT | 105k iridium |
| Ford | 7.5-10k | 30k inspection | 60-100k | 100k |
| Mazda | 7.5k / 12 mo | 30k inspection | 60k auto | 75-100k iridium |

2. **Gap detection**: line up actual service dates against the schedule. Each missed major service = inherited cost.
3. **"$X inherited cost" calculator** (typical NJ dealer-shop rates):
   - Missed CVT fluid service: $250-450
   - Missed spark plugs (4-cyl): $300-500
   - Missed transmission service: $350-650
   - Missed brake fluid flush: $120-180
   - Missed coolant change: $150-220

Sum and present as negotiation lever.

### Section 3 - OTD Proposal PDF (F&I Add-On Scan)

Scan every line item. Flag the following 12 common F&I add-ons as challengeable:

1. GAP insurance (~$400-900 dealer, $200 from credit union)
2. VSC / extended service contract (often $1.5-3.5k - negotiable or decline)
3. Tire & wheel protection ($400-900)
4. Paint / interior protection ($300-1k - usually pure margin)
5. Key replacement insurance ($200-400)
6. Theft etching / VIN window etch ($200-400 - sticker only)
7. Nitrogen tire fill ($30-100 - decline)
8. LoJack / tracking ($500-1k - decline unless required)
9. Undercoating / rustproofing ($400-900 - modern cars don't need)
10. Dealer prep fee ($200-1k - challenge as duplicative)
11. EV-prep / charging package ($300-800 - decline if buyer has home charger)
12. Battery conditioning / detail ($150-400)

Each gets a "challenge note" - see template below.

## Structured Extraction Templates

### CARFAX Accident Template (7 fields)

```
ACCIDENT RECORD #N
  Date:               YYYY-MM
  State / City:       NJ / Newark
  Impact Zone:        [Front / Rear / Side-L / Side-R / Roll-over]
  Repair Shop:        [name + city] OR "Not reported"
  Structural Damage:  Yes / No / Not reported
  Airbag Deployment:  Yes / No / Not reported
  ADAS Recal Cost:    $X-Y (see ADAS table; only if model has ADAS)
```

### Service Gap Output Format

```
SERVICE GAP REPORT
  Vehicle age:        X years / Y miles
  Records on file:    N entries
  Expected entries:   M entries (per brand schedule)
  Gaps identified:
    - {service name}  @ {expected mileage}  inherited cost ~${low-high}
    - ...
  Total inherited cost (low-high): $X-Y
  Negotiation ask:    deduct $Z from OTD or include 30-day service warranty
```

### Add-On Challenge Note

```
ADD-ON: {line name}
  Listed price:       $X
  Fair market range:  $Y-Z  (cite source: credit union / online quote)
  Recommendation:     [Itemize this line / Show fair-market alternative / Decline at close]
  Email language:     "please itemize {line} and provide the underwriting company; if it's a third-party product I will compare directly"
```

## ADAS Recalibration Cost by Brand

Use these ranges when accident report mentions front-impact or windshield replacement on an ADAS-equipped model. Add to "inherited cost" total.

| Brand System | Recal Cost Range |
|--------------|------------------|
| Subaru EyeSight | $400 - $1,200 |
| Honda Sensing | $300 - $1,000 |
| Toyota Safety Sense | $400 - $1,500 |
| Hyundai SmartSense | $400 - $1,200 |
| Ford Co-Pilot360 | $250 - $900 |
| GM Driver Assistance (incl SuperCruise) | $300 - $1,500 |
| Mazda i-Activsense | $400 - $1,200 |
| Nissan ProPILOT | $300 - $1,200 |
| Tesla Autopilot / FSD | $500 - $1,500 |
| VW / Audi Travel Assist | $300 - $1,200 |

## Full Reference

For deeper templates (rental fleet detection, NJ MVI nuances, lien-release verification, full add-on per-line scripts):

- `../orchestrator/references/pdf_review_checklist.md`

## Cross-Skill Handoffs

- "Is this CPO eligible / is this factory cert?" - hand to `cpo-eligibility`
- "How much does this affect OTD?" - hand to `otd-calculator`
- "Draft a reply asking dealer about these add-ons" - hand to `dealer-reply-drafter`
- Closing-day final verification - hand to `close-day-checklist`
