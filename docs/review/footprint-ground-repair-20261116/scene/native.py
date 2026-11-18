#!/usr/bin/env python3
"""V8 review-only scene. ADAPT V7 scene/native.py:1-362, V6 native.py:199-253.
Historical modules/files are read-only. Recommendations must be coordinator authored.
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
V7 = HERE.parent.parent / 'building-perspective-detail-20261116/scene'

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

v7 = import_path('_footprint_v8_v7', V7 / 'native.py')
v6, v5, a = v7.v6, v7.v5, v7.a
V5 = v7.V5
load, sha, dependency, close = v7.load, v7.sha, v7.dependency, v7.close
STATUS, NAMES, ORDER, CENTER = v7.STATUS, v7.NAMES, v7.ORDER, v7.CENTER
validate_executable = v7.validate_executable
HARNESS = 'AppTests/FootprintGroundSceneTests.swift'
TEST = 'FootprintGroundSceneTests/testQuietSouthNeutralOrdinaryScene()'
FIXTURE_VERSION = 'source-scene-footprint-008-ground-plan'
INPUT_SCHEMA, RECORD_SCHEMA = 'source-scene-native-008', 'source-scene-records-008'
PREPARED_DIR = 'native-inputs-v8'
BASELINE_SHA = '9728f0a030020dff0caad52e8d3791be092a3b6ada8b5ffd845ee9d370785889'
BASELINE_CAPTURE = V7 / 'native-capture-v7'
ROLES = v7.BASE_ROLES + v7.BUILDING_ROLES
PROP_NAMES = ['benchmark-prop-0', 'benchmark-prop-1']
plan_adapter = import_path('_footprint_v8_plan_binding', HERE / 'plan_binding.py')


def baseline():
    path = BASELINE_CAPTURE / 'source-scene-records.json'
    a.need(sha(path) == BASELINE_SHA, 'Immutable V7 baseline drift')
    record = load(path)
    a.need(sha(V7 / 'assembly.json') == record['assemblySHA256'], 'Immutable V7 assembly drift')
    a.need(sha(V7 / 'native-inputs-v7/native-inputs.json') == record['inputSHA256'], 'Immutable V7 preparation drift')
    return record


def validate_plan_binding(binding, root=ROOT):
    """Fail closed until the source plan contract is installed and recommended."""
    from_error = 'Source plan contract pending, coordinator recommendation required'
    a.need(isinstance(binding, dict), from_error)
    # Implemented by the explicit source-contract adapter, never by an optional hook.
    return plan_adapter.validate(binding, root)


def validate_manifest(manifest, root=ROOT):
    old = load(V7 / 'assembly.json')
    a.need(set(manifest) == {'schema', 'fixtureVersion', 'baselineRecordSHA256', 'viewCenterWorld',
                           'contextDependencies', 'sources', 'buildings', 'planBinding'}, 'Exact V8 assembly fields required')
    a.need(manifest['schema'] == 'footprint-ground-assembly-008' and manifest['fixtureVersion'] == FIXTURE_VERSION, 'Unknown V8 assembly')
    a.need(manifest['baselineRecordSHA256'] == BASELINE_SHA and manifest['viewCenterWorld'] == CENTER, 'Immutable baseline/framing drift')
    for key in ('contextDependencies', 'buildings'):
        a.need(manifest[key] == old[key], 'Frozen V7 binding drift: ' + key)
    a.need(manifest['sources'][:9] == old['sources'], 'Frozen V7 sources/registrations drift')
    a.need([s['role'] for s in manifest['sources']] == ROLES + ['ground-plan'], 'Exact ten source roles required')
    baseline()
    v7.expected_input(root, V7 / 'assembly.json')
    normalized = validate_plan_binding(manifest['planBinding'], root)
    a.need(manifest['sources'][9] == normalized['source'], 'Ground source is not bound semantic plan output')
    return normalized


def bind(recommendations, output=HERE / 'assembly.json', root=ROOT):
    a.need(not output.exists(), 'Preserve previous V8 binding')
    rec = load(recommendations)
    normalized = validate_plan_binding(rec, root)
    old = load(V7 / 'assembly.json')
    result = dict(schema='footprint-ground-assembly-008', fixtureVersion=FIXTURE_VERSION,
                  baselineRecordSHA256=BASELINE_SHA, viewCenterWorld=CENTER,
                  contextDependencies=old['contextDependencies'], sources=old['sources'] + [normalized['source']],
                  buildings=old['buildings'], planBinding=rec)
    validate_manifest(result, root)
    output.write_text(json.dumps(result, indent=2) + '\n')
    return result


def expected_input(root=ROOT, manifest=HERE / 'assembly.json'):
    m = load(manifest)
    plan = validate_manifest(m, root)
    return dict(schema=INPUT_SCHEMA, fixtureVersion=FIXTURE_VERSION, assemblySHA256=sha(manifest),
                harnessSourceSHA256=sha(root / HARNESS), baselineRecordSHA256=BASELINE_SHA,
                center=CENTER, buildings=m['buildings'], scenePlan=plan['scenePlan'],
                planSHA256=plan['planSHA256'], planBinding=m['planBinding'],
                sources=[dict(role=s['role'], file=s['role'] + '.png', sha256=s['image']['sha256'],
                              registration=s['registration'], recommendation='coordinator-recommended') for s in m['sources']])


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / PREPARED_DIR):
    prepared = expected_input(root, manifest)
    a.need(not output.exists(), 'Preserve previous V8 preparation')
    raw = [dependency(s['image'], root).read_bytes() for s in load(manifest)['sources']]
    output.mkdir(parents=True)
    for source, data in zip(prepared['sources'], raw):
        (output / source['file']).write_bytes(data)
    (output / 'native-inputs.json').write_text(json.dumps(prepared, indent=2) + '\n')
    return prepared


def validate_result(summary, tree):
    types.FunctionType(v5.validate_result.__code__, dict(v5.validate_result.__globals__, TEST=TEST))(summary, tree)


def validate_attachment_manifest(manifest):
    return types.FunctionType(v7.validate_attachment_manifest.__code__, dict(v7.validate_attachment_manifest.__globals__, TEST=TEST))(manifest)


def attachments(exports):
    validate_attachment_manifest(load(exports / 'manifest.json'))
    return v6.attachments(exports)


def baseline_pixels(found):
    """Nine full RGBA comparisons against immutable V7 candidate bytes."""
    old = baseline()
    for row in old['captures']:
        if row['arm'] != 'candidate':
            continue
        for suffix, digest in row['pngSHA256'].items():
            previous = BASELINE_CAPTURE / (row['name'] + suffix + '.png')
            a.need(sha(previous) == digest, 'Immutable V7 baseline image drift')
            current = found[row['name'].replace('-candidate-', '-control-') + suffix]
            with Image.open(previous) as before, Image.open(current) as after:
                a.need(before.size == after.size and before.convert('RGBA').tobytes() == after.convert('RGBA').tobytes(),
                       'V8 baseline pixel parity failed: ' + suffix)


def validate_records(record, prepared, input_sha):
    a.need(record.get('schema') == RECORD_SCHEMA and prepared.get('schema') == INPUT_SCHEMA, 'Wrong exact V8 schemas')
    a.need(record.get('fixtureVersion') == prepared.get('fixtureVersion') == FIXTURE_VERSION, 'Wrong exact V8 version')
    a.need('syntheticFixture' not in record and 'syntheticFixture' not in prepared, 'Synthetic is not native evidence')
    old = baseline()
    for key in ('status', 'fixture', 'cameraSourceFrames', 'playerSourceFrames', 'controlSHA256', 'runtimeSHA256'):
        a.need(record.get(key) == old[key], 'Frozen baseline metadata drift: ' + key)
    for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
        a.need(record.get(key, False) is False, 'Unearned evidence claim')
    a.need(record.get('baselineRecordSHA256') == prepared.get('baselineRecordSHA256') == BASELINE_SHA, 'Wrong V7 baseline reference')
    a.need(prepared.get('center') == CENTER, 'Frozen center changed')
    for key, value in [('inputSHA256', input_sha), ('assemblySHA256', prepared['assemblySHA256']),
                       ('harnessSourceReadSHA256', prepared['harnessSourceSHA256']), ('planSHA256', prepared['planSHA256'])]:
        a.need(record.get(key) == value, 'Stale source/plan/preparation: ' + key)
    a.need(prepared['sources'][:9] == load(V7 / 'native-inputs-v7/native-inputs.json')['sources'], 'Frozen source preparation drift')
    a.need([s['role'] for s in prepared['sources']] == ROLES + ['ground-plan'], 'Wrong source census')
    a.need(record.get('sourceSHA256') == {s['role']: s['sha256'] for s in prepared['sources']}, 'Wrong source byte census')
    a.need({role: record['sourceSHA256'][role] for role in ROLES} == old['sourceSHA256'], 'Frozen V7 bytes drift')
    normalized = validate_plan_binding(prepared['planBinding'])
    a.need(prepared['scenePlan'] == normalized['scenePlan'] and prepared['planSHA256'] == normalized['planSHA256'], 'Forged semantic plan preparation')
    ground = normalized['source']
    a.need(prepared['sources'][9] == dict(role='ground-plan', file='ground-plan.png', sha256=ground['image']['sha256'],
                                        registration=ground['registration'], recommendation='coordinator-recommended'), 'Forged ground source/registration binding')
    executable = record.get('loadedTestExecutable', {})
    path, digest = executable.get('path'), executable.get('sha256')
    a.need(isinstance(path, str) and Path(path).is_absolute() and Path(path).name == 'SSRuntimeTests' and Path(path).parent.name == 'SSRuntimeTests.xctest', 'Missing loaded executable path')
    a.need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None and digest != old['loadedTestExecutable']['sha256'], 'Stale/missing V8 executable')
    captures = record.get('captures', [])
    a.need([(c.get('arm'), c.get('zoom')) for c in captures] == ORDER, 'Exactly six ordered captures required')
    for row in captures:
        previous = next(c for c in old['captures'] if c['arm'] == 'candidate' and c['zoom'] == row['zoom'])
        candidate = row['arm'] == 'candidate'
        a.need(row.get('comparisonRole') == ('CANDIDATE_V8_SHARED_GROUND_PLAN' if candidate else 'BASELINE_V7_CANDIDATE'), 'Wrong comparison meaning')
        a.need(row.get('name') == f"source-scene-{row['arm']}-ordinary-z{round(row['zoom'] * 100)}", 'Wrong capture name')
        mutable = {'actors', 'preprojectionInventory', 'arm', 'name', 'pngSHA256', 'nativePixels', 'comparisonRole'}
        if candidate:
            mutable |= {'depthOrder', 'depthItems', 'depthConstraints'}
        for key in previous.keys() - mutable:
            a.need(row.get(key) == previous[key], 'Frozen V7 candidate field differs: ' + key)
        props = {p['name']: p for p in prepared['scenePlan']['props']} if candidate else {}
        for cohort in ('actors', 'preprojectionInventory'):
            current, prior = row.get(cohort, []), previous[cohort]
            a.need(len(current) == len(prior), 'Full upright census drift')
            for actor, original in zip(current, prior):
                prop = props.get(original['name'])
                allowed = {'worldRoot'} if prop else set()
                if candidate and cohort == 'actors':
                    allowed |= {'actualZ', 'depthRank'}
                    if prop: allowed |= {'projectedRoot'}
                a.need(set(actor) == set(original), 'Unknown/missing actor fields')
                for key in original.keys() - allowed:
                    a.need(actor[key] == original[key], 'Frozen actor differs: ' + original['name'] + '/' + key)
                if prop:
                    a.need(actor['worldRoot'] == prop['worldRoot'], 'Prop does not follow semantic plan')
                    # Review props retain WorldRenderer.renderDecorations' zero local Z.
                    if cohort == 'actors':
                        close(actor['projectedRoot'], [CENTER[i] + row['zoom'] * a.project([prop['worldRoot'][j] - CENTER[j] for j in range(2)])[i] for i in range(2)], 'prop projection')
        v5.validate_depth(row, CENTER)
        v6.validate_framing(row)
        a.need(row.get('buildingSourceSHA256') == previous['buildingSourceSHA256'], 'Frozen building sources drift')
        validate_contacts(row, prepared)
        a.need(set(row.get('pngSHA256', {})) == {'-native', '-half', '-grayscale'}, 'Wrong image census')
        a.need(all(isinstance(d, str) and re.fullmatch('[0-9a-f]{64}', d) for d in row['pngSHA256'].values()), 'Bad image hash')
    return captures


def validate_contacts(row, prepared):
    plan_adapter.validate_contacts(row, prepared)


# Exact inherited exporter, privately bound to V8 validators and 19-attachment census.
_globals = dict(v6.import_result.__globals__)
_globals.update(globals())
_import = types.FunctionType(v6.import_result.__code__, _globals, argdefs=v6.import_result.__defaults__)

def import_result(result, output, expected_executable, root=ROOT, packet=HERE):
    # Pixel parity is enforced before inherited importer writes any retained output.
    original = _globals['attachments']
    def checked(exports):
        found = original(exports)
        baseline_pixels(found)
        return found
    private = dict(_globals, attachments=checked)
    importer = types.FunctionType(v6.import_result.__code__, private, argdefs=v6.import_result.__defaults__)
    return importer(result, output, expected_executable, root, packet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['bind', 'prepare', 'import'])
    for name in ('recommendations', 'output', 'xcresult', 'test-executable'):
        parser.add_argument('--' + name, type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'bind':
            a.need(args.recommendations is not None, 'Coordinator-authored recommendation required')
            answer = bind(args.recommendations, args.output or HERE / 'assembly.json')
        elif args.action == 'prepare':
            answer = prepare(output=args.output or HERE / PREPARED_DIR)
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires xcresult/output/test-executable')
            answer = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(answer, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
