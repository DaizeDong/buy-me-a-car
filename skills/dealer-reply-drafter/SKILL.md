---
name: Dealer Reply Drafter
description: Use when the user has received a dealer email reply and wants to draft a counter, follow-up, or walk-away - without engaging the full 9-phase buy-me-a-car workflow. Triggers include "draft counter to dealer", "reply to this dealer email", "follow up with dealer", "respond to OTD quote", and Chinese phrases "回复 dealer", "给 dealer 起草回信", "对 dealer 报价做 counter", and Spanish phrases "responder al concesionario", "redactar una contraoferta al dealer", "dar seguimiento al concesionario".
---

# Dealer Reply Drafter

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> last_verified: 2026-05-18

Narrow sub-skill: one dealer reply in hand, one email to draft. No inventory pull, no mass outreach, no cron monitoring. For the full 9-phase workflow load `../orchestrator/SKILL.md` instead.

## When To Use

- Buyer pastes a dealer reply (OTD quote, ADM-laden offer, "let me check with manager" stall, urgency tactic) and wants the next outbound email
- Buyer is mid-cycle and just needs ONE counter / follow-up / walk-away drafted now
- Buyer has a fresh competitor anchor and wants to push it into an existing dealer thread

## When NOT To Use

- Buyer has not yet contacted dealers (use orchestrator Phase 4 outreach instead)
- Buyer needs market-data baseline for the first time (use orchestrator Phase 2)
- Buyer is at the F&I desk / close day (use `close-day-checklist` sub-skill)
- Buyer wants a CARFAX PDF reviewed (use `carfax-pdf-review` sub-skill)

## One-Page Workflow

### Step 1: Skim the dealer reply for 5 things

Before drafting, extract these explicitly. If any are missing, ask the buyer ONE clarifying question (not five - see gotcha E4).

1. **Sale price** - exact dollar amount, NOT a range
2. **Doc / tax / title / reg / "other" lines** - each as a separate number, in writing
3. **Anomalies** - fees not in the registering state's "Has" list per `../orchestrator/references/state_fees.md` (gotcha D8); ADM line names per gotcha D9; missing CARFAX / VIN / stock
4. **Urgency tactics** - "this car will be gone today", "manager said today only", repeated phone-only push (D1, D2)
5. **Trade allowance if applicable** - gross vs net of payoff; shell-game signal per `../orchestrator/references/trade_in.md` section 2

### Step 2: Pull REAL anchors only (Critical Rule #7)

Phase 4 / counter emails may only cite REAL-tagged data points. Forbidden:

- Synthesized Reddit anecdotes
- Fabricated dealer numbers ("a dealer offered $28k")
- Generic "buyers report X"
- Round-numbered placeholder anchors

Allowed:

- Named Edmunds / CarGurus / KBB regional median with city + sample size
- Named single-comp listing: `{Dealer} has a comparable {trim} at ${ask}`
- Locked competitor OTD by dollar amount (only if buyer has WRITTEN quote, per N1)
- Internal-spread anchor: same dealer's other listing (Anchor 1 in negotiation_playbook)

If buyer has no real anchors yet, the email is a follow-up asking for the OTD breakdown - NOT a counter. Do not invent numbers.

### Step 3: Pick email type

| Type | Length | Skeleton |
|---|---|---|
| Counter | ~10 lines hard cap | 3 numbered asks + 1 anchor sentence + 1 walk-away line |
| Follow-up / nudge | 4-6 lines | 1 specific ask |
| Walk-away | 4-6 lines | graceful close, door open |

Counter is the default when the dealer has sent a written OTD. Follow-up is for stalls ("let me check"), missing data, or T+24h reminders. Walk-away is when the dealer refuses to move OR the gap is structural (ADM refusal per D9, in-person-only pricing).

### Step 4: Apply E3 hard cap + voice spec

Read `../orchestrator/assets/dealer_reply_template.md` section Voice Specification BEFORE drafting. Key rules:

- Direct, no hedging. Imperative ("Please remove"), not subjunctive ("I would appreciate if")
- No softeners ("just", "maybe", "I hope you're well")
- One thank-you per email, at the open
- Numbered asks when there are 2+
- Anchor is ONE line: `{Dealer} {trim} at ${OTD} OTD, {miles} mi`
- Sign-off: `Thanks,` + buyer first name (hold consistent across all threads in cycle)
- Dealer-facing emails are ALWAYS English-only, ASCII-only (no Chinese, no Spanish)

### Step 5: Save via MCP `create_draft` with NO attachments inline (E5)

Pass body as plain text. If buyer wants screenshots attached, do NOT inline via MCP - generate full-res JPGs in `.firecrawl/quote-images/` and tell the buyer to manually paperclip via Gmail web UI. See gotcha E5 for the constraint chain.

After saving, confirm draft ID and ask buyer to review in Gmail before sending. Do NOT auto-send.

## Quick Reference Table

