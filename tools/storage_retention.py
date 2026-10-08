"""Bound private generated storage and retire explicitly reviewed ordinary files.

Payloads are never printed. Unknown paths, links, core artifacts and changed plans
fail closed. The caller must stop writers before applying a retirement plan.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
MAX_FILES = 2000
MAX_BYTES = 128 * 1024 * 1024
MAX_RUNS = 32


def relative_name(value):
    if not isinstance(value, str):
        raise ValueError("Retention paths must be strings")
    parts = value.replace("\\", "/").split("/")
    if any(not p or p.casefold() in {".", "..", ".git"} or ":" in p or p.endswith((" ", ".")) for p in parts):
        raise ValueError("Retention path must stay inside DATA")
    return "/".join(parts)


def matches(name, pattern):
    parts, patterns = name.casefold().split("/"), pattern.casefold().split("/")
    def visit(i, j):
        if j == len(patterns):
            return i == len(parts)
        if patterns[j] == "**":
            return visit(i, j + 1) or (i < len(parts) and visit(i + 1, j))
        return i < len(parts) and fnmatch.fnmatchcase(parts[i], patterns[j]) and visit(i + 1, j + 1)
    return visit(0, 0)


def _resolved_for_comparison(path):
    resolved = path.resolve()
    # Windows can retain the extended prefix when a sibling staging file is
    # renamed during resolve. It does not change the resolved destination.
    name = str(resolved)
    if name.startswith("\\\\?\\UNC\\"):
        return Path("\\\\" + name[8:])
    if name.startswith("\\\\?\\"):
        return Path(name[4:])
    return resolved


def _require_single_link(info):
    if info.st_nlink == 0:
        raise FileNotFoundError("Retention entry disappeared during inspection")
    if info.st_nlink != 1:
        raise ValueError("Retention refuses multiply linked files")


def checked(root, relative):
    root = Path(root).absolute()
    path = root / relative_name(relative)
    for item in (*reversed(root.parents), root):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
            raise ValueError("Retention root cannot contain a link")
    current = root
    for component in (None, *path.relative_to(root).parts):
        if component is not None:
            current /= component
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
            raise ValueError("Retention refuses linked paths")
        if stat.S_ISREG(info.st_mode):
            _require_single_link(info)
    resolved = _resolved_for_comparison(path)
    if resolved.is_relative_to(_resolved_for_comparison(ROOT)):
        raise ValueError("Runtime DATA cannot be inside the public tool")
    if not resolved.is_relative_to(_resolved_for_comparison(root)):
        raise ValueError("Retention path escaped DATA")
    return path


def files_under(root, relative, *, allow_vanished=False):
    start = checked(root, relative)
    if not start.exists():
        return []
    if start.is_file():
        return [start]
    result, pending = [], [start]
    while pending:
        directory = pending.pop()
        try:
            entries = sorted(directory.iterdir())
        except FileNotFoundError:
            if allow_vanished:
                continue
            raise
        for entry in entries:
            try:
                path = checked(root, entry.relative_to(root).as_posix())
                info = path.lstat()
                if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
                    raise ValueError("Retention refuses linked paths")
                if stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    _require_single_link(info)
                    result.append(path)
                else:
                    raise ValueError("Unsupported retention entry")
            except FileNotFoundError:
                if allow_vanished:
                    continue
                raise
    return result


def contract_relative_name(name, contract):
    """Keep registry paths DATA-relative and compare companion-root patterns."""
    name = relative_name(name)
    return "data/" + name if contract.get("tool") == "buy-me-a-car" else name


def build_plan(root, registry, contract):
    root = Path(root).absolute()
    if registry.get("schema_version") != 1 or contract.get("schema_version") != 1:
        raise ValueError("Unsupported retention schema")
    protected = [relative_name(p).casefold() for p in registry["protected_paths"]]
    core = [a["path_pattern"] for a in contract["artifacts"] if a["retention_rule"]["class"] == "core"]
    result = {}
    for item in registry["retirements"]:
        if item.get("completed") is not True or item.get("dependencies_released") is not True or not item.get("reason"):
            raise ValueError("Retirement needs completed work and released dependencies")
        name = relative_name(item["path"])
        folded = name.casefold()
        if any(folded == p or p.startswith(folded + "/") or folded.startswith(p + "/") for p in protected):
            raise ValueError("Retirement overlaps a protected dependency")
        for path in files_under(root, name):
            rel = path.relative_to(root).as_posix()
            artifact_path = contract_relative_name(rel, contract)
            if any(matches(artifact_path, p) for p in core):
                raise ValueError("Retirement includes a core artifact")
            if not any(matches(artifact_path, a["path_pattern"]) for a in contract["artifacts"]
                       if a["retention_rule"]["class"] in {"retired", "rebuildable"}):
                raise ValueError("Retirement includes an unclassified artifact")
            raw = path.read_bytes()
            result[rel] = {"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return {"schema_version": 1, "files": [result[k] for k in sorted(result)],
            "file_count": len(result), "bytes": sum(v["bytes"] for v in result.values())}


def apply_plan(root, registry, contract, expected):
    current = build_plan(root, registry, contract)
    if current != expected:
        raise ValueError("Retirement plan changed; review it again")
    for row in current["files"]:
        path = checked(root, row["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("Retirement input changed")
        path.unlink()
    return {"removed_files": current["file_count"], "removed_bytes": current["bytes"]}


def enforce_capacity(root, relative, *, max_files=MAX_FILES, max_bytes=MAX_BYTES):
    """Refuse additional generated output at capacity; never evict core records."""
    root = Path(root).absolute()
    name = relative_name(relative)
    tool = json.loads((ROOT / "storage.contract.json").read_text(encoding="utf-8"))["tool"]
    if tool == "buy-me-a-car":
        areas = ("audits", "diagnostics", "eval/model-runs", "research-runs", "browser-sessions", "playwright-mcp", "scratch")
        if not any(name == a or name.startswith(a + "/") for a in areas):
            return
    else:
        areas = ("agent-work", "grader-work", "edgar-cache", "calibration")
        if name.startswith("targets/") and "/runs/" in name:
            run = "/".join(name.split("/")[:4])
            if checked(root, run).exists():
                return
            targets = checked(root, "targets")
            runs = []
            if targets.exists():
                for target in targets.iterdir():
                    directory = checked(root, target.relative_to(root).as_posix() + "/runs")
                    if directory.exists():
                        runs.extend(checked(root, p.relative_to(root).as_posix()) for p in directory.iterdir())
            if len(runs) >= MAX_RUNS:
                raise ValueError("Run capacity reached; retire completed runs with their dependency review first")
            return
        if not any(name == a or name.startswith(a + "/") for a in areas):
            return
    count = size = 0
    for area in areas:
        for path in files_under(root, area, allow_vanished=True):
            # Atomic replacements can remove staging files during this advisory scan.
            # Retirement plans use the strict default and still require stable inputs.
            try:
                info = path.lstat()
                if (not stat.S_ISREG(info.st_mode)
                        or getattr(info, "st_file_attributes", 0) & 1024):
                    raise ValueError("Unsupported retention entry")
                _require_single_link(info)
            except FileNotFoundError:
                continue
            count += 1
            size += info.st_size
            if count >= max_files or size >= max_bytes:
                raise ValueError("Generated storage capacity reached; review and apply storage retirement before writing")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    contract = json.loads((ROOT / "storage.contract.json").read_text(encoding="utf-8"))
    if contract["tool"] == "self-evolve":
        from tools.sie.runtime_data import private_root
        root = private_root()
    else:
        from tools.runtime_paths import resolve_data_dir
        root = resolve_data_dir(required=True)
    registry_path = checked(root, "retention.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    plan = build_plan(root, registry, contract)
    if args.apply:
        print(json.dumps(apply_plan(root, registry, contract, plan)))
    else:
        print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
