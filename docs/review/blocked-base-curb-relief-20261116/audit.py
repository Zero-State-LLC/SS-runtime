#!/usr/bin/env python3
"""V9 independent immutable-byte and baseline-pixel audit.

ADAPT: footprint-ground-repair-20261116/verify_preservation.py:29-48,78-89.
Use a tracked portable receipt instead of requiring .git at verification time.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REFERENCE = '404d6b2bac5beeceeab4068d33c24dd5a001430c'
PROTECTED = ('App/', 'Sources/', 'SPEC_BASELINE.md',
             'AppTests/FootprintGroundSceneTests.swift',
             'AppTests/BuildingPerspectiveSceneTests.swift',
             'AppTests/SceneQAReviewDepth.swift',
             'docs/review/footprint-ground-repair-20261116/',
             'docs/review/building-perspective-detail-20261116/',
             'docs/review/scene-qa-framing-20261116/',
             'docs/review/scene-qa-repair-20261116/',
             'docs/review/footprint-consistency-20261116/')
RECEIPT = HERE / 'protected-files.json'
RECEIPT_SHA256 = '5086e2f19bda1f88b72e9854dc05ca652b5049f72c07de65e130fec96b874baa'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_file(root, name):
    require(isinstance(name, str) and name and not Path(name).is_absolute(), 'Unsafe protected path')
    require('..' not in Path(name).parts, 'Protected path traversal')
    root = root.resolve()
    path = root / name
    require(path.is_file(), 'Missing protected file: ' + name)
    require(not any(p.is_symlink() for p in [path, *path.parents] if p != root and root in p.parents), 'Aliased protected file: ' + name)
    require(path.resolve().is_relative_to(root), 'Escaping protected file: ' + name)
    return path


def snapshot():
    require(not RECEIPT.exists(), 'Refuse to replace immutable preservation receipt')
    raw = subprocess.check_output(['git', 'ls-tree', '-r', '-z', REFERENCE], cwd=ROOT)
    files = {}
    for row in raw.split(b'\0'):
        if not row:
            continue
        metadata, encoded = row.split(b'\t', 1)
        name = encoded.decode()
        if not any(name == prefix or name.startswith(prefix) for prefix in PROTECTED):
            continue
        mode, kind, old = metadata.decode().split()
        require(kind == 'blob' and mode in ('100644', '100755'), 'Unexpected protected entry')
        path = safe_file(ROOT, name)
        actual = subprocess.check_output(['git', 'hash-object', '--no-filters', '--', name], cwd=ROOT).decode().strip()
        require(actual == old, 'Preexisting protected drift: ' + name)
        files[name] = digest(path)
    require(len(files) > 200, 'Vacuous protected census')
    receipt = {'schema': 'v9-protected-bytes-001', 'referenceCommit': REFERENCE,
               'protectedPrefixes': list(PROTECTED), 'files': files}
    RECEIPT.write_text(json.dumps(receipt, indent=2) + '\n')
    return {'status': 'SNAPSHOT_CREATED', 'files': len(files), 'referenceCommit': REFERENCE}


def verify(receipt=None, root=ROOT):
    receipt = json.loads(RECEIPT.read_text()) if receipt is None else receipt
    encoded = (json.dumps(receipt, indent=2) + '\n').encode()
    require(hashlib.sha256(encoded).hexdigest() == RECEIPT_SHA256, 'Preservation receipt changed')
    require(receipt['schema'] == 'v9-protected-bytes-001' and receipt['referenceCommit'] == REFERENCE, 'Wrong preservation reference')
    require(receipt['protectedPrefixes'] == list(PROTECTED), 'Wrong protected scope')
    files = receipt['files']
    require(isinstance(files, dict) and len(files) > 200, 'Vacuous protected census')
    for name, expected in files.items():
        require(any(name == p or name.startswith(p) for p in PROTECTED), 'Unexpected protected file')
        require(digest(safe_file(root, name)) == expected, 'Protected bytes changed: ' + name)
    return {'status': 'PROTECTED_BYTES_UNCHANGED', 'files': len(files), 'referenceCommit': REFERENCE,
            'limitation': 'Portable unkeyed receipt establishes consistency, not independently authenticated origin'}


def baseline_pixels(old=None, new=None):
    old = old or ROOT / 'docs/review/footprint-ground-repair-20261116/scene/native-capture-v8'
    new = new or HERE / 'scene/native-capture-v9'
    checks = []
    for zoom in (100, 125, 140):
        for suffix in ('native', 'half', 'grayscale'):
            before = old / f'source-scene-candidate-ordinary-z{zoom}-{suffix}.png'
            after = new / f'source-scene-control-ordinary-z{zoom}-{suffix}.png'
            with Image.open(before) as a, Image.open(after) as b:
                aa, bb = a.convert('RGBA'), b.convert('RGBA')
                require(aa.size == bb.size and aa.tobytes() == bb.tobytes(), 'Baseline pixels differ: ' + after.name)
                checks.append({'zoom': zoom / 100, 'suffix': suffix, 'size': list(aa.size),
                               'rgbaSHA256': hashlib.sha256(aa.tobytes()).hexdigest()})
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['snapshot', 'verify', 'pixels'])
    args = parser.parse_args()
    print(json.dumps({'snapshot': snapshot, 'verify': verify, 'pixels': baseline_pixels}[args.action](), indent=2))
