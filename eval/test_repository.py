"""Negative controls for DATA presence, even when untracked or ignored."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import check_repository


class RepositoryBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / '.dataclass.json').write_text(json.dumps({
            'data': ['cycles/', 'inbox/'], 'data_sealed': ['old_feedback.md'],
            'fixture': ['example.txt'],
        }), encoding='utf-8')
        (self.root / 'example.txt').write_bytes(b'SYNTHETIC\n')
        self.recipe = patch.object(check_repository, 'build', return_value={'example.txt': b'SYNTHETIC\n'})
        self.recipe.start()
        self.addCleanup(self.recipe.stop)

    def test_empty_tool_passes(self):
        self.assertEqual(check_repository.check(self.root), [])

    def test_ignored_private_file_still_fails(self):
        (self.root / '.gitignore').write_text('cycles/\n', encoding='utf-8')
        (self.root / 'cycles' / 'example').mkdir(parents=True)
        (self.root / 'cycles' / 'example' / 'criteria.md').write_text('synthetic observation', encoding='utf-8')
        self.assertTrue(any('criteria.md' in item for item in check_repository.check(self.root)))

    def test_sealed_path_fails_without_git_index(self):
        (self.root / 'old_feedback.md').write_text('synthetic', encoding='utf-8')
        self.assertTrue(any('old_feedback.md' in item for item in check_repository.check(self.root)))

    def test_case_variants_of_data_and_sealed_paths_fail(self):
        (self.root / 'INBOX').mkdir()
        (self.root / 'INBOX' / 'state.json').write_text('{}', encoding='utf-8')
        (self.root / 'OLD_FEEDBACK.MD').write_text('synthetic', encoding='utf-8')
        failures = check_repository.check(self.root)
        self.assertTrue(any('state.json' in item for item in failures))
        self.assertTrue(any('OLD_FEEDBACK.MD' in item for item in failures))

    def test_fixture_edit_and_missing_declaration_fail(self):
        (self.root / 'example.txt').write_text('changed', encoding='utf-8')
        self.assertTrue(any('fixture' in item.lower() for item in check_repository.check(self.root)))
        with patch.object(check_repository, 'build', return_value={'other.txt': b'SYNTHETIC\n'}):
            self.assertTrue(any('declarations' in item for item in check_repository.check(self.root)))

    def test_unreadable_subtree_cannot_be_reported_clean(self):
        import os
        blocked = self.root / 'documents'
        blocked.mkdir()
        original = os.scandir
        def scan(path):
            if Path(path) == blocked:
                raise PermissionError('synthetic unreadable subtree')
            return original(path)
        with patch('os.scandir', side_effect=scan):
            with self.assertRaises(PermissionError):
                check_repository.check(self.root)


if __name__ == '__main__':
    unittest.main()
