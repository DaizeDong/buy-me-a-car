# Cron-Based Inbox Monitoring

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

## Gmail Search Syntax Tips

Use these in the `query` parameter of `mcp__claude_ai_Gmail__search_threads`:

| Pattern | Purpose |
|---------|---------|
| `to:{EMAIL} newer_than:1h` | Inbox-only, recent |
| `category:promotions` | Promotions tab (many dealer emails land here, NOT inbox) |
| `in:anywhere` | Include Spam and Trash |
| `-from:CARFAX` | Exclude Carfax notifications |
| `-from:no-reply -from:noreply -from:alerts` | Exclude common auto-mailers |
| `-from:bank -from:newsletter` | Exclude personal/work mail |

Full example query:

```
to:{BUYER_EMAIL} newer_than:1h
  -from:CARFAX -from:no-reply -from:noreply -from:alerts
  -from:bank
  -from:newsletter
  -from:your-academic-list -from:your-work-domain
```

This filters to "dealer-like, recent, not auto-generated" threads.

## Pagination

`pageSize: 30` (max 50) is sufficient for hourly scans of one buyer's inbox. Most buyers see 5-20 dealer replies in their busiest days.

## Skip-List Identification

Common auto-mailers to filter:

- `CARFAX@event.carfax.com` (Carfax confirmation per submission)
- `CARFAX@no-reply.carfax.com` (Carfax marketing)
- `no-reply@accounts.google.com` (Google security)
- `alerts@account.<bank-domain>` (banking)
- `onlinebanking@<bank-domain>` (banking)
- `noreply@<service-domain>` (banking)
- Various academic / professional list-server addresses

Common autoresponder phrases to skip:

- "currently closed"
- "will be in touch"
- "appreciate your patience"
- "Welcome to the Adventure at" (Subaru CRM template)
- "Reply YES to receive text messages"

## Cron Lifecycle

- 15-min intervals × 96 cycles/day × 7-day TTL = ~672 cycles max
- Session-only cron dies with the Claude Code session; use `durable: true` to persist across restarts only if the buying timeline is multi-day and the buyer wants to keep the assistant alive
- Cancel manually with `CronDelete <job_id>` once the buying decision is made

## Path Updates

If the project directory changes (e.g., files moved from home directory to `{HOME}\car_buying_2026\`), update the cron prompt:

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
