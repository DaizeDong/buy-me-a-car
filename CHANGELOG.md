# Changelog

All notable changes to this project are documented here (Keep a Changelog style).

## [Unreleased]

### Fixed

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
