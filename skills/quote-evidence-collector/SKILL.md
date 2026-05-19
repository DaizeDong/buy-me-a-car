---
name: Quote Evidence Collector
description: Use when the buyer wants to FIND online dealer quote screenshots (XHS / Reddit / Facebook / Carfax) to use as cross-bid anchors for negotiation, without engaging the full 9-phase pipeline. Triggers include "find quote screenshots", "find dealer evidence", "scrape XHS for quotes", "Reddit OTD reports", "搜集报价截图", "找证据图", "找别人 dealer 给的报价".
---

# Quote Evidence Collector

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.

last_verified: 2026-05-18

Narrow-trigger skill: surface REAL dealer quote screenshots from public sources
(XHS / Reddit / Facebook / aggregators) for use as cross-bid negotiation anchors.
Defers heavy method content to `../orchestrator/references/deal_data_sources.md`
and hands off finished image sets to `../dealer-reply-drafter/SKILL.md`.

## When to invoke

User says any of: "find quote screenshots", "find dealer evidence", "scrape XHS
for quotes", "Reddit OTD reports", "find what other people paid", or the CN
triggers in the frontmatter. Skip this skill if the buyer is still at Phase 1
(criteria not locked) -- the broader orchestrator should run instead.

## State-aware search decision tree

Per orchestrator gotcha S5: the buyer's state dictates which source has the
densest same-model quote evidence. Run the FIRST matching branch; do not blast
every source.

| Buyer state | Primary source | Secondary | Why |
|---|---|---|---|
| NJ / NY / CA | XHS (search_result + state keyword) | Reddit r/{Make}{Model} | Chinese-American buyer community concentrated in tri-state + CA; they routinely post dealer worksheets. |
| TX / FL / IL / GA / WA | Reddit r/{Make}{Model} + r/{State}Cars | XHS (generic only) | English-language buyer forums dominate; XHS has thin regional coverage. |
| Boomer-heavy makes (Ford F-150, RAM 1500, classic Mustang) | Facebook owner groups | Reddit | Owner FB groups are where pickup buyers post window stickers. |
| Other states | Reddit r/{Make}{Model} + r/{State}Cars | Aggregator screenshots (CarGurus, Edmunds) | Default fallback. |

Always run TWO parallel XHS searches when buyer's state is known: generic
keyword for national anchor + state-specific keyword (English state abbrev OR
Chinese state name, e.g. NJ / xin-ze-xi / niu-yue) for regional anchor. The
state-specific search surfaces same-dealer same-trim quotes that dwarf generic
posts in anchoring power (gotcha S5).

## 5-step XHS Playwright workflow

Verbatim from `../orchestrator/references/deal_data_sources.md` (XHS Post Image
Extraction). Run after the buyer has logged into XHS in the Playwright MCP
window (one-time QR / SMS, cookies persist).

### Step 1 -- browser_navigate to the post

Use the `/search_result/{id}?xsec_token=...` form, NOT the plain `/explore/{id}`
form. Per gotcha S3, the `/explore/` form 404s without an access token. Token
comes from a fresh search-page anchor's `href` -- do `browser_evaluate` on
`https://www.xiaohongshu.com/search_result?keyword=<query>` first, harvest
`a[href*="/search_result/"]` href values, then navigate. Tokens may expire after
~24h; re-search if 404.

### Step 2 -- browser_evaluate to extract images + body in one call

```js
() => ({
  imgs: Array.from(document.querySelectorAll('img'))
              .map(i => i.src)
              .filter(s => s.includes('xhscdn')),
  body: document.body.innerText.slice(0, 4000)
})
```

One MCP call returns both image URLs and post text -- saves round trips.

### Step 3 -- Python urllib download with Referer header bypass

XHS image hosts (`sns-webpic-qc.xhscdn.com`) return 403 to anonymous requests.
The Referer header pointing at xiaohongshu.com is the bypass.

```python
req = urllib.request.Request(url, headers={
    "Referer": "https://www.xiaohongshu.com/",
    "User-Agent": "Mozilla/5.0",
})
with urllib.request.urlopen(req) as r, open(fn + ".webp", "wb") as f:
    f.write(r.read())
```

### Step 4 -- PIL webp -> PNG conversion

```python
from PIL import Image
img = Image.open(fn + ".webp")
img.save(fn + ".png", "PNG")
```

The Read tool can view PNG; webp is unreliable across versions.

### Step 5 -- Read each downloaded image, `rm` non-evidence files

Per gotcha S4, ~80% of XHS post images are NOT useful quote evidence. Open every
PNG with Read, classify, delete rejects immediately so subsequent passes have a
clean working set.

## Image triage rules

