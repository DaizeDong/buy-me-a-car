# Cycle Feedback Log

Fill this in at the end of every completed (or aborted) buying cycle. This is the structured input to the next skill iteration — vague "it went OK" notes do not produce skill changes.

One row per cycle. Append; do not overwrite. Most recent cycle on top.

---

## Cycle: {YYYY-MM-DD short title, e.g. "2026-06-12 Forester CT cash"}

### Cycle metadata

| Field | Value |
|---|---|
| Date(s) | {YYYY-MM-DD to YYYY-MM-DD} |
| Buyer (handle / first name) | {e.g., buyer handle} |
| Dealer(s) involved | {e.g., 3 in-radius Subaru dealers} |
| Vehicle scenario (new / used, make / model / trim / year) | {e.g., used 2023 Subaru Outback Limited} |
| Buyer type axes (cash / finance / lease / trade / EV / pickup / luxury / HD / commercial) | {e.g., cash, no trade, no EV} |
| Registering state + ZIP | {e.g., CT <ZIP>} |
| Outcome | {Closed / Walked / Pivoted mid-cycle / Aborted} |
| Final OTD vs walk-away ceiling | {e.g., $28,950 OTD vs $30,000 ceiling — 3.5% under} |

### What worked

(Bullet list. Concrete — name the phase / reference / tactic that fired correctly. Worked = produced a measurable advantage or avoided a known failure mode.)

- {e.g., "P1 heads-up block fired (c) timeline + (h) trade-without-numbers, surfaced both to buyer before P2 — saved 2-3 days of wasted outreach on a too-short timeline."}
- {e.g., "D8 state-template-leak detection caught an NJ tire fee on the CT quote on first read; full re-quote produced a $90 reduction plus $40 reg correction."}

### What failed

Categorize each failure by phase or rule. Use the table below. Add rows as needed.

| Phase / rule | What happened | Where the skill failed (concretely) | Cost (time / dollars / leverage) |
|---|---|---|---|
| Phase 1 | {e.g., financing gate didn't fire even though buyer mentioned "thinking about a loan" in P0 chat} | {SKILL.md Phase 1 trigger lacks fuzzy match on "loan" / "thinking about financing" / "might finance" — only fires on explicit "I will finance"} | {1-2 hours of P3 work had to be redone after pivot} |
| Phase 2 | {e.g., baseline pull had 4 SYNTHESIZED rows that almost leaked into a Phase 4 email} | {Critical Rule #7 caught it at draft-review, but no automated guardrail at draft-creation time} | {15 min near-miss} |
| Phase 3 | {} | {} | {} |
| Phase 4 | {} | {} | {} |
| Phase 5 | {} | {} | {} |
| Phase 6 | {} | {} | {} |
| Phase 7 | {} | {} | {} |
| Phase 8 | {} | {} | {} |
| Phase 9 | {} | {} | {} |
| Outbound Email SOP | {} | {} | {} |
| Gotcha violation (specify which) | {e.g., D5 used/new mixing — counter to Toyota new-MY dealer cited a used-RAV4 OTD anchor by accident} | {Cross-bid anchor list in tracker did not visually segregate used vs new rows; agent grabbed the lowest OTD without checking the new/used flag} | {Dealer disengaged for 24h; cycle leverage reset} |

### Buyer-facing surprise

(One row per surprise. A "surprise" = something the buyer hit that the skill did not warn them about in advance.)

| Surprise | What the buyer expected | What actually happened | Should the skill have warned? Where? |
|---|---|---|---|
| {e.g., "GAP coverage pitched again at title-clerk window after F&I close"} | {Buyer expected F&I close = end of all add-on pitches} | {Title clerk re-pitched GAP "for plate protection"; buyer initialed declining} | {Yes — gotcha P3 close-day F&I hard-no should add a "title-clerk window is a second F&I pitch surface" note} |
| {} | {} | {} | {} |

### Skill-specific gap

(What's missing from the skill itself — a reference file that doesn't exist, a wrong number, a misclassified state, a missing buyer-type branch, a stale rule.)

| Gap | Concretely | Suggested fix |
|---|---|---|
| {e.g., "Phase 7 PPI report extraction template missing"} | {PPI PDF arrived; pdf_review_checklist.md has CARFAX + service-record + OTD-proposal templates but no PPI template; agent improvised} | {Add PPI extraction section to pdf_review_checklist.md: tire tread depth in /32"s, brake pad mm, battery CCA, fluid conditions, leak callouts, suspension flag, alignment readout} |
| {} | {} | {} |

### Action item — what to change in the next skill iteration

(One row per concrete change. Phrase as "EDIT {file} {section}: {change}".)

1. {e.g., "EDIT SKILL.md Phase 1 financing gate: expand trigger phrases to include 'loan', 'finance', 'might finance', 'thinking about financing', not just 'I will finance'."}
2. {e.g., "EDIT references/pdf_review_checklist.md: add PPI report extraction template as section 4 (after Service Record Gap Detection)."}
3. {e.g., "EDIT assets/dealer_reply_template.md: voice red flags table: add 'title-clerk window' as a new close-day pitch surface to call out in F&I hard-no script."}

### Cycle composite rating (optional, internal)

| Phase | Rating 1-10 | One-line reason |
|---|---|---|
| P1 | {} | {} |
| P2 | {} | {} |
| P3 | {} | {} |
| P4 | {} | {} |
| P5 | {} | {} |
| P6 | {} | {} |
| P7 | {} | {} |
| P8 | {} | {} |
| P9 | {} | {} |
| Composite | {} | {} |

---

## How to use this log

1. **Fill it in within 24h of cycle close** — memory degrades fast.
2. **Be concrete.** "P1 was OK" is useless. "P1 (h) trade-without-numbers fired correctly but did not trigger when buyer said 'I have an old Civic' (no payoff / mileage / title mention) — only fires on explicit 'I want to trade'" is actionable.
3. **Categorize failures by phase + rule.** This is the bucket the next iteration uses to prioritize.
4. **Distinguish buyer-facing surprise from skill-specific gap.** Surprises are downstream symptoms; gaps are the structural cause. Both belong in the log; only gaps get codified into reference files.
5. **Action items must reference a specific file + section** — "improve the skill" is not an action item.
6. **Append, don't edit.** Older cycles stay for trend analysis. If a gap appears in 3+ cycles, it is a Tier-1 fix for the next iteration.

When the next iteration starts (P5+ or P6 wave), read this log top-down and convert action items into delta-table rows in `p0_p5_execution/` or equivalent tracker.
