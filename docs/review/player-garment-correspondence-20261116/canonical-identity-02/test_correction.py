"""Issue245 correction tests. Original strict identity/contact/alpha methods inherited unchanged."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import render

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retained_tests',HERE/'pilot01-test_correspondence.py')
retained=importlib.util.module_from_spec(spec)
spec.loader.exec_module(retained)

class CanonicalCorrectionTests(retained.CorrespondenceTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owned,cls.derivative=render.identity_inputs(cls.model,HERE)
        cls.original=np.array(render.rgba(HERE/'inputs/source/south-neutral-original.png'))

    def test_exact_baggy_correspondence_and_patch(self):
        # Explicit new authority, never a tolerance: canonical inside, exact baggy outside.
        predicted=self.target.copy()
        predicted[self.owned]=self.original[self.owned]
        np.testing.assert_array_equal(self.pixels,predicted)
        np.testing.assert_array_equal(self.pixels[~self.owned],self.target[~self.owned])
        np.testing.assert_array_equal(self.pixels[self.owned],self.original[self.owned])
        changed=np.any(self.pixels!=self.target,axis=2)
        np.testing.assert_array_equal(changed,self.owned & np.any(self.original!=self.target,axis=2))
        self.assertEqual(int(changed.sum()),198)
        self.assertEqual(int(changed[:200].sum()),157)
        self.assertEqual(render.sha(HERE/'south-neutral.png'),'b32bfcba5ac7cee383715d5f0b918e53b2e7be56634886754ab82357431d6ed4')
        left=self.model['surfaces'][1]
        self.assertEqual((left['id'],left['anatomicalSide'],left['sheetRegion']),('left_thigh','left',[614,69,943,685]))

    def test_exact_source_copies(self):
        for path,entry in json.loads((HERE/'source-provenance.json').read_text()).items():
            self.assertEqual(render.sha(HERE/path),entry['sha256'],path)
        sheet=render.rgba(HERE/'inputs/source/trouser-sheet.png')
        for s in self.model['surfaces']:
            np.testing.assert_array_equal(np.array(sheet.crop(s['sheetRegion'])),np.array(render.rgba(HERE/s['material'])))

    def test_every_garment_pixel_has_explicit_triangle_owner(self):
        support=self.owned.copy()
        for name,layer in self.layers.items():
            mask=np.array(layer)[:,:,3]>0
            self.assertTrue(np.all(self.owners[name][mask]>=0))
            support |= mask
        for path in self.model['retainedLayers']:
            support |= np.array(render.rgba(HERE/path))[:,:,3]>0
        self.assertTrue(np.all(support[self.pixels[:,:,3]>0]))
        self.assertEqual(self.model['hiddenSurfaces'],[])

    def test_pilot01_exact_old_target_and_real_identity_failure(self):
        pilot,_,_=render.garment.render(self.model,HERE)
        np.testing.assert_array_equal(np.array(pilot),self.target)
        np.testing.assert_array_equal(np.array(render.rgba(HERE/'pilot01.png')),self.target)
        self.assertEqual(render.sha(HERE/'pilot01.png'),'a4ff7035ec256c613bc96eaf65b59a64e837c81adc895bcd4e5cd42e6f18a2a3')
        # Run the original strict assertion, not a relaxed restatement of it.
        check=retained.CorrespondenceTests('test_identity_upper_bytes')
        check.pixels=np.array(pilot)
        with self.assertRaises(AssertionError):
            check.test_identity_upper_bytes()
        self.assertIn('FAILED (failures=1)',(HERE/'pilot01-tests.log').read_text())

    def test_exact_partial_alpha_replacement_not_alpha_over(self):
        for x,y in [(125,119),(123,124)]:
            np.testing.assert_array_equal(self.pixels[y,x],self.original[y,x])
            self.assertEqual(int(self.pixels[y,x,3]),254)
        edge=self.owned & (self.original[:,:,3]>0) & (self.original[:,:,3]<255)
        np.testing.assert_array_equal(self.pixels[edge],self.original[edge])
        wrong=render.rgba(HERE/'pilot01.png')
        wrong.alpha_composite(render.rgba(HERE/'canonical-upper-derivative.png'))
        self.assertFalse(np.array_equal(np.array(wrong)[edge],self.original[edge]))

    def test_declared_ownership_is_source_derived(self):
        upper=np.array(render.rgba(HERE/'inputs/layers/original_upper.png'))
        expected=upper[:,:,3]>0
        expected[:200] |= self.original[:200,:,3]>0
        np.testing.assert_array_equal(self.owned,expected)
        self.assertEqual(int(expected.sum()),22664)
        self.assertFalse(np.any(self.owned[326:]))

    def test_mask_mutation_rejected_even_with_updated_file_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'packet'
            shutil.copytree(HERE,dest)
            policy=json.loads((dest/'identity-policy.json').read_text())
            mask=(self.owned*255).astype(np.uint8)
            mask[280,180]=255
            Image.fromarray(mask).save(dest/policy['mask'])
            policy['maskSHA256']=render.sha(dest/policy['mask'])
            (dest/'identity-policy.json').write_text(json.dumps(policy))
            with self.assertRaisesRegex(ValueError,'Ownership differs'):
                render.render(self.model,dest)

    def test_derivative_mutation_rejected_even_with_updated_file_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'packet'
            shutil.copytree(HERE,dest)
            policy=json.loads((dest/'identity-policy.json').read_text())
            derivative=self.derivative.copy()
            derivative[119,125,0]+=1
            Image.fromarray(derivative).save(dest/policy['derivative'])
            policy['derivativeSHA256']=render.sha(dest/policy['derivative'])
            (dest/'identity-policy.json').write_text(json.dumps(policy))
            with self.assertRaisesRegex(ValueError,'Derivative differs'):
                render.render(self.model,dest)

    def test_native_half_exact_aspect_svg(self):
        root=ET.parse(HERE/'comparison.svg').getroot()
        images=root.findall('{http://www.w3.org/2000/svg}image')
        self.assertEqual(len(images),9)
        for image in images:
            self.assertAlmostEqual(float(image.attrib['height'])/float(image.attrib['width']),416/384,places=12)
            self.assertTrue((HERE/image.attrib['href']).is_file())
        self.assertEqual(sum(float(i.attrib['width'])==64 for i in images),3)
        self.assertEqual(sum(float(i.attrib['width'])==32 for i in images),3)

    def test_standalone_replay_without_repository_or_flat_target_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'packet'
            shutil.copytree(HERE,dest)
            for name in ['inputs/south-baggy-neutral.png','pilot01.png']:
                (dest/name).unlink()
            result=subprocess.run([sys.executable,'-B','-c',"import json,render; from pathlib import Path; p=Path('.'); im,_,_=render.render(json.loads((p/'garment.json').read_text()),p); im.save('standalone.png')"],cwd=dest,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(render.sha(dest/'standalone.png'),render.sha(HERE/'south-neutral.png'))
            for name in ['inputs/south-baggy-neutral.png','pilot01.png']:
                shutil.copyfile(HERE/name,dest/name)
            result=subprocess.run([sys.executable,'-B','render.py'],cwd=dest,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            for name in ['south-neutral.png','comparison.png','comparison.svg','build.json']:
                self.assertEqual((dest/name).read_bytes(),(HERE/name).read_bytes(),name)

if __name__=='__main__':
    unittest.main(verbosity=2)
