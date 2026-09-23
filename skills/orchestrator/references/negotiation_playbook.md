# Negotiation Playbook

## Price semantics

Keep three values distinct: the dealer's current written OTD, the buyer's private
`WALK_AWAY` / `walk_away`, and an independently authorized outward `authorized_offer`.
The internal maximum never appears in dealer mail or attachments. Neither an exact
number nor a range derived from it is a disclosure strategy in any round.

An outward proposal needs explicit buyer authorization. The current renderer
requires it to be below the private ceiling and never calls it a cap. With no
approved offer, ask for the complete written quote. An exit can simply say:
"If that does not work, I will continue my search."

## Round 1 Cold Open

Ask for the exact vehicle's complete out-the-door price, with sale, tax, doc,
title, registration, other fees and conditional discounts separated. Supply only
the location and payment details needed and authorized for the quote. Do not
state financing capacity, a maximum monthly payment or a private target range.

Do not promise to close on a date, pay cash or accept financing unless that is
the buyer's current instruction. Lack of a competing quote is a reason to request
information, not a reason to manufacture an anchor.

## Real anchors and evidence

Allowed anchors are a confirmed current listing or a written competing OTD, with
seller, vehicle, new/used class, price basis, amount and observation date recorded.
The private evidence record must include the source artifact/text and SHA-256.
Expiration comes from the quoted validity or a conservative review deadline.
The buyer confirms the source before the record is eligible for outward use.

The executable validator checks artifact integrity, declared timing and field
agreement. It does not authenticate the dealer, independently fetch a source, or
prove that a car is still available. Recheck live availability before commitment.
Never cite the synthetic examples or eval corpus as real market evidence.

Avoid synthesized anecdotes, national averages with no source/sample, assumed
mileage adjustments and "locked" offers that are merely advertised listings.
Keep used and new vehicles separate. Check ownership when two stores are presented
as independent competitors. Use at most one concise anchor sentence per draft.

## OTD math and state rules

Use `scripts/otd_calculator.py` and current state-rule evidence for the supported
transaction branch. Its scope and any unsupported inputs must remain visible.
Do not copy old statewide fee tables or assume every state's tax base is
`sale + doc`. Trade credits, rebates, surtaxes, registration term, vehicle class,
residency and local rates can change the result.

Compare written quotes using identical assumptions. Keep loan payments, trade
payoff, down payment and optional products separate from vehicle OTD. Confirm
every fee and incentive against applicable current sources before saying a
charge is illegal, capped or refundable. A clean algebra check alone does not
verify tax law or dealer quote completeness.

## Counter-Offer Tactics

Select one to three approved asks: complete re-quote, optional add-on removal,
vehicle/inspection confirmation, or an authorized offer. State a suspected
wrong-state fee as a question until its applicability has been checked. Once
confirmed, request a full corrected OTD so the same amount cannot reappear under
another label.

Request removal of dealer markup separately from financing. Do not trade an
unwanted fee for a loan commitment. Cash is a payment method, not a guaranteed
discount; dealers can have financing incentives. Do not promise a savings amount
based on payment method alone.

For a replacement VIN, obtain written availability/sold confirmation and a fresh
line-item quote. Require any comparison adjustment to be explicit, evidenced and
approved. Do not carry an old quote over to a different vehicle silently.

## Walk-Away Lines

Reasons to stop include refusal to provide written terms, mandatory unwanted
products, refusal of an independent inspection, materially inconsistent vehicle
history, or a price above the buyer's private acceptance boundary. The buyer's
decision is private; the outward closing sentence need not explain the boundary.

Use an approved nonnumeric close, leave room for a later revised quote, and avoid
claiming another offer exists when it does not. A generated draft is not a
purchase acceptance and must not contain an unauthorized commitment.

## CPO and mileage comparisons

Verify the actual OEM program, in-service date, mileage, eligibility, warranty
exclusions and dealer enrollment status. Do not convert an advertised program
into confirmed coverage. Warranty value and mileage adjustments need comparable
market evidence; fixed dollar figures in an old playbook are not measurements.

## Test Drive Negotiation Pivot

After inspection/test drive, compare the complete written terms to the private
policy. Continue only within the user's authorization and contingencies. Never
accept a price ABOVE the private `walk_away`; a lower price still requires the
vehicle, title, financing and fee conditions to be acceptable.

## Sequential Dealer Pricing Disclosure

Request the dealer's own written quote first. Later rounds may disclose confirmed
competing evidence and a separately authorized offer. The private ceiling remains
private throughout. Repeat only when there is new information or a buyer-approved
reason; do not create artificial deadlines or untrue competing bids.

## Escalation Ladder When Dealer Delays

Agree on a follow-up deadline with the buyer. A typical optional cadence is one
follow-up after a business day, one final deadline if the buyer wants it, then a
private cold-status entry. These are suggestions, not evidence that a dealer is
stalling. Account for dealer hours, OOO and the buyer's actual close timeline.

Preserve thread continuity and source message IDs. Suppress automated follow-ups
to an absent rep; do not promise re-engagement on a guessed return date. Adding
a new recipient or contacting a general mailbox is an external action and needs
the user's authorization. Log outcomes under the private companion data path.

## Execution

Use `assets/dealer_reply_template.md` and `references/outbound_email_sop.md` for
structured rendering, deterministic checks and receipt-based saving. An uncertain
provider execution must be reconciled, never automatically replayed. Offline
workflow tests do not prove live Gmail handling or actual negotiation savings.
