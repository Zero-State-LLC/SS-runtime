"""Synthetic validator mutation tests only. These do not claim native evidence."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from PIL import Image

import verify_capture as v


class EvidenceReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='existing-art-validator-', dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        asset = self.root / 'asset.bin'
        asset.write_bytes(b'test-only resource')
        self.expected = {'test-asset': 'asset.bin'}
        commands = self.root / 'commands.json'
        commands.write_text(json.dumps({'seed': 1, 'ticks': 2, 'digest': 'd', 'commands': []}))
        record = self.root / 'record.json'
        record.write_text('{}')
        self.files = {'existing-art-legal-commands': commands, 'existing-art-encounter-records': record}
        rows = []
        for tick, tag in [(1, 'camera-integrity-3'), (2, 'dense')]:
            name = f'existing-art-tick-{tick}'
            image = self.root / f'{name}.png'
            Image.new('RGBA', (4, 3), (tick, 2, 3, 255)).save(image)
            self.files[name] = image
            rows.append(dict(tick=tick, image=name, pngSHA256=v.sha(image.read_bytes()), width=4, height=3,
                             digest='d', captureDigestAfter='d', tags=[tag], nearbyEnemyCount=2,
                             projectileCount=1, cameras=[dict(integrity=3, fieldVisible=True, fieldNodePresent=True)],
                             events=[]))
            row = rows[-1]
            row.update(sceneWidth=704, sceneHeight=326, cameraX=0, cameraY=0, playerX=0, playerY=0,
                       framing='staged snapshot Player center, not live follow',
                       crop=dict(x=-352, y=-163, width=704, height=326), enemies=[], projectiles=[])
            def node(kind, identity, x, y, name):
                return dict(kind=kind, id=identity, node=name, x=x, y=y, rootX=x, rootY=y,
                            nearby=True, nodeVisible=True, rootInCrop=True, boundsIntersectCrop=True,
                            bounds=dict(x=x-2, y=y-2, width=4, height=4))
            row['renderNodes'] = [node('player', 0, 0, 0, 'sprite-player')]
            if tag == 'dense':
                row['enemies'] = [dict(id=i, x=i*10, y=0) for i in [1, 2]]
                row['projectiles'] = [dict(id=3, x=30, y=0)]
                row['renderNodes'] += [node('enemy', i, i*10, 0, f'sprite-enemy-{i}') for i in [1, 2]]
                row['renderNodes'].append(node('projectile', 3, 30, 0, 'shot-3'))
        self.packet = dict(schema='existing-art-encounters-v2', scenarioSeeded=False, seed=1,
                           driver='DebugAutopilot run / ghostStep / seed1', terminalTick=2, tickLimit=6000,
                           finalDigest='d', replayDigest='d', sourceFidelity='BLOCKED', ownerAcceptance='NOT_GRANTED',
                           productionAdmission='NOT_GRANTED', evidenceKind='static paused GameScene existing production art and projection',
                           runtimeInputs=[dict(assetId='test-asset', path='asset.bin', sha256=v.sha(asset.read_bytes()), bytes=asset.stat().st_size)],
                           contractSHA256={name: v.sha((v.ROOT / 'Sources/SurveillanceCore/Resources/contracts' / name).read_bytes())
                                           for name in ['asset-catalog-001.json', 'presentation-assets-003.json', 'clip-metadata-001.json']},
                           replaySHA256=v.sha(commands.read_bytes()), captures=rows,
                           observed=['camera-integrity-3', 'dense'], notObserved=sorted(v.WANTED - {'camera-integrity-3', 'dense'}))

    def validate(self, packet=None, files=None):
        return v.validate_packet(self.packet if packet is None else packet,
                                 self.files if files is None else files, self.expected, self.root)

    def test_reject_stale_camera_and_offscreen_crop(self):
        for key, value in [('cameraX', 5000), ('crop', dict(x=5000, y=5000, width=704, height=326)),
                           ('framing', 'live follow')]:
            packet = copy.deepcopy(self.packet)
            packet['captures'][1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(packet)

    def test_reject_missing_hidden_or_false_dense_node_intersections(self):
        for mutate in [lambda r: r['renderNodes'].pop(),
                       lambda r: r['renderNodes'][0].update(nodeVisible=False),
                       lambda r: r['renderNodes'][1].update(rootX=5000),
                       lambda r: r['renderNodes'][1].update(rootInCrop=False),
                       lambda r: r['renderNodes'][1].update(bounds=dict(x=5000, y=5000, width=4, height=4)),
                       lambda r: r['renderNodes'][1].update(nodeVisible=False)]:
            packet = copy.deepcopy(self.packet)
            mutate(packet['captures'][1])
            with self.assertRaises(ValueError):
                self.validate(packet)

    def test_actual_stale_attempt_rejected_and_preserved_bytes_match(self):
        attempt = Path(__file__).parent / 'attempts/01-stale-framing/exports'
        files = v.attachments(attempt)
        packet = v.load(files['existing-art-encounter-records'])
        with self.assertRaisesRegex(ValueError, 'Wrong schema'):
            v.validate_packet(packet, files)
        for row in packet['captures']:
            self.assertEqual(v.sha(files[row['image']].read_bytes()), row['pngSHA256'])

    def test_actual_0701_is_rejected_old_schema_not_corrected_evidence(self):
        attempt = Path(__file__).parent / 'attempts/02-0701-old-schema/exports'
        files = v.attachments(attempt)
        packet = v.load(files['existing-art-encounter-records'])
        self.assertEqual(packet['schema'], 'existing-art-encounters-v1')
        self.assertNotIn('renderNodes', packet['captures'][0])
        with self.assertRaisesRegex(ValueError, 'Wrong schema'):
            v.validate_packet(packet, files)
        for row in packet['captures']:
            self.assertEqual(v.sha(files[row['image']].read_bytes()), row['pngSHA256'])

    def test_synthetic_reader_control(self):
        self.assertEqual(self.validate()['captures'], 2)

    def test_reject_seeded_replay_or_digest_mismatch(self):
        for key, value in [('scenarioSeeded', True), ('seed', 2), ('replayDigest', 'bad'), ('driver', 'seedScenario')]:
            packet = copy.deepcopy(self.packet)
            packet[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(packet)

    def test_reject_resource_mutation_and_missing_census(self):
        packet = copy.deepcopy(self.packet)
        packet['runtimeInputs'] = []
        with self.assertRaises(ValueError):
            self.validate(packet)
        (self.root / 'asset.bin').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.validate()

    def test_reject_contract_hash_mutation(self):
        packet = copy.deepcopy(self.packet)
        packet['contractSHA256']['clip-metadata-001.json'] = 'changed'
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_reject_resource_path_escape(self):
        with self.assertRaises(ValueError):
            v.safe(self.root, '../not-an-export')

    def test_reject_command_bytes_mutation(self):
        self.files['existing-art-legal-commands'].write_text('{}')
        with self.assertRaises(ValueError):
            self.validate()

    def test_reject_capture_bytes_and_dimension_mutation(self):
        packet = copy.deepcopy(self.packet)
        packet['captures'][0]['width'] = 5
        with self.assertRaises(ValueError):
            self.validate(packet)
        self.files['existing-art-tick-1'].write_bytes(b'not png')
        with self.assertRaises(ValueError):
            self.validate()

    def test_reject_invented_dense_or_camera_state(self):
        for index, key, value in [(1, 'nearbyEnemyCount', 0), (1, 'projectileCount', 0), (0, 'tags', ['camera-integrity-0'])]:
            packet = copy.deepcopy(self.packet)
            packet['captures'][index][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(packet)

    def test_reject_field_off_cone_and_undisclosed_missing_states(self):
        packet = copy.deepcopy(self.packet)
        packet['captures'][0]['cameras'][0]['fieldVisible'] = False
        with self.assertRaises(ValueError):
            self.validate(packet)
        packet = copy.deepcopy(self.packet)
        packet['notObserved'] = []
        with self.assertRaises(ValueError):
            self.validate(packet)

    def test_reject_acceptance_or_scope_claim(self):
        for key in ['ownerAcceptance', 'sourceFidelity', 'productionAdmission', 'evidenceKind']:
            packet = copy.deepcopy(self.packet)
            packet[key] = 'ACCEPTED'
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(packet)

    def test_reject_duplicate_or_missing_capture(self):
        packet = copy.deepcopy(self.packet)
        packet['captures'].append(copy.deepcopy(packet['captures'][0]))
        with self.assertRaises(ValueError):
            self.validate(packet)
        files = dict(self.files)
        files['extra'] = self.files['existing-art-tick-1']
        with self.assertRaises(ValueError):
            self.validate(files=files)

    def test_native_result_identity_zero_and_skips_fail_closed(self):
        summary = dict(result='Passed', passedTests=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = {'testNodes': [dict(nodeType='Test Case', nodeIdentifier=v.TEST, result='Passed')]}
        v.validate_result(summary, tree)
        for key, value in [('passedTests', 0), ('failedTests', 1), ('skippedTests', 1), ('expectedFailures', 1)]:
            changed = dict(summary)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                v.validate_result(changed, tree)
        tree['testNodes'][0]['nodeIdentifier'] = 'AnotherTest'
        with self.assertRaises(ValueError):
            v.validate_result(summary, tree)

    def test_real_resource_census_is_nonempty_and_paths_exist(self):
        resources = v.expected_resources()
        self.assertGreater(len(resources), 0)
        root = v.ROOT / 'Sources/SurveillanceCore/Resources/RuntimeAssets'
        for path in resources.values():
            self.assertTrue(v.safe(root, path).is_file())

    def test_source_has_no_state_manufacturing_or_candidate_art(self):
        source = (v.ROOT / 'AppTests/ExistingArtEncounterTests.swift').read_text()
        for forbidden in ['testing_', 'seedScenario(', 'renderBenchmark(', 'installBenchmarkCameraFrames(', 'BenchmarkReviewArt(']:
            self.assertNotIn(forbidden, source)
        self.assertIn('GhostRun.replay(', source)
        self.assertIn('XCTAssertEqual(session.snapshot, snap)', source)


if __name__ == '__main__':
    unittest.main()
