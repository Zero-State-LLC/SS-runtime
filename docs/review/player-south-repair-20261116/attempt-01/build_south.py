"""South-only recovered-source geometry proposal. No runtime or animation changes.
ADAPT exact recovered neutral material/geometry recipes in editable/, from
Documents/Codex/2026-10-13/can/outputs/SS-player-bounded-neutral and its aaron-package mirror.
Fixed-length IK adapted from player-all-release-source-20261116/build_source.py:75-86.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ORIGINAL = Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs')
NAMES = ['SS-player-bounded-proportions', 'SS-player-bounded-neutral', 'SS-player-settle-prototype']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    result = {}
    for name in NAMES:
        for path in sorted((ORIGINAL / name).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                result[str(path.relative_to(ORIGINAL))] = sha(path)
    result['benchmark'] = sha(REVIEW / 'bp001-decision-20261116/street-corner-approved-concept.png')
    return result


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def solve(hip, ankle, lengths):
    axis = ankle - hip
    distance = np.linalg.norm(axis)
    a, b = lengths
    assert abs(a-b) < distance < a+b
    axis /= distance
    along = (a*a-b*b+distance*distance)/(2*distance)
    forward = np.array([0., 1., 0.])
    forward -= axis*np.dot(forward, axis)
    forward /= np.linalg.norm(forward)
    return hip + along*axis + math.sqrt(a*a-along*along)*forward


def main():
    before = inventory()
    archive = HERE / 'original-input-hashes.json'
    if archive.exists():
        assert json.loads(archive.read_text()) == before, 'Original source changed'
    else:
        save(archive, before)
    work = HERE / 'editable'
    model = json.loads((work / 'model.json').read_text())
    pose = copy.deepcopy(json.loads((ORIGINAL / NAMES[1] / 'source/samples.json').read_text())[0])
    for leg in pose['legs']:
        leg['hip'][2] = model['neutralHipHeight']
        leg['knee'] = solve(np.array(leg['hip']), np.array(leg['ankle']), model['segmentLengths']).tolist()
    save(work / 'source/samples.json', [pose])
    save(work / 'boot/samples.json', [pose])
    subprocess.run([sys.executable, '-B', str(work / 'boot/material.py')], check=True)
    subprocess.run([sys.executable, '-B', str(work / 'assemble.py')], check=True)
    output = HERE / 'south-neutral.png'
    output.write_bytes((work / 'frames/00.png').read_bytes())
    # Comparison is an export only. Geometry/model generation never consumes this plate.
    paths = [ORIGINAL / NAMES[1] / 'frames/00.png',
             REVIEW / 'player-baggy-south-source-20261116/south-baggy-neutral.png', output]
    labels = ['Recovered neutral', 'Prior flat baggy preference (reference only)', 'Editable geometry proposal 01']
    plate = Image.new('RGB', (1152, 464), '#283036')
    draw = ImageDraw.Draw(plate)
    for i, (path, label) in enumerate(zip(paths, labels)):
        im = Image.open(path).convert('RGBA')
        plate.paste(im, (384*i, 40), im)
        draw.text((384*i+8, 8), label, fill='white')
    plate.save(HERE / 'south-comparison.png')
    cards = ''.join(f'<section><h2>{label}</h2><img src="{src}" width="384" height="416">'
                    f'<h3>Native logical64 ×69.333</h3><img src="{src}" width="64" style="height:69.333333px">'
                    f'<h3>Half logical32 ×34.667</h3><img src="{src}" width="32" style="height:34.666667px"></section>'
                    for label, src in [(labels[0], '../aaron-package/SS-player-bounded-neutral/frames/00.png'),
                                       (labels[1], '../player-baggy-south-source-20261116/south-baggy-neutral.png'),
                                       (labels[2], 'south-neutral.png')])
    (HERE / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>South editable proposal01</title>'
        '<style>body{background:#283036;color:#eee;font:16px system-ui;margin:24px}main{display:flex;gap:20px}section{width:384px}img{display:block}</style>'
        '<h1>South-first editable geometry proposal01</h1><p>PROPOSED, NOT ACCEPTED. Source-only, not native capture. '
        'Recovered hood/coat/equipment paint retained; real lower-body loft/skeleton parameters changed, no bitmap warp repair. '
        'Upper remains layered paint, not a finished rotatable model. No other facing until coordinator recommends south.</p>'
        '<main>'+cards+'</main>')
    assert inventory() == before, 'Original source changed during build'
    save(HERE / 'south-build.json', {'status': 'SOUTH_FIRST_PROPOSED_NOT_ACCEPTED',
        'modelSHA256': sha(work / 'model.json'), 'outputSHA256': sha(output),
        'originalFilesUnchanged': len(before), 'familyExpanded': False,
        'sourceMethod': 'recovered volumetric thigh/calf/boot surfaces with owned UV/material paint',
        'upperMethod': 'retained layered recovered paint, not reconstructed rotatable upper volume',
        'immutableReleasePhases': [5, 13], 'settleSeconds': .375,
        'limits': model['limits']})
    print('South sample ready:', output)


if __name__ == '__main__':
    main()
