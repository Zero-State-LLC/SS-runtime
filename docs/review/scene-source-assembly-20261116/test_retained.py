#!/usr/bin/env python3
"""Mutate copies of actual retained evidence, never native results or source art."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import retained as r

HERE = Path(__file__).resolve().parent


class RetainedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR', str(HERE)))
        self.addCleanup(self.temp.cleanup)
        self.capture = Path(self.temp.name) / 'capture'
        shutil.copytree(HERE / 'native-capture-1040', self.capture)
        self.report = r.n.load(self.capture / 'verification.json')

    def save_report(self):
        (self.capture / 'verification.json').write_text(json.dumps(self.report))

    def change_record(self, change):
        path = self.capture / 'source-scene-records.json'
        record = r.n.load(path)
        change(record)
        path.write_text(json.dumps(record))
        self.report['files'][path.name] = r.n.sha(path)
        self.save_report()

    def rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            r.verify(self.capture)

    def test_actual_retained_evidence(self):
        report = r.verify(self.capture)
        self.assertEqual(report['images'], 18)
        self.assertFalse(report['ownerAcceptance'])
        self.assertIn('NOT_NEW_NATIVE_RUN', report['status'])

    def test_historical_fixture_not_current(self):
        self.report['fixtureVersion'] = 'source-scene-continuation-002-three-zooms'
        self.save_report()
        self.rejected('Historical fixture')

    def test_missing_png(self):
        next(self.capture.glob('*.png')).unlink()
        self.rejected('Missing or unexpected')

    def test_unexpected_file(self):
        (self.capture / 'unrequested.txt').write_text('not captured')
        self.rejected('Missing or unexpected')

    def test_corrupt_png(self):
        path = next(self.capture.glob('*.png'))
        path.write_bytes(path.read_bytes() + b'changed')
        self.rejected('hash drift')

    def test_omitted_environment_despite_rehashed_record(self):
        self.change_record(lambda value: value['captures'][0]['actors'].pop())
        self.rejected('inventory census')

    def test_duplicate_environment_despite_rehashed_record(self):
        def change(value):
            actors = value['captures'][0]['actors']
            actors[-1] = dict(actors[-2])
        self.change_record(change)
        self.rejected('Duplicate or omitted')

    def test_warped_basis_despite_rehashed_record(self):
        def change(value):
            value['captures'][0]['actors'][5]['projectedBasisX'] = [0.707, 0.354]
        self.change_record(change)
        self.rejected('X basis')

    def test_wrong_png_dimensions_despite_rehashed_record(self):
        def change(value):
            value['captures'][0]['nativePixels'] = [704, 326]
        self.change_record(change)
        self.rejected('PNG dimensions')

    def test_unearned_acceptance(self):
        self.report['ownerAcceptance'] = True
        self.save_report()
        self.rejected('Unearned')

    def test_binary_metadata_disagreement(self):
        self.report['testExecutable']['expectedBuildSHA256'] = '0' * 64
        self.save_report()
        self.rejected('executable provenance')

    def test_original_control_drift_despite_rehashed_record(self):
        def change(value):
            value['controlSHA256']['camera.png'] = '0' * 64
        self.change_record(change)
        self.rejected('original control drift')

    def test_runtime_ground_drift_despite_rehashed_record(self):
        def change(value):
            key = next(iter(value['runtimeSHA256']))
            value['runtimeSHA256'][key] = '0' * 64
        self.change_record(change)
        self.rejected('runtime ground drift')


if __name__ == '__main__':
    unittest.main(verbosity=2)
