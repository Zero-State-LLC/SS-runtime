#!/usr/bin/env python3
"""Run all archived control checks with the strict supported metadata comparator.

The archived test and renderer remain byte-exact and hash-bound. Only its
interpreter-equality test is explicitly overridden, without skips or patching.
"""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from manifest_compare import compare_manifest,AUTHOR_CONTROL_SHA256
HERE=Path(__file__).resolve().parent
CONTROL=HERE/'control'
sys.path.insert(0,str(CONTROL))
spec=importlib.util.spec_from_file_location('archived_control_tests',CONTROL/'test_assembly.py')
archived=importlib.util.module_from_spec(spec)
spec.loader.exec_module(archived)

class SupportedControlTests(archived.PaintedAssemblyTests):
    def test_09_standalone_replay_identical(self):
        root=self.temporary()/'standalone'
        root.mkdir()
        for name in ('replay.py','assembly.json'):
            shutil.copy2(CONTROL/name,root/name)
        shutil.copytree(CONTROL/'inputs',root/'inputs')
        subprocess.run([sys.executable,'-W','error',str(root/'replay.py')],cwd=root,check=True,capture_output=True)
        retained=archived.verify()
        archived.verify(root)
        compare_manifest(CONTROL/'preview-01/manifest.json',root/'preview-01/manifest.json',AUTHOR_CONTROL_SHA256)
        for name in retained['exports']:
            self.assertEqual((root/'preview-01'/name).read_bytes(),(CONTROL/'preview-01'/name).read_bytes(),name)

if __name__=='__main__':
    unittest.main(verbosity=2)
