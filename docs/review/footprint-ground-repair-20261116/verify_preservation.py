#!/usr/bin/env python3
"""Independent historical/production byte preservation and actual baseline pixel check."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = '09f1432b25dc573d829e6181799ea18a37ca7c2e'
V7 = ROOT / 'docs/review/building-perspective-detail-20261116/scene/native-capture-v7'
V8 = HERE / 'scene/native-capture-v8'
PROTECTED = ('App/', 'Sources/', 'AppTests/BuildingPerspectiveSceneTests.swift',
             'AppTests/SceneQAReviewDepth.swift', 'SPEC_BASELINE.md',
             'docs/review/building-perspective-detail-20261116/',
             'docs/review/scene-qa-framing-20261116/',
             'docs/review/scene-qa-repair-20261116/',
             'docs/review/footprint-consistency-20261116/')


def require(value, message):
    if not value:
        raise ValueError(message)


def preserved():
    raw = subprocess.check_output(['git', 'ls-tree', '-r', '-z', BASE], cwd=ROOT)
    count = 0
    for row in raw.split(b'\0'):
        if not row:
            continue
        metadata, name = row.split(b'\t', 1)
        path = name.decode()
        if not any(path == p or path.startswith(p) for p in PROTECTED):
            continue
        mode, kind, digest = metadata.decode().split()
        require(kind == 'blob', 'Unexpected protected entry: ' + path)
        current = ROOT / path
        require(current.is_file() and not current.is_symlink(), 'Missing/aliased protected file: ' + path)
        actual = subprocess.check_output(['git', 'hash-object', '--no-filters', '--', path], cwd=ROOT).decode().strip()
        require(actual == digest, 'Historical/production bytes changed: ' + path)
        count += 1
    require(count > 100, 'Vacuous protected file census')
    return {'referenceCommit': BASE, 'protectedTrackedFiles': count, 'exactGitBlobEquality': True,
            'scope': list(PROTECTED)}


def building_crop_census():
    record = json.loads((V7 / 'source-scene-records.json').read_text())
    results = []
    for row in record['captures']:
        if row['arm'] != 'candidate':
            continue
        visible, outside = [], []
        for actor in row['actors']:
            if actor['name'] != 'benchmark-building' and 'environment-upright' not in actor['name']:
                continue
            require(actor['rotation'] == 0 and actor['scale'] == [1, 1], 'Unexpected building transform')
            w, h = [v * row['zoom'] for v in actor['size']]
            ax, ay = actor['anchor']
            x, y = actor['projectedRoot']
            cx, cy = row['centerWorld']
            x0, y0 = x - cx + 352 - ax * w, 163 - (y - cy) - (1 - ay) * h
            intersects = x0 < 704 and x0 + w > 0 and y0 < 326 and y0 + h > 0
            entry = {'name': actor['name'], 'logicalCanvasBounds': [x0, y0, w, h]}
            (visible if intersects else outside).append(entry)
        require(len(visible) + len(outside) == 14, 'Incomplete building census')
        results.append({'zoom': row['zoom'], 'possiblyVisible': visible, 'entireCanvasOutside': outside})
    require(len(results) == 3, 'Missing zoom census')
    return {'method': 'Conservative full sprite canvas versus 704x326 crop, not inferred visible alpha/contact',
            'source': 'immutable actual V7 candidate records, same building registration/framing required for V8',
            'views': results}


def baseline_pixels():
    checks = []
    for zoom in (100, 125, 140):
        for treatment in ('native', 'half', 'grayscale'):
            old = V7 / f'source-scene-candidate-ordinary-z{zoom}-{treatment}.png'
            new = V8 / f'source-scene-control-ordinary-z{zoom}-{treatment}.png'
            with Image.open(old) as a, Image.open(new) as b:
                aa, bb = a.convert('RGBA'), b.convert('RGBA')
                require(aa.size == bb.size and aa.tobytes() == bb.tobytes(), 'Baseline RGBA drift: ' + new.name)
                checks.append({'zoom': zoom / 100, 'treatment': treatment, 'dimensions': list(aa.size),
                               'rgbaSHA256': hashlib.sha256(aa.tobytes()).hexdigest(), 'exactPixels': True})
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--with-capture', action='store_true')
    args = parser.parse_args()
    result = {'preservation': preserved(), 'buildingCropCensus': building_crop_census(),
              'actualCaptureCompared': args.with_capture}
    if args.with_capture:
        result['baselinePixels'] = baseline_pixels()
    print(json.dumps(result, indent=2))
