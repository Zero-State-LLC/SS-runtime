"""Explicit audit of preserved pilot01, never falsely passes when originals are absent."""
import argparse
import json
from pathlib import Path
import garment_renderer

parser=argparse.ArgumentParser()
parser.add_argument('--pilot-root',type=Path,required=True)
args=parser.parse_args()
here=Path(__file__).resolve().parent
inventory=json.loads((here/'pilot01-immutable-inventory.json').read_text())
for name,expected in inventory.items():
    path=args.pilot_root/name
    if not path.is_file():
        raise SystemExit('Original pilot unavailable: '+str(path))
    if garment_renderer.sha(path)!=expected:
        raise SystemExit('Original pilot changed: '+str(path))
print(f'PASS: all {len(inventory)} original pilot files unchanged, including source inputs, renderer, strict tests, preview and red log.')
