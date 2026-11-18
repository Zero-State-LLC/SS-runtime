#!/usr/bin/env python3
"""Prepare/import the single quiet native scene fixture. Never launches a simulator.
ADAPT provenance checks: scripts/import_release_variation_native.py:33-67,116-130.
"""
import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from PIL import Image
import assemble as a

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HARNESS = 'AppTests/SourceSceneContinuationTests.swift'
TEST = 'SourceSceneContinuationTests/testQuietSouthNeutralOrdinaryScene()'
STATUS = 'NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE'
FIXTURE_VERSION = 'source-scene-continuation-003-upright-census'
ZOOMS = (1, 1.25, 1.4)
ORDER = [(arm, zoom) for arm in ('control', 'candidate') for zoom in ZOOMS]
NAMES = {f'source-scene-{arm}-ordinary-z{round(zoom * 100)}-{kind}' for arm, zoom in ORDER for kind in ('native', 'half', 'grayscale')}
CONTROLS = {'painted-player-south.png', 'camera.png', 'building-constrained.png', 'newsbox.png', 'tree.png'}


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return a.digest(path.read_bytes())


def expected_input(root=ROOT, manifest=HERE / 'assembly.json'):
    m = load(manifest)
    blockers, _ = a.validate(m, root)
    a.need(not blockers, 'SOURCE PENDING: ' + ' | '.join(blockers))
    sources = []
    for s in m['sources']:
        reg = s['registration']
        if s['role'] == 'paving':
            a.need(reg['drawSizeWorld'][0] == reg['drawSizeWorld'][1] and reg['rootPixelsTopLeft'] == [0, reg['canvasPixels'][1]], 'Native finite paving requires square bottom-left registration')
        if s['role'] in ('camera', 'player'):
            a.need(all(int(v) == v and abs(v) < 2**31 for v in reg['worldPosition']), 'Native actor position must be integral and bounded')
        sources.append({'role': s['role'], 'file': s['role'] + '.png', 'sha256': s['image']['sha256'],
                        'registration': reg, 'recommendation': 'coordinator-recommended'})
    return {'schema': 'source-scene-native-003', 'fixtureVersion': FIXTURE_VERSION, 'assemblySHA256': sha(manifest),
            'harnessSourceSHA256': sha(root / HARNESS), 'center': m['viewCenterWorld'], 'sources': sources}


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / 'native-inputs-v3'):
    record = expected_input(root, manifest)
    a.need(not output.exists(), 'Preserve prior preparation, use a fresh destination')
    # Validate everything before creating even an empty preparation directory.
    m = load(manifest)
    raw = {s['role']: a.dependency(root, s['image'], a.tracking(root)) for s in m['sources']}
    output.mkdir(parents=True)
    for source in record['sources']:
        (output / source['file']).write_bytes(raw[source['role']])
    (output / 'native-inputs.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def validate_result(summary, tree):
    a.need(summary.get('result') == 'Passed' and summary.get('passedTests') == 1 and summary.get('totalTestCount') == 1 and
           all(summary.get(k) == 0 for k in ('failedTests', 'skippedTests', 'expectedFailures')), 'Need exactly one passing native test, no skipped/expected failures')
    cases = []
    def walk(node):
        if node.get('nodeType') == 'Test Case':
            cases.append(node)
        for child in node.get('children', []):
            walk(child)
    for node in tree['testNodes']:
        walk(node)
    a.need(len(cases) == 1 and cases[0].get('nodeIdentifier') == TEST and cases[0].get('result') == 'Passed', 'Wrong actual native test identity')


def attachments(exports):
    found = {}
    for case in load(exports / 'manifest.json'):
        for item in case['attachments']:
            name = item.get('suggestedHumanReadableName', '')
            match = re.match(r'^(source-scene-(?:(?:control|candidate)-ordinary-z(?:100|125|140)-(?:native|half|grayscale)|records))(?:_|\.|$)', name)
            if not match:
                a.need(not name.startswith('source-scene-'), 'Unexpected native scene attachment/version')
                continue
            key = match.group(1)
            a.need(key not in found, 'Duplicate native attachment')
            path = a.safe(exports, item['exportedFileName'])
            a.need(path.is_file(), 'Missing native attachment')
            found[key] = path
    a.need(set(found) == NAMES | {'source-scene-records'}, 'Need eighteen real images and one records attachment')
    return found


def validate_records(record, prepared, input_sha):
    a.need(record.get('schema') == 'source-scene-records-003' and prepared.get('schema') == 'source-scene-native-003', 'Wrong exact records/preparation schema')
    a.need(record.get('status') == STATUS and record.get('fixture') == 'south-neutral-camera-neutral', 'Wrong native fixture/scope')
    a.need(record.get('fixtureVersion') == prepared.get('fixtureVersion') == FIXTURE_VERSION, 'Wrong exact fixtureVersion')
    a.need(record.get('cameraSourceFrames') == 1 and record.get('playerSourceFrames') == 1, 'Static source count, not clip/family evidence')
    a.need(record.get('inputSHA256') == input_sha and record.get('assemblySHA256') == prepared['assemblySHA256'] and record.get('harnessSourceReadSHA256') == prepared['harnessSourceSHA256'], 'Stale native preparation/harness source/assembly')
    a.need(record.get('sourceSHA256') == {s['role']: s['sha256'] for s in prepared['sources']}, 'Wrong actual native source bytes')
    executable = record.get('loadedTestExecutable', {})
    path, digest = executable.get('path'), executable.get('sha256')
    a.need(isinstance(path, str) and Path(path).is_absolute() and Path(path).name == 'SSRuntimeTests' and Path(path).parent.name == 'SSRuntimeTests.xctest', 'Missing actual loaded test executable path')
    a.need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None, 'Missing actual loaded test executable SHA256')
    captures = record.get('captures', [])
    a.need([(c.get('arm'), c.get('zoom')) for c in captures] == ORDER, 'Need exactly six ordered ordinary captures at 1/1.25/1.4')
    def close_pair(actual, expected, message):
        a.need(isinstance(expected, list) and len(expected) == 2 and all(type(v) in (int, float) and math.isfinite(v) for v in expected), message)
        a.need(isinstance(actual, list) and len(actual) == 2 and all(type(v) in (int, float) and math.isfinite(v) and math.isclose(v, w, rel_tol=0, abs_tol=0.002) for v, w in zip(actual, expected)), message)
    for c in captures:
        a.need(c.get('mode') == 'ordinary' and c.get('name') == f"source-scene-{c['arm']}-ordinary-z{round(c['zoom'] * 100)}", 'Wrong ordinary capture identity')
        a.need(all(c.get(k) is True for k in ('hudVisible', 'controlsRetained', 'fieldVisible', 'fieldUnchanged')), 'HUD/controls/field suppressed')
        a.need(bool(c.get('authorityBefore')) and c.get('authorityBefore') == c.get('authorityAfter'), 'Authority mutated')
        a.need(c.get('solidCount') == 24 and c.get('cameraRange', 0) > 0, 'Missing authoritative geometry')
        a.need(set(c.get('pngSHA256', {})) == {'-native', '-half', '-grayscale'}, 'Wrong image census')
        for key in ('cameraRoot', 'cameraRange', 'cameraHeadingMilli', 'cameraFieldAngleMilli', 'cameraFieldOrigin', 'solidCount', 'authorityBefore'):
            a.need(key in captures[0] and captures[0][key] == c.get(key), 'Control/candidate authority differs: ' + key)
        close_pair(c.get('centerWorld'), prepared['center'], 'Capture center drift')
        actors = c.get('actors', [])
        inventory = c.get('preprojectionInventory', [])
        environment = c.get('expectedEnvironmentNames', [])
        a.need(isinstance(environment, list) and bool(environment) and all(isinstance(name, str) and name.startswith('environment-upright-') for name in environment), 'Missing expected environment cohort')
        a.need(environment == sorted(set(environment)), 'Duplicate or unordered expected environment cohort')
        a.need(environment == captures[0].get('expectedEnvironmentNames'), 'Stale environment cohort across captures')
        a.need(len(actors) == len(inventory) == c.get('uprightCount') == 5 + len(environment) and c.get('environmentCount') == len(environment), 'Exact upright inventory census differs')
        actor_names = [actor.get('name') for actor in actors]
        a.need(actor_names == [actor.get('name') for actor in inventory] and len(set(actor_names)) == len(actor_names), 'Duplicate or omitted inventory/extraction node')
        a.need(actor_names[0] == 'sprite-player' and actor_names[1].startswith('sprite-camera-') and actor_names[2:5] == ['benchmark-building', 'benchmark-prop-0', 'benchmark-prop-1'] and actor_names[5:] == environment, 'Wrong observed actor/environment census')
        for actor, original in zip(actors, inventory):
            for key in ('worldRoot', 'size', 'anchor', 'scale'):
                close_pair(actor.get(key), original.get(key, []), 'Upright registration differs from independent inventory: ' + key)
            a.pair(actor.get('size'), 'upright size', True)
            scale = a.pair(actor.get('scale'), 'upright scale', True)
            a.need(math.isclose(scale[0], scale[1], rel_tol=0, abs_tol=0.00001), 'Nonuniform upright scale')
            a.need(actor.get('rotation') == original.get('rotation') == 0 and actor.get('hidden') is original.get('hidden') is False and actor.get('alpha') == original.get('alpha') and type(actor.get('alpha')) in (int, float) and 0 < actor['alpha'] <= 1, 'Hidden or transformed upright')
            close_pair(actor.get('projectedBasisX'), [c['zoom'] * scale[0], 0], 'Upright X basis was ground-warped or scaled')
            close_pair(actor.get('projectedBasisY'), [0, c['zoom'] * scale[1]], 'Upright Y basis was ground-warped or scaled')
            world = a.pair(actor.get('worldRoot'), 'observed world root')
            delta = a.project([world[0] - prepared['center'][0], world[1] - prepared['center'][1]])
            expected = [prepared['center'][i] + c['zoom'] * delta[i] for i in range(2)]
            close_pair(actor.get('projectedRoot'), expected, 'Projected root differs from midpoint/zoom')
        if c['arm'] == 'candidate':
            for role, index in [('player', 0), ('camera', 1), ('stone', 2)]:
                observed = actors[index]
                reg = next(s['registration'] for s in prepared['sources'] if s['role'] == role)
                anchor = [reg['rootPixelsTopLeft'][0] / reg['canvasPixels'][0], 1 - reg['rootPixelsTopLeft'][1] / reg['canvasPixels'][1]]
                for key, values in [('worldRoot', reg['worldPosition']), ('size', reg['drawSizeWorld']), ('anchor', anchor)]:
                    close_pair(observed.get(key), values, 'Observed registration differs: ' + role + '/' + key)
    for arm in ('control', 'candidate'):
        rows = [c for c in captures if c['arm'] == arm]
        a.need(all(row['preprojectionInventory'] == rows[0]['preprojectionInventory'] for row in rows), 'Stale preprojection inventory across zooms')
        for index in range(len(rows[0]['actors'])):
            for key in ('name', 'worldRoot', 'size', 'anchor', 'scale', 'rotation', 'hidden', 'alpha'):
                a.need(all(row['actors'][index].get(key) == rows[0]['actors'][index].get(key) for row in rows), 'Zoom changed unprojected actor registration')
    for zoom in ZOOMS:
        pair = [c for c in captures if c['zoom'] == zoom]
        for index in (0, 1, 3, 4, *range(5, len(pair[0]['actors']))):
            for key in ('name', 'worldRoot', 'projectedRoot'):
                a.need(pair[0]['actors'][index][key] == pair[1]['actors'][index][key], 'Control/candidate common actor root differs')
        a.need(pair[0]['preprojectionInventory'][5:] == pair[1]['preprojectionInventory'][5:], 'Control/candidate environment inventory differs')
    a.need(set(record.get('controlSHA256', {})) == CONTROLS, 'Original control census differs')
    return captures


