# Buyer-type close checklists

If multiple branches apply (financing + trade + EV), use each relevant checklist
below. Record not applicable or unknown with a reason. The [phase reference](../../orchestrator/references/phases.md#phase-9-close)
defines the workflow handoff; this page holds the buyer-type checklists.

### Cash buyer

Pre-arrival (T-1 day):
- [ ] Bank issuance timing, instrument, amount and verified payee confirmed if a cashier's check is used
- [ ] Insurance binder issued; policy number in hand
- [ ] Plate decision finalized (transfer vs new)
- [ ] VIN re-verified against latest dealer paperwork (no last-minute substitution per gotcha D10)
- [ ] PPI complete (`../../orchestrator/references/ppi_booking.md` - mobile inspector preferred)

On-site (close day):
- [ ] OTD breakdown in signed agreement matches counter-locked numbers exactly
- [ ] Every tax/fee line checked against current registration-jurisdiction evidence via [state-fee-lookup](../../state-fee-lookup/SKILL.md)
- [ ] No padded add-ons (paint protection / nitrogen / etching / VIN etching / theft deterrent)
- [ ] F&I hard-no script ready (see the [refusal script](../SKILL.md#fi-refusal-script))
- [ ] Required temporary permit or plates arranged; title/registration responsibilities and official timelines recorded

Post-close (T+1 to T+30):
- [ ] Title/registration delivery checked against the documented process and follow-up date
- [ ] Insurance binder converted to permanent policy

### Financing buyer

Pre-arrival:
- [ ] Lender comparison includes total financing cost and conditional incentives, using [payment methods](../../orchestrator/references/payment_methods.md#cash-versus-financed-acquisition)
- [ ] If CU: funding instrument (cashier's check or wire) confirmed pre-close; first-payment date confirmed
- [ ] Prepayment, incentive-clawback and lien terms verified from the actual lender and offer documents
- [ ] Pre-approval expiry and vehicle/funding conditions confirmed; a new application requires authorization
- [ ] Down payment instrument confirmed (cash, debit, or cashier's check)

On-site:
- [ ] Monthly payment math verified at close matches binding-constraint formula
- [ ] APR and term on the contract match pre-approval terms
- [ ] No "payment-packing" via extended warranty or GAP rolled into monthly (see the [F&I script](../SKILL.md#fi-refusal-script))

Post-close:
- [ ] If CU loan: title issued to buyer with CU lien notation; CU receives title via mail
- [ ] If captive: title goes to captive direct; buyer's name on registration
- [ ] Actual first-payment date and servicing instructions recorded from the contract

### Trade-in buyer

Pre-arrival (cross-ref `../../orchestrator/references/trade_in.md` section 4a-4d if active lien):
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
scheduled task. See [payoff handling](../../orchestrator/references/trade_in.md#4-payoff-handling-trade-with-outstanding-loan).

### EV buyer

Apply the [EV incentive rules](../SKILL.md#ev-incentive-status) before using this
branch. Historical rows below exclude 2026 purchases.

Pre-arrival (LIVE in 2026, cross-ref `../../orchestrator/references/ev_buyer_playbook.md`):
- [ ] Battery warranty docs reviewed (new EV) OR SoH report obtained (used EV) per section 6
- [ ] Charging port, adapter compatibility and any needed authorized order confirmed
- [ ] State EV rebate eligibility + paperwork confirmed (MSRP/income caps per state; this is the only live incentive)

Pre-arrival (HISTORICAL, pre-2025-10-01 acquisitions only; §30D terminated 2025-09-30, do NOT use for 2026):
- [ ] ~~Dealer is IRS Energy Credits Online registered~~ (N/A, §30D terminated)
- [ ] ~~Form 8936 ready for signing~~ (N/A, §30D terminated)
- [ ] ~~MAGI under threshold confirmed ($150k single / $300k joint for new; $75k / $150k for used)~~ (N/A, §30D/§25E terminated)

On-site (LIVE in 2026):
- [ ] Battery warranty registered to buyer at delivery (new EV)
- [ ] No EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup ADM line items per gotcha D9 + `../../orchestrator/references/ev_buyer_playbook.md` section 8
- [ ] Included charging equipment matches the window sticker or written offer; no assumed standard accessory

On-site (HISTORICAL, pre-2025-10-01 acquisitions only; do NOT apply to a 2026 close):
- [ ] ~~$7,500 reduction shown as separate line item on signed agreement~~ (N/A, §30D terminated; no federal credit line should appear)
- [ ] ~~Time of Sale report copy retained~~ (N/A, §30D terminated)

Post-close:
- [ ] Home charging plan and any authorized installation booking recorded
- [ ] Applicable rebate deadline, eligibility and required documents verified; record a submission only with authorization and receipt

### Pickup-truck buyer

Pre-arrival (cross-ref `../../orchestrator/references/vertical_playbooks.md#part-1-pickup-truck-specifics`):
- [ ] Exact VIN/configuration, OEM build information and tow equipment verified against [load/configuration requirements](../../orchestrator/references/vertical_playbooks.md#1-establish-the-load-and-configuration)
- [ ] Loaded towing and payload plan checked against all OEM vehicle, axle, hitch and trailer limits, with passengers/gear/tongue weight included
- [ ] Door labels and relevant OEM towing documents retained; no towing approval from a model name or advertisement alone
- [ ] Mechanic's PPI scope addresses frame/corrosion, suspension, drivetrain and towing equipment for this specific vehicle

On-site:
- [ ] Factory vs aftermarket hitch distinction confirmed in writing
- [ ] Brake controller, wiring and hitch assessed using the applicable OEM procedure
- [ ] Commercial, plow and towing history checked; condition and value assessed from records/PPI without default discounts
- [ ] Modifications evaluated for load limits, warranty and insurance implications using [equipment and inspection guidance](../../orchestrator/references/vertical_playbooks.md#3-factory-equipment-modifications-and-inspection)

Record the mechanic's findings on frame repairs/corrosion, suspension and towing
wear rather than inferring a diagnosis from a brief drive. Retain labels and OEM
documents for future load planning. See [pickup handoff](../../orchestrator/references/vertical_playbooks.md#5-pickup-decision-and-handoff).
