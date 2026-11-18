"""Temporary synthetic retained exports. None are real native evidence."""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
from test_native import n, r, synthetic


class RetainedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.root = Path(self.temp.name)
        self.capture = self.root / 'SYNTHETIC-NOT-NATIVE'; self.capture.mkdir()
        self.inputs = self.root / 'inputs'; self.inputs.mkdir()
        self.record, self.prepared, self.normalized = synthetic()
        for source in self.prepared['sources']:
            (self.inputs / source['file']).write_bytes(b'SYNTHETIC source mock')
        # Existing source hashes remain frozen, so bypass only staged-source hash reads
        # for these explicitly synthetic byte fixtures. Actual native/retained files use real hashes.
        self.input_file = self.inputs / 'native-inputs.json'
        self.save(self.input_file, self.prepared)
        self.record['inputSHA256'] = n.sha(self.input_file)
        for row in self.record['captures']:
            old = next(c for c in n.baseline()['captures'] if c['arm'] == 'candidate' and c['zoom'] == row['zoom'])
            for suffix in row['pngSHA256']:
                target = self.capture / (row['name'] + suffix + '.png')
                shutil.copyfile(n.BASELINE_CAPTURE / (old['name'] + suffix + '.png'), target)
                row['pngSHA256'][suffix] = n.sha(target)
        self.save(self.capture / 'source-scene-records.json', self.record)
        self.save(self.capture / 'summary.json', dict(result='Passed', passedTests=1, totalTestCount=1, failedTests=0, skippedTests=0, expectedFailures=0))
        self.save(self.capture / 'tests.json', dict(testNodes=[dict(nodeType='Test Case', nodeIdentifier=n.TEST, result='Passed')]))
        manifest = n.load(n.BASELINE_CAPTURE / 'attachment-manifest.json')
        manifest[0]['testIdentifier'] = n.TEST
        self.save(self.capture / 'attachment-manifest.json', manifest)
        self.report = dict(status=n.STATUS, fixtureVersion=n.FIXTURE_VERSION, nativeTests=1, captures=6, images=18,
                           xcresult='/SYNTHETIC/NOT-NATIVE.xcresult', inputSHA256=n.sha(self.input_file),
                           harnessSourceReadSHA256=self.record['harnessSourceReadSHA256'],
                           testExecutable=dict(loadedPath=self.record['loadedTestExecutable']['path'],
                                               loadedSHA256=self.record['loadedTestExecutable']['sha256'],
                                               expectedBuildPath='/SYNTHETIC/SSRuntimeTests.xctest/SSRuntimeTests',
                                               expectedBuildSHA256=self.record['loadedTestExecutable']['sha256']),
                           ownerAcceptance=False, physicalDeviceEvidence=False, animationFamilyEvidence=False, files={})
        self.rehash()

    def tearDown(self):
        self.temp.cleanup()

    def save(self, path, value):
        path.write_text(json.dumps(value, indent=2) + '\n')

    def rehash(self):
        self.report['files'] = {p.name: n.sha(p) for p in self.capture.iterdir() if p.name != 'verification.json'}
        self.save(self.capture / 'verification.json', self.report)

    def verify(self):
        original = r.n.sha
        sources = {self.inputs / s['file']: s['sha256'] for s in self.prepared['sources']}
        def staged_mock(path):
            return sources.get(Path(path), original(path))
        with patch.object(r.n, 'expected_input', return_value=self.prepared), \
             patch.object(r.n, 'validate_plan_binding', return_value=self.normalized), \
             patch.object(r.n, 'sha', side_effect=staged_mock):
            return r.verify(self.capture, self.inputs)

    def test_synthetic_retained_checks_nine_baseline_pairs(self):
        self.assertEqual(self.verify()['baselinePixelComparisons'], 9)

    def test_rehashed_wrong_test_export_rejected(self):
        manifest = n.load(self.capture / 'attachment-manifest.json')
        manifest[0]['testIdentifier'] = n.v7.TEST
        self.save(self.capture / 'attachment-manifest.json', manifest); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_authority_record_rejected(self):
        self.record['captures'][3]['cameraRoot'] = [1, 2]
        self.save(self.capture / 'source-scene-records.json', self.record); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_missing_contact_rejected(self):
        self.record['captures'][3]['visibleBuildingContacts'].pop()
        self.save(self.capture / 'source-scene-records.json', self.record); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_missing_attachment_rejected(self):
        manifest = n.load(self.capture / 'attachment-manifest.json'); manifest[0]['attachments'].pop()
        self.save(self.capture / 'attachment-manifest.json', manifest); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_baseline_pixel_forgery_rejected(self):
        row = self.record['captures'][0]; suffix = '-native'
        path = self.capture / (row['name'] + suffix + '.png')
        with Image.open(path) as image:
            image = image.convert('RGBA'); pixel = image.getpixel((0, 0))
            image.putpixel((0, 0), ((pixel[0] + 1) % 256, *pixel[1:])); image.save(path)
        row['pngSHA256'][suffix] = n.sha(path)
        self.save(self.capture / 'source-scene-records.json', self.record); self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_rehashed_wrong_binary_provenance_rejected(self):
        self.report['testExecutable']['loadedSHA256'] = '0' * 64; self.rehash()
        with self.assertRaises(ValueError): self.verify()

    def test_extra_retained_file_rejected(self):
        (self.capture / 'extra').write_bytes(b'x')
        with self.assertRaises(ValueError): self.verify()


if __name__ == '__main__':
    unittest.main()
