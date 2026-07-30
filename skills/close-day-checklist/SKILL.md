---
name: close-day-checklist
description: Use when buyer is ready to close (signing today/tomorrow), needs the day-of checklist for cash / financing / trade-in / EV / pickup buyers, F&I add-on refusal script, and timing of cashier's check / lien payoff / plate transfer. Triggers include "ready to close", "close day checklist", "F&I add-on refusal", "lien payoff timing", "提车清单", "准备签约", and Spanish phrases "lista para el dia de firma", "listo para cerrar el trato".
---

# Close Day Checklist

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> last_verified: 2026-05-18

Narrow sub-skill: buyer has a locked OTD in writing and is heading to the dealer to sign. No re-negotiation, no fresh outreach. For the full 9-phase workflow load `../orchestrator/SKILL.md`; for upstream counter / follow-up drafting load `dealer-reply-drafter`.

## When To Use

- Buyer is signing today or tomorrow and needs a sub-checklist by buyer type
- Buyer wants the F&I add-on refusal script to read verbatim at the F&I desk
- Buyer has a trade with active lien and needs the payoff workflow
- Buyer is an EV buyer and needs day-of EV mechanics (state rebate paperwork, battery/SoH, charging, NOTE: federal §30D POS credit transfer is TERMINATED 2025-09-30, historical only)
- Buyer is buying a pickup and needs the truck-specific PPI quick checklist

## When NOT To Use

