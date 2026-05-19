# Cron-Based Inbox Monitoring

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

After mass outreach to 30-50 dealers, replies trickle in over 24-72 hours. Manual checking is inefficient. Set up CronCreate to scan the buyer's Gmail every 15 minutes.

## CronCreate Setup

Use the CronCreate tool with these parameters:

```
cron: */15 * * * *
recurring: true
prompt: (see template below)
durable: false  (session-only is sufficient for one buying cycle)
```

## Cron Prompt Template

Replace {placeholders} with actual values.

```
Check {EMAIL} inbox for dealer mail received in the past 20 minutes
(keywords: {MAKE} OR {MODEL} OR {TRIM_LIST} OR dealer OR OTD OR Carfax OR Enterprise
 OR {DEALER_NAMES_LIST}).

For each real dealer reply (skip Carfax auto-confirms, autoresponders, non-dealer mail):
1. Read full thread.
2. Draft an OTD-focused reply per
   {PROJECT_DIR}\dealer_reply_template.md.
3. Save Gmail draft (use replyToMessageId for thread continuity).
4. Append a log entry to
   {PROJECT_DIR}\dealer_outreach_tracker.md
   under "Dealer Reply Log" section.

ALL email drafts must use plain ASCII. NO em-dash (the long dash, U+2014),
NO en-dash, NO markdown bold/italic markers, NO backticks,
NO [text](url) link syntax. Replace em-dash with comma, colon, or period
and new sentence. Verify body before saving each draft.

Skip:
- Carfax confirmation emails (from:CARFAX@event.carfax.com)
- Autoresponders ("currently closed" / "will be in touch" templates)
- Non-dealer mail (banking, academic, personal, marketing)

Output a one-line status per cycle: scanned N threads, processed X, skipped Y.
If no new mail: "No new dealer mail this cycle".
```

## Periodic Full Sweep (Critical — Backlog Detection)

**Problem**: The `newer_than:25m` sliding window in the cron prompt only catches mail that arrives DURING active cron cycles. If the buyer pauses the conversation for several cycles (e.g., overnight, during a meeting), any dealer mail that arrived in those gaps is permanently missed by subsequent cron runs — the window has already moved past it.

**Real incident from a prior search**: A Sales Manager at a local Honda dealer sent a substantive inventory response with 1 matching vehicle. The cron `newer_than:25m` checks every 15 minutes for 4 cycles did not flag it because the cron loop happened to be paused when the mail arrived. The buyer only caught it by asking for a full sweep.

**Fix**: Run a `newer_than:3d is:unread` full sweep at least once per buying-cycle day (or whenever the buyer notices replies have been quiet for a while). The full sweep query:

```
newer_than:3d is:unread
  (Subaru OR Forester OR Crosstrek OR Outback OR Honda OR CR-V
   OR Toyota OR RAV4 OR Mazda OR Ford OR Escape OR dealer OR OTD)
  -from:CARFAX -from:noreply -from:no-reply -in:sent -in:draft
```

Cross-reference results against the tracker. Any UNREAD + IMPORTANT thread from a real sales rep email address that the tracker does not log is a backlog miss. Process immediately.

## Spam + Promotions Sweep — Scheduled (Required)

Real dealer mail from CRM platforms (eDealerHub, VinSolutions, eLead) sometimes lands in SPAM, especially first-touch emails from dealers the buyer has never received mail from. Other CRM templates land in the Gmail Promotions tab due to bulk-mail headers. The default 15-min inbox-only cron query excludes both surfaces.

**Mechanized fix — run a dedicated spam + promotions sweep every 6 hours** alongside the main inbox cron. Do NOT rely on agent diligence or buyer prompting; bake it in. Recommended cron:

```
cron: 0 */6 * * *     # every 6 hours; e.g., midnight, 6 AM, noon, 6 PM ET
recurring: true
prompt: (template below)
durable: same as main cron
```

Sweep prompt template:

