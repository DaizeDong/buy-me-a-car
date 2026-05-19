# Email Draft Format Rules (Plain ASCII Only)

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

Gmail Drafts created via the `mcp__claude_ai_Gmail__create_draft` API render as plain text in Gmail compose view. Markdown markers and Unicode punctuation render as literal characters, which looks unprofessional to dealers.

## Language Rule (mandatory)

**Dealer-facing emails are ALWAYS English-only.** This is independent of the buyer's preferred language for chat dialogue, `criteria.md`, or the dossier. The rule covers:

- Every Gmail draft saved via `create_draft`
- Every first-touch, counter, follow-up, walk-away, hold, deposit, PPI, CARFAX, add-on refusal, F&I hard-no, and close-day email
- Every SMS or text-channel message sent to a dealer rep
- Every dealer-form submission (lead form, OTD request form, finance pre-qual form)

No Chinese characters, no Spanish text, no non-English content under any circumstance. CRM systems used by US dealers (VinSolutions, DealerSocket, eLead, DriveCentric) sometimes strip or mangle non-ASCII Unicode silently; the dealer rep may see "?" boxes or whitespace where the buyer's text should be. The buyer's negotiating posture degrades.

The bilingual SKILL trigger phrases ("buy me a car" / "帮我找车") signal acceptable buyer-side languages for the agent-to-buyer surface. They do NOT authorize bilingual content in dealer-facing emails. See SKILL.md § Language and audience separation for the full surface-by-surface language matrix.

If the buyer's `criteria.md` is in Chinese or another language, translate buyer-profile values (name, city, state, walk-away ceiling) into English at draft-creation time. The values go into the dealer email in English regardless of which language `criteria.md` was authored in.

## Do NOT Use

| Forbidden | Reason |
|-----------|--------|
| `**bold**` or `__bold__` | Renders as literal `**word**` |
| Backticks for code or values | Renders as literal backticks |
| `[text](url)` link syntax | Renders as literal brackets and parens |
| Em-dash `—` (U+2014) | Non-ASCII; some clients render `?` |
| En-dash `–` (U+2013) | Non-ASCII |
| Curly quotes `"smart"` `'smart'` | Non-ASCII; better to use straight quotes |
| Section dividers `---` or `***` | Renders literally |
| Heading markers `# H1` `## H2` | Renders as literal `#` chars |
| Strikethrough `~~text~~` | Renders literally |
| Unicode bullets `•` `▪` `◦` | Use ASCII `-` instead |
| Curly apostrophe `'` (U+2019) | Use straight apostrophe `'` |

## Do USE

| Allowed | Notes |
|---------|-------|
| ASCII hyphen `-` | For bullet lists, ranges ($2,300-3,450), dashes |
| Plain numbered lists `1. text` | Standard ASCII |
| Colon `:` for list-introducing phrases | "Mileage: at 73,000 mi" not "Mileage — at 73,000 mi" |
| Period + new sentence | Use to replace em-dash breaks: "Got it. Thanks." not "Got it — thanks." |
| Comma for soft pauses | "Got the quote, thanks." instead of "Got the quote — thanks." |
| Straight quotes `"` `'` | Standard ASCII |
| Blank lines for section separation | Instead of `---` or `***` |
| Plain text URLs | `https://example.com` written out, not `[Example](url)` |
| Sign-off: just the name | `{{BUYER_NAME}}` with NO leading dash, NO em-dash |

## Conversion Patterns

When migrating a markdown-laden draft to plain ASCII:

### Em-dash to alternative

| Source | Replacement |
|--------|-------------|
| `Got the quote — thanks.` | `Got the quote, thanks.` |
| `Mileage — at 73k mi` | `Mileage: at 73k mi` |
| `understand — I will move forward` | `understand. I will move forward` |
| `cash — no trade — no financing` | `cash, no trade, no financing` |

### Bold to no-emphasis

| Source | Replacement |
|--------|-------------|
| `**Sales price**: $20,500` | `Sales price: $20,500` |
| `**$30,000 OTD**` | `$30,000 OTD` |
| `**Key concerns**:` | `Key concerns:` |

### Code values to plain

| Source | Replacement |
|--------|-------------|
| `` VIN `1ABCD23456EFGHIJK7` `` | `VIN 1ABCD23456EFGHIJK7` |
| `` See `tracker.md` `` | `See tracker.md` |

### Link to plain URL

| Source | Replacement |
|--------|-------------|
| `[CARFAX Report](https://...)` | `CARFAX Report: https://...` |

### Section divider

Use a blank line, not `---`.

## Sign-Off Convention

| Forbidden | Allowed |
|-----------|---------|
| `— Buyer Name` | `Buyer Name` |
| `-- Name` | `Name` (or `-- Name` for traditional sig delimiter) |
| `Best, — Name` | `Best, Name` |

The traditional ASCII signature delimiter is two hyphens followed by a space (`-- `). This is acceptable but optional.

## Verification

Before creating any Gmail draft, scan the body for:

1. Any `**` chars → strip
2. Any `—` chars → replace with `, ` or `. ` or `: ` depending on context
3. Any backticks → strip
4. Any `[...](...)` patterns → write out
5. Any curly quotes → straighten

When in doubt, paste the draft into a plain text editor (Notepad, vim) and visually inspect. If it doesn't look right in plain text, dealers won't see it right either.

## Why This Matters

Dealer sales reps use varied email clients:
- Outlook with default plain-text rendering
- Gmail mobile app
- eDealerHub / VinSolutions CRM (often strips formatting)
- Older mail clients

Markdown markers and non-ASCII Unicode render inconsistently and look amateurish or even broken. A buyer who sends `**OTD $30,000**` in a critical negotiation email looks like they don't know how to use email.

Stay ASCII-only and the message reads correctly everywhere.

## Verification Habit

Before saving any Gmail draft, grep the body for the forbidden character set above. Dealer-facing emails are high-stakes; broken formatting in a counter-offer or walk-away email degrades the buyer's negotiating posture.
