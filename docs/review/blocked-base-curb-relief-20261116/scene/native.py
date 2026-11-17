#!/usr/bin/env python3
"""BP-001/007/012 T1045 V9 scene only.
ADAPT current footprint-ground-repair-20261116/scene/native.py:1-245.
Historical V8 files and failed2317 are immutable. No recommendation authority.
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
V8 = HERE.parent.parent / 'footprint-ground-repair-20261116/scene'

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

v8 = import_path('_v9_current_v8', V8 / 'native.py')
v7, v6, v5, a = v8.v7, v8.v6, v8.v5, v8.a
V5 = v8.V5
load, sha, close = v8.load, v8.sha, v8.close
dependency = v8.plan_adapter.dependency
STATUS, NAMES, ORDER, CENTER = v8.STATUS, v8.NAMES, v8.ORDER, v8.CENTER
HARNESS = 'AppTests/BlockedBaseCurbSceneTests.swift'
TEST = 'BlockedBaseCurbSceneTests/testQuietSouthNeutralOrdinaryScene()'
FIXTURE_VERSION = 'source-scene-base-curb-009-relief'
INPUT_SCHEMA, RECORD_SCHEMA = 'source-scene-native-009', 'source-scene-records-009'
PREPARED_DIR = 'native-inputs-v9'
BASELINE_SHA = 'f7a8e0119307305fa4cfd15281871f1c852787d3f6c1ba3d0bc2342c421bf762'
BASELINE_CAPTURE = V8 / 'native-capture-v8'
supplement_adapter = import_path('_v9_supplement_binding', HERE / 'supplement_binding.py')
validate_executable = v8.validate_executable


def baseline():
    path = BASELINE_CAPTURE / 'source-scene-records.json'
    a.need(sha(path) == BASELINE_SHA, 'Immutable actual V8 baseline record drift')
    record = load(path)
    a.need(sha(V8 / 'assembly.json') == record['assemblySHA256'], 'Immutable V8 assembly drift')
    a.need(sha(V8 / 'native-inputs-v8/native-inputs.json') == record['inputSHA256'], 'Immutable V8 preparation drift')
    return record


def validate_manifest(manifest, root=ROOT):
    old = load(V8 / 'assembly.json')
    a.need(set(manifest) == set(old) | {'supplementalBinding', 'supplements'}, 'Exact V9 assembly fields required')
    a.need(manifest['schema'] == 'blocked-base-curb-assembly-009' and manifest['fixtureVersion'] == FIXTURE_VERSION, 'Unknown V9 assembly')
    a.need(manifest['baselineRecordSHA256'] == BASELINE_SHA, 'Wrong V8 baseline')
    for key in set(old) - {'schema', 'fixtureVersion', 'baselineRecordSHA256'}:
        a.need(manifest[key] == old[key], 'Unchanged V8 binding drift: ' + key)
    baseline()
    # Retain all old authority, source/plan semantics, replay and path checks.
    prior = v8.expected_input(root, V8 / 'assembly.json')
    result = supplement_adapter.validate(manifest['supplementalBinding'], root)
    a.need(manifest['supplements'] == result['supplements'], 'Forged supplement registration/geometry')
    return prior, result


def bind(recommendations, output=HERE / 'assembly.json', root=ROOT):
    a.need(not output.exists(), 'Preserve previous V9 binding')
    rec = load(recommendations)
    result = supplement_adapter.validate(rec, root)
    manifest = load(V8 / 'assembly.json')
    manifest.update(schema='blocked-base-curb-assembly-009', fixtureVersion=FIXTURE_VERSION,
                    baselineRecordSHA256=BASELINE_SHA, supplementalBinding=rec,
                    supplements=result['supplements'])
    validate_manifest(manifest, root)
    output.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def expected_input(root=ROOT, manifest=HERE / 'assembly.json'):
    a.need(manifest.resolve() == manifest.absolute(), 'Symlinked assembly path forbidden')
    m = load(manifest)
    prior, normalized = validate_manifest(m, root)
    prior.update(schema=INPUT_SCHEMA, fixtureVersion=FIXTURE_VERSION, assemblySHA256=sha(manifest),
                 harnessSourceSHA256=sha(root / HARNESS), baselineRecordSHA256=BASELINE_SHA,
                 supplements=normalized['supplements'], supplementalBinding=m['supplementalBinding'],
                 supplementalManifestSHA256=m['supplementalBinding']['manifest']['sha256'])
    return prior


def prepare(root=ROOT, manifest=HERE / 'assembly.json', output=HERE / PREPARED_DIR):
    prepared = expected_input(root, manifest)
    a.need(not output.exists(), 'Preserve previous V9 preparation')
    m = load(manifest)
    raw = [(s['role'] + '.png', dependency(s['image'], root).read_bytes()) for s in m['sources']]
    raw += [(s['file'], dependency(s['image'], root).read_bytes()) for s in supplement_adapter.validate(m['supplementalBinding'], root)['sources']]
    a.need(len({name for name, _ in raw}) == len(raw), 'Supplement/base file collision')
    output.mkdir(parents=True)
    for name, data in raw:
        (output / name).write_bytes(data)
    (output / 'native-inputs.json').write_text(json.dumps(prepared, indent=2) + '\n')
    return prepared


def validate_result(summary, tree):
    return types.FunctionType(v5.validate_result.__code__, dict(v5.validate_result.__globals__, TEST=TEST))(summary, tree)


def validate_attachment_manifest(manifest):
    return types.FunctionType(v7.validate_attachment_manifest.__code__, dict(v7.validate_attachment_manifest.__globals__, TEST=TEST))(manifest)


def attachments(exports):
    validate_attachment_manifest(load(exports / 'manifest.json'))
    return v6.attachments(exports)


def baseline_pixels(found):
    for row in baseline()['captures']:
        if row['arm'] != 'candidate':
            continue
        for suffix, digest in row['pngSHA256'].items():
            before_path = BASELINE_CAPTURE / (row['name'] + suffix + '.png')
            a.need(sha(before_path) == digest, 'Immutable V8 baseline PNG drift')
            after_path = found[row['name'].replace('-candidate-', '-control-') + suffix]
            with Image.open(before_path) as before, Image.open(after_path) as after:
                a.need(before.size == after.size and before.convert('RGBA').tobytes() == after.convert('RGBA').tobytes(), 'Nine full V8 candidate RGBA baseline comparisons required')


def supplemental_expected(item, row):
    reg, zoom = item['registration'], row['zoom']
    root = v8.plan_adapter.projected(reg['worldPosition'], row)
    actor = dict(name=item['nodeName'], worldRoot=reg['worldPosition'], projectedRoot=root,
                 size=reg['drawSizeWorld'], anchor=[reg['rootPixelsTopLeft'][0] / reg['canvasPixels'][0], 1-reg['rootPixelsTopLeft'][1] / reg['canvasPixels'][1]],
                 scale=[1, 1], rotation=0, hidden=False, alpha=1,
                 originalLocalZ=0, originalWorldDepth=0, projectedBasisX=[zoom, 0], projectedBasisY=[0, zoom])
    vertices = []
    for xyz, pixel in zip(item['verticesWorldXYZ'], item['verticesPixelsTopLeft']):
        world = v8.plan_adapter.projected(xyz[:2], row)
        world[1] += xyz[2] * zoom
        local = [(pixel[0]-reg['rootPixelsTopLeft'][0])*reg['drawSizeWorld'][0]/reg['canvasPixels'][0],
                 (reg['rootPixelsTopLeft'][1]-pixel[1])*reg['drawSizeWorld'][1]/reg['canvasPixels'][1]]
        source = [root[i] + local[i]*zoom for i in range(2)]
        close(source, world, 'supplement XYZ source registration')
        vertices.append(dict(worldXYZ=xyz, sourcePixelsTopLeft=pixel, projectedSource=source, projectedWorldXYZ=world))
    witness = dict(nodeName=item['nodeName'], role=item['role'], sourceSHA256=item['sha256'], footprintWorld=item['footprintWorld'], vertices=vertices)
    return actor, witness


def validate_joint_depth(row, supplements):
    actors = row['actors'] + row['supplementalActors']
    expected = v5.expected_depth_items(dict(actors=row['actors']), CENTER)
    for item in supplements:
        root = item['registration']['worldPosition']
        expected.append(dict(name=item['nodeName'], worldRoot=root, footprint=item['footprintWorld'], projectedRootY=a.project(root)[1]))
    v8.plan_adapter.exact_tree(row.get('depthItems'), expected, 'joint geometry depth items')
    ordered = v5.depth_order(expected)
    a.need(row.get('depthOrder') == ordered['order'] and row.get('depthConstraints') == ordered['constraints'], 'Joint geometric ordering/constraints drift')
    base = max(p['originalWorldDepth'] for p in row['preprojectionInventory'])
    a.need(row.get('depthBase') == base and row.get('depthBand') == .5, 'No visibility depth boost')
    actual = []
    by_name = {p['name']: p for p in actors}
    a.need(len(by_name) == len(actors), 'Duplicate depth identity')
    for rank, name in enumerate(ordered['order']):
        actor = by_name[name]
        a.need(type(actor.get('depthRank')) is int and actor['depthRank'] == rank, 'Wrong joint geometry depth rank')
        value = actor.get('actualZ')
        a.need(type(value) in (int, float) and math.isfinite(value) and math.isclose(value, base + rank/len(actors)*.5, rel_tol=0, abs_tol=.00001), 'Wrong joint actual depth')
        actual.append(value)
    a.need(all(x < y for x, y in zip(actual, actual[1:])), 'Collapsed/inverted depth ranks')


def validate_records(record, prepared, input_sha):
    a.need(record.get('schema') == RECORD_SCHEMA and prepared.get('schema') == INPUT_SCHEMA, 'Wrong exact V9 schemas')
    a.need(record.get('fixtureVersion') == prepared.get('fixtureVersion') == FIXTURE_VERSION, 'Wrong exact V9 fixture')
    a.need('syntheticFixture' not in record and 'syntheticFixture' not in prepared, 'Synthetic is not native evidence')
    old = baseline()
    for key in ('status', 'fixture', 'cameraSourceFrames', 'playerSourceFrames', 'controlSHA256', 'runtimeSHA256', 'sourceSHA256'):
        a.need(record.get(key) == old[key], 'Frozen V8 metadata/source drift: ' + key)
    for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
        a.need(record.get(key, False) is False, 'Unearned evidence claim')
    a.need(record.get('baselineRecordSHA256') == prepared.get('baselineRecordSHA256') == BASELINE_SHA, 'Wrong actual V8 candidate baseline')
    a.need(prepared.get('center') == CENTER, 'Frozen center changed')
    for key, value in [('inputSHA256', input_sha), ('assemblySHA256', prepared['assemblySHA256']), ('harnessSourceReadSHA256', prepared['harnessSourceSHA256']), ('planSHA256', prepared['planSHA256']), ('supplementalManifestSHA256', prepared['supplementalManifestSHA256'])]:
        a.need(record.get(key) == value, 'Stale preparation: ' + key)
    previous_input = v8.expected_input(ROOT, V8 / 'assembly.json')
    for key in ('sources', 'scenePlan', 'planBinding', 'buildings', 'planSHA256'):
        a.need(prepared.get(key) == previous_input[key], 'Frozen V8 preparation/semantics drift: ' + key)
    normalized = supplement_adapter.validate(prepared['supplementalBinding'], ROOT)
    a.need(prepared['supplements'] == normalized['supplements'], 'Forged supplement source geometry')
    a.need(prepared['supplementalManifestSHA256'] == prepared['supplementalBinding']['manifest']['sha256'], 'Stale supplemental manifest')
    executable = record.get('loadedTestExecutable', {})
    path, digest = executable.get('path'), executable.get('sha256')
    a.need(isinstance(path, str) and Path(path).is_absolute() and Path(path).name == 'SSRuntimeTests' and Path(path).parent.name == 'SSRuntimeTests.xctest', 'Actual loaded executable required')
    a.need(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None and digest != old['loadedTestExecutable']['sha256'], 'Stale/missing V9 binary')
    rows = record.get('captures', [])
    a.need([(r.get('arm'), r.get('zoom')) for r in rows] == ORDER, 'Exactly six ordered captures required')
    extra = {'supplementalActors', 'supplementalSourceWitnesses', 'supplementalCount', 'totalPresentationUprightCount'}
    mutable = {'arm', 'name', 'comparisonRole', 'pngSHA256', 'nativePixels', 'actors', 'depthOrder', 'depthItems', 'depthConstraints'}
    for row in rows:
        previous = next(c for c in old['captures'] if c['arm'] == 'candidate' and c['zoom'] == row['zoom'])
        candidate = row['arm'] == 'candidate'
        supplements = prepared['supplements'] if candidate else []
        a.need(set(row) == set(previous) | extra, 'Unknown/missing V9 row fields')
        for key in previous.keys() - mutable:
            a.need(row.get(key) == previous[key], 'Frozen V8 candidate field drift: ' + key)
        a.need(row['name'] == f"source-scene-{row['arm']}-ordinary-z{round(row['zoom']*100)}", 'Wrong capture name')
        a.need(row['comparisonRole'] == ('CANDIDATE_V9_BASE_CURB_RELIEF' if candidate else 'BASELINE_V8_CANDIDATE'), 'Wrong comparison arm meaning')
        a.need(len(row['actors']) == 18 and row['uprightCount'] == 18 and row['supplementalCount'] == len(supplements) and row['totalPresentationUprightCount'] == 18 + len(supplements), 'Explicit 18 existing plus new supplement census required')
        for actor, original in zip(row['actors'], previous['actors']):
            a.need(set(actor) == set(original), 'Old actor schema changed')
            for key in original.keys() - ({'actualZ', 'depthRank'} if candidate else set()):
                a.need(actor[key] == original[key], 'Frozen old actor drift: ' + original['name'] + '/' + key)
        a.need(len(row['supplementalActors']) == len(row['supplementalSourceWitnesses']) == len(supplements), 'Missing/extra supplement runtime witnesses')
        for item, actor, witness in zip(supplements, row['supplementalActors'], row['supplementalSourceWitnesses']):
            expected_actor, expected_witness = supplemental_expected(item, row)
            a.need(set(actor) == set(expected_actor) | {'actualZ', 'depthRank'}, 'Supplement actor schema drift')
            v8.plan_adapter.exact_tree({k: actor[k] for k in expected_actor}, expected_actor, 'actual supplement registration')
            v8.plan_adapter.exact_tree(witness, expected_witness, 'actual supplement XYZ witnesses')
        validate_joint_depth(row, supplements)
        # V8 semantic plan applies to BOTH arms. Never reclassify supplement as an old actor.
        semantic_row = dict(row, arm='candidate')
        v8.validate_contacts(semantic_row, prepared)
        v6.validate_framing(row)
        a.need(set(row['pngSHA256']) == {'-native', '-half', '-grayscale'} and all(isinstance(d, str) and re.fullmatch('[0-9a-f]{64}', d) for d in row['pngSHA256'].values()), 'Exactly eighteen correctly hashed images required')
    return rows


def validate_prepared_files(prepared, directory):
    manifest = directory / 'native-inputs.json'
    a.need(manifest.resolve() == manifest.absolute() and manifest.is_file(), 'Prepared manifest path alias/missing')
    for item in prepared['sources'] + prepared['supplements']:
        a.need(Path(item['file']).name == item['file'], 'Prepared filename escape')
        path = directory / item['file']
        a.need(path.resolve() == path.absolute() and path.is_file() and sha(path) == item['sha256'], 'Prepared image missing/symlinked/stale')


def import_result(result, output, expected_executable, root=ROOT, packet=HERE):
    prepared = expected_input(root, packet / 'assembly.json')
    validate_prepared_files(prepared, packet / PREPARED_DIR)
    def checked(exports):
        found = attachments(exports)
        baseline_pixels(found)
        return found
    private = dict(v6.import_result.__globals__)
    private.update(globals())
    private['attachments'] = checked
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
            a.need(args.recommendations is not None, 'Final coordinator recommendation required')
            answer = bind(args.recommendations, args.output or HERE / 'assembly.json')
        elif args.action == 'prepare':
            answer = prepare(output=args.output or HERE / PREPARED_DIR)
        else:
            a.need(args.xcresult is not None and args.output is not None and args.test_executable is not None, 'Import requires actual result/output/fresh-built executable')
            answer = import_result(args.xcresult, args.output, args.test_executable)
        print(json.dumps(answer, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, str(error) + '\n')
