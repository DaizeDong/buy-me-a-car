"""Generated storage regression cases, containing no real runtime observations."""

def build():
    return {'eval/test_fleet_storage.py': b'"""Generated source-owned write and all-destination proof controls."""\nfrom pathlib import Path\nfrom types import SimpleNamespace\nfrom unittest.mock import patch\nfrom unittest import TestCase\nimport test_runtime_paths\n\n\nclass ArtifactAdmissionTests(TestCase):\n    setUp = test_runtime_paths.RuntimePathsTests.setUp\n    def test_undeclared_output_is_refused_before_parent_creation(self):\n        with self.assertRaises(self.runtime.DataBoundaryError):\n            self.runtime.data_path(\'new-kind/output.json\', for_write=True)\n        self.assertFalse((self.base / \'new-kind\').exists())\n\n    def test_retired_output_is_refused(self):\n        with self.assertRaises(self.runtime.DataBoundaryError):\n            self.runtime.data_path(\'diagnostics/output.json\', for_write=True)\n\n    def test_missing_data_child_stays_in_data_namespace(self):\n        root = self.base.parent\n        self.base.rmdir()\n        with patch.object(self.runtime, \'_guard_data_dir\', return_value=root), patch.dict(\'os.environ\', {}, clear=True):\n            self.assertEqual(self.runtime.resolve_data_dir(required=True), root / \'data\')\n            target = self.runtime.data_path(\'cycles/example/report.json\', for_write=True)\n            self.assertEqual(target, root / \'data/cycles/example/report.json\')\n        self.assertFalse((root / \'cycles\').exists())\n\n    def test_public_effective_push_destination_is_rejected(self):\n        self.proof.stop()\n        root = self.base.parent\n        proof = SimpleNamespace(root=str(root), repositories=(\'example/private\', \'example/public\'), signature=\'same\')\n        api = SimpleNamespace(prove_private_companion=lambda path: proof,\n            read_private_companion_git=lambda *args: SimpleNamespace(returncode=0, stdout=\'a\'*40))\n        with patch.object(self.runtime, \'_guard_module\', return_value=api), patch.object(\n                self.runtime, \'_run\', side_effect=lambda argv: \'false\' if \'repos/example/public\' in argv else \'true\') as query:\n            with self.assertRaises(self.runtime.DataBoundaryError):\n                self.runtime._private_repo_identity(self.base)\n        self.assertEqual(query.call_count, 2)\n\n    def test_atomic_staging_is_authorized_before_creation(self):\n        from skills.orchestrator.scripts import inbox_state\n        target = self.base / \'inbox/state.json\'\n        target.parent.mkdir()\n        target.write_text(\'synthetic retained state\')\n        calls = []\n        def admit(path):\n            calls.append(path)\n            if path.name.startswith(\'.\'):\n                raise self.runtime.DataBoundaryError(\'synthetic ignored staging\')\n            return path\n        with patch.object(inbox_state, \'_authorize_file\', side_effect=admit):\n            with self.assertRaises(self.runtime.DataBoundaryError):\n                inbox_state.atomic_write(target, {\'schema_version\': 1})\n        self.assertEqual(target.read_text(), \'synthetic retained state\')\n        self.assertEqual(list(target.parent.iterdir()), [target])\n        self.assertEqual(len(calls), 2)\n\n    def test_capacity_scan_tolerates_staging_removed_during_enumeration(self):\n        from tools import storage_retention as storage\n        folder = self.base / \'research-runs\'\n        folder.mkdir()\n        staging = folder / \'.report.json-synthetic\'\n        staging.write_text(\'synthetic staging\')\n        original = Path.iterdir\n        def entries(path):\n            result = list(original(path))\n            if path == folder:\n                staging.unlink()\n            return iter(result)\n        with patch.object(Path, \'iterdir\', entries):\n            storage.enforce_capacity(self.base, \'research-runs/next.json\', max_files=1)\n\n    def test_retirement_scan_still_refuses_disappearing_inputs(self):\n        from tools import storage_retention as storage\n        folder = self.base / \'research-runs\'\n        folder.mkdir()\n        staging = folder / \'.report.json-synthetic\'\n        staging.write_text(\'synthetic staging\')\n        original = Path.iterdir\n        def entries(path):\n            result = list(original(path))\n            if path == folder:\n                staging.unlink()\n            return iter(result)\n        with patch.object(Path, \'iterdir\', entries):\n            with self.assertRaises(FileNotFoundError):\n                storage.files_under(self.base, \'research-runs\')\n\n    def test_capacity_scan_tolerates_staging_removed_before_size_read(self):\n        from tools import storage_retention as storage\n        folder = self.base / \'research-runs\'\n        folder.mkdir()\n        staging = folder / \'.report.json-synthetic\'\n        staging.write_text(\'synthetic staging\')\n        original = storage.files_under\n        def enumerated(root, relative, **kwargs):\n            result = original(root, relative, **kwargs)\n            if staging in result:\n                staging.unlink()\n            return result\n        with patch.object(storage, \'files_under\', enumerated):\n            storage.enforce_capacity(self.base, \'research-runs/next.json\', max_files=1)\n' + ATOMIC_REPLACE_TESTS.encode()}


