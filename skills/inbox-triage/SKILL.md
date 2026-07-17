---
name: Dealer Inbox Triage
description: Use to triage incoming Gmail dealer replies, classify each as real reply / autoresponder (OOO) / CRM template / spam / promotions / autopiloted-marketing, and decide what action each needs. Triggers include "check my dealer inbox", "triage these emails", "is this real or autoresponder", "看下邮箱", "dealer 回复了吗", "spam folder check", and Spanish phrases "revisar mi bandeja de correos del concesionario", "ya respondio el dealer o es respuesta automatica".
---

# Dealer Inbox Triage

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.

Narrow-trigger skill: classify Gmail dealer mail into 4 actionable buckets and route each
to its next step. Defers drafting to `../dealer-reply-drafter/SKILL.md` and cron setup
details to `../orchestrator/references/cron_monitoring.md`.

## When to invoke

User says any of: "check my dealer inbox", "triage these emails", "is this real or
autoresponder", "看下邮箱", "dealer 回复了吗", "spam folder check", "what came in
overnight", "did anyone reply".

## The 4 buckets

Every dealer-domain email lands in exactly ONE bucket. Decide in order:

### 1. Real reply, buyer-specific human response

**Signals**: human prose, references buyer-supplied details (the buyer's name, the
specific VIN/stock number the buyer asked about, an OTD figure, an availability
confirmation, a counter-offer number). Sender is a named salesperson, not a generic
`sales@`, `info@`, or `noreply@` alias.

**Spanish / bilingual dealer mail**: a reply written in Spanish or mixed Spanish+English
is still a **bucket-1 real reply**, NOT spam, many US dealers staff bilingual reps and
will answer in the buyer's apparent language or their own. Language is never a spam
signal; judge by the bucket-1 content signals above (human prose, buyer-specific
numbers, named sender). When handing off:

- **Translate the substance for the buyer**: surface the actionable content in English ,
  OTD/price figures, VIN/stock confirmation, availability, any counter-offer or
  condition the rep stated. Give the buyer the meaning, not a word-for-word gloss.
