"""Technical source checks only. Passing does not establish visual acceptance."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock
import numpy as np
from PIL import Image

import build_south as b


class SouthSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parent
        cls.work = cls.root / 'editable'
        cls.before = b.sha(cls.root / 'south-neutral.png')
        subprocess.run([sys.executable, '-B', str(cls.root / 'build_south.py')], check=True)
        cls.model = json.loads((cls.work / 'model.json').read_text())
        cls.record = json.loads((cls.root / 'south-build.json').read_text())

    def test_byte_exact_rebuild_and_model_binding(self):
        self.assertEqual(b.sha(self.root / 'south-neutral.png'), self.before)
        self.assertEqual(self.record['outputSHA256'], self.before)
        self.assertEqual(self.record['modelSHA256'], b.sha(self.work / 'model.json'))

    @unittest.skipUnless(all((b.ORIGINAL / name).is_dir() for name in b.NAMES),
                         'External original audit unavailable; portable source checks still run')
    def test_original_sources_release5_13_and_benchmark_unchanged(self):
        original = json.loads((self.root / 'original-input-hashes.json').read_text())
        self.assertEqual(b.inventory(), original)
        for phase in [5, 13]:
            names = [name for name in original if name.startswith(f'SS-player-settle-prototype/phase-{phase:02d}/frames/') and name.endswith('.png')]
            self.assertEqual(len(names), 17)
        self.assertEqual(self.record['settleSeconds'], .375)

    def test_recovered_identity_paint_exact_no_flat_baggy_texture_import(self):
        original = b.NEUTRAL / 'source/body-source'
        for path in sorted(original.glob('*.png')):
            self.assertEqual(b.sha(path), b.sha(self.work / 'source/body-source' / path.name))
        # Visible head/shoulders/satchel area remains exact, not reinterpreted.
        old = np.array(Image.open(b.NEUTRAL / 'frames/00.png').convert('RGBA'))
        new = np.array(Image.open(self.root / 'south-neutral.png').convert('RGBA'))
        np.testing.assert_array_equal(old[:200], new[:200])
        self.assertNotIn('south-baggy-neutral', (self.work / 'thigh.py').read_text())

    def test_actual_geometry_controls_and_fixed_length_skeleton(self):
        sample = json.loads((self.work / 'source/samples.json').read_text())
        self.assertEqual(len(sample), 1)
        for leg in sample[0]['legs']:
            self.assertAlmostEqual(math.dist(leg['hip'], leg['knee']), 12.5)
            self.assertAlmostEqual(math.dist(leg['knee'], leg['ankle']), 14.5)
            self.assertEqual(leg['hip'][2], self.model['neutralHipHeight'])
            self.assertEqual(leg['heel'][2], 0)
            self.assertEqual(leg['toe'][2], 0)
        self.assertIn("MODEL['thighProfile']", (self.work / 'thigh.py').read_text())
        self.assertIn("MODEL['calfProfile']", (self.work / 'boot/source/boot_geometry.py').read_text())

    def test_real_alpha_registered_canvas_not_background_removal(self):
        image = Image.open(self.root / 'south-neutral.png')
        self.assertEqual(image.mode, 'RGBA')
        self.assertEqual(image.size, (384, 416))
        alpha = np.array(image)[:, :, 3]
        self.assertEqual(int(alpha.min()), 0)
        self.assertEqual(int(alpha.max()), 255)
        self.assertFalse(alpha[0].any() or alpha[-1].any() or alpha[:, 0].any() or alpha[:, -1].any())
        self.assertEqual(self.model['root'], [192, 336])

    def test_source_face_owned_part_boundaries_nonempty_and_disjoint(self):
        for side in ['right', 'left']:
            cloth = np.array(Image.open(self.work / f'parts/{side}-thigh-cloth.png'))[:, :, 3] > 0
            knee = np.array(Image.open(self.work / f'parts/{side}-knee-cover.png'))[:, :, 3] > 0
            self.assertTrue(cloth.any())
            self.assertTrue(knee.any())
            self.assertFalse(np.logical_and(cloth, knee).any())
        self.assertIn('owner[sl][mask]=2 if fi>=64 else 1', (self.work / 'thigh.py').read_text())

    def test_knee_shell_has_actual_final_composite_coverage(self):
        for side in ['right', 'left']:
            with Image.open(self.work / f'parts/{side}-visible-knee.png') as image:
                visible = np.array(image) > 0
            with Image.open(self.work / f'parts/{side}-knee-cover.png') as image:
                source = np.array(image)[:, :, 3] > 0
            self.assertTrue(visible.any(), 'No knee pixels survived final composition')
            self.assertFalse((visible & ~source).any())
        self.assertGreater(self.model['kneeCoverAnteriorOffset'], 0)
        self.assertLess(self.model['kneeCoverDepthRadius'], self.model['kneeCoverRadius'])

    def test_bilinear_paint_uses_alpha_and_underpaint_without_dark_halo(self):
        sys.path.insert(0, str(self.work))
        try:
            from thigh import cloth_sample
            texture = np.array([[[100,100,100,255],[0,0,0,0]],
                                [[100,100,100,255],[0,0,0,0]]], dtype=np.uint8)
            actual = cloth_sample(texture, np.array([[.5]]), np.array([[.5]]), base=(60,60,60))
            np.testing.assert_array_equal(actual, [[[80,80,80]]])
        finally:
            sys.path.pop(0)

    def test_portable_rebuild_does_not_require_external_originals(self):
        with mock.patch.object(b, 'ORIGINAL', self.root / 'absent-external-originals'):
            b.main()
            record = json.loads((self.root / 'south-build.json').read_text())
            self.assertEqual(record['externalOriginalAudit'], 'unavailable')
            self.assertIsNone(record['originalFilesUnchanged'])
            self.assertEqual(b.sha(self.root / 'south-neutral.png'), self.before)
        b.main()

    def test_south_gate_and_no_family_or_runtime_acceptance_claim(self):
        self.assertFalse(self.record['familyExpanded'])
        self.assertEqual(self.record['status'], 'SOUTH_FIRST_PROPOSED_NOT_ACCEPTED')
        self.assertFalse(any(self.root.glob('north*.png')))
        self.assertFalse(any(self.root.glob('east*.png')))
        self.assertFalse(any(self.root.glob('west*.png')))
        html = (self.root / 'index.html').read_text()
        self.assertIn('not native capture', html)
        self.assertIn('Upper remains layered paint', html)
        self.assertIn('height:34.666667px', html)


if __name__ == '__main__':
    unittest.main()
