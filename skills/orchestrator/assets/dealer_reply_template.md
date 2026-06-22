# Dealer Reply Templates

## Voice Specification (mandatory: read before drafting)

Every outbound dealer email must conform to the voice rules below. These are not stylistic preferences; they are the consistent persona the buyer is presenting across cross-bid dealers, and drift kills leverage (rep A and rep B compare notes; if the buyer sounds like a different buyer in two threads, the cross-bid signal is suspect).

**Tone rules:**

- Direct, no hedging. Write "I am asking you to remove the EV Prep Fee", NOT "I would appreciate if you could possibly look at removing the EV Prep Fee".
- No softeners ("just", "maybe", "I was wondering if", "if it's not too much trouble", "hope you're well", "hope this finds you well"). Cut them in revision.
- No flattery. Skip "great car!", "love your dealership", "your team has been wonderful". Move to the ask.
- One thank-you per email, at the open (acknowledge the prior touch). Do not repeat in the close.
- Numbered asks when there are 2+ asks. Free-form paragraphs only when there is exactly 1 ask.
- Anchor presentation: dealer name + dollar amount + 1-line context, on a single line. Never paragraph-form an anchor. Example: `Hoffman Honda has a comparable 2023 Outback Limited at $27,900 ask.` Not: `So I've been looking at this other dealership called Hoffman Honda and they actually have a really similar 2023 Outback Limited that they're asking $27,900 for, which is interesting because...`

**Buyer-voice variants (pick ONE per session, hold across all dealer threads):**

| Variant | Opening profile line | OTD framing | Walk-away framing |
|---|---|---|---|
| Cash buyer | "I am a cash buyer in {CITY} {STATE}, ready to close this week with a cashier's check." | "OTD all-in (sale + tax + doc + title + reg)" | "Above ${WALK} OTD I walk to my other anchors." |
| Financing buyer | "I have a pre-approval from {LENDER} at {APR}% / {TERM}mo, ${DOWN} cash down." | "Effective OTD cap from monthly + down is ${EFFECTIVE}." | "Above ${WALK} OTD or ${MAX_MONTHLY}/mo I walk." |
| EV buyer (state rebate) | "I am an EV buyer in {CITY} {STATE}, closing this week. NOTE: the federal $7,500 / $4,000 / §45W EV credits were terminated for vehicles acquired after 2025-09-30 (OBBBA, Public Law 119-21); do not quote them in the OTD. Confirm whether {STATE} rebate {PROGRAM} is still funded and how it applies." | "Net OTD after any state/local rebate (no federal credit)" | "Above ${WALK} net OTD I walk." |

Once a variant is chosen, every dealer email in that cycle uses the same opening profile line, the same OTD framing label, and the same walk-away framing.

**Length rules (hard caps, enforced by Outbound Email SOP Step 0):**

- First-touch: 10-15 content lines (greeting + buyer profile + vehicle ID + 5-line OTD breakdown ask + walk-away + sign-off).
- Counter: ~10 content lines, hard cap. 3 numbered asks max + 1 anchor sentence + 1 walk-away line.
- Follow-up / nudge: 4-6 content lines. 1 specific ask.
- F&I close-day script: paste verbatim, ~7 lines, do not edit length.

