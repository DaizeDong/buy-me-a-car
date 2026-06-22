# Deal Data Sources & Market Research Pipeline

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

This reference covers where to pull **real-time transaction prices, dealer discounts, and incentive data** to back up negotiation positions. Use this to replace heuristic estimates ("launch year discount is $500-1,500") with actual market data (e.g., "<Dealer Name> has 2026 <Model Trim> at $<internet-price> with $<advertised-discount> off").

## Verified Source Status (tested 2026-05-15 via Firecrawl)

Every entry below has been actually scraped. Do NOT assume a source works because it's a famous brand — many fail in specific ways.

| Source | Direct scrape | Key fields recovered | Workaround if blocked | Status |
|---|---|---|---|---|
| **CarEdge** (`caredge.com/shop-cars/new/{VIN}`) | ✅ Works | MSRP, Dealer Discount, Asking Price, Doc Fee, Invoice link | n/a | TIER 1 |
| **Subaru.com** (`subaru.com/vehicles/forester/`) | ✅ Works | Official MSRP across all trims/configs, Special Offers links, APR Financing | n/a | TIER 1 |
| **Dealer Internet Pricing** (e.g., `<dealer-domain>/new-...`) | ✅ Works | Internet Price, Dealer Savings $, manufacturer rebate links | n/a | TIER 1 |
| **Cars.com research** (`cars.com/research/{make}-{model}-{year}/`) | ✅ Works | Listing prices, trim MSRP ranges | n/a | TIER 1 |
| **KBB** (`kbb.com/{make}/{model}/{year}/`) | ✅ Works (huge page ~650KB) | Fair Purchase Price, MSRP range start-to-top-trim, base/loaded spread | n/a | TIER 1 |
| **CarGurus ZIP-filtered** (`cargurus.com/Cars/inventorylisting/...?zip={ZIP}`) | ✅ Works | Per-listing "Great Deal/Good Deal/Fair Price" ratings, prices | Plain `/Cars/l-Used-...` URL works less well — always include ZIP | TIER 1 |
| **Edmunds** (`edmunds.com/{make}/{model}/`) | ❌ **Akamai 403** | n/a directly | ✅ Wayback Machine: `web.archive.org/web/2026/https://www.edmunds.com/{make}/{model}/` recovers full content including "buyers paying X% below MSRP" data | TIER 2 (via workaround) |
| **Reddit** (any r/ URL) | ❌ **"Site not supported"** via scrape API | n/a via scrape API | ✅ **Browser session bypasses** — `firecrawl browser "open <url>"` + `get text body` extracts ALL buyer OTD data (verified: $37,378/$36,150/$35,573 OTD figures recovered from one post). No login required for public Reddit. Also `firecrawl search "site:reddit.com"` snippets work as fallback. | **TIER 1** (via browser session) |
| **TrueCar** (`truecar.com/prices-new/...`) | ❌ **JS client-side error** via scrape | n/a | ⚠ Untested via browser session; likely works since browser handles JS. If TrueCar zip-lookup is critical, try `firecrawl browser "open <truecar-url>"` + wait + `get text body`. | TIER 2 (try browser session) |
| **Facebook** (group post URLs) | ❌ **"Site not supported"** via scrape API | n/a via scrape API | ✅ Browser session with login: open URL via session, share Live View URL with buyer for FB login, then `get text body` extracts post + comments after auth. Cookies persist in `--profile` for future runs. | **TIER 1** (via browser session + login) |
| **Instagram** (post URLs) | ❌ **"Site not supported"** via scrape API | n/a via scrape API | ✅ Browser session with login (verified browser opens the page and shows login dialog — buyer logs in via Live View, profile saves cookies). Use `get text body` for caption text + `screenshot` for image content. | **TIER 1** (via browser session + login) |
| **XiaoHongShu** (`xiaohongshu.com/explore` or post URL) | ❌ **Login wall** via scrape | n/a | ✅ Browser session with login (verified browser opens search page, shows "登录后查看搜索结果" wall — buyer logs in via Live View with phone/QR, profile saves cookies for re-use). Then `get text body` extracts post Chinese text content. | **TIER 1** (via browser session + login) |
| **YouTube** (`youtube.com/watch?v=...`) | ⚠ Partial | Video title + description only, NOT full transcript | None — Firecrawl returns metadata, not auto-generated captions | TIER 3 (metadata) |
| **CarsDirect** (`carsdirect.com/deals-articles/...`) | ⚠ Generic article pages return placeholder prices ($10k/$20k/$30k buckets) | None on overview pages; specific deal article URLs work | ✅ `firecrawl search "site:carsdirect.com {make} {model} incentives {month}"` finds the right article URL | TIER 2 (need specific URL) |
| **Google Search direct scrape** | ❌ **CAPTCHA challenge** | n/a | ✅ Use `firecrawl search` command (uses different backend with proxy rotation) | n/a |

### Playwright MCP Local Browser (preferred over Firecrawl Live View for login sites)

When user needs to log into a site (XiaoHongShu, Facebook, Instagram), **Playwright MCP local browser is strictly better than Firecrawl Live View URL** because:
- Pops up an actual browser window on user's screen (vs requiring them to open a URL)
- User clicks/types directly with their own mouse/keyboard
- No need to share/copy a token URL
- Cookies persist in their actual browser profile

**Workflow** (verified 2026-05-17 on XiaoHongShu):

```python
# 1. Navigate to target URL — local browser pops up automatically
mcp__plugin_playwright_playwright__browser_navigate(
    url="https://www.xiaohongshu.com/search_result?keyword=<query>"
)

# 2. User logs in directly in the popped-up window (phone QR scan / SMS)
# Tell user: "Browser window is open on your screen. Login there."

# 3. After user confirms login, take snapshot or screenshot
mcp__plugin_playwright_playwright__browser_snapshot(depth=5)
mcp__plugin_playwright_playwright__browser_take_screenshot(
    type="png", filename="result.png", fullPage=True
)

# 4. Click into specific posts via ref IDs from snapshot
mcp__plugin_playwright_playwright__browser_click(
    element="MOMO post with dealer email screenshot",
    target="e210"  # ref from snapshot
)

# 5. Capture detail screenshots, navigate back, repeat

# 6. Close when done
mcp__plugin_playwright_playwright__browser_close()
```

