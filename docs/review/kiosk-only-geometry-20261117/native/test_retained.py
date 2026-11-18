"""Retained-evidence checks on temporary copies of actual capture-01, never synthetic proof."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import retained as r

HERE = Path(__file__).resolve().parent
CAPTURE = HERE / 'capture-01'
EXECUTABLE = HERE / 'derived/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests'


class RetainedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='retained-regression-', dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'capture'
        shutil.copytree(CAPTURE, self.path)

    def reject(self):
        with self.assertRaises((AssertionError, RuntimeError, ValueError)):
            r.check(self.path, EXECUTABLE)

    def test_actual_retained_evidence_passes(self):
        self.assertEqual(r.check(self.path, EXECUTABLE)['images'], 18)

    def test_modified_image_rejected(self):
        image = next(self.path.glob('*.png'))
        image.write_bytes(image.read_bytes() + b'tampered')
        self.reject()

    def test_missing_image_rejected(self):
        next(self.path.glob('*.png')).unlink()
        self.reject()

    def test_unlisted_output_rejected(self):
        (self.path / 'unlisted.txt').write_text('not evidence')
        self.reject()

    def test_acceptance_claim_rejected(self):
        path = self.path / 'verification.json'
        value = json.loads(path.read_text())
        value['ownerAcceptance'] = True
        path.write_text(json.dumps(value))
        self.reject()

    def test_symlinked_receipt_rejected(self):
        receipt = self.path / 'verification.json'
        receipt.unlink()
        receipt.symlink_to(CAPTURE / 'verification.json')
        self.reject()

    def test_recataloged_authority_mutation_rejected(self):
        path = self.path / 'source-scene-records.json'
        value = json.loads(path.read_text())
        value['captures'][0]['actors'][0]['name'] = 'mutated-authority'
        path.write_text(json.dumps(value))
        receipt = self.path / 'verification.json'
        report = json.loads(receipt.read_text())
        report['files'][path.name] = r.n.sha(path)
        receipt.write_text(json.dumps(report))
        self.reject()


if __name__ == '__main__':
    unittest.main(verbosity=2)
