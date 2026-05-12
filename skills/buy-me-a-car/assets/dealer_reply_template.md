# Dealer Reply Templates

**FORMAT RULE (mandatory for every email below and every bulk outreach message):**

All emails to dealers are PLAIN ASCII. Forbidden characters:
- em-dash (the long dash, U+2014)
- en-dash (U+2013)
- markdown bold/italic markers (double-asterisks, underscores around words)
- backticks
- markdown link syntax (square brackets and parens around URLs)
- curly quotes

Substitute em-dash with: comma, colon, period and new sentence, or ASCII hyphen-minus. See `references/email_format_rules.md` for the complete substitution table.

Verify each draft body for these characters before saving with `create_draft`.

## Initial OTD Ask (after dealer's first generic reply)

```
Hi {DEALER_REP_NAME},

Thanks for the quick response. To save us both time, I evaluate all deals by email before any in-person visit.

The vehicle I am interested in is the {YEAR MAKE MODEL TRIM} (VIN {VIN}, Stock {STOCK}) listed at ${PRICE} with {MILES} miles.

I am a cash buyer in {CITY} {STATE} (ZIP {ZIP}), ready to close this week pending an independent pre-purchase inspection.

Could you email me a written OTD price for this unit, broken out as:
- Sales price
- {STATE} sales tax ({TAX_RATE}%)
- Doc fee
- Title fee
- Registration fee
- Any other fees or add-ons

A clean OTD number by email is all I need to decide. I am comparing several similar units this week. First dealer with the right number gets the PPI slot and same-week cashier's check.

Thanks!

{BUYER_NAME}
{BUYER_EMAIL}
{BUYER_PHONE}
```

## Counter-Offer with Anchors

```
Hi {DEALER_REP_NAME},

Reviewed the OTD proposal. Confirming the details:

- {YEAR MODEL TRIM} ({VIN})
- {MILES} miles
- ${PRICE} sales + ${DOC} doc + ${TAX} tax + ${REG} reg = ${OTD} OTD

After running against my benchmarks and market data, here is where I can commit.

Data points:

1. Mileage: at {MILES}, this is {DELTA} more than the comparable car on my list (a {COMPARABLE} at ${COMP_OTD} OTD). Standard mileage adjustment of $0.10 to $0.15 per mile puts this ${DELTA_DOLLARS} below.

2. {OTHER_DATA_POINT_2}.

3. {OTHER_DATA_POINT_3}.

4. Market comp: regional median for this trim and mileage on AutoTrader / KBB is ${MARKET_LOW} to ${MARKET_HIGH}.

For the price, my target to commit is ${TARGET_OTD} OTD. Possible structures:

- Sales ${SALES_A} + Doc ${DOC_A} + Tax + Reg, approximately ${TARGET_OTD} OTD
- Or Sales ${SALES_B} + Doc ${DOC_B} + Tax + Reg, approximately ${TARGET_OTD} OTD
- Or any combination that gets there

I respect this is a meaningful ask. If ${TARGET_OTD} does not pencil out, I will move forward with my other offer. Cash close this week with cashier's check if it works.

Thanks!

{BUYER_NAME}
{BUYER_EMAIL}
{BUYER_PHONE}
```

## Refusing In-Person-Only Pricing

```
Hi {DEALER_REP_NAME},

I appreciate the offer, but I evaluate all deals by email/text before any in-person visit. This is non-negotiable with multiple OTD quotes already on the table.

If your managers can email a written OTD on the {VEHICLE}, broken down as sales price + {STATE} tax + doc + title + reg, I will keep your dealership in consideration.

For reference, I currently have:
- {COMPETING_OFFER_1}
- {COMPETING_OFFER_2}

If your number lands in that range by email, we have a deal.

If pricing strictly requires an in-person visit, I understand and will go with my current best offers. Thanks!

{BUYER_NAME}
{BUYER_EMAIL}
{BUYER_PHONE}
```

