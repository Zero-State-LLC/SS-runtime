#!/usr/bin/env python3
"""V7 isolated building-only binding/import. No simulator launch and no recommendations.
ADAPT v6 native.py import_result and v5 retained.py by private function globals.
Every historical packet remains read-only. The v6 candidate is BOTH arms' baseline.
"""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path
import re
import types
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V6 = HERE.parent.parent / 'scene-qa-framing-20261116'

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

v6 = import_path('_building_v7_v6', V6 / 'native.py')
v5, a = v6.v5, v6.a
V5 = v6.V5
load, sha = v6.load, v6.sha
validate_executable = v6.validate_executable
STATUS, NAMES, ORDER = v6.STATUS, v6.NAMES, v6.ORDER
HARNESS = 'AppTests/BuildingPerspectiveSceneTests.swift'
TEST = 'BuildingPerspectiveSceneTests/testQuietSouthNeutralOrdinaryScene()'
FIXTURE_VERSION = 'source-scene-building-007-perspective-detail'
INPUT_SCHEMA, RECORD_SCHEMA = 'source-scene-native-007', 'source-scene-records-007'
PREPARED_DIR = 'native-inputs-v7'
CENTER = [684, 724]
BASELINE_SHA = '1cc28f757fb6e9e7ed6e53843c745bcb63f8adc42a2eef6413362582eac4930d'
BASE_ROLES = ['paving', 'camera', 'player', 'stone']
BUILDING_ROLES = ['kiosk', 'context-01', 'context-02', 'context-04', 'context-05']
TARGETS = {'kiosk': 'solid-03-transit-kiosk', 'context-01': 'solid-01-residential-west',
           'context-02': 'solid-02-residential-north', 'context-04': 'solid-04-civic-west',
           'context-05': 'solid-05-civic-dais'}


# Read-only committed runtime source bytes checked against git HEAD on 2026-11-16.
# V6 did not record these per-building hashes. This is an independent source pin,
# NOT a retroactive claim that v6 measured them.
CONTEXT_HASHES = {
    'env_solid_01_residential_west': '1171bd8f9ff905b96e54cb33aac6ea98779b712f4119d2fa76593a2c693bdf6e',
    'env_solid_02_residential_north': '6c19e10ce277fe32c7085ab263ef7bbcb8f4c121509dd1053400bca097a5e154',
    'env_solid_04_civic_west': 'b1d9002bd547eb482190fa28e4c53557220a37eabbdceb54297186a04a7edb0b',
    'env_solid_05_civic_dais': '04a5ee7285c65271c67e3ad7649f9234413b38a05fa14483f1397f16f9bd4cb6',
    'env_solid_06_service_yard_a': '1ab4163fc697f478659dbe1117823474614bf899a048ecfe3702ca0d5cbcd0ab',
    'env_solid_07_service_yard_b': 'ce95b12fc9f3b3bde1c15d50f3f224d58bc53dffba4dfdcc4f7a3e4c41056616',
    'env_solid_08_service_divider': '4dcf193a7fe2b1ef6e8b9f87e3a5ec5eaefb0f96b3ad416a68aa81bf1b1d77ba',
    'env_solid_09_grid_island_a': 'a82bc7fa044f2a10e949be7acd1d15c7cc19d77a95f43bb021652f7a16fa5aaa',
    'env_solid_10_grid_island_b': '5e30a3bb7e6e2956d586a7c0fcb76eb3f7dce29a1de478260915b1ea11afcaa2',
    'env_solid_11_court_column_a': 'dc9e40e5db5ffc8889db3fb3019ba968d9f38306934304e33090266d50cd0782',
    'env_solid_12_court_column_b': '263ae419fe140746d282aa05519e1468e425a6b1b831dcdd0fde10de445228c0',
    'env_solid_13_phoenix_west': '7c53e2d05db5fd65af539183908dd7c8651e5d256b170dc9ed2db5c10e6d559a',
    'env_solid_14_phoenix_east': '14b3bfcb7ae6bb9bb7347eebfa2844ef55d9c85a2ece6c6cb35d5a25d6c8ba5c',
}


def node_name(solid):
    return 'benchmark-building' if solid == TARGETS['kiosk'] else 'environment-upright-env_' + solid.replace('-', '_')


def baseline():
    path = V6 / 'native-capture-v6/source-scene-records.json'
    a.need(sha(path) == BASELINE_SHA, 'Immutable v6 native baseline drift')
    record = load(path)
    a.need(sha(V6 / 'assembly.json') == record['assemblySHA256'], 'Immutable v6 assembly drift')
    a.need(sha(V6 / 'native-inputs-v6/native-inputs.json') == record['inputSHA256'], 'Immutable v6 preparation drift')
    return record