**Format rules (cross-reference Rule #1 + `references/email_format_rules.md`):**

- Plain ASCII only. No em-dash, en-dash, curly quotes, backticks, markdown bold/italic, markdown link syntax.
- No emojis under any circumstance.
- No jargon without first-use gloss in the same email. OTD, F&I, ADM, CPO, NACS need parenthetical on first use per Phase 1 jargon glossing rule. After first use in the same email, drop the gloss.

**Sign-off (mandatory, hold consistent across all threads in a cycle):**

Use exactly one of these two patterns, and pick ONE for the whole cycle:

```
Thanks,

{BUYER_FIRST_NAME}
```

OR (more formal, use only if the buyer's preferred persona is formal):

```
Best,

{BUYER_FIRST_NAME} {BUYER_LAST_NAME}
```

Do NOT mix "Thanks," in one thread and "Best," in another. Do NOT use "Best regards", "Sincerely", "Kind regards", "Warm regards", "Cheers", "All best", "Many thanks", or any other closer; these read as either too formal (legal-letter tone) or too casual (chat tone) and break the consistent buyer voice.

## Voice Red Flags (signal the agent is improvising, not using the template)

If any of these appear in a draft, the agent has drifted off-template. Strip them before saving:

| Red flag | Correction |
|---|---|
| "I hope you're well" / "I hope this finds you well" / "Hope all is well" | Delete entirely. Open with "Hi {NAME}," then the thanks-for-the-quote line. |
| "Best regards" / "Sincerely" / "Kind regards" / "Warm regards" | Replace with "Thanks," or "Best," per the sign-off rule above. |
| "team" instead of specific rep name (e.g., "Hi team," "thanks to the team") | Replace with the rep's actual name ({DEALER_REP_NAME}). If rep name is unknown, ask buyer or pull from the dealer's signature in the prior thread. Never address a counter to "team". |
| "I would appreciate if you could" / "It would be great if you could" / "Would it be possible to" | Replace with imperative: "Please remove", "Please re-quote", "I am asking you to". |
| "Just checking in" / "Just following up" / "Just wanted to ask" | Drop "just". Use "Following up on my {DATE} note." |
| "Sorry to bother you" / "I know you're busy" | Delete entirely. The dealer's job is to respond; no apology needed for asking. |
| "I think" / "I feel like" / "Maybe" / "Possibly" / "Perhaps" | Drop the hedge. State the position directly. |
| "I love this car" / "Beautiful car" / "Excited about" | Delete flattery; move to the ask. |
| Paragraph-form anchor (3+ sentences on one competitor's number) | Compress to one line: `{Dealer} {trim} at ${OTD} OTD, {miles} mi.` |
| Two or more thank-yous in one email | Cut to one, at the open. |
| Em-dash anywhere (U+2014) | Per Rule #1: replace with comma, colon, period, or ASCII hyphen-minus. |
| "Best, --" sign-off with dashes | Drop the dashes; use plain "Best," (or "Thanks,") per sign-off rule. |
| Mixed buyer-voice variant in the same cycle (e.g., one thread "cash buyer ready to close" + another thread "I have pre-approval from my credit union") | Pick one variant per session and hold across all dealers. If the buyer's posture changed mid-cycle, trigger Mid-Cycle Pivot Protocol; do not silently switch voice. |
| Bilingual content in dealer-facing email (Chinese characters, Spanish text, non-English glosses) | Dealer-facing emails are ALWAYS English-only, ASCII-only. See SKILL.md § Language and audience separation. |

When unsure, paste the draft into a plain text editor and re-read it as if you were the dealer rep. If it reads as "different buyer than last email" or "this person is going to be hard to close because they don't know what they want", the voice has drifted; rewrite from the template.

---

**SEND TIMING (mandatory for every email below):**

Send between 9 AM and 5 PM Mon-Thu dealer-local time. Best window is 9 AM - 12 PM dealer-local (sales desk fresh, same-day reply most likely). AVOID:
- Mon-Thu after 5 PM through next 9 AM (lands at bottom of next-day inbox)
- Friday after 12 PM (lands in weekend autoresponder bucket; Mon reply lag)
- Saturday + Sunday (read Monday behind weekend backlog)
- 11 PM - 7 AM dealer-local (rep treats as low-priority)

For multi-state cross-bid, use the earliest dealer-local 9 AM among the cohort as the send time. After-hours sends lose first-mover edge on parallel cross-bids because reps reply in inbox-surface order. See `SKILL.md` § Outbound Email SOP Step 5 for the full advisory + override protocol.

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

## Close-Day F&I Hard-No (Per Gotcha P3)

Use at the F&I (Finance & Insurance) office when add-ons are pitched after the OTD is locked in writing. Read verbatim or hand over a printed copy. Plain ASCII, no markdown.

```
Per my signed agreement dated {DATE} with {GM_OR_SALES_MGR_NAME},
the OTD is locked at ${OTD}. I decline GAP, VSC, tire-and-wheel,
paint protection, key replacement, nitrogen, dent / ding, and any
other add-on not in the original agreement. Please process the
close at the agreed OTD, or I will exit and we will both lose
time. Repeat: NO add-ons. I will sign only the original
agreement.

{BUYER_NAME}
```

### Pre-Close-Day F&I Heads-Up Email (Send to GM ~24h Before Close)

Send to the GM (the one on the signed agreement) BEFORE driving to the dealer. Pre-empts most close-day F&I friction by routing the no-add-ons signal to F&I before the buyer walks in.

```
Hi {GM_NAME},

Confirming the OTD at ${OTD} per our agreement dated {AGREEMENT_DATE}.

A quick heads-up so we don't burn time at close: I will decline any
F&I add-ons (GAP, VSC, tire-and-wheel, paint protection, key
replacement, nitrogen, dent / ding, and any other line not in the
original agreement). This has been my posture from Day 1; not a
last-minute change.

Please brief your F&I officer so we can move through the
paperwork at the locked OTD without back-and-forth on add-ons.

Close-day logistics:
- Time window: {TIME_WINDOW}
- Funding instrument: {CASHIERS_CHECK_OR_WIRE}
- Insurance binder: {CARRIER and POLICY_NUMBER}
- Plate decision: {TRANSFER_OR_NEW}
- ID set: {ID_LIST}

Thanks,

{BUYER_NAME}
```

### F&I Add-On Reframe (Use If F&I Pushes Anyway)

If the F&I officer pitches an add-on as "required" or shifts the math to monthly payment ("only $18/mo extra"), reply:

```
My agreement is OTD-locked, not monthly-locked. Adding $18/mo for
72 months is $1,296, not a small amount. I decline.

Please show me the line item in my signed agreement that
authorizes this charge. If it's not there, remove it; if you
cannot remove it, I will exit and the deal is dead. Per my OTD
lock at ${OTD}, adding anything constitutes a new deal that I have
not agreed to.

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
