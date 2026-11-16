#!/usr/bin/env python3
"""Verify whole-scene benchmark capture provenance. ADAPT ../player-ground-contact-20261116/verify_native.py.
Verification only: never reruns the simulator. Byte identity is provenance, not visual acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
from PIL import Image
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAPTURE = HERE / 'capture'
TEST = 'WholeSceneBenchmarkTests/testWholeSceneControlAndCompositionDiagnosticOrdinaryAndStaged()'
ARMS, MODES, ZOOMS, SHEETS = ('control', 'diagnostic'), ('ordinary', 'staged'), (100, 125, 140), ('native', 'half', 'grayscale')
PLATES = {f'wholescene-{a}-{m}-z{z}-{s}' for a in ARMS for m in MODES for z in ZOOMS for s in SHEETS}
NAME = re.compile(r'wholescene-(control|diagnostic)-(ordinary|staged)-z(100|125|140)-(native|half|grayscale)')
REFERENCE = ROOT / 'docs/review/bp001-decision-20261116/street-corner-approved-concept.png'
REFERENCE_SHA = '49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb'
RETAINED_CONTROL = ROOT / 'docs/review/bp001-reference-trial-20261116/plates/BP001-trial-quiet-street-midpoint-z125-native.png'
INPUTS = ['painted-player-south', 'camera', 'building-constrained', 'newsbox', 'tree']
SOURCE_FILES = ['AppTests/WholeSceneBenchmarkTests.swift', 'App/BenchmarkReviewArt.swift', 'project.yml']
DEFICITS = ('building NOT SOLVED: building-constrained.png fallback, no registered replacement',
            'paving material NOT SOLVED: env_ground_plaza retained',
            'soft contact shadows absent: none supplied, none authored',
            'Camera field and HUD prominence retained: authoritative/production, diagnostics only')
ROLES = ['sprite-player', 'sprite-camera-2', 'benchmark-building', 'benchmark-prop-0', 'benchmark-prop-1']
SUFFIXES = {'-native', '-half', '-grayscale'}
# Captured at simulator 3x: 704x326 points. Half and grayscale derive from native.
DIMENSIONS = {'native': (2112, 978), 'half': (1056, 489), 'grayscale': (2112, 978)}
# Input scope: only these five upright textures are hashed by the test. Paving/asphalt come from
# EnvironmentTextures (production bundle) and camera playback frames from CameraPlaybackTests; their
# bytes are NOT recorded by this capture and are reported as unbound inputs, not verified ones.
UNBOUND_INPUTS = ['env_ground_plaza', 'env_ground_asphalt', 'CameraPlaybackTests.candidateFrames()']

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def rgba(path):
    with Image.open(path) as image: return image.size, image.convert('RGBA').tobytes()

def validate_result(summary, tree):
    need(summary.get('result') == 'Passed' and summary.get('passedTests') == 1 and summary.get('failedTests') == 0
         and summary.get('skippedTests') == 0 and summary.get('expectedFailures') == 0,
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
            name = item['suggestedHumanReadableName']
            match = NAME.match(name)
            if match:
                need(match.group(0) not in plates, 'Duplicate plate'); plates[match.group(0)] = path
            elif name.startswith('wholescene-records'): records.append(path)
    need(set(plates) == PLATES and len(records) == 1, 'Expected36 plates and one record attachment')
    return plates, records[0]

def validate_records(packet):
    need(packet['status'] == 'WHOLE_SCENE_DIAGNOSTIC_NOT_CORRECTION_NOT_ACCEPTANCE', 'Scope/status lifted')
    need(tuple(packet['openDeficits']) == DEFICITS, 'Open deficits changed, removed or weakened')
    captures = packet['captures']
    need(sorted((c['arm'], c['mode'], round(c['zoom'] * 100)) for c in captures)
         == sorted((a, m, z) for a in ARMS for m in MODES for z in ZOOMS), 'Capture census changed')
    for c in captures:
        need(c['hudVisible'] == c['fieldVisible'] == (c['mode'] == 'ordinary'), 'Ordinary/staged visibility mislabelled')
        need(c['hudNodeCount'] > 0, 'HUD missing from fixture')
        need([a['name'] for a in c['actors']] == ROLES, 'Upright role census changed')
        need(set(c['pngSHA256']) == SUFFIXES, 'Sheet suffix census changed')
        need(c['nativePixels'] == list(DIMENSIONS['native']), 'Native capture dimensions changed')
        need(c['name'] == f"wholescene-{c['arm']}-{c['mode']}-z{round(c['zoom'] * 100)}", 'Capture name/label mismatch')
    need(set(packet['inputSHA256']) == {n + '.png' for n in INPUTS}, 'Input hash scope changed')
    for name in INPUTS:
        need(packet['inputSHA256'][name + '.png'] == sha(ROOT / f'AppTests/BenchmarkAssets/{name}.png'), f'Input bytes differ:{name}')
    return captures

def plate_facts(plates, captures):
    for capture in captures:
        for suffix, digest in capture['pngSHA256'].items():
            need(sha(plates[capture['name'] + suffix]) == digest, f'Plate hash disagrees with record:{capture["name"]}{suffix}')
    for key, path in plates.items():
        with Image.open(path) as image:
            need(image.format == 'PNG' and len(image.convert('RGB').getcolors(1 << 24) or ()) > 64, f'Blank or invalid plate:{key}')
            need(image.size == DIMENSIONS[key.rsplit('-', 1)[1]], f'Plate dimensions wrong:{key}')
            if key.endswith('-grayscale'):
                rgb = np.asarray(image.convert('RGB')); need(bool((rgb[..., 0] == rgb[..., 1]).all() and (rgb[..., 1] == rgb[..., 2]).all()), f'Grayscale plate has colour:{key}')
    # Control must reproduce the retained BP001 z125 plate; any difference is reported, never tolerated.
    size, mine = rgba(plates['wholescene-control-ordinary-z125-native'])
    rsize, retained = rgba(RETAINED_CONTROL)
    differing = sum(mine[i:i + 4] != retained[i:i + 4] for i in range(0, min(len(mine), len(retained)), 4)) if size == rsize else None
    control = {'size': list(size), 'retainedSize': list(rsize), 'differingPixels': differing,
               'sha': hashlib.sha256(mine).hexdigest(), 'retainedSHA': hashlib.sha256(retained).hexdigest()}
    need(size == rsize and differing == 0, f'Retained control mismatch: {control}')
    changed = sorted(f'{m}-z{z}' for m in MODES for z in ZOOMS
                     if rgba(plates[f'wholescene-control-{m}-z{z}-native'])[1] != rgba(plates[f'wholescene-diagnostic-{m}-z{z}-native'])[1])
    need(len(changed) == 6, 'Diagnostic arm identical to control in some view')
    staged = [(a, z) for a in ARMS for z in ZOOMS
              if rgba(plates[f'wholescene-{a}-ordinary-z{z}-native'])[1] != rgba(plates[f'wholescene-{a}-staged-z{z}-native'])[1]]
    need(len(staged) == 6, 'Staged view not distinct from ordinary in both arms')
    return {'retainedControl': control, 'diagnosticDiffersFromControl': changed, 'stagedDiffersFromOrdinary': len(staged)}

def offline_query(kind): return load(CAPTURE / ('summary.json' if kind == 'summary' else 'tests.json'))

def verify(exports, result, query=None):
    query = query or (lambda kind: json.loads(subprocess.check_output(
        ['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True)))
    summary, tree = query('summary'), query('tests')
    validate_result(summary, tree)
    need(offline_query('summary') == summary and offline_query('tests') == tree, 'Retained summary/tree differ from xcresult')
    need(sha(REFERENCE) == REFERENCE_SHA, 'Approved concept benchmark changed')
    plates, record = attachments(exports)
    need(sha(record) == sha(CAPTURE / 'wholescene-records.json'), 'Retained records differ from attachment')
    for key, path in plates.items(): need(sha(path) == sha(CAPTURE / f'{key}.png'), f'Retained plate differs:{key}')
    need({p.stem for p in CAPTURE.glob('wholescene-*.png')} == PLATES, 'Retained plate census differs')
    captures = validate_records(load(record))
    facts = plate_facts(plates, captures)
    return {'status': 'VERIFIED_PROVENANCE_DIAGNOSTIC_NOT_ACCEPTANCE', 'plates': len(plates), 'captures': len(captures),
            'sourceHashes': {n: sha(ROOT / n) for n in SOURCE_FILES}, 'unboundInputs': UNBOUND_INPUTS, **facts}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports', type=Path, required=True); parser.add_argument('--xcresult', type=Path, required=True)
    args = parser.parse_args()
    try: report = verify(args.exports, args.xcresult)
    except ValueError as error: print('VERIFICATION FAILED:', error); sys.exit(1)
    print(json.dumps(report, indent=2))
