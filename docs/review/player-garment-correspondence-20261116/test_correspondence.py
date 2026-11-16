import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import numpy as np
import render

HERE = Path(__file__).resolve().parent

class CorrespondenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads((HERE/'garment.json').read_text())
        cls.image,cls.layers,cls.owners = render.render(cls.model)
        cls.pixels = np.array(cls.image)
        cls.target = np.array(render.rgba(HERE/'inputs/south-baggy-neutral.png'))

    def test_exact_baggy_correspondence_and_patch(self):
        # Whole image exactness is stricter than a patch-area color/position heuristic.
        np.testing.assert_array_equal(self.pixels,self.target)
        self.assertEqual(render.sha(HERE/'south-neutral.png'),'a4ff7035ec256c613bc96eaf65b59a64e837c81adc895bcd4e5cd42e6f18a2a3')
        surface = self.model['surfaces'][1]
        self.assertEqual(surface['id'],'left_thigh')
        self.assertEqual(surface['anatomicalSide'],'left')
        self.assertEqual(surface['sheetRegion'],[614,69,943,685])

    def test_exact_source_copies(self):
        for path,entry in json.loads((HERE/'provenance.json').read_text()).items():
            self.assertEqual(render.sha(HERE/path),entry['sha256'],path)
        sheet = render.rgba(HERE/'inputs/source/trouser-sheet.png')
        for s in self.model['surfaces']:
            np.testing.assert_array_equal(np.array(sheet.crop(s['sheetRegion'])),np.array(render.rgba(HERE/s['material'])))

    def test_identity_upper_bytes(self):
        original = np.array(render.rgba(HERE/'inputs/source/south-neutral-original.png'))
        upper = np.array(render.rgba(HERE/'inputs/layers/original_upper.png'))
        opaque = upper[:,:,3] == 255
        np.testing.assert_array_equal(self.pixels[opaque],original[opaque])
        np.testing.assert_array_equal(self.pixels[:200],original[:200])
        self.assertGreater(int(opaque.sum()),21000)

    def test_boot_pixels_root_and_contact(self):
        original = np.array(render.rgba(HERE/'inputs/source/south-neutral-original.png'))
        boots = np.array(render.rgba(HERE/'inputs/layers/original_boots.png'))
        opaque = boots[:,:,3] == 255
        np.testing.assert_array_equal(self.pixels[opaque],original[opaque])
        np.testing.assert_array_equal(self.pixels[326:],original[326:])
        self.assertEqual(self.model['groundRoot'],[192,336])
        self.assertEqual(int(np.where(self.pixels[:,:,3]>0)[0].max()),358)
        for x0,x1 in [(150,187),(194,232)]:
            self.assertEqual(int(np.where(self.pixels[:,x0:x1,3]>0)[0].max()),358)

    def test_every_garment_pixel_has_explicit_triangle_owner(self):
        support = np.zeros(self.pixels.shape[:2],bool)
        for name,layer in self.layers.items():
            mask = np.array(layer)[:,:,3]>0
            self.assertTrue(np.all(self.owners[name][mask]>=0))
            support |= mask
        for path in self.model['retainedLayers']:
            support |= np.array(render.rgba(HERE/path))[:,:,3]>0
        self.assertTrue(np.all(support[self.pixels[:,:,3]>0]))
        self.assertEqual(self.model['hiddenSurfaces'],[])

    def test_alpha_correct_material_sampling(self):
        tex = np.array([[[255,0,0,255],[0,255,0,0]]],dtype=np.uint8)
        value = render.sample(tex,np.array([[.5,.5]]))[0]
        np.testing.assert_array_equal(value,[255,0,0,128])
        self.assertTrue(np.any((self.pixels[:,:,3]>0)&(self.pixels[:,:,3]<255)))

    def test_real_geometry_control_changes_visible_output_only(self):
        changed = copy.deepcopy(self.model)
        # A lower left-thigh grid row changes both triangle boundaries and material position.
        for i in range(20,25):
            changed['surfaces'][1]['vertices'][i]['position'][0] += 5
        image,layers,_ = render.render(changed)
        pixels = np.array(image)
        self.assertGreater(int(np.any(pixels!=self.pixels,axis=2).sum()),50)
        np.testing.assert_array_equal(pixels[:200],self.pixels[:200])
        np.testing.assert_array_equal(pixels[326:],self.pixels[326:])
        for name in ['right_thigh','right_shin_kneepad','left_shin_kneepad']:
            np.testing.assert_array_equal(np.array(layers[name]),np.array(self.layers[name]))

    def test_real_uv_control_changes_patch_without_other_parts(self):
        changed = copy.deepcopy(self.model)
        for i in range(10,20):
            changed['surfaces'][1]['vertices'][i]['uv'][0] += .12
        image,layers,_ = render.render(changed)
        self.assertGreater(int(np.any(np.array(image)!=self.pixels,axis=2).sum()),30)
        for name in ['right_thigh','right_shin_kneepad','left_shin_kneepad']:
            np.testing.assert_array_equal(np.array(layers[name]),np.array(self.layers[name]))

    def test_reject_unknown_version_and_degenerate_geometry(self):
        changed = copy.deepcopy(self.model)
        changed['schema']=2
        with self.assertRaises(ValueError):
            render.render(changed)
        changed = copy.deepcopy(self.model)
        changed['surfaces'][0]['vertices'][1]['position']=changed['surfaces'][0]['vertices'][0]['position'][:]
        with self.assertRaises(ValueError):
            render.render(changed)

    def test_standalone_replay_without_repository_or_flat_target_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'packet'
            shutil.copytree(HERE,dest)
            # Core render must work even with every flattened comparison absent.
            (dest/'inputs/south-baggy-neutral.png').unlink()
            (dest/'inputs/source/south-neutral-original.png').unlink()
            result = subprocess.run([sys.executable,'-B','-c',
                "import json,render; from pathlib import Path; p=Path('.'); im,_,_=render.render(json.loads((p/'garment.json').read_text()),p); im.save('standalone.png')"],cwd=dest,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(render.sha(dest/'standalone.png'),render.sha(HERE/'south-neutral.png'))
            # Full exporter replays all output bytes when comparison-only images are restored.
            for name in ['south-baggy-neutral.png','source/south-neutral-original.png']:
                shutil.copyfile(HERE/'inputs'/name,dest/'inputs'/name)
            result = subprocess.run([sys.executable,'-B','render.py'],cwd=dest,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            for name in ['south-neutral.png','comparison.png','mesh-overlay.png','build.json']:
                self.assertEqual((dest/name).read_bytes(),(HERE/name).read_bytes(),name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