```
Run a full spam + promotions sweep on {EMAIL}:

Query 1 (spam):
  in:spam newer_than:24h
    (Subaru OR Forester OR Crosstrek OR Outback OR Honda OR CR-V
     OR Toyota OR RAV4 OR Mazda OR Ford OR Escape OR Tundra OR F-150
     OR dealer OR OTD OR {DEALER_NAMES_LIST})

Query 2 (promotions):
  category:promotions newer_than:24h
    (Subaru OR Forester OR Crosstrek OR Outback OR Honda OR CR-V
     OR Toyota OR RAV4 OR Mazda OR Ford OR Escape OR Tundra OR F-150
     OR dealer OR OTD OR {DEALER_NAMES_LIST})

For each match:
1. If a real dealer message: advise buyer to mark Not Spam (spam) or
   move to Primary (promotions) so future replies route correctly.
2. Process the reply per the main-cron workflow: read thread, draft
   OTD reply, save Gmail draft, log to tracker.
3. Annotate the tracker entry "found via spam sweep" or
   "found via promotions sweep" so the buyer knows to apply the
   Gmail rule fix.
```

**Cron-cadence rationale**: 6 hours catches spam-promotions misroutes within at most ~6 hours of arrival (vs the worst-case 24-72 hr delay if the agent only ran spam manually). The 24-hour `newer_than:24h` window gives 4x overlap with the 6-hour interval, eliminating gap risk.

**Real incident**: A Subaru dealer sales rep's first OTD-with-PDF email landed in SPAM. The follow-up 24h later landed in INBOX. The default cron only saw the follow-up; the original PDF quote was buried in spam and only surfaced when the rep asked "did you get my quote?". A scheduled 6-hour sweep catches this within at most 6 hours.

## Morning Catch-Up Sweep — Scheduled (Overnight Gap Recovery)

The default 15-min main cron and the 6-hour spam/promotions sweep both depend on an active Claude session. The Claude harness's CronCreate only fires within active sessions; if the buyer sleeps 11 PM-7 AM, NO cron cycles fire during that window. Any dealer mail arriving overnight (a West-coast dealer working late, a CRM-scheduled auto-send at 2 AM, an Eastern dealer running midnight inventory blast) is invisible to the next-morning sliding `newer_than:25m` window.

**Mechanized fix — schedule a `newer_than:12h is:unread` morning catch-up sweep at the buyer's wake time** (default 7 AM ET; ask the buyer at Phase 5 setup). This sweep runs in addition to the resumed main cron and the 6-hour spam/promotions sweep.

```
cron: 0 7 * * *      # 7 AM daily; adjust to buyer's stated wake time
recurring: true
prompt: (template below)
durable: same as main cron
```

Sweep prompt template:

```
Run a morning catch-up sweep on {EMAIL} for overnight dealer mail
the 15-min cron may have missed during the session gap:

  newer_than:12h is:unread
    (Subaru OR Forester OR Crosstrek OR Outback OR Honda OR CR-V
     OR Toyota OR RAV4 OR Mazda OR Ford OR Escape OR Tundra OR F-150
     OR dealer OR OTD OR Carfax OR {DEALER_NAMES_LIST})
    -in:draft -in:sent
    -from:CARFAX@event.carfax.com
    -from:CARFAX@no-reply.carfax.com

Cross-reference each result against the tracker. Any UNREAD +
IMPORTANT thread from a real sales rep that the tracker does not
log is a backlog miss from the overnight gap. Process per the
main-cron workflow (read, draft, log).

Output status: "Morning sweep: scanned N threads, X new overnight
replies processed, Y were already in tracker."
```

**Cadence rationale**: A 12-hour window with `is:unread` is wider than the overnight gap (typically 7-9 hours) and ignores reads from yesterday afternoon. The `is:unread` filter avoids re-processing threads the main cron drafted yesterday evening; the 12-hour window catches the rare 6-9 PM previous-day reply if the buyer paused early.

