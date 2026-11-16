#!/usr/bin/env python3
"""Verify retained slice2 native evidence against xcresult provenance.
ADAPT scripts/import_release_variation_native.py:30-121 (result/tree, attachment census,
source hashes, image facts). Verification only: never reruns simulator or rewrites evidence.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NATIVE = HERE / 'native'
TEST = 'PlayerGroundContactNativeTests/testNativeRendererContactsAcrossCoreTracesSelectionsAndSourceVariants()'
TRACES = ('quarter', 'half', 'full', 'pause')
POLICIES = ('fixed-time', 'distance-phase')
FAMILIES = ('baseline', 'weight-transfer')
EXCLUDED = {'cardinal-full': 91, 'cardinal-half': 166, 'cardinal-quarter': 316, 'collision-stop': 91,
            'dodge': 91, 'reversal': 91, 'stationary': 91, 'wall-slide': 91}
CHANGED = {5, 6, 7, 13, 14, 15}
APPROVED = {4: 'c3a5d87a510040b2ee7ae15db599a0b2c48974ab2b2d851422640cbd4d4f826d',
            12: '85e869ac7fdad2b981adef08655e1473c2db667cb3d25d36c5126ef01131a7c6'}
CAPTURE = re.compile(r'groundcontact-(quarter|half|full|pause)-(fixed-time|distance-phase)-(baseline|weight-transfer)-sample-(\d+)-frame-(\d+)')
# Files whose bytes define what the native test executed.
SOURCE_FILES = ['AppTests/PlayerGroundContactNativeTests.swift', 'project.yml',
    'AppTests/BenchmarkAssets/player-source-s-poses.json',
    'AppTests/GroundContactAssets/player-groundcontact-core-traces.json',
    *[f'AppTests/BenchmarkAssets/player-source-s-{i:02d}.png' for i in range(16)],
    *[f'AppTests/GroundContactAssets/player-groundcontact-candidate-{i:02d}.png' for i in sorted(CHANGED)]]

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())

def validate_result(summary, tree):
    need(summary.get('result') == 'Passed' and summary.get('passedTests') == 1 and summary.get('failedTests') == 0
         and summary.get('skippedTests') == 0 and summary.get('expectedFailures') == 0,
         'Expected exactly1 passing native test; zero/failed/skipped/expected-failure runs rejected')
    cases = []
    def walk(node):
        if node.get('nodeType') == 'Test Case': cases.append(node)
        for child in node.get('children', []): walk(child)
    for node in tree['testNodes']: walk(node)
    need(len(cases) == 1 and cases[0]['nodeIdentifier'] == TEST and cases[0]['result'] == 'Passed',
         'Wrong focused native test identity/result')

def attachments(exports):
    exports = Path(exports).resolve(); captures = {}; records = []
    for case in load(exports / 'manifest.json'):
        for item in case['attachments']:
            path = (exports / item['exportedFileName']).resolve()
            need(path.is_relative_to(exports) and path.is_file(), 'Export path escape or missing export')
            name = item.get('suggestedHumanReadableName', '')
            match = CAPTURE.match(name)
            if match:
                key = match.group(0); need(key not in captures, 'Duplicate native capture'); captures[key] = path
            elif name.startswith('groundcontact-native-records'): records.append(path)
    need(len(captures) == 76 and len(records) == 1, 'Expected exactly76 captures and one record attachment')
    return captures, records[0]

def check_sources(traces_path=None):
    for index, digest in APPROVED.items():
        need(sha(ROOT / f'AppTests/BenchmarkAssets/player-source-s-{index:02d}.png') == digest, 'Approved release5/13 source changed')
    for index in CHANGED:
        candidate = ROOT / f'AppTests/GroundContactAssets/player-groundcontact-candidate-{index:02d}.png'
        need(sha(candidate) == sha(HERE / f'editable-candidate/frames/{index:02d}.png'), 'Bundled candidate differs from editable render')
    need(sha(ROOT / 'AppTests/GroundContactAssets/player-groundcontact-core-traces.json') == sha(HERE / 'core-traces.json'),
         'Bundled core traces differ from executed Swift core trace')
    return {name: sha(ROOT / name) for name in SOURCE_FILES}

def fixed_frame(offset):
    # Intended looping 16-frame 0.5s cycle at 60Hz. Independent of ClipTiming.
    return (offset * 32 // 60) % 16

def recorded_fixed_frame(offset):
    # DEFECT observed in executed test: ClipTiming.frameIndex clamps, never loops.
    return min(offset * 32 // 60, 15)

def validate_records(packet, traces, poses):
    need(packet.get('status') == 'STATIC_NATIVE_RENDERER_NOT_DISPLAY_CADENCE' and packet.get('threshold') is None,
         'Native scope/status or invented threshold changed')
    need(packet['excludedInvalidSouthFacingDodgeOrStationaryTraces'] == EXCLUDED, 'Excluded scenario census changed')
    by_name = {t['name']: t for t in traces}
    need(set(EXCLUDED) | set(TRACES) == set(by_name), 'Core trace census mismatch')
    for name, count in EXCLUDED.items(): need(len(by_name[name]['rows']) == count, f'Excluded row count drift:{name}')
    samples = [r for r in packet['records'] if r['kind'] == 'sample']
    segments = [r for r in packet['records'] if r['kind'] == 'segment']
    need(len(samples) == 2400 and len(segments) == 54, 'Expected2400 sample rows and54 segments')
    selection = []
    for trace in TRACES:
        rows = by_name[trace]['rows']
        for policy in POLICIES:
            for family in FAMILIES:
                group = [r for r in samples if (r['trace'], r['policy'], r['family']) == (trace, policy, family)]
                need(len(group) == {'quarter': 300, 'half': 150, 'full': 75, 'pause': 75}[trace],
                     f'Walking row count drift for {trace}/{policy}/{family}')
                start, travel = None, 0.0
                actual = iter(group)
                for row in rows:
                    travel += math.hypot(row['dxRaw'], row['dyRaw']) / 256
                    if not ((row['dxRaw'] or row['dyRaw'] or row['paused']) and not row['dodgeRemaining']):
                        start = None; continue
                    record = next(actual)
                    need((record['tick'], record['sample']) == (row['tick'], row['sample']), 'Native row/core tick drift')
                    need(record['authoritativeRaw'] == [row['xRaw'], row['yRaw']], 'Native row lost authoritative Q8 position')
                    need(record['texturePath'] == f"groundcontact-{family}-{record['frame']:02d}", 'Texture/frame identity mismatch')
                    qx = row['xRaw'] / 256 - record['snapshotWhole'][0]; qy = row['yRaw'] / 256 - record['snapshotWhole'][1]
                    need([qx, qy] == record['q8MinusSnapshot'] and 0 <= qx < 1 and 0 <= qy < 1, 'Snapshot quantization record invalid')
                    if start is None: start = row['tick']
                    if policy == 'fixed-time':
                        need(record['frame'] == recorded_fixed_frame(row['tick'] - start), 'Fixed-time record drift')
                        expected = fixed_frame(row['tick'] - start)
                    else:
                        expected = int(travel % 120 / 120 * 16)
                        need(record['frame'] == expected, 'Distance-phase selection mismatch')
                    if record['frame'] != expected:
                        selection.append((trace, policy, family, row['tick'], record['frame'], expected))
                    planted = {leg['side'] for leg in poses[record['frame']]['legs'] if leg['contact']}
                    need(set(record['contacts']) == planted, 'Recorded contacts disagree with pose landmarks')
    need(len(selection) == 900 and all(s[1] == 'fixed-time' for s in selection),
         f'Fixed-time defect census changed: {len(selection)} rows')
    return samples, segments, len(selection)

def image_facts(captures):
    digests = {}
    for key, path in captures.items():
        with Image.open(path) as image:
            need(image.format == 'PNG' and image.size == (480, 330), 'Native crop must be PNG160x110 points at3x (480x330)')
            pixels = image.convert('RGBA'); need(len(pixels.getcolors(maxcolors=1 << 24) or ()) > 32, 'Blank/flat native crop')
            digests[key] = hashlib.sha256(pixels.tobytes()).hexdigest()
    changed = unchanged = 0
    for key in [k for k in digests if '-baseline-' in k]:
        other = key.replace('-baseline-', '-weight-transfer-'); need(other in digests, 'Unpaired native capture')
        frame = int(key.rsplit('frame-', 1)[1]); differs = digests[key] != digests[other]
        need(differs == (frame in CHANGED), f'Pair difference disagrees with changed-key set:{key}')
        changed += differs; unchanged += not differs
    need((changed, unchanged) == (33, 5), 'Expected33 changed and5 unchanged native pairs')
    return {'changedPairs': changed, 'unchangedPairs': unchanged, 'rgbaSHA256': dict(sorted(digests.items()))}

def verify(exports, result, query=None):
    query = query or (lambda kind: json.loads(subprocess.check_output(
        ['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True)))
    validate_result(query('summary'), query('tests'))
    captures, record = attachments(exports)
    need(sha(record) == sha(NATIVE / 'native-records.json'), 'Retained records differ from xcresult attachment')
    for key, path in captures.items():
        need(sha(path) == sha(NATIVE / f'{key}.png'), f'Retained capture differs from attachment:{key}')
    need({p.stem for p in NATIVE.glob('groundcontact-*.png')} == set(captures), 'Retained capture census differs')
    hashes = check_sources()
    samples, segments, frozen = validate_records(load(record), load(HERE / 'core-traces.json')['traces'],
                                         load(ROOT / 'AppTests/BenchmarkAssets/player-source-s-poses.json'))
    facts = image_facts(captures)
    return {'status': 'VERIFIED_STATIC_NATIVE_NOT_CADENCE', 'samples': len(samples), 'segments': len(segments),
            'captures': len(captures), 'distancePhaseValid': True, 'fixedTimeValid': False,
            'fixedTimeFrozenRows': frozen,
            'fixedTimeDefect': 'ClipTiming.frameIndex clamps at frame15; executed fixed-time froze after30 ticks. Native fixed-time spans unusable.',
            'sourceHashes': hashes, **facts}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports', type=Path, required=True); parser.add_argument('--xcresult', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = verify(args.exports, args.xcresult)
    except ValueError as error:
        print('VERIFICATION FAILED:', error); sys.exit(1)
    report.pop('rgbaSHA256'); print(json.dumps(report, indent=2))
