#!/usr/bin/env python3
"""Bind the bounded v5 seam repair without rewriting v4 or reauthoring uprights."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'docs/review/scene-source-assembly-20261116'
GROUND_SHA = 'f4a3f542d8879b036c1a1979ab5fa03356b69350181fb526e190098982191dac'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}


def expected():
    manifest = json.loads((OLD / 'assembly.json').read_text())
    source = HERE / 'ground/ground-patch-square.png'
    if sha(source) != GROUND_SHA:
        raise ValueError('Source changed after coordinator review')
    paving = next(s for s in manifest['sources'] if s['role'] == 'paving')
    registration = {'canvasPixels': [4608, 4608], 'rootPixelsTopLeft': [0, 4608],
                    'worldPosition': [0, 0], 'drawSizeWorld': [2304, 2304], 'kind': 'ground',
                    'coordinates': 'WORLD_X_RIGHT_Y_UP_SOURCE_TOP_LEFT'}
    paving['image'] = dependency(source)
    paving['registration'] = registration
    paving['recommendation'] = {'reviewerRole': 'coordinator', 'decision': 'recommended',
        'scope': 'bounded-material-layout', 'sourceSHA256': GROUND_SHA,
        'registrationSHA256': hashlib.sha256(json.dumps(registration, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'evidence': dependency(HERE / 'COORDINATOR-GROUND.md'),
        'transcription': 'Bounded continuous-ground seam repair only. Square source is uniformly sampled, clipped to authoritative arena[0,0,2304,1536]. No layout/authority/source admission or owner acceptance.'}
    for path in [ROOT / 'intent/2026-11-16-scene-qa-repair.md', ROOT / 'AppTests/SceneQAReviewDepth.swift',
                 HERE / 'ground/build.py', HERE / 'ground/manifest.json']:
        manifest['contextDependencies'].append(dependency(path))
    manifest['qaRepair'] = {'issue': 249, 'groundBoundsWorld': [0, 0, 2304, 1536],
                            'sourceUprightsUnchanged': True, 'ownerAcceptance': False}
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = HERE / 'assembly.json'
    text = json.dumps(expected(), indent=2) + '\n'
    if args.check:
        if output.read_text() != text:
            raise ValueError('Bound source assembly drift')
        print('Bound v5 assembly matches exact original uprights, source recommendation and dependencies')
    else:
        with output.open('x') as stream:
            stream.write(text)
        print(output)
