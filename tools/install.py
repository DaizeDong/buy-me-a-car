"""Register all bundled skills in an agent skill directory without overwriting it."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


class InstallationError(RuntimeError):
    pass


def _link(source: Path, target: Path):
    try:
        target.symlink_to(source, target_is_directory=True)
    except OSError:
        if os.name != 'nt':
            raise
        import _winapi
        _winapi.CreateJunction(str(source), str(target))


def install(destination: Path, *, apply: bool = False) -> list[dict]:
    destination = Path(destination).expanduser().absolute()
    sources = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    if len(sources) != 16:
        raise InstallationError('Expected all 16 bundled skill directories; installation is incomplete.')
    planned = []
    conflicts = []
    for skill in sources:
        source = skill.parent.resolve()
        name = 'buy-me-a-car' if source.name == 'orchestrator' else source.name
        target = destination / name
        present = os.path.lexists(target)
        if present and target.resolve() != source:
            conflicts.append(name)
        planned.append({'name': name, 'source': str(source),
                        'status': 'already-installed' if present else 'create-link'})
    if conflicts:
        raise InstallationError('Existing unrelated skills conflict: ' + ', '.join(conflicts) + '. Nothing changed; choose another target or resolve these names manually.')
    if apply:
        destination.mkdir(parents=True, exist_ok=True)
        created = []
        for item in planned:
            if item['status'] == 'already-installed':
                continue
            try:
                _link(Path(item['source']), destination / item['name'])
            except OSError as exc:
                raise InstallationError('Installation partially applied; created links: ' + ', '.join(created) + '. Existing files were preserved. Resolve the link error and rerun idempotently.') from exc
            created.append(item['name'])
            item['status'] = 'installed'
    return planned


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path.home() / '.agents' / 'skills')
    parser.add_argument('--apply', action='store_true', help='Create missing links after complete conflict preflight')
    args = parser.parse_args(argv)
    try:
        result = install(args.target, apply=args.apply)
        print(json.dumps({'applied': args.apply, 'skills': result}, indent=2))
        return 0
    except InstallationError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
