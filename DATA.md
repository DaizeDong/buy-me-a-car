# Purchase DATA storage

Real purchase inputs, reports, source captures and inbox state belong in a verified
PRIVATE Git companion. Follow [CONFIG.md](CONFIG.md) to select and validate storage
with `tools/runtime_paths.py`. Missing or unknown proof fails; there is no public
or unversioned fallback.

Final reports include user-selected synthetic acceptance cases. Their synthetic
inputs do not make the requested final deliverable disposable. Preserve the final
HTML/PDF, structured configuration, validation and unique cited evidence.

## Companion lifecycle

The machine-readable artifact contract is [storage.contract.json](storage.contract.json).
Its paths are relative to the PRIVATE companion repository root. Runtime DATA
artifacts use the `data/` prefix; setup metadata and selected source captures have
separate root-level declarations. Each artifact
records its producer, consumer or final deliverable, schema and recovery method.
The companion README identifies selected final deliverables. Runtime records never
fall back into this public repository.

Keep a current `retention.json` in DATA, following
[schemas/storage-retention.schema.json](schemas/storage-retention.schema.json).
The register and its path entries remain relative to DATA. The native retention
command translates those paths to the contract's `data/` scope before checking
ownership and core protection; returned plan paths remain DATA-relative. The
retired nested development pattern is `data/data/**`, which does not cover
current DATA or final deliverables.

List active runs, supported rollback dependencies and selected final evidence in
`protected_paths`. A retirement entry requires completed work, released dependencies
and a concrete reason. Unknown files and core artifacts are refused even when a
retirement entry claims completion. Stop writers before maintenance; age is not
an inactivity proof. Preview with `python -m tools.storage_retention`, then apply the
reviewed selection with `python -m tools.storage_retention --apply`.

The command checks confinement, link metadata, content hashes and core protection
before removing ordinary files. It never follows junctions or rewrites event logs.
The registry is one current document, not a sequence of timestamped backups.
Restore retired bytes from its `source_commit` in the existing PRIVATE Git history.
Keep that commit reachable; no new archive bundle is required.

Selected fee-source captures at the companion root remain evidence for maintained
source citations. The dossier-specific `officials/capture_sources.py` helper is
a retained evidence-refresh dependency with DATA confinement; its declaration
does not run a capture. Review source age and refresh needs before use; retention
does not prove the fees are current. Unselected review responses are rebuildable
after their remaining evidence dependencies have been checked.

Generated-area admission refuses further writes once existing usage reaches
2,000 files or 128 MiB. The check measures current usage before a writer receives
its destination; it is an admission limit, not a per-write reservation. Core
purchase records, final reports and their source evidence are never evicted to
make room. Review completed work and its recovery obligations before reclaiming
capacity.

[Opt-in evaluation](eval/README.md) writes current records under `data/research-runs/`
in the companion. The former `data/eval/` namespace is retained as historical retired
material and cannot receive new writes. Restore current receipts and referenced
inputs together before any continuation.