| Need | Open |
|---|---|
| 5-element Cold Open recipe | `../orchestrator/references/negotiation_playbook.md` section Round 1 Cold Open |
| ASCII substitution table | `../orchestrator/references/email_format_rules.md` |
| Voice spec + red flags | `../orchestrator/assets/dealer_reply_template.md` section Voice Specification |
| State-fee leak detection | `../orchestrator/references/state_fees.md` "Does NOT have" lists (gotcha D8) |
| ADM kill list + exact language | orchestrator SKILL.md gotcha D9 |
| Bait-and-switch defenses | orchestrator SKILL.md gotcha D10 |
| Dealer-group ownership map | orchestrator SKILL.md gotcha D11 |
| Trade shell-game counter | `../orchestrator/references/trade_in.md` section 2 |
| F&I close-day script | orchestrator SKILL.md gotcha P3 + `close-day-checklist` sub-skill |

## Paste-Ready Skeletons

### Counter (3 asks + 1 anchor + walk-away)

```
Hi {REP_NAME},

Thanks for the breakdown. Three items:

1) {ASK_1: e.g., Please remove the $X [exact ADM line name] line per gotcha D9.}
2) {ASK_2: e.g., The $7.50 tire fee is an NJ line item; CT has no per-tire fee. Please re-quote OTD without it.}
3) {ASK_3: e.g., For the sale price, {NAMED_ANCHOR}. My target to commit is ${TARGET_OTD} OTD.}

{ONE_LINE_ANCHOR: e.g., Hoffman Honda has a comparable 2023 Outback Limited at $27,900 ask.}

Above ${WALK} OTD I will move forward with my other anchors. Cash buyer, cashier's check, ready to close {DAY} pending PPI.

Thanks,

{BUYER_FIRST_NAME}
```

### Follow-up (cross-bid anchor + deadline)

```
Hi {REP_NAME},

Following up on my {DATE} note about {VEHICLE / OTD ASK}.

My locked benchmark is now {COMPETITOR_DEALER} at ${COMPETITOR_OTD} OTD on a comparable unit.

To keep this unit in the running, I need a written OTD by EOD {T+48H_DATE}. After that, my other anchors firm up.

Thanks,

{BUYER_FIRST_NAME}
```

### Walk-away (graceful)

```
Hi {REP_NAME},

Understood, and I respect the policy.

For my needs and budget this week, the numbers do not pencil out at ${OTD} versus my comparable offers, so I will move forward with my other option. If anything changes (price adjustment, similar unit at a more competitive number, new arrival), please reach back out.

Wishing you the best on the sale.

Thanks,

{BUYER_FIRST_NAME}
```

## Gotcha Shortlist (mandatory pre-save scan)

| ID | Trigger | Action |
|---|---|---|
| E1 | Any `**`, em-dash, backtick, curly quote, `[text](url)` in draft body | Strip per email_format_rules.md substitution table |
| E3 | Counter > 10 content lines | Cut. 3 asks max + 1 anchor + 1 walk-away |
| E4 | Considering 2nd+ draft on same thread | Ask 2-3 clarifying questions FIRST; give buyer one bulk-delete search string if iteration unavoidable |
| E5 | Buyer asks to "attach screenshots" inline | Push back once; default to manual paperclip via Gmail web UI |
| D5 | Draft mixes used + new car anchors | Strip the off-class anchor; used/new desks have different incentives |
| D8 | Quote contains fee not in registering state's "Has" list | Demand FULL re-quote, not single-line deletion |
| D9 | ADM line on NEW MY inventory | First counter demands removal as precondition; do not couple to other concessions; one ask, one round |
| D10 | Dealer claims original VIN "just sold", pivots to higher-priced VIN | Demand sold-confirmation in writing; pivoted VIN must hit same OTD adjusted only for legitimate config delta; treat as new engagement |
| D11 | Buyer presenting 2+ "competing" anchors from sibling stores | Google parent group BEFORE citing as cross-bid; same parent = 1 anchor not 2 |

## Worked Example

**Context**: Dealer's first quote on {YEAR MAKE MODEL TRIM} came in at ~$33k OTD. Buyer's walk ceiling is in the low-$30k range. Two competing anchors locked.

**Counter v2 (3 asks)**:

```
Hi [name],

Thanks for the OTD breakdown. Three items:

1) The doc fee at $799 is at the NJ statutory cap; please tighten this to $499 or absorb into sale price.
2) Please confirm no Paint Protection / fabric guard / etching add-ons are in the quote; I want only sale + tax + doc + title + reg.
3) For the sale price, my target to commit is $30,750 OTD. Possible structures: Sales $28,500 + Doc $499 + Tax + Reg, or any combo that lands there.

My locked benchmarks are Dealer A at $30,946 OTD and Dealer B at $31,348 OTD on the same trim within 20 miles.

Above $31,500 OTD I will move forward with one of the locked anchors. Cash buyer, cashier's check, ready to close Thursday or Friday pending PPI.

Thanks,

{BUYER_FIRST_NAME}
```

5 elements present: 3 numbered asks, 1 anchor line (Dealer A + Dealer B by name + OTD), 1 walk-away. ~10 content lines. ASCII only. All anchors REAL-tagged.

## Stop Conditions

- Draft saved + buyer notified -> done. Do NOT iterate without buyer feedback (E4)
- Buyer has no real anchor and no written OTD -> switch to follow-up template, do not invent numbers
- Dealer refused ADM removal in prior round -> walk-away, route to next anchor (D9 rule 2: one ask, one round)
- More than 2 drafts in a row on same thread -> STOP, surface stale-draft cleanup search string, gather buyer intent before next draft
