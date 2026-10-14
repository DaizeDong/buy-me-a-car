# Runtime storage configuration

[config.contract.json](config.contract.json) classifies this skill as runtime-storage-only.
Purchase criteria, reports and quote inputs are selected per invocation. There is no global
product registry or settings initializer. [DATA.md](DATA.md) owns output lifecycle guidance.

## Discovery and switching

The first nonempty explicit environment selection is authoritative. If that selected path is
missing, resolution fails before writing rather than trying a lower-priority location. When no
explicit selector is set, discovery continues to the sibling convention below; there is no home-directory location.
Clear stale higher-priority variables before switching:

1. `BUY_ME_A_CAR_DATA_DIR`: the exact `data` child of the PRIVATE companion.
2. `BUY_ME_A_CAR_CONFIG`: the companion root.
3. `BUY_ME_A_CAR_CONFIG_DIR`: companion-root alias.
4. A proven sibling `buy-me-a-car-config` discovered by pinned Guards.

All layouts use `<companion>/data`; a missing child does not move output to the root.
Initialize the separate PRIVATE companion, then point one selection at it. Writes are
checked by path only: the target must stay inside `<companion>/data`, outside this source
tree, without traversal, links that escape, `.git` components or nested repositories. The
runtime does not query repository visibility; PRIVATE publication is enforced at commit time
by the Guards hooks and CI.

To switch A to B in PowerShell:

```powershell
Remove-Item Env:BUY_ME_A_CAR_DATA_DIR -ErrorAction SilentlyContinue
Remove-Item Env:BUY_ME_A_CAR_CONFIG_DIR -ErrorAction SilentlyContinue
$env:BUY_ME_A_CAR_CONFIG = "<private-companion-B>"
python tools/runtime_paths.py --write
python tools/doctor.py --private
```

For POSIX shells, use `unset BUY_ME_A_CAR_DATA_DIR BUY_ME_A_CAR_CONFIG_DIR` and
`export BUY_ME_A_CAR_CONFIG="<private-companion-B>"`. The path command checks the destination
without writing a purchase record. The doctor reports local dependencies separately from the
companion location; neither command proves mailbox, scheduler, model, PDF or real purchase outcomes.

## Output ownership

Every output kind should have one active declaration in [storage.contract.json](storage.contract.json).
The runtime does not admit writes against the contract; it confines them to the companion by path
before creating output parents. Add a reviewed producer, schema, consumer and recovery rule before
introducing a new output kind.

Follow [DATA.md](DATA.md) when retaining or restoring historical evaluation receipts and
referenced inputs.
