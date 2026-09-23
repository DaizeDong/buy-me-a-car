"""Install all skills idempotently without replacing unrelated user files."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class InstallationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('bmac_install_test', ROOT / 'tools' / 'install.py')
        self.install = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.install)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / 'skills'

    def test_dry_run_does_not_create_directory(self):
        planned = self.install.install(self.target)
        self.assertEqual(len(planned), 16)
        self.assertFalse(self.target.exists())

    def test_apply_links_all_skills_and_is_idempotent(self):
        first = self.install.install(self.target, apply=True)
        self.assertEqual(len(first), 16)
        for item in first:
            destination = self.target / item['name']
            self.assertTrue((destination / 'SKILL.md').is_file())
            self.assertEqual(destination.resolve(), Path(item['source']).resolve())
        second = self.install.install(self.target, apply=True)
        self.assertTrue(all(item['status'] == 'already-installed' for item in second))

    def test_any_conflict_prevents_partial_install(self):
        conflict = self.target / 'state-fee-lookup'
        conflict.mkdir(parents=True)
        marker = conflict / 'user-note.txt'
        marker.write_text('Preserve this unrelated skill.', encoding='utf-8')
        with self.assertRaises(self.install.InstallationError):
            self.install.install(self.target, apply=True)
        self.assertEqual(list(self.target.iterdir()), [conflict])
        self.assertEqual(marker.read_text(encoding='utf-8'), 'Preserve this unrelated skill.')

    def test_broken_link_conflict_prevents_partial_install(self):
        source = Path(self.tmp.name) / 'unrelated'
        source.mkdir()
        self.target.mkdir()
        conflict = self.target / 'state-fee-lookup'
        self.install._link(source, conflict)
        source.rmdir()
        self.assertFalse(conflict.exists())
        with self.assertRaisesRegex(self.install.InstallationError, 'conflict'):
            self.install.install(self.target, apply=True)
        self.assertEqual(list(self.target.iterdir()), [conflict])

    def test_partial_failure_reports_created_links_without_removing_user_paths(self):
        original = self.install._link
        calls = []
        def fail_second(source, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError('synthetic link failure')
            return original(source, target)
        with patch.object(self.install, '_link', side_effect=fail_second):
            with self.assertRaisesRegex(self.install.InstallationError, 'partially'):
                self.install.install(self.target, apply=True)
        self.assertTrue(calls[0].is_dir())


if __name__ == '__main__':
    unittest.main()
