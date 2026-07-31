# Gotchas, grouped by topic

> Moved out of SKILL.md under PHILOSOPHY P7: this section describes itself as explaining where
> the Critical Rules came from, which makes it a reference by definition. SKILL.md keeps the ID
> index; the incidents live here. Every gotcha is cited by ID from the phase summaries and from
> other references, so those citations resolve to this file unchanged.

Each gotcha is rooted in a real past incident. Use the topic groupings to find what's relevant. Where a workflow phase obviously triggers a gotcha, the gotcha is also referenced inline in the phase.

### E. Email & Drafting Hygiene

**E1. Plain ASCII required in every draft.** Dealers see literal `**bold**` and `—` characters that did not render. Strip markdown markers, em-dashes, en-dashes, backticks, and link syntax before saving any draft. See `references/email_format_rules.md`.

**E2. Empty `plaintextBody` on HTML-only emails hides inline OTD data.** Many dealer CRM platforms send HTML-only. Snippet truncates at ~200 chars, sometimes mid-sentence before the actual numbers. When `plaintextBody` is empty, alert the buyer that data may exist past the snippet boundary and ask them to verify in Gmail directly.

**E3. Keep dealer replies tight, ~10 content lines max.** Sales reps skim. Skeleton: 3 numbered asks + 1 anchor sentence + 1 walk-away line + sign-off. Cut without mercy: dealer knows their own car, can compute tax themselves, buyer profile only needs full restatement on first-touch. First-touch can be 15-20 lines; all subsequent counters compress to ~10.

**E4. MCP Gmail integration is read+create scope only, cannot edit, delete, or relabel anything.** `create_draft` makes a NEW draft on every call (no update mode). Both `label_message` and `label_thread` exist as tool surfaces but return "insufficient authentication scopes" when invoked, so even "add TRASH label" doesn't work. Iterating 3 rounds × 4 dealers creates 12 stale drafts that ONLY the user can manually trash via Gmail web UI. Protocol: ask 2-3 clarifying questions upfront (trim, payment method, attachments, what to include/exclude) BEFORE first draft. If iteration is unavoidable, give the user one Gmail search string that selects exactly the stale set for bulk delete (e.g., `in:drafts subject:Forester before:YYYY/MM/DD -subject:"final batch marker"`).

**E5. NEVER inline image attachments via MCP `create_draft`, the constraint chain forces 16-20KB tiny images that dealers can't read.** Why this is a hard rule, not a preference:
- MCP schema requires `attachments[].content` as inline base64 string.
- To pass base64 to MCP, must first Read it into context.
- Read tool has 25K-token output cap.
- Max base64 = ~25KB chars → max raw image ≈ 18-20KB.
- 18KB JPEG = ~360x400 px, dealer sees a blurry illegible square instead of a quote.
- Iterating to fit triggers 4-5 progressively smaller compressions, burning ~100K tokens on dead-end base64 reads.

**Correct workflow ALWAYS**:
1. Compose drafts via `create_draft` with NO `attachments` field.
2. Generate full-res JPGs (1080-1300px wide, quality 85-90, 100-300KB each) in `<workdir>/.firecrawl/quote-images/` with `_FINAL_` filename prefix.
3. List the exact files + per-dealer recommendation in a summary message.
4. User opens each draft in Gmail web UI → paperclip → selects files from local folder → saves → sends.

If the buyer asks to "insert images" or "attach screenshots", do NOT interpret as a request to inline via MCP. Push back once: "Per E5 the right play is high-res files + manual paperclip. The MCP inline path produces tiny unreadable images. Confirm you want manual attach (recommended) or the inline-tiny path." Default to manual unless explicitly overridden.

Per-dealer attachment etiquette:
- NEVER attach a dealer's own Internet Pricing screenshot back to them (shows you shop their own ad → kills negotiation).
- Safe to attach 3rd-party aggregator screenshots (CarGurus, Cars.com, Edmunds) to anyone.
- Safe to attach Competitor Dealer Y's quote to Dealer X (the "your competitor advertised this" play).
- Same attachment set across all 4 dealers in a parallel cross-bid is the simplest and works fine.

### I. Inbox & Cron Monitoring

