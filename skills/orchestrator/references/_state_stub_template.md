# State Detail-Stub Template

> **purpose**: The reusable skeleton for a per-state detail stub at full (CT/CA/TX/MD) depth, to be
> dropped into `references/state_fees.md`. Use this so every new state stub carries the same sections,
> the same "Does NOT have" leak-list discipline, and, non-negotiable, a `verified:` line.
>
> **authority rule**: The structured numbers (tax rate, doc cap, title, reg, trade-credit posture,
> EV surcharge) are owned by `data/state_fees.json`. A stub must MATCH that JSON, never contradict it.
> If you discover the JSON is wrong, fix the JSON first (separately), then write the stub.
>
> **freshness rule**: Every stub MUST end with a `verified:` line (see below). A stub without one is
> incomplete and must not be merged. `scripts/check_freshness.py` audits the JSON's dates; the stub's
> `verified:` line is the human-prose mirror of that.

---

## Skeleton (copy from `<<<` to `>>>`, delete the markers, fill every `<...>`)

```
<<<
### <XX> — <State Name>

- **Sales tax**: <state rate>% <mechanism note: flat / TAVT / HUT / SUT / excise / IMF>; <local stacking: "no local stacking" OR "+ X-Y% local at buyer ZIP">.
- **Doc fee cap**: <$N statutory cap, cite statute> OR <**No statutory cap** — typical industry range $X-Y; treat anything above $Y as a leak>. <one line on how it ranks vs neighbors>.
- **Title fee**: $<N>. **Registration**: $<N> <per year / biennial — annualize if biennial>.
- **Trade-in tax credit**: <**YES** — taxable base is sale price minus trade> OR <**NO** — full price taxed; this is the structural disadvantage vs <neighbor>> OR <N/A — no sales tax>.
- **Has**: <every real, citeable line item a buyer will see: lien recording, tire/battery/environmental fee, inspection at sale, EV reg surcharge $N, county emissions, etc. Omit the section if genuinely none.>
- **Does NOT have**: <leak list — name the fees buyers in OTHER states get hit with that do NOT apply here, so the reviewer can spot a padded out-of-state quote. Mirror the `does_not_have` array in state_fees.json for this state.>

#### <XX> Worked OTD Example (<county/ZIP>, <scenario: no trade>)

Sales $<P>, doc $<D>, <XX> <rate>%:

```
Taxable = $<P> + $<D> = $<P+D>
Tax     = $<P+D> × <rate decimal> = $<tax>
Title   = $<N>
Reg     = $<N> (<annualized if biennial>)
<other line items>
OTD     = <sum> = $<OTD>
```

#### <XX> Worked OTD Example (<county/ZIP>, $<T> trade)

Sales $<P>, doc $<D>, trade $<T>, <XX> <rate>%:

```
Net sale   = $<P> - $<T> = $<P-T>
Taxable    = $<P-T> + $<D> = $<...>   # OR full $P+$D if trade credit = NO
Tax        = $<...> × <rate decimal> = $<tax>
Title      = $<N>
Reg        = $<N>
<other line items>
Cash OTD   = $<OTD>
Tax savings on trade = $<T × rate> (<or $0 if no trade credit, call it out>)
```

verified: <YYYY-MM-DD> | source: <statute cite | DMV URL | both> | by: <author/agent>
>>>
```

---

## Mandatory `verified:` line rule

Every stub ends with exactly one line of this shape, as the last line of the stub:

```
verified: YYYY-MM-DD | source: <statute cite or stable URL> | by: <author>
```

- `verified:` date is the date you web-confirmed the numbers against the cited source, NOT the date
  you copied them from the summary table.
- `source:` must be authoritative: a state statute citation (e.g. `MD Transportation § 15-311.1`),
  a `.gov` DMV/DOR URL, or both. A secondary source (blog, dealer site) is not sufficient on its own
  for tax rate / doc cap.
- The date here should match `source_verified_date` for the same state in `data/state_fees.json`.
  If they drift, the JSON wins and the stub must be re-verified.
- A stub merged without this line is incomplete. Reviewers should reject it.

---

## Author checklist (run before merging a new stub)

- [ ] State `XX` and full name correct in the `###` heading.
- [ ] Tax rate, mechanism, doc cap, title, reg, trade-credit posture, EV surcharge ALL match
      the corresponding record in `data/state_fees.json` (no contradictions).
- [ ] If the stub revealed a JSON error, the JSON was fixed first (separately), not just the prose.
- [ ] Doc cap line states the statute (if capped) or says "no statutory cap" + typical range explicitly.
- [ ] Registration is annualized in the no-trade worked example if the state registers biennially.
- [ ] Trade-in worked example correctly applies (or correctly withholds) the trade tax credit per posture.
- [ ] "Does NOT have" leak list mirrors the `does_not_have` array for this state in state_fees.json.
- [ ] At least one no-trade and one with-trade worked OTD example, with arithmetic that actually sums.
- [ ] Final `verified:` line present, dated, with an authoritative `source:` and an author.
- [ ] `verified:` date equals the state's `source_verified_date` in state_fees.json.
- [ ] If this stub upgrades a state from `summary` to `full`, bump `detail_depth` to `full` in the JSON
      (separate edit by the JSON owner) so `render_state_data.py` reflects it.

---

## Notes

- Keep the depth consistent with existing full stubs (CT, CA, TX, IL, MD, FL, OH, NC, GA, MI, VA, WA, DC).
  Read one of those in `state_fees.md` before writing a new one to match tone and granularity.
- This template is intentionally prefixed `_` so it sorts to the top of `references/` next to
  `_data_sources.md` and is easy to spot as scaffolding rather than content.
