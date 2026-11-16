#!/usr/bin/env python3
"""Focused painted-source integrity checks, not visual acceptance."""
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
import audit

HERE=Path(__file__).resolve().parent

def verify(root=HERE):
    record=json.loads((root/'preview-01/manifest.json').read_text())
    need=lambda value,message: None if value else (_ for _ in ()).throw(ValueError(message))
    need(record['status']==r.STATUS and record['visualAttempt']==1,'Status')
    need(not any(record[k] for k in ('ownerAccepted','productionAdmitted','nativeCapture')),'Acceptance scope')
    need(record['modelSHA256']==r.sha(root/'assembly.json'),'Assembly changed')
    need(record['rendererSHA256']==r.sha(root/'replay.py'),'Renderer changed')
    for name,item in record['inputs'].items():
        need(item['sha256']==r.sha(root/'inputs'/name),'Input changed '+name)
    for name,digest in record['exports'].items():
        need(digest==r.sha(root/'preview-01'/name),'Export changed '+name)
    need(len(record['exports'])==14,'Export census')
    return record

class PaintedAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=json.loads((HERE/'assembly.json').read_text())
        cls.master,cls.layers,cls.crops,cls.inspection=r.render(cls.model)

    def temporary(self):
        temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(HERE)))
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def test_01_actual_rgba_and_raw_generation_metadata(self):
        verify()
        for name in ('components','junction-box'):
            with Image.open(HERE/'inputs'/f'{name}.png') as im:
                self.assertEqual(im.size,(1254,1254))
                self.assertEqual(im.mode,'RGBA')
                self.assertEqual(im.getchannel('A').getextrema(),(0,255))
                self.assertGreater(im.getchannel('A').histogram()[0],1_000_000)
            meta=json.loads((HERE/'inputs'/f'{name}-generation.json').read_text())
            self.assertEqual(meta['response_item']['size'],'1254x1254')
            self.assertEqual(meta['response_item']['background'],'transparent')
            self.assertEqual(meta['response_item']['action'],'edit')

    def test_02_source_crops_exact_and_complete_visible_paint(self):
        for layer in self.model['layers']:
            name=layer['name']
            with Image.open(HERE/'inputs'/layer['source']) as original:
                expected=original.crop(tuple(layer['crop']))
                self.assertEqual(self.crops[name].tobytes(),expected.tobytes())
            with Image.open(HERE/'preview-01/source-layers'/f'{name}.png') as exported:
                self.assertEqual(exported.tobytes(),expected.tobytes())
            self.assertEqual(self.inspection[name]['discardedVisiblePixels'],0)
            self.assertEqual(self.inspection[name]['discardedAlpha1to15Pixels'],self.inspection[name]['discardedAlphaMass'])
            self.assertLess(self.inspection[name]['cropBorderMaxAlpha'],16)

    def test_03_opaque_and_rgb_fake_alpha_rejected(self):
        layer=self.model['layers'][0]
        for image in (Image.new('RGB',(1254,1254),'black'),Image.new('RGBA',(1254,1254),(30,30,30,255))):
            with self.assertRaises(ValueError):
                r.inspect_source(image,layer)

    def test_04_clipped_complete_component_rejected(self):
        for index in range(3):
            layer=copy.deepcopy(self.model['layers'][index])
            layer['crop'][1]+=100
            with Image.open(HERE/'inputs'/layer['source']) as original:
                with self.assertRaisesRegex(ValueError,'clips visible'):
                    r.inspect_source(original,layer)

    def test_05_head_move_is_independent_uniform_transform(self):
        model=copy.deepcopy(self.model)
        model['layers'][1]['position'][0]+=10
        moved,layers,_,_=r.render(model)
        self.assertNotEqual(moved.tobytes(),self.master.tobytes())
        self.assertNotEqual(layers['complete-head'].tobytes(),self.layers['complete-head'].tobytes())
        for name in ('complete-pole','junction-box'):
            self.assertEqual(layers[name].tobytes(),self.layers[name].tobytes())

    def test_06_hidden_pole_paint_survives_removal(self):
        bare,layers,_,_=r.render(self.model,omit=('complete-head','junction-box'))
        for point in ((56,100),(58,175)):
            self.assertGreater(layers['complete-pole'].getpixel(point)[3],240)
            self.assertEqual(bare.getpixel(point),layers['complete-pole'].getpixel(point))
            self.assertNotEqual(bare.getpixel(point),self.master.getpixel(point))

    def test_07_no_nonuniform_shader_or_external_source(self):
        for key,value in [('scaleX',.8),('shader','lighting'),('source','../reference.png'),('uniformScale',0)]:
            model=copy.deepcopy(self.model)
            model['layers'][0][key]=value
            with self.assertRaises(ValueError):
                r.render(model)

    def test_08_renderer_reads_only_two_supplied_sources(self):
        real=Image.open
        names=[]
        def checked(path,*args,**kwargs):
            self.assertIn(Path(path).name,('components.png','junction-box.png'))
            names.append(Path(path).name)
            return real(path,*args,**kwargs)
        with patch.object(r.Image,'open',checked):
            image,_,_,_=r.render(self.model)
        self.assertEqual(set(names),{'components.png','junction-box.png'})
        self.assertEqual(image.tobytes(),self.master.tobytes())

    def test_09_standalone_replay_identical(self):
        root=self.temporary()/'standalone'
        root.mkdir()
        for name in ('replay.py','assembly.json'):
            shutil.copy2(HERE/name,root/name)
        shutil.copytree(HERE/'inputs',root/'inputs')
        subprocess.run([sys.executable,'-W','error',str(root/'replay.py')],cwd=root,check=True,capture_output=True)
        a=verify()
        b=verify(root)
        self.assertEqual(a,b)
        self.assertEqual((root/'preview-01/manifest.json').read_bytes(),(HERE/'preview-01/manifest.json').read_bytes())
        for name in a['exports']:
            self.assertEqual((root/'preview-01'/name).read_bytes(),(HERE/'preview-01'/name).read_bytes())

    def test_10_tampered_input_and_export_detected(self):
        root=self.temporary()/'packet'
        root.mkdir()
        for name in ('replay.py','assembly.json'):
            shutil.copy2(HERE/name,root/name)
        for name in ('inputs','preview-01'):
            shutil.copytree(HERE/name,root/name)
        file=root/'inputs/components.png'
        original=file.read_bytes()
        file.write_bytes(original+b'invalid')
        with self.assertRaisesRegex(ValueError,'Input changed'):
            verify(root)
        file.write_bytes(original)
        file=root/'preview-01/camera-native.png'
        file.write_bytes(file.read_bytes()+b'invalid')
        with self.assertRaisesRegex(ValueError,'Export changed'):
            verify(root)

    def test_11_native_sizes_and_transparent_rgb(self):
        for name,size in [('camera-native.png',(42,104)),('camera-half.png',(21,52)),('camera-master.png',(180,450))]:
            with Image.open(HERE/'preview-01'/name) as im:
                self.assertEqual(im.size,size)
                self.assertEqual(im.mode,'RGBA')
                pixels=im.tobytes()
                self.assertTrue(all(pixels[i:i+3]==b'\x00\x00\x00' for i in range(0,len(pixels),4) if pixels[i+3]==0))

    def test_12_boundary_audit_reports_unresolved_margin(self):
        report=audit.audit()
        for item in report['assemblyBoundary'].values():
            self.assertTrue(item['sourcePaintGeometricBoundsInsideCanvas'])
        pole=report['assemblyBoundary']['complete-pole']
        self.assertGreater(pole['canvasBorderMaxAlpha'],0)
        self.assertFalse(pole['antialiasPaddingSatisfied'])
        self.assertFalse(report['ownerAccepted'])
        self.assertEqual(report,json.loads((HERE/'source-audit.json').read_text()))

if __name__=='__main__':
    unittest.main(verbosity=2)
