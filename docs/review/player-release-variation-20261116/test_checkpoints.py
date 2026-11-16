#!/usr/bin/env python3
"""Regression-check actual rendered checkpoint reuse with read-only original masters."""
import argparse
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from PIL import Image
import variation as v

SOURCE=None

class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(v.HERE)))
        self.addCleanup(self.temp.cleanup)
        self.dst=Path(self.temp.name)/'phase-01'
        shutil.copytree(v.HERE/'artifacts/.work/phase-01',self.dst)
        self.samples=v.expected(v.BASE/'fixtures')[2][1]

    def check(self):return v.b.completed_work(SOURCE,self.dst,self.samples)

    def test_actual_checkpoint_valid(self):
        self.assertTrue(self.check())
        self.assertEqual(len(v.b.endpoint_checks(self.dst/'frames',SOURCE/v.b.NAMES[0]/'frames/00.png',SOURCE/v.b.NAMES[1]/'frames/00.png',1)),2)

    def test_changed_sample_rejected(self):
        path=self.dst/'source/samples.json';sample=v.load(path);sample[3]['legs'][0]['toe'][0]+=.1;v.b.save(path,sample)
        with self.assertRaisesRegex(ValueError,'Checkpoint source'):self.check()

    def test_changed_recipe_rejected(self):
        path=self.dst/'assemble.py';path.write_text(path.read_text()+'\n# mutation\n')
        with self.assertRaisesRegex(ValueError,'Checkpoint assembly'):self.check()

    def test_changed_boot_material_rejected(self):
        path=self.dst/'boot/material.py';path.write_text(path.read_text()+'\n# mutation\n')
        with self.assertRaisesRegex(ValueError,'Checkpoint recipe'):self.check()

    def test_changed_rendered_pixels_rejected(self):
        path=self.dst/'frames/03.png'
        with Image.open(path) as im:
            image=im.convert('RGBA');image.putpixel((0,0),(255,0,0,255));image.save(path)
        with self.assertRaisesRegex(ValueError,'rendered pixels'):self.check()

    def test_changed_frame_order_rejected(self):
        path=self.dst/'assembly-record.json';record=v.load(path);record['frames'].reverse();v.b.save(path,record)
        with self.assertRaisesRegex(ValueError,'assembly order'):self.check()

    def test_incomplete_checkpoint_rejected(self):
        (self.dst/'assembly-record.json').unlink()
        self.assertFalse(self.check())

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',required=True,type=Path)
    args,extra=parser.parse_known_args();SOURCE=args.source_root.resolve()
    unittest.main(argv=[__file__,*extra],verbosity=2)