**Playwright vs Firecrawl session decision matrix**:

| Use case | Tool | Why |
|---|---|---|
| Public Reddit, no login | Firecrawl browser session | Cloud-hosted, no local setup |
| XHS / FB / IG (login needed) | **Playwright MCP local** | Local pop-up, easier user login |
| Bulk scraping 50+ URLs | Firecrawl browser session | Cloud parallelism, no local CPU |
| Large screenshot capture | Playwright MCP | Faster, no upload bandwidth |
| Sites with DataDome / Akamai | Try both — Playwright local sometimes wins | Local IP less flagged than cloud |

### Inventory SRP scraping (Phase 3) — Playwright-first, real browser wins on ALL of them

**Verified 2026-06-21 (used CX-5, SF Bay Area).** This is about pulling LISTINGS (VIN + price + mileage + dealer) from search-result pages, distinct from the deal/pricing sources above. Finding: a headless `WebFetch` from a subagent gets **403 / DataDome / Akamai on every inventory SRP except CarGurus** — but the **real Playwright MCP browser unlocked all 8 sites tested** (Carfax, CarGurus, Cars.com, AutoTrader, Edmunds, TrueCar, CarMax, Carvana). Local Chromium clears the anti-bot checks that block both headless WebFetch and Firecrawl cloud.

Extraction priority: **JSON-LD** (`script[type="application/ld+json"]` @type Car — TrueCar, Carvana) > **embedded JS state** (Carfax `window.__MOBX_STATE__.SearchRequestStore.results.listings`) > **DOM cards + VIN regex** (`/JM3[A-Z0-9]{14}/g` on `innerHTML` — AutoTrader, Edmunds, CarMax, Cars.com).

The full per-site recipe table (URL pattern, exact selector/state path, fields, gotchas) lives in **`phases.md` -> Phase 3 -> "Per-site scraping recipe"**. Because Playwright is a single shared browser, run the Playwright-fallback passes sequentially (or collapse anti-bot sites into one browser-harvest subagent); keep only the WebFetch-first attempts parallel.

### Browser Session Workflow (UNLOCKS Reddit + FB + IG + XHS)

The Firecrawl `scrape` API blocks Reddit, Facebook, Instagram, XiaoHongShu, etc. with "we do not support this site". **The browser session command bypasses this filter entirely** because it operates a real Chromium instance rather than going through the scrape API. This is the single highest-leverage discovery for deal data — it unlocks the entire community-content tier.

**Verified working** (tested 2026-05-15): Reddit posts open via browser session and `get text body` extracts the FULL page content with all buyer-reported OTD numbers intact. Example output from one Reddit post: extracted "$37,378 otd / $36,150 otd / $35,573 otd" plus context (state, tax rate, dealer name) in a single 7KB text file.

**Standard 5-step workflow** for blocked-source content:

```bash
# 1. Launch session with persistent profile (cookies saved across sessions)
firecrawl browser launch-session --ttl 1800 --profile car-research

# Returns: Session ID + CDP URL + Live View URL
# Live View URL is what the buyer uses to log in interactively

# 2. Navigate to target URL (same session auto-targets via stored session ID)
firecrawl browser "open https://www.reddit.com/r/SubaruForester/comments/{post-id}/"

# 3. Wait for JS render (Reddit/SPA sites need time)
firecrawl browser "wait 3"

# 4. Extract full visible text from page body
firecrawl browser 'get text body' -o ".firecrawl/{site}-{topic}.txt"

# 5. Grep for key data
grep -oiE '\$[0-9]{1,3},?[0-9]{3}|(otd|out the door|MSRP|dealer)[^"]{0,100}' \
  ".firecrawl/{site}-{topic}.txt"
```

For sites requiring login (Facebook, Instagram, XiaoHongShu, sometimes Reddit if private subs):

```bash
# 1. Launch session with profile, capture Live View URL from stdout
firecrawl browser launch-session --ttl 1800 --profile car-research
# Live View URL: https://liveview.firecrawl.dev/<token>

# 2. Open the login page (or directly the target URL — site redirects to login)
firecrawl browser "open https://www.xiaohongshu.com/explore"

# 3. SHARE the Live View URL with the buyer
# Buyer opens URL in their browser. Their mouse/keyboard control the cloud Chromium.
# Buyer logs in via the cloud browser (scan QR / phone / SMS / 2FA — whatever site requires).
# Cookies are saved to the "car-research" profile after login.

# 4. Once buyer confirms login complete, navigate to target content
firecrawl browser "open https://www.xiaohongshu.com/explore/{post-id}"
firecrawl browser "wait 3"
firecrawl browser 'get text body' -o ".firecrawl/xhs-{post-id}.txt"

# 5. NEXT TIME: relaunch with same profile, cookies auto-restore
firecrawl browser launch-session --ttl 1800 --profile car-research
# No re-login needed.
```

**Profile management**:
- `--profile <name>` persists cookies + localStorage across `launch-session` calls
- `--no-save-changes` loads profile read-only (use to prevent profile pollution from one-off tests)
- Profile lives on Firecrawl cloud, not local — works across machines/sessions
- Recommended profile names: `car-research`, `dealer-portals`, `chinese-forums` — one per login domain cluster

**Image-heavy content** (lease flyers, dealer banners, Instagram ad creatives):

```bash
firecrawl browser "open <url>"
firecrawl browser "screenshot path.png"
# OR via scrape API:
firecrawl scrape <url> --format screenshot -o output.json
# Then jq extract the hosted PNG URL and Read it directly (vision-capable)
```

