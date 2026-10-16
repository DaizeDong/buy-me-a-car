"""Resolve real purchase output through the installed fleet_guards resolver, by path checks only.

No in-repository fallback is permitted. The runtime runs no git or gh subprocess
and does not query repository visibility; PRIVATE publication of the companion is
enforced at commit time by the .githooks shims.
"""
from __future__ import annotations

import argparse
import ntpath
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = 'buy-me-a-car'


class DataBoundaryError(RuntimeError):
    """A real output destination is not inside the private companion."""


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _guard_data_dir() -> Path | None:
    try:
        from fleet_guards.runtime import companion_resolver
    except ImportError as exc:
        raise ImportError('fleet_guards is not installed. Run: pip install -e "$(git config --get fleet.guards)"') from exc
    try:
        result = companion_resolver(source_root=REPO_ROOT).resolve_data_dir(SKILL)
    except (RuntimeError, OSError, ValueError) as exc:
        raise DataBoundaryError('The shared guard could not resolve the companion. Check BUY_ME_A_CAR_CONFIG and its origin.') from exc
    return Path(result).resolve() if result is not None else None


def _companion_root(directory: Path) -> Path:
    """The companion root that holds a DATA directory: separate from this source tree."""
    root = directory.parent if directory.name == 'data' else directory
    if _inside(root, REPO_ROOT) or _inside(REPO_ROOT, root):
        raise DataBoundaryError('DATA requires a separate PRIVATE companion.')
    return root


def resolve_data_dir(*, required: bool = False) -> Path | None:
    candidate = _guard_data_dir()
    if candidate is None:
        if required:
            raise DataBoundaryError('Uninitialized: clone a PRIVATE buy-me-a-car-config companion, create its data directory, and set BUY_ME_A_CAR_CONFIG.')
        return None
    candidate = candidate.resolve()
    if candidate.name != 'data':
        if os.environ.get('BUY_ME_A_CAR_DATA_DIR'):
            raise DataBoundaryError('BUY_ME_A_CAR_DATA_DIR must select the companion data child.')
        candidate = candidate / 'data'
    _companion_root(candidate)
    return candidate


def _relative_path(value: str | Path) -> Path:
    raw = str(value)
    normalized = raw.replace('\\', '/')
    parts = normalized.split('/')
    if (not raw or '\x00' in raw or ntpath.splitdrive(raw)[0]
            or normalized.startswith('/') or ':' in normalized
            or any(part.lower() in ('', '.', '..', '.git')
                   or part.endswith((' ', '.')) for part in parts)):
        raise DataBoundaryError('DATA path must be a nonempty relative path without traversal, drive, or .git components.')
    return Path(*parts)


def _checked_target(base: Path, relative: Path, *, for_write: bool, directory=False) -> Path:
    lexical = base / relative
    target = lexical.resolve()
    if not _inside(target, base):
        raise DataBoundaryError('DATA path escapes the private directory through a link or traversal.')
    node = base
    for part in relative.parts:
        node = node / part
        if os.path.lexists(node / '.git'):
            raise DataBoundaryError('DATA path enters a nested repository.')
    if for_write:
        if directory and target.is_file():
            raise DataBoundaryError('DATA directory destination is a file.')
        if not directory and target.is_dir():
            raise DataBoundaryError('DATA file destination is a directory.')
        from tools.storage_retention import enforce_capacity
        enforce_capacity(base, relative.as_posix())
        target.parent.mkdir(parents=True, exist_ok=True)
        # Recheck after directory creation before returning to a writer.
        if not _inside(lexical.resolve(), base):
            raise DataBoundaryError('DATA parent changed while resolving output.')
    return target


def data_path(relative: str | Path, *, for_write: bool = False, directory=False) -> Path | None:
    relative = _relative_path(relative)
    base = resolve_data_dir(required=for_write)
    if base is None:
        return None
    return _checked_target(base, relative, for_write=for_write, directory=directory)


def _expand_windows_short_path(path: Path) -> Path:
    """Expand 8.3 names without resolving junctions; preserve nonexistent tails."""
    if os.name != 'nt':
        return path
    import ctypes

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    get_long = kernel.GetLongPathNameW
    get_long.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
    get_long.restype = ctypes.c_uint
    buffer = ctypes.create_unicode_buffer(32768)
    candidate, suffix = path, []
    while True:
        length = get_long(str(candidate), buffer, len(buffer))
        if 0 < length < len(buffer):
            return Path(buffer.value).joinpath(*reversed(suffix))
        if (length or ctypes.get_last_error() not in (2, 3)
                or candidate.parent == candidate):
            raise DataBoundaryError('Cannot normalize Windows DATA path spelling.')
        suffix.append(candidate.name)
        candidate = candidate.parent


def validate_data_path(path: str | Path, *, for_write: bool = False, directory=False) -> Path:
    base = resolve_data_dir(required=True)
    supplied = Path(path).expanduser()
    if supplied.is_absolute():
        # Check original components before alias expansion can normalize spelling.
        _relative_path(Path(*supplied.parts[1:]))
        try:
            relative = _expand_windows_short_path(supplied).relative_to(base)
        except ValueError as exc:
            raise DataBoundaryError('Live input/output must be inside the private DATA directory.') from exc
    else:
        relative = supplied
    return _checked_target(base, _relative_path(relative), for_write=for_write, directory=directory)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('relative', nargs='?')
    parser.add_argument('--write', action='store_true', help='Require initialization and create validated output parents')
    args = parser.parse_args(argv)
    try:
        base = resolve_data_dir(required=args.write)
        if base is None:
            print('UNINITIALIZED: no private purchase data; initialize a private companion before writing.')
            return 0
        print(f'PRIVATE companion: {_companion_root(base)}', file=sys.stderr)
        print(data_path(args.relative, for_write=args.write) if args.relative else base)
        return 0
    except DataBoundaryError as exc:
        print(f'DATA boundary error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
