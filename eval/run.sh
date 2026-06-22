#!/usr/bin/env bash
# Run every eval/test_*.py with the stdlib unittest runner.
# Exits non-zero if ANY test fails or errors. No third-party deps (no pytest).
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/.." && pwd)"

# Pick a Python 3 interpreter.
PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; then
      PY="$cand"; break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "ERROR: no Python 3 interpreter found on PATH" >&2
  exit 2
fi

echo "Using interpreter: $($PY --version 2>&1) ($(command -v "$PY"))"
echo "Repo root: $REPO_ROOT"

status=0
shopt -s nullglob
tests=("$HERE"/test_*.py)
if [ ${#tests[@]} -eq 0 ]; then
  echo "ERROR: no test_*.py found in $HERE" >&2
  exit 2
fi

for t in "${tests[@]}"; do
  name="$(basename "$t")"
  echo ""
  echo "=================================================================="
  echo "RUN $name"
  echo "=================================================================="
  if ! "$PY" "$t"; then
    echo "FAILED: $name"
    status=1
  fi
done

echo ""
if [ "$status" -eq 0 ]; then
  echo "ALL EVAL TESTS PASSED"
else
  echo "EVAL FAILURES PRESENT (see above)"
fi
exit "$status"
