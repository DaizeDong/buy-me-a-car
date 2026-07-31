# Post-cycle feedback protocol

> Moved out of SKILL.md under PHILOSOPHY P7: it runs once, at cycle close or abort, not on every
> invocation. The log itself is `assets/feedback_log.md`; this is how to fill it.

After every completed (or aborted) cycle, fill `assets/feedback_log.md` to capture what failed, what surprised the buyer, and what skill-specific gap surfaced. This is the structured input to the next skill iteration.

The log is append-only, older cycles stay for trend analysis. If the same gap appears in 3+ cycles, it becomes a Tier-1 fix in the next iteration wave.

Concrete = actionable. "P1 was OK" produces no skill change. "P1 (h) trade-without-numbers fired correctly on explicit 'I want to trade' but did NOT fire on 'I have an old Civic'" is a specific Phase 1 trigger-phrase expansion that the next iteration can implement.

Trigger this step:
- At cycle close (after PPI passes, after deposit, after cashier's check, OR after walk-away)
- At cycle abort (after Mid-Cycle Pivot Protocol fires AND buyer changes target so significantly that the cycle does not resume)
- After every Gotcha violation (D5, D8, D9, D10, D11, P3, etc.), log even if the cycle continues; gotcha violations are the highest-leverage learning surface

The fill takes 10-15 minutes. Skipping it means the next iteration has nothing concrete to act on.

