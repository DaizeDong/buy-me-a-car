#!/usr/bin/env python3
"""Report local readiness without contacting mail, scheduling, or model services.

Only --private requests live GitHub visibility proof through runtime_paths.
A detected browser/package is not a completed PDF or integration acceptance test.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _check(ident, status, detail, *, required=False):
    return {"id": ident, "status": status, "required": required, "detail": detail}


def _package(module):
    try:
        loaded = importlib.import_module(module)
    except ImportError:
        return "missing", "Install the package in this Python environment."
    except Exception as exc:
        return "blocked", f"Import failed: {type(exc).__name__}."
    return "pass", "Import succeeded; version " + str(getattr(loaded, "__version__", "unknown")) + "."


def _executable(name):
    executable = shutil.which(name)
    if not executable:
        return "missing", "Executable not found on PATH."
    kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=10, **kwargs)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "blocked", f"Version probe failed: {type(exc).__name__}."
    if result.returncode:
        return "blocked", "Version probe returned a nonzero exit code."
    return "pass", "Executable responds; authentication and provider access are not tested."


def _browser():
    path = ROOT / "skills/orchestrator/scripts/generate_dossier.py"
    spec = importlib.util.spec_from_file_location("bmac_doctor_dossier", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        browser, kind = module.find_chrome()
    except (OSError, ValueError, ImportError) as exc:
        return "blocked", f"Browser discovery failed: {type(exc).__name__}."
    if browser:
        return "found_not_exercised", "Chromium-family browser detected; PDF rendering was not exercised."
    return "missing", "Install Chrome, Edge or Chromium, or set CHROME_BIN to its executable."


def _registration(target):
    source_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(source_files) != 16:
        return "blocked", {"registered": 0, "expected": 16, "error": "bundled_skill_set_incomplete"}
    registered, missing, conflicts = [], [], []
    for source_file in source_files:
        source = source_file.parent.resolve()
        name = "buy-me-a-car" if source.name == "orchestrator" else source.name
        installed = target / name
        if not os.path.lexists(installed):
            missing.append(name)
        else:
            try:
                matches = installed.resolve() == source and (installed / "SKILL.md").is_file()
            except OSError:
                matches = False
            (registered if matches else conflicts).append(name)
    return "pass" if len(registered) == 16 else "blocked" if conflicts else "missing", {
        "registered": len(registered), "expected": 16, "missing": missing, "conflicts": conflicts,
        "scope": "filesystem registration only; host skill discovery not exercised",
    }


def diagnose(target=None, *, check_private=False):
    target = Path(target or Path.home() / ".agents/skills").expanduser()
    checks = [_check("python", "pass" if sys.version_info >= (3, 10) else "blocked",
                     f"Python {sys.version_info.major}.{sys.version_info.minor}; minimum 3.10.", required=True)]
    for name, module, required in [("pyyaml", "yaml", True), ("pypdf", "pypdf", False)]:
        checks.append(_check(name, *_package(module), required=required))
    for executable, required in [("git", True), ("gh", False)]:
        checks.append(_check(executable, *_executable(executable), required=required))
    for name, files in {
        "guards": ["tools/datadir.py", "tools/data_boundary.py", "tools/pii_guard.py"],
        "style": ["tools/dash_guard.py", "tools/load_budget.py"],
    }.items():
        populated = (ROOT / name / ".git").is_file() and all((ROOT / name / item).is_file() for item in files)
        checks.append(_check(f"submodule_{name}", "pass" if populated else "missing",
                             "Populated submodule files found." if populated else
                             "Run git submodule update --init --recursive.", required=True))
    registration, detail = _registration(target)
    checks.append(_check("skill_registration", registration, detail, required=True))
    checks.append(_check("browser", *_browser()))
    if check_private:
        from tools.runtime_paths import DataBoundaryError, resolve_data_dir
        try:
            private = resolve_data_dir(required=False)
            checks.append(_check("private_data", "pass" if private else "uninitialized",
                                 "Private companion visibility verified; no data written." if private else
                                 "Initialize a private companion before live writes.", required=True))
        except (DataBoundaryError, OSError) as exc:
            checks.append(_check("private_data", "blocked", f"Private boundary proof failed: {type(exc).__name__}.", required=True))
    else:
        checks.append(_check("private_data", "not_checked", "Use --private for live visibility proof; no private probe ran."))
    ready = all(item["status"] == "pass" for item in checks if item["required"])
    return {
        "schema_version": 1, "status": "ready" if ready else "needs_setup", "checks": checks,
        "integrations": {
            "mail_transport": "manual import/export adapter protocol available",
            "gmail": "not verified; requires an installed, authorized host adapter",
            "scheduler": "not verified; repository installs no background service",
            "model": "not called; use the opt-in eval for actual model evidence",
            "pdf": "not rendered; browser and pypdf discovery are readiness checks only",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="agent skill directory to inspect")
    parser.add_argument("--private", action="store_true", help="verify private companion visibility live")
    args = parser.parse_args(argv)
    report = diagnose(args.target, check_private=args.private)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