## CARFAX / Service Records Request

```
Hi {DEALER_REP_NAME},

Thanks for the OTD. Before I commit, a few verification asks:

1. CARFAX report: could you forward the PDF? Single owner, no accidents, no salvage / lemon / flood title brands, no open recalls?

2. Pre-sale inspection: what did your service team find in their recent inspection? Tire tread, brake pad thickness, battery test reading, fluid conditions?

3. Service records: any maintenance history from the previous owner that you can share?

4. Open recalls: anything outstanding for this VIN?

If everything checks out, I am ready for an independent PPI and same-week close. Thanks!

{BUYER_NAME}
{BUYER_EMAIL}
{BUYER_PHONE}
```

## PPI Logistics Confirmation

```
Hi {DEALER_REP_NAME},

For the pre-purchase inspection, my preference is to bring an independent ASE-certified mobile mechanic to your premises. Estimated 1-2 hour inspection, no lift required.

Alternative: I can deliver the vehicle to a local shop within 5 miles of your dealership for a quick visit inspection.

Which works better on your end? Also, what is the earliest PPI slot available?

Thanks!

{BUYER_NAME}
```

## Walk-Away (Polite Close)

```
Hi {DEALER_REP_NAME},

Understood, and I respect your pricing policy.

For my needs and budget this week, the numbers do not pencil out at ${OTD} versus my comparable offers, so I will move forward with my other option. If anything changes on your end (price adjustment, a similar unit at a more competitive number, new arrival), please feel free to reach back out.

Wishing you the best on the sale.

Thanks!

{BUYER_NAME}
```

## Accept and Schedule PPI

```
Hi {DEALER_REP_NAME},

The ${OTD} OTD works. Here is the path to close:

1. PPI by my ASE-certified mobile mechanic, scheduled for {DAY_TIME} at your premises.
2. Subject to PPI passing, I will return with cashier's check on {CLOSING_DAY}.
3. Plate transfer: I will bring my existing {STATE} plates and current registration.
4. Subaru CPO enrollment (if applicable): please confirm this is included.

Could you confirm the PPI slot and prep the paperwork?

Thanks!

{BUYER_NAME}
```

## Hold / Deposit Request

```
Hi {DEALER_REP_NAME},

I would like to lock in this vehicle pending my Wednesday PPI. What is your hold / deposit policy? Refundable? Non-refundable? Amount?

If a small refundable deposit (e.g., $500) is sufficient, I can wire / Zelle that today.

Thanks!

{BUYER_NAME}
```

## Add-On Refusal

```
Hi {DEALER_REP_NAME},

Please remove the following add-ons from the proposal. I am not interested in dealer-installed accessories:

- {ADD_ON_1}
- {ADD_ON_2}

I want only: base sales price + state tax + doc fee + title + registration.

Thanks!

{BUYER_NAME}
```

## Refusal of Phone-Only Communication

```
Hi {DEALER_REP_NAME},

I prefer email/text for all transaction details. Phone is fine for quick coordination (test drive timing, hold confirmation) but pricing and OTD discussions need to be in writing.

Could you continue our discussion by email? My address is {EMAIL}.

Thanks!

{BUYER_NAME}
```

## Final Pricing Summary

```
Hi {DEALER_REP_NAME},

Confirming the final terms for the {VEHICLE}:

- VIN: {VIN}
- Sales price: ${PRICE}
- Doc fee: ${DOC}
- {STATE} sales tax (${TAX_RATE}%): ${TAX}
- Title fee: ${TITLE}
- Registration: ${REG}
- Other / add-ons: ${OTHER}
- {TOTAL_LABEL}: ${OTD}

Plate transfer: {YES_NO}, {existing plates / new plates}
PPI scheduled: {DATE_TIME}
Cashier's check delivery: {DATE_TIME}

Please confirm this matches your records and email a final purchase agreement / bill of sale.

Thanks!

{BUYER_NAME}
```
