# Changelog

All notable changes to this project are documented here (Keep a Changelog style).

## [Unreleased]

### Changed
- `tools/check_repository.py` no longer skips directories with a `.git` file (the submodule-era exemption); the README Roadmap badges show `v0.2.2` exactly, which the fleet-style doc contract now requires.
- Removed the `guards/` and `style/` submodules and the gate and sync workflows (pii-guard, dash-guard, doc-contract, load-budget, fleet-sync). The `.githooks` shims now run the privacy and dash checks from the local fleet-guards and fleet-style checkouts named by `git config fleet.guards` and `fleet.style`, and block when either is unset. `tools/runtime_paths.py` resolves the companion through the installed `fleet_guards.runtime.companion_resolver`, and `tools/doctor.py` checks that package instead of submodule files.
- Deleted the test suite (`eval/`) and the functional CI workflow; features confirmed working keep no tests.
- Removed the runtime PRIVATE proof. `tools/runtime_paths.py` no longer calls `prove_private_companion`, `gh api` visibility queries, `ssh -G` alias resolution or `authorize_artifact_write`; it resolves the companion through the pinned Guards resolver and checks each destination by path only (inside `<companion>/data`, outside this repository, no traversal, escaping links, `.git` components or nested repositories). Writes still fail when the companion is uninitialized. PRIVATE publication is enforced at commit time by the Guards hooks and CI. Proof-only tests, `tools/test_support.py` and `eval/test_visibility_any_gh_account.py` were removed and the fleet storage fixture was regenerated.
- `resolve_data_dir` checks own-repo containment once, through `_companion_root`, instead of first repeating the narrower inside-this-repository test.

### Fixed
- The live PRIVATE visibility check no longer depends on which gh account is active: it asks through the pinned guards kit's `query_github_visibility`, which tries the owner's stored account, every other stored account, then gh's default, and never switches the active account. Before, an active account that could not see the companion made every proof fail closed. Only PRIVATE is accepted.

### Documentation

- Replaced the bilingual Mermaid flowcharts with compact color PNGs and editable Graphviz sources. They show the initial buyer research HTML/PDF before written quotes and buyer-authorized steps through closing and handover.
- Consolidated report-delivery and storage guidance, corrected evaluation output paths, and aligned the email-format reference with the approved-offer and private-ceiling rules.

### Storage review threshold
- Set a 64 MiB companion working-data review threshold. Required observations and
  recovery state stay protected when the threshold is exceeded.

### Fixed

- Skip ordinary files already unlinked during advisory capacity scans when
  concurrent writers replace receipts; retirement still requires stable inputs.
- Retry local atomic receipt renames briefly when Windows metadata readers hold
  the destination open. Each attempt rechecks artifact authorization; exhausted
  or unrelated errors preserve the previous state and remain visible.
- Compare equivalent Windows extended paths consistently when capacity scans
  race sibling staging-file renames; actual DATA escapes remain rejected.
- Prove all effective companion fetch/push destinations, require source-owned active output declarations, and retain the `data` child in alternate installation layouts.
- Declare runtime-storage-only configuration; document exact precedence and safe companion switching in CONFIG.md, linked from both README editions.

- Align storage declarations with the whole companion repository while retaining
  DATA-relative native retirement plans; nested development material cannot
  classify current buyer evidence as retired.
- Restored the philosophy-first bilingual README, ordered badges, complete skill reference and version markers; clarified the different evidence requirements for buyer research and dealer proposals.
- Moved closing checklists and translated refusal scripts into linked on-demand references, and corrected helper-script links.
- Broad purchase requests now include a market comparison and buyer research HTML/PDF without a separate expansion prompt. Research supports zero written quotes and unknown costs; outward dealer proposals keep their stronger evidence requirements.
- Restored substantive research, visit preparation, private negotiation scenarios and pivot updates. Report schemas reject missing analysis and preserve duplicate-VIN observations, source access gaps and cost uncertainty.
- Real purchase input/output now requires a verified private companion; feedback no longer writes into a public asset. Generated fixtures and physical DATA checks are enforced separately.
- OTD uses decimal arithmetic, dated field evidence and explicit jurisdiction/transaction support. Corrected stale Maryland values and trade-in rules; unsupported calculations fail visibly.
- Dealer drafts separate the private maximum from an authorized outward offer. Inbox imports, cursor state and draft receipts survive restarts without replaying uncertain actions.
- Dossiers validate amounts, complete quotes and source artifacts, escape inserted text and verify fresh PDF output with page notices.
- All sixteen skills have an idempotent installer and readiness checks. Business tests now run in Windows/Linux CI, alongside existing guards.
- Browser extraction keeps card identity and prices together and reports incomplete fields and partial coverage. Removed unsupported savings, timing, site-access and fixed-page-count claims.
- Model evaluation now executes real tasks and a fresh-context review; registered skill names map explicitly to implementation directories.
- Added generated Alaska pickup response scenarios, private model/reviewer receipts and explicit AK calculation-refusal regressions. Pickup guidance now requires actual loaded weights and exact manufacturer limits; remote sourcing includes transport and winter requirements.

## [0.2.2] - 2026-05-19
### Changed
- docs: unify repo structure (Skill Repo Spec v1), philosophy-first README, bilingual top block, standardized badges.

### Added
- Multi-skill plugin: 1 orchestrator + 15 narrow sub-skills covering the full 9-phase pipeline (research -> outreach -> negotiate -> close).
- 50 US states + DC at fee-detail depth (34 web-verified); 16-brand CPO across 12 programs; 6 buyer paths incl. private-party.
- Trilingual surface (EN / CN / ES triggers; EN + CN dossier templates) with strict language-and-audience separation.
- `examples/` directory with 8 end-to-end worked scenarios.
