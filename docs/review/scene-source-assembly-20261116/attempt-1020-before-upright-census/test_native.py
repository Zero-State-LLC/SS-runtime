"""SYNTHETIC native records only. No simulator, xcresult or acceptance evidence."""
import copy
import json
from pathlib import Path
import unittest
import test_assembly as fixtures
import native as n
import assemble as a


class NativeGuardTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.AssemblyTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.manifest = self.root / 'SYNTHETIC-assembly.json'
        m = self.fixture.m
        for source in m['sources']:
            if source['role'] == 'paving':
                source['registration']['drawSizeWorld'] = [4, 4]
                source['registration']['rootPixelsTopLeft'] = [0, 12]
            else:
                source['registration']['worldPosition'] = [10, 20]
            source['recommendation']['registrationSHA256'] = a.digest(a.canonical(source['registration']))
        self.manifest.write_text(json.dumps(m))
        harness = self.root / n.HARNESS
        harness.parent.mkdir()
        harness.write_text('// SYNTHETIC HARNESS HASH FIXTURE, NOT COMPILED\n')
        self.prepared = n.expected_input(self.root, self.manifest)
        self.summary = {'result': 'Passed', 'passedTests': 1, 'totalTestCount': 1, 'failedTests': 0, 'skippedTests': 0, 'expectedFailures': 0}
        self.tree = {'testNodes': [{'nodeType': 'Test Case', 'nodeIdentifier': n.TEST, 'result': 'Passed'}]}
        self.executable = self.root / 'SYNTHETIC-build' / 'SSRuntimeTests.xctest' / 'SSRuntimeTests'
        self.executable.parent.mkdir(parents=True)
        self.executable.write_bytes(b'SYNTHETIC BINARY FIXTURE, NOT AN EXECUTABLE OR NATIVE EVIDENCE')
        self.record = {'status': n.STATUS, 'fixture': 'south-neutral-camera-neutral', 'fixtureVersion': n.FIXTURE_VERSION,
                       'cameraSourceFrames': 1, 'playerSourceFrames': 1,
                       'loadedTestExecutable': {'path': '/SYNTHETIC-installed/SSRuntimeTests.xctest/SSRuntimeTests', 'sha256': n.sha(self.executable)},
                       'inputSHA256': 'SYNTHETIC', 'assemblySHA256': self.prepared['assemblySHA256'], 'harnessSourceReadSHA256': self.prepared['harnessSourceSHA256'],
                       'sourceSHA256': {s['role']: s['sha256'] for s in self.prepared['sources']},
                       'controlSHA256': {name: 'SYNTHETIC' for name in n.CONTROLS}, 'captures': []}
        actors = []
        for role, name in [('player', 'sprite-player'), ('camera', 'sprite-camera-SYNTHETIC'), ('stone', 'benchmark-building')]:
            reg = next(s['registration'] for s in self.prepared['sources'] if s['role'] == role)
            actors.append({'name': name, 'worldRoot': reg['worldPosition'], 'size': reg['drawSizeWorld'],
                           'anchor': [reg['rootPixelsTopLeft'][0] / reg['canvasPixels'][0], 1 - reg['rootPixelsTopLeft'][1] / reg['canvasPixels'][1]]})
        actors.extend([{'name': f'benchmark-prop-{i}', 'worldRoot': [i + 2, i + 3], 'size': [5, 6], 'anchor': [0.5, 0]} for i in range(2)])
        for arm, zoom in n.ORDER:
            observed = copy.deepcopy(actors)
            for actor in observed:
                actor['projectedRoot'] = [zoom * v for v in a.project(actor['worldRoot'])]
            self.record['captures'].append({'arm': arm, 'mode': 'ordinary', 'zoom': zoom,
                'name': f'source-scene-{arm}-ordinary-z{round(zoom * 100)}', 'hudVisible': True, 'controlsRetained': True,
                'fieldVisible': True, 'fieldUnchanged': True, 'authorityBefore': 'SYNTHETIC', 'authorityAfter': 'SYNTHETIC',
                'solidCount': 2, 'cameraRoot': [10, 20], 'cameraRange': 240, 'cameraHeadingMilli': 0,
                'cameraFieldAngleMilli': 90000, 'cameraFieldOrigin': 'SYNTHETIC', 'centerWorld': [0, 0], 'actors': observed,
                'pngSHA256': {k: 'SYNTHETIC' for k in ('-native', '-half', '-grayscale')}})

    def test_synthetic_preparation_exact_bytes(self):
        target = self.root / 'SYNTHETIC-prepared'
        record = n.prepare(self.root, self.manifest, target)
        self.assertEqual(record, self.prepared)
        for source in record['sources']:
            self.assertEqual(n.sha(target / source['file']), source['sha256'])
        with self.assertRaisesRegex(a.Invalid, 'Preserve'):
            n.prepare(self.root, self.manifest, target)

    def test_real_pending_does_not_create_native_inputs(self):
        target = self.root / 'blocked'
        with self.assertRaisesRegex(a.Invalid, 'SOURCE PENDING'):
            n.prepare(manifest=n.HERE / 'assembly-pending-v2.json', output=target)
        self.assertFalse(target.exists())

    def test_synthetic_result_identity(self):
        n.validate_result(self.summary, self.tree)
        self.tree['testNodes'][0]['nodeIdentifier'] = 'Other/test()'
        with self.assertRaisesRegex(a.Invalid, 'identity'):
            n.validate_result(self.summary, self.tree)

    def test_zero_failed_skipped_expected_tests_rejected(self):
        for key, value in [('passedTests', 0), ('totalTestCount', 2), ('failedTests', 1), ('skippedTests', 1), ('expectedFailures', 1)]:
            summary = dict(self.summary, **{key: value})
            with self.subTest(key=key), self.assertRaises(a.Invalid):
                n.validate_result(summary, self.tree)

    def test_synthetic_records_pass(self):
        self.assertEqual(len(n.validate_records(self.record, self.prepared, 'SYNTHETIC')), 6)

    def test_static_scope_not_sixteen_frames(self):
        self.record['cameraSourceFrames'] = 16
        with self.assertRaises(a.Invalid):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def test_native_hash_or_fixture_mutation(self):
        for key in ('inputSHA256', 'assemblySHA256', 'harnessSourceReadSHA256', 'fixture', 'fixtureVersion'):
            record = copy.deepcopy(self.record)
            record[key] = 'wrong'
            with self.subTest(key=key), self.assertRaises(a.Invalid):
                n.validate_records(record, self.prepared, 'SYNTHETIC')

    def test_suppressed_field_hud_controls_or_authority_mutation(self):
        for key, value in [('hudVisible', False), ('controlsRetained', False), ('fieldVisible', False), ('fieldUnchanged', False), ('authorityAfter', 'changed'), ('cameraRange', 100)]:
            record = copy.deepcopy(self.record)
            record['captures'][1][key] = value
            with self.subTest(key=key), self.assertRaises(a.Invalid):
                n.validate_records(record, self.prepared, 'SYNTHETIC')

    def test_actual_registration_mutation(self):
        self.record['captures'][3]['actors'][0]['size'] = [99, 99]
        with self.assertRaisesRegex(a.Invalid, 'registration differs'):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def test_missing_ordinary_arm(self):
        self.record['captures'].pop()
        with self.assertRaises(a.Invalid):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def export_fixture(self):
        export = self.root / 'SYNTHETIC-exports'
        export.mkdir()
        items = []
        for index, name in enumerate(sorted(n.NAMES | {'source-scene-records'})):
            path = f'SYNTHETIC-{index}.bin'
            (export / path).write_bytes(b'SYNTHETIC NOT NATIVE')
            items.append({'suggestedHumanReadableName': name + '.png', 'exportedFileName': path})
        (export / 'manifest.json').write_text(json.dumps([{'attachments': items}]))
        return export, items

    def test_attachment_census_and_duplicates(self):
        export, items = self.export_fixture()
        self.assertEqual(len(n.attachments(export)), 19)
        items.append(items[0])
        (export / 'manifest.json').write_text(json.dumps([{'attachments': items}]))
        with self.assertRaisesRegex(a.Invalid, 'Duplicate'):
            n.attachments(export)

    def test_attachment_path_escape(self):
        export, items = self.export_fixture()
        items[0]['exportedFileName'] = '../escape.png'
        (export / 'manifest.json').write_text(json.dumps([{'attachments': items}]))
        with self.assertRaisesRegex(a.Invalid, 'escape'):
            n.attachments(export)

    def test_all_three_zooms_mandatory_and_ordered(self):
        for mutation in ('missing', 'duplicate', 'wrong', 'staged'):
            record = copy.deepcopy(self.record)
            if mutation == 'missing':
                record['captures'].pop(1)
            elif mutation == 'duplicate':
                record['captures'][1] = record['captures'][0]
            elif mutation == 'wrong':
                record['captures'][1]['zoom'] = 1.5
            else:
                record['captures'][1]['mode'] = 'staged'
            with self.subTest(mutation=mutation), self.assertRaises(a.Invalid):
                n.validate_records(record, self.prepared, 'SYNTHETIC')

    def test_projected_root_changes_with_zoom(self):
        roots = [c['actors'][0]['projectedRoot'] for c in self.record['captures'][:3]]
        self.assertAlmostEqual(roots[0][0], -7.071067811865475)
        self.assertAlmostEqual(roots[1][1], 13.258252147247765)
        self.assertAlmostEqual(roots[2][0], -9.899494936611665)
        self.record['captures'][1]['actors'][0]['projectedRoot'] = roots[0]
        with self.assertRaisesRegex(a.Invalid, 'Projected root'):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def test_loaded_executable_independent_of_source_read(self):
        evidence = n.validate_executable(self.record, self.executable)
        self.assertNotEqual(evidence['loadedPath'], evidence['expectedBuildPath'])
        self.assertNotEqual(evidence['loadedSHA256'], self.record['harnessSourceReadSHA256'])
        self.record['loadedTestExecutable']['sha256'] = self.record['harnessSourceReadSHA256']
        with self.assertRaisesRegex(a.Invalid, 'differs from expected'):
            n.validate_executable(self.record, self.executable)

    def test_stale_executable_rejected_even_with_current_source(self):
        self.executable.write_bytes(b'SYNTHETIC replacement binary')
        with self.assertRaisesRegex(a.Invalid, 'differs from expected'):
            n.validate_executable(self.record, self.executable)

    def test_loaded_executable_metadata_required(self):
        for key, value in [('path', 'relative/SSRuntimeTests'), ('path', '/SYNTHETIC/App/App'), ('sha256', 'not-a-sha')]:
            record = copy.deepcopy(self.record)
            record['loadedTestExecutable'][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(a.Invalid):
                n.validate_records(record, self.prepared, 'SYNTHETIC')

    def test_old_fixture_version_rejected(self):
        self.record['fixtureVersion'] = 'source-scene-continuation-001'
        with self.assertRaisesRegex(a.Invalid, 'fixtureVersion'):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def test_missing_zoom_image_rejected(self):
        export, items = self.export_fixture()
        items.pop()
        (export / 'manifest.json').write_text(json.dumps([{'attachments': items}]))
        with self.assertRaisesRegex(a.Invalid, 'eighteen'):
            n.attachments(export)

    def test_common_control_candidate_roots_retained(self):
        for c in self.record['captures'][:3]:
            actor = c['actors'][0]
            actor['worldRoot'] = [11, 20]
            actor['projectedRoot'] = [c['zoom'] * v for v in a.project(actor['worldRoot'])]
        with self.assertRaisesRegex(a.Invalid, 'common actor root'):
            n.validate_records(self.record, self.prepared, 'SYNTHETIC')

    def test_unrequested_scene_image_rejected(self):
        export, items = self.export_fixture()
        items.append({'suggestedHumanReadableName': 'source-scene-control-ordinary-z150-native.png', 'exportedFileName': items[0]['exportedFileName']})
        (export / 'manifest.json').write_text(json.dumps([{'attachments': items}]))
        with self.assertRaisesRegex(a.Invalid, 'Unexpected native scene'):
            n.attachments(export)

    def test_fixture_version_matches_swift_literal(self):
        # Static contract consistency only, never a compiler/native execution claim.
        source = (n.ROOT / n.HARNESS).read_text()
        self.assertIn('private let fixtureVersion = "' + n.FIXTURE_VERSION + '"', source)
        self.assertIn('Bundle(for: Self.self).executableURL', source)
        self.assertIn('"harnessSourceReadSHA256": sourceReadSHA256', source)

    def test_review_tests_require_explicit_compile_opt_in(self):
        # Static portable boundary check, not compiler/typecheck evidence.
        source = (n.ROOT / n.HARNESS).read_text()
        self.assertEqual(source.count('#if '), 1)
        self.assertIn('#if DEBUG && SS_SOURCE_SCENE_REVIEW', source)
        self.assertLess(source.index('#if DEBUG && SS_SOURCE_SCENE_REVIEW'), source.index('final class SourceSceneContinuationTests'))
        self.assertTrue(source.rstrip().endswith('#endif'))
        self.assertNotIn('XCTSkip', source)
        self.assertIn('SOURCE PENDING:', source)

    def test_placement_probe_does_not_require_source_inputs(self):
        source = (n.ROOT / n.HARNESS).read_text()
        probe = source.split('func testReadAuthoritativeScenePlacement()', 1)[1].split('func testQuietSouthNeutralOrdinaryScene()', 1)[0]
        for forbidden in ('native-inputs', 'assembly.json', 'renderBenchmark(', '.step(', 'prepare('):
            self.assertNotIn(forbidden, probe)
        for required in ('GameSession(seed: 1)', 'session.snapshot', 'source-scene-authoritative-placement',
                         'fieldOriginQ8', 'fieldOriginWorld', 'cameraCount', 'solidCount', 'loadedTestExecutable', 'harnessSourceReadSHA256'):
            self.assertIn(required, probe)

    def test_documented_commands_opt_in_and_select_only_one_test(self):
        doc = (n.HERE / 'NATIVE.md').read_text()
        commands = [line for line in doc.splitlines() if line.startswith('xcodebuild ')]
        self.assertEqual(len(commands), 2)
        for command in commands:
            self.assertIn("SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW'", command)
            self.assertEqual(command.count('-only-testing:'), 1)
        self.assertTrue(any('/testReadAuthoritativeScenePlacement test' in c for c in commands))
        self.assertTrue(any('/testQuietSouthNeutralOrdinaryScene test' in c for c in commands))

    def test_rejected_source_preparation(self):
        m = json.loads(self.manifest.read_text())
        m['sources'][0].update(status='rejected', image=None, registration=None, recommendation=None, reason='SYNTHETIC rejection')
        self.manifest.write_text(json.dumps(m))
        with self.assertRaisesRegex(a.Invalid, 'SOURCE PENDING'):
            n.expected_input(self.root, self.manifest)


if __name__ == '__main__':
    unittest.main(verbosity=2)
