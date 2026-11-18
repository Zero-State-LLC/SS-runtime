#!/usr/bin/env python3
"""BP-008 source-key proposal. Reuse original paint/geometry, never simulate movement.
ADAPT: supplied SS-player-bounded-proportions/{assemble.py,thigh.py,boot/material.py}
and player-all-release-source-20261116/build_source.py:75-86 (fixed-length IK).
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs')
BASE = SOURCE / 'SS-player-bounded-proportions'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')

def inventory():
    return {str(p.relative_to(SOURCE)): sha(p) for name in
            ('SS-player-bounded-proportions', 'SS-player-bounded-neutral', 'SS-player-settle-prototype')
            for p in sorted((SOURCE / name).rglob('*')) if p.is_file()}

def solve(hip, ankle):
    # Exact existing vetted 12.5/14.5 source solver, imported rather than approximated.
    path = HERE.parent / 'player-all-release-source-20261116/build_source.py'
    spec = importlib.util.spec_from_file_location('existing_source', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve(np.array(hip), np.array(ankle)).tolist()

def candidate(poses):
    result = copy.deepcopy(poses)
    for index, pose in enumerate(result):
        phase = index % 8
        # Preserve exact entry/exit keys 01/05/09/13 and all foot trajectories.
        # Reduce recovery apex by <=0.6 source units, never add bounce or speed.
        reduction = .6 * math.sin(math.pi * (phase - 4) / 4) if phase > 4 else 0.0
        for leg in pose['legs']:
            if reduction:
                leg['hip'][2] -= reduction
                leg['knee'] = solve(leg['hip'], leg['ankle'])
        pose['groundedRecoveryReduction'] = reduction
    return result

def build(render=True):
    before = inventory()
    save(HERE / 'original-input-hashes.json', before)
    baseline = json.loads((BASE / 'source/samples.json').read_text())
    revised = candidate(baseline)
    save(HERE / 'baseline-poses.json', baseline)
    save(HERE / 'candidate-poses.json', revised)
    work = HERE / 'editable-candidate'
    work.mkdir(exist_ok=True)
    for src, dest in ((BASE / 'source', work / 'source'), (BASE / 'boot/source', work / 'boot/source')):
        shutil.copytree(src, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('material.py', 'source.png', 'four-facing-source.png', 'registration.json', 'retained-body-contact.png'):
        shutil.copy2(BASE / 'boot' / name, work / 'boot' / name)
    for name in ('assemble.py', 'thigh.py'):
        shutil.copy2(BASE / name, work / name)
    save(work / 'source/samples.json', revised)
    save(work / 'boot/samples.json', revised)
    shutil.copytree(BASE / 'frames', HERE / 'baseline-frames', dirs_exist_ok=True)
    # Ten lower-body keys are unchanged. Reuse their exact original paint/depth
    # caches and render only the six revised keys with the same source renderer.
    shutil.copytree(BASE / 'boot/frames', work / 'boot/frames', dirs_exist_ok=True)
    material = (work / 'boot/material.py').read_text()
    old = "for i,sample in enumerate(json.loads((R/'samples.json').read_text())):"
    if material.count(old) != 1:
        raise ValueError('Original material render entry drift')
    material = material.replace(old, "for i,sample in [(i,s) for i,s in enumerate(json.loads((R/'samples.json').read_text())) if i in {5,6,7,13,14,15}]:")
    (work / 'boot/material.py').write_text(material)
    if render:
        for name in ('boot/material.py', 'assemble.py'):
            proc = subprocess.run([sys.executable, str(work / name)], cwd=work,
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True, timeout=180)
            (HERE / (Path(name).stem + '-render.log')).write_text(proc.stdout + proc.stderr)
            if proc.returncode:
                raise RuntimeError(proc.stderr[-3000:])
    after = inventory()
    if before != after:
        raise ValueError('Original source changed during build')
    save(HERE / 'source-proposal.json', {
        'status': 'BOUNDED_BRISK_GAIT_SOURCE_KEY_COMPARISON_NOT_VISUALLY_ACCEPTED',
        'cycleSeconds': .5, 'maximumWorldUnitsPerSecond': 240,
        'settleSecondsUnchanged': .375,
        'correction': 'Reduce recovery pelvis rise with fixed 12.5/14.5 IK, retain all toe/heel/ankle/contact targets, paint, costume sides and original 05/13 keys. Not a faster jog and not a foot-slip cure.',
        'preservedKeysOneBased': [1,5,9,13],
        'maximumRecoveryReductionSourceUnits': .6,
        'supportPattern': 'Unchanged right support 01-04, left support09-12. Original lift intervals05-08 and13-16 retained, not claimed newly grounded contacts.',
        'sourceProjection': 'xpx=192+6*x; ypx=336+6*(0.5*y-sqrt(0.75)*z)',
        'originalFilesUnchanged': len(before),
        'sourceFiles': {str(p.relative_to(HERE)): sha(p) for p in sorted(work.rglob('*')) if p.is_file()},
        'limits': ['Only six recovery keys change. No new flight pattern, no accepted gait selection.',
                   'Fixed exported support landmarks mean baseline/candidate modeled slip is intentionally equal.',
                   'Human normal-speed review must decide whether reduced recovery rise improves weight transfer.',
                   'No native rendering, live cadence or device claim. No existing settle sequence modified.']})
    print('Source proposal built. Original files unchanged:', len(before))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args()
    build(not args.no_render)
