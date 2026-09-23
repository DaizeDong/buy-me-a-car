# Outbound email SOP

## 1. Establish the approved content

Use existing user decisions first. Resolve only missing vehicle/trim, payment
posture, close date, attachment plan and outward offer decisions. A draft-only
request permits local composition; it does not authorize sending or new purchase
commitments. Keep `walk_away` private in every negotiation round.

Populate a private policy with buyer-approved ask sentences, a separately approved
`authorized_offer`, private values to exclude, and confirmed anchor records. Never
derive the outward offer from the internal maximum. Evidence needs its source,
text, SHA-256, observation/expiration dates, price basis and buyer confirmation.
Listing prices are not written OTD quotes. Document evidence gaps rather than
inventing statistics, competing bids, statutory caps or deadlines.

## 2. Render and validate before creating a provider draft

Select `ask_ids`, `anchor_ids` and `include_offer`, then call
`scripts/email_policy.py`. The CLI accepts only paths relative to the private
companion data directory:

```text
python skills/orchestrator/scripts/email_policy.py --policy negotiation/policy.json --plan negotiation/plan.json --output negotiation/draft.txt
```

This command reads and writes private companion paths through `tools/runtime_paths.py`.
It has no repository fallback. The validator rejects private ceiling/value leakage,
unauthorized offers, fabricated anchor IDs, stale/unconfirmed/mismatched evidence,
new/used mixing and any body that differs from the approved rendering.

Its `verified` result proves those deterministic checks only. Exact approved ask
sentences and evidence authenticity still need human review. A model's claim that
its draft is safe does not satisfy the gate. Missing independent qualitative review
must remain `unavailable`; do not call it passed.

## 3. Prepare attachments privately

Resolve attachment paths through `tools/runtime_paths.py`, for example
`attachments/quote-1.jpg` under private data. Preserve legibility and inspect the
actual exported image/PDF. Exclude buyer budget notes, local path headers, account
details and other private information from dealer-facing files.

Determine the installed host's actual attachment support. If it cannot attach full
resolution files reliably, give the buyer private file paths for manual attachment.
Do not claim "screenshots attached" until the attachments are present and checked.
Do not assume every connector has the same size restrictions or capabilities.

## 4. Record one operation, then reconcile one receipt

Import complete message pages and mark actionable messages with `inbox_state.py`.
Preparing a draft validates the plan again and records a stable operation ID, message
ID, account ID, exact body hash and status. Export commits `uncertain` BEFORE exposing
the operation to a host adapter. The adapter must deduplicate that operation ID.

Only a matching provider receipt changes status to `draft_saved`. If saving times
out, fails after submission, or the process dies, inspect provider state by operation
ID. Do not create another draft to discover whether the first call succeeded. A
provider-confirmed `not_created` receipt records failure; it does not auto-retry.

The offline import/export ledger is not a Gmail connector. With no live adapter,
report "local draft prepared; provider save unavailable". Do not invent a draft ID.

## 5. Buyer review and send

Present recipient, subject, body and attachment list. The ledger's operation is
`create_draft`, never send. Follow the buyer's existing authorization for any external
action; do not create a new approval ritual for decisions already supplied.

Before a changed quote produces a replacement, reconcile the old draft and identify
the affected draft IDs for the buyer. Never delete original inbound/sent messages.
Do not use broad Gmail search strings as a substitute for exact draft identity.

Business-hour delivery can be useful, but it is advisory. Do not assert universal
response-time advantages or invent urgency. When coordinating stores across time
zones, choose a time that is within each participating dealer's local hours.

After an authorized send, monitoring resumes from the persisted provider cursor.
See `cron_monitoring.md` for restart, pagination and adapter requirements.
