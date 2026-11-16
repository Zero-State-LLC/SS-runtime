"""Synthetic record mutations only. Never native evidence or a source recommendation."""
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
spec = importlib.util.spec_from_file_location('_v8_native_tests', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
r = n.import_path('_v8_retained_tests', HERE / 'retained.py')


def synthetic():
    old = n.baseline()
    plan = n.load(HERE.parent / 'plan/plan.json')
    prepared = n.load(n.V7 / 'native-inputs-v7/native-inputs.json')
    prepared.update(schema=n.INPUT_SCHEMA, fixtureVersion=n.FIXTURE_VERSION, assemblySHA256='a' * 64,
                    harnessSourceSHA256=n.sha(n.ROOT / n.HARNESS), baselineRecordSHA256=n.BASELINE_SHA,
                    planSHA256='b' * 64, scenePlan={key: plan[key] for key in ('props', 'buildings')},
                    planBinding={'SYNTHETIC_ONLY': True})
    prepared['sources'].append(dict(role='ground-plan', file='ground-plan.png', sha256='c' * 64,
                                    registration=plan['registration'], recommendation='coordinator-recommended'))
    normalized = dict(scenePlan=copy.deepcopy(prepared['scenePlan']), planSHA256=prepared['planSHA256'],
                      source=dict(image=dict(sha256='c' * 64), registration=copy.deepcopy(plan['registration'])))
    record = {k: copy.deepcopy(v) for k, v in old.items() if k != 'captures'}
    record.update(schema=n.RECORD_SCHEMA, fixtureVersion=n.FIXTURE_VERSION, inputSHA256='SYNTHETIC_NOT_NATIVE',
                  assemblySHA256=prepared['assemblySHA256'], harnessSourceReadSHA256=prepared['harnessSourceSHA256'],
                  baselineRecordSHA256=n.BASELINE_SHA, planSHA256=prepared['planSHA256'],
                  sourceSHA256={s['role']: s['sha256'] for s in prepared['sources']}, captures=[],
                  loadedTestExecutable=dict(path='/SYNTHETIC/SSRuntimeTests.xctest/SSRuntimeTests', sha256='d' * 64))
    for arm, zoom in n.ORDER:
        row = copy.deepcopy(next(c for c in old['captures'] if c['arm'] == 'candidate' and c['zoom'] == zoom))
        row.update(arm=arm, name=f'source-scene-{arm}-ordinary-z{round(zoom * 100)}',
                   comparisonRole='BASELINE_V7_CANDIDATE' if arm == 'control' else 'CANDIDATE_V8_SHARED_GROUND_PLAN',
                   pngSHA256={s: 'e' * 64 for s in ('-native', '-half', '-grayscale')})
        if arm == 'candidate':
            props = {p['name']: p for p in plan['props']}
            for cohort in ('actors', 'preprojectionInventory'):
                for actor in row[cohort]:
                    if actor['name'] in props:
                        actor['worldRoot'] = props[actor['name']]['worldRoot'].copy()
                        if cohort == 'actors': actor['projectedRoot'] = n.plan_adapter.projected(actor['worldRoot'], row)
            row['depthItems'] = n.v5.expected_depth_items(row, n.CENTER)
            depth = n.v5.depth_order(row['depthItems'])
            row['depthOrder'], row['depthConstraints'] = depth['order'], depth['constraints']
            for actor in row['actors']:
                actor['depthRank'] = depth['order'].index(actor['name'])
                actor['actualZ'] = row['depthBase'] + actor['depthRank'] / len(row['actors']) * .5
        row.update(n.plan_adapter.witnesses_expected(row, prepared))
        record['captures'].append(row)
    return record, prepared, normalized


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.record, self.prepared, self.normalized = synthetic()

    def validate(self):
        # Explicitly mocks coordinator recommendation, never writes binding/native outputs.
        with patch.object(n, 'validate_plan_binding', return_value=self.normalized):
            return n.validate_records(self.record, self.prepared, 'SYNTHETIC_NOT_NATIVE')

    def test_synthetic_contract_six_rows(self):
        self.assertEqual(len(self.validate()), 6)

    def test_each_authority_framing_and_control_field_fails_closed(self):
        fields = ['authorityBefore', 'authorityAfter', 'cameraRoot', 'cameraFieldOrigin', 'cameraRange',
                  'cameraHeadingMilli', 'cameraFieldAngleMilli', 'centerWorld', 'solids', 'solidCount',
                  'framing', 'groundBounds', 'groundSourceWorldSize', 'playerOutlineAlpha',
                  'playerShadowWorldRoot', 'playerShadowSize', 'playerShadowTextureSHA256',
                  'expectedEnvironmentNames', 'uprightCount', 'depthItems', 'depthOrder', 'depthConstraints',
                  'hudVisible', 'controlsRetained', 'fieldVisible', 'fieldUnchanged']
        for key in fields:
            with self.subTest(key=key):
                row = self.record['captures'][3]
                old = row[key]; row[key] = None
                with self.assertRaises((ValueError, TypeError)): self.validate()
                row[key] = old

    def test_every_frozen_actor_field_rejects(self):
        for index in range(18):
            for key in ('size', 'anchor', 'scale', 'rotation', 'hidden', 'alpha', 'originalLocalZ', 'originalWorldDepth'):
                with self.subTest(index=index, key=key):
                    actor = self.record['captures'][3]['actors'][index]
                    old = actor[key]; actor[key] = None
                    with self.assertRaises(ValueError): self.validate()
                    actor[key] = old

    def test_player_camera_building_roots_frozen(self):
        for index in (0, 1, 2, *range(5, 18)):
            actor = self.record['captures'][3]['actors'][index]
            old = actor['worldRoot']; actor['worldRoot'] = [1, 2]
            with self.assertRaises(ValueError): self.validate()
            actor['worldRoot'] = old

    def test_unplanned_prop_root_rejected(self):
        self.record['captures'][3]['actors'][4]['worldRoot'] = [858, 780]
        with self.assertRaises(ValueError): self.validate()

    def test_forged_rehashed_prop_plan_rejected(self):
        self.prepared['scenePlan']['props'][1]['worldRoot'] = [858, 780]
        self.record['planSHA256'] = self.prepared['planSHA256'] = 'f' * 64
        with self.assertRaises(ValueError): self.validate()

    def test_forged_plan_contact_rejected(self):
        self.prepared['scenePlan']['buildings'][2]['contactLandmarks'][0]['world'] = [512, 640]
        with self.assertRaises(ValueError): self.validate()

    def test_forged_rehashed_source_rejected(self):
        for index in (0, 1, 2, 4, 9):
            source = self.prepared['sources'][index]
            old = source['sha256']; source['sha256'] = 'f' * 64
            self.record['sourceSHA256'][source['role']] = 'f' * 64
            with self.assertRaises(ValueError): self.validate()
            source['sha256'] = old; self.record['sourceSHA256'][source['role']] = old

    def test_forged_ground_registration_rejected(self):
        self.prepared['sources'][9]['registration']['drawSizeWorld'] = [2304, 1536]
        with self.assertRaises(ValueError): self.validate()

    def test_stale_plan_and_harness_rejected(self):
        for key in ('planSHA256', 'harnessSourceReadSHA256', 'inputSHA256', 'assemblySHA256'):
            old = self.record[key]; self.record[key] = '0' * 64
            with self.assertRaises(ValueError): self.validate()
            self.record[key] = old

    def test_v7_executable_rejected(self):
        self.record['loadedTestExecutable'] = n.baseline()['loadedTestExecutable']
        with self.assertRaises(ValueError): self.validate()

    def test_missing_binary_rejected(self):
        self.record.pop('loadedTestExecutable')
        with self.assertRaises(ValueError): self.validate()

    def test_wrong_schema_version_rejected(self):
        for obj in (self.record, self.prepared):
            for key in ('schema', 'fixtureVersion'):
                old = obj[key]; obj[key] = 'future-999'
                with self.assertRaises(ValueError): self.validate()
                obj[key] = old

    def test_missing_and_duplicate_capture_rejected(self):
        self.record['captures'][0] = copy.deepcopy(self.record['captures'][1])
        with self.assertRaises(ValueError): self.validate()

    def test_actual_visible_contact_each_field_rejected(self):
        row = self.record['captures'][3]
        for index in range(5):
            for key in ('nodeName', 'sourceSHA256', 'meshContactStatus', 'landmarks'):
                witness = row['visibleBuildingContacts'][index]
                old = witness[key]; witness[key] = None
                with self.assertRaises(ValueError): self.validate()
                witness[key] = old
        row['visibleBuildingContacts'].pop()
        with self.assertRaises(ValueError): self.validate()

    def test_virtual_corner_cannot_replace_actual_contact(self):
        self.record['captures'][3]['visibleBuildingContacts'][0]['landmarks'][0]['world'] = [512, 640]
        with self.assertRaises(ValueError): self.validate()

    def test_projection_incrop_and_provenance_forgery_rejected(self):
        landmark = self.record['captures'][3]['visibleBuildingContacts'][0]['landmarks'][0]
        for key in list(landmark):
            old = landmark[key]; landmark[key] = None
            with self.assertRaises(ValueError): self.validate()
            landmark[key] = old

    def test_ground_transform_and_plan_claim_rejected(self):
        witness = self.record['captures'][3]['groundPlanWitness']
        for key in list(witness):
            old = witness[key]; witness[key] = None
            with self.assertRaises(ValueError): self.validate()
            witness[key] = old

    def test_prop_contact_shadow_witness_forgery_rejected(self):
        witness = self.record['captures'][3]['propPlanWitnesses'][1]
        for key in list(witness):
            old = witness[key]; witness[key] = None
            with self.assertRaises(ValueError): self.validate()
            witness[key] = old

    def test_baseline_v7_candidate_not_control(self):
        self.record['captures'][0]['actors'] = n.baseline()['captures'][0]['actors']
        with self.assertRaises(ValueError): self.validate()

    def test_baseline_prop_cannot_move(self):
        self.record['captures'][0]['actors'][4]['worldRoot'] = [858, 716]
        with self.assertRaises(ValueError): self.validate()

    def test_no_synthetic_native_claim(self):
        self.record['syntheticFixture'] = True
        with self.assertRaises(ValueError): self.validate()

    def test_zero_tests_and_stale_test_identity(self):
        summary = dict(result='Passed', passedTests=1, totalTestCount=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = dict(testNodes=[dict(nodeType='Test Case', nodeIdentifier=n.TEST, result='Passed')])
        n.validate_result(summary, tree)
        for key in ('passedTests', 'totalTestCount', 'failedTests', 'skippedTests'):
            bad = copy.deepcopy(summary); bad[key] += 1
            with self.assertRaises(ValueError): n.validate_result(bad, tree)
        tree['testNodes'][0]['nodeIdentifier'] = n.v7.TEST
        with self.assertRaises(ValueError): n.validate_result(summary, tree)

    def test_loaded_binary_compared_to_actual_bytes(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            binary = Path(temp) / 'SSRuntimeTests'; binary.write_bytes(b'SYNTHETIC ONLY')
            with self.assertRaises(ValueError): n.validate_executable(self.record, binary)
            self.record['loadedTestExecutable']['sha256'] = n.sha(binary)
            n.validate_executable(self.record, binary)
            binary.write_bytes(b'changed')
            with self.assertRaises(ValueError): n.validate_executable(self.record, binary)


class BindingAndPixels(unittest.TestCase):
    def test_missing_and_nonrecommended_plan_fails_without_output(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp)
            with self.assertRaises(FileNotFoundError): n.prepare(manifest=root / 'missing.json', output=root / 'inputs')
            self.assertFalse((root / 'inputs').exists())
            rec = root / 'rec.json'; rec.write_text(json.dumps({'schema': 'footprint-ground-recommendations-008'}))
            with self.assertRaises(ValueError): n.bind(rec, root / 'assembly.json')
            self.assertFalse((root / 'assembly.json').exists())

    def test_retained_old_version_rejected(self):
        with self.assertRaises(ValueError): r.verify(n.BASELINE_CAPTURE, n.V7 / 'native-inputs-v7')

    def test_baseline_pixel_oracle_all_nine_and_single_pixel_mutation(self):
        found = {}
        for row in n.baseline()['captures'][3:]:
            for suffix in row['pngSHA256']:
                found[row['name'].replace('-candidate-', '-control-') + suffix] = n.BASELINE_CAPTURE / (row['name'] + suffix + '.png')
        n.baseline_pixels(found)
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            key = sorted(found)[0]; path = Path(temp) / 'changed.png'
            with Image.open(found[key]) as image:
                image = image.convert('RGBA'); pixel = image.getpixel((0, 0))
                image.putpixel((0, 0), ((pixel[0] + 1) % 256, *pixel[1:])); image.save(path)
            found[key] = path
            with self.assertRaises(ValueError): n.baseline_pixels(found)

    def test_path_traversal_absolute_and_symlink_rejected(self):
        for path in ('../outside', '/absolute', 'x/../y', 'x//y', 'x\\y'):
            with self.assertRaises(ValueError): n.plan_adapter.dependency(dict(path=path, sha256='a' * 64), n.ROOT)
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp); (root / 'target').write_bytes(b'x'); (root / 'link').symlink_to(root / 'target')
            with self.assertRaises(ValueError): n.plan_adapter.dependency(dict(path='link', sha256=n.sha(root / 'target')), root)

    def test_attachment_export_exact_census_and_test(self):
        old = n.load(n.BASELINE_CAPTURE / 'attachment-manifest.json')
        old[0]['testIdentifier'] = n.TEST
        n.validate_attachment_manifest(old)
        old[0]['attachments'].pop()
        with self.assertRaises(ValueError): n.validate_attachment_manifest(old)


if __name__ == '__main__':
    unittest.main()