- OTD not yet locked in writing (use orchestrator Phase 6 / `dealer-reply-drafter` first)
- CARFAX not yet reviewed (use `carfax-pdf-review` sub-skill)
- PPI not yet booked (use `../orchestrator/references/ppi_booking.md`)
- Buyer wants to renegotiate at the F&I desk (don't - escalate per gotcha P3 F&I hard-no script)

## Critical Rules Invoked

- **Critical Rule #4: Read the actual CARFAX PDF yourself.** Verbal "clean 1-owner" has a real failure rate. See gotcha V2. Re-confirm CARFAX was read end-to-end BEFORE close day.
- **Critical Rule #1: Plain ASCII in every outbound email.** Close-day GM heads-up email + F&I hard-no email must be ASCII only.

## Close-Day Re-Confirmation (do this BEFORE buyer drives to dealer)

Re-read the close-day logistics mini-table from `criteria.md` and confirm each line:

- Bank cut-off + branch + hours (cashier's check issued same morning?)
- Insurance carrier (for binder + policy number)
- Plate decision (transfer existing vs new plates - saves $25-150 in most states)
- Available time windows on close day
- ID set (driver's license, secondary ID, proof of residence)
- Funding instrument (cash, cashier's check, wire, captive financing, CU financing)

Any change since Phase 1 (carrier switched, branch closed for holiday, plate decision flipped) must be caught NOW, not at the dealer.

## Sub-Checklist by Buyer Type

If multiple branches apply (financing + trade + EV), execute all of them. Full detail in `../orchestrator/references/phases.md#phase-9--close`.

### Cash buyer

Pre-arrival (T-1 day):
- [ ] Cashier's check confirmed ready for issue by bank cut-off (~9-10 AM); buffer for same-day
- [ ] Insurance binder issued; policy number in hand
- [ ] Plate decision finalized (transfer vs new)
- [ ] VIN re-verified against latest dealer paperwork (no last-minute substitution per gotcha D10)
- [ ] PPI complete (`../orchestrator/references/ppi_booking.md` - mobile inspector preferred)

On-site (close day):
- [ ] OTD breakdown in signed agreement matches counter-locked numbers exactly
- [ ] All line items cross-checked against `../orchestrator/references/state_fees.md` registering-state "Does NOT have" list (gotcha D8)
- [ ] No padded add-ons (paint protection / nitrogen / etching / VIN etching / theft deterrent)
- [ ] F&I hard-no script ready (see below)
- [ ] Temp permit issued at close; confirm permanent title timeline (4-8 weeks)

Post-close (T+1 to T+30):
- [ ] Title arrived in mail; if not, follow up at T+30
- [ ] Insurance binder converted to permanent policy

### Financing buyer

Pre-arrival:
- [ ] Captive-vs-CU decision resolved per `../orchestrator/references/payment_methods.md` (gotcha D9 sub-rule: not coupled to ADM or other concessions)
- [ ] If CU: funding instrument (cashier's check or wire) confirmed pre-close; first-payment date confirmed
- [ ] If captive: no rebate clawback on early payoff; lender lien notation on title
- [ ] Pre-approval re-pulled if approaching 30-day expiry
- [ ] Down payment instrument confirmed (cash, debit, or cashier's check)

On-site:
- [ ] Monthly payment math verified at close matches binding-constraint formula
- [ ] APR and term on the contract match pre-approval terms
- [ ] No "payment-packing" via extended warranty or GAP rolled into monthly (see F&I script)

Post-close:
- [ ] If CU loan: title issued to buyer with CU lien notation; CU receives title via mail
- [ ] If captive: title goes to captive direct; buyer's name on registration
- [ ] First payment due ~30-45 days post-funding

### Trade-in buyer

Pre-arrival (cross-ref `../orchestrator/references/trade_in.md` section 4a-4d if active lien):
- [ ] If lien: 10-day payoff letter from lien-holder in hand (NOT dealer's quote)
- [ ] Lien-holder auto-pay cancelled pre-close (avoid double-charge cycles)
- [ ] KBB Instant Cash Offer screenshot in hand as walk-floor anchor
- [ ] Key count verified (matches Phase 1 capture; missing 2nd key = $200-400 deduction)
- [ ] All personal items removed; both key fobs ready

On-site:
- [ ] Bill-of-sale shows: trade allowance, lien payoff routing, dealer commitment date
- [ ] State trade-in tax credit applied to GROSS trade allowance (NOT net of payoff) per `../orchestrator/references/state_fees.md`
- [ ] No shell-game: ACV and trade allowance NOT confused; sale price and trade negotiated separately

Post-close monitoring (calendar reminders at Day 5 / 10 / 14 / 21): payoff initiated, lien-holder received, release filed at DMV, release confirmation in hand. If not released by Day 30, escalate per `../orchestrator/references/trade_in.md` section 5.

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
- [ ] NACS vs CCS1 port confirmed; adapter ordered if needed
- [ ] State EV rebate eligibility + paperwork confirmed (MSRP/income caps per state; this is the only live incentive)

Pre-arrival (HISTORICAL, pre-2025-10-01 acquisitions only; §30D terminated 2025-09-30, do NOT use for 2026):
- [ ] ~~Dealer is IRS Energy Credits Online registered~~ (N/A, §30D terminated)
- [ ] ~~Form 8936 ready for signing~~ (N/A, §30D terminated)
- [ ] ~~MAGI under threshold confirmed ($150k single / $300k joint for new; $75k / $150k for used)~~ (N/A, §30D/§25E terminated)

On-site (LIVE in 2026):
- [ ] Battery warranty registered to buyer at delivery (new EV)
- [ ] No EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup ADM line items per gotcha D9 + `../orchestrator/references/ev_buyer_playbook.md` section 8
- [ ] L1 OEM charge cable included in delivery (factory accessory, NOT a separate purchase)

On-site (HISTORICAL, pre-2025-10-01 acquisitions only; do NOT apply to a 2026 close):
- [ ] ~~$7,500 reduction shown as separate line item on signed agreement~~ (N/A, §30D terminated; no federal credit line should appear)
- [ ] ~~Time of Sale report copy retained~~ (N/A, §30D terminated)

Post-close:
- [ ] Home L2 install scheduled (Qmerit / Treehouse / ChargePoint) if not already
- [ ] State EV rebate application submitted (verify state DOE / clean-energy office deadline, the only live incentive)

### Pickup-truck buyer

Pre-arrival (cross-ref `../orchestrator/references/vertical_playbooks.md#part-1--pickup-truck-specifics`):
- [ ] Factory tow package verified at delivery via VIN decode + door-jamb option codes (Ford 53A/535, Ram AHT, GM NHT, Toyota tow prep)
- [ ] Real tow capacity matches buyer's stated use case (engine x axle x package per section 1)
- [ ] Payload capacity NOT exceeded by buyer's actual use (tongue + passenger + gear math per section 3)
- [ ] PPI included pickup-specific items: frame, transmission cooler, hitch wear, body mounts, exhaust manifold (V8), turbo seals (EcoBoost)

On-site:
- [ ] Factory vs aftermarket hitch distinction confirmed in writing
- [ ] Integrated trailer brake controller functional test (dash-mounted gain knob; green LED on 7-pin connect)
- [ ] No ex-plow / ex-fleet posture concealed (CARFAX commercial fleet = $1-2k off; plow prep = $1.5-3k off)
- [ ] Lift kit / oversized tires inspected for warranty + insurance impact (per section 6)

Quick PPI items (frame / suspension / tow wear): frame (no rust-through, no welds outside factory locations, no bent crossmembers); suspension under-load (no clunk on speed bump, no sag past load index); tow wear (hitch ball threads, 7-pin pin corrosion, wiring harness chafe). Post-close: record door-jamb payload number for future tow planning.

## F&I Hard-No Verbatim Script (gotcha P3)

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

### Verbatim Refusal Script (buyer-spoken language)

**Spoken-only carve-out.** The two scripts above are the dealer-facing baseline:
English + ASCII, fine to print and hand across the desk or paste into email. A buyer
who is more fluent in Spanish or Chinese may instead *say the refusal out loud* in
their own language, spoken words are the agent-to-buyer surface, not a dealer
artifact. The hard rule still holds for everything WRITTEN or EMAILED to the dealer:
English + ASCII only (Critical Rule #1). Do NOT print these translations, do NOT
paste them into a Gmail draft, do NOT hand them to F&I as a document. Read aloud only.
See `../orchestrator/SKILL.md` § Language and Audience Separation and
`../../data/fragments/es_refusal_scope.md`.

Load-bearing F&I terms below were checked against real US-Spanish-market usage, not
literal-translated. Still: have a native speaker or Codex review the phrasing before a
buyer relies on it at the desk.

> Translation status: DRAFT, pending Codex / native-speaker review.

**Add-on name glossary (US Spanish market, verified usage):**

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

### Pre-close-day heads-up email (send to GM ~24h before close)

Pre-empts most close-day F&I friction. Full template in `../orchestrator/assets/dealer_reply_template.md` section Pre-Close-Day F&I Heads-Up Email. Key elements:

- Confirm locked OTD with agreement date
- Decline list (GAP, VSC, tire-and-wheel, paint, key, nitrogen, dent/ding)
- Close-day logistics: time window, funding instrument, insurance binder, plate decision, ID set

## Universal Cross-References

| Need | Open |
|---|---|
| Full Phase 9 detail (all 5 buyer types) | `../orchestrator/references/phases.md#phase-9--close` |
| Lien payoff full workflow | `../orchestrator/references/trade_in.md` section 4a-4d |
| EV federal credit status (§30D/§25E/§45W all TERMINATED 2025-09-30, historical) + live state rebates | `../orchestrator/references/ev_buyer_playbook.md` section 1; `ev-buyer-helper` CRITICAL banner |
| Pickup-specific PPI items | `../orchestrator/references/vertical_playbooks.md#part-1--pickup-truck-specifics` section 4 |
| State-fee leak detection ("Does NOT have") | `../orchestrator/references/state_fees.md` section Tri-State / New England detail stubs (gotcha D8) |
| F&I hard-no full text + reframe | `../orchestrator/assets/dealer_reply_template.md` section Close-Day F&I Hard-No |
| Financing close-day instruments | `../orchestrator/references/payment_methods.md` |
| CPO enrollment at close | per-OEM CPO programs in `../orchestrator/references/` (subaru_cpo_program.md, honda_cpo_program.md, etc.) |
| HD pickup / commercial van / luxury close routing | `../orchestrator/references/vertical_playbooks.md#part-2--heavy--commercial--luxury` section 6 |
| Lease-end options | `../orchestrator/references/lease_playbook.md` section Lease-end options |

## Stop Conditions

- All buyer-type-relevant boxes checked + F&I script in hand -> buyer is ready to drive to dealer
- Any pre-arrival item unchecked -> STOP, resolve before close (do NOT proceed without cashier's check ready or insurance binder issued)
- F&I refuses to remove add-ons after hard-no script + reframe -> exit per script; the deal is dead, not negotiable
- Trade lien payoff not confirmed by Day 14 -> escalate per `../orchestrator/references/trade_in.md` section 5