**Available agent-browser commands inside session** (verified subset):
- `open <url>` — navigate
- `wait <ms|selector>` — wait for content to render
- `snapshot` — accessibility tree with @ref IDs (structured, AI-friendly)
- `get text <selector>` — extract text from element (use `body` for full page)
- `get html <selector>` — extract HTML
- `screenshot [path]` — capture PNG
- `pdf <path>` — save as PDF
- `click <@ref|selector>` — click element
- `fill <@ref|selector> <text>` — fill form field
- `eval <js>` — run JavaScript
- `scroll <up|down|left|right> [px]` — scroll page

**NOT a command inside session**: `scrape` (use `get text body` instead for markdown-equivalent text extraction)

### Image Attachment Workflow for Outbound Emails

Capturing screenshots is one step; getting them into outbound dealer emails is another. Key constraints + workflow learned 2026-05-17:

**File size discipline** (PNG → JPG compression mandatory for attachments):
```python
from PIL import Image
img = Image.open('source.png')
if img.size[0] > 1200:  # max 1200px wide preserves text legibility
    img = img.resize((1200, int(img.size[1]*1200/img.size[0])), Image.LANCZOS)
if img.mode == 'RGBA': img = img.convert('RGB')
img.save('compressed.jpg', 'JPEG', quality=75, optimize=True)
```
Typical compression: 1-1.2 MB PNG → 80-120 KB JPG (10x reduction, text still readable).

**MCP Gmail attachment cost reality**:
- Each base64 attachment is `file_size × 1.34` chars
- 100 KB JPG → 134K chars → ~33K tokens per attachment
- 4 emails × 3 attachments = ~400K tokens (eats context window)
- **Recommendation**: create drafts via MCP with NO attachments, then tell user to attach manually via Gmail web UI (paperclip icon)
- User retains control over which dealer gets which screenshot

**Cross-dealer attachment etiquette** (critical):
- NEVER attach Dealer X's Internet Pricing screenshot when emailing Dealer X (insulting, shows you're shopping their own ad against them)
- Safe to attach 3rd-party aggregator screenshots (CarGurus, Cars.com, Edmunds Wayback) to all dealers
- Safe to attach Dealer Y's screenshot to Dealer X (the "your competitor advertised this" play)
- Per-dealer attachment list should be explicit in summary to user

**Hosting alternative**:
- Save screenshots to working directory `quote-images/`
- Tell user the full local path (e.g., `C:\Users\<user>\car_buying_<year>\.firecrawl\quote-images\`)
- User attaches via Gmail web UI → paperclip → navigate to folder
- Clean separation: MCP creates draft text + body, user attaches images

### XHS Post Image Extraction via Playwright MCP (verified 2026-05-18)

For pulling individual quote screenshots OUT of XHS posts (not the cover thumb, not a full-page screenshot), use the Playwright DOM-extract workflow. Firecrawl `--format screenshot` only captures the rendered viewport, which is usually the post header + first image only. The DOM-extract workflow grabs ALL post images at full resolution.

**Step 1 — Find posts via state-specific search**:
```javascript
// Navigate to: https://www.xiaohongshu.com/search_result?keyword=forester+NJ+报价&type=51
// Extract titled cards (NOT plain anchors, which lack titles)
() => {
  const sections = Array.from(document.querySelectorAll('section'));
  const out = [];
  const seen = new Set();
  for (const s of sections) {
    const a = s.querySelector('a[href*="/search_result/"]');
    if (!a) continue;
    const href = a.href;
    if (!href || seen.has(href)) continue;
    seen.add(href);
    const titleEl = s.querySelector('.title, .footer .title, span.title');
    const title = (titleEl ? titleEl.innerText : s.innerText || '')
      .trim().replace(/\s+/g,' ').slice(0, 200);
    out.push({href, title});
  }
  return out.slice(0, 15);
}
```

**Critical: capture the `/search_result/{id}?xsec_token=...` href, NOT the plain `/explore/{id}` form** — the latter 404s without the token. Tokens may expire after ~24h; re-search if you get 404.

**Step 2 — Open a post and extract image URLs + body text**:
```javascript
() => {
  const imgs = Array.from(document.querySelectorAll('img'));
  const out = [];
  const seen = new Set();
  for (const i of imgs) {
    if (!i.src) continue;
    if (i.naturalWidth < 400) continue;  // filter icons + thumbs
    if (i.src.includes('avatar') || i.src.includes('icon') || i.src.startsWith('data:')) continue;
    if (seen.has(i.src)) continue;
    seen.add(i.src);
    out.push({src: i.src, w: i.naturalWidth, h: i.naturalHeight});
  }
  const desc = document.querySelector('#detail-desc, .desc, .note-content, .content');
  return {imgs: out, body: desc ? desc.innerText.slice(0, 1500) : ''};
}
```

The body text often contains key context (selling price, OTD, dealer name, location) — capture it in the same call so you can decide image priority before downloading.

**Step 3 — Download webp images with hotlink-bypass headers**:
```python
import urllib.request, ssl
from PIL import Image
ssl._create_default_https_context = ssl._create_unverified_context

# XHS rejects requests without a Referer header pointing at xiaohongshu.com
hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.xiaohongshu.com/'
}

req = urllib.request.Request(url, headers=hdr)
with urllib.request.urlopen(req) as r, open(fn + '.webp', 'wb') as f:
    f.write(r.read())

# Convert webp to PNG so the Read tool can view it
img = Image.open(fn + '.webp')
img.save(fn + '.png')
```

The image hosts (`sns-webpic-qc.xhscdn.com`) return 403 to anonymous requests. The Referer header is the bypass.

**Step 4 — Triage: view EVERY downloaded image before keeping**:

Roughly 80% of XHS post images are NOT useful quote evidence. Common discardable types:
- Stock manufacturer photos of the car (cover image)
- Author's delivery selfie / parking-lot photo of the new car
- Apple Notes screenshot with handwritten title text only
- Decorative cover card with emoji + post title
- Pure photo of the dealer building or sales lot

Useful types (keep):
- Dealer worksheet (Stock #, VIN, MSRP, Discount, Selling Price, fees, OTD breakdown)
- Email screenshot from sales rep with selling price / OTD text
- iMessage / WhatsApp screenshot with sales rep's quoted number
- Costco Auto Program quote sheet
- Side-by-side dealer comparison spreadsheet

Use the Read tool on each downloaded PNG, then `rm` the non-evidence files immediately.

**Step 5 — Compress evidence for Gmail attachment**:
```python
# After triage, compress kept images to attachment-friendly JPGs
shortlist = ['xhs-quote-a.png', 'xhs-quote-b.png', ...]
for png in shortlist:
    img = Image.open(png)
    if img.size[0] > 1200:
        new_h = int(img.size[1] * 1200 / img.size[0])
        img = img.resize((1200, new_h), Image.LANCZOS)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(png.replace('.png', '.jpg'), 'JPEG', quality=80, optimize=True)
