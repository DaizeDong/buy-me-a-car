"""Private output boundaries, including symlink and missing-proof cases."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class RuntimePathsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / 'private' / 'data'
        self.base.mkdir(parents=True)
        path = ROOT / 'tools' / 'runtime_paths.py'
        spec = importlib.util.spec_from_file_location('runtime_paths_under_test', path)
        self.runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.runtime)
        self.guard = patch.object(self.runtime, '_guard_data_dir', return_value=self.base)
        self.proof = patch.object(self.runtime, '_private_repo_identity', return_value='example-owner/example-private')
        self.guard.start()
        self.proof.start()
        self.addCleanup(self.guard.stop)
        self.addCleanup(self.proof.stop)

    def test_private_output_creates_only_validated_parents(self):
        target = self.runtime.data_path('cycles/example/feedback.json', for_write=True)
        self.assertEqual(target, self.base / 'cycles/example/feedback.json')
        self.assertTrue(target.parent.is_dir())
        self.assertFalse(target.exists())

    def test_uninitialized_read_is_empty_and_write_fails(self):
        with patch.object(self.runtime, '_guard_data_dir', return_value=None):
            self.assertIsNone(self.runtime.data_path('inbox/state.json'))
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.data_path('inbox/state.json', for_write=True)

    def test_tool_repo_rejected_even_if_visibility_claims_private(self):
        with patch.object(self.runtime, '_guard_data_dir', return_value=ROOT / 'data'):
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.data_path('live.json', for_write=True)

    def test_unknown_or_public_visibility_blocks_write(self):
        for value in ('public', 'unknown'):
            with self.subTest(value=value), patch.object(self.runtime, '_private_repo_identity', side_effect=self.runtime.DataBoundaryError(value)):
                with self.assertRaises(self.runtime.DataBoundaryError):
                    self.runtime.data_path('new/live.json', for_write=True)
                self.assertFalse((self.base / 'new').exists())

    def test_traversal_absolute_and_windows_stream_rejected(self):
        for value in ('../escape.json', '/outside.json', 'C:\\outside.json', 'a/../../escape.json', 'a:file.json', '.git/config', 'nested/.GIT/config', 'a/.. /escape.json', 'a\\..\\escape.json'):
            with self.subTest(value=value), self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.data_path(value, for_write=True)

    def test_absolute_output_must_stay_inside_private_data(self):
        target = self.base / 'exports' / 'report.html'
        self.assertEqual(self.runtime.validate_data_path(target, for_write=True), target)
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.validate_data_path(Path(self.tmp.name) / 'outside.html', for_write=True)

    def test_symlink_escape_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        link = self.base / 'linked'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            if __import__('os').name != 'nt':
                self.skipTest('symlink creation unavailable')
            import _winapi
            _winapi.CreateJunction(str(outside), str(link))
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.data_path('linked/private.json', for_write=True)
        self.assertFalse((outside / 'private.json').exists())

    def test_no_origin_or_no_gh_proof_is_not_private(self):
        with patch.object(self.runtime, '_guard_data_dir', return_value=self.base):
            self.proof.stop()
            with patch.object(self.runtime, '_run', side_effect=self.runtime.DataBoundaryError('no origin')):
                with self.assertRaises(self.runtime.DataBoundaryError):
                    self.runtime.resolve_data_dir(required=True)

    def test_remote_identity_accepts_github_and_proved_ssh_alias(self):
        for remote in ('https://github.com/example-owner/private.git', 'git@github.com:example-owner/private.git'):
            self.assertEqual(self.runtime._github_repo(remote), 'example-owner/private')
        with patch.object(self.runtime, '_run', return_value='hostname github.com\nuser git') as run:
            self.assertEqual(self.runtime._github_repo('git@example-alias:example-owner/private.git'), 'example-owner/private')
            run.assert_called_once_with(['ssh', '-G', 'example-alias'])

    def test_unproved_and_malformed_origins_fail(self):
        for remote in ('https://example.com/owner/repo.git', 'file:///private', 'owner/repo',
                       'https://github.com/owner/repo/extra', 'https://u:secret@example.com/owner/repo'):
            with self.subTest(remote=remote), self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime._github_repo(remote)
        with patch.object(self.runtime, '_run', return_value='hostname example.com'):
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime._github_repo('git@example-alias:owner/repo')

    def test_actual_nested_git_origin_is_checked_before_write(self):
        import subprocess
        nested = self.base / 'nested'
        nested.mkdir()
        subprocess.run(['git', 'init', '-q', str(nested)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(nested), 'remote', 'add', 'origin',
                        'https://github.com/example-owner/public.git'], check=True, capture_output=True)
        self.proof.stop()
        original = self.runtime._run
        def run(command):
            if command[0] == 'gh':
                return 'false'
            return original(command)
        with patch.object(self.runtime, '_run', side_effect=run):
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime._checked_target(self.base, Path('nested/record.json'), for_write=True)
        self.assertFalse((nested / 'record.json').exists())

    def test_explicit_missing_env_pointer_does_not_fall_back(self):
        self.guard.stop()
        with patch.dict('os.environ', {'BUY_ME_A_CAR_DATA_DIR': str(self.base / 'missing')}):
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime._guard_data_dir()


if __name__ == '__main__':
    unittest.main()
