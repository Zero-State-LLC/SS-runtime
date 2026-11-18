#!/usr/bin/env python3
"""V6 center-only framing evidence. Strict v5 contract reused, never modified.

The explicit adapter first requires exact v6 schemas/version, then supplies copies
with the exact v5 schema identifiers to the unchanged v5 validator. No caller can
choose a version, bypass v5 assertions, or mutate the historical module globals.
"""
import argparse
import copy
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V5 = HERE.parent / 'scene-qa-repair-20261116'


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v5 = import_path('_scene_framing_v6_strict_v5', V5 / 'native.py')
a = v5.a
load, sha = v5.load, v5.sha
attachments, validate_executable = v5.attachments, v5.validate_executable
STATUS, NAMES, ORDER = v5.STATUS, v5.NAMES, v5.ORDER
HARNESS = 'AppTests/SceneQAFramingTests.swift'
TEST = 'SceneQAFramingTests/testQuietSouthNeutralOrdinaryScene()'
FIXTURE_VERSION = 'source-scene-qa-006-control-framing'
INPUT_SCHEMA, RECORD_SCHEMA = 'source-scene-native-006', 'source-scene-records-006'
PREPARED_DIR = 'native-inputs-v6'
CENTER = [684, 724]
V5_RECORD_SHA256 = '9047ffac34ccbd95cf4d22ad939443d5dab8b582409b0426e346d90d7497651f'
CONTROL_NAMES = {'stick': 'control_stick_base', 'dodge': 'control_dodge', 'pause': 'control_pause'}


def bind(output=HERE / 'assembly.json'):
    a.need(not output.exists(), 'Preserve existing framing assembly')
    manifest = load(V5 / 'assembly.json')
    manifest['viewCenterWorld'] = CENTER.copy()
    output.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def expected_input(root=ROOT, manifest=HERE / 'assembly.json'):
    actual = load(manifest)
    previous = load(root / 'docs/review/scene-qa-repair-20261116/assembly.json')
    expected = copy.deepcopy(previous)
    expected['viewCenterWorld'] = CENTER.copy()
    a.need(actual == expected, 'V6 assembly may change only the exact view center')
    prepared = v5.expected_input(root, manifest)
    prepared.update(schema=INPUT_SCHEMA, fixtureVersion=FIXTURE_VERSION,
                    harnessSourceSHA256=sha(root / HARNESS))
    a.need(prepared['center'] == CENTER, 'Wrong v6 center')
    return prepared


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / PREPARED_DIR):
    prepared = expected_input(root, manifest)
    a.need(not output.exists(), 'Preserve prior preparation, use a fresh destination')
    raw = {s['role']: a.dependency(root, s['image'], a.tracking(root)) for s in load(manifest)['sources']}
    output.mkdir(parents=True)
    for source in prepared['sources']:
        (output / source['file']).write_bytes(raw[source['role']])
    (output / 'native-inputs.json').write_text(json.dumps(prepared, indent=2) + '\n')
    return prepared


def validate_result(summary, tree):
    translated = copy.deepcopy(tree)
    cases = []
    def visit(node):
        if node.get('nodeType') == 'Test Case':
            cases.append(node)
        for child in node.get('children', []):
            visit(child)
    for node in translated['testNodes']:
        visit(node)
    a.need(len(cases) == 1 and cases[0].get('nodeIdentifier') == TEST, 'Wrong exact v6 test identity')
    cases[0]['nodeIdentifier'] = v5.TEST
    v5.validate_result(summary, translated)


