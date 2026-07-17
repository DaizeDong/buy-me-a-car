---
name: CPO Eligibility Check
description: Use to check Certified Pre-Owned eligibility, coverage, and embedded value for a specific vehicle (VIN/year/mileage) against the brand's CPO program. Covers Subaru, Honda, Toyota, Hyundai, Kia, Ford, GM, Mazda, Stellantis (Ram/Jeep/Chrysler/Dodge/Fiat), Lexus, Genesis, Acura. Triggers include "is this car CPO eligible", "CPO program details for X", "embedded CPO value", "should I pay for CPO", "factory CPO vs dealer certified", "Subaru CPO" / "Honda Certified" etc., and Spanish phrases "es un auto certificado por el fabricante", "vale la pena pagar por la certificacion CPO".
---

# CPO Eligibility Check

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 2C sub-skill split from orchestrator)

Quick lookup for factory CPO eligibility, coverage terms, and embedded dollar value across 12 brands (8 mainstream + Stellantis SPOTiCAR + 3 luxury exceptions: Lexus, Genesis, Acura). Use this skill when a dealer claims "Certified" or buyer is deciding whether the CPO premium is worth paying.

## When To Use

- Buyer asks "is this car CPO eligible" with VIN/year/mileage
- Dealer listing shows "Certified" and buyer needs eligibility verification
- Buyer wants brand-specific CPO program details
- Buyer is comparing CPO premium vs paying out-of-pocket extended warranty
- Buyer suspects "fake CPO" (dealer-house program masquerading as factory)

## When NOT To Use

- Luxury / heavy commercial brands (BMW, MB, Audi, Porsche, RAM HD, F-250+) - see `../orchestrator/references/vertical_playbooks.md#part-2--heavy--commercial--luxury`. **Exceptions: Lexus L/Certified, Genesis CPO, and Acura Precision Certified/Used ARE documented factory programs in this skill**, see their per-brand reference files below and the Luxury exceptions table.
- Closing-day paperwork verification - delegate to `close-day-checklist`
- General OTD math - delegate to `otd-calculator`

## Quick Decision Matrix

Given (brand, model year, odometer), determine eligibility in one pass:

```
ELIGIBLE if:
  (current_year - model_year) <= brand_max_years
  AND odometer < brand_max_miles
  AND sold by authorized brand dealer
  AND passes brand inspection
```

If ineligible, the "Certified" badge is either dealer-house (not factory) or fraud - always demand the factory CPO certificate PDF before accepting any CPO-related price premium.

## 12-Brand Comparison Table

### Mainstream (9 brands)

| Brand | Max Age | Max Miles | Inspection | Powertrain | Embedded $ | Market Premium |
|-------|---------|-----------|------------|------------|------------|----------------|
| Subaru | 5 yr | 80k | 152 pt | 7yr / 100k | $2.0-2.5k | $1.0-1.5k |
| Honda | 5-7 yr (tier) | 80k | 182 pt | 7yr / 100k | $1.8-2.4k | $1.0-1.5k |
| Toyota | 6 yr | 85k | 160 pt | 7yr / 100k + 10yr/150k hybrid | $2.5-3.0k | $1.2-1.8k |
| Hyundai | 7 yr | 80k | 150 pt | 10yr / 100k + 10yr/100k EV batt | $2.5-3.5k | $1.0-1.5k |
| Kia | 7 yr | 80k | 165 pt | 10yr / 100k ($50 B2B deductible) | $2.5-3.5k | $1.0-1.5k |
| Ford (Gold) | 6 yr | 80k | 172 pt | 7yr / 100k | $2.0-2.5k | $1.0-1.5k |
| Ford (Blue) | 10 yr | 120k | limited | 90 day / 4k only | $200-400 | marketing-grade |
| GM | 6 yr | 75k | 172 pt | 6yr / 100k + 2 maint visits | $1.5-2.0k | $800-1.2k |
| Mazda | 7 yr | 80k | 160 pt | 7yr / 100k + CarPlay (2018+) | $1.8-2.5k | $800-1.4k |
| Stellantis SPOTiCAR (Ram/Jeep/Chrysler/Dodge/Fiat) | 10 MY (top tier 5 MY) | 120k (top tier <75k) | 125 pt | 7yr / 100k from in-service + 3mo/3k Maximum Care | $1.0-1.8k top / $0.3-0.8k CPO Go | UNVERIFIED pin |

