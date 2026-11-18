"""Actual independent roof-layer alpha, registration, mutation and composition checks."""
import copy
import math
import unittest
from pathlib import Path
from PIL import Image, ImageChops
import replay
P=Path(__file__).resolve().parent

class RoofLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=replay.load(P/'roof-layer.json')
        cls.reg=replay.load(P/'output/registration.json')
        cls.info=replay.load(P/'output/roof-layer-registration.json')
        with Image.open(P/'inputs/roof-vent.png') as im: cls.source=im.copy()
        cls.layer=replay.render_roof_layer(cls.spec,cls.reg)
        with Image.open(P/'output/building-alpha.png') as im: cls.building=im.copy()

    def test_raw_unchanged_true_alpha_not_opaque_background(self):
        self.assertEqual(replay.sha(P/'inputs/roof-vent.png'),'b99f0b536306bf317e897bda133640bd1e3ee14eeddcdb1871ec60209bea90f2')
        self.assertEqual(replay.sha(P/'inputs/roof-vent-provider.json'),'23fdd4da08a8aec3bf24f717e4e719c1b2e325ee6124b710f1c269f2c0cd2851')
        self.assertEqual(self.source.mode,'RGBA')
        self.assertEqual(self.source.size,(1254,1254))
        hist=self.source.getchannel('A').histogram()
        self.assertGreater(hist[0],1254*1254*.1)
        # Issue246: exact255 was a false premise, not a product opacity threshold.
        # These values were independently observed before changing the test.
        self.assertEqual(hist[0],1025198)
        self.assertEqual(hist[252],86412)
        self.assertEqual(hist[253],431845)
        self.assertEqual(hist[255],256)
        replay.validate_roof_alpha(self.source)
        self.assertGreater(sum(hist[1:255]),0)
        self.assertEqual(self.layer.getpixel((0,0))[3],0)
        self.assertEqual(self.layer.getchannel('A').getextrema()[0],0)
        self.assertGreaterEqual(self.layer.getchannel('A').getextrema()[1],250)

    def test_false_alpha_sources_rejected(self):
        mutations=[self.source.convert('RGB'),self.source.copy(),self.source.copy(),self.source.copy()]
        mutations[1].putalpha(255)
        mutations[2].putalpha(128)
        mutations[3].putalpha(self.source.getchannel('A').point(lambda a:128 if a else 0))
        for source in mutations:
            with self.assertRaises(AssertionError): replay.validate_roof_alpha(source)

    def test_only_three_source_texels_normalized(self):
        derived=replay.roof_material(self.spec)
        expected={(512,213),(873,919),(821,965)}
        diff={(i%1254,i//1254) for i,(a,b) in enumerate(zip(self.source.getdata(),derived.getdata())) if a!=b}
        self.assertEqual(diff,expected)
        for xy in expected:
            self.assertEqual(self.source.getpixel(xy),(255,0,255,1))
            self.assertEqual(derived.getpixel(xy),(0,0,0,0))
        with Image.open(P/'output/roof-vent-material.png') as exported:
            self.assertEqual(exported.tobytes(),derived.tobytes())
        for xy,value in [((512,213),(255,0,255,2)),((512,213),(0,0,0,0)),((12,12),(255,0,255,1))]:
            bad=self.source.copy()
            bad.putpixel(xy,value)
            with self.assertRaises(AssertionError): replay.normalize_roof_material(bad,self.spec)
        bad_spec=copy.deepcopy(self.spec)
        bad_spec['materialRGBRepairs'][0]['xy']=[12,12]
        with self.assertRaises(AssertionError): replay.normalize_roof_material(self.source,bad_spec)

    def test_exact_roof_z_and_independent_projection(self):
        x,y,z=self.spec['localWorldAnchor']
        self.assertEqual([x,y,z],[78,85,132])
        mesh=replay.load(P/'mesh.json')
        roof=next(f for f in mesh['faces'] if f['name']=='roof')
        self.assertTrue(all(mesh['vertices'][i][2]==z for i in roof['indices']))
        expected=[500+5*(x-y)/math.sqrt(2),1160-5*((x+y)/(2*math.sqrt(2))+z)]
        for actual,want in zip(self.info['projectedBuildingRoot'],expected): self.assertAlmostEqual(actual,want)
        self.assertEqual(self.info['worldAnchor'],[590,725,132])
        for k in (0,1):
            self.assertAlmostEqual(self.info['buildingPixelOrigin'][k]+.17*self.spec['sourceRoot'][k],expected[k])
        self.assertEqual(self.spec['uniformSourcePixelsToWorldUnits'],.17/5)
        self.assertFalse(self.spec['gameplayAuthority'])
        self.assertFalse(self.spec['includedInOBJ'])

    def test_root_anchor_z_and_scale_mutations_are_live(self):
        for field,delta in [('sourceRoot',40),('localWorldAnchor',10)]:
            spec=copy.deepcopy(self.spec)
            spec[field][-1]+=delta
            result=replay.render_roof_layer(spec,self.reg)
            self.assertNotEqual(result.tobytes(),self.layer.tobytes(),field)
            info=replay.roof_layer_registration(spec,self.reg)
            if field=='localWorldAnchor':
                self.assertAlmostEqual(info['projectedBuildingRoot'][1],self.info['projectedBuildingRoot'][1]-50)
        spec=copy.deepcopy(self.spec)
        spec['uniformSourceToBuildingPixels']=.21
        changed=replay.render_roof_layer(spec,self.reg)
        self.assertNotEqual(changed.tobytes(),self.layer.tobytes())
        info=replay.roof_layer_registration(spec,self.reg)
        self.assertEqual(info['projectedBuildingRoot'],self.info['projectedBuildingRoot'])
        # Both axes use exactly the same scalar, and the authored root stays registered.
        for k in (0,1):
            self.assertAlmostEqual(info['buildingPixelOrigin'][k]+.21*spec['sourceRoot'][k],info['projectedBuildingRoot'][k])

    def test_material_mutation_and_layer_removal(self):
        material=Image.new('RGBA',self.source.size,(30,190,80,255))
        material.putalpha(replay.roof_material(self.spec).getchannel('A'))
        changed=replay.render_roof_layer(self.spec,self.reg,material)
        self.assertNotEqual(changed.tobytes(),self.layer.tobytes())
        self.assertEqual(changed.getchannel('A').tobytes(),self.layer.getchannel('A').tobytes())
        self.assertNotEqual(Image.alpha_composite(self.building,changed).tobytes(),Image.alpha_composite(self.building,self.layer).tobytes())
        self.assertNotEqual(Image.alpha_composite(self.building,self.layer).tobytes(),self.building.tobytes())

    def test_exact_composition_layer_bounds_and_no_magenta(self):
        with Image.open(P/'output/preview-alpha.png') as expected:
            self.assertEqual(expected.tobytes(),Image.alpha_composite(self.building,self.layer).tobytes())
        with Image.open(P/'output/roof-layer-alpha.png') as expected:
            self.assertEqual(expected.tobytes(),self.layer.tobytes())
        bbox=self.layer.getchannel('A').getbbox()
        self.assertGreater(min(bbox[:2]),0)
        self.assertLess(bbox[2],1000)
        self.assertLess(bbox[3],1200)
        # Compositing a transparent layer cannot punch holes in the base mesh.
        composite=Image.alpha_composite(self.building,self.layer)
        self.assertIsNone(ImageChops.subtract(self.building.getchannel('A'),composite.getchannel('A')).getbbox())
        for r,g,b,a in composite.getdata():
            self.assertFalse(a>0 and r>180 and b>180 and g<100)

    def test_reintroduced_output_residue_fails_strict_guard(self):
        changed=self.layer.copy()
        changed.putpixel((444,60),(255,0,255,1))
        with self.assertRaises(AssertionError):
            for r,g,b,a in changed.getdata():
                self.assertFalse(a>0 and r>180 and b>180 and g<100)

    def test_original_building_geometry_registration_and_pixels_unchanged(self):
        hashes={'building-alpha.png':'86e47afa788dba29f5e62f765058a0befdbb3404b68b00d1a1a66ec1cd75d363','building.obj':'0ac6325294b8f22e9fdb89e5b6b5e72d439540b287bb15bab935100a8d44c404','building.mtl':'7aa20e10d162aad9238f0277c13dd4114e47a3ce7e8a5b3fa02b4ca6541a3c65','registration.json':'425e33108f4a7d94c1c8a1424a3d94e2ac5845b9600475669edc07da38693e52'}
        for name,digest in hashes.items(): self.assertEqual(replay.sha(P/'output'/name),digest,name)
        self.assertEqual(self.reg['authoritativeBounds'],[512,640,640,768])

if __name__=='__main__': unittest.main(verbosity=2)
