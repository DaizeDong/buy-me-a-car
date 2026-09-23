"""Readiness reporting must distinguish installed files from live integrations."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import doctor, runtime_paths


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "skills"
        self.dependencies = patch.multiple(
            doctor, _package=lambda name: ("pass", "synthetic import proof"),
            _executable=lambda name: ("pass", "synthetic executable proof"),
            _browser=lambda: ("found_not_exercised", "synthetic browser discovery"),
        )
        self.dependencies.start()
        self.addCleanup(self.dependencies.stop)

    def test_missing_registration_is_not_ready_and_probe_does_not_create_paths(self):
        with patch.object(runtime_paths, "resolve_data_dir", side_effect=AssertionError("private probe forbidden")):
            report = doctor.diagnose(self.target)
        self.assertEqual(report["status"], "needs_setup")
        self.assertFalse(self.target.exists())
        registration = next(item for item in report["checks"] if item["id"] == "skill_registration")
        self.assertEqual(registration["detail"]["registered"], 0)
        self.assertEqual(registration["detail"]["expected"], 16)
        self.assertIn("not verified", report["integrations"]["gmail"])
        self.assertIn("not verified", report["integrations"]["scheduler"])
        self.assertIn("not called", report["integrations"]["model"])

    def test_all_registered_is_ready_without_optional_browser_or_pdf(self):
        from tools.install import install
        install(self.target, apply=True)
        with patch.object(doctor, "_browser", return_value=("missing", "no browser")), \
             patch.object(doctor, "_package", side_effect=lambda name: ("missing", "no parser") if name == "pypdf" else ("pass", "imported")):
            report = doctor.diagnose(self.target)
        self.assertEqual(report["status"], "ready")
        self.assertIn("not rendered", report["integrations"]["pdf"])

    def test_explicit_private_probe_reports_missing_and_unknown_separately(self):
        with patch.object(runtime_paths, "resolve_data_dir", return_value=None):
            report = doctor.diagnose(self.target, check_private=True)
        self.assertEqual(next(item for item in report["checks"] if item["id"] == "private_data")["status"], "uninitialized")
        with patch.object(runtime_paths, "resolve_data_dir", side_effect=runtime_paths.DataBoundaryError("synthetic unknown proof")):
            report = doctor.diagnose(self.target, check_private=True)
        self.assertEqual(next(item for item in report["checks"] if item["id"] == "private_data")["status"], "blocked")

    def test_registration_conflicts_are_not_counted_as_installed(self):
        unrelated = self.target / "buy-me-a-car"
        unrelated.mkdir(parents=True)
        (unrelated / "SKILL.md").write_text("Synthetic unrelated skill.", encoding="utf-8")
        status, detail = doctor._registration(self.target)
        self.assertEqual(status, "blocked")
        self.assertEqual(detail["conflicts"], ["buy-me-a-car"])
        self.assertEqual(detail["registered"], 0)


if __name__ == "__main__":
    unittest.main()