**Real incident**: In any active buying cycle, expect 1-3 dealer replies overnight per active cross-bid. Without the morning sweep, the resumed 7 AM main cron's `newer_than:25m` window only sees mail from 6:35 AM onward — 3-6 dealer threads sit silently unread until they bump with a follow-up, sometimes 24-72 hours later.

## Gmail Search Syntax Tips

Use these in the `query` parameter of `mcp__claude_ai_Gmail__search_threads`:

| Pattern | Purpose |
|---------|---------|
| `to:{EMAIL} newer_than:1h` | Inbox-only, recent |
| `category:promotions` | Promotions tab (many dealer emails land here, NOT inbox) |
| `in:anywhere` | Include Spam and Trash |
| `in:spam` | Only spam folder |
| `is:unread` | Filter to unread (helpful for backlog sweep) |
| `-from:CARFAX` | Exclude Carfax notifications |
| `-from:no-reply -from:noreply -from:alerts` | Exclude common auto-mailers |
| `-from:bank -from:newsletter` | Exclude personal/work mail |
| `-in:draft -in:sent` | Exclude buyer's own drafts and sent items from the result set |

Full example query for default cron cycle:

```
newer_than:25m
  (Subaru OR Forester OR Crosstrek OR Outback OR Honda OR Mazda
   OR dealer OR OTD OR Carfax OR Enterprise OR {DEALER_NAMES})
  -in:draft -in:sent
  -from:CARFAX@event.carfax.com
  -from:CARFAX@no-reply.carfax.com
```

`-in:draft -in:sent` matters — Gmail thread search returns the buyer's own messages alongside dealer messages. Filtering them out keeps result counts honest.

## Gmail API Quirks (Important)

### 1. plaintextBody can be missing for HTML-only emails

Many dealer CRM platforms send emails with HTML body only (no `multipart/alternative` with plaintext). The Gmail API's `messageFormat: FULL_CONTENT` returns `plaintextBody` only when a plaintext part exists. For HTML-only messages, `plaintextBody` is empty or null and only the snippet (first ~200 chars) is available.

**Real incident**: A Subaru dealer rep sent a substantive reply with the full OTD breakdown (sales, tax, doc, fees, total) inline in the body. Gmail API returned `plaintextBody: ""` because the email was HTML-only. The agent only saw the snippet ("[buyer name], a brief note confirming one of the two matching vehicles had sold, another was available, and title and registration would be handled directly") which cut off before the actual numbers. The agent wrote a follow-up asking for numbers the rep had already sent.

**Fix protocol**: After fetching a thread, check if the latest dealer message has `plaintextBody`. If empty:

- Re-read the snippet carefully — it may already contain the key data.
- Tell the buyer: "This message is HTML-only and the Gmail API does not return the full body. Snippet shows: [snippet]. If there are inline numbers (sales, tax, OTD) past where the snippet cuts off, please paste them so the draft reply can reference them accurately."
- Do NOT assume the dealer "did not send numbers" just because plaintextBody is empty.

### 2. PDF attachments cannot be read by Gmail API

Even with `messageFormat: FULL_CONTENT`, the Gmail API exposes attachment IDs but not extracted text. The agent cannot read CARFAX PDFs, dealer OTD proposals, or service-record PDFs in-context.

**Protocol**:
1. Acknowledge the PDF was attached.
2. Ask the buyer to either share the file path locally or paste the OTD numbers inline.
3. As a fallback, ask the dealer to paste the OTD breakdown in the email body for "side-by-side comparison".

### 3. Snippet truncation can hide key data

The snippet field shows the first ~200 characters of the body. For dealer replies that start with "thanks!" or "great to hear!" before getting to the actual numbers, the snippet may not contain the key data. Always fetch the full thread and check both `plaintextBody` and any continuation past the snippet boundary.

## Real Human vs Autoresponder Heuristics

Not every email from a `@dealer.com` address is actionable. The cron must differentiate.

### Skip (autoresponder / template)

