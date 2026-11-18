#!/usr/bin/env python3
"""Offline mutation tests over ACTUAL retained capture. Missing capture is an error, not a skip.
Run only after native import. Synthetic pre-capture guards live in test_evidence_guards.py.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
import verify_capture as v

CAPTURE=Path(__file__).resolve().parent/'capture'

class RetainedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        v.need((CAPTURE/'eat-records.json').is_file(),'Actual native evidence has not been captured/imported')
        cls.temp=Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR'))).resolve()
        cls.exports=cls.temp/'exports'; cls.exports.mkdir()
        manifest=v.load(CAPTURE/'attachment-manifest.json')
        for case in manifest:
            for item in case['attachments']:
                name=item['suggestedHumanReadableName'].split('_')[0]
                if not name.startswith('eat-'): continue
                source=CAPTURE/(name+('.json' if name=='eat-records' else '.png'))
                target=(cls.exports/item['exportedFileName']).resolve()
                v.need(target.is_relative_to(cls.exports),'Export path escape')
                target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,target)
        (cls.exports/'manifest.json').write_text(json.dumps(manifest))
        cls.summary=v.load(CAPTURE/'summary.json'); cls.tree=v.load(CAPTURE/'tests.json')
        cls.allowed=v.load(CAPTURE/'run-scope.json')['allowedTests']
        cls.files=v.attachments(cls.exports); cls.native_packet=v.load(cls.files['eat-records'])
    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp)
    def packet(self): return copy.deepcopy(self.native_packet)
    def test_actual_retained_evidence_without_xcrun(self):
        report,_=v.verify(self.exports,self.summary,self.tree,allowed_tests=self.allowed)
        self.assertEqual(report['captures'],52); self.assertEqual(report['arms'],2)
        self.assertGreater(report['rows'],760)
    def test_zero_test_and_wrong_identity_mutations(self):
        summary=dict(self.summary,totalTestCount=0,passedTests=0)
        with self.assertRaises(ValueError): v.verify(self.exports,summary,self.tree,allowed_tests=self.allowed)
        tree=copy.deepcopy(self.tree)
        def change(nodes):
            for node in nodes:
                if node.get('nodeIdentifier')==v.TEST: node['nodeIdentifier']='Wrong/test()'
                change(node.get('children',[]))
        change(tree['testNodes'])
        with self.assertRaises(ValueError): v.verify(self.exports,self.summary,tree,allowed_tests=self.allowed)
    def test_bound_input_and_selection_mutations(self):
        packet=self.packet(); packet['resourceInventory'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Resource'): v.validate_packet(packet,self.files)
        packet=self.packet(); row=packet['arms'][0]['records'][0]; row['sourceSHA256']='0'*64
        with self.assertRaisesRegex(ValueError,'source'): v.validate_packet(packet,self.files)
        packet=self.packet(); packet['arms'][0]['records'][0]['deliveredPath']='unbound.png'
        with self.assertRaisesRegex(ValueError,'source'): v.validate_packet(packet,self.files)
    def test_independent_position_and_delta_mutations(self):
        for key in ('rawX','rawY','deltaRawX','deltaRawY','renderedX','renderedY'):
            packet=self.packet(); packet['arms'][0]['records'][10][key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError): v.validate_packet(packet,self.files)
    def test_pause_and_frozen_selection_mutations(self):
        packet=self.packet(); rows=packet['arms'][0]['records']; index=next(i for i,r in enumerate(rows) if r['paused'])
        rows.pop(index)
        for i,row in enumerate(rows): row['ordinal']=i
        with self.assertRaisesRegex(ValueError,'pause hold'): v.validate_packet(packet,self.files)
        packet=self.packet(); rows=packet['arms'][0]['records']; selected=next(r for r in rows if r['requestedClip']=='player_move')['deliveredPath']
        for row in rows:
            if row['requestedClip']=='player_move':
                row['deliveredPath']=selected
                row['sourceSHA256']=next(r['sha256'] for r in packet['resourceInventory'] if r['path']==selected)
        with self.assertRaisesRegex(ValueError,'Frozen'): v.validate_packet(packet,self.files)
    def test_attachment_hash_and_missing_capture_mutations(self):
        packet=self.packet(); capture=packet['arms'][0]['captures'][0]
        files=dict(self.files); files.pop(capture['name'])
        with self.assertRaises(ValueError): v.validate_packet(packet,files)
        packet=self.packet(); packet['arms'][0]['captures'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'hash'): v.validate_packet(packet,self.files)
    def test_projection_and_dimensions_mutations(self):
        packet=self.packet(); capture=next(c for c in packet['arms'][0]['captures'] if c['mapping']!='shipping')
        capture['observedPlayerSceneRoot'][0]+=1
        with self.assertRaisesRegex(ValueError,'root mismatch'): v.validate_packet(packet,self.files)
        packet=self.packet(); packet['arms'][0]['captures'][0]['nativePixels'][0]+=1
        with self.assertRaisesRegex(ValueError,'dimensions'): v.validate_packet(packet,self.files)
    def test_capture_phase_and_scope_mutations(self):
        packet=self.packet(); packet['arms'][0]['captures'][0]['name']='eat-normal-unknown-shipping'
        with self.assertRaisesRegex(ValueError,'census'): v.validate_packet(packet,self.files)
        packet=self.packet(); packet['unsupported']=[]
        with self.assertRaisesRegex(ValueError,'scope'): v.validate_packet(packet,self.files)
    def test_replay_and_per_tick_authority_mutations(self):
        packet=self.packet(); packet['arms'][0]['replayDigest']='0'*64
        with self.assertRaisesRegex(ValueError,'replay'): v.validate_packet(packet,self.files)
        packet=self.packet(); packet['arms'][0]['records'][10]['digest']='0'*64
        with self.assertRaisesRegex(ValueError,'authority'): v.validate_packet(packet,self.files)

if __name__=='__main__': unittest.main()
