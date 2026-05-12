# Email Draft Format Rules (Plain ASCII Only)

Gmail Drafts created via the `mcp__claude_ai_Gmail__create_draft` API render as plain text in Gmail compose view. Markdown markers and Unicode punctuation render as literal characters, which looks unprofessional to dealers.

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
| Sign-off: just the name | `[Buyer name]` with NO leading dash, NO em-dash |

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
