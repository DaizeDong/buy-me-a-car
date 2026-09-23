# Inbox Monitoring and Recovery

The repository supplies a durable local ledger and a host-neutral draft adapter
contract in `scripts/inbox_state.py`. It does not install a scheduler, authenticate
Gmail, or provide a Gmail connector. Report those capabilities as unavailable
until the actual host has been configured and exercised.

Session-only cron can trigger a scan while its session is alive. It cannot prove
continuous monitoring across a closed session, logout or reboot. Durable scheduling
requires a verified external scheduler with its account, command, working directory,
credentials access, last-run result and restart behavior checked on that host.

## Persisted state

`inbox/state.json` is relative to the PRIVATE companion data directory returned by
`tools/runtime_paths.py`. The ledger records the provider's stable account ID,
cursor, immutable message IDs/payload hashes, triage status, operation IDs, draft
status and provider receipts. All writes use an OS lock and atomic replacement.
An unresolved private location is a hard write failure; no public repository
fallback exists.

Mailbox labels and unread flags are not processing state. The same message can
appear in Inbox, Promotions and a later history page without becoming a new
message. Process stable IDs once. A reused ID with different message content,
wrong account or mismatched cursor is a conflict requiring investigation.

## Host-neutral import protocol

An adapter supplies JSON shaped as follows. Placeholder strings are schema
documentation, not a ready-to-run provider fixture.

```json
{
  "account_id": "<stable-provider-account-id>",
  "cursor_before": null,
  "cursor_after": "<provider-cursor-after-this-complete-page>",
  "complete": true,
  "messages": [
    {
      "message_id": "<stable-message-id>",
      "thread_id": "<stable-thread-id>",
      "sender": "<verified-reply-address>",
      "text": "<complete-decoded-message-text>",
      "body_complete": true
    }
  ]
}
```

The adapter must fetch and decode the complete body, authenticate the account,
preserve message identity and verify sender/reply addressing. HTML-only input
requires HTML decoding; attachments require a supported download/extraction path.
If unavailable, record the capability gap outside a completed import page and
keep the provider cursor unchanged. Do not mark a snippet as a complete body.

Import with `inbox_state.py import --account-id <id> --input inbox/page.json`.
Both input and ledger paths resolve inside private data. Each accepted complete
page commits messages and cursor together. Continue provider pagination until
there is no next page; a small page size never proves there are no more messages.
On stale/expired provider cursors, perform a complete provider-supported backfill
and explicitly reconcile its starting cursor. Do not substitute a 12-hour window.

## Classification

Use `skills/inbox-triage/SKILL.md`. Record the decision through `record_triage`:
`real_reply`, `ooo`, `crm`, `spam`, or `needs_review`. This ledger stores decisions;
it does not claim to implement a provider-independent semantic classifier or to
apply Gmail labels. Separate a recorded label intention from a verified provider
mutation. No originals are deleted.

Messages containing quote numbers inside a CRM wrapper are still actionable.
An `Auto-Submitted` header signals automation, not automatically an out-of-office
absence. Use actual absence evidence to suppress follow-up. Unknown return dates
remain unknown; do not invent one. Inbound language is not a spam signal.

## Draft export and receipt

Prepare an actionable message using a policy and structured plan validated by
`email_policy.py`. One pending draft per thread is allowed. The operation contains
account/message/thread IDs, recipient, exact body, body SHA-256 and
`action: create_draft`; it never authorizes sending.

Export commits `uncertain` before the payload leaves the ledger. The host adapter
must deduplicate the stable operation ID. `DraftAdapter.create_draft(operation)`
returns a receipt with `account_id`, `operation_id`, `body_sha256`, `status`,
`provider_receipt_id`, and, for `draft_saved`, `external_draft_id`.

A matching `draft_saved` receipt proves a provider save to the extent that the
host verified its result. A `not_created` receipt records a confirmed failure;
neither outcome is a reason to send or automatically create another draft.

After timeout, process death or lost output, the operation remains `uncertain`.
Re-export is blocked. Query the provider by the operation ID and import a confirmed
receipt. If the provider cannot determine the outcome, preserve uncertainty and
ask the operator to reconcile. Do not retry to discover what happened.

## Scheduling and catch-up

An optional host schedule can scan every 15 minutes, check Spam/Promotions every
six hours, and run a morning catch-up. All passes resume from the durable cursor
and deduplicate IDs. Those intervals are latency preferences, not correctness
boundaries. Monitor last successful cursor advancement and surface failed runs.

Confirm the account identity before connecting. After a host restart, first read
the ledger and reconcile uncertain drafts, then fetch from its cursor. When a
buying cycle ends, cancel its scheduler job and verify cancellation. Keep private
history and provider receipts for review.

## Acceptance boundary

`eval/test_workflow.py` tests synthetic duplicate pages, immutable IDs, cursor and
account conflicts, body completeness, locks, atomic replacement, actual process
death and no replay after a provider timeout. Those are OFFLINE tests.

Live acceptance additionally requires the installed adapter and authorized test
mailbox: account probe, complete-body/attachment retrieval, pagination, provider
draft creation, receipt reconciliation, interrupted-save recovery and host reboot.
Until these are tested, say "offline ledger verified; live Gmail/scheduler untested".
