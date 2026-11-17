"""Byte-preservation audit for the one approved architectural decision aid."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ALLOWED = {'intent/2026-11-17-architectural-scale-review.md', 'docs/handoff/NEXT.md'}
PREFIX = 'docs/review/architectural-scale-20261117/'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Outward path: ' + name)
    return path


def snapshot():
    target = HERE / 'protected-files.json'
    if target.exists():
        raise RuntimeError('Initial protection snapshot is immutable')
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    files = {name: digest(resolve(ROOT, name)) for name in names
             if name and name not in ALLOWED and not name.startswith(PREFIX)}
    record = {'schema': 'architectural-protection-001',
              'baseCommit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
              'files': files}
    target.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print('Protected tracked files:', len(files))


def check(root=ROOT, manifest=None):
    record = manifest or json.loads((HERE / 'protected-files.json').read_text())
    if record.get('schema') != 'architectural-protection-001' or not record.get('files'):
        raise ValueError('Missing protection census')
    for name, expected in record['files'].items():
        path = resolve(root, name)
        if not path.is_file() or digest(path) != expected:
            raise ValueError('Protected byte drift: ' + name)
    print('Protected tracked bytes verified:', len(record['files']))


if __name__ == '__main__':
    if sys.argv[1:] == ['snapshot']:
        snapshot()
    elif sys.argv[1:] == ['check']:
        check()
    else:
        raise SystemExit('Usage: audit.py snapshot|check')
