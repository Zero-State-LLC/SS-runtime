#!/usr/bin/env python3
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import verify as v

class EvidenceTests(unittest.TestCase):
    def test_actual_evidence(self):
        rows=v.verify()
        self.assertEqual(len(rows),3)
    def test_exact_nonzero_results(self):
        summary=v.load(v.HERE/'capture/summary.json'); tree=v.load(v.HERE/'capture/tests.json')
        for key,value in [('totalTestCount',0),('passedTests',0),('failedTests',1),('skippedTests',1),('expectedFailures',1)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                v.validate_result(dict(summary,**{key:value}),tree)
        with self.assertRaises(ValueError): v.validate_result(summary,{'testNodes':[]})
    def test_record_mutations(self):
        row=next(row for row in v.verify() if row['record']['selectionIndex']==2)
        for key,value in [('swipes',0),('initiallyHittable',True),('selectionResult','selected=2;count=2'),('target','signalJammer'),('windowWidth',375),('captureMethod','app.screenshot'),('voiceOverSession',True),('physicalDevice',True),('gameResumeVerified',True),('accessibilityLabel','')]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                v.validate_record(dict(row['record'],**{key:value}),row['case'])
    def test_changed_attachment_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            capture=Path(tmp)/'capture'; shutil.copytree(v.HERE/'capture',capture)
            name=next(name for name in v.load(capture/'inventory.json') if name.endswith('.png'))
            (capture/name).write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'hash'): v.verify(capture)
    def test_missing_and_escape_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            capture=Path(tmp)/'capture'; shutil.copytree(v.HERE/'capture',capture)
            manifest=v.load(capture/'manifest.json'); inventory=v.load(capture/'inventory.json')
            original=manifest[0]['attachments'][0]['exportedFileName']
            manifest[0]['attachments'][0]['exportedFileName']='../outside.json'
            inventory['../outside.json']=inventory.pop(original)
            (capture/'manifest.json').write_text(json.dumps(manifest))
            inventory['manifest.json']=v.sha(capture/'manifest.json')
            (capture/'inventory.json').write_text(json.dumps(inventory))
            with self.assertRaisesRegex(ValueError,'escape'): v.verify(capture)
    def test_cropped_attempt_does_not_qualify(self):
        capture=v.HERE/'attempts/01-window-capture'
        records=list(capture.rglob('*.json'))
        rejected=0
        for path in records:
            record=v.load(path)
            if isinstance(record,dict) and 'selectionResult' in record:
                self.assertNotEqual(record.get('captureMethod'),'XCUIScreen.main.screenshot')
                rejected+=1
        self.assertEqual(rejected,3)

if __name__=='__main__': unittest.main()
