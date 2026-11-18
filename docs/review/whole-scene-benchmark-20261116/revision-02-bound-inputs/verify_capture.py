#!/usr/bin/env python3
"""Verify slice1 revision 02 (bound inputs). Provenance only, not visual acceptance.
Revision 01 packets are read for comparison, never modified, and are NOT retroactively attested:
pixel equality shows reproduction under bound inputs at this run, not what revision 01 executed."""
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
ROOT = HERE.parents[3]
REVIEW = ROOT / 'docs/review'
CAPTURE = HERE / 'capture'
TEST = 'WholeSceneBoundInputsTests/testBoundInputsRevision02()'
RUNS = [('wholescene', 'control', 'ordinary'), ('wholescene', 'control', 'staged'), ('wholescene', 'diagnostic', 'ordinary'),
        ('wholescene', 'diagnostic', 'staged'), ('paving', 'plaza', 'ordinary'), ('paving', 'muted', 'ordinary')]
ZOOMS, SHEETS = (100, 125, 140), ('native', 'half', 'grayscale')
PLATES = {f'r02-{f}-{a}-{m}-z{z}-{s}' for f, a, m in RUNS for z in ZOOMS for s in SHEETS}
NAME = re.compile(r'r02-(wholescene|paving)-(control|diagnostic|plaza|muted)-(ordinary|staged)-z(100|125|140)-(native|half|grayscale)')
DIMENSIONS = {'native': (2112, 978), 'half': (1056, 489), 'grayscale': (2112, 978)}
ROLES = ['sprite-player', 'sprite-camera-2', 'benchmark-building', 'benchmark-prop-0', 'benchmark-prop-1']
UPRIGHTS = ['painted-player-south', 'camera', 'building-constrained', 'newsbox', 'tree']
RUNTIME = {'env_ground_plaza': 'env_ground_plaza@1x.png', 'env_ground_asphalt': 'env_ground_asphalt@1x.png'}
CAMERA = [('operationalIdle', 4), ('hit', 2), ('criticalEnter', 3), ('destroy', 4), ('fieldOff', 1), ('destroyedIdle', 2)]
CAMERA_FILES = [f'actor_camera_{s}_none_{i:02d}@4x.png' for s, n in CAMERA for i in range(1, n + 1)]
PAVING_SHA = 'c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125'
SWIFT = {'AppTests/WholeSceneBenchmarkTests.swift': '93d9d99f50aade5911a3fbe30edf94413492c40d5ea31016518bd7c7ea0200f0',
         'AppTests/WholeScenePavingTests.swift': 'bbac7ae0ccacbcc3e6ca8e2afcc535b4dea5baa7c28b9141e417434588fcafb8'}
DEFICITS = ('building NOT SOLVED: building-constrained.png fallback, no registered replacement',
            'paving material: muted trial only, seam/repetition pending, no source repair',
            'soft contact shadows absent: none supplied, none authored',
            'Camera field and HUD prominence retained: authoritative/production, diagnostics only')

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def rgba(path):
    with Image.open(path) as image: return image.convert('RGBA').tobytes()

def find_file(name, directory):
    # Exact repository path of the bundled source (the test bundle copies these files unmodified).
    path = ROOT / directory / name
    need(path.is_file(), f'Missing source file {directory}/{name}')
    return path

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
            elif name.startswith('r02-records'): records.append(path)
    need(set(plates) == PLATES and len(records) == 1, 'Expected54 plates and one record attachment')
    return plates, records[0]

def validate_inputs(packet):
    """Bind recorded run-time SHAs to the actual repository source files."""
    need(packet['status'] == 'SLICE1_REVISION02_BOUND_INPUTS_NOT_ACCEPTANCE' and packet['revision'] == 2, 'Scope/status/revision lifted')
    need('does not retroactively attest' in packet['supersedesNothing'], 'Retroactive attestation disclaimer removed')
    need(tuple(packet['openDeficits']) == DEFICITS, 'Open deficits changed or weakened')
    need(set(packet['uprightInputSHA256']) == {n + '.png' for n in UPRIGHTS + ['whole-scene-muted-paving']}, 'Upright input scope changed')
    for name in UPRIGHTS:
        need(packet['uprightInputSHA256'][name + '.png'] == sha(ROOT / f'AppTests/BenchmarkAssets/{name}.png'), f'Upright bytes differ:{name}')
    need(packet['uprightInputSHA256']['whole-scene-muted-paving.png'] == PAVING_SHA == sha(ROOT / 'AppTests/WholeSceneAssets/whole-scene-muted-paving.png'), 'Paving bytes differ')
    need(set(packet['runtimeAssets']) == set(RUNTIME), 'Runtime asset scope changed')
    for asset, path in RUNTIME.items():
        record = packet['runtimeAssets'][asset]
        need(record['path'] == path, f'Runtime asset path changed:{asset}')
        need(record['sha256'] == sha(find_file(path, 'Sources/SurveillanceCore/Resources/RuntimeAssets')), f'Runtime asset bytes differ:{asset}')
    need(sorted(packet['cameraFrameSHA256']) == sorted(CAMERA_FILES), 'Camera frame census changed')
    for name, digest in packet['cameraFrameSHA256'].items():
        need(digest == sha(find_file(name, 'AppTests/BenchmarkAssets')), f'Camera frame bytes differ:{name}')