```

Target: 5 final images, ~600 KB combined pack. Document the shortlist in `quote_evidence_shortlist.md` with per-image: what it shows, why it anchors the buyer's market, per-dealer attachment recommendation.

**Geographic search rule** (high-leverage learning):

Generic `forester 报价` returns posts from CA / TX / MI / PA / WV — quotes that anchor the WRONG regional market. Adding state name to the query exposes the buyer's actual tri-state evidence:

| Query | Top NJ-relevant posts in top 10 |
|---|---|
| `forester 报价` | ~2 / 10 |
| `forester NJ 报价` | ~5 / 10 |
| `forester 新泽西 砍价` | ~6 / 10 |

Always run TWO parallel XHS searches when buyer's state is known: (a) generic keyword for national pricing anchor, (b) state-specific keyword for regional dealer anchor. The state-specific search consistently surfaces actual same-dealer same-trim quotes that dwarf generic posts in anchoring power.

### Image Extraction (`--format screenshot`)

`firecrawl scrape --format screenshot` returns a hosted PNG URL in the `screenshot` field. Confirmed working on:
- Dealer specials pages (where text is rendered inside flyer images)
- Listing pages (vehicle photos)

The PNG is hosted at `storage.googleapis.com/firecrawl-scrape-media/screenshot-{uuid}.png` and remains accessible for hours. Read it with the Read tool to extract data from image-only content (lease flyers, dealer banners, etc.).

```bash
firecrawl scrape "https://dealer.com/specials" --format markdown,screenshot \
  -o ".firecrawl/dealer-specials.json"

