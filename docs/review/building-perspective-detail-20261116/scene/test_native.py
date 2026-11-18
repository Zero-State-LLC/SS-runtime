"""Portable synthetic mutation tests only. Never creates or claims v7 native evidence.
The in-memory fixture starts with read-only v6 candidate metadata, explicitly
synthetic PNG hashes and fake binary bytes. Temporary retained fixtures are mocks.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_v7_scene_test_native', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
r = n.import_path('_v7_scene_test_retained', HERE / 'retained.py')


def synthetic():
    old = n.baseline()
    prepared = n.load(n.V6 / 'native-inputs-v6/native-inputs.json')
    prepared.update(schema=n.INPUT_SCHEMA, fixtureVersion=n.FIXTURE_VERSION,
                    assemblySHA256='a' * 64, harnessSourceSHA256=n.sha(n.ROOT / n.HARNESS),
                    baselineRecordSHA256=n.BASELINE_SHA, buildings=[])
    for role, solid_id in n.TARGETS.items():
        solid = next(s for s in n.v5.authority()['solids'] if s['id'] == solid_id)
        root = [512, 640] if role == 'kiosk' else solid['centerWorld']
        reg = dict(canvasPixels=[1024, 1024], rootPixelsTopLeft=[512, 512], worldPosition=root, drawSizeWorld=[1024, 1024])
        pixels = [[512 + n.a.project([v[i] - root[i] for i in range(2)])[0],
                   512 - n.a.project([v[i] - root[i] for i in range(2)])[1]] for v in n.vertices(solid)]
        prepared['sources'].append(dict(role=role, file=role + '.png', sha256='b' * 64,
                                        registration=reg, recommendation='coordinator-recommended'))
        prepared['buildings'].append(dict(role=role, nodeName=n.node_name(solid_id), solidID=solid_id, groundPixelsTopLeft=pixels))
    record = {key: copy.deepcopy(value) for key, value in old.items() if key != 'captures'}
    record.update(schema=n.RECORD_SCHEMA, fixtureVersion=n.FIXTURE_VERSION, inputSHA256='SYNTHETIC_NOT_NATIVE',
                  assemblySHA256=prepared['assemblySHA256'], harnessSourceReadSHA256=prepared['harnessSourceSHA256'],
                  baselineRecordSHA256=n.BASELINE_SHA, captures=[],
                  sourceSHA256={s['role']: s['sha256'] for s in prepared['sources']},
                  loadedTestExecutable={'path': '/SYNTHETIC/SSRuntimeTests.xctest/SSRuntimeTests', 'sha256': 'c' * 64})
    for arm, zoom in n.ORDER:
        row = copy.deepcopy(next(c for c in old['captures'] if c['arm'] == 'candidate' and c['zoom'] == zoom))
        row.update(arm=arm, name=f'source-scene-{arm}-ordinary-z{round(zoom * 100)}',
                   comparisonRole='BASELINE_V6_CANDIDATE' if arm == 'control' else 'CANDIDATE_V7_BUILDING_ONLY',
                   pngSHA256={suffix: 'd' * 64 for suffix in ('-native', '-half', '-grayscale')})
        if arm == 'candidate':
            for binding in prepared['buildings']:
                for cohort in ('actors', 'preprojectionInventory'):
                    actor = next(a for a in row[cohort] if a['name'] == binding['nodeName'])
                    actor.update(size=[1024, 1024], anchor=[.5, .5])
        row['buildingSourceSHA256'] = n.expected_building_hashes(row, prepared)
        row['groundFootprints'] = n.footprint_expected(row, prepared)
        record['captures'].append(row)
    return record, prepared


class Records(unittest.TestCase):
    def setUp(self):
        self.record, self.prepared = synthetic()

    def validate(self):
        return n.validate_records(self.record, self.prepared, 'SYNTHETIC_NOT_NATIVE')

    def test_synthetic_contract_is_not_native_run(self):
        self.assertEqual(len(self.validate()), 6)

    def test_each_immutable_field_rejects_mutation(self):
        fields = ['authorityBefore', 'authorityAfter', 'cameraRoot', 'cameraFieldOrigin', 'cameraRange',
                  'cameraHeadingMilli', 'cameraFieldAngleMilli', 'centerWorld', 'solids', 'solidCount',
                  'framing', 'groundBounds', 'groundSourceWorldSize', 'playerOutlineAlpha',
                  'playerShadowWorldRoot', 'playerShadowSize', 'playerShadowTextureSHA256',
                  'expectedEnvironmentNames', 'uprightCount', 'depthOrder', 'depthItems', 'depthConstraints',
                  'hudVisible', 'controlsRetained', 'fieldVisible', 'fieldUnchanged']
        for key in fields:
            with self.subTest(field=key):
                original = self.record['captures'][3][key]
                self.record['captures'][3][key] = None
                with self.assertRaises(ValueError): self.validate()
                self.record['captures'][3][key] = original

    def test_every_actor_immutable_field_rejects(self):
        for index in range(len(self.record['captures'][3]['actors'])):
            for key in ('worldRoot', 'hidden', 'alpha', 'originalWorldDepth', 'actualZ', 'depthRank', 'scale', 'rotation'):
                with self.subTest(actor=index, field=key):
                    actor = self.record['captures'][3]['actors'][index]
                    original = actor[key]; actor[key] = None
                    with self.assertRaises(ValueError): self.validate()
                    actor[key] = original

    def test_non_target_size_anchor_immutable(self):
        for index in (0, 1, 3, 4, *range(9, 18)):
            for key in ('size', 'anchor'):
                with self.subTest(index=index, key=key):
                    actor = self.record['captures'][3]['actors'][index]
                    original = actor[key]; actor[key] = [123, 123]
                    with self.assertRaises(ValueError): self.validate()
                    actor[key] = original

    def test_baseline_is_v6_candidate_not_old_control(self):
        old = n.baseline()['captures'][0]
        self.record['captures'][0]['actors'] = old['actors']
        with self.assertRaises(ValueError): self.validate()

    def test_baseline_registration_cannot_change(self):
        self.record['captures'][0]['actors'][2]['size'] = [1024, 1024]
        with self.assertRaises(ValueError): self.validate()

    def test_candidate_registration_must_match_binding(self):
        self.record['captures'][3]['actors'][2]['size'][0] += 1
        with self.assertRaises(ValueError): self.validate()

    def test_hidden_or_omitted_full_census(self):
        self.record['captures'][3]['actors'].pop()
        with self.assertRaises(ValueError): self.validate()

    def test_per_vertex_projection_mutations(self):
        for field in ('worldVertices', 'projectedGround', 'groundPixelsTopLeft', 'localVertices', 'projectedSource'):
            with self.subTest(field=field):
                witness = self.record['captures'][3]['groundFootprints'][0]
                witness[field][0][0] += 1
                with self.assertRaises(ValueError): self.validate()
                witness[field][0][0] -= 1

    def test_missing_vertex_and_building_hash(self):
        self.record['captures'][3]['groundFootprints'][0]['worldVertices'].pop()
        with self.assertRaises(ValueError): self.validate()
        self.record, self.prepared = synthetic()
        self.record['captures'][3]['buildingSourceSHA256'].pop('benchmark-building')
        with self.assertRaises(ValueError): self.validate()

    def test_unknown_versions(self):
        for container, field in ((self.record, 'schema'), (self.record, 'fixtureVersion'), (self.prepared, 'schema'), (self.prepared, 'fixtureVersion')):
            original = container[field]; container[field] = 'future-999'
            with self.assertRaises(ValueError): self.validate()
            container[field] = original

    def test_missing_actual_executable(self):
        self.record.pop('loadedTestExecutable')
        with self.assertRaises(ValueError): self.validate()

    def test_v6_executable_is_not_v7_evidence(self):
        self.record['loadedTestExecutable'] = n.baseline()['loadedTestExecutable']
        with self.assertRaises(ValueError): self.validate()

    def test_explicit_synthetic_claim_rejected_as_native(self):
        self.record['syntheticFixture'] = True
        with self.assertRaises(ValueError): self.validate()

    def test_rehashed_source_drift(self):
        self.prepared['sources'][0]['sha256'] = 'f' * 64
        self.record['sourceSHA256']['paving'] = 'f' * 64
        with self.assertRaises(ValueError): self.validate()

    def test_exact_one_test_identity(self):
        summary = dict(result='Passed', passedTests=1, totalTestCount=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = dict(testNodes=[dict(nodeType='Test Case', nodeIdentifier=n.TEST, result='Passed')])
        n.validate_result(summary, tree)
        for key in ('passedTests', 'totalTestCount', 'skippedTests', 'failedTests'):
            changed = copy.deepcopy(summary); changed[key] += 1
            with self.assertRaises(ValueError): n.validate_result(changed, tree)
        tree['testNodes'][0]['nodeIdentifier'] = n.v6.TEST
        with self.assertRaises(ValueError): n.validate_result(summary, tree)

    def test_actual_built_executable_comparison(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            binary = Path(temp) / 'SSRuntimeTests'; binary.write_bytes(b'SYNTHETIC executable, not native')
            with self.assertRaises(ValueError): n.validate_executable(self.record, binary)
            self.record['loadedTestExecutable']['sha256'] = n.sha(binary)
            n.validate_executable(self.record, binary)
            binary.write_bytes(b'changed')
            with self.assertRaises(ValueError): n.validate_executable(self.record, binary)

    def test_missing_preparation_fails_without_creating_output(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp)
            with self.assertRaises(FileNotFoundError): n.prepare(manifest=root / 'missing.json', output=root / 'inputs')
            self.assertFalse((root / 'inputs').exists())

    def test_bind_does_not_invent_recommendations(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp); rec = root / 'recommendations.json'
            rec.write_text(json.dumps(dict(schema='building-perspective-recommendations-007', sources=[], buildings=[])))
            with self.assertRaises(ValueError): n.bind(rec, root / 'assembly.json')
            self.assertFalse((root / 'assembly.json').exists())

    def test_historical_native_records_rejected_unchanged(self):
        with self.assertRaises(ValueError): n.validate_records(n.baseline(), self.prepared, 'SYNTHETIC_NOT_NATIVE')

    def test_missing_retained_capture_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            with self.assertRaises(FileNotFoundError): r.verify(Path(temp))

    def test_historical_retained_capture_rejected(self):
        with self.assertRaises(ValueError): r.verify(n.V6 / 'native-capture-v6', n.V6 / 'native-inputs-v6')


if __name__ == '__main__':
    unittest.main()
