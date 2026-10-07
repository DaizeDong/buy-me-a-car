"""Retirement must preserve core data and reject stale or escaping selections."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.make_fixtures import retention_samples
from tools import storage_retention as storage


def setup_case(tmp_path):
    case = retention_samples()
    for name in ("core", "scratch"):
        path = tmp_path / case[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(case["content"])
    return case


def selected(case, path):
    registry = copy.deepcopy(case["registry"])
    registry["retirements"] = [{"path": path, "reason": "Synthetic completed review",
                                "completed": True, "dependencies_released": True}]
    return registry


class StorageRetentionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.case = setup_case(self.root)

    def test_core_cannot_be_retired_even_when_marked_complete(self):
        case = self.case
        with self.assertRaisesRegex(ValueError, "core"):
            storage.build_plan(self.root, selected(case, case["core"]), case["contract"])
        self.assertEqual((self.root / case["core"]).read_bytes(), case["content"])

    def test_companion_root_contract_preserves_data_relative_core(self):
        case = self.case
        with self.assertRaisesRegex(ValueError, "core"):
            storage.build_plan(self.root, selected(case, case["core"]), case["companion_contract"])
        self.assertEqual((self.root / case["core"]).read_bytes(), case["content"])

    def test_companion_root_contract_returns_data_relative_retirement(self):
        case = self.case
        plan = storage.build_plan(self.root, selected(case, case["scratch"]), case["companion_contract"])
        self.assertEqual([row["path"] for row in plan["files"]], [case["scratch"]])

    def test_source_contract_preserves_selected_capture_helper(self):
        case = self.case
        helper = self.root / case["capture_helper"]
        helper.parent.mkdir(parents=True, exist_ok=True)
        helper.write_bytes(case["content"])
        contract = json.loads((storage.ROOT / "storage.contract.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "core"):
            storage.build_plan(self.root, selected(case, case["capture_helper"]), contract)
        self.assertEqual(helper.read_bytes(), case["content"])

    def test_nested_development_rule_cannot_cover_other_data(self):
        case = self.case
        nested = self.root / case["nested_development"]
        nested.parent.mkdir(parents=True, exist_ok=True)
        nested.write_bytes(case["content"])
        plan = storage.build_plan(self.root, selected(case, case["nested_development"]), case["companion_contract"])
        self.assertEqual(plan["file_count"], 1)
        unrelated = "unclassified/synthetic.json"
        path = self.root / unrelated
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(case["content"])
        with self.assertRaisesRegex(ValueError, "unclassified"):
            storage.build_plan(self.root, selected(case, unrelated), case["companion_contract"])

    def test_protected_dependency_blocks_parent_retirement(self):
        case = self.case
        registry = selected(case, "diagnostics")
        registry["protected_paths"] = [case["scratch"]]
        with self.assertRaisesRegex(ValueError, "protected"):
            storage.build_plan(self.root, registry, case["contract"])
        self.assertTrue((self.root / case["scratch"]).exists())

    def test_changed_plan_fails_before_any_deletion(self):
        case = self.case
        registry = selected(case, case["scratch"])
        plan = storage.build_plan(self.root, registry, case["contract"])
        (self.root / case["scratch"]).write_bytes(case["changed"])
        with self.assertRaisesRegex(ValueError, "changed"):
            storage.apply_plan(self.root, registry, case["contract"], plan)
        self.assertEqual((self.root / case["scratch"]).read_bytes(), case["changed"])

    def test_only_reviewed_retired_bytes_are_removed(self):
        case = self.case
        registry = selected(case, case["scratch"])
        plan = storage.build_plan(self.root, registry, case["contract"])
        self.assertEqual(plan["files"][0]["sha256"], hashlib.sha256(case["content"]).hexdigest())
        self.assertEqual(storage.apply_plan(self.root, registry, case["contract"], plan)["removed_files"], 1)
        self.assertEqual((self.root / case["core"]).read_bytes(), case["content"])
        self.assertEqual(storage.build_plan(self.root, registry, case["contract"])["file_count"], 0)

    def test_unfinished_work_cannot_be_retired(self):
        case = self.case
        registry = selected(case, case["scratch"])
        registry["retirements"][0]["dependencies_released"] = False
        with self.assertRaisesRegex(ValueError, "dependencies"):
            storage.build_plan(self.root, registry, case["contract"])

    def test_link_metadata_blocks_retirement_before_reading(self):
        case = self.case
        path = self.root / case["scratch"]
        original = Path.lstat
        for marker in ("reparse", "hardlink"):
            def metadata(item):
                info = original(item)
                if item == path:
                    return SimpleNamespace(st_mode=info.st_mode,
                                           st_nlink=2 if marker == "hardlink" else 1,
                                           st_file_attributes=1024 if marker == "reparse" else 0)
                return info
            with self.subTest(marker=marker), patch.object(Path, "lstat", metadata):
                with self.assertRaisesRegex(ValueError, "link"):
                    storage.build_plan(self.root, selected(case, case["scratch"]), case["contract"])
            self.assertEqual(path.read_bytes(), case["content"])

    def test_capacity_stops_generated_admission_without_evicting_core(self):
        case = self.case
        with self.assertRaisesRegex(ValueError, "capacity"):
            storage.enforce_capacity(self.root, "diagnostics/next.json", max_files=1)
        storage.enforce_capacity(self.root, case["core"], max_files=1)
        self.assertEqual((self.root / case["core"]).read_bytes(), case["content"])

    def test_retirement_path_cannot_escape_data(self):
        for path in ("../outside", ".git/config", ".GIT/config", "x/../core", "/absolute", "x:stream"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                storage.relative_name(path)

    def test_glob_star_cannot_hide_an_extra_path_component(self):
        self.assertTrue(storage.matches("dossiers/case/report.pdf", "dossiers/*/*.pdf"))
        self.assertFalse(storage.matches("dossiers/case/old/report.pdf", "dossiers/*/*.pdf"))