# Then extract image URL:
python -c "import json; d=json.load(open('.firecrawl/dealer-specials.json')); print(d['screenshot'])"
# -> https://storage.googleapis.com/firecrawl-scrape-media/screenshot-xxx.png
```

For image-heavy social posts (Instagram lease ads, dealer flyers) where text extraction fails, screenshot is the only reliable path.

## When To Pull Deal Data

- **Pre-outreach (Phase 2-3)**: Before sending mass OTD requests, establish realistic OTD floor for the target trim/year/region. Saves wasted cycles on impossible asks.
- **Mid-negotiation (Phase 5)**: When a dealer's quote needs anchoring, cite specific competitor's advertised Internet Price as cross-bid leverage.
- **Pivot decisions**: When user asks "can I get $X for trim Y?" — verify with 5 minutes of data before answering. Heuristic guesses about discount magnitudes are reliably wrong by $1,000-3,000.
- **New car path consideration**: If user is debating new vs used, pull current MSRP - actual asking price spread to compute opportunity cost honestly.

## Core Data Sources (Tier 1 — Most Reliable)

### CarEdge (caredge.com)

- **What**: Real dealer asking prices vs MSRP, showing dealer discount in dollars
- **URL pattern**: `caredge.com/shop-cars/new/{VIN}` for specific listing, or `caredge.com/{make}/{model}` for trim-level data
- **Best signal**: "Dealer Discount −$X,XXX" line item directly from dealer DMS
- **Use for**: Establishing "what dealers are advertising" baseline. If 5 dealers all advertise $1,200-$2,500 discount, that's the floor for negotiation.
- **Firecrawl query**: `"{year} {make} {model} {trim}" caredge.com`
- **Caveat**: Advertised discount is opening position; actual transaction often $500-1,500 lower. Use as lower bound, not target.

### Edmunds True Market Value (edmunds.com)

- **What**: National averages of "Buyers paying X% below MSRP, saving $X across most trims"
- **URL pattern**: `edmunds.com/{make}/{model}/{year}/`
- **Best signal**: The "buyers are paying X% below MSRP" headline (typically updated monthly)
- **Use for**: Setting expectation of national average discount. If Edmunds says 6.7% below MSRP, NJ aggressive dealers should be at 7-8% off.
- **Firecrawl query**: `"{year} {make} {model} prices reviews" site:edmunds.com`
- **Caveat**: National average — high-volume metros (NJ, CA, TX) often beat it; rural areas often miss it.

### TrueCar (truecar.com)

- **What**: Zip-code-aware "What Others Are Paying" with histogram of recent transactions
- **Use for**: ZIP-specific transaction data (e.g., a given ZIP shows median paid for trim X)
- **Firecrawl query**: `"{year} {make} {model} {trim}" site:truecar.com`
- **Caveat**: Sometimes shows MSRP-anchored numbers, not transaction-anchored. Cross-check with CarEdge.

### Specific Dealer Internet Pricing Pages

- **What**: Dealer DMS-pulled live inventory with discount math shown
- **Best dealers (in-state example)**:
  - <Dealer name> (suburb): aggressive on Internet Price
  - <In-state dealer A>: moderate, sometimes hidden ("Call Now")
  - <In-state dealer B>: aggressive with explicit dealer-specific discount
  - <In-state dealer D>: moderate
  - <In-state dealer E>: often hides ("Please Call")
  - <In-state dealer> (suburb): moderate
- **Use for**: Cross-bid anchors in counter-offers ("<In-state dealer> has same trim at $X internet price")
- **Firecrawl query pattern**: `"{year} {make} {model} {trim}" site:{dealer-domain}.com`
- **Caveat**: "Internet Price" sometimes excludes doc fee + tax + reg, sometimes includes manufacturer rebates assuming financing. Always verify components.

## Community Sources (Tier 2 — Real Buyer Reports)

### Reddit (r/SubaruForester, r/Subaru, r/cars, r/AskCarSales, r/CarPricing)

- **What**: Real buyer purchase reports with "MSRP $X, paid $Y, OTD $Z, state, dealer name"
- **Search pattern**: `site:reddit.com "{year} {make} {model} {trim}" OTD` or `site:reddit.com "{year} {make} {model}" discount`
- **Best signal**: Recent posts (within 30 days) with specific dollar amounts and dealer/state
- **Use for**: Actual transaction data points that don't appear in Edmunds/CarEdge averages
- **Caveat**: Cherry-picked best deals get upvoted. Average 3-5 reports across months to get a realistic median.

### Facebook Groups (Brand-specific + regional)

- **What**: "Subaru Forester Owners Group", "Subaru Forester Hybrid", "{state} Subaru Owners"
- **Use for**: Regional discount data (Midwest, NJ, CA) — Facebook has more state-level activity than Reddit
- **Firecrawl query**: `"{year} {make} {model} {trim} otd" site:facebook.com`
- **Caveat**: Most posts behind login; Firecrawl gets only snippets. Use snippets to confirm magnitudes, then user can dig deeper if needed.

### XiaoHongShu (小红书 / xiaohongshu.com)

- **What**: Chinese-speaking US buyers post regional purchase deals, especially active in NJ/NY/CA Asian community areas
- **Search**: Has its own search; Firecrawl can scrape individual post URLs but not search results
- **Use for**: When user references "I saw on XiaoHongShu someone got $X off" — verify by asking for the post URL or trim/region/dealer details
- **Caveat**: Heavy bias toward best-case posts; many include incentive stacks (loyalty conquest cash + recent grad + military) that don't transfer to all buyers. Always ask "what trim, what region, what month, did they trade in another car?"

### Spanish-Language (ES) Buyer Communities — US Hispanic / Latino market

> **Verified 2026-06-22 via web_search.** This is the ES analog of the XHS tier: where Spanish-speaking US buyers exchange car info. **Hard rule (anti-hallucination): only the sources below were confirmed to exist with a real resolving URL. Do NOT add any ES source you have not just re-verified via web_search — a fabricated community is worse than none.** Re-verify reachability before each engagement; FB group IDs and subreddit activity drift.
>
> **Reality check vs XHS**: the ES tier is materially *weaker* for dealer-quote evidence than XHS. Two structural reasons: (1) Spanish-language Reddit is **fragmented** (per Sherlock Comms LATAM analysis — Brazil/Portuguese has the dense activity; Spanish is spread thin and country-split), and most large ES subs (r/mexico, r/espanol) are **MX/LATAM-domestic**, where prices/taxes/incentives do NOT transfer to US OTD math. (2) The US-Latino Facebook groups are **private-seller buy/sell marketplaces** (FSBO listings), not a dealer-worksheet-screenshot posting culture like XHS. Treat ES as a *thin supplementary* anchor for Spanish-dominant buyers, never as a primary OTD-evidence source. Cross-check every datapoint against the English Reddit + aggregator tiers.

**Reachability legend**: `OPEN` = readable without login (subreddits, public web). `LOGIN` = Facebook account + group-join approval required (use Playwright local browser, same workflow as FB groups above).

#### Reddit (ES) — OPEN, but mostly LATAM-domestic pricing

| Subreddit | URL | What it is | Reachability | Deal-evidence value |
|---|---|---|---|---|
| **r/mexico** | `reddit.com/r/mexico` | Largest active Spanish hub on Reddit (MX ~15.7M Reddit users; confirmed primary ES discussion space). Car-buying threads appear but pricing is **MX-domestic** (pesos, tenencia, MX dealers). | OPEN | LOW for US OTD — wrong-market prices. Useful only for general buying-process / scam-avoidance discussion. |
| **r/espanol** | `reddit.com/r/espanol` | General Spanish-language catch-all; occasional car-advice threads. Fragmented, low car-specific density. | OPEN | LOW — thin, no consistent US dealer quotes. |
| **r/AskLatinAmerica** | `reddit.com/r/asklatinamerica` | Q&A across LATAM + diaspora; can field "buying a car in the US" questions from Spanish speakers. | OPEN | LOW-MED — ask-and-answer, not posted quote screenshots. |
| **r/carros**, **r/mecanica** | `reddit.com/r/carros`, `reddit.com/r/mecanica` | General ES cars / mechanics subs. Mecanica is repair-focused (useful for used-car condition vetting), not pricing. | OPEN | LOW for pricing; mecanica MED for used-car inspection questions. |

Use the same Reddit extraction path as the English tier (browser session / `firecrawl search "site:reddit.com ..."`). Query in Spanish: `comprar carro usado concesionario precio OTD`, `cuánto pagaste por`, `me dieron de descuento`.

#### Facebook (ES) US-Latino buy/sell groups — LOGIN required

All groups below returned a **real resolving group URL** on 2026-06-22. They are FSBO/marketplace groups (private-seller listings + asking prices), NOT dealer-worksheet culture — value is as a *regional private-party price floor*, not dealer-discount evidence. Member counts are no longer publicly shown by FB, so "active" cannot be asserted from search alone — **open in Playwright and check the most-recent-post date before citing.**

| Group | URL | Region | Reachability |
|---|---|---|---|
| COMPRA Y VENTA DE AUTOS EN VIRGINIA #LATINOS | `facebook.com/groups/706490468073515` | VA | LOGIN + join |
| COMPRA Y VENTA DE AUTOS HOUSTON TX | `facebook.com/groups/186744047475623` | Houston TX | LOGIN + join |
| CARROS CASH HOUSTON TX Y SUS ALREDEDORES | `facebook.com/groups/237983615635519` | Houston TX | LOGIN + join |
| Compra y venta de Carros usados Los Angeles | `facebook.com/groups/219715817773528` | LA CA | LOGIN + join |
| VENTAS de autos nuevos y USADOS (Los Angeles) | `facebook.com/groups/711862078920360` | LA CA | LOGIN + join |
| Compra-Venta de Autos en California | `facebook.com/groups/568277525205205` | CA (statewide) | LOGIN + join |

Search inside a joined group in Spanish for a target model (`Honda CR-V`, `precio`, `OTD`, `descuento`). FB workflow = same Playwright local-browser login path as the brand FB groups described above.

#### REJECTED (NOT communities — do not list as deal sources)

These surfaced under "latino car" searches but are **dealer storefronts / lead-gen / content sites, not peer buyer communities** — they post their own asking prices, not independent buyer quote evidence. Listing them as community sources would be a category error:

- `autoslatinos.com`, `carrosenusa.com` — online used-car dealers / lead-gen.
- Facebook **Pages** (not groups): "Auto Latinos" (LA), "Autos Latinos" (Hollywood FL), "Latinos Unidos Auto Sales" (Houston) — dealer business pages.
- `autonationusa.com/espanol`, `franco automotors`, `latinocerca.com` — dealer chain / dealer directory.
- LATAM-domestic FB groups (Buenos Aires, Lima Perú, CDMX) — **wrong market**, non-US pricing.

If a new "latino autos" result appears, classify it first: a **group** where many buyers post = candidate community (verify + add); a **page/site** selling cars = dealer, reject.

### Instagram & TikTok Dealer Posts

- **What**: Dealer-posted lease ads reveal manufacturer lease cash structure (e.g., "$349/mo 36mo $2,500 down" implies ~$3,000-4,000 lease cash baked in)
- **Use for**: Lease cash can sometimes be converted to cash buyer discount via the "lease then immediately buy out" trick (works when lease cash > residual gap math)
- **Firecrawl query**: `"{year} {make} {model} hybrid lease" site:instagram.com`
- **Caveat**: Lease cash conversion requires careful math + dealer cooperation; not always feasible.

### YouTube Pricing Channels

- **CarEdge YouTube**: Monthly deal report videos
- **YAA (Your Auto Advocate)**: Industry-insider analysis of incentive structures
- **Lucky Lopez**: Dealer-perspective discount commentary
- **Use for**: Macro deal-flow trends ("December incentives doubled vs November") that explain why a specific car is or isn't moving on price
- **Firecrawl query**: Video transcripts not directly scrapeable via Firecrawl; use YouTube native search and watch directly.

## Manufacturer & Industry Sources (Tier 3 — Background)

### Kelley Blue Book Fair Market Range (kbb.com)

- **What**: MSRP, "Fair Purchase Price" (KBB-computed regional fair price), trade-in value
- **Use for**: Understanding what's "fair" vs "great" before negotiating
- **Caveat**: KBB Fair Purchase Price is conservative; actual aggressive deals beat it by $500-2,000.

### CarsDirect (carsdirect.com)

- **What**: Detailed incentive stack reports — manufacturer cash + dealer cash + finance cash + lease cash + loyalty/conquest/military/recent grad
- **Use for**: Understanding what the manufacturer is paying the dealer this month — directly affects how much room dealer has to discount
- **Firecrawl query**: `"{year} {make} {model} incentives" site:carsdirect.com`
- **Best signal**: "Manufacturer to Dealer Cash" line — this is invisible margin the dealer can give up

### Subaru of America (subaru.com)

- **What**: Official MSRP, current incentive offers (lease specials, APR cash, college grad, loyalty)
- **URL pattern**: `subaru.com/deals` or `subaru.com/{model}/build`
- **Use for**: Verifying which incentives the buyer qualifies for + current month's APR cash
- **Caveat**: Manufacturer site shows public-facing offers only; dealer-only programs (regional MSDP, dealer cash) not listed here.

## Source-Specific Extraction Patterns (verified)

After scraping each source, use these specific grep patterns to extract the high-value data quickly:

```bash
# CarEdge - dealer discount math
grep -oiE '(msrp|dealer discount|asking price|doc fee)[^"]{0,100}' caredge.json

