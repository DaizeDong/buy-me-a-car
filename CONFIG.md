# Runtime storage configuration

[config.contract.json](config.contract.json) classifies this skill as runtime-storage-only.
Purchase criteria, reports and quote inputs are selected per invocation. There is no global
product registry or settings initializer. [DATA.md](DATA.md) owns output lifecycle guidance.

## Discovery and switching

The first nonempty explicit environment selection is authoritative. If that selected path is
missing, resolution fails before writing rather than trying a lower-priority location. When no
explicit selector is set, discovery continues through the sibling and home conventions below.
Clear stale higher-priority variables before switching:

1. `BUY_ME_A_CAR_DATA_DIR`: the exact `data` child of the PRIVATE companion.
2. `BUY_ME_A_CAR_CONFIG`: the companion root.
3. `BUY_ME_A_CAR_CONFIG_DIR`: companion-root alias.
4. A proven sibling `buy-me-a-car-config` discovered by pinned Guards.
5. `~/.buy-me-a-car-config`.
6. Legacy `~/.buy-me-a-car-data`, only when it contains the required companion `data` child.

All layouts use `<companion>/data`; a missing child does not move output to the root.
Initialize and commit the separate PRIVATE companion, authenticate `gh`, then point one
selection at it. All effective fetch and push destinations must prove PRIVATE. Public,
unknown, unborn, ignored, undeclared and retired output targets fail before parent creation.

To switch A to B in PowerShell:

```powershell
Remove-Item Env:BUY_ME_A_CAR_DATA_DIR -ErrorAction SilentlyContinue
Remove-Item Env:BUY_ME_A_CAR_CONFIG_DIR -ErrorAction SilentlyContinue
$env:BUY_ME_A_CAR_CONFIG = "<private-companion-B>"
python tools/runtime_paths.py --write
python tools/doctor.py --private
```

For POSIX shells, use `unset BUY_ME_A_CAR_DATA_DIR BUY_ME_A_CAR_CONFIG_DIR` and
`export BUY_ME_A_CAR_CONFIG="<private-companion-B>"`. The path command performs admission
without writing a purchase record. The doctor reports local dependencies separately from
PRIVATE proof; neither command proves mailbox, scheduler, model, PDF or real purchase outcomes.

## Output ownership

Every write must match exactly one active declaration in [storage.contract.json](storage.contract.json).
The pinned Guards authorizer checks the source contract and version-control eligibility before
creating output parents. Retained historical paths do not authorize new writes. Add a reviewed
producer, schema, consumer and recovery rule before introducing a new output kind.

Current evaluation output locations and continuation commands are documented in the
[evaluation guide](eval/README.md). Follow [DATA.md](DATA.md) when retaining or restoring their
receipts and referenced inputs.
