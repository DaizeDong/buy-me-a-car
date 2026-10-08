"""Generated source-owned write and all-destination proof controls."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from unittest import TestCase
import test_runtime_paths


class ArtifactAdmissionTests(TestCase):
    setUp = test_runtime_paths.RuntimePathsTests.setUp
    def test_undeclared_output_is_refused_before_parent_creation(self):
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.data_path('new-kind/output.json', for_write=True)
        self.assertFalse((self.base / 'new-kind').exists())

    def test_retired_output_is_refused(self):
        with self.assertRaises(self.runtime.DataBoundaryError):
            self.runtime.data_path('diagnostics/output.json', for_write=True)

    def test_missing_data_child_stays_in_data_namespace(self):
        root = self.base.parent
        self.base.rmdir()
        with patch.object(self.runtime, '_guard_data_dir', return_value=root), patch.dict('os.environ', {}, clear=True):
            self.assertEqual(self.runtime.resolve_data_dir(required=True), root / 'data')
            target = self.runtime.data_path('cycles/example/report.json', for_write=True)
            self.assertEqual(target, root / 'data/cycles/example/report.json')
        self.assertFalse((root / 'cycles').exists())

    def test_public_effective_push_destination_is_rejected(self):
        self.proof.stop()
        root = self.base.parent
        proof = SimpleNamespace(root=str(root), repositories=('example/private', 'example/public'), signature='same')
        api = SimpleNamespace(prove_private_companion=lambda path: proof,
            read_private_companion_git=lambda *args: SimpleNamespace(returncode=0, stdout='a'*40))
        with patch.object(self.runtime, '_guard_module', return_value=api), patch.object(
                self.runtime, '_run', side_effect=lambda argv: 'false' if 'repos/example/public' in argv else 'true') as query:
            with self.assertRaises(self.runtime.DataBoundaryError):
                self.runtime._private_repo_identity(self.base)
        self.assertEqual(query.call_count, 2)

    def test_atomic_staging_is_authorized_before_creation(self):
        from skills.orchestrator.scripts import inbox_state
        target = self.base / 'inbox/state.json'
        target.parent.mkdir()
        target.write_text('synthetic retained state')
        calls = []
        def admit(path):
            calls.append(path)
            if path.name.startswith('.'):
                raise self.runtime.DataBoundaryError('synthetic ignored staging')
            return path
        with patch.object(inbox_state, '_authorize_file', side_effect=admit):
            with self.assertRaises(self.runtime.DataBoundaryError):
                inbox_state.atomic_write(target, {'schema_version': 1})
        self.assertEqual(target.read_text(), 'synthetic retained state')
        self.assertEqual(list(target.parent.iterdir()), [target])
        self.assertEqual(len(calls), 2)

    def test_capacity_scan_tolerates_staging_removed_during_enumeration(self):
        from tools import storage_retention as storage
        folder = self.base / 'research-runs'
        folder.mkdir()
        staging = folder / '.report.json-synthetic'
        staging.write_text('synthetic staging')
        original = Path.iterdir
        def entries(path):
            result = list(original(path))
            if path == folder:
                staging.unlink()
            return iter(result)
        with patch.object(Path, 'iterdir', entries):
            storage.enforce_capacity(self.base, 'research-runs/next.json', max_files=1)

    def test_retirement_scan_still_refuses_disappearing_inputs(self):
        from tools import storage_retention as storage
        folder = self.base / 'research-runs'
        folder.mkdir()
        staging = folder / '.report.json-synthetic'
        staging.write_text('synthetic staging')
        original = Path.iterdir
        def entries(path):
            result = list(original(path))
            if path == folder:
                staging.unlink()
            return iter(result)
        with patch.object(Path, 'iterdir', entries):
            with self.assertRaises(FileNotFoundError):
                storage.files_under(self.base, 'research-runs')

    def test_capacity_scan_tolerates_staging_removed_before_size_read(self):
        from tools import storage_retention as storage
        folder = self.base / 'research-runs'
        folder.mkdir()
        staging = folder / '.report.json-synthetic'
        staging.write_text('synthetic staging')
        original = storage.files_under
        def enumerated(root, relative, **kwargs):
            result = original(root, relative, **kwargs)
            if staging in result:
                staging.unlink()
            return result
        with patch.object(storage, 'files_under', enumerated):
            storage.enforce_capacity(self.base, 'research-runs/next.json', max_files=1)


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