# In-state dealer Internet Pricing
grep -oiE '(SAVINGS|Internet Price|MSRP)[^"]{0,80}' dealer.json

# KBB - Fair Purchase Price + MSRP range
grep -oiE '(MSRP|Fair Purchase|starting at)[^"]{0,100}' kbb.md

# Subaru.com - official offers
grep -oiE '(Special Offers|APR FINANCING|Customer Cash|Lease)[^"]{0,80}' subaru-com.md

# CarGurus - deal ratings (only on ZIP-filtered URL)
grep -oiE '(Great Deal|Good Deal|Fair Price|Overpriced)[^"]{0,40}' cargurus-zip.md

# Edmunds via Wayback - savings narrative
grep -oiE '(buyers paying|below msrp|savings of|fair price|true market value)[^"]{0,150}' edmunds-wayback.md

# Reddit search snippets - buyer-reported OTD
python -c "import json; d=json.load(open('reddit-search.json'));
[print('-',w['title'][:80],'\n  ',w['description'][:200]) for w in d['data']['web']]"
```

Real-world output sample (Reddit Google search for 2026 Forester Hybrid):
```
- Quoted $35573 out the door price for a 2026 Subaru Forester...
  1st dealer - $37378 otd 2nd dealer - $36150 otd 3rd dealer - $35573 otd
- 2026 forester touring NY/NJ/PA
  They would not budge any further but took 0.9% financing and no extended warranty.
  So you might be able to get it for about $39k OTD.
- Would you pay $35800+tax for a 2026 Hybrid Limited?
  That's about right to me. I paid $31,800 for a hybrid premium with some small add-ons
  before taxes and fees.
```

Reddit search snippets carry the EXACT data we need (state, trim, dealer count, OTD figures). Direct page scrape isn't needed.

## Firecrawl Query Recipes (Verified Working)

The 5-query pipeline below has been verified to recover the data needed for OTD baseline + buyer reports + incentive stack + dealer-specific Internet Price + manufacturer official MSRP. Run in parallel via background `&`.

```bash
mkdir -p .firecrawl

# 1. National baseline + dealer discount range (CarEdge + others surface here)
firecrawl search "{year} {make} {model} {trim} discount deal {year} invoice MSRP" \
  --limit 8 --tbs qdr:m \
  -o ".firecrawl/{model}-discount-search.json" --json &