def validate_captures(packet):
    captures = packet['captures']
    need(sorted((c['fixture'], c['arm'], c['mode'], round(c['zoom'] * 100)) for c in captures)
         == sorted((f, a, m, z) for f, a, m in RUNS for z in ZOOMS), 'Capture census changed')
    hidden = {c['hudHiddenByProduction'] for c in captures}
    need(len(hidden) == 1, 'Production HUD hidden-node state differs between runs')
    for c in captures:
        need(c['name'] == f"r02-{c['fixture']}-{c['arm']}-{c['mode']}-z{round(c['zoom'] * 100)}", 'Capture name/label mismatch')
        need(c['hudVisible'] == c['fieldVisible'] == (c['mode'] == 'ordinary') and c['hudNodeCount'] > 0, 'Visibility mislabelled')
        need([a['name'] for a in c['actors']] == ROLES and set(c['pngSHA256']) == {'-native', '-half', '-grayscale'}, 'Role/suffix census changed')
        need(c['nativePixels'] == list(DIMENSIONS['native']), 'Native dimensions changed')
        expected = 'whole-scene-muted-paving.png' if c['arm'] == 'muted' else RUNTIME['env_ground_plaza']
        need(c['paving'] == expected, 'Paving label mismatch')
    return captures

def r01_counterpart(capture, sheet):
    z = round(capture['zoom'] * 100)
    if capture['fixture'] == 'wholescene':
        return REVIEW / f"whole-scene-benchmark-20261116/capture/wholescene-{capture['arm']}-{capture['mode']}-z{z}-{sheet}.png"
    return REVIEW / f"whole-scene-paving-20261116/capture/paving-{capture['arm']}-ordinary-z{z}-{sheet}.png"

def has_more_than_64_colors(image):
    # Pillow returns None precisely when the actual color count exceeds maxcolors.
    # This preserves >64 semantics without sorting every framebuffer pixel.
    return image.convert('RGB').getcolors(maxcolors=64) is None


def plate_facts(plates, captures):
    for c in captures:
        for suffix, digest in c['pngSHA256'].items():
            need(sha(plates[c['name'] + suffix]) == digest, f'Plate hash disagrees with record:{c["name"]}{suffix}')
    for key, path in plates.items():
        with Image.open(path) as image:
            need(image.format == 'PNG' and image.size == DIMENSIONS[key.rsplit('-', 1)[1]], f'Plate dimensions wrong:{key}')
            rgb = np.asarray(image.convert('RGB'))
            need(has_more_than_64_colors(image), f'Blank plate:{key}')
            if key.endswith('-grayscale'): need(bool((rgb[..., 0] == rgb[..., 1]).all() and (rgb[..., 1] == rgb[..., 2]).all()), f'Grayscale has colour:{key}')
    # Reproduction comparison against the immutable revision-01 plates (reported, never tolerated).
    mismatches = [f"{c['name']}-{s}" for c in captures for s in SHEETS if rgba(plates[f"{c['name']}-{s}"]) != rgba(r01_counterpart(c, s))]
    need(not mismatches, f'Revision-02 does not reproduce revision-01 pixels: {mismatches}')
    return {'r01PixelEqual': len(captures) * 3, 'r01PixelMismatches': mismatches}

def offline_query(kind): return load(CAPTURE / ('summary.json' if kind == 'summary' else 'tests.json'))

def verify(exports, result, query=None):
    query = query or (lambda kind: json.loads(subprocess.check_output(
        ['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True)))
    summary, tree = query('summary'), query('tests')
    validate_result(summary, tree)
    need(offline_query('summary') == summary and offline_query('tests') == tree, 'Retained summary/tree differ from xcresult')
    for path, digest in SWIFT.items(): need(sha(ROOT / path) == digest, f'Revision-01 Swift changed:{path}')
    plates, record = attachments(exports)
    need(sha(record) == sha(CAPTURE / 'r02-records.json'), 'Retained records differ from attachment')
    for key, path in plates.items(): need(sha(path) == sha(CAPTURE / f'{key}.png'), f'Retained plate differs:{key}')
    need({p.stem for p in CAPTURE.glob('r02-*.png')} == PLATES, 'Retained plate census differs')
    packet = load(record)
    validate_inputs(packet)
    captures = validate_captures(packet)
    facts = plate_facts(plates, captures)
    return {'status': 'VERIFIED_BOUND_INPUTS_REVISION02_NOT_ACCEPTANCE', 'plates': len(plates), 'captures': len(captures),
            'boundRuntimeAssets': len(packet['runtimeAssets']), 'boundCameraFrames': len(packet['cameraFrameSHA256']),
            'boundUprightInputs': len(packet['uprightInputSHA256']), **facts}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports', type=Path, required=True); parser.add_argument('--xcresult', type=Path, required=True)
    args = parser.parse_args()
    try: report = verify(args.exports, args.xcresult)
    except ValueError as error: print('VERIFICATION FAILED:', error); sys.exit(1)
    print(json.dumps(report, indent=2))