| Signal | Example |
|--------|---------|
| Phrase "currently closed" or "outside business hours" | After-hours auto-ack |
| Phrase "will be in touch during normal business hours" | First-touch auto-ack |
| Phrase "Type YES for updates" or "Reply STOP to opt out" | SMS-style auto |
| Phrase "moving fast" with no specific number change | Scarcity nurture template |
| Phrase "Did you receive your information" with HTML-only body and generic tagline | Re-engagement template |
| Phrase "I Can Help" with generic finance / lease / trade-in pitch and no specific vehicle reference | Generic nurture template |
| Sender pattern `sales@dealer-domain.edealerhub.com` with no rep name in signature | CRM auto-mail |

### Out-of-Office autoresponder detection (skip + flag + suppress re-ping)

OOO autoresponders look like real human replies (real sender, real signature, named rep) but are not actionable. They are a distinct skip class from the templated-marketing autoresponders above because the rep IS real and will be back — the buyer should not re-ping until the return date, and the cron should not draft counters into the void.

**Keyword / regex detection** (case-insensitive substring match; match ANY one signal triggers OOO classification):

| Signal | Example phrase |
|--------|---------------|
| "out of office" | "I am out of office until..." |
| "OOO" (whole word) | "OOO until Monday" |
| "out of the office" | "I'm out of the office this week" |
| "away from the office" | "I am away from the office through Friday" |
| "on vacation" / "on holiday" / "on PTO" | "I'm on vacation until 5/22" |
| "until [Mon-Sun]" or "until [Month] [day]" | "back in the office Monday" / "until May 22" |
| "I'll respond when I return" | Standard Gmail OOO template |
| "I will respond when I return" | Outlook OOO template |
| "for urgent matters please contact" | Typical OOO escalation line |
| "automated reply" / "automatic reply" | Outlook OOO subject prefix |
| "this is an automated response" | Generic OOO |
| "thanks for your message I'll get back to you [on/when/after]" | OOO + return date |
| Gmail Subject prefix `Auto reply:` or `Automatic reply:` | Outlook OOO subject prefix |
| Gmail header `Auto-Submitted: auto-replied` (RFC 3834) | Programmatic OOO header — strongest single signal |

**Action protocol when OOO detected:**

1. **Do NOT draft a reply.** No counter, no follow-up. Drafting into an OOO inbox creates 3-7 days of stale negotiation drift.
2. **Parse return date if present.** Regex for "until {Day-of-week}", "until {Month} {day}", "back on {date}", "returning {date}". If a date is parseable, store it in the tracker entry as `oo_return_date: YYYY-MM-DD`. If not parseable, store `oo_return_date: unknown — confirm with buyer`.
3. **Flag the dealer's tracker row.** Append a row to the tracker under "Dealer Reply Log":
   ```
   [timestamp] | {Dealer} | {Rep} | OOO_AUTORESPONDER | return_date={parsed_or_unknown} |
     SUPPRESS re-ping until return | flag for buyer awareness
   ```
4. **Suppress re-ping logic.** Until `oo_return_date` passes, the cron must NOT auto-draft any new outbound to this rep, even if the buyer asks "ping the silent dealers". Surface to buyer: "{Rep} at {Dealer} is OOO until {return_date}. Not pinging. Re-evaluate after return."
5. **On return date:** the cron's next morning sweep should re-include this rep in the active set. The buyer may want to send a fresh "checking back in" note manually.
6. **Edge case: OOO with substantive numbers in the BODY.** Some reps configure OOO with "for [partner] coverage during my absence, here are current prices on [vehicle]: $X. Otherwise I'll respond Monday." Rare but possible. If the body contains a sales-price / OTD / stock number despite OOO header, process the numbers as actionable BUT still flag OOO and suppress re-ping to the OOO rep — route any counter to the partner if named.

### Process (real human or templated-with-data)