Stellantis SPOTiCAR is one program covering 5 brands (Ram, Jeep, Chrysler, Dodge, Fiat). It is two-tier: **Certified (top)** = <=5 model years AND <75,000 mi; **CPO Go** = 6-10 model years AND 75,001-120,000 mi. Outer bound for both tiers: <=10 MY AND <=120,000 mi, clean title, pass the 125-point inspection. Powertrain runs 7yr/100k from the original in-service date (so CPO Go units are often largely exhausted). Certified Upgrade warranty plans available only on units <=74,999 mi.

### Luxury exceptions (3 brands)

These three are documented factory programs (not routed to the luxury vertical playbook). Genesis and Acura are luxury-tier; Lexus is the luxury exception with an unlimited-mileage comprehensive edge.

| Brand | Max Age | Max Miles | Inspection | Powertrain / Comprehensive | Embedded $ | Market Premium |
|-------|---------|-----------|------------|----------------------------|------------|----------------|
| Lexus (L/Certified) | 6 yr | 80k | 161 pt | 2yr / unlimited B2B (stacks to up to 6yr total); no separate long-tail powertrain term | $1.5-2.5k | varies (UNVERIFIED pin) |
| Genesis (luxury) | 5 MY | 60k | 191 pt | 10yr / 100k powertrain + 6yr/75k comprehensive ($50 PT deductible) | $2.5-3.5k | <$1.0-1.5k target |
| Acura - Precision Certified | 6 yr | 80k | 182 pt | 7yr / 100k powertrain + 2yr/100k limited B2B | $1.8-2.8k | $1.0-2.0k |
| Acura - Precision Used | 10 yr | none | 112 pt | 6mo / 7.5k limited + powertrain (NOT transferable) | $0.3-0.7k | $0.3-0.7k |

Lexus L/Certified has NO 7yr/100k powertrain figure by design, its benefit is a 2yr/UNLIMITED-mile comprehensive B2B extension stacking onto the factory 4yr/50k to reach up to 6yr/unlimited. Genesis CPO reinstates the 10yr/100k powertrain for the 2nd owner (non-CPO used Genesis drops to 5yr/60k). Acura is two-tier: Precision Certified (top) vs Precision Used (lower, not transferable, no mileage cap). Acura/Genesis/Lexus embedded $ are brand-specific (NOT cross-applied from Subaru/Honda/Toyota).

Numbers reflect 2026 program terms. Powertrain term measured from original in-service date, NOT CPO sale date.

## Standout Facts (one-line cheat sheet)

- **Subaru**: 152-pt inspection, 7yr/100k powertrain from in-service, $0 deductible, transferable. Strongest mid-tier program.
- **Honda**: Dual-tier - Standard (5yr/86k) vs HondaTrue Certified+ (7yr/100k). CR-V eligibility commonly cited.
- **Toyota**: 10yr/150k Hybrid Component coverage is the killer perk - huge embedded value on RAV4 Hybrid, Camry Hybrid, Prius.
- **Hyundai**: 10yr/100k powertrain AND 10yr/100k EV battery - longest term in non-luxury. Best for Ioniq 5/6, Kona EV.
- **Kia**: Same 10yr/100k as Hyundai but $50 B2B deductible (Hyundai is $0). Cheaper certification fee at some dealers.
- **Ford**: Gold Certified is real factory CPO. Blue Certified is 90-day / 4k-mile dealer-house marketing - do NOT pay a premium for Blue.
- **GM**: 6yr/100k is shortest non-luxury powertrain. Partial offset: 2 included maintenance visits (oil + tire rotation).
- **Mazda**: 7yr/100k plus guaranteed CarPlay/AndroidAuto on 2018+. Solid 24/7 roadside.
- **Stellantis SPOTiCAR (Ram/Jeep/Chrysler/Dodge/Fiat)**: one program, 5 brands, two tiers. Certified (top) = <=5 MY / <75k mi; CPO Go = 6-10 MY / 75-120k mi. 125-pt inspection, 7yr/100k powertrain from in-service ($0 deductible) + 3mo/3k Maximum Care. Powertrain runs from in-service, so CPO Go value is age-sensitive. Mopar extended warranty hard ceiling at 80,001+ mi.
- **Lexus (L/Certified)**: luxury exception in this skill. 161-pt inspection, 2yr/UNLIMITED-mile comprehensive B2B stacking to up to 6yr total, $0 deductible, + 4-service/2yr/20k complimentary maintenance. Unlimited-mileage is the edge vs a self-bought (mileage-capped) Lexus Platinum VSA (~$1,955 for 6/100k).
- **Genesis (luxury)**: 5MY/60k, 191-pt inspection (deepest in Hyundai group). CPO **reinstates 10yr/100k powertrain for 2nd owner** (non-CPO used Genesis drops to 5yr/60k) + adds 6yr/75k comprehensive. $50 powertrain deductible. Luxury repair = 2x-4x Hyundai/Kia, so embedded value is the highest in the group on a dollar basis. Negotiate premium below ~$1,000 (KBB guidance).
- **Acura (Precision Certified / Precision Used)**: two-tier Honda luxury division. Precision Certified = <=6 MY / <80k mi -> 182-pt, 7yr/100k powertrain + 2yr/100k limited B2B, $0 deductible, transferable. Precision Used = <=10 MY / no mileage cap -> 112-pt, 6mo/7.5k only, NOT transferable. Acura Care VSC separate-buy runs $1,500-$3,500+.

