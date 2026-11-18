#!/usr/bin/env python3
"""Issue #262: separate immutable V9 history from strictly bounded current bytes.

No network, checkout mutation, worktree, receipt regeneration, or audit patching.
Requires the pinned commits and their ancestry locally, plus Pillow for frozen tests.
Use --scratch-dir (or JCODE_SCRATCH_DIR), outside the checkout, for the export.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unicodedata

HISTORICAL = '6c3be49c0322874a7c037d4e0b29495e311a6c3a'
REFERENCE = '404d6b2bac5beeceeab4068d33c24dd5a001430c'
APPROVED = '0c20990c8a6334b6c93d42db0336fc4cf2ab62f9'
ADDITIONS = {
    'App/KioskPlayableReview.swift': ('8449f6d09932e5c977f495c66135a12b18554232', '7124ebd37a12e742fb9492af23b1d83cdda32dba93b3a9aa7760573656dcc3d4'),
    'App/LiveWorldProjection.swift': ('bb874117fc53fabbc66c7925ee4eb519c2afbcef', '74e551043e73206160e791f1e2410d45105ee53a353216587c56679feaadac75'),
}
PACKET = 'docs/review/blocked-base-curb-relief-20261116'
FROZEN = {
    PACKET + '/audit.py': '68cef48cd14ddc073bfd2653e348796ee5caa965ead20ff941e829fab0fcd1b5',
    PACKET + '/test_audit.py': '72b65d16daa6d9d55fd82d34ccf359dff1e54a0f75470989e2c5c8023d8a1dc1',
    PACKET + '/protected-files.json': '5086e2f19bda1f88b72e9854dc05ca652b5049f72c07de65e130fec96b874baa',
}
PRODUCTION_INTENT = 'intent/2026-11-17-production-qualification.md'
# Each step is (exact commit, parent SHA256, result SHA256).
# These are authorization-specific transitions, not wildcard path exemptions.
TRANSITIONS = {
    'App/GameScene.swift': [
        ('8449f6d09932e5c977f495c66135a12b18554232', 'a3b154e63f208fe999c5ee88b1c02c8ab34002d3708dd8712ec8935dd6fa7e67', 'cae3458565a7e07ebc9c78582579b7d12e835f2123c3048f6d53b0e3784e2121'),
        ('bb874117fc53fabbc66c7925ee4eb519c2afbcef', 'cae3458565a7e07ebc9c78582579b7d12e835f2123c3048f6d53b0e3784e2121', 'a47aaa54f2d432f6dee6cc0e7ee7486b88189e9a6a4b76f1839c02d0fd8e344b'),
    ],
    'App/WorldRenderer.swift': [
        ('8449f6d09932e5c977f495c66135a12b18554232', 'e6cb6a52d8322380818d21a8390d70a5ac8ce3e3cf0481fb516efdf65c4850f8', '295b642e3c87bc68d603b258bc4471d779a22e24bc81ec65cd57059c95be24ac'),
        ('bb874117fc53fabbc66c7925ee4eb519c2afbcef', '295b642e3c87bc68d603b258bc4471d779a22e24bc81ec65cd57059c95be24ac', 'a8da26f22384bf692b1d421a1c27569f0af7d1250a44326eaba8a42a0e8449db'),
    ],
    'Sources/SurveillanceCore/Contracts/GateRegistry.swift': [
        ('0aa395145de56852722256590f8b74cf7fd17118', 'ae965ed72da30942d02ed755dc56b7b5c503d9e9474b65d52c643d86dec25886', '73b54d83768fb486f12d5c78ee604b81f7eee531661f607ba05739b9e4cb5c49'),
    ],
    'Sources/SurveillanceCore/Determinism/SHA256.swift': [
        ('4294f737e20ff50900faa572768902c51fdca94e', '14544f4bdffd72d2d4a36ac8d6193bdb21c0990a05acccffd10071ee2f39eb1d', '7216a0b94732134b3b5497ab47fdd4035c9239a63736e784263af1d341e27739'),
    ],
    'Sources/SurveillanceCore/Presentation/PresentationSnapshot.swift': [
        ('fed8a3d18067c226376d9779f42bbc194dffcdab', '71675cee588bba0c316c3cd591f4539b8e2b0c939506c98325cb6db903a395a7', '5cac8af2877bdf71751ca93d66eea82050e015036535dd54148653ff2120d022'),
    ],
}
# Exact commit objects bind these documents, including the contemporary scope text.
AUTHORIZATION = {
    '8449f6d09932e5c977f495c66135a12b18554232': [PRODUCTION_INTENT, 'docs/review/kiosk-only-geometry-20261117/COORDINATOR-REVIEW.md', 'docs/review/kiosk-only-geometry-20261117/native/playable/ACTUAL-PLAYABLE-REVIEW.md'],
    'bb874117fc53fabbc66c7925ee4eb519c2afbcef': ['intent/2026-11-17-live-world-projection.md', 'docs/review/live-world-projection-20261117/COORDINATOR-REVIEW.md'],
    '0aa395145de56852722256590f8b74cf7fd17118': [PRODUCTION_INTENT, 'docs/review/production-execution-20261117/README.md'],
    '4294f737e20ff50900faa572768902c51fdca94e': [PRODUCTION_INTENT, 'docs/review/production-execution-20261117/HASH-PERFORMANCE.md'],
    'fed8a3d18067c226376d9779f42bbc194dffcdab': [PRODUCTION_INTENT, 'docs/review/kiosk-only-geometry-20261117/native/playable/SOCKET-ORDERING-REPAIR.md'],
}
POLICY_SHA256 = '453e5785e280f113a6f289c7cccd8008a7e3b3d5aa44c42da8c0fa5d83e93919'
FETCH_HELP = ('Missing local history. Coordinator must fetch outside this verifier: '
              'use actions/checkout fetch-depth: 0, or git fetch --unshallow origin '
              'for an existing shallow clone. Include the reviewed PR branch and its ancestors. '
              'This verifier never fetches.')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def policy_digest(transitions, authorization):
    return sha256(json.dumps({'transitions': transitions, 'authorization': authorization,
                             'approvedCommit': APPROVED, 'additions': ADDITIONS},
                             sort_keys=True, separators=(',', ':')).encode())


def safe_name(name):
    require(isinstance(name, str) and name and '\\' not in name and '\x00' not in name,
            'Unsafe path: ' + repr(name))
    parts = name.split('/')
    require(not PurePosixPath(name).is_absolute() and all(p not in ('', '.', '..') for p in parts),
            'Unsafe path: ' + name)
    return parts


def safe_file(root, name):
    parts = safe_name(name)
    path = root
    for i, part in enumerate(parts):
        path = path / part
        try:
            info = path.lstat()
        except FileNotFoundError as error:
            raise ValueError('Missing protected file: ' + name) from error
        require(not stat.S_ISLNK(info.st_mode), 'Aliased protected file: ' + name)
        if i < len(parts) - 1:
            require(stat.S_ISDIR(info.st_mode), 'Non-directory parent: ' + name)
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Non-regular or aliased protected file: ' + name)
    return path


def git_env():
    # Ignore caller redirection/config injection and replace refs. Never lazy-fetch.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0')
    return env


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], env=git_env(),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0, 'Git failed: ' + ' '.join(args) + '\n' +
            result.stderr.decode(errors='replace') + '\n' + FETCH_HELP)
    return result.stdout


def exact_commit(root, commit):
    require(len(commit) == 40 and all(c in '0123456789abcdef' for c in commit), 'Commit must be exact full SHA')
    require(git(root, 'rev-parse', '--verify', commit + '^{commit}').decode().strip() == commit,
            'Commit identity mismatch: ' + commit)


def ancestor(root, before, after):
    git(root, 'merge-base', '--is-ancestor', before, after)


def tree(root, commit):
    entries = {}
    for row in git(root, 'ls-tree', '-r', '-z', commit).split(b'\0'):
        if row:
            meta, encoded = row.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            name = encoded.decode('utf-8')
            safe_name(name)
            require(kind == 'blob' and mode in ('100644', '100755'), 'Unsupported Git entry: ' + name)
            entries[name] = (mode, oid)
    require(entries, 'Empty Git tree')
    return entries


def blob(root, commit, name):
    safe_name(name)
    return git(root, 'cat-file', 'blob', commit + ':' + name)


def verify_bytes(root, expected, head_tree=None, index=None, approved_tree=None):
    for name, digest in expected.items():
        path = safe_file(root, name)
        data = path.read_bytes()
        require(sha256(data) == digest, 'Protected bytes changed: ' + name)
        if approved_tree is not None:
            require(name in approved_tree, 'Missing approved file: ' + name)
            approved_mode, approved_oid = approved_tree[name]
            actual_mode = '100755' if path.stat().st_mode & 0o111 else '100644'
            require(actual_mode == approved_mode, 'Worktree/approved mode mismatch: ' + name)
            require(head_tree is not None and head_tree.get(name) == (approved_mode, approved_oid),
                    'HEAD/approved entry mismatch: ' + name)
        if head_tree is not None:
            require(name in head_tree, 'Missing HEAD file: ' + name)
            mode, oid = head_tree[name]
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            require(actual == oid, 'HEAD/worktree mismatch: ' + name)
            if index is not None:
                require(index.get(name) == [(mode, oid, '0')], 'Index/HEAD mismatch: ' + name)


def load_receipt(root):
    verify_bytes(root, FROZEN)
    receipt = json.loads(safe_file(root, PACKET + '/protected-files.json').read_bytes())
    require(receipt['referenceCommit'] == REFERENCE and len(receipt['files']) == 1766,
            'Wrong original receipt census/reference')
    return receipt


def verify_provenance(root, head, receipt, transitions=None, authorization=None):
    transitions = TRANSITIONS if transitions is None else transitions
    authorization = AUTHORIZATION if authorization is None else authorization
    require(policy_digest(transitions, authorization) == POLICY_SHA256, 'Authorization policy changed')
    for commit in (REFERENCE, HISTORICAL, APPROVED, *authorization):
        exact_commit(root, commit)
        ancestor(root, commit, head)
    ancestor(root, REFERENCE, HISTORICAL)
    evidence = []
    for commit, names in authorization.items():
        ancestor(root, HISTORICAL, commit)
        parent = git(root, 'rev-parse', commit + '^').decode().strip()
        exact_commit(root, parent)
        entries = tree(root, commit)
        for name in names:
            require(name in entries, 'Missing authorization document: ' + name)
            data = blob(root, commit, name)
            require(data.strip(), 'Empty authorization document: ' + name)
            evidence.append({'commit': commit, 'path': name, 'sha256': sha256(data)})
    expected = dict(receipt['files'])
    for name, steps in transitions.items():
        require(name in expected, 'Transition outside original receipt: ' + name)
        previous = HISTORICAL
        for commit, before, after in steps:
            require(before == expected[name] and before != after, 'Broken transition chain: ' + name)
            ancestor(root, previous, commit)
            require(sha256(blob(root, commit + '^', name)) == before,
                    'Authorization parent source mismatch: ' + name)
            require(sha256(blob(root, commit, name)) == after,
                    'Authorization result source mismatch: ' + name)
            expected[name] = after
            previous = commit
    for name, (commit, digest) in ADDITIONS.items():
        require(name not in expected and commit in authorization, 'Unauthorized added path: ' + name)
        ancestor(root, commit, APPROVED)
        require(sha256(blob(root, commit, name)) == digest,
                'Added authorization source mismatch: ' + name)
        require(sha256(blob(root, APPROVED, name)) == digest,
                'Added approved source mismatch: ' + name)
        expected[name] = digest
    return expected, evidence


def preflight(root):
    require(git(root, 'rev-parse', '--show-toplevel').decode().strip() == str(root),
            '--repo must be the checkout root')
    # A shallow clone is sufficient only when every pinned commit, parent and
    # ancestry edge can actually be proved below. Do not reject unrelated shallow roots.
    # Partial clones may trigger networking in older Git despite NO_LAZY_FETCH.
    config = git(root, 'config', '--local', '--list').decode().lower()
    require('partialclone' not in config and '.promisor=' not in config,
            'Partial/promisor clones are unsupported. Supply a complete local clone. ' + FETCH_HELP)
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    exact_commit(root, head)
    return head


def protected_names(names, prefixes):
    return {name for name in names if any(name == p or name.startswith(p) for p in prefixes)}


def verify_census(receipt, approved_tree, head_tree, index, untracked):
    prefixes = receipt['protectedPrefixes']
    approved = protected_names(approved_tree, prefixes)
    require(approved == set(receipt['files']) | set(ADDITIONS), 'Approved protected census changed')
    for label, names in (('HEAD', head_tree), ('Index', index)):
        actual = protected_names(names, prefixes)
        require(actual == approved, label + ' protected census mismatch: ' +
                ', '.join(sorted(actual ^ approved)))
    unexpected = protected_names(untracked, prefixes)
    require(not unexpected, 'Untracked protected additions: ' + ', '.join(sorted(unexpected)))


def verify_current(root):
    head = preflight(root)
    receipt = load_receipt(root)
    expected, evidence = verify_provenance(root, head, receipt)
    head_tree = tree(root, head)
    approved_tree = tree(root, APPROVED)
    index = {}
    for row in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            index.setdefault(name.decode(), []).append(tuple(meta.decode().split()))
    untracked = [name.decode() for name in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if name]
    verify_census(receipt, approved_tree, head_tree, index, untracked)
    verify_bytes(root, {**expected, **FROZEN}, head_tree, index, approved_tree)
    require(git(root, 'rev-parse', 'HEAD').decode().strip() == head, 'HEAD changed during verification')
    return {'scope': 'CURRENT_HEAD', 'head': head, 'approvedCommit': APPROVED,
            'protectedFiles': len(receipt['files']), 'currentProtectedFiles': len(expected),
            'approvedAddedFiles': len(ADDITIONS),
            'unchangedOriginalFiles': len(receipt['files']) - len(TRANSITIONS),
            'explicitTransitionFiles': len(TRANSITIONS), 'authorizationEvidence': evidence}


def extract_archive(archive, destination, expected):
    """Extract only regular files/directories, then prove exact Git blob closure.

    Never tar.extract/extractall: links, devices, traversal, aliases, duplicates,
    export-ignore and export-subst differences all fail closed.
    """
    require(destination.is_dir() and not any(destination.iterdir()), 'Export destination must be empty')
    seen, aliases, files = set(), {}, set()
    for member in archive:
        name = member.name.rstrip('/') if member.isdir() else member.name
        parts = safe_name(name)
        require(name not in seen, 'Duplicate archive entry: ' + name)
        seen.add(name)
        for i in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:i])
            alias = unicodedata.normalize('NFC', prefix).casefold()
            require(aliases.setdefault(alias, prefix) == prefix, 'Aliased archive entry: ' + name)
        path = destination.joinpath(*parts)
        require(member.isdir() or member.isreg(), 'Unsafe archive entry type: ' + name)
        if member.isdir():
            path.mkdir(parents=True, exist_ok=True)
            continue
        require(name in expected, 'Unexpected archive file: ' + name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with archive.extractfile(member) as source, path.open('xb') as output:
            shutil.copyfileobj(source, output)
        data = safe_file(destination, name).read_bytes()
        mode, oid = expected[name]
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(actual == oid, 'Archive/Git source mismatch: ' + name)
        path.chmod(int(mode[-3:], 8))
        files.add(name)
    require(files == set(expected), 'Archive missing tracked files: ' + ', '.join(sorted(set(expected) - files)[:5]))
    return len(files)


def export_snapshot(root, destination):
    exact_commit(root, HISTORICAL)
    entries = tree(root, HISTORICAL)
    with tempfile.TemporaryFile(dir=destination.parent) as errors:
        with subprocess.Popen(['git', '-C', str(root), 'archive', '--format=tar', HISTORICAL],
                              env=git_env(), stdout=subprocess.PIPE, stderr=errors) as process:
            try:
                with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
                    count = extract_archive(archive, destination, entries)
                process.stdout.close()
                code = process.wait()
                errors.seek(0)
                require(code == 0, 'Historical archive failed: ' + errors.read().decode(errors='replace'))
            except BaseException:
                process.kill()
                process.wait()
                process.stdout.close()
                raise
    return count


def historical_commands(snapshot):
    base = [sys.executable, '-B', '-W', 'error::ResourceWarning']
    return [base + [str(snapshot / PACKET / 'test_audit.py')],
            base + [str(snapshot / PACKET / 'audit.py'), 'verify']]


def verify_historical(root, scratch):
    head = preflight(root)
    exact_commit(root, HISTORICAL)
    ancestor(root, HISTORICAL, head)
    require(scratch.is_dir(), 'Scratch directory must exist')
    require(not scratch.is_relative_to(root), 'Scratch export must be outside caller checkout')
    with tempfile.TemporaryDirectory(prefix='v9-preservation-', dir=scratch) as directory:
        snapshot = Path(directory).resolve()
        count = export_snapshot(root, snapshot)
        verify_bytes(snapshot, FROZEN)
        env = os.environ.copy()
        env.pop('PYTHONPATH', None)
        env.pop('PYTHONHOME', None)
        env.update(PYTHONDONTWRITEBYTECODE='1', JCODE_SCRATCH_DIR=str(snapshot.parent),
                   TMPDIR=str(snapshot.parent))
        for command in historical_commands(snapshot):
            print('HISTORICAL_COMMAND ' + json.dumps(command), flush=True)
            subprocess.run(command, cwd=snapshot, env=env, check=True)
        return {'scope': 'HISTORICAL_ONLY', 'commit': HISTORICAL, 'exactExportFiles': count,
                'commandsPassed': 2, 'currentHeadClaim': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scope', choices=('all', 'current', 'historical'))
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--scratch-dir', type=Path, default=os.environ.get('JCODE_SCRATCH_DIR'))
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    try:
        results = []
        if args.scope in ('all', 'current'):
            results.append(verify_current(root))
        if args.scope in ('all', 'historical'):
            require(args.scratch_dir is not None, 'Set --scratch-dir or JCODE_SCRATCH_DIR outside checkout')
            results.append(verify_historical(root, args.scratch_dir.resolve()))
        print(json.dumps({'status': 'VERIFIED', 'scopes': results}, indent=2))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print('V9_PRESERVATION_FAILED: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
