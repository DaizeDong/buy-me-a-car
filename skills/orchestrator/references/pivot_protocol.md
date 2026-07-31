# Mid-cycle pivot protocol

> Moved out of SKILL.md under PHILOSOPHY P7: it fires on roughly one cycle in three, so it is
> on-demand. SKILL.md keeps the load-bearing field list and the STOP rule that sends you here.

Mid-cycle = the buyer is somewhere between Phase 3 and Phase 9 and changes a load-bearing field that invalidates the in-flight artifacts. Common pivots:

- **Used to new** (or new to used), different desks, different incentive stacks, mileage adjustments no longer apply.
- **Cash to financing** (or financing to cash), binding-constraint changes from OTD ceiling to monthly cap; pre-approval / captive paths must be re-asked.
- **Model A to model B**, entire Phase 2 baseline, Phase 3 inventory pull, and Phase 4 outreach become irrelevant; new cross-bid set must be assembled.
- **ZIP / radius change**, registering state may change → tax rate, doc cap, "Has" / "Does NOT have" lists shift; in-flight quotes are state-template-leak suspects.
- **Walk-away ceiling change**, entire OTD ladder + Phase 6 counter-math is rooted in this number.
- **Trade-in added or removed mid-cycle**, separates-the-negotiation tactic must be reset; payoff workflow restarts.
- **EV-eligibility flip**, NACS / CCS1 port, SoH thresholds, state rebate re-enter; ICE OTD math no longer applies. (Federal §30D / §25E / §45W credits are TERMINATED for vehicles acquired after 2025-09-30, no longer part of EV math for current purchases; state/local rebates only.)

When the buyer changes any of these mid-cycle, the protocol is:

1. **STOP all in-flight drafting immediately.** Do not append new context to existing dealer threads. Do not save another draft. Do not send another counter. The next dealer reply that arrives during the pivot is held without drafting until the reset is complete.

2. **Enumerate ALL stale artifacts** in a single message to the buyer. Buyer needs the full list to clean up Gmail drafts, tracker rows, and baseline files. Use this template:

   ```
   Pivot detected: [old value] -> [new value] on field [X].
   The following artifacts are now stale and must be cleaned up
   before we resume:

   Gmail drafts:
     - in:drafts subject:[OLD_MODEL] before:[TODAY]
       (estimated [N] drafts — use this Gmail search string to
       bulk-select for trash)
     - any reply drafts referencing [old payment method / old ZIP /
       old walk-away]

   Working-directory files (review + delete or rename with .STALE
   suffix):
     - criteria.md (entire P1 capture is rooted in the old field)
     - .firecrawl/[OLD_MODEL]-deal-baseline.md (entire Phase 2
       baseline)
     - market_research/reports/report_*.md (Phase 3 site reports
       on the old model)
     - master_comparison.md (Phase 3 dedup)
     - dealer_outreach_tracker.md rows for outreach sent under old
       criteria (do not delete the file; mark rows with
       STATUS=STALE_PIVOT)
     - [old_model]_negotiation_prep.md
     - [old_model]_dossier.{md,html,pdf}

   Dealer-side cleanup:
     - For each dealer with an active thread on the old criteria,
       send a polite walk-away (see assets/dealer_reply_template.md
       "Walk-Away (Polite Close)") OR a pivot note ("Changing
       targets, will be back in touch if [new model] inventory
       overlaps your store"). Do NOT leave dealers hanging — they
       remember and it costs leverage on the next outreach.
   ```

3. **Re-run Phase 1.** Full criteria.md regeneration. Do NOT copy-paste from the old file and edit, the buyer-type router gates (financing / trade / EV), heads-up block, close-day logistics table, and walk-away ceiling all interact, and partial edits leave field-level inconsistencies that surface as bugs later (e.g., old financing fields stay populated after a financing-to-cash pivot, then trigger a binding-constraint computation that no longer applies). Restart from `assets/criteria_template.md`.

4. **Re-pull Phase 2 baseline.** New 5-query Firecrawl pipeline against the new model / state / incentive stack. Save to `.firecrawl/[NEW_MODEL]-deal-baseline.md`. Do NOT reuse the old baseline; manufacturer incentives and regional deal data shift weekly.

5. **Resume Phase 3 and onward** with the new criteria. New inventory pull, new mass outreach, new tracker (or new STATUS=ACTIVE rows in the existing tracker below the STALE_PIVOT rows).

Pivot frequency: empirically, ~30% of buying cycles see at least one load-bearing pivot between Phase 1 and Phase 9. Without this protocol, the agent silently keeps appending new context to stale artifacts, dealer drafts go out with mixed criteria (gotcha D5 firing pattern), tracker rows multiply with no clear cut-line, and the close-day execution operates on wrong assumptions (wrong walk-away, wrong payment instrument, wrong registering state). The protocol forces a hard reset.

**Mini-pivot exception**, changes to non-load-bearing fields (must-haves list edit, color preference, mileage cap ±5k mi, trim swap within same model + same MY + same financing posture) do NOT trigger the full reset. Update criteria.md inline, mark the change in the heads-up block, and proceed. The reset is reserved for the load-bearing axes listed above.

