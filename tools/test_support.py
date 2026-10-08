"""Synthetic PRIVATE metadata seam for algorithm tests; owner matching remains real."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def install_artifact_proof(test, runtime):
    original = runtime._guard_module
    storage = original('storage_contract')
    api = SimpleNamespace(
        prove_private_companion=lambda root, visibility_map=None: SimpleNamespace(
            root=str(root), repositories=('example/synthetic-private',), signature='synthetic'),
        read_private_companion_git=lambda proof, *args: SimpleNamespace(
            returncode=1 if args[0] == 'check-ignore' else 0, stdout='a'*40))
    def module(name):
        return storage if name == 'storage_contract' else original(name)
    for seam in (patch.object(storage, 'load_boundary', return_value=api),
                 patch.object(runtime, '_guard_module', side_effect=module)):
        seam.start()
        test.addCleanup(seam.stop)