# 2. State-specific dealer pricing (each NJ/NY/PA dealer's Internet Pricing surfaces)
firecrawl search "{year} {make} {model} {trim} {state} dealer price out the door" \
  --limit 8 \
  -o ".firecrawl/{model}-{state}-search.json" --json &

# 3. Recent buyer reports (Reddit content reaches via search, direct scrape blocked)
firecrawl search "site:reddit.com {year} {make} {model} {trim} OTD paid" \
  --limit 10 --tbs qdr:m \
  -o ".firecrawl/{model}-reddit-reports.json" --json &

# 4. Manufacturer incentive stack
firecrawl search "{year} {make} {model} incentives rebate {month} {year}" \
  --limit 5 --tbs qdr:m \
  -o ".firecrawl/{model}-incentives.json" --json &

# 5. Official MSRP from manufacturer site (verified working)
firecrawl scrape "https://www.subaru.com/vehicles/{model}/index.html" \
  --format markdown \
  -o ".firecrawl/{model}-official.md" &

wait
```

For each top-N candidate dealer, also pull their specific listing page (verified working on multiple in-state dealer sites):

```bash
# Dealer listing pulls Internet Price + Savings + sometimes incentive details
firecrawl scrape "{dealer-website}/{vehicle-listing-url}" --format markdown \
  -o ".firecrawl/{dealer}-{vin}-listing.md"

# Image-heavy dealer specials/banners require screenshot
firecrawl scrape "{dealer-website}/specials" --format markdown,screenshot \
  -o ".firecrawl/{dealer}-specials.json"
```

For Edmunds-specific average-paid data (blocked direct):

```bash
# Edmunds via Wayback Machine (verified working bypass)
firecrawl scrape "https://web.archive.org/web/2026/https://www.edmunds.com/{make}/{model}/" \
  --format markdown \
  -o ".firecrawl/{model}-edmunds-wayback.md"
```

For KBB Fair Purchase Price:

```bash
firecrawl scrape "https://www.kbb.com/{make}/{model}/{year}/" --format markdown \
  -o ".firecrawl/{model}-kbb.md"
```

For CarGurus deal ratings (must use ZIP-filtered URL):

```bash
firecrawl scrape "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?entitySelectingHelper.selectedEntity={cargurus-model-id}&zip={ZIP}" \
  --format markdown \
  -o ".firecrawl/{model}-cargurus-zip.md"
```

### Anti-Pattern: Sources That Look Useful But Don't Work via Firecrawl `scrape` API

Do NOT use direct `firecrawl scrape` on these — but **most have working browser-session workarounds**:

| Source | scrape API status | Browser session status |
|---|---|---|
| Reddit | ❌ "Site not supported" | ✅ Works (no login needed for public posts) |
| Facebook | ❌ "Site not supported" | ✅ Works (login via Live View required) |
| Instagram | ❌ "Site not supported" | ✅ Works (login via Live View required) |
| XiaoHongShu | ❌ Login wall | ✅ Works (login via Live View required) |
| TrueCar | ❌ JS client-side error | ⚠ Try browser session — likely works |
| Edmunds | ❌ Akamai 403 | ⚠ Try browser session OR Wayback Machine |
| Google search direct | ❌ CAPTCHA | Use `firecrawl search` (different backend) |

**Sequence to try when a source fails**:
1. `firecrawl scrape <url> --format markdown` — fastest, most sources work
2. If "Site not supported" → `firecrawl browser launch-session --profile <name>` + `firecrawl browser "open <url>"` + `firecrawl browser 'get text body'`
3. If browser session shows login wall → share Live View URL with buyer, after login same workflow works + cookies persist in profile
4. If still blocked → Wayback Machine (`web.archive.org/web/{year}/{url}`)
5. If all else fails → ask buyer to screenshot and paste text content

The browser-session workflow handles ~95% of previously-"blocked" sources. The 5% that genuinely fail (rare) usually have aggressive CAPTCHA + IP-binding (e.g., banking sites, some adult sites — irrelevant for car research).

## Data Synthesis Worksheet

After pulling 4-6 sources, synthesize into a one-page baseline table. Save as `.firecrawl/{model}-deal-baseline.md`.

### Provenance column (mandatory)

Every evidence row in the worksheet MUST carry a `provenance` field with exactly one of two values:

- **`REAL`** — sourced from an actual scrape/snippet/screenshot. Row must include the source URL and a `pulled-at` timestamp (ISO `YYYY-MM-DD HH:MM` local). Only REAL rows are quotable in Phase 4 dealer emails (see SKILL.md Critical Rule #7).
- **`SYNTHESIZED`** — placeholder, interpolation, "typical for this make/state", or any row reconstructed from memory / averages / heuristics. Row must include a `reasoning` note explaining how the value was estimated. SYNTHESIZED rows are for internal reasoning only — never paste into a dealer email.

Example pair (one of each):

| Source | Trim | Price | Provenance | URL / Reasoning | Pulled-at |
|---|---|---|---|---|---|
| <Dealer A> in registering state | Premium Hybrid | $<internet-price> | REAL | <dealer-pricing-URL> | YYYY-MM-DD HH:MM |
| (estimate) typical state markup | Premium Hybrid | ~$<estimate> | SYNTHESIZED | Edmunds national avg -X% × MSRP $<msrp>; no state-specific listing pulled this run | n/a |

Mixing the two in a single roll-up is fine for internal math; surfacing the SYNTHESIZED row externally is not.

### Worksheet template

```markdown
# {Year} {Make} {Model} {Trim} - Deal Baseline (as of YYYY-MM-DD)

## MSRP Range (across configurations)
- Base trim: $X,XXX  [provenance: REAL | SYNTHESIZED]
- With common options (color premium, etc.): $Y,YYY  [provenance: ...]
- Loaded: $Z,ZZZ  [provenance: ...]

## National Average Discount (Edmunds + CarEdge)
- Edmunds: X% below MSRP, ~$X,XXX off  [provenance: REAL, url, pulled-at]
- CarEdge: median asking $X,XXX off MSRP across N listings  [provenance: REAL, url, pulled-at]

