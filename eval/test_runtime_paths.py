"""Private output boundaries by path: symlinks, traversal, nested repositories and the tool repo."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class RuntimePathsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve() / 'private' / 'data'
        self.base.mkdir(parents=True)
        path = ROOT / 'tools' / 'runtime_paths.py'
        spec = importlib.util.spec_from_file_location('runtime_paths_under_test', path)
        self.runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.runtime)
        self.guard = patch.object(self.runtime, '_guard_data_dir', return_value=self.base)
        self.guard.start()
        self.addCleanup(self.guard.stop)

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

    def test_tool_repo_rejected(self):
        with patch.object(self.runtime, '_guard_data_dir', return_value=ROOT / 'data'):
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.data_path('live.json', for_write=True)

    def test_traversal_absolute_and_windows_stream_rejected(self):
        for value in ('../escape.json', '/outside.json', 'C:\\outside.json', 'a/../../escape.json', 'a:file.json', '.git/config', 'nested/.GIT/config', 'a/.. /escape.json', 'a\\..\\escape.json'):
            with self.subTest(value=value), self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.data_path(value, for_write=True)

    def test_absolute_output_must_stay_inside_private_data(self):
        target = self.base / 'cycles/example' / 'report.html'
        self.assertEqual(self.runtime.validate_data_path(target, for_write=True), target)
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.validate_data_path(Path(self.tmp.name) / 'outside.html', for_write=True)

    def test_absolute_paths_reject_unsafe_components_before_normalization(self):
        for suffix in ('exports/../report.html', '.git/../report.html', '.GIT/config',
                       'nested./report.html', 'nested /report.html', 'report.html:stream'):
            with self.subTest(suffix=suffix), self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime.validate_data_path(self.base / suffix, for_write=True)
        self.assertFalse((self.base / 'report.html').exists())

    @unittest.skipUnless(os.name == 'nt', 'Windows short-name aliases require Windows')
    def test_windows_short_alias_accepts_missing_outputs_but_rejects_escapes(self):
        import ctypes
        import _winapi

        ancestor = Path(self.tmp.name).resolve() / 'Long Alias Parent'
        base = ancestor / 'private' / 'data'
        base.mkdir(parents=True)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        get_short = kernel.GetShortPathNameW
        get_short.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
        get_short.restype = ctypes.c_uint
        buffer = ctypes.create_unicode_buffer(32768)
        length = get_short(str(ancestor), buffer, len(buffer))
        if not length or length >= len(buffer):
            raise ctypes.WinError(ctypes.get_last_error())
        alias = Path(buffer.value) / 'private' / 'data'
        if alias == base:
            self.skipTest('Filesystem does not expose a distinct Windows short-name alias')
        self.assertEqual(alias.resolve(), base)
        with patch.object(self.runtime, '_guard_data_dir', return_value=base):
            output = self.runtime.validate_data_path(alias / 'cycles/example' / 'report.html', for_write=True)
            self.assertEqual(output, base / 'cycles/example' / 'report.html')
            self.assertTrue(output.parent.is_dir())
            self.assertFalse(output.exists())
            outside = ancestor / 'outside'
            outside.mkdir()
            _winapi.CreateJunction(str(outside), str(base / 'linked'))
            for path in (alias / 'linked' / 'escape.json', alias / 'cycles/example' / '..' / 'report.html'):
                with self.subTest(path=path), self.assertRaises(self.runtime.DataBoundaryError):
                    self.runtime.validate_data_path(path, for_write=True)
            self.assertFalse((outside / 'escape.json').exists())

    def test_external_link_into_private_data_is_still_rejected(self):
        link = Path(self.tmp.name).resolve() / 'external-link'
        try:
            link.symlink_to(self.base, target_is_directory=True)
        except OSError:
            if os.name != 'nt':
                self.skipTest('symlink creation unavailable')
            import _winapi
            _winapi.CreateJunction(str(self.base), str(link))
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.validate_data_path(link / 'cycles/example' / 'report.html', for_write=True)
        self.assertFalse((self.base / 'cycles/example').exists())

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

    def test_nested_repository_is_refused_before_write(self):
        import subprocess
        nested = self.base / 'nested'
        nested.mkdir()
        subprocess.run(['git', 'init', '-q', str(nested)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(nested), 'remote', 'add', 'origin',
                        'https://github.com/example-owner/public.git'], check=True, capture_output=True)
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
