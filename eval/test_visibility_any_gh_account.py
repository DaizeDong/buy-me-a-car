"""The live PRIVATE check must not depend on which gh account is ACTIVE.

A plain `gh api repos/OWNER/NAME --jq .private` asks only with the account `gh auth switch` last
selected. When another session switched it to an account that cannot see the companion, every
proof failed closed. The query now goes through the pinned guards kit, which asks every stored gh
account. These tests run the REAL kit against a synthetic gh (the kit's own fixture generator)
whose active account cannot see the repository; nothing here touches the real gh.

The synthetic gh is installed so that a bare `subprocess.run(['gh', ...])` resolves it on every
OS, and it also answers the legacy `gh api repos/OWNER/NAME --jq .private` with the ACTIVE account
only. The previous code therefore fails the call-path tests because it asked only the active
account, not because gh could not be found.
"""
import importlib.util
import io
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'example-owner/example-private'
ARGV = ['gh', 'api', '--hostname', 'github.com', 'repos/' + REPOSITORY, '--jq', '.private']


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Legacy `gh api` answered with the ACTIVE credential only (GH_TOKEN wins, as in real gh); every
# other call goes to the kit's own synthetic gh program unchanged.
_RESOLVABLE_GH = r'''
import json, os, runpy, sys
STATE, PROGRAM = %r, %r
argv = sys.argv[1:]
if argv[:1] != ["api"]:
    sys.argv = [PROGRAM, STATE] + argv
    runpy.run_path(PROGRAM, run_name="__main__")
    sys.exit(0)
with open(STATE, encoding="utf-8") as stream:
    state = json.load(stream)
tokens = {login.casefold(): token for login, token in state["tokens"].items()}
owners = {token: login for login, token in state["tokens"].items()}
explicit = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
credential = explicit or tokens.get(state["active"].casefold())
with open(state["log"], "a", encoding="utf-8") as log:
    log.write(json.dumps({"argv": argv, "credential": owners.get(credential, "unknown") if credential else None,
                          "explicit": bool(explicit), "gh_host": os.environ.get("GH_HOST")}) + "\n")
name = next((arg[len("repos/"):] for arg in argv if arg.startswith("repos/")), "")
if name.casefold() not in {repo.casefold() for repo in state["sees"].get(owners.get(credential, ""), [])}:
    sys.stderr.write("gh: Not Found (HTTP 404)\n")
    sys.exit(1)
sys.stdout.write("true\n" if state["visibility"][name.casefold()] in ("PRIVATE", "INTERNAL") else "false\n")
'''


def _resolvable_gh(stub):
    """Install the synthetic gh where a bare `gh` argv resolves it; return that directory.

    The kit's launcher is a .cmd on Windows, which CreateProcess never finds for a bare `gh`
    (it appends only .exe), so the previous code failed there with FileNotFoundError instead of
    the active-account refusal under test. pip's console-script launcher runs the zip appended to
    it with the given interpreter, exactly like any installed entry point."""
    directory = stub['state'].parent / 'gh-resolvable'
    directory.mkdir()
    source = _RESOLVABLE_GH % (str(stub['state']), str(stub['state'].parent / 'gh_stub.py'))
    if os.name == 'nt':
        distlib = importlib.util.find_spec('pip._vendor.distlib')
        assert distlib is not None, 'pip is required to build the synthetic gh.exe'
        name = 't64-arm.exe' if platform.machine().upper() == 'ARM64' else 't64.exe'
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, 'w') as bundle:
            bundle.writestr('__main__.py', source)
        (directory / 'gh.exe').write_bytes((Path(distlib.origin).parent / name).read_bytes() + b'#!"'
                                           + os.fsencode(sys.executable) + b'" -I\n' + archive.getvalue())
    else:
        script = directory / 'gh_resolvable.py'
        script.write_text(source, encoding='utf-8')
        launcher = directory / 'gh'
        launcher.write_text('#!/bin/sh\nexec "%s" -I "%s" "$@"\n' % (sys.executable, script), encoding='utf-8')
        launcher.chmod(launcher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return directory


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
        environment['PATH'] = str(_resolvable_gh(stub))
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
        result = subprocess.run(list(ARGV), capture_output=True, text=True,
                                **({'creationflags': 0x08000000} if os.name == 'nt' else {}))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call['credential'] for call in self.fixtures.gh_stub_calls(stub)], ['other-account'])

    def _companion_proof(self):
        """The supported proof API answers the companion's destinations; visibility is the real kit."""
        kit = self.runtime._guard_module('data_boundary')
        root = Path(self.tmp.name) / 'companion'
        root.mkdir()
        proof = SimpleNamespace(root=str(root), repositories=(REPOSITORY,), signature='synthetic-stable-signature')
        api = SimpleNamespace(
            prove_private_companion=lambda path: proof,
            read_private_companion_git=lambda proof, *args: SimpleNamespace(returncode=0, stdout='synthetic-head'),
            query_github_visibility=kit.query_github_visibility, GitError=kit.GitError)
        patcher = patch.object(self.runtime, '_guard_module', return_value=api)
        patcher.start()
        self.addCleanup(patcher.stop)
        return root

    def test_data_destination_proof_asks_any_account(self):
        """The production call site in _private_repo_identity, not only _run, must ask any account."""
        stub = self._switched_gh('PRIVATE')
        root = self._companion_proof()
        self.assertEqual(self.runtime._private_repo_identity(root), REPOSITORY)
        calls = self.fixtures.gh_stub_calls(stub)
        self.assertEqual([call['credential'] for call in calls if call['argv'][:2] == ['repo', 'view']],
                         ['example-owner'])
        self.assertFalse([call for call in calls if call['argv'][:1] == ['api'] or call['argv'][:2] == ['auth', 'switch']])

    def test_data_destination_proof_refuses_public(self):
        self._switched_gh('PUBLIC')
        root = self._companion_proof()
        with self.assertRaises(self.runtime.DataBoundaryError) as refused:
            self.runtime._private_repo_identity(root)
        self.assertIn('public or unknown', str(refused.exception.__cause__))

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
