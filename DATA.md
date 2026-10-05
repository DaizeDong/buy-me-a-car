# Purchase DATA storage

Real purchase inputs, reports, source captures and inbox state belong in a verified
PRIVATE Git companion. tools/runtime_paths.py resolves BUY_ME_A_CAR_CONFIG or
BUY_ME_A_CAR_DATA_DIR and proves repository visibility before access. Missing or
unknown proof fails; there is no public or unversioned fallback.

Final reports include user-selected synthetic acceptance cases. Their synthetic
inputs do not make the requested final deliverable disposable. Preserve the final
HTML/PDF, structured configuration, validation and unique cited evidence.

## Companion lifecycle

The machine-readable artifact contract is [storage.contract.json](storage.contract.json).
Its paths are relative to the PRIVATE companion's DATA directory. Each artifact
records its producer, consumer or final deliverable, schema and recovery method.
The companion README identifies selected final deliverables. Runtime records never
fall back into this public repository.

Keep a current `retention.json` in DATA, following
[schemas/storage-retention.schema.json](schemas/storage-retention.schema.json).
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

Generated-area admission refuses further writes once existing usage reaches
2,000 files or 128 MiB. The check measures current usage before a writer receives
its destination; it is an admission limit, not a per-write reservation. Core
purchase records, final reports and their source evidence are never evicted to
make room. Review completed work and its recovery obligations before reclaiming
capacity.
