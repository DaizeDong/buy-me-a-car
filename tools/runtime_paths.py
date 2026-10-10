"""Resolve real purchase output through the pinned guard and prove it is private.

No in-repository or unversioned fallback is permitted. Visibility is checked
against GitHub on each resolution; unavailable or ambiguous proof is an error.
"""
from __future__ import annotations

import argparse
import importlib.util
import ntpath
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = 'buy-me-a-car'


class DataBoundaryError(RuntimeError):
    """A real output destination lacks a verifiable private boundary."""


_VISIBILITY_PREFIX = ['gh', 'api', '--hostname', 'github.com']
_VISIBILITY_SUFFIX = ['--jq', '.private']


def _run(command: list[str]) -> str:
    if (len(command) == 7 and list(command[:4]) == _VISIBILITY_PREFIX and list(command[5:]) == _VISIBILITY_SUFFIX
            and isinstance(command[4], str) and command[4].startswith('repos/')):
        return _github_private(command[4][len('repos/'):])
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='strict', timeout=20,
                                check=False)
    except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired) as exc:
        raise DataBoundaryError(f'Cannot verify private DATA destination: {command[0]} unavailable or failed.') from exc
    if result.returncode:
        # Do not echo command arguments, remote URLs or auth diagnostics.
        raise DataBoundaryError(f'Cannot verify private DATA destination: {command[0]} exited {result.returncode}.')
    return result.stdout.strip()


