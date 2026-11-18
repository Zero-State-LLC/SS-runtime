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
from PIL import Image
import replay as p
from author import padded_model
from manifest_compare import compare_manifest,AUTHOR_FINAL_SHA256,AUTHOR_CONTROL_SHA256
HERE=Path(__file__).resolve().parent

class PaddingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=json.loads((HERE/'assembly.json').read_text())
        cls.old=json.loads((HERE/'control/assembly.json').read_text())
        cls.master,cls.layers,cls.crops,_=p.r.render(cls.model,HERE/'inputs')

    def temporary(self):
        temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(HERE)))
        self.addCleanup(temp.cleanup)
        return Path(temp.name)

    def test_01_exact_authorized_changes_only(self):
        self.assertEqual(self.model,padded_model())
        self.assertEqual(self.model['canvas'],[204,450])
        self.assertEqual(self.model['root'],[58,427])
        self.assertEqual(self.model['logicalScale'],self.old['logicalScale'])
        for old,new in zip(self.old['layers'],self.model['layers']):
            expected=copy.deepcopy(old)
            expected['position'][0]+=12
            self.assertEqual(new,expected)

    def test_02_archived_margin_failure_remains(self):
        with Image.open(HERE/'control/preview-01/camera-master.png') as im:
            self.assertEqual(p.border_alpha(im),215)
        old=json.loads((HERE/'control/source-audit.json').read_text())
        self.assertFalse(old['assemblyBoundary']['complete-pole']['antialiasPaddingSatisfied'])
        self.assertEqual(old['assemblyBoundary']['complete-pole']['canvasBorderMaxAlpha'],215)

    def test_03_actual_final_border_passes_all_sizes_and_layers(self):
        for image in [self.master,*self.layers.values(),p.r.scaled(self.master,self.model['logicalScale']),p.r.scaled(self.master,self.model['logicalScale']/2)]:
            self.assertEqual(p.border_alpha(image),0)
        for name in ('camera-master.png','camera-native.png','camera-half.png'):
            with Image.open(HERE/'final'/name) as im:
                self.assertEqual(p.border_alpha(im),0)

    def test_04_unclipped_pixels_identical_and_fringe_restored(self):
        evidence=p.invariants(self.model,self.master,self.layers)
        self.assertEqual(evidence['restoredLeftFringePixels'],35)
        self.assertEqual(evidence['restoredLeftFringeAlphaSum'],57)
        self.assertEqual(evidence['changedPriorColumns'],[0,1,2])
        self.assertEqual(evidence['preservedUnclippedPixels'],79650)
        self.assertEqual(evidence,json.loads((HERE/'final/padding-evidence.json').read_text()))

    def test_05_pasting_old_clipped_image_is_rejected(self):
        fake=Image.new('RGBA',(204,450))
        with Image.open(HERE/'control/preview-01/camera-master.png') as old:
            fake.paste(old,(12,0))
        with self.assertRaisesRegex(ValueError,'No clipped fringe restored'):
            p.invariants(self.model,fake,self.layers)

    def test_06_source_pixels_crops_and_raw_files_unchanged(self):
        for source in (HERE/'inputs').iterdir():
            self.assertEqual(source.read_bytes(),(HERE/'control/inputs'/source.name).read_bytes())
        for name,crop in self.crops.items():
            with Image.open(HERE/'control/preview-01/source-layers'/f'{name}.png') as old:
                self.assertEqual(crop.tobytes(),old.tobytes())
            self.assertEqual((HERE/'final/source-layers'/f'{name}.png').read_bytes(),(HERE/'control/preview-01/source-layers'/f'{name}.png').read_bytes())

    def test_07_root_relative_mapping_identical(self):
        s=self.model['logicalScale']
        for old,new in zip(self.old['layers'],self.model['layers']):
            for u,v in [(0,0),(100,100),(250,400)]:
                a=[old['position'][0]+u*old['uniformScale']-self.old['root'][0],self.old['root'][1]-old['position'][1]-v*old['uniformScale']]
                b=[new['position'][0]+u*new['uniformScale']-self.model['root'][0],self.model['root'][1]-new['position'][1]-v*new['uniformScale']]
                for x,y in zip(a,b):
                    self.assertAlmostEqual(x*s,y*s,places=12)

    def test_08_registration_matches_source_and_uniform_scale(self):
        reg=json.loads((HERE/'final/registration.json').read_text())
        s=self.model['logicalScale']
        self.assertEqual(reg['sourceSHA256'],p.r.sha(HERE/'final/camera-master.png'))
        self.assertEqual(reg['rootPixelsTopLeft'],[58,427])
        self.assertEqual(reg['canvasPixels'],[204,450])
        self.assertEqual(reg['drawSizeWorld'],[204*s,450*s])
        self.assertEqual(reg['spriteAnchorBottomLeft'],[58/204,1-427/450])
        self.assertEqual(reg['nativeRasterSize'],[47,104])
        self.assertEqual(reg['halfRasterSize'],[24,52])
        self.assertFalse(reg['ownerAccepted'])
        self.assertFalse(reg['productionAdmitted'])

    def test_09_archive_original_twelve_checks_still_pass(self):
        proc=subprocess.run([sys.executable,'-W','error',str(HERE/'test_control_supported.py')],check=True,capture_output=True,text=True)
        self.assertIn('Ran 12 tests',proc.stderr)
        self.assertIn('OK',proc.stderr)

    def test_10_standalone_all_outputs_and_manifest_identical(self):
        root=self.temporary()/'packet'
        shutil.copytree(HERE,root,ignore=shutil.ignore_patterns('__pycache__','tmp*','*.log','final'))
        subprocess.run([sys.executable,'-W','error',str(root/'replay.py')],check=True,capture_output=True,cwd=root)
        expected=json.loads((HERE/'final/manifest.json').read_text())
        compare_manifest(HERE/'final/manifest.json',root/'final/manifest.json',AUTHOR_FINAL_SHA256)
        for name in expected['exports']:
            self.assertEqual((root/'final'/name).read_bytes(),(HERE/'final'/name).read_bytes(),name)

    def test_11_any_new_geometry_or_scale_change_rejected(self):
        for mutate in [lambda m:m['root'].__setitem__(0,57),lambda m:m.update(logicalScale=.23),lambda m:m['layers'][1].update(uniformScale=.28)]:
            model=copy.deepcopy(self.model)
            mutate(model)
            with self.assertRaisesRegex(ValueError,'authorized symmetric padding'):
                p.invariants(model,self.master,self.layers)

    def test_12_final_manifest_hashes_current_inputs_and_exports(self):
        manifest=json.loads((HERE/'final/manifest.json').read_text())
        self.assertTrue(manifest['technicalPaddingOnly'])
        for name,digest in manifest['sources'].items():
            self.assertEqual(p.r.sha(HERE/name),digest,name)
        for name,digest in manifest['exports'].items():
            self.assertEqual(p.r.sha(HERE/'final'/name),digest,name)

    def test_13_manifest_comparator_accepts_only_actual_interpreter(self):
        for relative,pin in [('final/manifest.json',AUTHOR_FINAL_SHA256),('control/preview-01/manifest.json',AUTHOR_CONTROL_SHA256)]:
            author=HERE/relative
            expected=json.loads(author.read_text())
            expected['python']=sys.version.split()[0]
            target=self.temporary()/'manifest.json'
            target.write_text(json.dumps(expected))
            compare_manifest(author,target,pin)
            expected['python']='false-interpreter'
            target.write_text(json.dumps(expected))
            with self.assertRaisesRegex(AssertionError,'actual sys.version'):
                compare_manifest(author,target,pin)

    def test_14_manifest_comparator_rejects_all_noninterpreter_changes(self):
        for relative,pin in [('final/manifest.json',AUTHOR_FINAL_SHA256),('control/preview-01/manifest.json',AUTHOR_CONTROL_SHA256)]:
            author=HERE/relative
            original=json.loads(author.read_text())
            original['python']=sys.version.split()[0]
            for key,value in [('pillow','false-pillow'),('status','ACCEPTED'),('exports',{}),('ownerAccepted',True),('unexpectedField',1)]:
                mutated=copy.deepcopy(original)
                mutated[key]=value
                target=self.temporary()/'manifest.json'
                target.write_text(json.dumps(mutated))
                with self.assertRaisesRegex(AssertionError,'Non-interpreter'):
                    compare_manifest(author,target,pin)
            mutated=copy.deepcopy(original)
            mutated.pop('pillow')
            target=self.temporary()/'manifest.json'
            target.write_text(json.dumps(mutated))
            with self.assertRaisesRegex(AssertionError,'Non-interpreter'):
                compare_manifest(author,target,pin)

    def test_15_retained_author_manifest_bytes_are_separately_pinned(self):
        for relative,pin in [('final/manifest.json',AUTHOR_FINAL_SHA256),('control/preview-01/manifest.json',AUTHOR_CONTROL_SHA256)]:
            author=HERE/relative
            self.assertEqual(p.r.sha(author),pin)
            changed=self.temporary()/'author.json'
            changed.write_bytes(author.read_bytes()+b' ')
            with self.assertRaisesRegex(AssertionError,'author manifest pin'):
                compare_manifest(changed,author,pin)

if __name__=='__main__':
    unittest.main(verbosity=2)
