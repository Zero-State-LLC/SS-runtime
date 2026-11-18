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
import importlib.util


def import_path(name, path):
    """Private module names keep unittest discovery independent of sys.path order."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


a = import_path('_scene_qa_v5_assemble', Path(__file__).resolve().parent.parent / 'scene-source-assembly-20261116/assemble.py')

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HARNESS = 'AppTests/SceneQARepairTests.swift'
TEST = 'SceneQARepairTests/testQuietSouthNeutralOrdinaryScene()'
STATUS = 'NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE'
FIXTURE_VERSION = 'source-scene-qa-005-footprint-ground'
ZOOMS = (1, 1.25, 1.4)
ORDER = [(arm, zoom) for arm in ('control', 'candidate') for zoom in ZOOMS]
NAMES = {f'source-scene-{arm}-ordinary-z{round(zoom * 100)}-{kind}' for arm, zoom in ORDER for kind in ('native', 'half', 'grayscale')}
CONTROLS = {'painted-player-south.png', 'camera.png', 'building-constrained.png', 'newsbox.png', 'tree.png'}
OLD = HERE.parent / 'scene-source-assembly-20261116'
PLACEMENT_SHA256 = 'b112b8685dd03c1cd1fd0214f7b010e33dbde3e714c5f21e4e48c4e342238e07'


def authority():
    path = OLD / 'authoritative-placement-1014.json'
    a.need(sha(path) == PLACEMENT_SHA256, 'Pinned authoritative placement drift')
    return load(path)


def solid_rows():
    return [{key: row[key] for key in ('id', 'minWorld', 'maxWorld')} for row in authority()['solids']]


def environment_solids():
    # ADAPT EnvironmentLibrary.solidAssetId(forSolidId:) and the fixture's
    # backed permanent-solid census. Mounts/gates are not upright textures.
    return {'environment-upright-env_' + row['id'].replace('-', '_'): row
            for row in authority()['solids']
            if row['id'].startswith('solid-') and row['id'] != 'solid-03-transit-kiosk'}


def expected_depth_items(capture, center):
    solids = environment_solids()
    kiosk = next(row for row in authority()['solids'] if row['id'] == 'solid-03-transit-kiosk')
    items = []
    for actor in capture['actors']:
        name, root = actor['name'], actor['worldRoot']
        solid = kiosk if name == 'benchmark-building' else solids.get(name)
        if name.startswith('environment-upright-'):
            a.need(solid is not None and root == solid['centerWorld'], 'Environment root differs from authority')
        items.append({'name': name, 'worldRoot': root,
                      'footprint': solid['minWorld'] + solid['maxWorld'] if solid else None,
                      'projectedRootY': a.project(root)[1]})
    return items


def validate_repairs(capture, prepared):
    a.need(capture.get('solids') == solid_rows(), 'Exact authoritative solid IDs/bounds differ')
    for solid in capture['solids']:
        a.pair(solid['minWorld'], 'authoritative solid minimum')
        a.pair(solid['maxWorld'], 'authoritative solid maximum')
    a.need(capture['expectedEnvironmentNames'] == sorted(environment_solids()), 'Authoritative environment census differs')
    candidate = capture['arm'] == 'candidate'
    roots = {'sprite-player': next(s['registration']['worldPosition'] for s in prepared['sources'] if s['role'] == 'player'),
             'sprite-camera-3': [496, 672], 'benchmark-building': [512, 640],
             'benchmark-prop-0': [691, 639], 'benchmark-prop-1': [858, 780]}
    roots.update({name: solid['centerWorld'] for name, solid in environment_solids().items()})
    a.need(set(roots) == {row['name'] for row in capture['actors']}, 'Exact authoritative actor cohort differs')
    for actor in capture['actors']:
        a.need(actor['worldRoot'] == roots[actor['name']], 'Actor world root differs from bound authority/source')
    a.need(type(capture.get('playerOutlineAlpha')) in (int, float) and
           capture['playerOutlineAlpha'] == (0 if candidate else 1), 'Player outline treatment differs')
    a.pair(capture.get('playerShadowWorldRoot'), 'shadow root')
    size = a.pair(capture.get('playerShadowSize'), 'shadow size', True)
    a.need(size == capture.get('originalPlayerShadowSize'), 'Existing shadow size changed')
    digest = capture.get('playerShadowTextureSHA256')
    a.need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None and
           digest == capture.get('originalPlayerShadowTextureSHA256'), 'Existing shadow texture changed')
    a.need(capture.get('shadowTreatment') == ('ground-root-existing-soft-shadow' if candidate else 'original-offset-soft-shadow'), 'Wrong shadow treatment')
    if candidate:
        a.need(capture['playerShadowWorldRoot'] == capture['actors'][0]['worldRoot'], 'Shadow must be exactly at player world root')
        projected = a.pair(capture.get('playerShadowProjectedRoot'), 'projected shadow root')
        a.need(all(math.isclose(value, expected, rel_tol=0, abs_tol=0.002)
                   for value, expected in zip(projected, capture['actors'][0]['projectedRoot'])),
               'Projected shadow must match candidate player projected root')
        reg = next(s['registration'] for s in prepared['sources'] if s['role'] == 'paving')
        a.need(reg['worldPosition'] == [0, 0] and reg['drawSizeWorld'] == [2304, 2304], 'Ground source must cover full-world square')
        placement = authority()
        arena = placement['arenaMinWorld'] + [placement['arenaMaxWorld'][i] - placement['arenaMinWorld'][i] for i in range(2)]
        a.need(capture.get('groundBounds') == arena, 'Ground bounds must be exact authoritative arena rectangle without source padding')
        a.need(all(type(value) in (int, float) for value in capture['groundBounds']), 'Ground bounds must be numeric')
        a.need(a.pair(capture.get('groundSourceWorldSize'), 'ground source world size', True) == reg['drawSizeWorld'],
               'Ground source adapter size must match square registration')


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
            a.need(reg['worldPosition'] == [0, 0] and reg['drawSizeWorld'] == [2304, 2304], 'Ground source must cover full-world square')
        if s['role'] in ('camera', 'player'):
            a.need(all(int(v) == v and abs(v) < 2**31 for v in reg['worldPosition']), 'Native actor position must be integral and bounded')
        sources.append({'role': s['role'], 'file': s['role'] + '.png', 'sha256': s['image']['sha256'],
                        'registration': reg, 'recommendation': 'coordinator-recommended'})
    return {'schema': 'source-scene-native-005', 'fixtureVersion': FIXTURE_VERSION, 'assemblySHA256': sha(manifest),
            'harnessSourceSHA256': sha(root / HARNESS), 'center': m['viewCenterWorld'], 'sources': sources}


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / 'native-inputs-v5'):
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
    a.need(record.get('schema') == 'source-scene-records-005' and prepared.get('schema') == 'source-scene-native-005', 'Wrong exact records/preparation schema')
    for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
        a.need(record.get(key, False) is False, 'Unearned native evidence claim: ' + key)
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
        selected = next(row for row in authority()['cameras'] if row['id'] == 3)
        for key, field in [('cameraRoot', 'rootWorld'), ('cameraRange', 'range'), ('cameraHeadingMilli', 'headingMilli'), ('cameraFieldAngleMilli', 'fieldAngleMilli')]:
            a.need(c.get(key) == selected[field], 'Camera differs from pinned authority: ' + key)
        a.need(c.get('authorityBefore') == authority()['authorityBefore'], 'Pinned simulation authority differs')
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
        validate_repairs(c, prepared)
        validate_depth(c, prepared['center'])
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
        for key in ('playerShadowSize', 'playerShadowTextureSHA256', 'originalPlayerShadowSize', 'originalPlayerShadowTextureSHA256'):
            a.need(pair[0].get(key) == pair[1].get(key), 'Control/candidate existing shadow differs: ' + key)
    a.need(set(record.get('controlSHA256', {})) == CONTROLS, 'Original control census differs')
    return captures


def depth_order(items):
    """Portable geometry oracle for SceneQAReviewDepth, no Swift/native invocation.

    A pair shares a view ray only when its x-y intervals overlap. Strict
    world-axis separation supplies edges, not rendered sprite extents.
    """
    items = sorted(items, key=lambda item: item['name'])
    edges = []
    for index, first in enumerate(items):
        af = first['footprint'] or first['worldRoot'] * 2
        for second in items[index + 1:]:
            bf = second['footprint'] or second['worldRoot'] * 2
            if max(af[0] - af[3], bf[0] - bf[3]) > min(af[2] - af[1], bf[2] - bf[1]):
                continue
            def separates(back, front):
                return [{'axis': axis, 'backMinimum': back[i], 'frontMaximum': front[i + 2]}
                        for i, axis in enumerate(('x', 'y')) if back[i] > front[i + 2]]
            forward, reverse = separates(af, bf), separates(bf, af)
            if forward and not reverse:
                edges.append({'back': first['name'], 'front': second['name'], 'separations': forward})
            elif reverse and not forward:
                edges.append({'back': second['name'], 'front': first['name'], 'separations': reverse})
    edges.sort(key=lambda edge: (edge['back'], edge['front']))
    remaining = {item['name']: item for item in items}
    names = []
    while remaining:
        blocked = {edge['front'] for edge in edges if edge['back'] in remaining}
        ready = [item for name, item in remaining.items() if name not in blocked]
        a.need(bool(ready), 'Cyclic authoritative footprint depth constraints')
        next_item = min(ready, key=lambda item: (-item['projectedRootY'], item['name']))
        names.append(next_item['name'])
        del remaining[next_item['name']]
    return {'order': names, 'constraints': edges}


def validate_depth(capture, center):
    """Independent authoritative footprint ordering, never rendered bounds or alpha."""
    actors = capture['actors']
    inventory = capture['preprojectionInventory']
    def finite(value):
        return type(value) in (int, float) and math.isfinite(value)
    for actor, original in zip(actors, inventory):
        for key in ('originalWorldDepth', 'originalLocalZ'):
            a.need(finite(original.get(key)) and actor.get(key) == original[key], 'Original upright depth differs from inventory')
    base = max(item['originalWorldDepth'] for item in inventory)
    a.need(capture.get('depthBase') == base and capture.get('depthBand') == 0.5, 'Depth band must start at original maximum upright depth')
    expected_items = expected_depth_items(capture, center)
    observed_items = capture.get('depthItems')
    a.need(isinstance(observed_items, list) and len(observed_items) == len(expected_items), 'Missing exact depth geometry census')
    for observed, expected in zip(observed_items, expected_items):
        a.need(isinstance(observed, dict) and set(observed) == set(expected), 'Wrong depth geometry fields')
        a.pair(observed['worldRoot'], 'depth geometry world root')
        footprint = observed['footprint']
        a.need(footprint is None or (isinstance(footprint, list) and len(footprint) == 4 and all(finite(v) for v in footprint)), 'Invalid depth footprint numbers')
        for key in ('name', 'worldRoot', 'footprint'):
            a.need(observed[key] == expected[key], 'Depth geometry/footprint differs from bound authority: ' + key)
        a.need(finite(observed['projectedRootY']) and math.isclose(observed['projectedRootY'], expected['projectedRootY'], rel_tol=0, abs_tol=0.002), 'Depth projected-root priority differs')
    derived = depth_order(expected_items)
    a.need(capture.get('depthConstraints') == derived['constraints'], 'Authoritative footprint constraints differ')
    a.need(capture.get('depthOrder') == derived['order'], 'Wrong footprint depth order or deterministic tie-break')
    by_name = {item['name']: item for item in actors}
    ordered = [by_name[name] for name in derived['order']]
    actual = []
    for rank, actor in enumerate(ordered):
        value = actor.get('actualZ')
        expected = base + rank / len(ordered) * 0.5
        a.need(type(actor.get('depthRank')) is int and actor['depthRank'] == rank, 'Wrong unique upright depth rank')
        a.need(finite(value) and base <= value < base + 0.5 and math.isclose(value, expected, rel_tol=0, abs_tol=0.00001), 'Actual upright depth rank mismatch or out of band')
        actual.append(value)
    a.need(len(set(actual)) == len(actual) and all(x < y for x, y in zip(actual, actual[1:])), 'Equal or inverted upright depths')


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
    inputs = packet / 'native-inputs-v5' / 'native-inputs.json'
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
            answer = prepare(output=args.output or HERE / 'native-inputs-v5')
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires --xcresult, fresh --output and --test-executable')
            answer = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(answer, indent=2))
    except (a.Invalid, OSError, ValueError, KeyError, TypeError) as error:
        p.exit(2, str(error) + '\n')
