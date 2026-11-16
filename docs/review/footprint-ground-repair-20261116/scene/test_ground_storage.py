"""Issue253 source-only guards, not a new SpriteKit execution claim.
Actual storage probe is coordinator-owned ../ground-property-probe-2318.log.
"""
import hashlib
from pathlib import Path
import struct
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


class GroundStorageGuard(unittest.TestCase):
    def test_exact_ieee754_storage_value(self):
        stored = struct.unpack('f', struct.pack('f', .1))[0]
        self.assertEqual(stored, 0.10000000149011612)
        self.assertNotEqual(stored, .1)

    def test_only_authorized_assertion_line_changed(self):
        old_path = HERE / 'attempt-01-native2317/FootprintGroundSceneTests.swift'
        old = old_path.read_bytes()
        self.assertEqual(hashlib.sha256(old).hexdigest(), '47264781c7059f5dd7f650c30aac6ac1c50ebe913ab2270b9757f75ce0aed3c1')
        current = (ROOT / 'AppTests/FootprintGroundSceneTests.swift').read_text().splitlines()
        before = old.decode().splitlines()
        self.assertEqual(len(current), len(before))
        changed = [(a, b) for a, b in zip(before, current) if a != b]
        self.assertEqual(len(changed), 1)
        old_line, new_line = changed[0]
        old_condition = old_line.split(', "Ground patch coverage/transform drift')[0]
        new_condition = new_line.split(', "Ground patch coverage/transform drift')[0]
        self.assertEqual(new_condition, old_condition.replace('patch.zPosition == 0.1', 'patch.zPosition == CGFloat(Float(0.1))'))
        for field in ('size', 'anchor', 'zPosition', 'expectedStoredZ', 'hidden', 'alpha'):
            self.assertIn(field + '=', new_line)
        self.assertNotIn('accuracy:', new_line)
        self.assertNotIn('abs(', new_line)

    def test_failed_preparation_retains_old_harness_hash(self):
        import json
        path = HERE / 'attempt-01-native2317/native-inputs-v8/native-inputs.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), '01b8a38131be4157c3c8120cb6d378cdc21b5e31fb580673d1a46374604d5f78')
        self.assertEqual(json.loads(path.read_text())['harnessSourceSHA256'], '47264781c7059f5dd7f650c30aac6ac1c50ebe913ab2270b9757f75ce0aed3c1')


if __name__ == '__main__':
    unittest.main()
