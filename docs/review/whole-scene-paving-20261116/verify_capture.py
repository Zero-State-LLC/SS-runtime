#!/usr/bin/env python3
"""Verify the muted-paving native trial. ADAPT ../whole-scene-benchmark-20261116/verify_capture.py.
Provenance only: never reruns the simulator, never claims visual acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAPTURE = HERE / 'capture'
TEST = 'WholeScenePavingTests/testMutedPavingVersusPlazaOrdinaryOnly()'
ARMS, ZOOMS, SHEETS = ('plaza', 'muted'), (100, 125, 140), ('native', 'half', 'grayscale')
PLATES = {f'paving-{a}-ordinary-z{z}-{s}' for a in ARMS for z in ZOOMS for s in SHEETS}
NAME = re.compile(r'paving-(plaza|muted)-ordinary-z(100|125|140)-(native|half|grayscale)')
DIMENSIONS = {'native': (2112, 978), 'half': (1056, 489), 'grayscale': (2112, 978)}
ROLES = ['sprite-player', 'sprite-camera-2', 'benchmark-building', 'benchmark-prop-0', 'benchmark-prop-1']
PAVING = ROOT / 'AppTests/WholeSceneAssets/whole-scene-muted-paving.png'
PAVING_SOURCE = Path('/Users/appliedalchemylabs/.jcode/generated-images/1794806293758-ig_0a14a4739e7f6a34016afa91ec2a2487d0a32bc6c445c7818d.png')
PAVING_SHA = 'c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125'
INPUTS = ['painted-player-south', 'camera', 'building-constrained', 'newsbox', 'tree']
PRIOR_PACKET = ROOT / 'docs/review/whole-scene-benchmark-20261116/capture'
PRIOR_TEST = ROOT / 'AppTests/WholeSceneBenchmarkTests.swift'
PRIOR_TEST_SHA = '93d9d99f50aade5911a3fbe30edf94413492c40d5ea31016518bd7c7ea0200f0'
OPEN = ('seam/repetition pending: opposite-edge RGB mean abs difference about 13-14/255, not mathematically seamless',
        'building NOT SOLVED: building-constrained.png fallback', 'soft contact shadows absent',
        'Camera field and HUD prominence retained')

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def rgba(path):
    with Image.open(path) as image: return image.size, image.convert('RGBA').tobytes()

def validate_result(summary, tree):
    need(summary.get('result') == 'Passed' and summary.get('passedTests') == 1 and summary.get('totalTestCount') == 1
         and summary.get('failedTests') == 0 and summary.get('skippedTests') == 0 and summary.get('expectedFailures') == 0,
         'Expected exactly1 passing test; zero/failed/skipped/expected-failure runs rejected')
    cases = []
    def walk(node):
        if node.get('nodeType') == 'Test Case': cases.append(node)
        for child in node.get('children', []): walk(child)
    for node in tree['testNodes']: walk(node)
    need(len(cases) == 1 and cases[0]['nodeIdentifier'] == TEST and cases[0]['result'] == 'Passed', 'Wrong test identity/result')

def attachments(exports):
    exports = Path(exports).resolve(); plates, records = {}, []
    for case in load(exports / 'manifest.json'):
        for item in case['attachments']:
            path = (exports / item['exportedFileName']).resolve()
            need(path.is_relative_to(exports) and path.is_file(), 'Export path escape or missing export')
            name = item['suggestedHumanReadableName']; match = NAME.match(name)
            if match:
                need(match.group(0) not in plates, 'Duplicate plate'); plates[match.group(0)] = path
            elif name.startswith('paving-records'): records.append(path)
    need(set(plates) == PLATES and len(records) == 1, 'Expected18 plates and one record attachment')
    return plates, records[0]

def edge_mad(path):
    p = np.asarray(Image.open(path).convert('RGB')).astype(float)
    return float(abs(p[:, 0] - p[:, -1]).mean()), float(abs(p[0] - p[-1]).mean())

def validate_records(packet):
    need(packet['status'] == 'PAVING_MATERIAL_TRIAL_NOT_ACCEPTANCE', 'Scope/status lifted')
    need(tuple(packet['openItems']) == OPEN, 'Open items changed or weakened')
    need(packet['pavingSource'] == {'bundleName': 'whole-scene-muted-paving.png', 'sha256': PAVING_SHA, 'pixels': [1254, 1254],
                                    'tileUnits': 128, 'slabsPerTile': '4x4 authored', 'worldUnitsPerSlab': 32}, 'Paving provenance drift')
    need(set(packet['inputSHA256']) == {n + '.png' for n in INPUTS + ['whole-scene-muted-paving']}, 'Input hash scope changed')
    need(packet['inputSHA256']['whole-scene-muted-paving.png'] == PAVING_SHA, 'Executed paving bytes differ from source')
    for name in INPUTS: need(packet['inputSHA256'][name + '.png'] == sha(ROOT / f'AppTests/BenchmarkAssets/{name}.png'), f'Input bytes differ:{name}')
    captures = packet['captures']
    need(sorted((c['arm'], round(c['zoom'] * 100)) for c in captures) == sorted((a, z) for a in ARMS for z in ZOOMS), 'Capture census changed')
    hidden = {c['hudHiddenByProduction'] for c in captures}
    for c in captures:
        need(c['mode'] == 'ordinary' and c['fieldVisible'] is True and c['hudNodeCount'] > 0, 'Not an ordinary capture')
        need(c['name'] == f"paving-{c['arm']}-ordinary-z{round(c['zoom'] * 100)}", 'Capture name/label mismatch')
        need([a['name'] for a in c['actors']] == ROLES and set(c['pngSHA256']) == {'-native', '-half', '-grayscale'}, 'Role/suffix census changed')
        need(c['nativePixels'] == list(DIMENSIONS['native']), 'Native dimensions changed')
    need(len(hidden) == 1, 'Production HUD hidden-node state differs between arms')
    for z in ZOOMS:
        roots = [[a['projectedRoot'] for a in c['actors']] for c in captures if round(c['zoom'] * 100) == z]
        need(roots[0] == roots[1], f'Upright roots differ between arms at z{z}')
    return captures

def plate_facts(plates, captures):
    for c in captures:
        for suffix, digest in c['pngSHA256'].items():
            need(sha(plates[c['name'] + suffix]) == digest, f'Plate hash disagrees with record:{c["name"]}{suffix}')
    for key, path in plates.items():
        with Image.open(path) as image:
            need(image.format == 'PNG' and image.size == DIMENSIONS[key.rsplit('-', 1)[1]], f'Plate dimensions wrong:{key}')
            rgb = np.asarray(image.convert('RGB'))
            need(len(np.unique(rgb.reshape(-1, 3), axis=0)) > 64, f'Blank plate:{key}')
            if key.endswith('-grayscale'): need(bool((rgb[..., 0] == rgb[..., 1]).all() and (rgb[..., 1] == rgb[..., 2]).all()), f'Grayscale plate has colour:{key}')
    changed = [z for z in ZOOMS if rgba(plates[f'paving-plaza-ordinary-z{z}-native'])[1] != rgba(plates[f'paving-muted-ordinary-z{z}-native'])[1]]
    need(len(changed) == 3, 'Muted paving identical to plaza in some zoom')
    return {'armsDifferAtZooms': changed}

def offline_query(kind): return load(CAPTURE / ('summary.json' if kind == 'summary' else 'tests.json'))

def verify(exports, result, query=None):
    query = query or (lambda kind: json.loads(subprocess.check_output(
        ['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True)))
    summary, tree = query('summary'), query('tests')
    validate_result(summary, tree)
    need(offline_query('summary') == summary and offline_query('tests') == tree, 'Retained summary/tree differ from xcresult')
    need(sha(PAVING) == PAVING_SHA, 'Bundled paving asset changed')
    if PAVING_SOURCE.exists(): need(sha(PAVING_SOURCE) == PAVING_SHA, 'Paving differs from generated source')
    need(sha(PRIOR_TEST) == PRIOR_TEST_SHA, 'Prior WholeSceneBenchmarkTests.swift changed')
    need(len(list(PRIOR_PACKET.glob('wholescene-*.png'))) == 36, 'Prior 36 plates missing')
    prior = load(PRIOR_PACKET / 'wholescene-records.json')
    for c in prior['captures']:
        for suffix, digest in c['pngSHA256'].items(): need(sha(PRIOR_PACKET / f"{c['name']}{suffix}.png") == digest, 'Prior plate bytes changed')
    plates, record = attachments(exports)
    need(sha(record) == sha(CAPTURE / 'paving-records.json'), 'Retained records differ from attachment')
    for key, path in plates.items(): need(sha(path) == sha(CAPTURE / f'{key}.png'), f'Retained plate differs:{key}')
    need({p.stem for p in CAPTURE.glob('paving-*.png')} == PLATES, 'Retained plate census differs')
    captures = validate_records(load(record))
    facts = plate_facts(plates, captures)
    lr, tb = edge_mad(PAVING)
    return {'status': 'VERIFIED_PROVENANCE_TRIAL_NOT_ACCEPTANCE', 'plates': len(plates), 'captures': len(captures),
            'sourceEdgeMeanAbsDiff': {'leftRight': round(lr, 3), 'topBottom': round(tb, 3), 'seamless': False},
            'unboundInputs': load(record)['unboundInputs'], **facts}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports', type=Path, required=True); parser.add_argument('--xcresult', type=Path, required=True)
    args = parser.parse_args()
    try: report = verify(args.exports, args.xcresult)
    except ValueError as error: print('VERIFICATION FAILED:', error); sys.exit(1)
    print(json.dumps(report, indent=2))