| Signal | Example |
|--------|---------|
| Personal greeting + named rep signature with direct phone/extension | "Hi [name], ... [Rep name], ext [extension], [rep]@[dealer-domain].com" |
| Specific stock number, VIN, or sales price referenced | "Stock TE080871A, 2021 CR-V EX-L, 31k miles" |
| Specific question answered (yours or theirs) | "Yes the numbers I provided are accurate for this car" |
| Inline OTD breakdown (sales / tax / doc / fees / total) | Real human OR CRM with embedded inventory data |
| Inventory list with prices (even if HTML-templated) | Sales rep using CRM tool to send shortlist |

**Key insight**: Templated emails are not always skippable. A CRM-generated email that embeds specific inventory data (stock, VIN, sales price, miles, color) IS actionable, even if the surrounding wrapper is template boilerplate. The test is "does it contain specific vehicle data?" not "does it look like a template?".

## Pagination

`pageSize: 30` (max 50) is sufficient for hourly scans of one buyer's inbox. Most buyers see 5-20 dealer replies in their busiest days.

## Skip-List Identification

Common auto-mailers to filter:

- `CARFAX@event.carfax.com` (Carfax confirmation per submission)
- `CARFAX@no-reply.carfax.com` (Carfax marketing)
- `no-reply@accounts.google.com` (Google security)
- `alerts@<your-bank-alerts-domain>` (banking — e.g., chime, bofa, chase, etc.)
- `onlinebanking@<your-bank-ealerts-domain>` (banking)
- `noreply@<aggregator-service>.com` (banking aggregators — e.g., plaid, mx, finicity)
- Various academic / professional list-server addresses

Common autoresponder phrases to skip:

- "currently closed"
- "will be in touch"
- "appreciate your patience"
- "Welcome to the Adventure at" (Subaru CRM template)
- "Reply YES to receive text messages"
- "moving fast" / "moving quickly this week" (scarcity nurture)
- "Did you receive your information" (re-engagement template)
- "Your quote has arrived" (template tagline with no actual quote attached)

Common OOO autoresponder phrases (skip + flag dealer for buyer follow-up — see Out-of-Office subsection above for full action protocol):

- "out of office" / "OOO" / "out of the office" / "away from the office"
- "on vacation" / "on holiday" / "on PTO"
- "until [day-of-week / date]" / "back on [date]" / "returning [date]"
- "I'll respond when I return" / "I will respond when I return"
- "for urgent matters please contact"
- "automated reply" / "automatic reply" / "this is an automated response"
- Subject line prefix `Auto reply:` / `Automatic reply:` / `Out of Office:`
- Header `Auto-Submitted: auto-replied` (RFC 3834 — strongest single signal)

## Cron Lifecycle

- 15-min intervals × 96 cycles/day × 7-day TTL = ~672 cycles max
- Session-only cron dies with the Claude Code session; use `durable: true` to persist across restarts only if the buying timeline is multi-day and the buyer wants to keep the assistant alive
- Cancel manually with `CronDelete <job_id>` once the buying decision is made

## Path Updates

If the project directory changes (e.g., files moved from home directory to `{HOME}\car-buying-cycle\`), update the cron prompt:

1. Get job ID via `CronList`
2. `CronDelete <old_id>`
3. `CronCreate` with updated paths

## Coordinating with User Sends

The cron job creates drafts but never sends. The user manually reviews and sends from Gmail Drafts folder. This is the right architecture — never auto-send dealer emails since:

- An incorrect draft could damage relationships
- User needs to verify final wording, especially OTD numbers and walk-away phrasing
- Gmail API best practice: separate authoring (AI) from sending (human)

## Status Reporting Conventions

Per cycle, output one of:

- `No new dealer mail this cycle` — if no new threads match
- `Scanned N threads, processed X new replies, skipped Y` — if new mail
- For each processed reply, mention: dealer name, key finding, draft ID

## Stopping the Loop

When buyer makes their final decision (commits to a vehicle and signs):

1. Run `CronDelete <id>` to stop the loop
2. Send polite walk-away emails to all other active dealers
3. Archive the working directory with date stamp
