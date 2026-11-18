"""Retained-material kiosk geometry and real rendered-output checks."""
import copy
import math
from pathlib import Path
import tempfile
import unittest
from PIL import Image
import build as b


class TexturedKioskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current, cls.candidate, cls.mapping, cls.dependencies = b.inputs()
        cls.output = b.HERE / 'output'
        cls.manifest = b.load(cls.output / 'manifest.json')
        cls.bindings = b.load(cls.output / 'bindings.json')

    def test_exact_manifest_closure_and_no_acceptance(self):
        self.assertEqual(self.manifest['inputs'], self.dependencies)
        self.assertFalse(self.manifest['ownerAcceptance'])
        self.assertFalse(self.manifest['productionAdmitted'])
        paths = {str(p.relative_to(self.output)): p for p in self.output.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        self.assertEqual(set(paths), set(self.manifest['outputs']))
        for name, path in paths.items():
            self.assertFalse(path.is_symlink())
            self.assertEqual(b.sha(path), self.manifest['outputs'][name])

    def test_all_three_current_layers_reproduce_v9(self):
        for name in ['building-alpha.png', 'roof-layer-alpha.png', 'source-full.png']:
            with Image.open(self.output / 'current' / name) as image:
                self.assertTrue(b.rgba_equal(image.convert('RGBA'), b.OLD / 'output' / name))

    def test_candidate_exact_rerender_and_composition(self):
        textures = b.base.textures(b.load(b.OLD / 'materials.json'))
        image = b.replay.render(self.candidate, textures)
        reg = b.registration(self.candidate)
        roof = b.base.render_roof_layer(b.roof_spec('candidate', self.mapping), reg)
        for value, name in [(image, 'building-alpha.png'), (roof, 'roof-layer-alpha.png'),
                            (Image.alpha_composite(image, roof), 'source-full.png')]:
            self.assertTrue(b.rgba_equal(value, self.output / 'candidate' / name))

    def test_registrations_derive_only_from_authored_mesh(self):
        for arm, mesh in [('current', self.current), ('candidate', self.candidate)]:
            reg = b.load(self.output / arm / 'registration.json')
            self.assertEqual(reg, b.registration(mesh))
            self.assertEqual(reg['worldPosition'], [512, 640])
            self.assertEqual(reg['authoritativeBounds'], [512, 640, 640, 768])
            self.assertEqual(reg['sourcePixelsPerWorldUnit'], 5)
            for canvas, draw in zip(reg['canvasPixels'], reg['drawSizeWorld']):
                self.assertAlmostEqual(canvas / draw, 5)
            self.assertFalse(reg['ownerAccepted'])
            self.assertFalse(reg['productionAdmitted'])

    def test_ground_correspondence_and_virtual_corner_disclosure(self):
        for arm in ['current', 'candidate']:
            reg = b.load(self.output / arm / 'registration.json')
            for world, point in zip(reg['groundBoundaryWorld'], reg['groundPixelsTopLeft']):
                x, y = world[0] - 512, world[1] - 640
                self.assertAlmostEqual((point[0] - reg['rootPixelsTopLeft'][0]) / 5, (x - y) / math.sqrt(2))
                self.assertAlmostEqual((reg['rootPixelsTopLeft'][1] - point[1]) / 5, (x + y) / (2 * math.sqrt(2)))
            self.assertIn('virtual', reg['groundBoundaryProvenance'][0])
            self.assertIn('not visible', reg['groundBoundaryProvenance'][0])

    def test_vent_only_follows_roof_z(self):
        old = b.load(self.output / 'current/roof-spec.json')
        new = b.load(self.output / 'candidate/roof-spec.json')
        self.assertEqual(old['localWorldAnchor'], [78, 85, 125])
        self.assertEqual(new['localWorldAnchor'], [78, 85, 100])
        restored = copy.deepcopy(new)
        restored['localWorldAnchor'][2] = 125
        self.assertEqual(restored, old)
        for arm in ['current', 'candidate']:
            reg = b.load(self.output / arm / 'registration.json')
            self.assertEqual(b.load(self.output / arm / 'roof-layer-registration.json'),
                             b.base.roof_layer_registration(b.roof_spec(arm, self.mapping), reg))

    def test_topology_material_uv_xy_and_z_are_exact(self):
        b.validate_geometry(self.current, self.candidate, self.mapping)
        self.assertEqual(self.current['faces'], self.candidate['faces'])
        self.assertEqual([v[:2] for v in self.current['vertices']], [v[:2] for v in self.candidate['vertices']])

    def test_xy_mutation_rejected(self):
        candidate = copy.deepcopy(self.candidate)
        candidate['vertices'][0][0] += 1
        with self.assertRaises(ValueError):
            b.validate_geometry(self.current, candidate, self.mapping)

    def test_uv_material_and_z_mutations_rejected(self):
        for kind in ['uv', 'material', 'z']:
            candidate = copy.deepcopy(self.candidate)
            if kind == 'uv':
                candidate['faces'][0]['uv'][0][0] += .01
            elif kind == 'material':
                candidate['faces'][0]['material'] = 'other'
            else:
                candidate['vertices'][0][2] += .1
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                b.validate_geometry(self.current, candidate, self.mapping)

    def test_alpha_is_real_and_not_clipped_to_canvas(self):
        for arm in ['current', 'candidate']:
            with Image.open(self.output / arm / 'source-full.png') as image:
                self.assertEqual(image.mode, 'RGBA')
                alpha = image.getchannel('A')
                left, top, right, bottom = alpha.getbbox()
                self.assertGreater(left, 0)
                self.assertGreater(top, 0)
                self.assertLess(right, image.width)
                self.assertLess(bottom, image.height)
                self.assertGreater(alpha.histogram()[0], 10000)
                self.assertGreater(alpha.histogram()[255], 10000)

    def test_bindings_match_actual_new_sources(self):
        for arm in ['current', 'candidate']:
            binding = self.bindings[arm]
            self.assertEqual(binding['sourceSHA256'], b.sha(self.output / binding['sourceFile']))
            reg = b.load(self.output / arm / 'registration.json')
            self.assertEqual(binding['registration'], {key: reg[key] for key in binding['registration']})
        self.assertNotEqual(self.bindings['current']['sourceSHA256'], self.bindings['candidate']['sourceSHA256'])
        self.assertEqual(self.bindings['current']['registration']['canvasPixels'][0], self.bindings['candidate']['registration']['canvasPixels'][0])

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory(dir=b.HERE) as directory:
            target = Path(directory)
            sentinel = target / 'keep.txt'
            sentinel.write_text('preserve')
            with self.assertRaises(ValueError):
                b.build(target)
            self.assertEqual(sentinel.read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main(verbosity=2)