**I1. Carfax submissions look successful but dealers often delay 12+ hours.** Schedule cron monitoring at 15-min intervals starting the morning AFTER submission, not within minutes.

**I2. Dealer email lands in Promotions AND occasionally Spam.** Search must be tab-agnostic or include `category:promotions`. Run a separate `in:spam` sweep at least once per buying-cycle day (eDealerHub / VinSolutions CRM platforms get spam-flagged often).

**I3. `newer_than:25m` sliding window misses backlog during pauses.** Overnight / meeting gaps make dealer mail permanently invisible to subsequent runs. Run one `newer_than:3d is:unread` full sweep per buying-cycle day.

**I4. Templated CRM emails are not always skippable.** A CRM email that embeds specific inventory data (stock, VIN, sales price, miles, color) IS actionable, even if the wrapper is boilerplate. Test: "does it contain vehicle-specific data?" not "does it look like a template?". Skip only pure marketing taglines.

**I5. Do not trash the dealer's original email or sent replies, it breaks future thread anchors.** When cleaning drafts, only delete items in `DRAFT` label state; never trash items with `INBOX` or `SENT` labels. Recovery if accidentally trashed: send a fresh email with `Re: <original subject> - <small qualifier>` so it threads in dealer's inbox.

### D. Dealer Behavior & Communication

**D1. "Best price upfront" dealers will not negotiate.** Recognize quickly (rental-return chains like Enterprise, no-haggle independents, some volume Subaru stores at MSRP) and pivot rather than waste cycles.

**D2. The 72-hour urgency claim is sometimes real, sometimes pressure.** Confirm by asking about the hold/deposit mechanism.

**D3. Local relationship dealers (Chinese, family, community) value direct over aggressive.** Do not deploy multi-round anchor tactics; one fair counter is enough.

**D4. Verify dealer hours and rep availability before scheduling.** A Wednesday test drive with a rep who is off Wednesday wastes everyone's time.

**D5. NEVER mention competing USED car offers when inquiring NEW car pricing (and vice versa).** Used and new desks have different incentive structures; mixing closes off negotiation ("if you have used at $32k, just buy that, we cannot match"). Keep negotiations completely separate.

**D6. When asking for multiple trim quotes, specify ONE "preferred" + ONE "alternative".** Lumping 4 trims yields generic "starting from $X" pitches. The 1+1 pattern yields two real labeled quotes.

**D7. Dealer-attached `proposal.pdf` hides actual OTD numbers from Claude.** Ask the user to open the PDF, OR ask the dealer to paste the OTD breakdown inline in the email body for "side-by-side comparison". Many dealers happily comply.

**D8. Dealer state-fee-template leak = full re-quote leverage, not single-line tweak.** When a dealer quote contains a fee that does not exist in the buyer's REGISTERING state, treat it as evidence that the entire OTD was generated from an out-of-state CRM template. Cross-check the rest of the line items against the registering state's "Does NOT have" list in `references/state_fees.md`. The correct response is to demand a full re-quote ("please re-issue the OTD using CT line items"), not just deletion of the leaking line. Other defaults in the same template, wrong reg fee structure, wrong tax rate tier, wrong title fee, are likely also wrong but harder to spot once the obvious leak is patched.
Example from the CT Outback case: dealer quote on a CT registration carried an NJ $7.50 tire fee (5 tires × $1.50 NJ rate). CT has no per-tire fee on retail dealer sales. The leak also coincided with an under-collected CT 2-year reg ($80 vs ~$120), second template error caught only because the first one triggered full-quote review. Single-line deletion would have left the under-collected reg in place.

**D9. ADM kill list, demand removal in first counter, do NOT negotiate around it.** When a dealer quote contains any Additional Dealer Markup line on NEW MY inventory (see `references/outreach_strategy.md` § New-Car ADM Detection, full kill list: Market Adjustment, Hybrid Premium / Hybrid Adjustment / Toyota Premium, Dealer Markup / Dealer Adjustment, Allocation Fee / Allocation Premium / Protection Plus when bundled with MSRP-overage), the FIRST counter must demand removal as a precondition, not propose a counter-amount or middle-meet. ADM is dealer-side margin theater dressed as a fee; trying to "split the difference" implicitly accepts that ADM is a real line item. It is not.

