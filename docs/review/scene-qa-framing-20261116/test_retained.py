"""Portable SYNTHETIC v6 packet mutations. No new native evidence is claimed."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

HERE = Path(__file__).resolve().parent

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

r = module('_qa6_retained_tests', 'retained.py')
f = module('_qa6_synthetic_fixtures', 'test_native.py')


class RetainedV6Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.addCleanup(self.temp.cleanup)
        self.capture = Path(self.temp.name) / 'SYNTHETIC-capture'
        self.prepared = Path(self.temp.name) / 'SYNTHETIC-prepared'
        self.capture.mkdir()
        self.prepared.mkdir()
        self.record, inputs = f.synthetic_fixture()
        for source in inputs['sources']:
            shutil.copyfile(r.n.V5 / 'native-inputs-v5' / source['file'], self.prepared / source['file'])
        self.save(self.prepared / 'native-inputs.json', inputs)
        self.record['inputSHA256'] = r.n.sha(self.prepared / 'native-inputs.json')
        for row in self.record['captures']:
            row['nativePixels'] = [704, 326]
            for suffix in row['pngSHA256']:
                path = self.capture / (row['name'] + suffix + '.png')
                # Deliberately blank synthetic rasters, NOT screenshots.
                image = Image.new('RGB', (352, 163) if suffix == '-half' else (704, 326), 'gray')
                image.save(path)
                image.close()
                row['pngSHA256'][suffix] = r.n.sha(path)
        self.save(self.capture / 'source-scene-records.json', self.record)
        self.save(self.capture / 'summary.json', dict(result='Passed', passedTests=1, totalTestCount=1,
                  failedTests=0, skippedTests=0, expectedFailures=0, syntheticFixture=True))
        self.save(self.capture / 'tests.json', {'testNodes': [{'nodeType': 'Test Case', 'nodeIdentifier': r.n.TEST, 'result': 'Passed'}]})
        self.save(self.capture / 'attachment-manifest.json', [{'SYNTHETIC': 'NOT AN XCRESULT EXPORT'}])
        binary = self.record['loadedTestExecutable']
        self.report = dict(status=r.n.STATUS, fixtureVersion=r.n.FIXTURE_VERSION, nativeTests=1, captures=6, images=18,
                           inputSHA256=self.record['inputSHA256'], harnessSourceReadSHA256=self.record['harnessSourceReadSHA256'],
                           ownerAcceptance=False, physicalDeviceEvidence=False, animationFamilyEvidence=False,
                           syntheticFixture=True, testExecutable=dict(loadedPath=binary['path'], loadedSHA256=binary['sha256'],
                           expectedBuildPath='/SYNTHETIC/build/SSRuntimeTests.xctest/SSRuntimeTests', expectedBuildSHA256=binary['sha256']),
                           files={path.name: r.n.sha(path) for path in self.capture.iterdir()})
        self.save_report()
        # Only source admission is substituted: validation, image bytes, hashes,
        # authority, binary agreement and every record invariant run normally.
        self.binding = patch.object(r.n, 'expected_input', return_value=inputs)
        self.binding.start()
        self.addCleanup(self.binding.stop)

    @staticmethod
    def save(path, value):
        path.write_text(json.dumps(value, indent=2) + '\n')

    def save_report(self):
        self.save(self.capture / 'verification.json', self.report)

    def change_record(self, change):
        change(self.record)
        path = self.capture / 'source-scene-records.json'
        self.save(path, self.record)
        self.report['files'][path.name] = r.n.sha(path)
        self.save_report()

    def verify(self):
        return r.verify(self.capture, self.prepared)

    def test_synthetic_packet_contract_only(self):
        result = self.verify()
        self.assertEqual(result['images'], 18)
        self.assertIn('NOT_NEW_NATIVE_RUN', result['status'])
        self.assertFalse(result['ownerAcceptance'])

    def test_historical_v5_not_current(self):
        self.binding.stop()
        with self.assertRaisesRegex(ValueError, 'Historical'):
            r.verify(r.n.V5 / 'native-capture-v5')

    def test_unearned_acceptance_rejected(self):
        for field in ('ownerAcceptance', 'physicalDeviceEvidence', 'animationFamilyEvidence'):
            self.report[field] = True
            self.save_report()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Unearned'):
                self.verify()
            self.report[field] = False

    def test_edited_bytes_rejected(self):
        path = self.capture / 'summary.json'
        path.write_text(path.read_text() + ' ')
        with self.assertRaisesRegex(ValueError, 'hash drift'):
            self.verify()

    def test_rehashed_outline_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3].update(playerOutlineAlpha=1))
        with self.assertRaisesRegex(ValueError, 'outline'):
            self.verify()

    def test_rehashed_footprint_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3]['depthItems'][2].update(footprint=None))
        with self.assertRaisesRegex(ValueError, 'footprint|geometry'):
            self.verify()

    def test_rehashed_shadow_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3].update(playerShadowWorldRoot=[0, 0]))
        with self.assertRaisesRegex(ValueError, 'Shadow'):
            self.verify()

    def test_rehashed_ground_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3].update(groundBounds=[0, 0, 2304, 2304]))
        with self.assertRaisesRegex(ValueError, 'Ground'):
            self.verify()

    def test_rehashed_ground_source_adapter_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3].update(groundSourceWorldSize=[2304, 1536]))
        with self.assertRaisesRegex(ValueError, 'Ground'):
            self.verify()

    def test_rehashed_projected_shadow_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3].update(playerShadowProjectedRoot=[0, 0]))
        with self.assertRaisesRegex(ValueError, 'Projected shadow'):
            self.verify()

    def test_rehashed_visible_control_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3]['framing']['visibleControls'][0].update(bounds=[0, 0, 1, 1]))
        with self.assertRaisesRegex(ValueError, 'visible control bounds'):
            self.verify()

    def test_rehashed_actor_canvas_forgery_rejected(self):
        self.change_record(lambda record: record['captures'][3]['framing']['actorCanvasBounds'][1].update(bounds=[0, 0, 1, 1]))
        with self.assertRaisesRegex(ValueError, 'actor canvas'):
            self.verify()

    def test_executable_hash_disagreement(self):
        self.report['testExecutable']['expectedBuildSHA256'] = '0' * 64
        self.save_report()
        with self.assertRaisesRegex(ValueError, 'executable provenance'):
            self.verify()

    def test_image_hash_disagreement_even_after_report_rehash(self):
        row = self.record['captures'][0]
        path = self.capture / (row['name'] + '-native.png')
        image = Image.new('RGB', (704, 326), 'red')
        image.save(path)
        image.close()
        self.report['files'][path.name] = r.n.sha(path)
        self.save_report()
        with self.assertRaisesRegex(ValueError, 'hash disagreement'):
            self.verify()

    def test_preparation_hash_disagreement(self):
        path = self.prepared / 'native-inputs.json'
        path.write_text(path.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'input manifest drift'):
            self.verify()

    def test_symlink_and_extra_file_rejected(self):
        path = self.capture / 'summary.json'
        outside = Path(self.temp.name) / 'summary.json'
        path.rename(outside)
        path.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlinked'):
            self.verify()

    def test_extra_file_rejected(self):
        (self.capture / 'unexpected.txt').write_text('SYNTHETIC')
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            self.verify()

    def test_source_read_provenance_disagreement(self):
        self.report['harnessSourceReadSHA256'] = '0' * 64
        self.save_report()
        with self.assertRaisesRegex(ValueError, 'Source-read'):
            self.verify()

    def test_import_collision_safe(self):
        import sys
        with patch.dict(sys.modules, {'native': object(), 'assemble': object(), 'retained': object()}):
            loaded = module('_qa6_retained_collision', 'retained.py')
            self.assertEqual(loaded.n.FIXTURE_VERSION, r.n.FIXTURE_VERSION)


if __name__ == '__main__':
    unittest.main(verbosity=2)
