"""Validate only staged files in a fresh export, excluding unpublished siblings."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKET = 'docs/review/architectural-scale-20261117'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--export', required=True, type=Path)
    args = parser.parse_args()
    target = args.export.resolve()
    if target.exists():
        raise RuntimeError('Fresh non-existing export path required')
    target.mkdir(parents=True)
    subprocess.run(['git', 'checkout-index', '--all', '--prefix=' + str(target) + '/'], cwd=ROOT, check=True)
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    commands = [
        [sys.executable, PACKET + '/test_audit.py'],
        [sys.executable, PACKET + '/audit.py', 'check'],
        [sys.executable, PACKET + '/source/test_source.py'],
        [sys.executable, PACKET + '/test_gallery.py'],
    ]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
    for command in commands:
        print('COMMAND', json.dumps(command), flush=True)
        subprocess.run(command, cwd=target, env=env, check=True)
    replay = target.parent / (target.name + '-replay')
    command = [sys.executable, PACKET + '/source/build.py', '--out', str(replay)]
    print('COMMAND', json.dumps(command), flush=True)
    subprocess.run(command, cwd=target, env=env, check=True)
    original = target / PACKET / 'source/output'
    names = {p.name for p in original.iterdir() if p.is_file()}
    if names != {p.name for p in replay.iterdir() if p.is_file()}:
        raise RuntimeError('Replay output census mismatch')
    for name in sorted(names):
        if (original / name).read_bytes() != (replay / name).read_bytes():
            raise RuntimeError('Replay byte mismatch: ' + name)
    print('EXACT_RENDER_REPLAY_VERIFIED', len(names), flush=True)
    print('TRACKED_EXPORT_VALIDATED', json.dumps({'export': str(target),
          'trackedFiles': len([n for n in tracked if n]), 'commandCount': len(commands) + 1}), flush=True)


if __name__ == '__main__':
    main()