def dependency(record, root=ROOT):
    a.need(isinstance(record, dict) and set(record) == {'path', 'sha256'}, 'Exact dependency fields required')
    path = a.safe(root, record['path'])
    a.need(path.is_file() and not path.is_symlink() and sha(path) == record['sha256'], 'Dependency missing/changed: ' + record['path'])
    return path


def vertices(solid):
    x, y = solid['minWorld']; xx, yy = solid['maxWorld']
    return [[x, y], [xx, y], [xx, yy], [x, yy]]


def close(actual, expected, label, tolerance=.002):
    if isinstance(expected, list):
        a.need(isinstance(actual, list) and len(actual) == len(expected), 'Wrong ' + label)
        for x, y in zip(actual, expected):
            close(x, y, label, tolerance)
    else:
        a.need(type(actual) in (int, float) and math.isfinite(actual) and math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance), 'Wrong ' + label)


def validate_building(source, binding, root=ROOT):
    role = source['role']
    a.need(role in TARGETS and binding['role'] == role, 'Unknown building role')
    a.need(set(binding) == {'role', 'nodeName', 'solidID', 'groundPixelsTopLeft'}, 'Exact building correspondence fields required')
    solid = next(row for row in v5.authority()['solids'] if row['id'] == TARGETS[role])
    a.need(binding['solidID'] == solid['id'] and binding['nodeName'] == node_name(solid['id']), 'Wrong target building')
    reg = source['registration']
    a.need(set(reg) == {'canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld'}, 'Exact building registration fields required')
    for field in reg:
        a.pair(reg[field], field, field in ('canvasPixels', 'drawSizeWorld'))
    expected_root = [512, 640] if role == 'kiosk' else solid['centerWorld']
    a.need(reg['worldPosition'] == expected_root, 'Building root differs from explicit authority')
    a.need(all(0 <= x <= n for x, n in zip(reg['rootPixelsTopLeft'], reg['canvasPixels'])), 'Root outside source canvas')
    pixels = binding['groundPixelsTopLeft']
    a.need(isinstance(pixels, list) and len(pixels) == 4, 'Four explicit ground vertices required')
    for pixel, world in zip(pixels, vertices(solid)):
        a.pair(pixel, 'ground pixel')
        a.need(all(0 <= x <= n for x, n in zip(pixel, reg['canvasPixels'])), 'Ground vertex outside source canvas')
        local = [(pixel[0] - reg['rootPixelsTopLeft'][0]) * reg['drawSizeWorld'][0] / reg['canvasPixels'][0],
                 (reg['rootPixelsTopLeft'][1] - pixel[1]) * reg['drawSizeWorld'][1] / reg['canvasPixels'][1]]
        close(local, list(a.project([world[i] - expected_root[i] for i in range(2)])), 'source geometry ground correspondence')
    image = dependency(source['image'], root)
    with Image.open(image) as im:
        a.need(im.format == 'PNG' and list(im.size) == reg['canvasPixels'] and im.mode == 'RGBA', 'Building PNG registration/mode mismatch')
        im.verify()
    rec = source['recommendation']
    a.need(source['status'] == 'recommended' and rec['reviewerRole'] == 'coordinator' and
           rec['decision'] == 'recommended' and rec['scope'] == 'isolated-ordinary-scene' and
           rec['sourceSHA256'] == source['image']['sha256'], 'Coordinator must recommend exact building bytes')
    dependency(rec['evidence'], root)
    a.need(isinstance(source.get('dependencies'), list) and len(source['dependencies']) >= 2, 'Editable source and registration dependencies required')
    for record in source['dependencies']:
        dependency(record, root)


def validate_manifest(manifest, root=ROOT):
    base = load(V6 / 'assembly.json')
    a.need(manifest.get('schema') == 'building-perspective-assembly-007' and manifest.get('fixtureVersion') == FIXTURE_VERSION, 'Unknown building assembly version')
    a.need(manifest.get('viewCenterWorld') == CENTER and manifest.get('baselineRecordSHA256') == BASELINE_SHA, 'Wrong immutable comparison/framing')
    a.need(manifest.get('contextDependencies') == base['contextDependencies'], 'Non-building dependencies changed')
    a.need(manifest.get('sources', [])[:4] == base['sources'], 'V6 candidate sources/registrations/recommendations changed')
    a.need([s['role'] for s in manifest['sources']] == BASE_ROLES + BUILDING_ROLES, 'Nine ordered exact sources required')
    a.need([b['role'] for b in manifest.get('buildings', [])] == BUILDING_ROLES, 'Five ordered exact building bindings required')
    # Independently validate the unchanged v6 binding and every original source byte.
    v6.expected_input(root, V6 / 'assembly.json')
    baseline()
    for source, binding in zip(manifest['sources'][4:], manifest['buildings']):
        validate_building(source, binding, root)
    return manifest


