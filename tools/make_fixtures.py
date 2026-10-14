"""Regenerate public synthetic fixtures from code, never from real-run files."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECIPES = Path(__file__).resolve().parent / 'fixture_recipes'


def build() -> dict[str, bytes]:
    payloads = {}
    for path in sorted(RECIPES.glob('*.py')):
        if path.name.startswith('_'):
            continue
        spec = importlib.util.spec_from_file_location('fixture_recipe_' + path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for relative, payload in module.build().items():
            rel = Path(relative)
            if rel.is_absolute() or '..' in rel.parts or relative in payloads:
                raise ValueError(f'Invalid or duplicate fixture output: {relative}')
            if not isinstance(payload, bytes):
                raise TypeError(f'Fixture payload must be bytes: {relative}')
            payloads[relative] = payload
    if not payloads:
        raise ValueError('No fixture recipes loaded')
    return payloads


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='Write basenames to an isolated directory for the fleet guard')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    payloads = build()
    failures = []
    names = set()
    for relative, payload in payloads.items():
        if args.out:
            name = Path(relative).name
            if name in names:
                raise ValueError(f'Fixture basenames must be unique for guard compatibility: {name}')
            names.add(name)
            destination = args.out / name
        else:
            destination = ROOT / relative
        if args.check:
            if not destination.is_file() or destination.read_bytes().replace(b'\r\n', b'\n') != payload.replace(b'\r\n', b'\n'):
                failures.append(relative)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
    if failures:
        print('Fixture drift: ' + ', '.join(failures), file=sys.stderr)
        return 1
    print(f'{len(payloads)} synthetic fixtures ' + ('verified' if args.check else 'generated'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
