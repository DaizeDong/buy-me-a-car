---
name: Close Day Checklist
description: Use when buyer is ready to close (signing today/tomorrow), needs the day-of checklist for cash / financing / trade-in / EV / pickup buyers, F&I add-on refusal script, and timing of cashier's check / lien payoff / plate transfer. Triggers include "ready to close", "close day checklist", "F&I add-on refusal", "lien payoff timing", "提车清单", "准备签约".
---

# Close Day Checklist

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> last_verified: 2026-05-18

Narrow sub-skill: buyer has a locked OTD in writing and is heading to the dealer to sign. No re-negotiation, no fresh outreach. For the full 9-phase workflow load `../orchestrator/SKILL.md`; for upstream counter / follow-up drafting load `dealer-reply-drafter`.

## When To Use

- Buyer is signing today or tomorrow and needs a sub-checklist by buyer type
- Buyer wants the F&I add-on refusal script to read verbatim at the F&I desk
- Buyer has a trade with active lien and needs the payoff workflow
- Buyer is an EV buyer and needs the Section 30D POS credit transfer day-of mechanics
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

### EV buyer (Section 30D POS credit transfer)

Pre-arrival (cross-ref `../orchestrator/references/ev_buyer_playbook.md` section 1):
- [ ] Dealer is IRS Energy Credits Online registered (verify ID on dealer letterhead BEFORE deposit)
- [ ] Form 8936 ready for signing
- [ ] MAGI under threshold confirmed ($150k single / $300k joint for new; $75k / $150k for used)
- [ ] Battery warranty docs reviewed (new EV) OR SoH report obtained (used EV) per section 6
- [ ] NACS vs CCS1 port confirmed; adapter ordered if needed

On-site (day-of mechanics):
- [ ] $7,500 reduction shown as separate line item on signed agreement (NOT bundled into sale price)
- [ ] Time of Sale report copy retained (required at tax filing the following year)
- [ ] Battery warranty registered to buyer at delivery (new EV)
- [ ] No EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup ADM line items per gotcha D9 + `../orchestrator/references/ev_buyer_playbook.md` section 8
- [ ] L1 OEM charge cable included in delivery (factory accessory, NOT a separate purchase)

Post-close:
- [ ] Home L2 install scheduled (Qmerit / Treehouse / ChargePoint) if not already
- [ ] State EV rebate application submitted (verify state DOE / clean-energy office deadline)

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
| EV Section 30D POS credit mechanics | `../orchestrator/references/ev_buyer_playbook.md` section 1 |
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
