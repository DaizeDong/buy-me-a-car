"""Check the physical public DATA boundary and synthetic fixture declarations."""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.make_fixtures import build


def matches(relative: str, pattern: str) -> bool:
    relative, pattern = relative.casefold(), pattern.casefold().rstrip('/')
    return fnmatch.fnmatchcase(relative, pattern) or fnmatch.fnmatchcase(relative, pattern + '/*')


def check(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    manifest = json.loads((root / '.dataclass.json').read_text(encoding='utf-8'))
    failures = []
    prohibited = manifest.get('data', []) + manifest.get('data_sealed', [])
    if not prohibited or not manifest.get('data'):
        failures.append('DATA declarations are missing; runtime writers require explicit private paths.')
    def unreadable(error):
        raise error

    for directory, names, files in os.walk(root, followlinks=False, onerror=unreadable):
        current = Path(directory)
        # Submodules are separately pinned repositories, identified by shape.
        if current != root and (current / '.git').is_file():
            names[:] = []
            continue
        names[:] = [name for name in names if name not in {'.git', '__pycache__', '.pytest_cache', '.venv', 'venv'}]
        for name in names + files:
            path = current / name
            relative = path.relative_to(root).as_posix()
            if any(matches(relative, pattern) for pattern in prohibited):
                failures.append(f'DATA physically present in public tree: {relative}')
            try:
                path.resolve().relative_to(root)
            except ValueError:
                failures.append(f'Link exposes a path outside the public tree: {relative}')
    generated = build()
    if set(manifest.get('fixture', [])) != set(generated):
        failures.append('FIXTURE declarations do not match tools/make_fixtures.py outputs.')
    for relative, expected in generated.items():
        path = root / relative
        if not path.is_file() or path.read_bytes().replace(b'\r\n', b'\n') != expected.replace(b'\r\n', b'\n'):
            failures.append(f'Synthetic fixture missing or changed outside generator: {relative}')
    return failures


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        failures = check(args.repo)
    except (OSError, ValueError, TypeError) as exc:
        print(f'Repository check could not run: {type(exc).__name__}', file=sys.stderr)
        return 2
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('Public DATA paths physically absent; every declared synthetic fixture reproduced.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
