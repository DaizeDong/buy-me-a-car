"""The live PRIVATE check must not depend on which gh account is ACTIVE.

A plain `gh api repos/OWNER/NAME --jq .private` asks only with the account `gh auth switch` last
selected. When another session switched it to an account that cannot see the companion, every
proof failed closed. The query now goes through the pinned guards kit, which asks every stored gh
account. These tests run the REAL kit against a synthetic gh (the kit's own fixture generator)
whose active account cannot see the repository; nothing here touches the real gh.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'example-owner/example-private'
ARGV = ['gh', 'api', '--hostname', 'github.com', 'repos/' + REPOSITORY, '--jq', '.private']


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnyAccountVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.runtime = _load('runtime_paths_visibility_under_test', ROOT / 'tools' / 'runtime_paths.py')
        self.fixtures = _load('_bmac_guard_make_fixtures', ROOT / 'guards' / 'tools' / 'make_fixtures.py')

    def _switched_gh(self, visibility, *, sees=None, name='gh'):
        root = Path(self.tmp.name) / name
        stub = self.fixtures.make_gh_cli_stub(
            root, accounts=['example-owner', 'other-account'], active='other-account',
            sees={'example-owner': [REPOSITORY]} if sees is None else sees,
            visibility={REPOSITORY: visibility})
        environment = {key: value for key, value in os.environ.items()
                       if key.upper() not in {'GH_TOKEN', 'GITHUB_TOKEN', 'GH_HOST', 'GH_ENTERPRISE_TOKEN'}}
        environment['PATH'] = str(stub['bin'])
        patcher = patch.dict('os.environ', environment, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        return stub

    def test_switched_active_account_still_proves_private(self):
        stub = self._switched_gh('PRIVATE')
        self.assertEqual(self.runtime._run(list(ARGV)), 'true')
        calls = self.fixtures.gh_stub_calls(stub)
        self.assertFalse([call for call in calls if call['argv'][:2] == ['auth', 'switch']])
        self.assertEqual([call['credential'] for call in calls if call['argv'][:2] == ['repo', 'view']],
                         ['example-owner'])

    def test_public_repository_is_never_reported_private(self):
        for visibility in ('PUBLIC', 'INTERNAL'):
            with self.subTest(visibility=visibility):
                self._switched_gh(visibility, name='gh-' + visibility)
                self.assertEqual(self.runtime._run(list(ARGV)), 'false')

    def test_plain_active_account_query_is_the_incident(self):
        """Negative control: the stub's active account cannot see the repository, as on 2026-10-09."""
        stub = self._switched_gh('PRIVATE')
        result = subprocess.run([str(stub['launcher']), 'repo', 'view', REPOSITORY, '--json', 'nameWithOwner,visibility'],
                                capture_output=True, text=True, env=dict(os.environ, GH_HOST='github.com'),
                                **({'creationflags': 0x08000000} if os.name == 'nt' else {}))
        self.assertNotEqual(result.returncode, 0)

    def test_no_credential_can_see_it_refuses(self):
        self._switched_gh('PRIVATE', sees={})
        with self.assertRaisesRegex(self.runtime.DataBoundaryError, 'no gh credential'):
            self.runtime._run(list(ARGV))

    def test_a_kit_without_the_api_refuses(self):
        class Kit:
            GitError = RuntimeError
        with patch.object(self.runtime, '_guard_module', return_value=Kit):
            with self.assertRaisesRegex(self.runtime.DataBoundaryError, 'account-independent'):
                self.runtime._run(list(ARGV))


if __name__ == '__main__':
    unittest.main()
