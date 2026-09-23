---
name: close-day-checklist
description: Use when buyer is ready to close (signing today/tomorrow), needs the day-of checklist for cash / financing / trade-in / EV / pickup buyers, F&I add-on refusal script, and timing of cashier's check / lien payoff / plate transfer. Triggers include "ready to close", "close day checklist", "F&I add-on refusal", "lien payoff timing", "提车清单", "准备签约", and Spanish phrases "lista para el dia de firma", "listo para cerrar el trato".
---

# Close Day Checklist

Prepare the buyer for an inspection, final contract review and collection using
current written evidence. Verify applicable fees, warranty, incentives and seller
terms against their sources. A completed checklist is preparation for the buyer's
decision, not proof that a vehicle is suitable or a purchase succeeded.

Reuse known criteria and the current buyer research package. For a visit before
terms are locked, fill the private [negotiation and visit preparation](../orchestrator/assets/negotiation_prep_template.md)
with unknowns and questions; a test drive does not require two competing quotes.
Use [dealer-reply-drafter](../dealer-reply-drafter/SKILL.md) for a revised written
offer. Save real notes under verified private DATA. Sending, booking, paying or
signing requires authorization for that action and an execution receipt.

## When To Use

- Buyer is signing today or tomorrow and needs a sub-checklist by buyer type
- Buyer wants the F&I add-on refusal script to read verbatim at the F&I desk
- Buyer has a trade with active lien and needs the payoff workflow
- Buyer is an EV buyer and needs day-of EV mechanics (state rebate paperwork, battery/SoH, charging, NOTE: federal §30D POS credit transfer is TERMINATED 2025-09-30, historical only)
- Buyer is buying a pickup and needs the truck-specific PPI quick checklist

## When NOT To Use

- For broad vehicle research, use [buy-me-a-car](../orchestrator/SKILL.md).
- Before signing, resolve missing written terms, history/title evidence and material
  inspection findings. Use [CARFAX review](../carfax-pdf-review/SKILL.md) and
  [inspection planning](../ppi-scheduler/SKILL.md) when relevant.
- Changed terms at the F&I desk require a fresh comparison and buyer decision;
  do not treat an earlier agreement as authorization to accept the changes.

## Evidence and communication

- Read the actual history/title and service records for a used vehicle; for a new
  vehicle, review the window sticker and delivery inspection record. Record missing
  pages and unresolved claims using the [PDF checklist](../orchestrator/references/pdf_review_checklist.md).
- Buyer-facing notes use the buyer's language. The constrained dealer-email
  renderer supports ASCII English; follow its reviewed draft contract and the
  [email SOP](../orchestrator/references/outbound_email_sop.md) for external messages.
- Keep private ceilings and negotiation notes out of dealer-facing documents.

## Close-Day Re-Confirmation (do this BEFORE buyer drives to dealer)

Re-read the private criteria and visit preparation; verify changed or unresolved
logistics instead of asking the buyer to repeat known facts:

- Bank cut-off + branch + hours (cashier's check issued same morning?)
- Insurance carrier (for binder + policy number)
- Plate decision (transfer existing versus new plates; verify eligibility and fees)
- Available time windows on close day
- ID set (driver's license, secondary ID, proof of residence)
- Funding instrument (cash, cashier's check, wire, captive financing, CU financing)

Any change since Phase 1 (carrier switched, branch closed for holiday, plate decision flipped) must be caught NOW, not at the dealer.

## Sub-Checklist by Buyer Type

If multiple branches apply (financing + trade + EV), read and use each relevant
checklist before preparing the close-day plan. Record not applicable or unknown
with a reason. The [phase reference](../orchestrator/references/phases.md#phase-9-close)
defines the workflow handoff.

| Buyer type | Read on demand |
|---|---|
| Cash | [Cash-buyer checklist](references/buyer-type-checklists.md#cash-buyer) |
| Financing | [Financing-buyer checklist](references/buyer-type-checklists.md#financing-buyer) |
| Trade-in | [Trade-in-buyer checklist](references/buyer-type-checklists.md#trade-in-buyer) |
| EV | [EV-buyer checklist](references/buyer-type-checklists.md#ev-buyer) |
| Pickup truck | [Pickup-truck checklist](references/buyer-type-checklists.md#pickup-truck-buyer) |

### EV incentive status

> **⚠️ Federal §30D POS credit transfer is TERMINATED 2025-09-30 (OBBBA / Public Law
> 119-21).** For any 2026 purchase there is **NO federal $7,500 §30D credit**, no IRS
> ECO registration check, no Form 8936, no Time of Sale report, no $7,500 line item to
> verify at close. Do NOT expect or insert a federal credit line in the signed agreement.
> The §30D items in the EV checklist are retained as **HISTORICAL** (pre-2025-10-01 acquisitions only).
> The only live close-day EV incentive layer is **state/local rebates**, see the EV checklist and the CRITICAL banner in `ev-buyer-helper`.

## F&I refusal script

Use a signed-agreement claim only when that agreement exists and supports it.
Otherwise state the buyer's current requested terms without inventing an agreement.

Read verbatim or hand printed copy at the F&I (Finance & Insurance) desk when add-ons are pitched after the OTD is locked in writing. Plain ASCII, NO markdown:

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

### If F&I pushes anyway (reframe)

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

### Buyer-language refusal preparation

The linked scripts are optional preparation for the buyer. Use a signed-agreement
claim only if that agreement actually exists and says what the script asserts.
Otherwise state the buyer's present terms without inventing a prior commitment.
Have the buyer review the wording and desired response before any external use.
Written messages use [dealer-reply-drafter](../dealer-reply-drafter/SKILL.md);
unsupported languages need an explicitly reviewed alternative.

For Spanish or Chinese spoken preparation, read the [glossary and refusal scripts](references/buyer-language-refusal.md) on demand. Translation status: draft terminology for contextual review.

### Prepare a close-day heads-up draft

If useful, prepare the specific recipient and content with
[dealer-reply-drafter](../dealer-reply-drafter/SKILL.md) and its
[executable template contract](../orchestrator/assets/dealer_reply_template.md#executable-plan).
Send only within existing authorization; retain the provider receipt. Include:

- Confirm locked OTD with agreement date
- Decline list (GAP, VSC, tire-and-wheel, paint, key, nitrogen, dent/ding)
- Close-day logistics: time window, funding instrument, insurance binder, plate decision, ID set

## Universal Cross-References

| Need | Open |
|---|---|
| Buyer-type close checklists | [Buyer-type checklists](references/buyer-type-checklists.md) |
| Workflow handoff | [Phase 9](../orchestrator/references/phases.md#phase-9-close) |
| Price ladder, visit questions, decision matrix and backup | [Private visit preparation](../orchestrator/assets/negotiation_prep_template.md) |
| Lien payoff full workflow | `../orchestrator/references/trade_in.md` section 4a-4d |
| EV federal credit status (§30D/§25E/§45W all TERMINATED 2025-09-30, historical) + live state rebates | `../orchestrator/references/ev_buyer_playbook.md` section 1; `ev-buyer-helper` CRITICAL banner |
| Pickup-specific PPI items | [Equipment and inspection](../orchestrator/references/vertical_playbooks.md#3-factory-equipment-modifications-and-inspection) |
| Applicable tax and fees | [State fee lookup](../state-fee-lookup/SKILL.md) and [review rules](../orchestrator/references/state_fees.md#review-rules) |
| F&I refusal preparation | [Script on this page](#fi-refusal-script) and [buyer-language preparation](#buyer-language-refusal-preparation) |
| Financing close-day instruments | `../orchestrator/references/payment_methods.md` |
| CPO enrollment at close | per-OEM CPO programs in `../orchestrator/references/` (subaru_cpo_program.md, honda_cpo_program.md, etc.) |
| HD pickup / commercial van / luxury close routing | [Close-day routing](../orchestrator/references/vertical_playbooks.md#6-quick-reference-phase-9-close-day-routing) |
| Lease-end options | `../orchestrator/references/lease_playbook.md` section Lease-end options |

## Stop Conditions

- A visit may proceed with a clear inspection purpose and recorded open questions;
  unresolved material terms or inspection concerns block a purchase recommendation.
- Before signing or paying, resolve the applicable funding, insurance, title,
  vehicle and contract requirements with evidence. The buyer makes the decision.
- If the seller changes terms or refuses an agreed condition, update the private
  decision matrix and compare alternatives. Do not accept or send a counter automatically.
- For a missed payoff milestone, prepare a documented follow-up under the existing
  authorization and lender instructions; never report a lien released without proof.

## Deliverable

Return the updated private visit-preparation path, completed/relevant checklist,
unresolved questions, document references and next authorized action. After a visit,
record actual findings and the buyer's decision, and refresh the buyer research
HTML/PDF when the conclusion changes. Distinguish prepared, booked, inspected,
signed and collected using the evidence for each state.

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