def validate_executable(record, expected_executable):
    """Compare actual runtime Bundle executable hash with explicit built test product.

    The installed runtime path is retained, not assumed equal to the build product path.
    This is distinct from reading a current Swift source file and hashing its bytes.
    """
    a.need(expected_executable.is_file(), 'Expected built test executable is missing')
    actual = record['loadedTestExecutable']
    a.need(sha(expected_executable) == actual['sha256'], 'Loaded test executable differs from expected built product')
    return {'loadedPath': actual['path'], 'loadedSHA256': actual['sha256'],
            'expectedBuildPath': str(expected_executable.resolve()), 'expectedBuildSHA256': sha(expected_executable)}


def import_result(result, output, expected_executable, root=ROOT, packet=HERE):
    a.need(not output.exists(), 'Preserve prior native evidence')
    prepared = expected_input(root, packet / 'assembly.json')
    inputs = packet / 'native-inputs-v3' / 'native-inputs.json'
    a.need(load(inputs) == prepared, 'Prepared source manifest drift')
    for s in prepared['sources']:
        a.need(sha(inputs.parent / s['file']) == s['sha256'], 'Prepared image drift')
    def query(kind):
        return json.loads(subprocess.check_output(['xcrun', 'xcresulttool', 'get', 'test-results', kind, '--path', str(result)], text=True))
    summary, tree = query('summary'), query('tests')
    validate_result(summary, tree)
    with tempfile.TemporaryDirectory(prefix='source-scene-import-', dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
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
        for c in captures:
            size = c['nativePixels']
            a.need(len(size) == 2 and size[0] % 704 == 0 and size[1] % 326 == 0 and size[0] // 704 == size[1] // 326 and 1 <= size[0] // 704 <= 4, 'Wrong native crop/scale')
            for suffix, digest in c['pngSHA256'].items():
                path = found[c['name'] + suffix]
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
    report = {'status': STATUS, 'fixtureVersion': FIXTURE_VERSION, 'nativeTests': 1, 'captures': 6, 'images': 18,
              'xcresult': str(result.resolve()), 'inputSHA256': sha(inputs), 'harnessSourceReadSHA256': record['harnessSourceReadSHA256'],
              'testExecutable': executable,
              'ownerAcceptance': False, 'physicalDeviceEvidence': False, 'animationFamilyEvidence': False,
              'files': {p.name: sha(p) for p in sorted(output.iterdir())}}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['prepare', 'import'])
    p.add_argument('--xcresult', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--test-executable', type=Path, help='Exact newly built SSRuntimeTests.xctest/SSRuntimeTests binary, required for import')
    args = p.parse_args()
    try:
        if args.action == 'prepare':
            answer = prepare(output=args.output or HERE / 'native-inputs-v3')
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires --xcresult, fresh --output and --test-executable')
            answer = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(answer, indent=2))
    except (a.Invalid, OSError, ValueError, KeyError, TypeError) as error:
        p.exit(2, str(error) + '\n')
