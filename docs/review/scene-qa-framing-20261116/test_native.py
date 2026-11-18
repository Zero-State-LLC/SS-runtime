"""Synthetic v6 framing mutations and read-only actual v5 overlap witness.
No v6 native evidence is created or claimed by these tests.
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
spec = importlib.util.spec_from_file_location('_framing_tests_native_v6', HERE / 'native.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


def add_framing(row):
    row['framing'] = {'coordinateSystem': 'logical-crop-top-left-704x326', 'safeAreaInsets': [0, 0, 0, 0],
                      'visibleControls': n.expected_controls(),
                      'actorCanvasBounds': [{'name': a['name'], 'bounds': n.actor_canvas(a, row)} for a in row['actors'][:2]]}


def synthetic_fixture():
    record = n.load(n.V5 / 'native-capture-v5/source-scene-records.json')
    prepared = n.load(n.V5 / 'native-inputs-v5/native-inputs.json')
    record.update(schema=n.RECORD_SCHEMA, fixtureVersion=n.FIXTURE_VERSION, inputSHA256='SYNTHETIC-V6-NOT-NATIVE', syntheticFixture=True)
    prepared.update(schema=n.INPUT_SCHEMA, fixtureVersion=n.FIXTURE_VERSION, center=n.CENTER.copy())
    for row in record['captures']:
        row['centerWorld'] = n.CENTER.copy()
        for actor in row['actors']:
            delta = n.a.project([actor['worldRoot'][i] - n.CENTER[i] for i in range(2)])
            actor['projectedRoot'] = [n.CENTER[i] + row['zoom'] * delta[i] for i in range(2)]
        delta = n.a.project([row['playerShadowWorldRoot'][i] - n.CENTER[i] for i in range(2)])
        row['playerShadowProjectedRoot'] = [n.CENTER[i] + row['zoom'] * delta[i] for i in range(2)]
        add_framing(row)
    return record, prepared


class FramingTests(unittest.TestCase):
    def setUp(self):
        self.record, self.prepared = synthetic_fixture()

    def validate(self, record=None, prepared=None):
        return n.validate_records(record or self.record, prepared or self.prepared, 'SYNTHETIC-V6-NOT-NATIVE')

    def test_synthetic_all_six_captures(self):
        self.assertEqual(len(self.validate()), 6)

    def test_issue250_default_pause_stroke_matches_renderer(self):
        # Independent exact synthetic regression for native2122's measured
        # default pause stroke. Do not derive this expectation from the oracle.
        for row in self.record['captures']:
            for control in row['framing']['visibleControls']:
                stroke = 1 if control['role'] == 'pause' else 2 * 704 / 896
                x, y, width, height = control['pathBounds']
                control['lineWidth'] = stroke
                control['bounds'] = [x - stroke / 2, y - stroke / 2,
                                     width + stroke, height + stroke]
        self.assertEqual(len(self.validate()), 6)

    def test_issue250_scaled_pause_stroke_rejected(self):
        row = self.record['captures'][0]
        pause = next(c for c in row['framing']['visibleControls'] if c['role'] == 'pause')
        stroke = 2 * 704 / 896
        x, y, width, height = pause['pathBounds']
        pause['lineWidth'] = stroke
        pause['bounds'] = [x - stroke / 2, y - stroke / 2, width + stroke, height + stroke]
        with self.assertRaisesRegex(ValueError, 'Visible control stroke changed'):
            self.validate()

    def test_v5_known_camera_stick_overlap_red_witness(self):
        # Actual retained v5 actors, analytically reconstructed fixed production
        # control bounds. V5 did not measure control bounds, so not mislabeled as such.
        record = n.load(n.V5 / 'native-capture-v5/source-scene-records.json')
        row = next(r for r in record['captures'] if r['arm'] == 'candidate' and r['zoom'] == 1.4)
        add_framing(row)
        self.assertTrue(n.overlaps(row['framing']['actorCanvasBounds'][1]['bounds'], row['framing']['visibleControls'][0]['bounds']))
        with self.assertRaisesRegex(ValueError, 'overlaps visible control: sprite-camera-3/stick'):
            n.validate_framing(row)

    def test_center_only_keeps_vertical_framing(self):
        baseline = n.load(n.V5 / 'native-capture-v5/source-scene-records.json')
        for row, old in zip(self.record['captures'], baseline['captures']):
            for actor, previous in zip(row['actors'][:2], old['actors'][:2]):
                actual, prior = n.actor_canvas(actor, row), n.actor_canvas(previous, old)
                self.assertAlmostEqual(actual[0] - prior[0], 52 * 2**.5 * row['zoom'], delta=.002)
                self.assertAlmostEqual(actual[1], prior[1], delta=.002)

    def test_actual_v5_not_admitted_as_v6(self):
        record = n.load(n.V5 / 'native-capture-v5/source-scene-records.json')
        prepared = n.load(n.V5 / 'native-inputs-v5/native-inputs.json')
        with self.assertRaisesRegex(ValueError, 'v6 schema'):
            n.validate_records(record, prepared, record['inputSHA256'])
        n.v5.validate_records(record, prepared, record['inputSHA256'])

    def test_wrapper_does_not_mutate_callers_or_v5_globals(self):
        before = copy.deepcopy((self.record, self.prepared))
        self.validate()
        self.assertEqual((self.record, self.prepared), before)
        self.assertEqual(n.v5.FIXTURE_VERSION, 'source-scene-qa-005-footprint-ground')
        self.assertEqual(n.v5.TEST, 'SceneQARepairTests/testQuietSouthNeutralOrdinaryScene()')
        with self.assertRaisesRegex(ValueError, 'schema'):
            n.v5.validate_records(self.record, self.prepared, 'SYNTHETIC-V6-NOT-NATIVE')

    def test_overlap_even_with_consistent_measured_rectangle_rejected(self):
        row = self.record['captures'][5]
        actor = row['actors'][1]
        actor['projectedRoot'][0] -= 100
        add_framing(row)
        with self.assertRaisesRegex(ValueError, 'overlaps visible control'):
            n.validate_framing(row)
        with self.assertRaisesRegex(ValueError, 'Projected root'):
            self.validate()

    def test_clipped_actor_even_with_consistent_measurement_rejected(self):
        row = self.record['captures'][3]
        row['actors'][0]['projectedRoot'][0] += 1000
        add_framing(row)
        with self.assertRaisesRegex(ValueError, 'outside crop'):
            n.validate_framing(row)

    def test_forged_control_bounds_or_activation_zone_rejected(self):
        for key, value in [('bounds', [0, 97.8, 352, 228.2]), ('bounds', [0, 0, 1, 1]),
                           ('pathBounds', [0, 0, 1, 1]), ('layoutBounds', [0, 0, 1, 1]),
                           ('hidden', True), ('alpha', 0), ('lineWidth', 0), ('nodeName', 'stickZone')]:
            record = copy.deepcopy(self.record)
            record['captures'][0]['framing']['visibleControls'][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.validate(record)

    def test_missing_or_duplicate_controls_and_actor_bounds_rejected(self):
        for key in ('visibleControls', 'actorCanvasBounds'):
            record = copy.deepcopy(self.record)
            record['captures'][3]['framing'][key].pop()
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(record)
        self.record['captures'][3]['framing']['visibleControls'][1] = self.record['captures'][3]['framing']['visibleControls'][0]
        with self.assertRaises(ValueError):
            self.validate()

    def test_measured_canvas_must_equal_registered_canvas(self):
        self.record['captures'][3]['framing']['actorCanvasBounds'][1]['bounds'][2] = 1
        with self.assertRaisesRegex(ValueError, 'measured actor canvas'):
            self.validate()

    def test_nonfinite_measured_bound_rejected(self):
        self.record['captures'][3]['framing']['actorCanvasBounds'][0]['bounds'][0] = float('nan')
        with self.assertRaisesRegex(ValueError, 'Invalid rectangle'):
            self.validate()

    def test_prior_v5_guards_still_enforced(self):
        for key, value in [('fieldUnchanged', False), ('hudVisible', False), ('playerOutlineAlpha', 1),
                           ('groundBounds', [0, 0, 2304, 2304]), ('depthBand', 1),
                           ('playerShadowWorldRoot', [0, 0]), ('solidCount', 23)]:
            record = copy.deepcopy(self.record)
            record['captures'][3][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(record)

    def test_unauthorized_center_rejected(self):
        self.prepared['center'] = [685, 724]
        with self.assertRaisesRegex(ValueError, 'center'):
            self.validate()

    def test_only_center_may_change_in_manifest(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            manifest = Path(temp) / 'assembly.json'
            n.bind(manifest)
            prepared = n.expected_input(manifest=manifest)
            self.assertEqual(prepared['center'], n.CENTER)
            self.assertEqual(prepared['schema'], n.INPUT_SCHEMA)
            self.assertEqual(prepared['harnessSourceSHA256'], n.sha(n.ROOT / n.HARNESS))
            m = n.load(manifest)
            m['sources'][0]['registration']['drawSizeWorld'] = [1, 1]
            manifest.write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError, 'only the exact view center'):
                n.expected_input(manifest=manifest)

    def test_prepare_keeps_prior_outputs_and_exact_sources(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp)
            manifest, output = root / 'assembly.json', root / 'prepared'
            n.bind(manifest)
            prepared = n.prepare(manifest=manifest, output=output)
            for source in prepared['sources']:
                self.assertEqual(n.sha(output / source['file']), source['sha256'])
            with self.assertRaisesRegex(ValueError, 'Preserve'):
                n.prepare(manifest=manifest, output=output)
            with self.assertRaisesRegex(ValueError, 'Preserve'):
                n.bind(manifest)

    def test_v6_test_identity_not_v5_and_no_skip(self):
        summary = dict(result='Passed', passedTests=1, totalTestCount=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = {'testNodes': [dict(nodeType='Test Case', nodeIdentifier=n.TEST, result='Passed')]}
        n.validate_result(summary, tree)
        self.assertEqual(tree['testNodes'][0]['nodeIdentifier'], n.TEST)
        tree['testNodes'][0]['nodeIdentifier'] = n.v5.TEST
        with self.assertRaisesRegex(ValueError, 'identity'):
            n.validate_result(summary, tree)
        tree['testNodes'][0]['nodeIdentifier'] = n.TEST
        summary['skippedTests'] = 1
        with self.assertRaises(ValueError):
            n.validate_result(summary, tree)

    def test_discovery_import_collisions_do_not_select_other_native(self):
        import sys
        with patch.dict(sys.modules, {'native': object(), 'assemble': object(), 'retained': object()}):
            loaded = n.import_path('_framing_collision', HERE / 'native.py')
            self.assertEqual(loaded.FIXTURE_VERSION, n.FIXTURE_VERSION)
            retained = n.import_path('_framing_retained_collision', HERE / 'retained.py')
            self.assertEqual(retained.n.FIXTURE_VERSION, n.FIXTURE_VERSION)
            self.assertEqual(retained._previous.n.FIXTURE_VERSION, n.v5.FIXTURE_VERSION)

    def test_static_harness_contract(self):
        source = (n.ROOT / n.HARNESS).read_text()
        for literal in ('input.center == [684, 724]', 'RuntimeAssetRegistry.HUD.stickBase',
                        'path.boundingBoxOfPath', 'actorCanvasBounds', 'visibleControls',
                        'Player/Camera canvas overlaps visible control', n.FIXTURE_VERSION,
                        n.INPUT_SCHEMA, n.RECORD_SCHEMA, n.PREPARED_DIR):
            self.assertIn(literal, source)
        self.assertNotIn('stickZone', source)
        self.assertIn('#if DEBUG && SS_SOURCE_SCENE_REVIEW', source)
        self.assertNotIn('XCTSkip', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
