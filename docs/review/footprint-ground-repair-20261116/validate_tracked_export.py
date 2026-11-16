#!/usr/bin/env python3
"""Validate this packet from the Git index, never unpublished working siblings."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PACKET = 'docs/review/footprint-ground-repair-20261116'


def main():
    scratch = Path(os.environ.get('JCODE_SCRATCH_DIR', str(ROOT.parent)))
    export = Path(tempfile.mkdtemp(prefix='footprint-v8-tracked-export-', dir=scratch))
    names = [s for s in subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0') if s]
    subprocess.run(['git', 'checkout-index', '--all', '--prefix=' + str(export) + '/'], cwd=ROOT, check=True)
    receipt = {'schema': 'tracked-scene-inputs-001',
               'gitHead': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
               'files': {n: hashlib.sha256((export / n).read_bytes()).hexdigest() for n in names if (export / n).is_file()}}
    (export / 'tracked-inputs.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('Export:', export, 'tracked files:', len(receipt['files']), flush=True)
    commands = [
        ['python3', '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', 'discover', '-s', PACKET, '-p', 'test_*.py', '-v'],
        ['python3', '-B', '-W', 'error::ResourceWarning', PACKET + '/plan/test_plan.py'],
        ['python3', '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', 'discover', '-s', PACKET + '/scene', '-p', 'test_*.py', '-v'],
        ['python3', '-B', PACKET + '/scene/retained.py', PACKET + '/scene/native-capture-v8'],
        ['python3', '-B', PACKET + '/verify_prop_bases.py'],
        ['node', PACKET + '/gallery/test_evidence.js', '--require-v8'],
        ['node', PACKET + '/gallery/test_loader.js', '--require-v8'],
    ]
    for command in commands:
        print('COMMAND', ' '.join(command), flush=True)
        subprocess.run(command, cwd=export, check=True)
    print(json.dumps({'status': 'TRACKED_EXPORT_VALIDATED', 'export': str(export),
                      'trackedFiles': len(receipt['files']), 'commandCount': len(commands),
                      'newNativeExecution': False, 'ownerAcceptance': False}), flush=True)


if __name__ == '__main__':
    main()
