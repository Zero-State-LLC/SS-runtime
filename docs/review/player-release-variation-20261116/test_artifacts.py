#!/usr/bin/env python3
"""Tamper actual delivered variation artifacts in isolated copies, fail rather than skip."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import variation as v
import verify_packet

class VariationArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(v.HERE)))
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'artifacts'
        shutil.copytree(v.HERE/'artifacts',self.root,ignore=shutil.ignore_patterns('.work','*.mp4','*.html','contact-plate.png','contact-overview.png'))

    def change(self,path,mutate):
        obj=v.load(self.root/path);mutate(obj);v.b.save(self.root/path,obj)

    def verify(self):return verify_packet.verify(self.root)

    def test_all272_frames32_endpoints_and34_preserved(self):
        result=self.verify()
        self.assertEqual(result['orderedFrames'],272)
        self.assertEqual(result['endpointProvenanceChecks'],32)
        self.assertEqual(result['preservedFrameHashes'],34)
        self.assertEqual(result['archivedInputHashRecords'],1012)
        self.assertEqual(result['geometryRows'],544)
        self.assertFalse(result['variationNativeVerified'])

    def test_missing_frame_rejected(self):
        (self.root/'phase-01/frames/03.png').unlink()
        with self.assertRaisesRegex(ValueError,'PNG set'):self.verify()

    def test_extra_frame_rejected(self):
        shutil.copy2(self.root/'phase-01/frames/03.png',self.root/'phase-01/frames/17.png')
        with self.assertRaisesRegex(ValueError,'PNG set'):self.verify()

    def test_phase_order_rejected(self):
        self.change('manifest.json',lambda m:m['phases'].reverse())
        with self.assertRaisesRegex(ValueError,'Phase order'):self.verify()

    def test_pose_order_rejected(self):
        self.change('manifest.json',lambda m:m['phases'][0]['frames'].reverse())
        with self.assertRaisesRegex(ValueError,'Frame order'):self.verify()

    def test_timing_rejected(self):
        self.change('manifest.json',lambda m:m['timing']['frameUnits'].__setitem__(0,4))
        with self.assertRaisesRegex(ValueError,'timing'):self.verify()

    def test_frame_bytes_rejected(self):
        path=self.root/'phase-01/frames/03.png';path.write_bytes(path.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'byte hash'):self.verify()

    def test_updated_file_hash_still_checks_rgba(self):
        path=self.root/'phase-01/frames/03.png'
        with Image.open(path) as im:
            image=im.convert('RGBA');image.putpixel((0,0),(255,0,0,255));image.save(path)
        self.change('manifest.json',lambda m:m['phases'][0]['frames'][3].__setitem__('fileSHA256',v.b.sha(path)))
        with self.assertRaisesRegex(ValueError,'RGBA hash'):self.verify()

    def test_endpoint_origin_rejected(self):
        self.change('input-inventory.json',lambda m:m.__setitem__('SS-player-bounded-proportions/frames/00.png','0'*64))
        with self.assertRaisesRegex(ValueError,'Endpoint original'):self.verify()

    def test_preserved_original_hash_rejected(self):
        self.change('input-inventory.json',lambda m:m.__setitem__('SS-player-settle-prototype/phase-05/frames/03.png','0'*64))
        with self.assertRaisesRegex(ValueError,'Preserved frame'):self.verify()

    def test_profile_tamper_rejected(self):
        self.change('profiles.json',lambda m:m[0].__setitem__('lift',3.24))
        with self.assertRaisesRegex(ValueError,'Profile provenance'):self.verify()

    def test_geometry_fact_tamper_rejected(self):
        self.change('geometry-contact-checks.json',lambda m:m[0]['measurements'][3].__setitem__('reach',20))
        with self.assertRaisesRegex(ValueError,'Geometry facts'):self.verify()

    def test_trajectory_tamper_even_updated_sample_hash(self):
        path='phase-01/samples.json'
        self.change(path,lambda m:m[3]['legs'][0]['knee'].__setitem__(0,99))
        self.change('manifest.json',lambda m:m['phases'][0].__setitem__('samplesSHA256',v.b.sha(self.root/path)))
        with self.assertRaisesRegex(ValueError,'trajectory changed'):self.verify()

    def test_baseline_dependency_tamper_rejected(self):
        self.change('dependencies.json',lambda m:m.__setitem__('build_source.py','0'*64))
        with self.assertRaisesRegex(ValueError,'Baseline provenance'):self.verify()

    def test_implementation_tamper_rejected(self):
        self.change('implementation.json',lambda m:m.__setitem__('variation.py','0'*64))
        with self.assertRaisesRegex(ValueError,'Implementation provenance'):self.verify()

    def test_complete_inventory_drift_rejected(self):
        self.change('input-inventory.json',lambda m:m.__setitem__('SS-player-bounded-proportions/README.md','0'*64))
        with self.assertRaisesRegex(ValueError,'Complete1012-file'):self.verify()

    def test_native_claim_lift_rejected(self):
        self.change('manifest.json',lambda m:m.__setitem__('nativeVariationVerified',True))
        with self.assertRaisesRegex(ValueError,'native acceptance'):self.verify()

    def test_owner_provenance_rejected(self):
        self.change('manifest.json',lambda m:m.__setitem__('ownerDirectionUTC','2026-11-17T00:00:00Z'))
        with self.assertRaisesRegex(ValueError,'Owner direction'):self.verify()

    def test_baseline_sample_hash_tamper_rejected(self):
        baseline=Path(self.temp.name)/'baseline'
        shutil.copytree(v.BASE,baseline,ignore=shutil.ignore_patterns('.work','__pycache__','*.mp4','*.html','contact-plate.png'))
        path=baseline/'artifacts/phase-01/samples.json'
        samples=v.load(path);samples[3]['legs'][0]['knee'][0]+=.1;v.b.save(path,samples)
        with patch.object(v,'BASE',baseline):
            with self.assertRaisesRegex(ValueError,'sample hash changed'):self.verify()

    def test_variation_identity_rejected(self):
        self.change('manifest.json',lambda m:m.__setitem__('variation','unrelated proposal'))
        with self.assertRaisesRegex(ValueError,'Variation identity'):self.verify()

    def test_baseline_pixels_substituted_for_variation_rejected(self):
        original=v.load(v.BASE/'artifacts/manifest.json')['phases'][0]
        for frame in original['frames']:
            shutil.copy2(v.BASE/'artifacts'/frame['path'],self.root/frame['path'])
        self.change('manifest.json',lambda m:m['phases'][0].__setitem__('frames',original['frames']))
        with self.assertRaisesRegex(ValueError,'pixels absent'):self.verify()

    def test_lifted_acceptance_rejected(self):
        self.change('manifest.json',lambda m:m.__setitem__('status','APPROVED'))
        with self.assertRaisesRegex(ValueError,'status'):self.verify()

if __name__=='__main__':unittest.main(verbosity=2)
