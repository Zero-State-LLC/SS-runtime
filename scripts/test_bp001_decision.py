#!/usr/bin/env python3
"""Regression tests for BP-001 evidence verification, not art acceptance."""
import copy
import json
import unittest
from unittest.mock import patch

import verify_bp001_decision as audit


class DecisionEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provenance = json.loads((audit.PACK / "capture-provenance.json").read_text())
        cls.palette = json.loads((audit.PACK / "palette-report.json").read_text())

    def test_real_committed_evidence(self):
        result = audit.verify()
        self.assertEqual(result["plates"], 24)
        self.assertEqual(result["ownerChoice"], "UNRECORDED")
        self.assertFalse(result["shippingMappingChanged"])

    def test_changed_source_is_rejected(self):
        original = audit.sha
        def changed(path):
            return "0" * 64 if path == audit.ROOT / audit.SOURCES[0] else original(path)
        with patch.object(audit, "sha", side_effect=changed):
            with self.assertRaisesRegex(AssertionError, "capture source changed"):
                audit.verify()

    def test_changed_plate_is_rejected(self):
        original = audit.sha
        def changed(path):
            return "0" * 64 if path.parent == audit.PLATES else original(path)
        with patch.object(audit, "sha", side_effect=changed):
            with self.assertRaisesRegex(AssertionError, "plate drift"):
                audit.verify()

    def test_owner_acceptance_cannot_be_inferred(self):
        bad = copy.deepcopy(self.provenance)
        bad["ownerChoice"] = "MIDPOINT_ACCEPTED"
        with patch.object(audit.json, "loads", side_effect=[bad]):
            with self.assertRaises(AssertionError):
                audit.verify()

    def test_changed_measurement_is_rejected(self):
        bad = copy.deepcopy(self.palette)
        bad["plates"][0]["meanLuminance"] = 0
        with patch.object(audit.json, "loads", side_effect=[self.provenance, bad]):
            with self.assertRaisesRegex(AssertionError, "palette drift"):
                audit.verify()


if __name__ == "__main__":
    unittest.main()
