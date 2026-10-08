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
