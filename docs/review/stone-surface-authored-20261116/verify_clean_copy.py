"""Verify actual entrypoints with only this packet and two tracked external inputs.
No historical attempt is executed or rewritten. No visual-design changes are made.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXTERNAL = (
    'docs/review/bp001-decision-20261116/street-corner-approved-concept.png',
    'Sources/SurveillanceCore/Resources/contracts/civic-seam-arena-004.json',
)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    for item in json.loads((HERE/'inputs/provenance.json').read_text())['inputs']:
        assert sha(HERE/'inputs'/item['file']) == item['sha256'], item['file']
    scratch = Path(os.environ.get('JCODE_SCRATCH_DIR', str(HERE)))
    with tempfile.TemporaryDirectory(prefix='stone-clean-copy-', dir=scratch) as directory:
        root = Path(directory)
        packet = root/HERE.relative_to(ROOT)
        shutil.copytree(HERE, packet, ignore=shutil.ignore_patterns('__pycache__', 'stone-clean-copy-*'))
        for relative in EXTERNAL:
            subprocess.run(['git', 'ls-files', '--error-unmatch', relative], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
            target = root/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            # Export committed bytes, not the working tree or any untracked siblings.
            target.write_bytes(subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=ROOT))
        assert not (packet.parent/'stone-editable-master-20261116').exists()
        print('ISOLATED ROOT:', root, flush=True)
        print('EXTERNAL INPUTS: committed benchmark and arena contract only', flush=True)
        subprocess.run([sys.executable, str(packet/'author_mesh.py')], cwd=root, check=True)
        assert sha(packet/'mesh.json') == sha(HERE/'mesh.json'), 'authored mesh changed'
        subprocess.run([sys.executable, str(packet/'replay.py')], cwd=root, check=True)
        exports = list(HERE.glob('*.png')) + list((HERE/'surfaces').iterdir())
        for original in exports:
            assert sha(original) == sha(packet/original.relative_to(HERE)), str(original)
        old_reg = json.loads((HERE/'registration.json').read_text())
        new_reg = json.loads((packet/'registration.json').read_text())
        old_reg.pop('sourceSHA256')
        new_reg.pop('sourceSHA256')
        assert old_reg == new_reg, 'registration mapping changed'
        subprocess.run([sys.executable, str(packet/'replay_painted.py')], cwd=root, check=True)
        assert sha(packet/'painted-direct-replay.png') == sha(HERE/'preview-alpha.png')
        subprocess.run([sys.executable, str(packet/'test_source.py')], cwd=root, check=True)
        print(f'PASS: author mesh byte-identical, {len(exports)} existing PNG/SVG exports byte-identical, registration mapping unchanged, direct painted replay identical, nine source tests passed.', flush=True)
        # Only metadata changes because the executable and input provenance changed.
        shutil.copy2(packet/'registration.json', HERE/'registration.json')
        print('Updated source hashes only in packet registration.json.', flush=True)

if __name__ == '__main__':
    main()
