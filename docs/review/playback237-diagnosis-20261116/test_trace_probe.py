import hashlib
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from trace_probe import diagnose

ROOT = Path(__file__).resolve().parent


class RetainedPlaybackRegression(unittest.TestCase):
    def load(self, index):
        return json.loads((ROOT / 'evidence' / f'act{index}.json').read_text())

    def test_retained_provenance_hashes(self):
        manifest = json.loads((ROOT / 'evidence/attachments.json').read_text())
        self.assertEqual(manifest['artifact'], 14198828420)
        self.assertEqual(len(manifest['attachments']), 6)
        for attachment in manifest['attachments']:
            raw = (ROOT / 'evidence' / attachment['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), attachment['sha256'])

    def test_exact_failed_case_and_five_controls(self):
        for index in range(6):
            with self.subTest(index=index):
                self.assertEqual(diagnose(self.load(index))['missing'],
                                 [15] if index == 4 else [])
        rows = self.load(4)
        self.assertEqual(len(rows), 63)
        self.assertTrue(all(r['tracksPlayer'] for r in rows))
        self.assertTrue(all(not r['reducedMotion'] for r in rows))
        self.assertTrue(all(r['magnification'] == 1.25 for r in rows))

    def test_strict_cli_remains_red_on_real_failure(self):
        result = subprocess.run([sys.executable, str(ROOT / 'trace_probe.py'),
                                 str(ROOT / 'evidence/act4.json'), '--require-all-poses'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)['missing'], [15])

    def test_regular_retained_control_is_green(self):
        result = subprocess.run([sys.executable, str(ROOT / 'trace_probe.py'),
                                 str(ROOT / 'evidence/act0.json'), '--require-all-poses'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_actual_gaps_and_unattributed_time(self):
        gaps = diagnose(self.load(4))['gaps']
        first = next(g for g in gaps if g['fromTick'] == 29)
        second = next(g for g in gaps if g['fromTick'] == 49)
        self.assertEqual((first['fromFrame'], first['toFrame']), (14, 0))
        self.assertAlmostEqual(first['spriteKitDelta'], 0.06444891666660624)
        self.assertEqual((second['fromFrame'], second['toFrame']), (9, 3))
        self.assertGreater(second['outsidePreviousUpdateSeconds'], 0.299)
        self.assertLess(second['previousUpdateSeconds'], 0.018)

    def test_deleted_observation_is_not_reconstructed(self):
        rows = [r for r in self.load(0) if r['frame'] != 15]
        self.assertEqual(diagnose(rows)['missing'], [15])

    def test_fail_closed_on_empty_invalid_or_reversed_trace(self):
        with self.assertRaises(ValueError):
            diagnose([])
        invalid = copy.deepcopy(self.load(4))
        invalid[0]['frame'] = 16
        with self.assertRaises(ValueError):
            diagnose(invalid)
        with self.assertRaises(ValueError):
            diagnose(list(reversed(self.load(4))))


if __name__ == '__main__':
    unittest.main()