ATOMIC_REPLACE_TESTS = r"""

class AtomicReplaceTests(TestCase):
    def setUp(self):
        from skills.orchestrator.scripts import inbox_state
        test_runtime_paths.RuntimePathsTests.setUp(self)
        seam = patch.object(inbox_state, 'validate_data_path', side_effect=self.runtime.validate_data_path)
        seam.start()
        self.addCleanup(seam.stop)

    def test_atomic_replace_recovers_from_windows_metadata_readers(self):
        import json
        from skills.orchestrator.scripts import inbox_state
        target = self.base / 'inbox/state.json'
        target.parent.mkdir()
        original_replace = inbox_state.os.replace
        for code in (5, 32):
            with self.subTest(winerror=code):
                target.write_text('synthetic retained state')
                error = PermissionError('synthetic Windows reader contention')
                error.winerror = code
                staged = []
                def replace(source, destination):
                    self.assertEqual(destination.read_text(), 'synthetic retained state')
                    staged.append((source, source.read_bytes()))
                    if len(staged) == 1:
                        raise error
                    return original_replace(source, destination)
                with patch.object(inbox_state.os, 'replace', side_effect=replace):
                    try:
                        inbox_state.atomic_write(target, {'revision': 2})
                    except PermissionError:
                        self.fail('Transient Windows reader contention must not discard the completed state')
                self.assertEqual(json.loads(target.read_text()), {'revision': 2})
                self.assertEqual(staged[0], staged[1])
                self.assertEqual(list(target.parent.iterdir()), [target])

    def test_atomic_replace_exhaustion_preserves_previous_state(self):
        from skills.orchestrator.scripts import inbox_state
        target = self.base / 'inbox/state.json'
        target.parent.mkdir()
        target.write_text('synthetic retained state')
        error = PermissionError('synthetic permanent Windows denial')
        error.winerror = 5
        with patch.object(inbox_state.os, 'replace', side_effect=error) as replace:
            with self.assertRaises(PermissionError) as caught:
                inbox_state.atomic_write(target, {'revision': 2})
        self.assertIs(caught.exception, error)
        self.assertEqual(replace.call_count, 6)
        self.assertEqual(target.read_text(), 'synthetic retained state')
        self.assertEqual(list(target.parent.iterdir()), [target])

    def test_atomic_replace_does_not_retry_other_permission_failures(self):
        from skills.orchestrator.scripts import inbox_state
        target = self.base / 'inbox/state.json'
        target.parent.mkdir()
        for code in (None, 87):
            with self.subTest(winerror=code):
                target.write_text('synthetic retained state')
                error = PermissionError('synthetic unrelated denial')
                if code is not None:
                    error.winerror = code
                with patch.object(inbox_state.os, 'replace', side_effect=error) as replace:
                    with self.assertRaises(PermissionError) as caught:
                        inbox_state.atomic_write(target, {'revision': 2})
                self.assertIs(caught.exception, error)
                self.assertEqual(replace.call_count, 1)
                self.assertEqual(target.read_text(), 'synthetic retained state')
                self.assertEqual(list(target.parent.iterdir()), [target])

    def test_atomic_replace_reauthorizes_before_retry(self):
        from skills.orchestrator.scripts import inbox_state
        target = self.base / 'inbox/state.json'
        target.parent.mkdir()
        target.write_text('synthetic retained state')
        error = PermissionError('synthetic Windows reader contention')
        error.winerror = 32
        original_authorize = inbox_state._authorize_file
        attempts = []
        def replace(source, destination):
            attempts.append(source)
            raise error
        def authorize(path):
            if attempts:
                raise self.runtime.DataBoundaryError('synthetic authorization revoked')
            return original_authorize(path)
        with patch.object(inbox_state.os, 'replace', side_effect=replace), patch.object(
                inbox_state, '_authorize_file', side_effect=authorize):
            with self.assertRaisesRegex(self.runtime.DataBoundaryError, 'authorization revoked'):
                inbox_state.atomic_write(target, {'revision': 2})
        self.assertEqual(len(attempts), 1)
        self.assertEqual(target.read_text(), 'synthetic retained state')
        self.assertEqual(list(target.parent.iterdir()), [target])


class ResolvedPathComparisonTests(TestCase):
    setUp = test_runtime_paths.RuntimePathsTests.setUp

    def test_capacity_scan_counts_staging_with_extended_resolved_prefix(self):
        from tools import storage_retention as storage
        folder = self.base / 'research-runs'
        folder.mkdir()
        staging = folder / '.report.json-synthetic'
        staging.write_text('synthetic staging')
        original = Path.resolve
        def resolve(path, *args, **kwargs):
            resolved = original(path, *args, **kwargs)
            return Path('\\\\?\\' + str(resolved)) if path == staging else resolved
        with patch.object(Path, 'resolve', resolve):
            with self.assertRaisesRegex(ValueError, 'Generated storage capacity reached'):
                storage.enforce_capacity(self.base, 'research-runs/next.json', max_files=1)
        self.assertEqual(staging.read_text(), 'synthetic staging')

    def test_extended_resolved_prefix_cannot_hide_a_real_escape(self):
        from tools import storage_retention as storage
        target = self.base / 'research-runs' / 'output.json'
        original = Path.resolve
        def resolve(path, *args, **kwargs):
            if path == target:
                return Path('\\\\?\\' + str(self.base.parent / 'outside.json'))
            return original(path, *args, **kwargs)
        with patch.object(Path, 'resolve', resolve):
            with self.assertRaisesRegex(ValueError, 'Retention path escaped DATA'):
                storage.checked(self.base, 'research-runs/output.json')
        self.assertFalse(target.exists())
"""
