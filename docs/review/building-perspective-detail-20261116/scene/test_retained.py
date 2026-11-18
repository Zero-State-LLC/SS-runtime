"""Temporary synthetic retained/importer mocks. NOT captured or executed evidence.
No files are written in a real v7 native-inputs/native-capture packet.
"""
import copy
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
spec = importlib.util.spec_from_file_location('_building_retained_test_helpers', HERE / 'test_native.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
r, n = h.r, h.r.n


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


class RetainedMutations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='SYNTHETIC-v7-unit-test-', dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.root = Path(self.temp.name)
        self.capture = self.root / 'mock-capture'; self.capture.mkdir()
        self.inputs = self.root / 'mock-inputs'; self.inputs.mkdir()
        self.record, self.prepared = h.synthetic()
        for source in self.prepared['sources']:
            path = self.inputs / source['file']
            if source['role'] in n.BASE_ROLES:
                shutil.copyfile(n.V6 / 'native-inputs-v6' / source['file'], path)
            else:
                Image.new('RGBA', tuple(source['registration']['canvasPixels']), (22, 33, 44, 255)).save(path)
                source['sha256'] = n.sha(path)
        self.record['sourceSHA256'] = {s['role']: s['sha256'] for s in self.prepared['sources']}
        save(self.inputs / 'native-inputs.json', self.prepared)
        self.record['inputSHA256'] = n.sha(self.inputs / 'native-inputs.json')
        self.binary = self.root / 'SSRuntimeTests.xctest/SSRuntimeTests'
        self.binary.parent.mkdir(); self.binary.write_bytes(b'SYNTHETIC TEST BYTES NOT AN EXECUTABLE')
        self.record['loadedTestExecutable']['sha256'] = n.sha(self.binary)
        for row in self.record['captures']:
            row['buildingSourceSHA256'] = n.expected_building_hashes(row, self.prepared)
            row['groundFootprints'] = n.footprint_expected(row, self.prepared)
            row['nativePixels'] = [704, 326]
            for suffix in row['pngSHA256']:
                path = self.capture / (row['name'] + suffix + '.png')
                size = (352, 163) if suffix == '-half' else (704, 326)
                Image.new('RGB', size, (11, 11, 11)).save(path)
                row['pngSHA256'][suffix] = n.sha(path)
        save(self.capture / 'source-scene-records.json', self.record)
        save(self.capture / 'summary.json', dict(result='Passed', passedTests=1, totalTestCount=1,
                                               failedTests=0, skippedTests=0, expectedFailures=0))
        save(self.capture / 'tests.json', dict(testNodes=[dict(nodeType='Test Case', nodeIdentifier=n.TEST, result='Passed')]))
        manifest = [dict(testIdentifier=n.TEST, attachments=[dict(suggestedHumanReadableName=name + ('.json' if name.endswith('records') else '.png'),
                        exportedFileName=name + ('.json' if name.endswith('records') else '.png'),
                        isAssociatedWithFailure=False, deviceId='SYNTHETIC-NOT-A-NATIVE-RUN')
                        for name in sorted(n.NAMES | {'source-scene-records'})])]
        save(self.capture / 'attachment-manifest.json', manifest)
        self.report = dict(status=n.STATUS, fixtureVersion=n.FIXTURE_VERSION, nativeTests=1, captures=6, images=18,
                           inputSHA256=self.record['inputSHA256'], harnessSourceReadSHA256=self.record['harnessSourceReadSHA256'],
                           testExecutable=dict(loadedPath=self.record['loadedTestExecutable']['path'],
                                               loadedSHA256=n.sha(self.binary), expectedBuildSHA256=n.sha(self.binary),
                                               expectedBuildPath=str(self.binary)),
                           ownerAcceptance=False, physicalDeviceEvidence=False, animationFamilyEvidence=False)
        self.rehash()
        self.binding = patch.object(n, 'expected_input', return_value=self.prepared)
        self.binding.start()

    def tearDown(self):
        self.binding.stop(); self.temp.cleanup()

    def rehash(self):
        self.report['files'] = {p.name: n.sha(p) for p in self.capture.iterdir() if p.name != 'verification.json'}
        save(self.capture / 'verification.json', self.report)

    def verify(self):
        return r.verify(self.capture, self.inputs)

    def mutate_record(self, change):
        change(self.record)
        save(self.capture / 'source-scene-records.json', self.record)
        self.rehash()

    def mock_import(self, output):
        def query(command, **kwargs):
            name = 'summary.json' if command[4] == 'summary' else 'tests.json'
            return (self.capture / name).read_text()
        def export(command, **kwargs):
            destination = Path(command[-1]); destination.mkdir()
            for path in self.capture.iterdir():
                if path.name == 'attachment-manifest.json':
                    shutil.copyfile(path, destination / 'manifest.json')
                elif path.name.endswith('.png') or path.name == 'source-scene-records.json':
                    shutil.copyfile(path, destination / path.name)
        with patch.dict(n._import_globals, {'expected_input': lambda *args: self.prepared, 'PREPARED_DIR': 'mock-inputs'}), \
             patch.object(n.v6.subprocess, 'check_output', side_effect=query), \
             patch.object(n.v6.subprocess, 'run', side_effect=export):
            return n.import_result(self.root / 'SYNTHETIC.xcresult', output, self.binary, root=n.ROOT, packet=self.root)

    def test_mock_importer_v7_integration_not_native_run(self):
        output = self.root / 'mock-imported'
        report = self.mock_import(output)
        self.assertEqual((report['nativeTests'], report['captures'], report['images']), (1, 6, 18))
        self.assertEqual(report['fixtureVersion'], n.FIXTURE_VERSION)
        self.assertEqual(r.verify(output, self.inputs)['images'], 18)

    def test_mock_importer_rejects_actual_binary_mismatch_before_output(self):
        self.binary.write_bytes(b'changed built bytes')
        output = self.root / 'must-not-exist'
        with self.assertRaises(ValueError): self.mock_import(output)
        self.assertFalse(output.exists())

    def test_mock_importer_rejects_retired_test_identity(self):
        tree = n.load(self.capture / 'tests.json')
        tree['testNodes'][0]['nodeIdentifier'] = n.v6.TEST
        save(self.capture / 'tests.json', tree)
        output = self.root / 'must-not-exist'
        with self.assertRaises(ValueError): self.mock_import(output)
        self.assertFalse(output.exists())

    def test_mock_retained_not_new_native(self):
        result = self.verify()
        self.assertEqual(result['status'], 'RETAINED_BYTES_AND_CONTRACT_VERIFIED_NOT_NEW_NATIVE_RUN')
        self.assertIn('not a fresh local binary', result['binaryCheck'])

    def test_actual_optional_binary_recheck(self):
        result = r.verify(self.capture, self.inputs, self.binary)
        self.assertIn('rehashed', result['binaryCheck'])
        self.binary.write_bytes(b'forged executable')
        with self.assertRaises(ValueError): r.verify(self.capture, self.inputs, self.binary)

    def test_rehashed_forged_actor(self):
        self.mutate_record(lambda rec: rec['captures'][0]['actors'][0].update(worldRoot=[1, 2]))
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_forged_authority(self):
        self.mutate_record(lambda rec: rec['captures'][0].update(cameraFieldOrigin='forged'))
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_forged_ground_vertex(self):
        self.mutate_record(lambda rec: rec['captures'][3]['groundFootprints'][0]['projectedSource'][0].__setitem__(0, 123))
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_forged_baseline(self):
        self.mutate_record(lambda rec: rec.update(baselineRecordSHA256='0' * 64))
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_missing_actual_binary(self):
        self.mutate_record(lambda rec: rec.pop('loadedTestExecutable'))
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_forged_provenance_disagreement(self):
        self.report['testExecutable']['expectedBuildSHA256'] = 'f' * 64
        self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_zero_test_summary(self):
        summary = n.load(self.capture / 'summary.json'); summary.update(totalTestCount=0, passedTests=0)
        save(self.capture / 'summary.json', summary); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_missing_image_even_with_rehashed_manifest(self):
        next(self.capture.glob('*.png')).unlink(); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_unknown_retained_version(self):
        self.report['fixtureVersion'] = 'source-scene-future-999'; self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_extra_retained_file(self):
        (self.capture / 'unexpected.txt').write_text('not evidence')
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_empty_attachment_manifest_rejected(self):
        save(self.capture / 'attachment-manifest.json', []); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_old_test_attachment_manifest_rejected(self):
        manifest = n.load(self.capture / 'attachment-manifest.json')
        manifest[0]['testIdentifier'] = n.v6.TEST
        save(self.capture / 'attachment-manifest.json', manifest); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_duplicate_attachment_manifest_rejected(self):
        manifest = n.load(self.capture / 'attachment-manifest.json')
        manifest[0]['attachments'][1] = manifest[0]['attachments'][0]
        save(self.capture / 'attachment-manifest.json', manifest); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_prepared_source_rehash_cannot_change_bound_bytes(self):
        (self.inputs / 'paving.png').write_bytes(b'forged source')
        with self.assertRaises(ValueError): self.verify()


if __name__ == '__main__':
    unittest.main()
