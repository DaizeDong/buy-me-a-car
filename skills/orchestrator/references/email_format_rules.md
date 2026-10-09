# Email draft format rules

Historical format observation: **2026-05-18** (skill stress test iteration 5 and
P0-P5 consolidation). The `mcp__claude_ai_Gmail__create_draft` API used in that
check rendered drafts as plain text. Verify the current host's capabilities
before exporting a draft; that observation does not establish present access.

## Language and audience

The shipped dealer-email renderer produces plain ASCII English. Apply this
format to dealer drafts, first contact, counters, follow-ups, walk-away messages,
holds, deposits, PPI/CARFAX requests, add-on refusals, F&I and close-day emails.
Use the same format for dealer SMS and form text prepared through this workflow.
Buyer conversation, criteria and reports use their separately supported languages.

If the buyer requests a different outward language, explain the renderer's
ASCII-only limit and prepare an explicitly reviewed alternative. Do not silently
drop or transliterate unsupported text. Follow the
[reply drafter](../../dealer-reply-drafter/SKILL.md) for the current language,
content, line-count and approval requirements.

Translate only approved outward content from the buyer's criteria. Keep the
private `walk_away` ceiling and any range derived from it out of dealer text,
filenames and attachments. An `authorized_offer` is a separate buyer-approved
amount; translating criteria does not authorize its disclosure or an offer.

## Plain-text format

Markdown markers can remain visible in plain-text email, and non-ASCII characters
may be altered by dealer CRM systems such as VinSolutions, DealerSocket, eLead
and DriveCentric. Use these formatting rules:

| Content | Required format |
|---|---|
| Emphasis | Plain words; remove `**bold**`, `__bold__` and `~~text~~` markers |
| Code or values | Plain text without backticks |
| Links | Write the URL out instead of `[text](url)` |
| Headings and separators | Plain labels and blank lines instead of `#`, `##`, `---` or `***` |
| Bullets and ranges | ASCII hyphen `-`; no Unicode bullets |
| Pauses | Comma, colon or a new sentence instead of U+2014 em dash or U+2013 en dash |
| Quotation marks | Straight ASCII quotes and apostrophes instead of curly forms, including U+2019 |
| Lists | ASCII numbered lists such as `1. text` |
| Sign-off | Buyer name without a leading dash; optional traditional delimiter `-- ` on its own line |

## Verification

Before saving a provider draft:

1. Apply the [outbound email SOP](outbound_email_sop.md) and validate the exact
   approved rendering with `scripts/email_policy.py`.
2. Check for Markdown emphasis, backticks, Markdown links, heading markers,
   section dividers, curly punctuation and non-ASCII bullets.
3. Inspect the plain text for readable line breaks, complete URLs and an accurate
   sign-off. Dealer clients include Outlook, Gmail mobile, eDealerHub and
   VinSolutions; ASCII formatting does not guarantee identical display in each.
4. Verify the recipient, subject, body and attachments under the existing
   authorization. Follow the SOP for operation IDs, provider receipts and
   uncertain execution; format validation alone does not prove a draft was saved.
