#!/usr/bin/env bash
# Shell entrypoint for the same validated dossier-to-PDF pipeline.
# Pass generator arguments, including --mode, --config, --output, --to-pdf.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys' >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1 && python -c 'import sys' >/dev/null 2>&1; then
    PYTHON=python
else
    echo 'Error: a working Python 3 interpreter is required' >&2
    exit 2
fi
exec "$PYTHON" "$SCRIPT_DIR/generate_dossier.py" "$@"