## Regional Dealer Internet Pricing ({state})
| Dealer | Trim | MSRP | Internet Price | Discount | Provenance | Source URL | Pulled-at |
|---|---|---|---|---|---|---|---|
| Dealer A | X | $X | $Y | -$Z | REAL | url | YYYY-MM-DD HH:MM |
| Dealer B (estimate) | X | $X | $Y | -$Z | SYNTHESIZED | reasoning: ... | n/a |
| ... | | | | | | | |

## Real Buyer Reports (Reddit + Facebook past 30 days)
- {state-1}: MSRP $X paid $Y OTD $Z  [provenance: REAL, reddit URL, pulled-at]
- {state-2}: ...  [provenance: SYNTHESIZED, reasoning: extrapolated from {state-1}; do not cite]

## Manufacturer Incentives (current month)
- Lease cash: $X  [provenance: REAL | SYNTHESIZED]
- APR cash: $Y  [provenance: ...]
- Loyalty / Conquest: $Z (if buyer trades in qualifying vehicle)  [provenance: ...]
- Other (military, recent grad, college): $W  [provenance: ...]

## Realistic OTD Targets ({state}, your buyer profile)
- Stretch (95th percentile aggressive): $X
- Realistic (60th percentile): $Y
- Walk-away if dealer can't beat: $Z

(Targets are derived from the rows above; mark which inputs were REAL vs SYNTHESIZED so Phase 4 knows which numbers may be cited externally.)
```

## Common Mistakes To Avoid

1. **Confusing trim levels across model lines.** "2026 Forester Premium" gas trim ($32-33k MSRP) vs "2026 Forester Premium Hybrid" ($34-35k MSRP) are $2,500-3,500 apart. A discount applied to one does NOT apply to the other.

2. **Confusing model year transitions.** When two MYs overlap (e.g., late 2025 has both 2025 and 2026 in inventory), discounts on outgoing MY are 2-3x larger than incoming MY. Check the build date / production date, not just nameplate year.

3. **Confusing financing-conditional discounts with cash-buyer discounts.** Many advertised discounts assume buyer takes manufacturer's APR cash (must finance through SubaruMotorsFinance + may have early-payoff penalty). Cash buyers may not qualify — explicitly ask "is this discount cash-eligible or finance-only?"

4. **Trusting single-source data.** One Reddit post showing $5,000 off doesn't mean $5,000 off is achievable for your buyer. Cross-reference 3+ independent sources before quoting a discount target.

5. **Ignoring regional pricing zones.** Subaru pricing zones (1A NJ/NY/CT, 2 PA/MD, etc.) have different MSRP, different dealer holdback, different regional MSDP. Cross-state shopping (PA dealer to NJ buyer) involves real tax/title complexity that may eat half the savings.

6. **Trusting heuristic ranges from prior knowledge.** Used vehicle pricing changes month-to-month (sometimes week-to-week as quarterly incentives reset). Pull fresh data every time, especially when the user pushes back on a quoted estimate.

7. **Confusing advertised "Internet Price" with OTD.** Internet Price almost never includes tax + doc + reg + add-ons. Always project to OTD using state's tax rate + actual doc fee + reg estimate before comparing across dealers.

## Worked Example (2026 Subaru Forester Hybrid, in-state)

User asked: "Can I get a 2026 Forester Premium Hybrid at $35k OTD?"

**Initial heuristic estimate (BAD)**: "Premium Hybrid MSRP ~$36,500, launch year discount $500-1,500, so OTD $38,000-39,000. $35k unlikely."

**After pulling real data via Firecrawl**:

| Source | Data point |
|---|---|
| Reddit r/SubaruForester | "2026 Forester Hybrid prices decreased by up to $1,985" — Subaru NA pulled MSRP back |
| Edmunds | National avg 6.7% below MSRP, ~$2,483 off |
| Facebook Subaru Forester Group | Midwest 2025 Hybrid Premium MSRP $38,994, paid -$4,500 |
| CarEdge | 2026 Forester Premium gas MSRP $35,492 → asking $34,262 (-$1,230) |
| <In-state dealer A> | 2026 Premium Hybrid Internet Price ~$34,000 (advertised -fee bundle off) |
| <In-state dealer B> | 2026 Premium gas: -$2,250 advertised discount |
| Lease ad | $349/mo, 36mo, $2,500 down → $3-4k lease cash baked in |

**Corrected estimate**:
- Realistic NJ floor for Premium Hybrid: MSRP ~$35,400 - $4,000-4,500 aggressive discount = $30,900-31,400 sell
- + NJ tax/doc/reg ~$3,400
- = **OTD $34,300-34,800** ← actually achievable, just needs hard 5-6 dealer cross-bid

**Lesson**: The data-backed answer was $3,000-4,000 different from the heuristic answer, in the direction that mattered to the buyer's decision.

## Integration with Other Skill Phases

- **Phase 1 (Requirements)**: After collecting buyer requirements, run baseline data pull immediately. Use baseline to set realistic OTD target before user commits emotionally to a number.
- **Phase 3 (Mass outreach)**: Inject baseline data into first-touch email — "I'm seeing comparable trims listed at $X-$Y across NJ dealers; my OTD target for this VIN is $Z."
- **Phase 5 (Negotiation)**: Each cross-bid counter cites a specific competitor's advertised Internet Price (with URL on file in `.firecrawl/`).
- **Phase 7 (Dossier)**: The dossier's "Regional Market Average" section should be backed by 5+ sources from this pipeline.

## When To Re-Pull Data

- Start of every new buyer engagement (data goes stale fast)
- When transitioning from used to new car path (different sources, different incentive stack)
- When user references a deal they saw elsewhere ("XiaoHongShu / Reddit / friend got $X off") — verify directly within 5 minutes
- Monthly during slow buying cycles (incentives reset around 1st of each month)
- When dealer pushes back on a counter ("we can't go lower because market is tight") — re-pull regional data to verify or call the bluff
