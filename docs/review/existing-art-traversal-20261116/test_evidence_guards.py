#!/usr/bin/env python3
"""Synthetic guard regressions only until native capture is imported.
No motion model, simulated gameplay trace or claimed native evidence is generated here.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from PIL import Image
import verify_capture as v

class EvidenceGuardTests(unittest.TestCase):
    def setUp(self): self.temp=Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR')))
    def tearDown(self): shutil.rmtree(self.temp)
    def test_exact_nonzero_result_and_identity(self):
        summary={'result':'Passed','totalTestCount':1,'passedTests':1,'failedTests':0,'skippedTests':0,'expectedFailures':0}
        tree={'testNodes':[{'nodeType':'Test Case','nodeIdentifier':v.TEST,'result':'Passed'}]}
        v.validate_result(summary,tree)
        for key,value in [('totalTestCount',0),('failedTests',1),('skippedTests',1),('passedTests',0),('expectedFailures',1)]:
            with self.subTest(key=key),self.assertRaises(ValueError): v.validate_result(dict(summary,**{key:value}),tree)
        changed=copy.deepcopy(tree); changed['testNodes'][0]['nodeIdentifier']='Other/test()'
        with self.assertRaisesRegex(ValueError,'identity'): v.validate_result(summary,changed)
    def test_export_path_missing_duplicate_and_escape(self):
        path=self.temp/'record.json'; path.write_text('{}')
        item={'suggestedHumanReadableName':'eat-records_uuid','exportedFileName':'record.json','isAssociatedWithFailure':False}
        manifest=[{'testIdentifier':v.TEST,'attachments':[item]}]
        (self.temp/'manifest.json').write_text(json.dumps(manifest))
        self.assertEqual(v.attachments(self.temp),{'eat-records':path})
        for items in ([item,item],[dict(item,exportedFileName='missing')],[dict(item,exportedFileName='../escape')]):
            (self.temp/'manifest.json').write_text(json.dumps([{'testIdentifier':v.TEST,'attachments':items}]))
            with self.assertRaises(ValueError): v.attachments(self.temp)
    def test_bound_resource_hash_bytes_and_escape(self):
        path=self.temp/'source.png'; path.write_bytes(b'synthetic resource, not native evidence')
        resource={'assetId':'test','path':path.name,'sha256':v.sha(path),'bytes':path.stat().st_size}
        packet={'resourceInventory':[resource]}
        self.assertEqual(v.validate_resources(packet,self.temp),{'source.png':v.sha(path)})
        for key,value in [('sha256','0'*64),('bytes',0),('path','../outside')]:
            changed=copy.deepcopy(packet); changed['resourceInventory'][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): v.validate_resources(changed,self.temp)
    def test_q8_root_and_delta_reconstruction(self):
        # Static arithmetic fixture only. No movement or collision implementation copied.
        row={'rawX':101,'rawY':205,'deltaRawX':1,'deltaRawY':5,'snapshotX':0,'snapshotY':0,'renderedX':0,'renderedY':0}
        self.assertEqual(v.validate_root(row,(100,200)),(101,205))
        for key,value in [('deltaRawX',2),('deltaRawY',0),('renderedX',1),('renderedY',1),('snapshotX',1),('snapshotY',1),('rawX',101.0)]:
            with self.subTest(key=key),self.assertRaises(ValueError): v.validate_root(dict(row,**{key:value}),(100,200))
    def test_negative_fractional_and_one_unit_mapping_guards(self):
        for raw, expected in [(-257,-1),(-255,0),(-256,-1),(257,1),(255,0),(0,0)]:
            row={'rawX':raw,'rawY':-raw,'deltaRawX':0,'deltaRawY':0,
                 'snapshotX':expected,'snapshotY':-expected,'renderedX':expected,'renderedY':-expected}
            with self.subTest(raw=raw):
                v.validate_root(row,(raw,-raw))
                for key in ('snapshotX','snapshotY','renderedX','renderedY'):
                    with self.assertRaises(ValueError):
                        v.validate_root(dict(row,**{key:row[key]+1}),(raw,-raw))
                if raw%256:
                    with self.assertRaises(ValueError):
                        v.validate_root(dict(row,renderedX=raw/256),(raw,-raw))
    def test_pause_count_digest_position_and_texture_mutations(self):
        row={'digest':'a'*64,'texturePNG_SHA256':'b'*64,'rawX':100,'rawY':200}
        paused=[dict(row) for _ in range(8)]; v.validate_pause(paused)
        with self.assertRaises(ValueError): v.validate_pause(paused[:-1])
        for key,value in [('digest','c'*64),('texturePNG_SHA256','c'*64),('rawX',101),('rawY',201)]:
            changed=copy.deepcopy(paused); changed[-1][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): v.validate_pause(changed)
    def test_actual_png_hash_dimensions_and_blankness(self):
        path=self.temp/'plate.png'; image=Image.new('RGB',(704,326))
        image.putdata([(i%256,(i//256)%256,17) for i in range(704*326)]); image.save(path)
        capture={'sha256':v.sha(path),'nativePixels':[704,326]}
        v.validate_capture_image(capture,path)
        with self.assertRaisesRegex(ValueError,'hash'): v.validate_capture_image(dict(capture,sha256='0'*64),path)
        with self.assertRaisesRegex(ValueError,'dimensions'): v.validate_capture_image(dict(capture,nativePixels=[352,163]),path)
        Image.new('RGB',(704,326)).save(path)
        with self.assertRaisesRegex(ValueError,'Blank'): v.validate_capture_image(dict(capture,sha256=v.sha(path)),path)
    def test_scope_and_zero_capture_packet_rejected(self):
        with self.assertRaisesRegex(ValueError,'scope'): v.validate_packet({'schema':'existing-art-traversal-001','status':'ACCEPTED'}, {})
        with self.assertRaisesRegex(ValueError,'Missing records'):
            (self.temp/'manifest.json').write_text('[]'); v.attachments(self.temp)
    def test_one_based_phase_boundaries(self):
        self.assertEqual(v.phase(20),'quarter-west'); self.assertEqual(v.phase(21),'half-west')
        self.assertEqual(v.phase(55),'approach-west'); self.assertEqual(v.phase(56),'reverse-east')
        self.assertEqual(v.phase(380),'release')

    def test_exact_coordinated_three_and_wrong_case_attachments(self):
        summary={'result':'Passed','totalTestCount':3,'passedTests':3,'failedTests':0,'skippedTests':0,'expectedFailures':0}
        tree={'testNodes':[{'nodeType':'Test Case','nodeIdentifier':name,'result':'Passed'} for name in sorted(v.COORDINATED_TESTS)]}
        v.validate_result(summary,tree,v.COORDINATED_TESTS)
        with self.assertRaises(ValueError): v.validate_result(summary,tree)
        changed=copy.deepcopy(tree); changed['testNodes'][0]['nodeIdentifier']='Unrelated/test()'
        with self.assertRaisesRegex(ValueError,'identity'): v.validate_result(summary,changed,v.COORDINATED_TESTS)
        (self.temp/'record.json').write_text('{}')
        item={'suggestedHumanReadableName':'eat-records_uuid','exportedFileName':'record.json','isAssociatedWithFailure':False}
        for case_id,failure in [('Other/test()',False),(v.TEST,True)]:
            case={'testIdentifier':case_id,'attachments':[dict(item,isAssociatedWithFailure=failure)]}
            (self.temp/'manifest.json').write_text(json.dumps([case]))
            with self.assertRaises(ValueError): v.attachments(self.temp)

if __name__=='__main__': unittest.main()
