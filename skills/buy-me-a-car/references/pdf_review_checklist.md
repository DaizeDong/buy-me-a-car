# PDF Review Checklist

When dealers send PDFs, open them with the Read tool and extract specific signals. Three common PDF types:

## CARFAX Vehicle History Report

Located in dealer email as a PDF attachment, usually titled with the VIN.

### Strong Positive Signals

- "CARFAX 1-Owner Vehicle" badge
- "No Accidents Reported"
- "No Total Loss"
- "No Structural Damage"
- "No Airbag Deployment"
- "No Odometer Rollback"
- "Personal Vehicle" (not fleet/rental)
- "Last Owned in {State}" matching buyer's state (no out-of-state title hassle)
- "Reliability Forecast: Good" or "Great"
- Annual mileage under 12,000-15,000 mi/year average

### Concerning Signals

- Multiple owners (especially within first 3 years)
- "Accident Reported" (any severity)
- Salvage / Junk / Rebuilt / Lemon title brand
- Flood / Hail / Fire damage history
- "Not Actual Mileage" or "Exceeds Mechanical Limits"
- "Total Loss" reported
- Open recalls listed under "Manufacturer Recall"
- Rental fleet history (heavy use, multiple unknown drivers)
- Out-of-state purchase requiring cross-state title transfer (NJ has specific MVC requirements)

### Service Record Gaps

Even on a 1-owner / no-accident car, CARFAX often shows only registration renewals and emissions checks, not actual service work. This is a gap, not a problem — many owners use independent shops that don't report to CARFAX.

Ask the dealer for dealership-internal service records as a follow-up. See `pdf_review_checklist.md` section "Service Records PDF" below.

### Reading Strategy

Page 1 has the summary badges (1-Owner / Accidents / Title Brands / Mileage check). If all green, proceed to Page 2 for detailed history. Look for:

- First title issue date and state
- Loan/lien reported (needs release confirmation before purchase)
- Inspection records (NJ MVI every 2 years for older cars)
- Registration gap years (could indicate storage / non-use period)
- Last reported odometer reading (should match dealer's listed mileage)

## Dealer Service Records PDF

Some dealers (especially when they sold the car originally) have full internal service history. These are gold — they reveal what was actually maintained.

### Check For

- **Oil change frequency** — every 5-7k miles synthetic is good
- **CVT fluid change** — Subaru spec 60k mi for severe service, 100k for normal. Critical for XT turbo variants
- **Spark plugs** — 60k mi typical interval (60k-100k depending on plug type)
- **Coolant flush** — 100k mi typical
- **Brake fluid flush** — every 2-3 years
- **Brake pads/rotors** — wear-based, look for replacement records
- **Tires** — replacement records, tire brand consistency
- **Battery** — replacement records, especially for cars 4+ years old in cold climates
- **Transmission diff fluid** — 60k mi typical for AWD
- **Spark plugs** — 60k-100k mi typical

### Red Flag Patterns

- Battery flagged 2-3 times but never replaced (still original old battery — high failure risk)
- CVT fluid never serviced past 60k mi (expensive failure if not maintained)
- Oil changes inconsistent (long gaps suggest skipped maintenance)
- Recurring same issue (e.g., "customer states X" multiple times)
- "Customer concern" notes without resolution

### Service Code Decoding (Subaru example)

- PDI = Pre-Delivery Inspection (first sale prep)
- SAS = Subaru Added Security (maintenance plan service)
- INTS = Intermediate service (oil + filter + inspection)
- LOFS = Lube Oil and Filter Service
- CDR = Charging system / battery test
- COR = Check for Open Recalls
- MB4T = Mount and Balance 4 Tires

## OTD Proposal PDF

Dealers send a 1-page "proposal" document with the final OTD numbers. Format varies but usually includes:

### What to Verify

- **VIN match** with listed car
- **Stock #** for internal dealer tracking
- **Mileage** matches what was discussed
- **Sales price** vs the asking price (any reduction?)
- **NJ tax** computed correctly (6.625% on sales + doc fee)
- **Doc fee** within reasonable range ($499-799 NJ)
- **Title fee** ~$60-100 NJ
- **Registration fee** ~$46-84 NJ (varies by car weight)
- **No surprise add-ons** (paint, fabric, nitrogen, etching)
- **Balance Due** matches the breakdown sum

### Common Tricks

- Doc fee at NJ max ($799) without negotiation room
- "Market Value Selling Price" label that does not match actual market
- "Internet Price" footnote requiring lead form unlock (you already did this)
- Add-ons buried at subtotal level

### Math Check

If the dealer's "total" doesn't match: sales + doc + tax + title + reg + add-ons, something is wrong. Ask for itemized clarification.

## CARFAX from Dealer vs Self-Pulled

Some dealers attach the CARFAX PDF, others provide a CARFAX-hosted URL link. Both are equally valid. The PDF is preferred for archival in `dealer_pdfs/` folder.

If the dealer provides only a link, save it; also recommend the user click and save-as-PDF for their records.

## Cross-Reference With Tracker

After PDF analysis, update `dealer_outreach_tracker.md` with:

- 1-owner / multi-owner finding
- Accident history (or absence)
- Specific service records gaps (e.g., "no CVT fluid in records")
- Open recalls (specific to this VIN)
- Any inherited maintenance costs the buyer will face post-sale
- Notable cosmetic notes (e.g., "louie rear bumper" = small paint touch-up done by dealer's in-house painter)

This converts the buyer's hidden risk into known cost. A vehicle with a $500 inherited CVT service due is effectively $500 more expensive than its listed OTD.
