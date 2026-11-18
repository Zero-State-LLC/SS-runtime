#!/usr/bin/env python3
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import replay as r
import verify as v

HERE = Path(__file__).resolve().parent

class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads((HERE/'model.json').read_text())
        cls.master,cls.layers,_ = r.render(cls.model)

    def temporary(self):
        temp = tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR', str(HERE)))
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def modified(self,name):
        model = copy.deepcopy(self.model)
        return model,next(p for p in model['parts'] if p['name']==name)

    def assert_only_component_changed(self, layers, name):
        for key in layers:
            if key == name:
                self.assertNotEqual(layers[key].tobytes(),self.layers[key].tobytes())
            else:
                self.assertEqual(layers[key].tobytes(),self.layers[key].tobytes(),key)

    def test_01_manifest_and_actual_metadata(self):
        self.assertEqual(v.verify()['exports'],38)
        prov=json.loads((HERE/'provenance.json').read_text())
        self.assertEqual(prov['actualMaterialSize'],[1254,1254])
        self.assertNotEqual(prov['actualMaterialSize'],prov['requestedMaterialSize'])
        meta=json.loads((HERE/'inputs/iron-generation.json').read_text())
        self.assertEqual(meta['response_item']['size'],'1254x1254')
        self.assertEqual(meta['response_item']['action'],'generate')
        self.assertEqual(prov['files']['iron.png']['mode'],'RGB')

    def test_02_uv_edit_changes_only_mapped_component(self):
        model,p=self.modified('pole')
        p['uv'][0] += 100
        master,layers,_=r.render(model)
        self.assert_only_component_changed(layers,'pole')
        self.assertEqual(master.getchannel('A').tobytes(),self.master.getchannel('A').tobytes())
        self.assertNotEqual(master.tobytes(),self.master.tobytes())

    def test_03_shading_edit_changes_only_component(self):
        model,p=self.modified('hood')
        p['shading']['ambient'] *= .65
        _,layers,_=r.render(model)
        self.assert_only_component_changed(layers,'hood')
        self.assertEqual(layers['hood'].getchannel('A').tobytes(),self.layers['hood'].getchannel('A').tobytes())

    def test_04_geometry_mutation_changes_contour(self):
        model,p=self.modified('hood')
        p['transform'][0] *= .8
        _,layers,_=r.render(model)
        self.assert_only_component_changed(layers,'hood')
        self.assertNotEqual(layers['hood'].getchannel('A').tobytes(),self.layers['hood'].getchannel('A').tobytes())

    def test_05_hidden_complete_geometry_survives_omission(self):
        image,layers,_=r.render(self.model,omit=('middle_ring',))
        self.assertGreater(layers['pole'].getpixel((45,300))[3],250)
        self.assertGreater(image.getpixel((45,300))[3],250)
        self.assertNotEqual(image.getpixel((45,300)),self.master.getpixel((45,300)))
        self.assertEqual(layers['pole'].tobytes(),self.layers['pole'].tobytes())

    def test_06_material_is_only_render_image_dependency(self):
        real=Image.open
        opened=[]
        def restricted(path,*args,**kwargs):
            self.assertEqual(Path(path).resolve(),(HERE/'inputs/iron.png').resolve())
            opened.append(path)
            return real(path,*args,**kwargs)
        with patch.object(r.Image,'open',restricted):
            image,_,_=r.render(self.model)
        self.assertEqual(len(opened),1)
        self.assertEqual(image.tobytes(),self.master.tobytes())

    def test_07_bad_status_uv_and_external_material_fail_closed(self):
        for mutate in [lambda m:m.update(schema=99),lambda m:m.update(status='ACCEPTED'),
                       lambda m:m['parts'][0].update(uv=[1200,0,360,640]),
                       lambda m:m['parts'][0].update(material='../../reference.png')]:
            model=copy.deepcopy(self.model)
            mutate(model)
            with self.assertRaises(ValueError):
                r.render(model)

    def test_08_clean_copy_replay_all_exports_identical(self):
        root=self.temporary()/'standalone'
        root.mkdir()
        # Only this packet's required files, no repository or sibling paths.
        for name in ('replay.py','model.json','provenance.json','verify.py'):
            shutil.copy2(HERE/name,root/name)
        shutil.copytree(HERE/'inputs',root/'inputs')
        subprocess.run([sys.executable,str(root/'replay.py')],cwd=root,check=True,capture_output=True)
        a=json.loads((HERE/'pilot-01/manifest.json').read_text())
        b=json.loads((root/'pilot-01/manifest.json').read_text())
        self.assertEqual(a,b)
        self.assertEqual((HERE/'pilot-01/manifest.json').read_bytes(),(root/'pilot-01/manifest.json').read_bytes())
        for name in a['exports']:
            self.assertEqual((HERE/'pilot-01'/name).read_bytes(),(root/'pilot-01'/name).read_bytes(),name)
        subprocess.run([sys.executable,str(root/'verify.py')],cwd=root,check=True,capture_output=True)

    def test_09_corrupted_input_and_output_detected(self):
        root=self.temporary()/'packet'
        shutil.copytree(HERE,root,ignore=shutil.ignore_patterns('__pycache__','tmp*'))
        target=root/'inputs/iron.png'
        original=target.read_bytes()
        target.write_bytes(original+b'corruption')
        with self.assertRaisesRegex(ValueError,'Input hash'):
            v.verify(root)
        target.write_bytes(original)
        target=root/'pilot-01/camera-native.png'
        target.write_bytes(target.read_bytes()+b'corruption')
        with self.assertRaisesRegex(ValueError,'Export hash'):
            v.verify(root)

    def test_10_corrections_are_explicit_and_material_is_preserved(self):
        prior=json.loads((HERE/'inputs/prior-geometry.json').read_text())
        old={p['name']:p for p in prior['parts']}
        now={p['name']:p for p in self.model['parts']}
        self.assertEqual(set(old),set(now))
        self.assertEqual(now['hood']['transform'][:2],[.95,.85])
        self.assertEqual(now['foot']['transform'][:2],[.92,.9])
        self.assertNotEqual(now['bracket']['contour'],old['bracket']['contour'])
        self.assertEqual(now['pole']['contour'],old['pole']['contour'])
        prov=json.loads((HERE/'provenance.json').read_text())
        self.assertEqual(r.sha(HERE/'inputs/iron.png'),prov['files']['iron.png']['sha256'])

    def test_11_broad_surface_gain_remains_editable(self):
        model,p=self.modified('service_box')
        p['faces'][0]['gain'] *= .5
        _,layers,_=r.render(model)
        self.assert_only_component_changed(layers,'service_box')

if __name__=='__main__':
    unittest.main(verbosity=2)