def _github_private(repository: str) -> str:
    """Live PRIVATE answer for OWNER/NAME, independent of the ACTIVE gh account.

    A plain `gh api repos/OWNER/NAME` asks only with whichever account `gh auth switch` last
    selected, so an active account that cannot see the companion failed every proof closed. The
    pinned guards kit asks with the owner's stored account, then every other stored account, then
    gh's default, and refuses only when none can see it. Returns 'true' only for PRIVATE."""
    api = _guard_module('data_boundary')
    ask = getattr(api, 'query_github_visibility', None)
    if not callable(ask):
        raise DataBoundaryError('Guards dependency lacks the account-independent visibility API.')
    try:
        visibility = ask(repository)
    except api.GitError as exc:
        raise DataBoundaryError('Cannot verify private DATA destination: no gh credential can see it.') from exc
    return 'true' if visibility == 'PRIVATE' else 'false'


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _guard_data_dir() -> Path | None:
    guard_path = REPO_ROOT / 'guards' / 'tools' / 'datadir.py'
    if not guard_path.is_file():
        raise DataBoundaryError('Missing guards submodule. Run git submodule update --init --recursive.')
    # An explicit broken pointer is an error, not permission to use a different
    # existing companion. Discovery itself remains owned by the pinned guard.
    for name in ('BUY_ME_A_CAR_DATA_DIR', 'BUY_ME_A_CAR_CONFIG', 'BUY_ME_A_CAR_CONFIG_DIR'):
        value = os.environ.get(name)
        if value:
            if not Path(value).expanduser().is_dir():
                raise DataBoundaryError(f'{name} does not name an existing private directory.')
            break
    spec = importlib.util.spec_from_file_location('_bmac_guard_datadir', guard_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        result = module.resolve_data_dir(SKILL, create=False)
    except (RuntimeError, OSError, ValueError) as exc:
        raise DataBoundaryError('The shared guard could not prove the companion. Check BUY_ME_A_CAR_CONFIG and its origin.') from exc
    return Path(result).resolve() if result is not None else None


def _github_repo(remote: str) -> str:
    if '://' in remote:
        parsed = urlsplit(remote)
        if parsed.scheme not in ('https', 'ssh') or parsed.password:
            raise DataBoundaryError('Only authenticated GitHub private repositories are supported for DATA.')
        host, path = parsed.hostname, parsed.path.lstrip('/')
    else:
        match = re.fullmatch(r'(?:[^@/:\s]+@)?([^/:\s]+):([^\s]+)', remote)
        if not match:
            raise DataBoundaryError('DATA origin is missing or is not a supported GitHub remote.')
        host, path = match.groups()
    if host != 'github.com':
        # Resolve SSH host aliases through their effective configuration, not a
        # hardcoded list of personal aliases. HTTP hosts cannot be SSH aliases.
        if remote.startswith('https://') or not re.fullmatch(r'[A-Za-z0-9_.-]+', host or ''):
            raise DataBoundaryError('Cannot verify visibility for a non-GitHub DATA origin.')
        config = _run(['ssh', '-G', host])
        hosts = [line.split(None, 1)[1].strip().lower() for line in config.splitlines()
                 if line.lower().startswith('hostname ')]
        if hosts != ['github.com']:
            raise DataBoundaryError('DATA SSH alias does not resolve to github.com.')
    path = path.removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', path):
        raise DataBoundaryError('DATA origin must identify exactly one GitHub owner/repository.')
    return path


def _existing_directory(path: Path) -> Path:
    candidate = path if path.is_dir() else path.parent
    while not candidate.exists() and candidate != candidate.parent:
        candidate = candidate.parent
    return candidate


def _guard_module(name):
    path = REPO_ROOT / 'guards' / 'tools' / (name + '.py')
    if not path.is_file():
        raise DataBoundaryError('Missing guards submodule; initialize it before accessing DATA.')
    key = '_bmac_guard_' + name
    spec = importlib.util.spec_from_file_location(key, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def _private_repo_identity(directory: Path) -> str:
    try:
        api = _guard_module('data_boundary')
        proof = api.prove_private_companion(_existing_directory(directory))
        root = Path(proof.root).resolve()
        if _inside(root, REPO_ROOT) or _inside(REPO_ROOT, root):
            raise DataBoundaryError('DATA requires a separate PRIVATE companion.')
        head = api.read_private_companion_git(proof, 'rev-parse', '--verify', 'HEAD')
        if head.returncode or not head.stdout.strip():
            raise DataBoundaryError('DATA companion must have committed history.')
        for identity in proof.repositories:
            if _run(['gh', 'api', '--hostname', 'github.com', f'repos/{identity}', '--jq', '.private']) != 'true':
                raise DataBoundaryError('DATA publication destination is public or unknown.')
        current = api.prove_private_companion(_existing_directory(directory))
        if (proof.root, proof.repositories, proof.signature) != (current.root, current.repositories, current.signature):
            raise DataBoundaryError('DATA publication destinations changed during proof.')
        return ', '.join(proof.repositories)
    except (OSError, ValueError, RuntimeError) as exc:
        raise DataBoundaryError('Cannot prove every PRIVATE DATA publication destination.') from exc


def _authorize_target(base: Path, relative: Path, *, directory=False) -> Path:
    try:
        receipt = _guard_module('storage_contract').authorize_artifact_write(
            REPO_ROOT, base.parent, 'data/' + relative.as_posix(), directory=directory)
        return Path(receipt.path)
    except (OSError, ValueError, RuntimeError) as exc:
        raise DataBoundaryError('Output lacks source-owned, versioned artifact authorization.') from exc


def resolve_data_dir(*, required: bool = False) -> Path | None:
    candidate = _guard_data_dir()
    if candidate is None:
        if required:
            raise DataBoundaryError('Uninitialized: clone a PRIVATE buy-me-a-car-config companion, create its data directory, and set BUY_ME_A_CAR_CONFIG. Authenticate gh to verify its visibility.')
        return None
    candidate = candidate.resolve()
    if candidate.name != 'data':
        if os.environ.get('BUY_ME_A_CAR_DATA_DIR'):
            raise DataBoundaryError('BUY_ME_A_CAR_DATA_DIR must select the companion data child.')
        candidate = candidate / 'data'
    if _inside(candidate, REPO_ROOT):
        raise DataBoundaryError('Real DATA cannot be stored inside the public tool repository.')
    _private_repo_identity(candidate)
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
    _private_repo_identity(_existing_directory(target))
    if for_write:
        if _authorize_target(base, relative, directory=directory) != target:
            raise DataBoundaryError("Artifact authority returned a different destination.")
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
            raise DataBoundaryError('Live input/output must be inside the proven private DATA directory.') from exc
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
        print(f'PRIVATE companion: {_private_repo_identity(base)}', file=sys.stderr)
        print(data_path(args.relative, for_write=args.write) if args.relative else base)
        return 0
    except DataBoundaryError as exc:
        print(f'DATA boundary error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
