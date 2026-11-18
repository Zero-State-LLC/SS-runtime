#!/usr/bin/env python3
"""New guard regressions only. Frozen V9 tests are executed unchanged by the CLI.

All filesystem/Git mutations occur in invocation-owned scratch directories.
Includes a real Git index/HEAD fixture borrowing local read-only objects, never
fetching or creating a worktree/commit. No Swift or simulator execution.
"""
import copy
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import verify_v9_preservation as v

REPO = Path(__file__).resolve().parents[1]
SCRATCH = Path(os.environ.get('JCODE_SCRATCH_DIR', tempfile.gettempdir())).resolve()


def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class PathAndArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='v9-unit-', dir=SCRATCH)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def test_bytes_changed_missing_and_aliases(self):
        source = self.root / 'file'
        source.write_bytes(b'original')
        expected = {'file': v.sha256(b'original')}
        v.verify_bytes(self.root, expected)
        source.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'bytes changed'):
            v.verify_bytes(self.root, expected)
        source.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            v.verify_bytes(self.root, expected)
        actual = self.root / 'actual'
        actual.write_bytes(b'original')
        source.symlink_to(actual)
        with self.assertRaisesRegex(ValueError, 'Aliased'):
            v.verify_bytes(self.root, expected)
        source.unlink()
        os.link(actual, source)
        with self.assertRaisesRegex(ValueError, 'aliased'):
            v.verify_bytes(self.root, expected)

    def test_parent_alias_and_unsafe_names(self):
        (self.root / 'real').mkdir()
        (self.root / 'real/file').write_bytes(b'ok')
        (self.root / 'alias').symlink_to(self.root / 'real', target_is_directory=True)
        for name in ('../escape', '/absolute', 'real/../real/file', 'real//file',
                     './real/file', 'real\\file', '', 'alias/file'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                v.safe_file(self.root, name)

    def extract(self, rows, expected):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode='w') as archive:
            for name, kind, content in rows:
                member = tarfile.TarInfo(name)
                member.type = kind
                if kind in (tarfile.SYMTYPE, tarfile.LNKTYPE):
                    member.linkname = '../outside'
                member.size = len(content) if kind == tarfile.REGTYPE else 0
                archive.addfile(member, io.BytesIO(content) if member.size else None)
        data.seek(0)
        destination = self.root / 'export'
        destination.mkdir()
        try:
            with tarfile.open(fileobj=data, mode='r|') as archive:
                return v.extract_archive(archive, destination, expected)
        finally:
            shutil.rmtree(destination)

    def test_exact_archive(self):
        rows = [('dir', tarfile.DIRTYPE, b''), ('dir/file', tarfile.REGTYPE, b'content')]
        self.assertEqual(self.extract(rows, {'dir/file': ('100644', oid(b'content'))}), 1)

    def test_archive_rejects_unsafe_types_names_aliases_and_duplicates(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE, tarfile.FIFOTYPE):
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, 'Unsafe archive entry type'):
                self.extract([('file', kind, b'')], {'file': ('100644', oid(b''))})
        for name in ('../escape', '/absolute', './file', 'a//b', 'a\\b'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Unsafe path'):
                self.extract([(name, tarfile.REGTYPE, b'')], {})
        for names in (('file', 'file'), ('File', 'file'), ('Dir/one', 'dir/two'), ('é', 'e\u0301')):
            rows = [(name, tarfile.REGTYPE, b'x') for name in names]
            expected = {name: ('100644', oid(b'x')) for name in names}
            with self.subTest(names=names), self.assertRaisesRegex(ValueError, 'Duplicate|Aliased'):
                self.extract(rows, expected)
        self.assertFalse((self.root / 'outside').exists())

    def test_archive_requires_complete_unmodified_git_tree(self):
        cases = [([], {'file': ('100644', oid(b'x'))}, 'missing tracked'),
                 ([('file', tarfile.REGTYPE, b'x')], {}, 'Unexpected archive'),
                 ([('file', tarfile.REGTYPE, b'y')], {'file': ('100644', oid(b'x'))}, 'source mismatch')]
        for rows, expected, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.extract(rows, expected)

    def test_head_and_index_cannot_be_hidden_by_restored_worktree(self):
        (self.root / 'file').write_bytes(b'good')
        expected = {'file': v.sha256(b'good')}
        with self.assertRaisesRegex(ValueError, 'HEAD/worktree mismatch'):
            v.verify_bytes(self.root, expected, {'file': ('100644', oid(b'bad'))})
        with self.assertRaisesRegex(ValueError, 'Index/HEAD mismatch'):
            v.verify_bytes(self.root, expected, {'file': ('100644', oid(b'good'))},
                           {'file': [('100644', oid(b'bad'), '0')]})

    def test_historical_commands_are_full_unchanged_entrypoints(self):
        commands = v.historical_commands(self.root)
        base = [sys.executable, '-B', '-W', 'error::ResourceWarning']
        self.assertEqual(commands, [base + [str(self.root / v.PACKET / 'test_audit.py')],
                                    base + [str(self.root / v.PACKET / 'audit.py'), 'verify']])

    def test_git_environment_disables_redirect_replace_and_lazy_fetch(self):
        with patch.dict(os.environ, {'GIT_DIR': '/bad', 'GIT_CONFIG_COUNT': '1',
                                    'GIT_CONFIG_KEY_0': 'evil', 'GIT_CONFIG_VALUE_0': 'evil'}):
            env = v.git_env()
        self.assertNotIn('GIT_DIR', env)
        self.assertNotIn('GIT_CONFIG_COUNT', env)
        self.assertEqual(env['GIT_NO_REPLACE_OBJECTS'], '1')
        self.assertEqual(env['GIT_NO_LAZY_FETCH'], '1')


class RepositoryGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='v9-git-tests-', dir=SCRATCH)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name).resolve()
        subprocess.run(['git', 'init', '-q', str(cls.root)], check=True, env=v.git_env())
        objects = Path(v.git(REPO, 'rev-parse', '--git-path', 'objects').decode().strip())
        if not objects.is_absolute():
            objects = REPO / objects
        (cls.root / '.git/objects/info/alternates').write_text(str(objects.resolve()) + '\n')
        shallow = Path(v.git(REPO, 'rev-parse', '--git-path', 'shallow').decode().strip())
        if not shallow.is_absolute():
            shallow = REPO / shallow
        if shallow.exists():
            shutil.copyfile(shallow, cls.root / '.git/shallow')
        cls.head = v.git(REPO, 'rev-parse', 'HEAD').decode().strip()
        v.git(cls.root, 'update-ref', 'HEAD', cls.head)
        v.git(cls.root, 'read-tree', cls.head)
        cls.receipt = v.load_receipt(REPO)
        for name in {**cls.receipt['files'], **v.ADDITIONS, **v.FROZEN}:
            path = cls.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / name, path)

    @contextmanager
    def changed(self, name, data=None, alias=None):
        path = self.root / name
        original = path.read_bytes()
        original_mode = path.stat().st_mode & 0o777
        path.unlink()
        if alias is not None:
            path.symlink_to(alias)
        elif data is not None:
            path.write_bytes(data)
        try:
            yield
        finally:
            if path.exists() or path.is_symlink():
                path.unlink()
            path.write_bytes(original)
            path.chmod(original_mode)

    def test_real_current_head_all_1766_paths(self):
        result = v.verify_current(self.root)
        self.assertEqual(result['head'], self.head)
        self.assertEqual(result['protectedFiles'], 1766)
        self.assertEqual(result['currentProtectedFiles'], 1768)
        self.assertEqual(result['approvedAddedFiles'], 2)
        self.assertEqual(result['approvedCommit'], v.APPROVED)
        self.assertEqual(result['unchangedOriginalFiles'], 1761)
        self.assertEqual(result['explicitTransitionFiles'], 5)
        self.assertEqual(len(result['authorizationEvidence']), 11)

    def test_every_authorized_path_still_rejects_arbitrary_bytes(self):
        for name in v.TRANSITIONS:
            with self.subTest(name=name), self.changed(name, b'unauthorized'), \
                    self.assertRaisesRegex(ValueError, 'Protected bytes changed'):
                v.verify_current(self.root)

    def test_original_protected_path_rejects_change_and_missing_file(self):
        name = 'SPEC_BASELINE.md'
        for data in (b'changed', None):
            with self.subTest(data=data), self.changed(name, data), self.assertRaises(ValueError):
                v.verify_current(self.root)

    def test_current_transition_cannot_roll_back_to_historical_bytes(self):
        name = 'App/GameScene.swift'
        historical = v.blob(self.root, v.HISTORICAL, name)
        with self.changed(name, historical), self.assertRaisesRegex(ValueError, 'Protected bytes changed'):
            v.verify_current(self.root)

    def test_receipt_audit_and_test_audit_drift_rejected(self):
        for name in v.FROZEN:
            with self.subTest(name=name), self.changed(name, b'changed frozen file'), \
                    self.assertRaisesRegex(ValueError, 'Protected bytes changed'):
                v.verify_current(self.root)

    def test_equal_byte_file_and_parent_symlinks_rejected(self):
        name = 'App/GameScene.swift'
        with self.changed(name, alias=REPO / name), self.assertRaisesRegex(ValueError, 'Aliased'):
            v.verify_current(self.root)
        app = self.root / 'App'
        saved = self.root / 'saved-app'
        app.rename(saved)
        app.symlink_to(saved, target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError, 'Aliased'):
                v.verify_current(self.root)
        finally:
            app.unlink()
            saved.rename(app)

    def test_policy_mutations_are_not_new_authorization(self):
        for operation in ('remove', 'add', 'hash', 'commit', 'review'):
            transitions, authorization = copy.deepcopy(v.TRANSITIONS), copy.deepcopy(v.AUTHORIZATION)
            name = 'App/GameScene.swift'
            if operation == 'remove':
                del transitions[name]
            elif operation == 'add':
                transitions['App/extra.swift'] = transitions[name]
            elif operation == 'review':
                authorization[next(iter(authorization))] = []
            else:
                step = list(transitions[name][0])
                step[0 if operation == 'commit' else 2] = '0' * (40 if operation == 'commit' else 64)
                transitions[name][0] = step
            with self.subTest(operation=operation), self.assertRaisesRegex(ValueError, 'policy changed'):
                v.verify_provenance(self.root, self.head, self.receipt, transitions, authorization)

    def test_authorization_parent_and_result_source_mismatch_rejected(self):
        original_blob = v.blob
        name = 'App/GameScene.swift'
        commit = v.TRANSITIONS[name][0][0]
        for revision, message in ((commit + '^', 'parent source mismatch'),
                                  (commit, 'result source mismatch')):
            def altered(root, rev, path):
                return b'wrong source' if (rev, path) == (revision, name) else original_blob(root, rev, path)
            # Fault injection at the new Git reader only, never frozen audit/test semantics.
            with self.subTest(revision=revision), patch.object(v, 'blob', side_effect=altered), \
                    self.assertRaisesRegex(ValueError, message):
                v.verify_provenance(self.root, self.head, self.receipt)

    def test_staged_bad_bytes_cannot_hide_behind_clean_worktree(self):
        name = 'App/GameScene.swift'
        bad = self.root / 'bad'
        bad.write_bytes(b'staged unauthorized')
        digest = v.git(self.root, 'hash-object', '-w', str(bad)).decode().strip()
        v.git(self.root, 'update-index', '--cacheinfo', '100644,' + digest + ',' + name)
        try:
            with self.assertRaisesRegex(ValueError, 'Index/HEAD mismatch'):
                v.verify_current(self.root)
        finally:
            v.git(self.root, 'read-tree', self.head)
            bad.unlink()

    def test_missing_commit_and_severed_ancestry_fail_with_fetch_guidance(self):
        with self.assertRaisesRegex(ValueError, 'never fetches'):
            v.exact_commit(self.root, '0' * 40)
        with self.assertRaisesRegex(ValueError, 'exact full SHA'):
            v.exact_commit(self.root, v.HISTORICAL[:7])
        shallow = self.root / '.git/shallow'
        original = shallow.read_bytes() if shallow.exists() else None
        shallow.write_text(self.head + '\n')
        try:
            with self.assertRaisesRegex(ValueError, 'never fetches'):
                v.verify_current(self.root)
        finally:
            if original is None:
                shallow.unlink()
            else:
                shallow.write_bytes(original)

    def test_partial_clone_rejected_without_fetch(self):
        v.git(self.root, 'config', 'remote.fake.promisor', 'true')
        try:
            with self.assertRaisesRegex(ValueError, 'Partial/promisor'):
                v.verify_current(self.root)
        finally:
            v.git(self.root, 'config', '--unset', 'remote.fake.promisor')

    def test_approved_additions_reject_changed_missing_and_aliased_bytes(self):
        for name in v.ADDITIONS:
            for kind in ('changed', 'missing', 'alias'):
                options = {'data': b'bad'} if kind == 'changed' else {}
                if kind == 'alias':
                    options['alias'] = REPO / name
                with self.subTest(name=name, kind=kind), self.changed(name, **options), \
                        self.assertRaises(ValueError):
                    v.verify_current(self.root)

    def test_added_source_at_authorization_and_approved_commit_must_match(self):
        original_blob = v.blob
        name = 'App/KioskPlayableReview.swift'
        for revision in (v.ADDITIONS[name][0], v.APPROVED):
            def altered(root, rev, path):
                return b'wrong added source' if (rev, path) == (revision, name) else original_blob(root, rev, path)
            with self.subTest(revision=revision), patch.object(v, 'blob', side_effect=altered), \
                    self.assertRaisesRegex(ValueError, 'Added .* source mismatch'):
                v.verify_provenance(self.root, self.head, self.receipt)

    def test_untracked_and_staged_protected_additions_rejected(self):
        name = 'App/Unauthorized.swift'
        path = self.root / name
        path.write_bytes(b'not approved')
        try:
            with self.assertRaisesRegex(ValueError, 'Untracked protected additions'):
                v.verify_current(self.root)
            v.git(self.root, 'add', '--', name)
            with self.assertRaisesRegex(ValueError, 'Index protected census mismatch'):
                v.verify_current(self.root)
        finally:
            v.git(self.root, 'read-tree', self.head)
            path.unlink()

    def test_head_census_rejects_extra_or_removed_tracked_protected_file(self):
        original_tree = v.tree
        for operation in ('add', 'remove'):
            def altered(root, revision):
                entries = original_tree(root, revision)
                if revision == self.head:
                    if operation == 'add':
                        entries['Sources/Unauthorized.swift'] = ('100644', oid(b'bad'))
                    else:
                        del entries['App/LiveWorldProjection.swift']
                return entries
            with self.subTest(operation=operation), patch.object(v, 'tree', side_effect=altered), \
                    self.assertRaisesRegex(ValueError, 'HEAD protected census mismatch'):
                v.verify_current(self.root)

    def test_approved_census_cannot_admit_another_path(self):
        approved = v.tree(self.root, v.APPROVED)
        approved['Sources/Unauthorized.swift'] = ('100644', oid(b'bad'))
        with self.assertRaisesRegex(ValueError, 'Approved protected census changed'):
            v.verify_census(self.receipt, approved, approved, approved, [])

    def test_original_and_added_worktree_executable_drift_rejected(self):
        for name in ('App/GameScene.swift', 'App/KioskPlayableReview.swift'):
            path = self.root / name
            original_mode = path.stat().st_mode & 0o777
            path.chmod(original_mode | 0o111)
            try:
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Worktree/approved mode mismatch'):
                    v.verify_current(self.root)
            finally:
                path.chmod(original_mode)

    def test_staged_mode_drift_hidden_by_restored_worktree_rejected(self):
        name = 'App/GameScene.swift'
        v.git(self.root, 'update-index', '--chmod=+x', '--', name)
        self.assertEqual((self.root / name).stat().st_mode & 0o111, 0)
        try:
            with self.assertRaisesRegex(ValueError, 'Index/HEAD mismatch'):
                v.verify_current(self.root)
        finally:
            v.git(self.root, 'read-tree', self.head)

    def test_matching_head_index_worktree_mode_drift_is_not_authorized(self):
        name = 'App/GameScene.swift'
        data = (self.root / name).read_bytes()
        approved = {name: ('100644', oid(data))}
        changed_head = {name: ('100755', oid(data))}
        changed_index = {name: [('100755', oid(data), '0')]}
        path = self.root / name
        original_mode = path.stat().st_mode & 0o777
        path.chmod(original_mode | 0o111)
        try:
            with self.assertRaisesRegex(ValueError, 'Worktree/approved mode mismatch'):
                v.verify_bytes(self.root, {name: v.sha256(data)}, changed_head, changed_index, approved)
        finally:
            path.chmod(original_mode)
        # Even a self-consistent new HEAD/index is not a new mode authorization.
        with self.assertRaisesRegex(ValueError, 'HEAD/approved entry mismatch'):
            v.verify_bytes(self.root, {name: v.sha256(data)}, changed_head, changed_index, approved)

    def test_added_policy_and_approval_commit_are_pinned(self):
        changed = dict(v.ADDITIONS)
        changed['App/KioskPlayableReview.swift'] = (v.ADDITIONS['App/KioskPlayableReview.swift'][0], '0' * 64)
        with patch.object(v, 'ADDITIONS', changed), self.assertRaisesRegex(ValueError, 'policy changed'):
            v.verify_provenance(self.root, self.head, self.receipt)
        with patch.object(v, 'APPROVED', self.head), self.assertRaisesRegex(ValueError, 'policy changed'):
            v.verify_provenance(self.root, self.head, self.receipt)

    def test_historical_child_failure_is_failure_and_export_is_cleaned(self):
        exports = []
        def minimal_export(root, destination):
            exports.append(destination)
            for name in v.FROZEN:
                path = destination / name
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / name, path)
            return len(v.FROZEN)
        with patch.object(v, 'export_snapshot', side_effect=minimal_export), \
                patch.object(v, 'historical_commands', return_value=[[sys.executable, '-c', 'raise SystemExit(23)']]), \
                self.assertRaises(subprocess.CalledProcessError) as raised:
            v.verify_historical(self.root, SCRATCH)
        self.assertEqual(raised.exception.returncode, 23)
        self.assertEqual(len(exports), 1)
        self.assertFalse(exports[0].exists())

    def test_historical_export_inside_caller_checkout_rejected(self):
        with self.assertRaisesRegex(ValueError, 'outside caller checkout'):
            v.verify_historical(self.root, self.root)

    def test_cli_returns_nonzero_for_current_drift(self):
        with self.changed('App/GameScene.swift', b'bad'):
            result = subprocess.run([sys.executable, '-B', str(REPO / 'scripts/verify_v9_preservation.py'),
                                     'current', '--repo', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('V9_PRESERVATION_FAILED', result.stderr)
        self.assertNotIn('"status": "VERIFIED"', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
