#!/usr/bin/env python3
"""Focused source tests, not a visual acceptance score."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageOps

HERE=Path(__file__).resolve().parent
ATTEMPT=Path(os.environ.get('CAMERA_SURFACE_ATTEMPT',str(HERE/'attempt-01')))
spec=importlib.util.spec_from_file_location('surface_build',ATTEMPT/'source/build.py')
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
OLD=HERE.parent/'camera-editable-master-20261116'
PINNED={'attempt-01':'0097c829d1dee2d0dd0b98c5b0f126ac40cce6e7c4c015f3a762144176a65dde',
        'attempt-02':'eee5365461132b98a7badf2cbf74e9ee4a4530345b2982c44cf0e56d8525dc59'}
REFERENCE_SHA='49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image(path):
    with Image.open(path) as im:
        return im.copy()


def hidden_check(model,root):
    order=[part['name'] for part in model['parts']]
    for probe in model['hidden']:
        point=tuple(probe['point'])
        under=image(root/'layers'/f'{probe["under"]}--underpaint.png')
        over=image(root/'layers'/f'{probe["over"]}--complete.png')
        assert order.index(probe['under'])<order.index(probe['over'])
        assert under.getpixel(point)[3]==255
        # The neck edge is intentionally antialiased. >240 verifies actual overlap,
        # while the underlying fully painted surface must be exactly opaque.
        assert over.getpixel(point)[3]>240


class SurfaceSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=build.load_source(ATTEMPT/'source/surfaces.py')
        cls.master=image(ATTEMPT/'camera-master.png')

    def test_01_archived_cli_exact_rebuild_all_outputs(self):
        with tempfile.TemporaryDirectory(prefix='cli-check-',dir=HERE) as tmp:
            command=[sys.executable,str(ATTEMPT/'source/build.py'),'--source',str(ATTEMPT/'source/surfaces.py'),'--output',tmp]
            run=subprocess.run(command,capture_output=True,text=True,check=False)
            self.assertEqual(run.returncode,0,run.stderr)
            for path in Path(tmp).rglob('*'):
                if path.is_file():
                    self.assertEqual(path.read_bytes(),(ATTEMPT/path.relative_to(tmp)).read_bytes(),str(path))

    def test_02_manifest_and_benchmark_pinned_hash(self):
        manifest=json.loads((ATTEMPT/'manifest.json').read_text())
        self.assertEqual(digest(build.REF),REFERENCE_SHA)
        self.assertEqual(manifest['reference_sha256'],REFERENCE_SHA)
        for name,sha in manifest['files'].items():
            self.assertEqual(digest(ATTEMPT/name),sha,name)

    def test_03_both_original_attempts_remain_immutable(self):
        for attempt,sha in PINNED.items():
            root=OLD/attempt
            self.assertEqual(digest(root/'manifest.json'),sha)
            manifest=json.loads((root/'manifest.json').read_text())
            for name,expected in manifest['files'].items():
                self.assertEqual(digest(root/name),expected,name)

    def test_04_real_alpha_zero_transparent_rgb_all_outputs(self):
        for path in list((ATTEMPT/'layers').glob('*.png'))+[ATTEMPT/f'camera-{n}.png' for n in ['master','native','half']]:
            im=image(path)
            self.assertEqual(im.mode,'RGBA',path.name)
            self.assertEqual(im.getchannel('A').getextrema()[0],0,path.name)
            self.assertGreater(im.getchannel('A').getextrema()[1],0,path.name)
            data=im.tobytes()
            self.assertTrue(all((r,g,b)==(0,0,0) for r,g,b,a in zip(data[0::4],data[1::4],data[2::4],data[3::4]) if a==0),path.name)
        self.assertEqual(self.master.getchannel('A').getextrema(),(0,255))
        self.assertGreater(sum(self.master.getchannel('A').histogram()[1:255]),0)

    def test_05_actual_hidden_underpaint(self):
        hidden_check(self.model,ATTEMPT)

    def test_06_missing_underpaint_detected(self):
        with tempfile.TemporaryDirectory(prefix='negative-',dir=HERE) as tmp:
            root=Path(tmp)
            (root/'layers').mkdir()
            for probe in self.model['hidden']:
                for name in [probe['under']+'--underpaint.png',probe['over']+'--complete.png']:
                    (root/'layers'/name).write_bytes((ATTEMPT/'layers'/name).read_bytes())
            under=image(root/'layers/pole--underpaint.png')
            under.putpixel((45,300),(0,0,0,0))
            under.save(root/'layers/pole--underpaint.png')
            with self.assertRaises(AssertionError):
                hidden_check(self.model,root)

    def test_07_remove_collar_reveals_painted_pole(self):
        with tempfile.TemporaryDirectory(prefix='reveal-',dir=HERE) as tmp:
            actual=build.render(self.model,Path(tmp),omit=['middle_ring'])
        self.assertEqual(actual.getpixel((45,300))[3],255)
        self.assertNotEqual(actual.getpixel((45,300)),self.master.getpixel((45,300)))
        self.assertEqual(actual.crop((0,0,180,270)).tobytes(),self.master.crop((0,0,180,270)).tobytes())

    def test_08_individually_editable_paint_changes_no_geometry(self):
        model=copy.deepcopy(self.model)
        hood=next(p for p in model['parts'] if p['name']=='hood')
        next(s for s in hood['surfaces'] if s['name']=='small_hot_glint')['color']='#cd9876'
        with tempfile.TemporaryDirectory(prefix='paint-edit-',dir=HERE) as tmp:
            actual=build.render(model,Path(tmp))
        self.assertEqual(actual.getchannel('A').tobytes(),self.master.getchannel('A').tobytes())
        self.assertNotEqual(actual.getpixel((105,108)),self.master.getpixel((105,108)))
        self.assertEqual(actual.crop((0,180,180,450)).tobytes(),self.master.crop((0,180,180,450)).tobytes())
        self.assertEqual(model['root'],self.model['root'])

    def test_09_source_render_never_reads_any_raster(self):
        with tempfile.TemporaryDirectory(prefix='raster-free-',dir=HERE) as tmp:
            with patch.object(build.Image,'open',side_effect=AssertionError('No input raster allowed')):
                actual=build.render(self.model,Path(tmp))
        self.assertEqual(actual.tobytes(),self.master.tobytes())

    def test_10_authored_anchor_exact_uniform_native_half(self):
        self.assertEqual(self.model['root'],[46,427])
        self.assertEqual(self.model['landmarks']['ground_root'],[46,427])
        self.assertAlmostEqual(self.model['scale'],96/418)
        self.assertEqual(self.master.getpixel((46,427))[3],255)
        for label,factor,size in [('native',1,(42,104)),('half',2,(21,52))]:
            scale=self.model['scale']/factor
            expected=self.master.transform(size,Image.Transform.AFFINE,(1/scale,0,0,0,1/scale,0),Image.Resampling.BICUBIC)
            expected.paste((0,0,0,0),(0,0),expected.getchannel('A').point(lambda a:255 if a==0 else 0))
            actual=image(ATTEMPT/f'camera-{label}.png')
            self.assertEqual(actual.size,size)
            self.assertEqual(actual.tobytes(),expected.tobytes())

    def test_11_individual_surface_census_no_raster_svg(self):
        import xml.etree.ElementTree as ET
        root=ET.parse(ATTEMPT/'camera-surfaces.svg').getroot()
        self.assertEqual(root.findall('.//{http://www.w3.org/2000/svg}image'),[])
        ids={element.get('id') for element in root.iter()}
        census=json.loads((ATTEMPT/'surface-census.json').read_text())
        self.assertEqual(len(census),sum(len(p['surfaces']) for p in self.model['parts']))
        self.assertEqual(len({s['id'] for s in census}),len(census))
        for surface in census:
            self.assertIn(surface['id'],ids)
            self.assertTrue((ATTEMPT/'layers'/f'{surface["id"]}.png').exists())

    def test_12_unretouched_comparison_and_exact_grayscale(self):
        original=image(build.REF).convert('RGB').crop((890,20,1070,470))
        self.assertEqual(original.tobytes(),image(ATTEMPT/'reference-window.png').tobytes())
        self.assertEqual(ImageOps.grayscale(image(ATTEMPT/'comparison-color.png')).tobytes(),image(ATTEMPT/'comparison-grayscale.png').tobytes())

if __name__=='__main__':
    unittest.main(verbosity=2)
