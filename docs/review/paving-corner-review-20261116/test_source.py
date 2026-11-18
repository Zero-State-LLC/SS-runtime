"""Portable material/layout checks. They do not certify visual fidelity."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from PIL import Image, ImageChops, ImageOps
import build as b


class PavingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec, cls.source = b.read_source()
        cls.tile, cls.rows = b.material(cls.spec, cls.source)
        cls.root = Path(__file__).resolve().parent

    @classmethod
    def tearDownClass(cls):
        cls.source.close()
        cls.tile.close()

    def test_exact_deterministic_export_rebuild(self):
        retained = json.loads((self.root/'manifest.json').read_text())
        with tempfile.TemporaryDirectory(dir=self.root) as directory:
            report = b.build(Path(directory))
            self.assertEqual(report, retained)
            for name, digest in retained['outputs'].items():
                self.assertEqual(b.sha(self.root/name), digest)

    def test_input_and_parameter_hashes_bound(self):
        record = json.loads((self.root/'manifest.json').read_text())
        self.assertEqual(record['sourceSHA256'], b.sha(self.root/'source.json'))
        self.assertEqual(record['inputSHA256'], self.spec['inputSHA256'])
        with tempfile.TemporaryDirectory(dir=self.root) as directory:
            spec = copy.deepcopy(self.spec)
            spec['input'] = str((self.root/self.spec['input']).resolve())
            spec['inputSHA256'] = '0'*64
            root = Path(directory)
            (root/'source.json').write_text(json.dumps(spec))
            with mock.patch.object(b, 'HERE', root):
                with self.assertRaisesRegex(ValueError, 'digest changed'):
                    b.read_source()

    def test_all_64_material_cells_distinct_not_four_slab_repeat(self):
        self.assertEqual(len(self.rows), 64)
        self.assertEqual(len({row['pixelsSHA256'] for row in self.rows}), 64)
        self.assertEqual(len({tuple(row['sourceSlabs']) for row in self.rows}), 64)
        self.assertEqual(self.tile.size, (1024,1024))
        self.assertEqual(self.spec['slabWorldUnits'], 32)
        self.assertEqual(self.spec['slabsPerSupertile']*32, 256)

    def test_exact_opposite_edges_and_no_widened_joint(self):
        w,h = self.tile.size
        self.assertEqual(self.tile.crop((0,0,1,h)).tobytes(), self.tile.crop((w-1,0,w,h)).tobytes())
        self.assertEqual(self.tile.crop((0,0,w,1)).tobytes(), self.tile.crop((0,h-1,w,h)).tobytes())
        self.assertEqual(self.spec['jointBlendPixels'], 1.5)
        self.assertEqual(self.tile.getpixel((0,64)), tuple(self.spec['jointRGB']))
        self.assertNotEqual(self.tile.getpixel((2,64)), tuple(self.spec['jointRGB']))

    def test_authored_curb_join_and_decorative_side_placement(self):
        layout = self.spec['corner']
        x,y,r = layout['verticalEdgeX'],layout['horizontalEdgeY'],layout['radius']
        for point in [(x,y+r),(x-r,y)]:
            self.assertAlmostEqual(b.curb_distance(*point,layout),0)
        self.assertLess(b.curb_distance(x-r,y+r,layout),0)
        self.assertGreater(b.curb_distance(x+10,y+r,layout),0)
        tx,ty,_,_ = layout['tactile']
        dx,dy,_,_ = layout['drain']
        self.assertLess(b.curb_distance(tx,ty,layout),0)
        self.assertGreater(b.curb_distance(dx,dy,layout),layout['curbWidth'])
        self.assertEqual(layout['worldBounds'], [448,384,1024,960])

    def test_grayscale_and_transparency_preserved(self):
        with Image.open(self.root/'corner-midpoint-preview.png') as color:
            with Image.open(self.root/'corner-midpoint-grayscale.png') as gray:
                self.assertEqual(color.size, (704,352))
                self.assertEqual(color.getchannel('A').tobytes(),gray.getchannel('A').tobytes())
                self.assertEqual(ImageOps.grayscale(color).tobytes(),gray.getchannel('R').tobytes())
                self.assertEqual(gray.getchannel('R').tobytes(),gray.getchannel('G').tobytes())
                self.assertEqual(gray.getchannel('G').tobytes(),gray.getchannel('B').tobytes())
                self.assertEqual(color.getchannel('A').getextrema(), (0,255))

    def test_no_native_or_collision_acceptance_claim(self):
        record = json.loads((self.root/'manifest.json').read_text())
        self.assertEqual(record['status'], 'SOURCE_MATERIAL_PROPOSAL_NOT_NATIVE_OR_ACCEPTED')
        self.assertIn('Finite eight-slab repeat, not aperiodic',record['limits'])
        self.assertTrue(any('not changed collision' in item for item in record['limits']))
        self.assertTrue(any('not native' in item for item in record['limits']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
