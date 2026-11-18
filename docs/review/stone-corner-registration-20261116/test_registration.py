"""Packet consistency guards only. These do not validate registration or fidelity."""
import hashlib
import json
import unittest
from pathlib import Path

PACKET = Path(__file__).resolve().parent

class RegistrationRecordTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((PACKET / 'registration.json').read_text())

    def test_original_unchanged(self):
        source = PACKET / self.record['source']
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                         '1226f74865aceafc0835501465e0be6aa94c8bbdad7f3b3e61af00a4af2ee475')

    def test_no_verified_registration(self):
        for key in ('observedWallContactLandmarks', 'hiddenWallContactLandmarks',
                    'groundContactAnchor', 'worldFootprintCorrespondence', 'uniformDrawScale'):
            with self.subTest(key=key):
                self.assertIn(key, self.record)
                self.assertIsNone(self.record[key])

    def test_gates_closed(self):
        for key in ('readyForNative', 'ownerAccepted', 'productionAdmitted'):
            self.assertIs(self.record[key], False)
        self.assertEqual(self.record['registrationBlocker'], 'MISSING_CORRESPONDENCE')

    def test_contour_is_provisional(self):
        diag = self.record['plintheBaseEdgeDiagnostic']
        self.assertIn('PROVISIONAL', diag['note'])
        for key in ('leftPlintheBase', 'rightPlintheBase'):
            self.assertIn('PROVISIONAL', diag[key]['interpretation'])
        self.assertNotIn('slopeAnalysis', self.record)
        self.assertNotIn('registrationConclusion', self.record)

    def test_corrected_preview_and_withdrawal(self):
        page = (PACKET / 'index.html').read_text()
        self.assertIn('Alpha contours are not wall contact', page)
        self.assertIn('prompt targets only', page)
        for name in ('native-size-preview.png', 'side-by-side-comparison.png', 'side-by-side-half.png'):
            self.assertFalse((PACKET / name).exists())
            self.assertTrue((PACKET / 'withdrawn' / name).is_file())
        self.assertTrue((PACKET / 'landmark-overlay.png').is_file())

if __name__ == '__main__':
    unittest.main(verbosity=2)
