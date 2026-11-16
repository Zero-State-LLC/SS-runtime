#!/usr/bin/env python3
"""Self-contained final-source tests. Historical external audit remains test_source.py."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageOps

HERE=Path(__file__).resolve().parent
ATTEMPT=Path(os.environ.get('CAMERA_FINAL_ROOT',str(HERE/'attempt-02')))
spec=importlib.util.spec_from_file_location('surface_build',ATTEMPT/'source/build.py')
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
INPUT_SHA={'reference.png':'49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb',
           'first-surface-master.png':'82009e85c221f060f24c98e905d7e7447ec5729cf85bad2fb64fd86dc13e7b93',
           'prior-procedural-master.png':'96e8ec13a8527d1df7c806a0202abba8e523ceb210b8d634304dc42f7a66af50'}
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
    def assert_manifest_replay(self, actual, retained):
        # The recorded author environment remains immutable. A fresh replay must
        # truthfully report its own interpreter, not impersonate the author's.
        self.assertEqual(actual.get('python'), sys.version.split()[0])
        expected=copy.deepcopy(retained)
        expected['python']=sys.version.split()[0]
        self.assertEqual(actual,expected)

    def assert_export_replay(self, actual, retained):
        if actual.name=='manifest.json':
            self.assert_manifest_replay(json.loads(actual.read_text()),json.loads(retained.read_text()))
        else:
            self.assertEqual(actual.read_bytes(),retained.read_bytes(),str(actual))

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
                    self.assert_export_replay(path,ATTEMPT/path.relative_to(tmp))

    def test_02_manifest_and_benchmark_pinned_hash(self):
        self.assertEqual(digest(ATTEMPT/'manifest.json'),'12fa45195617a7423d7402c80e57c6490c17ce14822757f49d879464ed6c7826')
        manifest=json.loads((ATTEMPT/'manifest.json').read_text())
        self.assertEqual(digest(build.REF),REFERENCE_SHA)
        self.assertEqual(manifest['reference_sha256'],REFERENCE_SHA)
        for name,sha in manifest['files'].items():
            self.assertEqual(digest(ATTEMPT/name),sha,name)

    def test_03_bundled_comparison_inputs_are_pinned(self):
        for name,expected in INPUT_SHA.items():
            self.assertEqual(digest(ATTEMPT/'source/inputs'/name),expected,name)

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

    def test_13_surface_only_no_contour_anchor_or_alpha_changes(self):
        geometry=ATTEMPT/'source/geometry.json'
        self.assertEqual(digest(geometry),'2746d816dbd94d8a8ce435d019b253ef30629d112e489d14d3b2df90b8d00326')
        original=json.loads(geometry.read_text())
        for key in ['canvas','root','scale','landmarks','hidden']:
            self.assertEqual(original[key],self.model[key],key)
        self.assertEqual([(p['name'],p['contour']) for p in original['parts']],
                         [(p['name'],p['contour']) for p in self.model['parts']])
        first=image(ATTEMPT/'source/inputs/first-surface-master.png')
        self.assertEqual(first.getchannel('A').tobytes(),self.master.getchannel('A').tobytes())
        self.assertNotEqual(first.tobytes(),self.master.tobytes())

    def test_14_detached_source_replay_forbids_external_packet_reads(self):
        with tempfile.TemporaryDirectory(prefix='detached-',dir=HERE) as tmp:
            root=Path(tmp)
            detached=root/'source'
            shutil.copytree(ATTEMPT/'source',detached)
            out=root/'rebuilt'
            # Read audit proves this replay cannot fall back to original packet files.
            audit='''import os,sys,runpy
blocked=os.path.realpath(sys.argv[1])
allowed=os.path.realpath(sys.argv[2])
script=os.path.realpath(sys.argv[3])
output=sys.argv[4]
def guard(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)):
        path=os.path.realpath(os.fsdecode(args[0]))
        if path.startswith(blocked+os.sep) and not path.startswith(allowed+os.sep):
            raise RuntimeError('External packet read forbidden: '+path)
sys.addaudithook(guard)
sys.argv=[script,'--source',os.path.join(os.path.dirname(script),'surfaces.py'),'--output',output]
runpy.run_path(script,run_name='__main__')
'''
            run=subprocess.run([sys.executable,'-c',audit,str(HERE),str(root),str(detached/'build.py'),str(out)],
                               cwd=detached,capture_output=True,text=True,check=False)
            self.assertEqual(run.returncode,0,run.stderr)
            for name in ['camera-master.png','camera-native.png','camera-half.png','comparison-color.png','manifest.json']:
                self.assert_export_replay(out/name,ATTEMPT/name)

    def test_15_manifest_runtime_version_must_be_truthful(self):
        retained=json.loads((ATTEMPT/'manifest.json').read_text())
        actual=copy.deepcopy(retained)
        actual['python']=sys.version.split()[0]
        self.assert_manifest_replay(actual,retained)
        for value in ('wrong-interpreter',None):
            with self.subTest(value=value),self.assertRaises(AssertionError):
                self.assert_manifest_replay(dict(actual,python=value),retained)

    def test_16_only_interpreter_metadata_may_differ(self):
        retained=json.loads((ATTEMPT/'manifest.json').read_text())
        actual=copy.deepcopy(retained)
        actual['python']=sys.version.split()[0]
        for key in ('pillow','reference_sha256','files'):
            changed=copy.deepcopy(actual)
            if key=='files':
                changed[key][next(iter(changed[key]))]='0'*64
            else:
                changed[key]='changed'
            with self.subTest(key=key),self.assertRaises(AssertionError):
                self.assert_manifest_replay(changed,retained)
        with self.assertRaises(AssertionError):
            self.assert_manifest_replay(dict(actual,unexpected='claim'),retained)

if __name__=='__main__':
    unittest.main(verbosity=2)
