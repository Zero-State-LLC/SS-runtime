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


def validate_records(packet, traces, poses):
    need(packet.get('status') == 'STATIC_NATIVE_RENDERER_NOT_DISPLAY_CADENCE' and packet.get('threshold') is None,
         'Native scope/status or invented threshold changed')
    need(packet['excludedInvalidSouthFacingDodgeOrStationaryTraces'] == EXCLUDED, 'Excluded scenario census changed')
    by_name = {t['name']: t for t in traces}
    need(set(EXCLUDED) | set(TRACES) == set(by_name), 'Core trace census mismatch')
    for name, count in EXCLUDED.items(): need(len(by_name[name]['rows']) == count, f'Excluded row count drift:{name}')
    samples = [r for r in packet['records'] if r['kind'] == 'sample']
    segments = [r for r in packet['records'] if r['kind'] == 'segment']
    need(len(samples) == 2400 and len(segments) == 116, 'Expected2400 sample rows and116 segments')
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
                    expected = fixed_frame(row['tick'] - start) if policy == 'fixed-time' else int(travel % 120 / 120 * 16)
                    need(record['frame'] == expected, f'{policy} selection mismatch (runtime#238 freeze rejected)')
                    planted = {leg['side'] for leg in poses[record['frame']]['legs'] if leg['contact']}
                    need(set(record['contacts']) == planted, 'Recorded contacts disagree with pose landmarks')
                frames = [f['frame'] for f in group]
                need(set(frames) == set(range(16)), f'Not all16 frames selected:{trace}/{policy}/{family}')
                need(sum(b < a for a, b in zip(frames, frames[1:])) >= 1, f'No loop wrap:{trace}/{policy}/{family}')
    need(packet.get('captureCount') == 76 and packet.get('fixedTimeLoop', '').endswith('runtime#238 corrected'),
         'Capture count/loop declaration drift')
    reconstruct(samples, segments, traces, poses)
    return samples, segments

TOLERANCE = 0.002  # SpriteKit Float32 tree conversion; same bound the native XCTest asserts.

def project_root(whole):
    wx, wy = whole[0] - 736, whole[1] - 654
    return (352 + (wx - wy) / math.sqrt(2), 163 + (wx + wy) / (2 * math.sqrt(2)))

def reconstruct(samples, segments, traces, poses):
    """Independent numeric rebuild of root, contacts and planted segments from snapshot positions."""
    by_name = {t['name']: t for t in traces}
    for trace in TRACES:
        for policy in POLICIES:
            for family in FAMILIES:
                group = iter(r for r in samples if (r['trace'], r['policy'], r['family']) == (trace, policy, family))
                active, rebuilt = {'left': [], 'right': []}, []
                def close(side):
                    points = active[side]
                    if len(points) > 1:
                        rebuilt.append((side, len(points), max(math.dist(a, b) for a in points for b in points)))
                    active[side] = []
                for row in by_name[trace]['rows']:
                    if not ((row['dxRaw'] or row['dyRaw'] or row['paused']) and not row['dodgeRemaining']):
                        close('left'); close('right'); continue
                    record = next(group)
                    root = project_root(record['snapshotWhole'])
                    need(math.dist(root, record['projectedRoot']) <= TOLERANCE, 'Projected root disagrees with snapshot projection')
                    for leg in poses[record['frame']]['legs']:
                        if not leg['contact']: close(leg['side']); continue
                        point = (root[0] + leg['toe'][0], root[1] - 0.5 * leg['toe'][1])
                        recorded = record['contacts'].get(leg['side'])
                        need(recorded is not None and math.dist(point, recorded) <= TOLERANCE, 'Contact point disagrees with reconstruction')
                        active[leg['side']].append(point)
                close('left'); close('right')
                actual = [(s['side'], s['samples'], s['nativeSceneSpanLogical']) for s in segments
                          if (s['trace'], s['policy'], s['family']) == (trace, policy, family)]
                need([(a, b) for a, b, _ in actual] == [(a, b) for a, b, _ in rebuilt], f'Segment census disagrees:{trace}/{policy}/{family}')
                for (_, _, span), (_, _, mine) in zip(actual, rebuilt):
                    need(abs(span - mine) <= 2 * TOLERANCE, f'Segment span disagrees:{trace}/{policy}/{family}')

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

def offline_query(kind):
    """Retained xcresult JSON for portable (no xcrun) verification. Live CLI compares against the bundle."""
    return load(NATIVE / ('summary.json' if kind == 'summary' else 'tests.json'))

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
    runtime = load(record)['runtimeBundledSourceSHA256']
    need(len(runtime) == 24, 'Runtime bundled source census changed')
    for name, digest in runtime.items():
        folder = 'GroundContactAssets' if 'groundcontact' in name else 'BenchmarkAssets'
        need(sha(ROOT / 'AppTests' / folder / name) == digest, f'Executed bundled bytes differ from source:{name}')
    need(load(NATIVE / 'summary.json') == query('summary'), 'Retained summary differs from xcresult')
    need(load(NATIVE / 'tests.json') == query('tests'), 'Retained test tree differs from xcresult')
    samples, segments = validate_records(load(record), load(HERE / 'core-traces.json')['traces'],
                                         load(ROOT / 'AppTests/BenchmarkAssets/player-source-s-poses.json'))
    facts = image_facts(captures)
    return {'status': 'VERIFIED_STATIC_NATIVE_NOT_CADENCE', 'samples': len(samples), 'segments': len(segments),
            'captures': len(captures), 'distancePhaseValid': True, 'fixedTimeValid': True,
            'runtimeBundledSources': len(runtime),
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
