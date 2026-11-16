#!/usr/bin/env python3
"""Portable offline mutation tests for verify_capture.py. No xcrun or simulator: exports are rebuilt in a
temp dir from retained capture/ files and the retained attachment manifest."""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock
from PIL import Image
import verify_capture as v

RESULT = Path('offline-retained.xcresult')  # never opened

def scratch(): return Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR')))

def rebuild_exports(target):
    manifest = v.load(v.CAPTURE / 'attachment-manifest.json'); target.mkdir()
    for case in manifest:
        for item in case['attachments']:
            stem = item['suggestedHumanReadableName'].split('_')[0]
            shutil.copy(v.CAPTURE / (stem + ('.json' if stem == 'wholescene-records' else '.png')), target / item['exportedFileName'])
    (target / 'manifest.json').write_text(json.dumps(manifest))
    return target

class WholeSceneCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = scratch(); cls.exports = rebuild_exports(cls.temp / 'exports')
        cls.summary, cls.tree = v.offline_query('summary'), v.offline_query('tests')
        cls.records = v.load(v.CAPTURE / 'wholescene-records.json')

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp)

    def query(self, summary=None, tree=None):
        return lambda kind: copy.deepcopy(summary or self.summary) if kind == 'summary' else copy.deepcopy(tree or self.tree)

    def copied(self):
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); shutil.copytree(self.exports, temp / 'e'); return temp / 'e'

    def export_of(self, exports, stem):
        for case in v.load(exports / 'manifest.json'):
            for item in case['attachments']:
                if item['suggestedHumanReadableName'].startswith(stem): return exports / item['exportedFileName']

    def testActualEvidenceVerifiesOfflineWithoutXcrun(self):
        with mock.patch.object(v.subprocess, 'check_output', side_effect=AssertionError('xcrun used')):
            report = v.verify(self.exports, RESULT, v.offline_query)
        self.assertEqual((report['plates'], report['captures']), (36, 12))
        self.assertEqual(report['retainedControl']['differingPixels'], 0)
        self.assertEqual(len(report['diagnosticDiffersFromControl']), 6)
        self.assertEqual(report['stagedDiffersFromOrdinary'], 6)
        self.assertEqual(report['unboundInputs'], v.UNBOUND_INPUTS)

    def testRejectsZeroFailedSkippedAndIdentity(self):
        for field, value in [('passedTests', 0), ('failedTests', 1), ('skippedTests', 1), ('expectedFailures', 1), ('result', 'Failed')]:
            summary = copy.deepcopy(self.summary); summary[field] = value
            with self.assertRaises(ValueError): v.validate_result(summary, self.tree)
        tree = json.loads(json.dumps(self.tree).replace(v.TEST, 'Other/testOther()'))
        with self.assertRaises(ValueError): v.validate_result(self.summary, tree)
        changed = copy.deepcopy(self.summary); changed['finishTime'] = 0
        with self.assertRaisesRegex(ValueError, 'Retained summary'): v.verify(self.exports, RESULT, self.query(summary=changed))

    def testRejectsAttachmentCensusPathAndBytes(self):
        exports = self.copied(); manifest = v.load(exports / 'manifest.json')
        manifest[0]['attachments'] = [a for a in manifest[0]['attachments'] if 'z140-half' not in a['suggestedHumanReadableName']]
        (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, '36 plates'): v.attachments(exports)
        exports = self.copied(); manifest = v.load(exports / 'manifest.json')
        manifest[0]['attachments'][0]['exportedFileName'] = '../../etc/hosts'; (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'escape'): v.attachments(exports)
        exports = self.copied(); path = self.export_of(exports, 'wholescene-diagnostic-ordinary-z125-native')
        Image.new('RGB', (2112, 978), (5, 5, 5)).save(path)
        with self.assertRaisesRegex(ValueError, 'Retained plate differs'): v.verify(exports, RESULT, self.query())

    def mutate(self, change, pattern):
        records = copy.deepcopy(self.records); change(records)
        with self.assertRaisesRegex(ValueError, pattern): v.validate_records(records)

    def testRejectsScopeDeficitCensusAndLabelling(self):
        self.mutate(lambda r: r.update(status='CORRECTED'), 'status')
        self.mutate(lambda r: r['openDeficits'].pop(0), 'deficits')
        self.mutate(lambda r: r.update(openDeficits=['building solved'] + r['openDeficits'][1:]), 'deficits')
        self.mutate(lambda r: r['openDeficits'].__setitem__(1, r['openDeficits'][1].replace('NOT SOLVED', 'improved')), 'deficits')
        self.mutate(lambda r: r['captures'][0]['actors'][0].update(name='sprite-enemy'), 'role')
        self.mutate(lambda r: r['captures'][0]['pngSHA256'].pop('-half'), 'suffix')
        self.mutate(lambda r: r['captures'][0].update(nativePixels=[704, 326]), 'dimensions')
        self.mutate(lambda r: r['captures'][0].update(mode='staged' if r['captures'][0]['mode'] == 'ordinary' else 'ordinary', hudVisible=not r['captures'][0]['hudVisible'], fieldVisible=not r['captures'][0]['fieldVisible']), 'census|label')
        self.mutate(lambda r: r['inputSHA256'].update({'extra.png': '0' * 64}), 'Input hash scope')
        self.mutate(lambda r: r['captures'].pop(), 'census')
        self.mutate(lambda r: r['captures'][0].update(hudVisible=not r['captures'][0]['hudVisible']), 'visibility')
        self.mutate(lambda r: r['captures'][0].update(hudNodeCount=0), 'HUD')
        self.mutate(lambda r: r['captures'][0]['actors'].pop(), 'Upright')
        self.mutate(lambda r: r['inputSHA256'].update({'tree.png': '0' * 64}), 'Input bytes')

    def testRejectsWrongDimensionsColouredGrayAndStagedDiagnosticSameAsOrdinary(self):
        plates, _ = v.attachments(self.exports)
        temp = scratch(); self.addCleanup(shutil.rmtree, temp)
        small = temp / 'small.png'; shutil.copy(plates['wholescene-control-ordinary-z100-half'], small)
        with Image.open(small) as im: im.resize((352, 163)).save(small)
        with self.assertRaisesRegex(ValueError, 'dimensions wrong'):
            v.plate_facts({**plates, 'wholescene-control-ordinary-z100-half': small}, self.record_hashes({'wholescene-control-ordinary-z100-half': small}))
        colour = temp / 'colour.png'; shutil.copy(plates['wholescene-control-ordinary-z100-grayscale'], colour)
        with Image.open(colour) as im:
            im = im.convert('RGBA'); im.putpixel((5, 5), (200, 10, 10, 255)); im.save(colour)
        with self.assertRaisesRegex(ValueError, 'Grayscale plate has colour'):
            v.plate_facts({**plates, 'wholescene-control-ordinary-z100-grayscale': colour}, self.record_hashes({'wholescene-control-ordinary-z100-grayscale': colour}))
        same = {**plates, 'wholescene-diagnostic-staged-z140-native': plates['wholescene-diagnostic-ordinary-z140-native']}
        with self.assertRaisesRegex(ValueError, 'Staged view not distinct'):
            v.plate_facts(same, self.record_hashes({'wholescene-diagnostic-staged-z140-native': plates['wholescene-diagnostic-ordinary-z140-native']}))

    def record_hashes(self, replaced):
        captures = copy.deepcopy(self.records['captures'])
        for c in captures:
            for suffix in c['pngSHA256']:
                if c['name'] + suffix in replaced: c['pngSHA256'][suffix] = v.sha(replaced[c['name'] + suffix])
        return captures

    def testRejectsRetainedControlMismatchVisibly(self):
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); fake = temp / 'retained.png'
        shutil.copy(v.RETAINED_CONTROL, fake)
        with Image.open(fake) as im:
            im = im.convert('RGBA'); im.putpixel((10, 10), (255, 0, 0, 255)); im.save(fake)
        plates, _ = v.attachments(self.exports)
        with mock.patch.object(v, 'RETAINED_CONTROL', fake), self.assertRaisesRegex(ValueError, "differingPixels': 1"):
            v.plate_facts(plates, self.records['captures'])

    def testRejectsPlateRecordHashAndIdenticalArms(self):
        plates, _ = v.attachments(self.exports)
        captures = copy.deepcopy(self.records['captures']); captures[0]['pngSHA256']['-native'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Plate hash'): v.plate_facts(plates, captures)
        swapped = dict(plates); swapped['wholescene-diagnostic-staged-z100-native'] = plates['wholescene-control-staged-z100-native']
        captures = copy.deepcopy(self.records['captures'])
        for c in captures:
            if c['name'] == 'wholescene-diagnostic-staged-z100': c['pngSHA256']['-native'] = v.sha(plates['wholescene-control-staged-z100-native'])
        with self.assertRaisesRegex(ValueError, 'identical to control'): v.plate_facts(swapped, captures)

    def testRejectsBlankPlateAndChangedConcept(self):
        plates, _ = v.attachments(self.exports)
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); blank = temp / 'b.png'
        Image.new('RGB', (2112, 978), (9, 9, 9)).save(blank)
        captures = copy.deepcopy(self.records['captures'])
        for c in captures:
            if c['name'] == 'wholescene-diagnostic-ordinary-z100': c['pngSHA256']['-half'] = v.sha(blank)
        with self.assertRaisesRegex(ValueError, 'Blank'):
            v.plate_facts({**plates, 'wholescene-diagnostic-ordinary-z100-half': blank}, captures)
        real = v.sha
        with mock.patch.object(v, 'sha', lambda p: '0' * 64 if str(p).endswith('approved-concept.png') else real(p)), \
             self.assertRaisesRegex(ValueError, 'concept'):
            v.verify(self.exports, RESULT, self.query())

if __name__ == '__main__':
    unittest.main(verbosity=2)