| Verdict | Image type |
|---|---|
| KEEP | dealer worksheet / sales-rep email or SMS screenshot / Costco quote sheet / iMessage with $ amounts / window sticker / OTD breakdown PDF page |
| DISCARD | manufacturer stock photo / delivery selfie / Apple Notes title card / decorative emoji cover / pure marketing creative |

When unsure, KEEP and let the buyer adjudicate. Discarding a real worksheet is
worse than carrying one extra file.

## Image compression for manual paperclip

Per orchestrator E5 (manual-paperclip is the only legible path; MCP inline
forces 16-20 KB tiny unreadable images):

```python
from PIL import Image
img = Image.open("xhs-quote-a.png")
img = img.resize((1300, int(img.height * 1300 / img.width)), Image.LANCZOS)
img.save("_FINAL_dealer-a-premium-otd.jpg", "JPEG",
         quality=88, optimize=True)
```

Target: 100-300 KB JPGs, 1080-1300 px width, fully legible. Filename:
`_FINAL_<dealer>-<trim>-<datapoint>.jpg`. The `_FINAL_` prefix makes the curated
set obvious in the working directory.

## REAL vs SYNTHESIZED tagging

Per Critical Rule #7: every collected datapoint MUST be tagged at capture time.

| Tag | Definition | Citable to dealer? |
|---|---|---|
| REAL | Actually scraped with source URL + pulled-at timestamp + image on disk. | YES -- paste the number, attach the image. |
| SYNTHESIZED | Internal-reasoning estimate from heuristics, training data, or "buyers report X". | NEVER -- for thinking only. |

Pasting a SYNTHESIZED number into a dealer email converts internal reasoning
into a fabricated citation -- unrecoverable if challenged. Per-image metadata
should record: `source_url`, `pulled_at`, `tag=REAL`, `dealer_or_anonymized`,
`trim`, `state`.

## Per-dealer attachment etiquette (E5)

| Sending to dealer X | Can attach | Cannot attach |
|---|---|---|
| Any dealer | 3rd-party aggregator (CarGurus, Cars.com, Edmunds) / Reddit / XHS / Competitor Dealer Y's quote | Dealer X's own ad or Internet Pricing screenshot |

Attaching X's own ad back to X reveals you shop their public listing -- kills
negotiation. Same attachment set across all parallel-bid dealers is fine.

## Handoff to dealer-reply-drafter

After triage + compression, emit a per-draft attachment recipe table:

| Dealer | Draft id | Files (in order) | Why |
|---|---|---|---|
| an in-state Subaru dealer | draft-LS-01 | `_FINAL_dealer-a-premium-otd.jpg`, `_FINAL_xhs-touring-32k.jpg` | Two locked benchmarks for the OTD ask |
| <Dealer name> | draft-OR-01 | `_FINAL_dealer-a-premium-otd.jpg`, `_FINAL_xhs-touring-32k.jpg` | Same set (parallel cross-bid; gotcha D11 confirmed independent) |

Then hand off to `../dealer-reply-drafter/SKILL.md` for compose.

## Worked example

Buyer state NJ, target 2024 Subaru Outback Premium. Decision tree -> XHS primary.
Ran TWO parallel XHS searches: generic Mandarin quote keyword ("bao-jia") +
state-prefixed Mandarin quote keyword (NJ + Mandarin state name + "bao-jia").

- ~15 posts surface, ~50 images downloaded.
- After triage: ~10 keepers (dealer worksheets + email screenshots from
  in-state dealer brands).
- Compress to `_FINAL_*.jpg` at 1300 px / quality 88, all under 300 KB.
- All tagged REAL with source URLs + pulled_at timestamp.
- First-touch emails cite the in-state dealer anchors by city, attach
  2 files each via manual paperclip.

Cycle time: ~50 minutes from "find me quotes" to "emails ready to send".

## Cross-references

- `../orchestrator/references/deal_data_sources.md` (XHS Post Image Extraction
  + Browser Session Workflow).
- `../orchestrator/SKILL.md` Critical Rule #7 -- REAL vs SYNTHESIZED tagging.
- `../orchestrator/SKILL.md` gotchas S3 (404 without xsec_token), S4 (80% noise),
  S5 (state keyword for regional density).
- E5 attachment etiquette in `../orchestrator/SKILL.md` Outbound Email SOP.

## Output contract

```
Quote evidence pass -- <timestamp>
  Sources searched: [XHS:<n_searches>, Reddit:<n>, FB:<n>]
  Raw images downloaded: N
  After triage (KEEP): N  [list filenames]
  After triage (DISCARD): N
  REAL-tagged + compressed: N  [list _FINAL_*.jpg names]
  Per-dealer attachment recipe: [table above]
```

Then hand off to `../dealer-reply-drafter/SKILL.md` with the recipe table.