Exact email language (paste-ready, paraphrase the line name to match the dealer's quote):

> *"Please remove the $X [exact ADM line name as it appears on the quote] line. Per current market on [Year Make Model Trim], MSRP is the ceiling, not the floor; [Edmunds/CarGurus] [region] shows the fair-price band at or under MSRP. If the ADM stays, OTD walks above my ceiling and this unit cannot win."*

Three rules:
1. **Do not couple ADM removal to any other concession** (captive financing, F&I add-ons, faster close). ADM is its own line; coupling lets the dealer trade a fake concession for a real one. The captive-vs-CU rebate question (`references/payment_methods.md` § Captive-vs-credit-union rebate playbook) is decided on its own merits AFTER ADM is killed.
2. **One ask, one round.** If dealer refuses ADM removal in the reply, mark dead and route to the next-best MSRP-clean candidate. Do not negotiate to a smaller ADM ($1,495 → $750); a $750 phantom line is still phantom. The Phase 3 ADM Tier-3 ranking already pre-positions Tier-1/2 MSRP-clean alternatives for exactly this pivot.
3. **Cross-state-net override stays the Phase 3 decision, not Phase 6 leverage.** If a DE/NH/OR ADM dealer's net OTD still beats a PA MSRP-clean offer (per `outreach_strategy.md` § Cross-state ADM nuance), that decision was already made at Tier-2 promotion in Phase 3. Phase 6 still demands removal first, the cross-state arbitrage is the back-up, not the opening ask.

Example from the RAV4 Hybrid PA case: a PA Toyota dealer opened at ~$40k OTD with $1,495 "Toyota Market Adjustment" baked in. ADM removal alone drops OTD to ~$39k (well inside the buyer's ceiling and binding cap). Counter-coupling ADM removal with captive-lender financing would have lost ~$1,000 in interest savings the captive rebate-rate offer was offering independently.

**D10. "Listing disappeared" / bait-and-switch protocol.** When a dealer claims the original VIN-X you asked about is "just sold" / "in the wash bay being prepped for another buyer" / "in transit and never made it to the lot" and pivots to VIN-Y at a higher price OR more miles OR with ADM, treat this as a bait-and-switch attempt by default. The original-listing-still-active rate after a "just sold" claim is empirically ~40-60% (the listing reappears 24-72h later at higher price), and the pivoted VIN-Y is almost never at the same OTD-per-config as the original VIN-X anchor.

Required defenses (all three, not pick-one):

1. **Proof-of-sale ask.** Reply in writing: *"Can you forward the sold-date confirmation (bill of sale screenshot, CRM `STATUS=Sold` timestamp, or the listing-removed date from your inventory system)? I want to make sure I'm not still racing the same VIN with the next dealer."* Refusal or vagueness = bait-and-switch confirmed. Compliance = legitimate. If listing reappears within 7 days on Carfax / Cars.com / dealer website, the dealer lied, walk and log permanently as a low-trust counterparty.

2. **Same-or-better OTD on the substitute, no upgrade markup.** If the dealer pivots to VIN-Y, the substitute must come in at the same or lower OTD as the original VIN-X benchmark, adjusted ONLY for legitimate config delta (trim, miles, color) using `references/negotiation_playbook.md` mileage and trim adjustments. The dealer cannot use the bait-and-switch as a free upgrade-markup opportunity. Reply: *"For the substitute to work, the OTD needs to land at or under $X (the locked OTD on the original VIN, adjusted for [Y miles delta x $0.10-0.15/mi] / [trim premium of $A] / [no other variables])."*

3. **Pause and re-anchor, treat the pivot as a NEW dealer engagement.** Do NOT let the dealer pivot mid-conversation to a different VIN as if it's the same negotiation. If the pivot is forced (buyer wants the substitute), restart the engagement: re-run Phase 3 single-VIN anchor analysis on the new VIN against `references/deal_data_sources.md` market data, re-pull cross-bid quotes from the other dealers for the same config, and re-anchor before sending any counter. A 5-line "OK what's the OTD on VIN-Y?" reply without re-anchoring concedes the entire negotiation.

Real-world pattern: dealer's original VIN-X listed at $26,500 (great deal, low miles, in-state, MSRP-clean). Buyer responds same day, dealer replies T+24h "just sold to another buyer this morning, but I have VIN-Y at $29,200 with 8k more miles, same trim, fresh on the lot." Without D10, buyer accepts the pivot and pays $2,700 over the anchor; with D10, buyer demands sold-confirmation (dealer cannot produce), waits 5 days, sees the original VIN-X relisted at $27,900, confirms the pivot was theater, walks.

**D11. Dealer group ownership check, same parent = 1 anchor, not 2.** Before treating two dealer OTD quotes as "independent cross-bids", check the parent group. Many large auto groups own multiple dealers per region, and inter-group coordination on pricing is routine (the same regional GM sets the OTD floor for sibling stores). Two quotes from sibling stores are NOT real cross-bid leverage, they're a single anchor presented twice with inflated room for "competing" theater.

Check method (run BEFORE Phase 6 cross-bid disclosure, ideally at Phase 4 outreach time):

1. **Google "[dealer name] Auto Group ownership" or "[dealer name] parent company".** Public-corp dealer groups disclose ownership; mid-tier groups have it on About pages. DealerInspire partner directory + dealer.com partner listings also surface parent groups.
2. **Common parent groups to memorize (US, 2024-2026):**
   - **Penske Automotive Group** (NYSE: PAG), ~150 US dealers across Honda, Toyota, BMW, Mercedes, Audi, VW, Porsche, Land Rover, Lexus, Acura. Sibling-store dense in CA, FL, NY, NJ, TX.
   - **Berkshire Hathaway Automotive (BHA)**, ~100 US dealers; concentrated in TX (former Van Tuyl), AZ, CO, GA, FL, IL, IN, MS, OK. Operates as "Berkshire Hathaway Automotive" but local stores often retain founder names (e.g., "Sewell" in TX).
   - **Asbury Automotive Group** (NYSE: ABG), ~150 US dealers; concentrated in FL, GA, TX, NC, MO, IN, CO, NJ.
   - **AutoNation** (NYSE: AN), ~315 US dealers; concentrated in FL, TX, CA, AZ, NV, CO, IL.
   - **Sonic Automotive** (NYSE: SAH), ~110 US dealers; concentrated in CA, TX, NC, GA, FL.
   - **Lithia Motors / Driveway** (NYSE: LAD), ~290+ US dealers; nationwide, fastest-growing roll-up 2020-2026.
   - **Group 1 Automotive** (NYSE: GPI), ~150 US dealers; concentrated in TX, OK, FL, GA, LA, MA, NJ, NH, NY, MS.
   - **Hendrick Automotive Group**, ~140 US dealers (private); concentrated in NC, SC, VA, TN, GA, AL, FL, CA, KS, MO.
   - **Holman / Holman Automotive**, ~40 US dealers; concentrated in NJ, PA, FL.
   - **Ken Garff Automotive Group**, ~60+ US dealers; concentrated in UT, NV, CA, AZ, TX, IA, MI.

Treatment when sibling-store overlap found:

- **Collapse the duplicate.** Treat both quotes as a single anchor representing the parent group's floor. Use the lower of the two as your reference number.
- **Do NOT cite the sibling quote as a competitor.** Citing Penske-Honda-of-Old-Bridge against Penske-Honda-of-East-Brunswick to a Penske rep is comedy, they share an internal pricing dashboard. The dealer will laugh and price will not move.
- **Replace the duplicate with a true cross-group anchor.** Phase 4 outreach should target 3-4 different parent groups in radius, not 3-4 stores from the same group. If radius is sibling-store-saturated (common in FL, TX, CA metro areas with Penske / AutoNation / Asbury density), expand radius or accept fewer truly-independent anchors.

Real-world pattern: a buyer gets 4 quotes for a 2023 Camry XLE from <Dealer A>, <Dealer B>, <Dealer C>, and <Dealer D>. Two of them (<Dealer A> and <Dealer B>) turn out to be owned by the same regional dealer group (same GM, one shared inventory system). Phase 6 buyer cites <Dealer A>'s $32,400 OTD to <Dealer B>'s rep, expecting a $200-500 drop. The rep replies "that's our sister store, our system shows the same floor, best I can do is match $32,400." The two same-group quotes are 1 anchor, not 2. Real cross-bid leverage comes from the two independents (<Dealer C> and <Dealer D>). With D11, buyer routes outreach correctly from the start.

### S. Data Sourcing & Sources

**S1. Pull real-time deal data BEFORE quoting any discount or OTD estimate.** Heuristics are reliably wrong by $1-3k in either direction. The 5-query Firecrawl pipeline takes ~5 minutes and corrects baselines that would otherwise misdirect the entire negotiation. See `references/deal_data_sources.md`.

**S2. For login-required sites (XHS / Facebook / Instagram), Playwright MCP local browser beats Firecrawl Live View URL.** Playwright pops a browser window on the user's screen, they log in via QR/SMS in 30 seconds. Subsequent navigation, snapshot, evaluate, screenshot all operate on that logged-in session. Cookies persist in user's local Chrome profile.

**S3. XHS `/explore/{id}` direct URLs 404 without an access token.** The same post works via `/search_result/{id}?xsec_token={token}&xsec_source=` where token comes from a fresh search-page anchor's `href`. Tokens may expire after ~24h. Always source XHS URLs from a current search-page `browser_evaluate`, never from memory or old links.

**S4. ~80% of XHS post images are NOT quote evidence.** Stock photos, delivery selfies, Apple Notes title cards, decorative emoji covers. Protocol: extract all img URLs via `browser_evaluate`, download all candidates, Read each one, `rm` the non-evidence files immediately. Useful keepers: dealer worksheets, sales-rep email/SMS screenshots, Costco quote sheets.

**S5. For regional anchor evidence, XHS search MUST include the state/region keyword.** Generic `forester 报价` returns posts from CA/TX/MI/PA/WV, wrong regional market. Adding `NJ` / `新泽西` / `纽约` exposes posts from the buyer's tri-state area with same-dealer same-trim quotes. Run two parallel searches when buyer's state is known: generic for national anchor + state-specific for regional anchor.

### N. Negotiation Mechanics

**N1. Use OTD anchors transparently across multiple dealers.** Once 2+ written OTDs exist, cite them by dollar amount in counters: "My locked benchmarks are X at $X,XXX and Y at $X,XXX, for your unit to switch me, OTD needs to land near those." Converts each competitor offer into a market data point. Pulls subsequent offers down reliably.

**N2. Parallel "drop $X" asks elicit counter-offers within 1-3 hours when framed correctly.** Formula: "Your X at $A vs locked alternative at $B with [advantage]. For your unit to win, OTD needs to land near $TARGET. If math does not pencil, I will go with the locked alternative by [deadline]." In practice, 3 dealers in one metro each dropped OTD within 1-3h (Rep A -$X,XXX, Rep B -$X,XXX, Rep C -$X,XXX). Run dealers in parallel, never sequentially.

### V. Vehicle Verification

**V1. CARFAX 1-owner is necessary but not sufficient.** Service records reveal whether the 1 owner actually maintained the car. Missing CVT fluid service at 60k is a $300-400 inherited cost.

**V2. Require dealer-provided full CARFAX PDF or live URL before accepting OTD or scheduling PPI.** Verbal "clean carfax, 1-owner" has a real failure rate. Real incident: a dealer's written "clean CARFAX" claim turned out to hide a prior minor damage event with front + left + right impact zones. Buyer revised target down by $1.5-2k AND requested body-shop docs + EyeSight recalibration + structural report. Never accept OTD on verbal CARFAX summary.

### P. PPI & Test Drive

**P1. With 2-4 final candidates, book mobile PPI in parallel and cancel after dealer choice finalized.** Mobile services (Lemon Protector $139+ in NY/NJ/CT, YourMechanic, Pep Boys Mobile) eliminate dealer-side transport coordination. Stagger times (9 AM / 10 / 11 / 12 PM) to avoid form conflicts. Each NOTES field: "BOOKING X OF N - TENTATIVE, finalizing by [time]". Inspector phone gets dealer phone + VIN + address per slot.

**P2. Online PPI booking forms have predictable quirks.** Year dropdowns cap at current/-1 year (newer vehicles need NOTES annotation). DATE inputs are `<input type="date">` requiring ISO YYYY-MM-DD. State defaults to service's HQ state. Phone TYPE defaults to "Cell" but dealer phone should be "Work". Always re-snapshot after `fill_form` before Submit.

**P3. Close-day F&I (Finance & Insurance) hard-no script.** After OTD is locked in writing and the agreement is signed, the F&I office is the highest-frequency point of last-minute margin recovery: GAP coverage ($795-$1,295), VSC / extended service contracts ($1,495-$3,000), tire-and-wheel protection ($399-$799), paint / fabric protection ($499-$1,299), key replacement ($299-$499), nitrogen tires ($199), dent / ding ($499). Each is presented as "small monthly add" ($25/mo) hiding the lump-sum capitalization. F&I officers are paid on attach rate; expect 3-5 distinct pitches in a 30-45 minute close, often with paperwork shuffled so add-ons appear pre-initialed.

Paste-ready hard-no script (read verbatim if pressured, or hand over the printed copy):

```
Per my signed agreement dated [DATE] with [GM/Sales Manager name],
the OTD is locked at $[X]. I decline GAP, VSC, tire-and-wheel,
paint protection, key replacement, nitrogen, dent / ding, and any
other add-on not in the original agreement. Please process the
close at the agreed OTD, or I will exit and we will both lose
time. Repeat: NO add-ons. I will sign only the original
agreement.
```

Operational rules:

1. **Do NOT initial any new line item without a 5-minute pause to re-read.** F&I officers shuffle paperwork; a "just initial here for the title work" is sometimes a GAP authorization slipped into the stack. If anything is newly initialed-for, pause, take the page out of the folder, read every line, and verify it matches the agreement. The pause itself is a tactic, it slows the close and signals the buyer is not in a hurry.
2. **Mandatory add-on response.** If F&I claims an add-on is "required by the dealership" (it is not, with the rare exception of state-mandated docs), reply: *"Please show me the line item in my signed agreement that authorizes this charge. If it's not there, remove it; if you cannot remove it, I will exit and the deal is dead. Per my OTD lock at $[X], adding anything constitutes a new deal that I have not agreed to."*
3. **Monthly-payment-shift trick.** F&I will sometimes say "we can add GAP and your monthly only goes up $18". Reply: *"My agreement is OTD-locked, not monthly-locked. Adding $18/mo for 72 months is $1,296. I decline."* The monthly-shift framing exploits financing-buyer focus on monthly cap; D9-style ADM-vs-financing decoupling applies here too.
4. **Recourse if F&I refuses to honor the locked OTD.** Walk to the sales floor and ask for the GM by name (the one on the signed agreement). The GM signed off; the F&I officer is breaking the agreement. If the GM also refuses, the deal is dead. State law in most jurisdictions allows buyer to recover the deposit if the dealer materially changes the terms.
5. **Pre-close communication.** At Phase 6 close-day kickoff (before driving to dealer), re-confirm with the GM in writing: *"Confirming the OTD at $[X] per our agreement dated [DATE]. I will decline any F&I add-ons at close per my no-add-ons posture from Day 1. Please brief your F&I officer so we don't burn time on add-on pitches."* This pre-empts ~70% of close-day F&I friction by routing the no-add-ons signal to F&I before the buyer walks in.

Cross-references: `assets/dealer_reply_template.md` § "Add-On Refusal" + the new F&I close-day hard-no template; `references/negotiation_playbook.md` § "Add-On Refusal" pricing detail. See also gotcha D9 for the structurally identical ADM-removal protocol, F&I add-ons are ADM in a different uniform.

### H. Session & State Hygiene

**H1. A previous Claude Code session may have invented fictitious dealer dialogue.** Always cross-check any "tracker log" entry against actual Gmail thread before acting. Counter-offers built on hallucinated context are how deals fall apart.

**H2. Cleaning drafts: only delete `DRAFT`-label items.** See I5, accidentally trashing INBOX/SENT items breaks future reply threading.

