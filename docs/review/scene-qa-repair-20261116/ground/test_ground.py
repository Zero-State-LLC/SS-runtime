#!/usr/bin/env python3
"""Portable ground tests. These do not certify native pixels or aesthetics."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageChops
import build as ground

class GroundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = ground.original()
        cls.spec, cls.source = cls.old.read_source()
        cls.tile, _ = cls.old.material(cls.spec, cls.source)
        cls.image = Image.open(ground.HERE/'ground-arena.png').convert('RGB')
        cls.manifest = json.loads((ground.HERE/'manifest.json').read_text())

    def assertPixelsEqual(self, a, b):
        self.assertEqual(a.size, b.size)
        self.assertIsNone(ImageChops.difference(a.convert('RGB'), b.convert('RGB')).getbbox())

    def test_01_authoritative_bounds_and_registration(self):
        self.assertEqual(ground.bounds(), [0,0,2304,1536])
        self.assertEqual(self.image.size, (4608,3072))
        self.assertEqual(self.manifest['registration']['worldOriginBottomLeft'], [0,0])
        self.assertEqual(self.manifest['registration']['pixelsPerWorldUnit'], 2)

    def test_02_red_capable_real_v4_crop_coverage(self):
        report = ground.coverage(self.spec['corner']['worldBounds'])
        self.assertEqual([round(r['zoom'],2) for r in report['results']], [1,1.25,1.4])
        self.assertTrue(all(not r['covered'] for r in report['results']))
        result = subprocess.run([sys.executable, str(ground.HERE/'build.py'), '--probe','v4'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)['passed'])

    def test_03_fixed_crop_coverage_and_inverse_roundtrip(self):
        self.assertTrue(ground.coverage(ground.bounds())['passed'])
        for row in ground.rows():
            for sx,sy in [(-352,-163),(352,163),(0,0),(352,-163),(-352,163)]:
                x,y = ground.inverse(row,sx,sy)
                dx,dy = x-row['centerWorld'][0],y-row['centerWorld'][1]
                self.assertAlmostEqual(row['zoom']*(dx-dy)/2**.5,sx)
                self.assertAlmostEqual(row['zoom']*(dx+dy)/(2*2**.5),sy)
        # Mutation: shifting the full texture east exposes the captured crop.
        self.assertFalse(ground.coverage([700,0,3004,1536])['passed'])

    def test_04_entire_original_interior_exact(self):
        # Pixel equality includes drain, tactile panel, crossing, rails, manhole,
        # rounded/straight curb and the material's absolute-world phase.
        with Image.open(ground.ORIGINAL/'corner-topdown.png') as old:
            self.assertPixelsEqual(self.image.crop((896,1152,2048,2304)), old)
        shifted = self.image.crop((898,1152,2050,2304))
        with Image.open(ground.ORIGINAL/'corner-topdown.png') as old:
            self.assertIsNotNone(ImageChops.difference(shifted,old).getbbox())

    def test_05_no_artificial_old_patch_boundary(self):
        # Independently render strips spanning ALL FOUR former finite edges.
        # Exact oracle equality allows real curb/joints, but rejects a rectangular
        # beige/asphalt seam, alpha edge or a clamped/repeated finite motif.
        for rect in [[444,380,452,964],[1020,380,1028,964],
                     [444,380,1028,388],[444,956,1028,964]]:
            spec = copy.deepcopy(self.spec)
            spec['corner']['worldBounds'] = rect
            expected = self.old.context(spec,self.tile)
            x0,y0,x1,y1 = rect
            actual = self.image.crop((x0*2,(1536-y1)*2,x1*2,(1536-y0)*2))
            self.assertPixelsEqual(actual,expected)
            damaged = actual.copy()
            damaged.paste((200,180,150),(0,0,1,damaged.height))
            self.assertIsNotNone(ImageChops.difference(damaged,expected).getbbox())

    def test_06_opaque_complete_arena_and_no_repeated_motif(self):
        with Image.open(ground.HERE/'ground-arena.png') as image:
            self.assertEqual(image.mode,'RGB')
            self.assertEqual(image.convert('RGBA').getchannel('A').getextrema(),(255,255))
        # Rails keep their absolute x through both old horizontal boundaries.
        for x in [860,900]:
            for y in [100,383,384,960,961,1400]:
                self.assertEqual(self.image.getpixel((x*2,(1536-y)*2)),(29,29,29))
        # A whole-corner tile would create another drain 576 world units away.
        self.assertNotEqual(self.image.getpixel((814*2,(1536-674)*2)),
                            self.image.getpixel(((814+576)*2,(1536-674)*2)))

    def test_07_square_groundpatch_uv_adapter(self):
        with Image.open(ground.HERE/'ground-patch-square.png') as adapter:
            self.assertEqual(adapter.size,(4608,4608))
            self.assertPixelsEqual(adapter.crop((0,1536,4608,4608)),self.image)
            # WorldRenderer.swift:458-474 crops bottom-left [0,0,1,2/3].
            self.assertEqual(self.manifest['groundPatches']['tileUnits'],2304)
            self.assertEqual(self.manifest['groundPatches']['normalizedTextureRect'],[0,0,1,2/3])

    def test_08_immutable_sources_fail_closed(self):
        self.assertEqual(ground.dependencies(),self.manifest['dependenciesSHA256'])
        with patch.object(ground,'sha',return_value='0'*64):
            with self.assertRaisesRegex(ValueError,'Immutable dependency changed'):
                ground.dependencies()

    def test_09_deterministic_rebuild_and_output_hashes(self):
        before = ground.dependencies()
        with tempfile.TemporaryDirectory(prefix='rebuild-',dir=ground.HERE) as temp:
            rebuilt = ground.build(Path(temp))
            self.assertEqual(rebuilt,self.manifest)
            for name,digest in self.manifest['outputsSHA256'].items():
                self.assertEqual(ground.sha(ground.HERE/name),digest)
                self.assertEqual(ground.sha(Path(temp)/name),digest)
        self.assertEqual(ground.dependencies(),before)

if __name__ == '__main__':
    unittest.main(verbosity=2)