def bind(recommendations, output=HERE / 'assembly.json', root=ROOT):
    """Consume coordinator-authored source objects, never author a recommendation.

    recommendations JSON: {schema:building-perspective-recommendations-007,
    sources:[five exact source objects], buildings:[five correspondence objects]}.
    """
    a.need(not output.exists(), 'Preserve existing v7 binding')
    rec = load(recommendations)
    a.need(set(rec) == {'schema', 'sources', 'buildings'} and rec['schema'] == 'building-perspective-recommendations-007', 'Unknown coordinator recommendation schema')
    old = load(V6 / 'assembly.json')
    result = dict(schema='building-perspective-assembly-007', fixtureVersion=FIXTURE_VERSION,
                  baselineRecordSHA256=BASELINE_SHA, viewCenterWorld=CENTER,
                  contextDependencies=old['contextDependencies'], sources=old['sources'] + rec['sources'], buildings=rec['buildings'])
    validate_manifest(result, root)
    output.write_text(json.dumps(result, indent=2) + '\n')
    return result


def expected_input(root=ROOT, manifest=HERE / 'assembly.json'):
    m = validate_manifest(load(manifest), root)
    return dict(schema=INPUT_SCHEMA, fixtureVersion=FIXTURE_VERSION, assemblySHA256=sha(manifest),
                harnessSourceSHA256=sha(root / HARNESS), baselineRecordSHA256=BASELINE_SHA,
                center=CENTER, buildings=m['buildings'],
                sources=[dict(role=s['role'], file=s['role'] + '.png', sha256=s['image']['sha256'],
                              registration=s['registration'], recommendation='coordinator-recommended') for s in m['sources']])


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / PREPARED_DIR):
    result = expected_input(root, manifest)
    a.need(not output.exists(), 'Preserve previous preparation')
    m = load(manifest)
    raw = [dependency(s['image'], root).read_bytes() for s in m['sources']]
    output.mkdir(parents=True)
    for source, data in zip(result['sources'], raw):
        (output / source['file']).write_bytes(data)
    (output / 'native-inputs.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def validate_result(summary, tree):
    # Private exact-test adapter, not a rewritten result or a native-run claim.
    validator = types.FunctionType(v5.validate_result.__code__, dict(v5.validate_result.__globals__, TEST=TEST))
    validator(summary, tree)


def validate_attachment_manifest(manifest):
    a.need(isinstance(manifest, list) and len(manifest) == 1 and manifest[0].get('testIdentifier') == TEST, 'Wrong exact export manifest test identity')
    rows = manifest[0].get('attachments', [])
    a.need(isinstance(rows, list) and len(rows) == 19, 'Exactly nineteen exported fixture attachments required')
    names, exported = [], []
    devices = set()
    for row in rows:
        name = row.get('suggestedHumanReadableName', '')
        match = re.fullmatch(r'(source-scene-(?:(?:control|candidate)-ordinary-z(?:100|125|140)-(?:native|half|grayscale)|records))(?:_[^/]+)?\.(?:png|json)', name)
        a.need(match is not None and row.get('isAssociatedWithFailure') is False, 'Invalid/failed fixture attachment')
        key = match.group(1)
        suffix = '.json' if key == 'source-scene-records' else '.png'
        filename = row.get('exportedFileName')
        a.need(isinstance(filename, str) and Path(filename).name == filename and filename.endswith(suffix), 'Invalid export file identity')
        a.need(name.endswith(suffix), 'Wrong exported attachment type')
        device = row.get('deviceId')
        a.need(isinstance(device, str) and bool(device), 'Missing capture device identity')
        devices.add(device); names.append(key); exported.append(filename)
    a.need(set(names) == NAMES | {'source-scene-records'} and len(set(names)) == len(names) and len(set(exported)) == len(exported), 'Duplicate/missing export attachment')
    a.need(len(devices) == 1, 'Mixed export devices')
    return names


def attachments(exports):
    validate_attachment_manifest(load(exports / 'manifest.json'))
    return v6.attachments(exports)


def expected_building_hashes(row, prepared, root=ROOT):
    sources = {s['role']: s for s in prepared['sources']}
    replaced = {b['nodeName']: b['role'] for b in prepared['buildings']} if row['arm'] == 'candidate' else {}
    result = {}
    for actor in row['actors']:
        name = actor['name']
        if name in replaced:
            result[name] = sources[replaced[name]]['sha256']
        elif name == 'benchmark-building':
            result[name] = sources['stone']['sha256']
        elif name.startswith('environment-upright-'):
            asset = name.removeprefix('environment-upright-')
            matches = list((root / 'Sources/SurveillanceCore/Resources/RuntimeAssets').rglob(asset + '@1x.png'))
            a.need(len(matches) == 1 and sha(matches[0]) == CONTEXT_HASHES.get(asset), 'Unmodified context source drift ' + asset)
            result[name] = CONTEXT_HASHES[asset]
    return result


def footprint_expected(row, prepared):
    sources = {s['role']: s for s in prepared['sources']}
    bindings = {b['nodeName']: b for b in prepared['buildings']} if row['arm'] == 'candidate' else {}
    solids = {node_name(s['id']): s for s in v5.authority()['solids'] if s['id'].startswith('solid-')}
    result = []
    for actor in row['actors']:
        name = actor['name']
        if name not in solids:
            continue
        world = vertices(solids[name])
        projected = [[CENTER[i] + row['zoom'] * a.project([v[j] - CENTER[j] for j in range(2)])[i] for i in range(2)] for v in world]
        witness = dict(nodeName=name, worldVertices=world, projectedGround=projected,
                       correspondence='authority-only-baseline-source-not-rederived')
        if name in bindings:
            binding = bindings[name]; source = sources[binding['role']]; reg = source['registration']
            local = [[(p[0] - reg['rootPixelsTopLeft'][0]) * reg['drawSizeWorld'][0] / reg['canvasPixels'][0],
                      (reg['rootPixelsTopLeft'][1] - p[1]) * reg['drawSizeWorld'][1] / reg['canvasPixels'][1]] for p in binding['groundPixelsTopLeft']]
            source_projected = [[actor['projectedRoot'][i] + v[i] * row['zoom'] * actor['scale'][i] for i in range(2)] for v in local]
            close(source_projected, projected, 'source vertex versus authoritative projection')
            witness.update(correspondence='explicit-source-geometry', role=binding['role'], sourceSHA256=source['sha256'],
                           groundPixelsTopLeft=binding['groundPixelsTopLeft'], localVertices=local, projectedSource=source_projected)
        result.append(witness)
    return result


def validate_records(record, prepared, input_sha):
    a.need(record.get('schema') == RECORD_SCHEMA and prepared.get('schema') == INPUT_SCHEMA, 'Wrong exact v7 schema')
    a.need(record.get('fixtureVersion') == prepared.get('fixtureVersion') == FIXTURE_VERSION, 'Wrong exact v7 fixtureVersion')
    a.need('syntheticFixture' not in record and 'syntheticFixture' not in prepared, 'Synthetic evidence is not native evidence')
    old = baseline()
    for key in ('status', 'fixture', 'cameraSourceFrames', 'playerSourceFrames', 'controlSHA256', 'runtimeSHA256'):
        a.need(record.get(key) == old[key], 'Immutable v6 metadata differs: ' + key)
    for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
        a.need(record.get(key, False) is False, 'Unearned evidence claim')
    a.need(record.get('baselineRecordSHA256') == prepared.get('baselineRecordSHA256') == BASELINE_SHA, 'Missing immutable v6 reference')
    a.need(prepared.get('center') == CENTER, 'Framing center changed')
    for key, value in [('inputSHA256', input_sha), ('assemblySHA256', prepared['assemblySHA256']), ('harnessSourceReadSHA256', prepared['harnessSourceSHA256'])]:
        a.need(record.get(key) == value, 'Stale preparation/source: ' + key)
    a.need(record.get('sourceSHA256') == {s['role']: s['sha256'] for s in prepared['sources']}, 'Wrong source byte census')
    a.need({role: record['sourceSHA256'][role] for role in BASE_ROLES} == old['sourceSHA256'], 'Immutable v6 candidate source bytes differ')
    a.need([s['role'] for s in prepared['sources']] == BASE_ROLES + BUILDING_ROLES, 'Wrong prepared role census')
    a.need(prepared['sources'][:4] == load(V6 / 'native-inputs-v6/native-inputs.json')['sources'], 'V6 non-building/base source drift')
    executable = record.get('loadedTestExecutable', {})
    path, digest = executable.get('path'), executable.get('sha256')
    a.need(isinstance(path, str) and Path(path).is_absolute() and Path(path).name == 'SSRuntimeTests' and Path(path).parent.name == 'SSRuntimeTests.xctest', 'Missing actual loaded executable path')
    a.need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None and digest != old['loadedTestExecutable']['sha256'], 'Missing/current v7 loaded executable SHA')
    captures = record.get('captures', [])
    a.need([(c.get('arm'), c.get('zoom')) for c in captures] == ORDER, 'Exactly six ordered captures required')
    replacements = {b['nodeName']: b for b in prepared['buildings']}
    a.need(set(replacements) == {node_name(s) for s in TARGETS.values()}, 'Wrong replacement cohort')
    for row in captures:
        previous = next(c for c in old['captures'] if c['arm'] == 'candidate' and c['zoom'] == row['zoom'])
        a.need(row.get('comparisonRole') == ('BASELINE_V6_CANDIDATE' if row['arm'] == 'control' else 'CANDIDATE_V7_BUILDING_ONLY'), 'Wrong comparison arm meaning')
        a.need(row.get('name') == f"source-scene-{row['arm']}-ordinary-z{round(row['zoom'] * 100)}", 'Wrong capture name')
        # Every prior immutable authority, framing, depth, census and treatment field
        # is compared directly to READ-ONLY native v6 candidate, never a normalized copy.
        mutable = {'actors', 'preprojectionInventory', 'arm', 'name', 'pngSHA256', 'nativePixels'}
        for key in previous.keys() - mutable:
            a.need(row.get(key) == previous[key], 'Immutable v6 candidate field differs: ' + key)
        for cohort in ('actors', 'preprojectionInventory'):
            current, prior = row.get(cohort, []), previous[cohort]
            a.need(len(current) == len(prior), 'Dynamic full census differs')
            for actor, original in zip(current, prior):
                binding = replacements.get(original['name']) if row['arm'] == 'candidate' else None
                allowed = {'size', 'anchor'} if binding else set()
                a.need(set(actor) == set(original), 'Unknown/omitted actor fields')
                for key in original.keys() - allowed:
                    a.need(actor[key] == original[key], 'Immutable actor field differs: ' + original['name'] + '/' + key)
                if binding:
                    reg = next(s['registration'] for s in prepared['sources'] if s['role'] == binding['role'])
                    close(actor['size'], reg['drawSizeWorld'], 'explicit building size')
                    close(actor['anchor'], [reg['rootPixelsTopLeft'][0] / reg['canvasPixels'][0], 1 - reg['rootPixelsTopLeft'][1] / reg['canvasPixels'][1]], 'explicit building anchor', .000001)
                    a.need(actor['worldRoot'] == reg['worldPosition'], 'Explicit building root differs')
        v5.validate_depth(row, CENTER)
        v6.validate_framing(row)
        a.need(row.get('buildingSourceSHA256') == expected_building_hashes(row, prepared), 'Building source bytes differ')
        expected = footprint_expected(row, prepared)
        actual = row.get('groundFootprints', [])
        a.need(len(actual) == len(expected), 'Missing per-building ground witnesses')
        for observed, wanted in zip(actual, expected):
            a.need(set(observed) == set(wanted), 'Unknown/missing footprint witness fields')
            for key, value in wanted.items():
                if isinstance(value, list):
                    close(observed[key], value, 'per-vertex ' + key)
                else:
                    a.need(observed[key] == value, 'Wrong footprint identity/source: ' + key)
        a.need(set(row.get('pngSHA256', {})) == {'-native', '-half', '-grayscale'}, 'Wrong image census')
        a.need(all(isinstance(d, str) and re.fullmatch('[0-9a-f]{64}', d) for d in row['pngSHA256'].values()), 'Invalid image digest')
    return captures


# Reuse exact v6 attachment export/count, image dimensions, and actual executable
# comparison. Override globals privately, without changing a historical module.
_import_globals = dict(v6.import_result.__globals__)
_import_globals.update(globals())
_import = types.FunctionType(v6.import_result.__code__, _import_globals, argdefs=v6.import_result.__defaults__)

def import_result(result, output, expected_executable, root=ROOT, packet=HERE):
    return _import(result, output, expected_executable, root, packet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['bind', 'prepare', 'import'])
    parser.add_argument('--recommendations', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--xcresult', type=Path)
    parser.add_argument('--test-executable', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'bind':
            a.need(args.recommendations is not None, 'Coordinator-authored --recommendations required')
            answer = bind(args.recommendations, args.output or HERE / 'assembly.json')
        elif args.action == 'prepare':
            answer = prepare(output=args.output or HERE / PREPARED_DIR)
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires result, fresh output and built executable')
            answer = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(answer, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
