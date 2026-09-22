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

If multiple branches apply (financing + trade + EV), use each relevant checklist
below. Record not applicable or unknown with a reason. The [phase reference](../orchestrator/references/phases.md#phase-9-close)
defines the workflow handoff; this page holds the buyer-type checklists.

### Cash buyer

Pre-arrival (T-1 day):
- [ ] Bank issuance timing, instrument, amount and verified payee confirmed if a cashier's check is used
- [ ] Insurance binder issued; policy number in hand
- [ ] Plate decision finalized (transfer vs new)
- [ ] VIN re-verified against latest dealer paperwork (no last-minute substitution per gotcha D10)
- [ ] PPI complete (`../orchestrator/references/ppi_booking.md` - mobile inspector preferred)

On-site (close day):
- [ ] OTD breakdown in signed agreement matches counter-locked numbers exactly
- [ ] Every tax/fee line checked against current registration-jurisdiction evidence via [state-fee-lookup](../state-fee-lookup/SKILL.md)
- [ ] No padded add-ons (paint protection / nitrogen / etching / VIN etching / theft deterrent)
- [ ] F&I hard-no script ready (see below)
- [ ] Required temporary permit or plates arranged; title/registration responsibilities and official timelines recorded

Post-close (T+1 to T+30):
- [ ] Title/registration delivery checked against the documented process and follow-up date
- [ ] Insurance binder converted to permanent policy

### Financing buyer

Pre-arrival:
- [ ] Lender comparison includes total financing cost and conditional incentives, using [payment methods](../orchestrator/references/payment_methods.md#cash-versus-financed-acquisition)
- [ ] If CU: funding instrument (cashier's check or wire) confirmed pre-close; first-payment date confirmed
- [ ] Prepayment, incentive-clawback and lien terms verified from the actual lender and offer documents
- [ ] Pre-approval expiry and vehicle/funding conditions confirmed; a new application requires authorization
- [ ] Down payment instrument confirmed (cash, debit, or cashier's check)

On-site:
- [ ] Monthly payment math verified at close matches binding-constraint formula
- [ ] APR and term on the contract match pre-approval terms
- [ ] No "payment-packing" via extended warranty or GAP rolled into monthly (see F&I script)

Post-close:
- [ ] If CU loan: title issued to buyer with CU lien notation; CU receives title via mail
- [ ] If captive: title goes to captive direct; buyer's name on registration
- [ ] Actual first-payment date and servicing instructions recorded from the contract

### Trade-in buyer

Pre-arrival (cross-ref `../orchestrator/references/trade_in.md` section 4a-4d if active lien):
- [ ] If lien: 10-day payoff letter from lien-holder in hand (NOT dealer's quote)
- [ ] Lender's payoff and payment instructions confirmed; keep required payments current until payoff is applied
- [ ] Any trade offer used as an anchor remains valid and its inspection/expiry conditions are recorded
- [ ] Key count verified; any deduction is supported by a written valuation or replacement quote
- [ ] All personal items removed; both key fobs ready

On-site:
- [ ] Bill-of-sale shows: trade allowance, lien payoff routing, dealer commitment date
- [ ] Applicable trade-in tax treatment verified from current jurisdictional rules; allowance and lien payoff remain separate
- [ ] No shell-game: ACV and trade allowance NOT confused; sale price and trade negotiated separately

Post-close: record agreed payoff and lien-release milestones, verify each with the
responsible party, and prepare follow-up for missed dates. Reminders or messages
require their own authorization; do not claim monitoring exists without a durable
scheduled task. See [payoff handling](../orchestrator/references/trade_in.md#4-payoff-handling-trade-with-outstanding-loan).

### EV buyer

> **⚠️ Federal §30D POS credit transfer is TERMINATED 2025-09-30 (OBBBA / Public Law
> 119-21).** For any 2026 purchase there is **NO federal $7,500 §30D credit**, no IRS
> ECO registration check, no Form 8936, no Time of Sale report, no $7,500 line item to
> verify at close. Do NOT expect or insert a federal credit line in the signed agreement.
> The §30D items below are retained as **HISTORICAL** (pre-2025-10-01 acquisitions only).
> The only live close-day EV incentive layer is **state/local rebates**, see the bottom
> of this checklist and the CRITICAL banner in `ev-buyer-helper`.

Pre-arrival (LIVE in 2026, cross-ref `../orchestrator/references/ev_buyer_playbook.md`):
- [ ] Battery warranty docs reviewed (new EV) OR SoH report obtained (used EV) per section 6
- [ ] Charging port, adapter compatibility and any needed authorized order confirmed
- [ ] State EV rebate eligibility + paperwork confirmed (MSRP/income caps per state; this is the only live incentive)

Pre-arrival (HISTORICAL, pre-2025-10-01 acquisitions only; §30D terminated 2025-09-30, do NOT use for 2026):
- [ ] ~~Dealer is IRS Energy Credits Online registered~~ (N/A, §30D terminated)
- [ ] ~~Form 8936 ready for signing~~ (N/A, §30D terminated)
- [ ] ~~MAGI under threshold confirmed ($150k single / $300k joint for new; $75k / $150k for used)~~ (N/A, §30D/§25E terminated)

On-site (LIVE in 2026):
- [ ] Battery warranty registered to buyer at delivery (new EV)
- [ ] No EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup ADM line items per gotcha D9 + `../orchestrator/references/ev_buyer_playbook.md` section 8
- [ ] Included charging equipment matches the window sticker or written offer; no assumed standard accessory

On-site (HISTORICAL, pre-2025-10-01 acquisitions only; do NOT apply to a 2026 close):
- [ ] ~~$7,500 reduction shown as separate line item on signed agreement~~ (N/A, §30D terminated; no federal credit line should appear)
- [ ] ~~Time of Sale report copy retained~~ (N/A, §30D terminated)

Post-close:
- [ ] Home charging plan and any authorized installation booking recorded
- [ ] Applicable rebate deadline, eligibility and required documents verified; record a submission only with authorization and receipt

### Pickup-truck buyer

Pre-arrival (cross-ref `../orchestrator/references/vertical_playbooks.md#part-1-pickup-truck-specifics`):
- [ ] Exact VIN/configuration, OEM build information and tow equipment verified against [load/configuration requirements](../orchestrator/references/vertical_playbooks.md#1-establish-the-load-and-configuration)
- [ ] Loaded towing and payload plan checked against all OEM vehicle, axle, hitch and trailer limits, with passengers/gear/tongue weight included
- [ ] Door labels and relevant OEM towing documents retained; no towing approval from a model name or advertisement alone
- [ ] Mechanic's PPI scope addresses frame/corrosion, suspension, drivetrain and towing equipment for this specific vehicle

On-site:
- [ ] Factory vs aftermarket hitch distinction confirmed in writing
- [ ] Brake controller, wiring and hitch assessed using the applicable OEM procedure
- [ ] Commercial, plow and towing history checked; condition and value assessed from records/PPI without default discounts
- [ ] Modifications evaluated for load limits, warranty and insurance implications using [equipment and inspection guidance](../orchestrator/references/vertical_playbooks.md#3-factory-equipment-modifications-and-inspection)

Record the mechanic's findings on frame repairs/corrosion, suspension and towing
wear rather than inferring a diagnosis from a brief drive. Retain labels and OEM
documents for future load planning. See [pickup handoff](../orchestrator/references/vertical_playbooks.md#5-pickup-decision-and-handoff).

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

The scripts below are optional preparation for the buyer. Use a signed-agreement
claim only if that agreement actually exists and says what the script asserts.
Otherwise state the buyer's present terms without inventing a prior commitment.
Have the buyer review the wording and desired response before any external use.
Written messages use [dealer-reply-drafter](../dealer-reply-drafter/SKILL.md);
unsupported languages need an explicitly reviewed alternative.

Translation status: draft terminology for contextual review.

**Add-on name glossary:**

| English (source of truth) | Spanish (spoken) | Note |
|---|---|---|
| OTD / out-the-door price | precio final / precio total ("out the door") | keep "OTD" alongside; dealers use the English acronym |
| doc fee | cargo por documentacion | dealer charge, not a government fee |
| trade-in | vehiculo a cuenta / vehiculo de intercambio | "a cuenta" = applied as credit |
| down payment | enganche / pago inicial | "enganche" is the common term |
| cashier's check | cheque de caja (= cheque de gerencia) | both names = one instrument |
| GAP insurance | seguro GAP (Proteccion Garantizada para Auto) | "seguro GAP" is standard in US docs |
| extended warranty / VSC | garantia extendida / contrato de servicio vehicular | |
| tire-and-wheel | proteccion de llantas y rines | |
| paint protection | proteccion de pintura | |
| ceramic coating | recubrimiento ceramico | |
| key replacement | reemplazo de llave | |
| nitrogen (tire fill) | nitrogeno (en las llantas) | |
| dent / ding (PDR) | reparacion de abolladuras sin pintura | |

> Regional vocabulary note (say what the buyer says): the word for "car" varies by region,
> **carro** (Mexico / Central America / Caribbean), **coche** (Spain / Southern Cone),
> **auto** (neutral, understood everywhere). Mirror the buyer's own word; the scripts
> below use the neutral **vehiculo** to stay region-safe. Technical product names
> (seguro GAP, garantia extendida, doc fee, OTD) stay fixed regardless of region.

**Spanish (ES), hard-no, spoken:**

```
Segun mi acuerdo firmado con fecha {DATE} con {GM_OR_SALES_MGR_NAME},
el precio final (OTD) esta fijado en ${OTD}. Rechazo el seguro GAP,
la garantia extendida (contrato de servicio), la proteccion de
llantas y rines, la proteccion de pintura, el recubrimiento
ceramico, el reemplazo de llave, el nitrogeno, la reparacion de
abolladuras, y cualquier otro complemento que no este en el acuerdo
original. Por favor cierre la venta al OTD acordado, o me retiro y
los dos perdemos el tiempo. Repito: ningun complemento. Solo firmo
el acuerdo original.

{BUYER_NAME}
```

**Spanish (ES), if F&I pushes anyway (reframe), spoken:**

```
Mi acuerdo esta fijado por el OTD, no por el pago mensual. Agregar
$18 al mes por 72 meses son $1,296, no es poca cosa. Lo rechazo.

Por favor muestreme la linea en mi acuerdo firmado que autoriza
este cargo. Si no esta ahi, quitelo; si no puede quitarlo, me retiro
y el trato se cae. Segun mi OTD fijado en ${OTD}, agregar cualquier
cosa es un trato nuevo que yo no he aceptado.

{BUYER_NAME}
```

**Chinese (ZH), hard-no, spoken:**

```
根据我在 {DATE} 与 {GM_OR_SALES_MGR_NAME} 签署的协议,
落地总价 (OTD) 已锁定为 ${OTD}。我拒绝 GAP 保险、延长保修
(服务合同)、轮胎轮毂保障、车漆保护、陶瓷镀膜、配钥匙、
氮气充气、凹痕修复,以及任何不在原始协议中的附加项目。
请按约定的 OTD 完成成交,否则我会离开,我们都浪费时间。
重申:不要任何附加项目。我只签原始协议。

{BUYER_NAME}
```

**Chinese (ZH), if F&I pushes anyway (reframe), spoken:**

```
我的协议锁的是 OTD 总价,不是月供。每月加 $18、分 72 期就是
$1,296,不是小数目。我拒绝。

请在我签署的协议里指出哪一行授权了这笔费用。没有就删掉;
删不掉我就离开,这笔交易作废。按我锁定的 OTD ${OTD},
加任何东西都是我没同意过的新交易。

{BUYER_NAME}
```

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
| Buyer-type close checklists | [Checklists on this page](#sub-checklist-by-buyer-type) |
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