- **Outbound counter stays in English**: the draft handed to
  `../dealer-reply-drafter/SKILL.md` is composed in English regardless of the inbound
  language (per the buyer's drafting preference). Do not mirror Spanish in the reply
  unless the buyer explicitly asks.

**Action**: hand off to `../dealer-reply-drafter/SKILL.md` to compose a ~10-line counter.
Apply Gmail label `Triage/RealReply`. Do NOT archive the inbound; keep it in INBOX so
the human can verify before the draft is sent.

### 2. OOO autoresponder

**13-keyword detection list** (case-insensitive substring match in subject OR first 500
chars of body):

1. `out of office`
2. `out-of-office`
3. `ooo` (whole-word; avoid "loose" false positive)
4. `auto-reply`
5. `automatic reply`
6. `away from the office`
7. `on vacation`
8. `out of the office`
9. `will be back`
10. `until <date>` (regex: `until\s+(?:\w+\s+)?\d{1,2}`)
11. `i am currently out`
12. `i'm currently out`
13. `returning on`

**RFC 3834 header signal**: `Auto-Submitted: auto-replied` OR `Auto-Submitted:
auto-generated`. If present, classify OOO even without keyword match. RFC 3834 is the
authoritative signal, keywords are the fallback for dealers that omit the header.

**Action**: extract the return date (regex from item 10 above, or "returning on
<date>"). Apply label `Triage/OOO_until_YYYY-MM-DD`. Suppress all re-pings to this
sender until the return date. Do NOT draft a reply.

### 3. CRM template / autopiloted marketing

**Signals**: generic salutation ("Dear Valued Customer", "Hi there"), boilerplate
("Thank you for your interest in <Brand>!"), unsubscribe footer, no buyer-specific
numbers, sent from a marketing alias (`marketing@`, `news@`, `specials@`,
`<dealer>@e.<brand>.com`).

**CAUTION, gotcha I4**: A CRM-wrapped email that contains specific vehicle data
(stock #, VIN, sale price, miles, color matching what the buyer asked about) IS
actionable. Test: "does this email contain a vehicle-specific number that matches the
buyer's open ask?" If yes, treat as Real reply (bucket 1), not CRM. Skip only pure
marketing taglines.

**Action**: archive (skip INBOX). Apply label `Triage/CRM`. No draft.

### 4. Spam / phishing

**Signals**: lookalike domain (`.co` instead of `.com`, swapped chars), prize/giveaway
language, attached executables, "verify your account" links to non-dealer URLs, mail
already in Spam folder.

**Action**: leave in Spam (or move to Spam if landed in Inbox). Apply label
`Triage/Spam`. Notify operator only if 3+ from same sender in 24h (possible compromised
dealer account).

## Gmail search patterns

Run these in sequence each triage pass. Default account is buyer's primary Gmail; see
multi-account warning below.

```
# Real-reply candidates (last 2 days, not your own drafts)
from:<dealer-domain> newer_than:2d -in:draft

# Spam check (dealer mail mis-flagged as spam in last 24h)
from:<dealer-domain> in:spam newer_than:24h

# Promotions tab check (dealer mail in Promotions in last 24h)
from:<dealer-domain> category:promotions newer_than:24h

# Overnight catch-up (unread, last 12 hours, any tab)
newer_than:12h is:unread
```

For multi-dealer buying cycles, run the first 3 once per known dealer domain, then the
overnight catch-up across the whole account.

## 3 scheduled crons

Configure these via CronCreate per `../orchestrator/references/cron_monitoring.md`.
This skill is the consumer; the orchestrator reference is the source of truth for the
prompt templates.

| Cron | Cadence | Purpose |
|---|---|---|
| **15-min inbox sweep** | `*/15 * * * *` during buying hours | Catch real replies fast; route through this skill's 4-bucket classifier. |
| **6-hour spam + promo sweep** | `0 */6 * * *` | Catch dealer mail mis-flagged into Spam or Promotions (gotcha I2). |
| **7 AM morning catch-up** | `0 7 * * *` | Full `newer_than:12h is:unread` sweep to cover overnight gap (gotcha I3). |

## Multi-account warning

This skill operates on the **default Gmail account** of whatever Gmail MCP/connector is
attached. If the buyer has separate work and personal Gmail accounts (common, buyers
often route dealer mail to personal to avoid corporate spam filters), confirm with the
buyer upfront WHICH account is the dealer inbox. Misconfiguration here causes silent
failure: the triage will return "no new mail" while the dealer mail piles up in the
other account.

Checklist before first triage:
- [ ] Confirmed which Gmail account holds dealer mail.
- [ ] That account is the one attached to the active Gmail MCP / connector.
- [ ] If buyer uses a forwarding rule (work → personal), confirm the rule is active.

## Worked example, today's inbox state

Buyer scenario: 4 dealers contacted yesterday for the same 2024 Subaru Outback. Today's
inbox after running this skill:

| Sender | Bucket | Why | Next step |
|---|---|---|---|
| Dealer A rep (named) | 1, Real reply | Named salesperson, quotes OTD $34,820 on stock #SU2419 | Hand to dealer-reply-drafter; counter at $33,500 anchor. |
| Dealer B | (silent) | No reply yet, 18h elapsed | No action, gotcha I1 says 12+ hr delay normal. Wait for 24h mark before re-ping. |
| Dealer C rep (named) | (silent) | No reply yet, 14h elapsed | Same as Dealer B. |
| Dealer D rep (named) | (silent) | No reply yet, 20h elapsed | Same, but flag for re-ping at 24h. |

Net: 1 reply to draft, 3 silent dealers being patient. This is a normal, healthy state
on day 2 of a buying cycle, NOT a failure.

## Critical gotcha cross-refs

These are defined in `../orchestrator/SKILL.md` gotcha section:

- **gotcha I1**, Dealers commonly delay 12+ hours; silence on day 1 is normal.
- **gotcha I2**, Dealer mail lands in Promotions AND occasionally Spam; the 6-hour
  spam+promo sweep is mandatory.
- **gotcha I3**, Sliding `newer_than:25m` windows miss backlog across overnight gaps;
  the 7 AM morning catch-up is mandatory.
- **gotcha I4**, CRM-wrapped emails with embedded vehicle data ARE actionable; do not
  bucket-3 them just because the wrapper is templated.
- **gotcha I5**, Never trash a dealer's original email or the buyer's sent reply ,
  it breaks future thread anchors. Triage only moves labels; it never deletes.

## Output contract

After every triage pass, return a one-screen summary to the operator:

```
Triage pass — <timestamp>
  Real replies (need draft): N  [list senders]
  OOO (suppressed until <date>): N  [list senders + return dates]
  CRM (archived): N
  Spam (quarantined): N
  Silent dealers (no action, day X of cycle): N  [list]
```

Then hand off any bucket-1 items to `../dealer-reply-drafter/SKILL.md`.