## Out-of-CPO Options

If the car is ineligible OR the CPO premium is wider than $2k, consider:

1. **Factory extended warranty** (sold by authorized brand dealer, backed by OEM): typically $1.5-3.5k for 7yr/100k bumper-to-bumper. Negotiable - never pay sticker. Best value.
2. **Independent extended warranty** (Endurance, Carchex, CARCHEX, olive): $1.8-4k for similar term. Watch claim-denial rates and authorized-repair networks. Read fine print on wear items.
3. **Self-insure**: bank the $2-3k CPO premium and pay repairs as they come. Best for 1-2 owner cars with full service records under 60k miles.

See `../orchestrator/references/vertical_playbooks.md#part-2--heavy--commercial--luxury` for luxury extended warranty notes (BMW/MB factory programs run $3-6k).

## Fake CPO Label Detection

Red flags that a "Certified" sticker is dealer-house (NOT factory CPO):

- Listed at independent dealer (not authorized brand dealer)
- No factory CPO certificate PDF when requested by email
- Warranty paperwork shows third-party administrator (Endurance, CornerStone, etc.) not OEM
- Term offered does not match brand's published program (e.g., "5yr/60k powertrain" on a Subaru - real Subaru CPO is 7yr/100k)
- Vehicle age/mileage exceeds brand's eligibility (see matrix above)
- Charges a "certification fee" but cannot produce inspection report

Full red-flag list: `../orchestrator/references/vertical_playbooks.md#part-2--heavy--commercial--luxury` section "Fake CPO Label Detection".

## Verification Checklist (before paying CPO premium)

1. Factory CPO certificate PDF in buyer's hand (not just "we'll email it")
2. Authorized brand dealer confirmed via OEM dealer locator
3. Warranty registered in brand's CRM - call brand 1-800 with VIN to verify before signing
4. Inspection report PDF (Subaru 152pt, Honda 182pt, etc.) - check date, technician signature, pass status on each line
5. CPO start date = vehicle in-service date (not today) - confirm in writing

## Per-Brand Full Detail References

For full program details (warranty granularity, transfer rules, deductibles, exclusions, model-year cutoffs):

- Subaru: `../orchestrator/references/subaru_cpo_program.md`
- Honda: `../orchestrator/references/honda_cpo_program.md`
- Toyota: `../orchestrator/references/toyota_cpo_program.md`
- Hyundai: `../orchestrator/references/hyundai_cpo_program.md`
- Kia: `../orchestrator/references/kia_cpo_program.md`
- Ford (Gold + Blue): `../orchestrator/references/ford_bluecert_program.md`
- GM: `../orchestrator/references/gm_cpo_program.md`
- Mazda: `../orchestrator/references/mazda_cpo_program.md`
- Stellantis SPOTiCAR (Ram/Jeep/Chrysler/Dodge/Fiat): `../orchestrator/references/stellantis_cpo_program.md`
- Lexus (L/Certified): `../orchestrator/references/lexus_cpo_program.md`
- Genesis: `../orchestrator/references/genesis_cpo_program.md`
- Acura (Precision Certified + Precision Used): `../orchestrator/references/acura_cpo_program.md`

## Cross-Skill Handoffs

- CARFAX / service records on the candidate vehicle: hand off to `carfax-pdf-review`
- OTD impact of CPO premium: hand off to `otd-calculator`
- Drafting an email asking dealer "is this factory CPO certified": hand off to `dealer-reply-drafter`
