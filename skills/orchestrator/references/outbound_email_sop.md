# Outbound email SOP, composition and attachments

> Moved out of SKILL.md under PHILOSOPHY P7: this is a procedure needed only in Phase 4 and on
> each counter, not on every run. SKILL.md keeps the pre-draft gate and the length limits, which
> are the checkable rules.

This is the ordered procedure for any dealer outreach, first-touch, counter, or follow-up. Following the order prevents the most common failure modes (draft accumulation, illegible inline images, mixed anchors).

### Step 0: Gather requirements ONCE before opening a draft

Ask in a single message (not piecemeal):

- Exact trim / option package (e.g., "Premium with Option Package 15", not "Premium Hybrid or Premium gas")
- Payment method with detail (card name + monthly cashback cap if CC, see `references/payment_methods.md`)
- Attachment plan: which screenshots, manual or inline (default: manual)
- Used-car vs new-car context: which thread is this? Do NOT mix in counters.
- Deadline / close date for inclusion in walk-away line

If buyer answers vaguely, ask follow-ups before drafting. Drafting before this is locked = inevitable iteration = clutter (see E4).

**Email-type branching (pick ONE before drafting).** First-touch / counter / follow-up have different shapes; lumping them is the root of most line-count and citation errors.

| Type | Line count | Body skeleton |
|---|---|---|
| First-touch | 15-20 lines | Greeting + buyer profile (1-2 lines: city/state, cash-or-financing, close-window) + vehicle ID + 5-line OTD breakdown ask + walk-away line + sign-off |
| Counter | ~10 lines (E3 hard cap) | Greeting + 3 numbered asks + 1 anchor sentence + 1 walk-away line + sign-off. NO buyer-profile recap (dealer already has it). |
| Follow-up / nudge | 4-6 lines | Greeting + reference to prior thread + 1 specific ask (e.g., "any update on the OTD?") + deadline + sign-off |

**Pre-draft mandatory Y/N checklist (5 items).** Run this BEFORE the first `create_draft` call in any session. If ANY item answers N, STOP and ask the buyer. Do not draft.

| # | Gate | What "Y" looks like |
|---|---|---|
| 1 | Trim + option package locked? | "Forester Limited with Option Package 25", not "Limited or Touring" |
| 2 | Payment method locked? | "3% cashback Visa, $50k monthly cap", not "cash or card" |
| 3 | Attachments planned? | "_FINAL_xhs-25500.jpg + _FINAL_cargurus-good-deal.jpg, manual paperclip", not "some screenshots" |
| 4 | Anchor strategy + new-vs-used context locked? | "Cross-dealer anchor citing Rep A $X,XXX / Rep B $X,XXX; NEW MY thread, no used candidates referenced", not "I'll cite something" |
| 5 | Walk-away deadline + dollar amount confirmed? | "$30,500 OTD walk-away, close by Wed May 22", not "close this week" |

If any gate is N, the correct action is a single clarifying message back to the buyer, NOT a "best guess and iterate" draft. Iteration with `create_draft` only creates new drafts (no edit mode); 4 dealers × 3 rounds = 12 stale drafts the buyer must manually trash (see E4).

### Step 1: Prepare attachment files at FULL resolution (no MCP)

In the working directory:

```bash
mkdir -p .firecrawl/quote-images/
```

For each evidence image (XHS post screenshot, Reddit quote, dealer worksheet):

```python
from PIL import Image
img = Image.open('source.png')
if img.size[0] > 1300:
    h = int(img.size[1] * 1300 / img.size[0])
    img = img.resize((1300, h), Image.LANCZOS)
if img.mode == 'RGBA': img = img.convert('RGB')
img.save('_FINAL_<dealer>-<trim>-<datapoint>.jpg', 'JPEG', quality=88, optimize=True)
```

Target: 100-300KB JPGs at 1080-1300px width, fully legible. Use `_FINAL_` prefix so the user can find them at a glance.

### Step 2: Compose drafts via MCP with NO attachments field

```python
create_draft(
    to=[...],
    subject=...,
    body=...,  # plain ASCII, ~15 lines first-touch / ~10 lines counter
    # NO attachments key
)
```

In the body, reference attachments by name: "Screenshots attached." Do not include URLs or markdown link syntax.

If buyer asks to "insert" or "attach" images, push back ONCE:

> "Per E5: manual paperclip is the only way to send legible attachments. The MCP inline path forces ~16KB images that arrive blurry. I'll prepare the files at full resolution and you paperclip them in Gmail UI. Sound good?"

Default to manual. Only inline if buyer explicitly overrides.

### Step 3: Hand off to buyer with a per-draft attachment recipe

In the summary to buyer, output a table like:

| Dealer | Draft ID | Files to paperclip | Why |
|---|---|---|---|
| Dealer A | `r-xxxx` | `_FINAL_A.jpg`, `_FINAL_B.jpg` | NJ benchmark + ceiling reference |
| Dealer B | `r-yyyy` | `_FINAL_A.jpg`, `_FINAL_B.jpg` | Same; skip Dealer B's own ad |
| ... | ... | ... | ... |

Tell buyer: "Open each draft in Gmail web UI → paperclip → folder path → select listed files → leave as draft → I will tell you when to send."

### Step 4: Verify before send (buyer-side checks)

Buyer's pre-send checklist:
- ASCII body (no `**bold**`, no em-dashes)
- Attachments named clearly
- Subject line matches across all 4 emails in the cross-bid
- Walk-away deadline date is correct (especially after time has passed since drafting)
- Used-car / new-car threads not mixed

### Step 4.5: Mid-cycle pivot protocol (when a load-bearing field changes)

If the buyer changes a load-bearing field AFTER drafts have been created (trim, payment method, walk-away ceiling, anchor strategy, used-vs-new context, deadline), do NOT layer 4 new drafts on top of the 4 stale ones. Run this 4-step protocol:

1. **STOP drafting immediately.** No new `create_draft` calls until the protocol completes.
2. **Surface the stale drafts to the buyer with a bulk-delete Gmail search string** (per E4). Example: `in:drafts subject:"2024 Forester Limited" before:2026/05/18 -subject:"final batch"` selects the exact stale set. Tell the buyer: "These 4 drafts are now stale because trim/payment/X changed. Open Gmail web UI, paste this search, Select All, Move to Trash, then I'll create the new batch."
3. **Re-run Step 0** in full (gather + 5-item Y/N gate + email-type pick). The load-bearing change may cascade (e.g., trim change → anchor strategy needs re-lock; payment change → walk-away ceiling math shifts).
4. **Resume from Step 1** (full-res attachments may need regen if the screenshot set changed) → Step 2 (new drafts) → Step 3 → Step 4 → Step 5.

Never assume "the buyer will sort the stale drafts themselves." MCP Gmail cannot delete drafts. Without the bulk-delete search string, stale Premium drafts and new Limited drafts coexist in the Drafts folder and the buyer's risk of accidentally sending a stale one is real.

### Step 5: Send all 4 in a single 5-minute window

Cross-bids work because dealers feel parallel pressure. Sending them an hour apart loses leverage. Buyer hits Send on all 4 within 5 minutes.

**Send-window advisory (dealer-local time).** Recommend send between **9 AM and 5 PM Mon-Thu dealer-local time**. Reasoning:

| Window | Reply timing | Recommendation |
|---|---|---|
| Mon-Thu 9 AM - 12 PM | Same-day reply most likely; sales desk fresh | BEST |
| Mon-Thu 12 PM - 5 PM | Same-day or next-morning reply | GOOD |
| Mon-Thu 5 PM - 9 AM (overnight) | Lands at bottom of next-day inbox; rep replies in inbox-surface order | AVOID, lose first-mover edge on cross-bid |
| Friday after 12 PM | Lands in weekend autoresponder bucket; Mon reply | AVOID, 3-day reply lag |
| Sat - Sun | Read Monday morning behind weekend backlog | AVOID |
| 11 PM-7 AM dealer-local | Lands at bottom of inbox; rep treats as low-priority | AVOID |

If buyer asks to send outside the recommended window, push back ONCE with reasoning: *"Send at [time] will land at bottom of [day]'s inbox, sales rep works through inbox top-down, so we lose first-mover edge on the parallel cross-bid. Recommend hold until [next 9-10 AM dealer-local slot]."* Then comply if buyer overrides. The advisory is guidance, not a hard block, but the buyer should know the trade-off before sending.

Multi-state cross-bid: use the EARLIEST dealer-local 9 AM among the 4 dealers as the cohort send time (e.g., NJ + NY + CT + PA → all Eastern, 9 AM ET works; if MI dealer added, 9 AM ET = 8 AM CT, wait until 9 AM CT so the MI dealer also sees it in morning prime).

### Step 6: Cron monitoring kicks in

After send, the cron job (Phase 5) picks up replies. See `references/cron_monitoring.md`.

### Common deviations and corrections

| Deviation | Correction |
|---|---|
| Buyer says "just attach images for me" | Push back once (Step 2). Only inline if overridden. |
| Drafts created before trim is finalized | Stop. Re-ask Step 0. Don't iterate. |
| New car email cites used car offer | Discard draft, recompose without used anchor (gotcha D5). |
| Image looks tiny in draft preview | Confirm: was it inlined via MCP? If yes, regenerate at full res + manual attach. |
| 12+ stale drafts in Gmail Drafts folder | Give buyer one search string for bulk delete (gotcha E4). |

