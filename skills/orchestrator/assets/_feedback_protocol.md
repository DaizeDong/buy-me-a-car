# Post-cycle feedback protocol

Record feedback at cycle close, abort, material pivot, or a rule violation. Resolve the private DATA directory with `tools/runtime_paths.py` first, then use `cycles/<cycle-id>/feedback/<event-id>.md` beneath it. The public `feedback_template.md` is a blank shape to copy; it is never the destination.

If the companion is missing, a read-only status check reports uninitialized. Recording feedback is a write and must fail with initialization guidance. Keep real observations in the private companion Git repository so its version history and normal backup workflow preserve them. Do not fall back to a public asset, repository-relative scratch directory, or an unversioned home directory.

Use a stable event ID so re-entering a session does not append the same observation twice. Preserve earlier events and link corrections. Record the affected phase, expected and observed behavior, private source artifact, and measured impact. Mark missing evidence or unknown impact explicitly.

When improving the public tool, reproduce the mechanism with generated synthetic inputs in `tools/fixture_recipes/`. Publish the generalized bug and correction only. Never quote an actual buyer message, price history, contact, inventory selection, or private infrastructure detail in the fixture or changelog.
