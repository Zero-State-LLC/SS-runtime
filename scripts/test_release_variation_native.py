#!/usr/bin/env python3
"""Importer guard regressions. Parser fixtures are synthetic, never native evidence."""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from PIL import Image
import import_release_variation_native as native

PACKET=native.ROOT/'docs/review/player-release-variation-native-20261116'

class ImportGuards(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(PACKET)))
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.rows=[{'family':f,'phase':p,'pose':k,'tickOffset':(k*180+127)//128,'source':native.source.name(f,p,k),
                    'sourceSHA256':'0'*64,'capture':f'releasevariation-{f}-{p:02d}-pose-{k:02d}'} for f,p,k in native.ORDER]
        self.items=[{'suggestedHumanReadableName':r['capture'],'exportedFileName':native.filename(r['family'],r['phase'],r['pose'])} for r in self.rows]
        self.items.append({'suggestedHumanReadableName':'releasevariation-pose-records','exportedFileName':'records.json'})
        self.summary={'passedTests':3,'totalTestCount':3,'failedTests':0,'skippedTests':0,'expectedFailures':0,'result':'Passed'}
        self.tree={'testNodes':[{'children':[{'nodeType':'Test Case','nodeIdentifier':t,'result':'Passed'} for t in sorted(native.TESTS)]}]}

    def save(self):
        (self.root/'manifest.json').write_text(json.dumps([{'attachments':self.items}]))
        (self.root/'records.json').write_text(json.dumps(self.rows))

    def test_complete_parser_census(self):
        self.save();images,_,rows=native.attachments(self.root)
        self.assertEqual(len(images),476);self.assertEqual(rows,self.rows)

    def test_exact_result_identities(self):
        self.assertEqual(len(native.validate_result(self.summary,self.tree)),3)

    def test_zero_test_exit_zero_rejected(self):
        self.summary.update(passedTests=0,totalTestCount=0)
        with self.assertRaisesRegex(ValueError,'actual passing'):native.validate_result(self.summary,self.tree)

    def test_failure_skip_expected_failure_rejected(self):
        for field in ('failedTests','skippedTests','expectedFailures'):
            bad=dict(self.summary);bad[field]=1
            with self.assertRaises(ValueError):native.validate_result(bad,self.tree)

    def test_other_test_names_rejected(self):
        self.tree['testNodes'][0]['children'][0]['nodeIdentifier']='Unrelated/test()'
        with self.assertRaisesRegex(ValueError,'identities'):native.validate_result(self.summary,self.tree)

    def test_failed_case_despite_green_summary_rejected(self):
        self.tree['testNodes'][0]['children'][0]['result']='Failed'
        with self.assertRaisesRegex(ValueError,'identities'):native.validate_result(self.summary,self.tree)

    def test_missing_image_rejected(self):
        self.items.pop(0);self.save()
        with self.assertRaisesRegex(ValueError,'476'):native.attachments(self.root)

    def test_duplicate_image_rejected(self):
        self.items.append(self.items[0]);self.save()
        with self.assertRaisesRegex(ValueError,'Duplicate'):native.attachments(self.root)

    def test_missing_record_rejected(self):
        self.items.pop();self.save()
        with self.assertRaisesRegex(ValueError,'476'):native.attachments(self.root)

    def test_path_escape_rejected(self):
        self.items[0]['exportedFileName']='../escape.png';self.save()
        with self.assertRaisesRegex(ValueError,'escape'):native.attachments(self.root)

    def test_records_must_preserve_phase_family_pose_order(self):
        self.rows[0],self.rows[1]=self.rows[1],self.rows[0]
        with self.assertRaisesRegex(ValueError,'ordered'):native.validate_records(self.rows)

    def test_wrong_family_rejected(self):
        self.rows[0]['family']='proposed'
        with self.assertRaisesRegex(ValueError,'ordered'):native.validate_records(self.rows)

    def test_wrong_tick_rejected(self):
        self.rows[16]['tickOffset']=22
        with self.assertRaisesRegex(ValueError,'tick'):native.validate_records(self.rows)

    def test_wrong_texture_rejected(self):
        self.rows[1]['source']='player-releasevariation-01-01'
        with self.assertRaisesRegex(ValueError,'source identity'):native.validate_records(self.rows)

    def test_wrong_capture_name_rejected(self):
        self.rows[1]['capture']='other-image'
        with self.assertRaisesRegex(ValueError,'capture name'):native.validate_records(self.rows)

    def test_invalid_actual_sha_rejected(self):
        self.rows[1]['sourceSHA256']='unverified'
        with self.assertRaisesRegex(ValueError,'SHA'):native.validate_records(self.rows)

    def test_png_preservation_test_only(self):
        text=(native.ROOT/'project.yml').read_text();production,tests=text.split('  SSRuntimeTests:',1)
        for flag in ('COMPRESS_PNG_FILES: NO','STRIP_PNG_TEXT: NO'):
            self.assertIn(flag,tests);self.assertNotIn(flag,production)
        self.assertIn('- path: AppTests',tests)