def control_layout():
    """Independent integer HUDLayout/center-anchor mapping for 704x326, zero insets.
    Sources: HUDLayout.swift:98-173, HUDAnchor.swift:26-57. Not stickZone.
    """
    def rounded(n, d=1000):
        return (n + d // 2) // d
    scale = min(rounded(704 * 1000, 844), rounded(326 * 1000, 390))
    offset = [(704 - rounded(844 * scale)) // 2, (326 - rounded(390 * scale)) // 2]
    result = {}
    for role, (cx, cy, width, height) in {'stick': (104, 286, 144, 144),
                                        'dodge': (760, 286, 88, 88), 'pause': (806, 36, 44, 44)}.items():
        x, y = offset[0] + rounded((cx - width // 2) * scale), offset[1] + rounded((cy - height // 2) * scale)
        w, h = rounded(width * scale), rounded(height * scale)
        x -= (width - w) // 2
        y -= (height - h) // 2
        result[role] = [max(0, min(x, 704 - width)), max(0, min(y, 326 - height)), width, height]
    return result


def expected_controls():
    rows = []
    for role, rect in control_layout().items():
        # HUDRenderer.drawControls scales stick/dodge only. Pause retains
        # SKShapeNode's default one-point stroke (issue250, native2122).
        stroke = 1 if role == 'pause' else 2 * 704 / 896
        rows.append(dict(role=role, nodeName=CONTROL_NAMES[role], layoutBounds=rect, pathBounds=rect,
                         bounds=[rect[0] - stroke / 2, rect[1] - stroke / 2, rect[2] + stroke, rect[3] + stroke],
                         lineWidth=stroke, alpha=1, hidden=False))
    return rows


def rectangle(value, label):
    a.need(isinstance(value, list) and len(value) == 4 and
           all(type(v) in (int, float) and math.isfinite(v) for v in value) and value[2] > 0 and value[3] > 0,
           'Invalid rectangle: ' + label)
    return value


def close_rect(actual, expected, label):
    rectangle(actual, label)
    a.need(all(math.isclose(x, y, rel_tol=0, abs_tol=.002) for x, y in zip(actual, expected)), 'Wrong measured ' + label)


def in_crop(rect):
    x, y, w, h = rect
    return x >= 0 and y >= 0 and x + w <= 704 and y + h <= 326


def overlaps(first, second):
    x, y, w, h = first
    xx, yy, ww, hh = second
    return x < xx + ww and xx < x + w and y < yy + hh and yy < y + h


def actor_canvas(actor, row):
    width = actor['size'][0] * actor['scale'][0] * row['zoom']
    height = actor['size'][1] * actor['scale'][1] * row['zoom']
    root = actor['projectedRoot']
    return [root[0] - row['centerWorld'][0] + 352 - actor['anchor'][0] * width,
            163 - (root[1] - row['centerWorld'][1]) - (1 - actor['anchor'][1]) * height, width, height]


def validate_framing(row):
    frame = row.get('framing', {})
    a.need(frame.get('coordinateSystem') == 'logical-crop-top-left-704x326' and frame.get('safeAreaInsets') == [0, 0, 0, 0], 'Missing exact logical framing coordinates')
    controls = frame.get('visibleControls')
    a.need(isinstance(controls, list) and len(controls) == 3, 'Exact three visible controls required')
    for observed, expected in zip(controls, expected_controls()):
        a.need(observed.get('role') == expected['role'] and observed.get('nodeName') == expected['nodeName'], 'Wrong actual visible control identity')
        a.need(observed.get('hidden') is False and type(observed.get('alpha')) in (int, float) and observed['alpha'] == 1, 'Visible control hidden/transparent')
        a.need(type(observed.get('lineWidth')) in (int, float) and math.isclose(observed['lineWidth'], expected['lineWidth'], rel_tol=0, abs_tol=.00001), 'Visible control stroke changed')
        for key in ('bounds', 'pathBounds', 'layoutBounds'):
            close_rect(observed.get(key), expected[key], 'visible control ' + key)
        a.need(in_crop(observed['bounds']), 'Visible control outside crop')
    actors = frame.get('actorCanvasBounds')
    a.need(isinstance(actors, list) and len(actors) == 2, 'Exact Player/Camera canvas census required')
    for observed, actor in zip(actors, row['actors'][:2]):
        a.need(observed.get('name') == actor['name'], 'Wrong measured actor identity')
        expected = actor_canvas(actor, row)
        close_rect(observed.get('bounds'), expected, 'actor canvas')
        a.need(in_crop(expected), 'Player/Camera canvas outside crop')
        for control in controls:
            a.need(not overlaps(expected, control['bounds']), 'Player/Camera canvas overlaps visible control: ' + actor['name'] + '/' + control['role'])


def validate_records(record, prepared, input_sha):
    a.need(record.get('schema') == RECORD_SCHEMA and prepared.get('schema') == INPUT_SCHEMA, 'Wrong exact v6 schema')
    a.need(record.get('fixtureVersion') == prepared.get('fixtureVersion') == FIXTURE_VERSION, 'Wrong exact v6 fixtureVersion')
    a.need(prepared.get('center') == CENTER, 'Wrong exact v6 center')
    old_record, old_prepared = copy.deepcopy(record), copy.deepcopy(prepared)
    old_record.update(schema='source-scene-records-005', fixtureVersion=v5.FIXTURE_VERSION)
    old_prepared.update(schema='source-scene-native-005', fixtureVersion=v5.FIXTURE_VERSION)
    v5.validate_records(old_record, old_prepared, input_sha)
    baseline_path = V5 / 'native-capture-v5/source-scene-records.json'
    a.need(sha(baseline_path) == V5_RECORD_SHA256, 'Immutable v5 baseline drift')
    baseline = load(baseline_path)
    for key in ('sourceSHA256', 'controlSHA256', 'runtimeSHA256'):
        a.need(record.get(key) == baseline[key], 'Framing-only source bytes changed: ' + key)
    for row, previous in zip(record['captures'], baseline['captures']):
        for key in ('playerShadowWorldRoot', 'playerShadowSize', 'originalPlayerShadowSize',
                    'playerShadowTextureSHA256', 'originalPlayerShadowTextureSHA256',
                    'playerOutlineAlpha', 'shadowTreatment', 'groundBounds', 'groundSourceWorldSize'):
            a.need(row.get(key) == previous.get(key), 'Framing-only treatment changed: ' + key)
        for actor, old_actor in zip(row['actors'], previous['actors']):
            for key in ('name', 'worldRoot', 'size', 'anchor', 'scale', 'rotation', 'hidden', 'alpha',
                        'originalWorldDepth', 'originalLocalZ', 'actualZ', 'depthRank'):
                a.need(actor[key] == old_actor[key], 'Framing-only actor changed: ' + key)
        validate_framing(row)
    return record['captures']


def import_result(result, output, expected_executable, root=ROOT, packet=HERE):
    """ADAPT v5 import_result with explicit v6 input directory and validators."""
    a.need(not output.exists(), 'Preserve prior native evidence')
    prepared = expected_input(root, packet / 'assembly.json')
    inputs = packet / PREPARED_DIR / 'native-inputs.json'
    a.need(load(inputs) == prepared, 'Prepared source manifest drift')
    for source in prepared['sources']:
        a.need(sha(inputs.parent / source['file']) == source['sha256'], 'Prepared image drift')
    def query(kind):
        return json.loads(subprocess.check_output(['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True))
    summary, tree = query('summary'), query('tests')
    validate_result(summary, tree)
    with tempfile.TemporaryDirectory(prefix='scene-framing-import-', dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
        exports = Path(temp) / 'exports'
        subprocess.run(['xcrun', 'xcresulttool', 'export', 'attachments', '--path', str(result), '--output-path', str(exports)], check=True)
        found = attachments(exports)
        record = load(found['source-scene-records'])
        captures = validate_records(record, prepared, sha(inputs))
        executable = validate_executable(record, expected_executable)
        for name, digest in record['controlSHA256'].items():
            a.need(sha(root / 'AppTests/BenchmarkAssets' / name) == digest, 'Original control drift: ' + name)
        a.need(len(record.get('runtimeSHA256', {})) == 2, 'Need exact plaza/asphalt runtime bytes')
        for name, digest in record['runtimeSHA256'].items():
            a.safe(root, name)
            matches = list((root / 'Sources/SurveillanceCore/Resources/RuntimeAssets').rglob(Path(name).name))
            a.need(len(matches) == 1 and sha(matches[0]) == digest, 'Runtime ground asset drift')
        for row in captures:
            size = row['nativePixels']
            a.need(len(size) == 2 and size[0] % 704 == 0 and size[1] % 326 == 0 and size[0] // 704 == size[1] // 326 and 1 <= size[0] // 704 <= 4, 'Wrong native crop/scale')
            for suffix, digest in row['pngSHA256'].items():
                path = found[row['name'] + suffix]
                a.need(sha(path) == digest, 'Attachment differs from captured bytes')
                expected = tuple(v // 2 for v in size) if suffix == '-half' else tuple(size)
                with Image.open(path) as image:
                    a.need(image.format == 'PNG' and image.size == expected, 'Wrong native/half/grayscale dimensions')
                    image.verify()
        output.mkdir(parents=True)
        for name, path in found.items():
            shutil.copyfile(path, output / (name + ('.json' if name.endswith('records') else '.png')))
        shutil.copyfile(exports / 'manifest.json', output / 'attachment-manifest.json')
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (output / 'tests.json').write_text(json.dumps(tree, indent=2) + '\n')
    report = dict(status=STATUS, fixtureVersion=FIXTURE_VERSION, nativeTests=1, captures=6, images=18,
                  xcresult=str(result.resolve()), inputSHA256=sha(inputs), harnessSourceReadSHA256=record['harnessSourceReadSHA256'],
                  testExecutable=executable, ownerAcceptance=False, physicalDeviceEvidence=False, animationFamilyEvidence=False,
                  files={path.name: sha(path) for path in sorted(output.iterdir())})
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['bind', 'prepare', 'import'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--xcresult', type=Path)
    parser.add_argument('--test-executable', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'bind':
            result = bind(args.output or HERE / 'assembly.json')
        elif args.action == 'prepare':
            result = prepare(output=args.output or HERE / PREPARED_DIR)
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires --xcresult, fresh --output and --test-executable')
            result = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
