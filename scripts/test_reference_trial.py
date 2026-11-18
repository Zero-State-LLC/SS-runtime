#!/usr/bin/env python3
"""Regression checks for the static trial evidence verifier, not visual acceptance."""
import unittest
from unittest.mock import patch

import verify_reference_trial as trial


class ReferenceTrialEvidenceTests(unittest.TestCase):
    def test_complete_native_packet(self):
        result = trial.verify()
        self.assertEqual(result['plates'], 72)
        self.assertEqual(result['metrics'], 12)
        self.assertEqual(result['ownerChoice'], 'UNRECORDED')
        self.assertFalse(result['shippingMappingChanged'])

    def test_attachment_census(self):
        expected = trial.expected()
        self.assertEqual(len(expected), 85)
        self.assertEqual(list(expected.values()).count('png'), 72)
        self.assertEqual(list(expected.values()).count('json'), 13)

    def test_changed_capture_source_is_rejected(self):
        original = trial.digest
        target = trial.ROOT / 'AppTests/ReferenceProjectionTrial.swift'
        with patch.object(trial, 'digest', side_effect=lambda p: 'changed' if p == target else original(p)):
            with self.assertRaisesRegex(AssertionError, 'Capture source drift'):
                trial.verify()

    def test_changed_plate_is_rejected(self):
        original = trial.digest
        with patch.object(trial, 'digest', side_effect=lambda p: 'changed' if p.parent.name == 'plates' else original(p)):
            with self.assertRaisesRegex(AssertionError, 'Attachment bytes drift'):
                trial.verify()


if __name__ == '__main__':
    unittest.main()
