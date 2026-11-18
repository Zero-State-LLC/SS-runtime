"""SYNTHETIC v5 records derived from v4 geometry, NOT native execution evidence.
Historical records are read only as a fixture skeleton and remain untouched.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('_qa5_native_tests', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


def synthetic_fixture():
    prepared = n.load(n.OLD / 'native-inputs-v4/native-inputs.json')
    record = n.load(n.OLD / 'native-capture-1040/source-scene-records.json')
    prepared.update(schema='source-scene-native-005', fixtureVersion=n.FIXTURE_VERSION)
    paving = next(s for s in prepared['sources'] if s['role'] == 'paving')
    paving['registration'].update(worldPosition=[0, 0], drawSizeWorld=[2304, 2304])
    record.update(schema='source-scene-records-005', fixtureVersion=n.FIXTURE_VERSION,
                  inputSHA256='SYNTHETIC-NOT-NATIVE', syntheticFixture=True)
    record['loadedTestExecutable'] = {'path': '/SYNTHETIC/SSRuntimeTests.xctest/SSRuntimeTests',
                                     'sha256': n.a.digest(b'SYNTHETIC BINARY NOT COMPILED')}
    for row in record['captures']:
        candidate = row['arm'] == 'candidate'
        row.update(solids=n.solid_rows(), playerOutlineAlpha=0 if candidate else 1,
                   playerShadowWorldRoot=copy.deepcopy(row['actors'][0]['worldRoot']),
                   playerShadowProjectedRoot=copy.deepcopy(row['actors'][0]['projectedRoot']),
                   playerShadowSize=[32, 12], originalPlayerShadowSize=[32, 12],
                   playerShadowTextureSHA256=n.a.digest(b'SYNTHETIC EXISTING SHADOW'),
                   originalPlayerShadowTextureSHA256=n.a.digest(b'SYNTHETIC EXISTING SHADOW'),
                   shadowTreatment='ground-root-existing-soft-shadow' if candidate else 'original-offset-soft-shadow',
                   groundBounds=[0, 0, 2304, 1536] if candidate else [],
                   groundSourceWorldSize=[2304, 2304] if candidate else [])
        row['depthItems'] = n.expected_depth_items(row, prepared['center'])
        assign_depth(row)
    return prepared, record


def assign_depth(row):
    result = n.depth_order(row['depthItems'])
    row['depthConstraints'] = result['constraints']
    row['depthOrder'] = result['order']
    by_name = {actor['name']: actor for actor in row['actors']}
    for rank, name in enumerate(row['depthOrder']):
        by_name[name].update(depthRank=rank, actualZ=row['depthBase'] + rank / len(by_name) * .5)


class NativeV5Tests(unittest.TestCase):
    def setUp(self):
        self.prepared, self.record = synthetic_fixture()

    def validate(self, record=None):
        return n.validate_records(record or self.record, self.prepared, 'SYNTHETIC-NOT-NATIVE')

    def reject(self, mutation, message=None):
        record = copy.deepcopy(self.record)
        mutation(record)
        with self.assertRaisesRegex(ValueError, message or '.'):
            self.validate(record)

    def test_synthetic_v5_contract(self):
        self.assertEqual(len(self.validate()), 6)
        self.assertTrue(self.record['syntheticFixture'])

    def test_real_v4_rejected_not_reinterpreted(self):
        prepared = n.load(n.OLD / 'native-inputs-v4/native-inputs.json')
        record = n.load(n.OLD / 'native-capture-1040/source-scene-records.json')
        with self.assertRaisesRegex(ValueError, 'schema'):
            n.validate_records(record, prepared, record['inputSHA256'])

    def test_outline_shadow_ground_mutations(self):
        for key, value in [('playerOutlineAlpha', 1), ('playerShadowWorldRoot', [736, 653]),
                           ('playerShadowSize', [33, 12]), ('playerShadowTextureSHA256', '0' * 64),
                           ('shadowTreatment', 'invented-shadow'), ('groundBounds', [448, 384, 1024, 960])]:
            with self.subTest(key=key):
                self.reject(lambda r: r['captures'][3].update({key: value}))

    def test_control_outline_stays_old(self):
        self.reject(lambda r: r['captures'][0].update(playerOutlineAlpha=0), 'outline')

    def test_ground_adapter_rejects_displayed_padding_or_rectangular_source(self):
        for key, value in [('groundBounds', [0, 0, 2304, 2304]),
                           ('groundBounds', [0, 0, 2303, 1536]),
                           ('groundSourceWorldSize', [2304, 1536]),
                           ('groundSourceWorldSize', [2303, 2303])]:
            with self.subTest(key=key, value=value):
                self.reject(lambda r: r['captures'][3].update({key: value}), 'Ground')

    def test_projected_shadow_must_match_player_each_zoom(self):
        for index in (3, 4, 5):
            with self.subTest(index=index):
                self.reject(lambda r: r['captures'][index]['playerShadowProjectedRoot'].__setitem__(0,
                            r['captures'][index]['actors'][0]['projectedRoot'][0] + .01), 'Projected shadow')
        self.reject(lambda r: r['captures'][3].pop('playerShadowProjectedRoot'), 'shadow')
        self.reject(lambda r: r['captures'][3].update(playerShadowProjectedRoot=[float('nan'), 0]), 'shadow')

    def test_exact_solids_not_only_census(self):
        self.reject(lambda r: r['captures'][3]['solids'][2]['minWorld'].__setitem__(0, 511), 'solid')
        self.reject(lambda r: r['captures'][3]['solids'][2].update(id='forged'), 'solid')
        self.reject(lambda r: r['captures'][3]['solids'].reverse(), 'solid')

    def test_depth_geometry_not_self_reported(self):
        for key, value in [('footprint', [511, 640, 640, 768]), ('worldRoot', [511, 640]),
                           ('projectedRootY', 0), ('name', 'unknown')]:
            with self.subTest(key=key):
                self.reject(lambda r: r['captures'][3]['depthItems'][2].update({key: value}))
        self.reject(lambda r: r['captures'][3]['depthItems'][0].update(footprint=[0, 0, 1, 1]))

    def test_depth_order_band_and_constraint_mutations(self):
        self.reject(lambda r: r['captures'][3]['depthOrder'].reverse())
        self.reject(lambda r: r['captures'][3].update(depthConstraints=[]))
        self.reject(lambda r: r['captures'][3].update(depthBand=1))
        self.reject(lambda r: r['captures'][3]['actors'][0].update(actualZ=100))
        self.reject(lambda r: r['captures'][3]['actors'][0].update(depthRank=0))

    def test_kiosk_camera_constraint_is_not_root_only_sort(self):
        items = [dict(name='kiosk', worldRoot=[512, 640], footprint=[512, 640, 640, 768], projectedRootY=1152),
                 dict(name='camera', worldRoot=[496, 672], footprint=None, projectedRootY=1168)]
        result = n.depth_order(items)
        self.assertEqual(result['order'], ['kiosk', 'camera'])
        self.assertEqual(result['constraints'], [{'back': 'kiosk', 'front': 'camera', 'separations': [
            {'axis': 'x', 'backMinimum': 512, 'frontMaximum': 496}]}])
        self.assertEqual(n.depth_order(list(reversed(items))), result)

    def test_unconstrained_equal_priority_tie_is_lexical(self):
        items = [dict(name=name, worldRoot=[0, 0], footprint=None, projectedRootY=0) for name in ('z', 'a')]
        self.assertEqual(n.depth_order(items), {'order': ['a', 'z'], 'constraints': []})

    def test_ray_box_oracle_1089_positions(self):
        kiosk = dict(name='kiosk', worldRoot=[512, 640], footprint=[512, 640, 640, 768], projectedRootY=1152)
        for x in range(448, 705, 8):
            for y in range(576, 833, 8):
                item = dict(name='point', worldRoot=[x, y], footprint=None, projectedRootY=x + y)
                result = n.depth_order([kiosk, item])
                # Independent ray p+t*(1,1) intersection, not the axis rule.
                enter, leave = max(512 - x, 640 - y), min(640 - x, 768 - y)
                expected = []
                if enter <= leave and enter > 0:
                    expected = [('kiosk', 'point')]
                elif enter <= leave and leave < 0:
                    expected = [('point', 'kiosk')]
                with self.subTest(x=x, y=y):
                    self.assertEqual([(e['back'], e['front']) for e in result['constraints']], expected)

    def test_self_consistent_forged_footprint_still_rejected(self):
        def forge(record):
            row = record['captures'][3]
            row['depthItems'][2]['footprint'] = [400, 640, 640, 768]
            row['solids'][2]['minWorld'] = [400, 640]
            assign_depth(row)
        self.reject(forge, 'solid')

    def test_forged_environment_root_in_inventory_and_depth_rejected(self):
        def forge(record):
            row = record['captures'][3]
            row['actors'][-1]['worldRoot'] = [2241, 192]
            row['preprojectionInventory'][-1]['worldRoot'] = [2241, 192]
            row['depthItems'][-1]['worldRoot'] = [2241, 192]
            delta = n.a.project([2241 - self.prepared['center'][0], 192 - self.prepared['center'][1]])
            row['actors'][-1]['projectedRoot'] = [self.prepared['center'][i] + row['zoom'] * delta[i] for i in range(2)]
        self.reject(forge, 'bound authority')

    def test_basis_inventory_and_alpha_guards_preserved(self):
        for key, value in [('projectedBasisY', [1, 0]), ('projectedRoot', [0, 0]),
                           ('alpha', 0), ('hidden', True), ('size', [1, 1]),
                           ('scale', [1, 2]), ('originalWorldDepth', 99)]:
            with self.subTest(key=key):
                self.reject(lambda r: r['captures'][3]['actors'][0].update({key: value}))

    def test_hud_field_authority_and_census_preserved(self):
        for key, value in [('hudVisible', False), ('controlsRetained', False), ('fieldVisible', False),
                           ('fieldUnchanged', False), ('authorityAfter', 'changed'), ('solidCount', 23),
                           ('cameraRange', 1), ('expectedEnvironmentNames', []), ('uprightCount', 17)]:
            with self.subTest(key=key):
                self.reject(lambda r: r['captures'][3].update({key: value}))

    def test_source_binary_and_schema_guards(self):
        for key in ('schema', 'fixtureVersion', 'inputSHA256', 'assemblySHA256', 'harnessSourceReadSHA256'):
            with self.subTest(key=key):
                self.reject(lambda r: r.update({key: 'forged'}))
        self.reject(lambda r: r['loadedTestExecutable'].update(sha256='bad'))
        self.reject(lambda r: r['captures'].pop())

    def test_unearned_claim_inside_record_rejected(self):
        for key in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
            with self.subTest(key=key):
                self.reject(lambda r: r.update({key: True}), 'Unearned')

    def test_actual_binary_hash_mismatch(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            executable = Path(temp) / 'SSRuntimeTests'
            executable.write_bytes(b'SYNTHETIC BINARY NOT COMPILED')
            n.validate_executable(self.record, executable)
            executable.write_bytes(b'SYNTHETIC STALE BINARY')
            with self.assertRaisesRegex(ValueError, 'differs'):
                n.validate_executable(self.record, executable)

    def test_result_identity_and_skips(self):
        summary = dict(result='Passed', passedTests=1, totalTestCount=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = {'testNodes': [{'nodeType': 'Test Case', 'nodeIdentifier': n.TEST, 'result': 'Passed'}]}
        n.validate_result(summary, tree)
        for key in ('failedTests', 'skippedTests', 'expectedFailures'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                n.validate_result(dict(summary, **{key: 1}), tree)
        tree['testNodes'][0]['nodeIdentifier'] = 'SourceSceneContinuationTests/testQuietSouthNeutralOrdinaryScene()'
        with self.assertRaises(ValueError):
            n.validate_result(summary, tree)

    def test_private_import_ignores_unrelated_module_names(self):
        import sys
        with patch.dict(sys.modules, {'native': object(), 'assemble': object(), 'depth': object()}):
            loaded = n.import_path('_qa5_collision_test', HERE / 'native.py')
            self.assertEqual(loaded.a.SCHEMA, 'scene-source-assembly-001')
            self.assertEqual(loaded.FIXTURE_VERSION, n.FIXTURE_VERSION)


if __name__ == '__main__':
    unittest.main(verbosity=2)