class ActualCaptureGuards(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR',str(PACKET)))
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'capture'
        # Requires the actual completed capture, never skips or creates substitutes.
        shutil.copytree(PACKET/'capture',self.root)

    def change(self,name,mutate):
        path=self.root/name;obj=native.load(path);mutate(obj);path.write_text(json.dumps(obj))

    def test_actual476_captures_and28_endpoints(self):
        report=native.verify_capture(self.root)
        self.assertEqual(report['verifiedPoses'],476)
        self.assertEqual(report['nativeEndpointEqualities'],28)
        self.assertEqual(report['passedActualTests'],3)
        self.assertFalse(report['liveCadenceVerified'])

    def test_capture_hash_tamper_rejected(self):
        path=self.root/'variation-phase-01-pose-03.png';path.write_bytes(path.read_bytes()+b'tamper')
        with self.assertRaisesRegex(ValueError,'attachment hash'):native.verify_capture(self.root)

    def test_extra_capture_rejected(self):
        shutil.copy2(self.root/'variation-phase-01-pose-03.png',self.root/'extra.png')
        with self.assertRaisesRegex(ValueError,'PNG census'):native.verify_capture(self.root)

    def test_missing_attachment_hash_rejected(self):
        self.change('verification.json',lambda m:m['attachmentHashes'].pop('tests.json'))
        with self.assertRaisesRegex(ValueError,'hash census'):native.verify_capture(self.root)

    def test_actual_bundle_digest_rejected_even_with_updated_record_hash(self):
        self.change('pose-records.json',lambda rows:rows[1].__setitem__('sourceSHA256','1'*64))
        self.change('verification.json',lambda m:m['attachmentHashes'].__setitem__('pose-records.json',native.sha(self.root/'pose-records.json')))
        with self.assertRaisesRegex(ValueError,'bundled PNG bytes'):native.verify_capture(self.root)

    def test_source_configuration_drift_rejected(self):
        self.change('verification.json',lambda m:m['sourceHashes'].__setitem__('project.yml','0'*64))
        with self.assertRaisesRegex(ValueError,'source/configuration'):native.verify_capture(self.root)

    def test_lifted_live_claim_rejected(self):
        self.change('verification.json',lambda m:m.__setitem__('liveCadenceVerified',True))
        with self.assertRaisesRegex(ValueError,'scope lifted'):native.verify_capture(self.root)

    def test_lifted_art_claim_rejected(self):
        self.change('verification.json',lambda m:m.__setitem__('artAdmission',True))
        with self.assertRaisesRegex(ValueError,'scope lifted'):native.verify_capture(self.root)

    def test_native_endpoint_pixels_rejected_even_with_updated_file_hash(self):
        path=self.root/'variation-phase-01-pose-16.png'
        with Image.open(path) as im:
            image=im.convert('RGBA');image.putpixel((0,0),(255,0,0,255));image.save(path)
        self.change('verification.json',lambda m:m['attachmentHashes'].__setitem__(path.name,native.sha(path)))
        with self.assertRaisesRegex(ValueError,'endpoint RGBA'):native.verify_capture(self.root)

    def test_native_dimensions_rejected_even_with_updated_file_hash(self):
        path=self.root/'variation-phase-01-pose-03.png'
        with Image.open(path) as im:im.resize((192,144)).save(path)
        self.change('verification.json',lambda m:m['attachmentHashes'].__setitem__(path.name,native.sha(path)))
        with self.assertRaisesRegex(ValueError,'PNG576x432'):native.verify_capture(self.root)

    def test_timing_declaration_tamper_rejected(self):
        self.change('verification.json',lambda m:m.__setitem__('authoredNeutralBoundarySeconds',0.4))
        with self.assertRaisesRegex(ValueError,'timing declaration'):native.verify_capture(self.root)

    def test_changed_native_facts_rejected(self):
        self.change('verification.json',lambda m:m['imageFacts'].__setitem__('pairedEndpointRGBAEqualities',27))
        with self.assertRaisesRegex(ValueError,'image facts'):native.verify_capture(self.root)

if __name__=='__main__':unittest.main(verbosity=2)
