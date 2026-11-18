#!/usr/bin/env python3
"""Portable offline tests for the paving trial verifier. No xcrun or simulator."""
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

RESULT = Path('offline-retained.xcresult')

def scratch(): return Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR')))

def rebuild_exports(target):
    manifest = v.load(v.CAPTURE / 'attachment-manifest.json'); target.mkdir()
    for case in manifest:
        for item in case['attachments']:
            stem = item['suggestedHumanReadableName'].split('_')[0]
            shutil.copy(v.CAPTURE / (stem + ('.json' if stem == 'paving-records' else '.png')), target / item['exportedFileName'])
    (target / 'manifest.json').write_text(json.dumps(manifest))
    return target

class PavingTrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = scratch(); cls.exports = rebuild_exports(cls.temp / 'exports')
        cls.summary, cls.tree = v.offline_query('summary'), v.offline_query('tests')
        cls.records = v.load(v.CAPTURE / 'paving-records.json')

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp)

    def query(self, summary=None):
        return lambda kind: copy.deepcopy(summary or self.summary) if kind == 'summary' else copy.deepcopy(self.tree)

    def mutate(self, change, pattern):
        records = copy.deepcopy(self.records); change(records)
        with self.assertRaisesRegex(ValueError, pattern): v.validate_records(records)

    def testActualEvidenceVerifiesWithoutXcrun(self):
        with mock.patch.object(v.subprocess, 'check_output', side_effect=AssertionError('xcrun used')):
            report = v.verify(self.exports, RESULT, v.offline_query)
        self.assertEqual((report['plates'], report['captures']), (18, 6))
        self.assertFalse(report['sourceEdgeMeanAbsDiff']['seamless'])
        self.assertTrue(12 < report['sourceEdgeMeanAbsDiff']['leftRight'] < 15 and 12 < report['sourceEdgeMeanAbsDiff']['topBottom'] < 15)

    def testRejectsZeroTestRunAndIdentity(self):
        rejected = v.load(v.HERE / 'attempts/02-zero-tests-rejected/summary.json')
        with self.assertRaises(ValueError): v.validate_result(rejected, {'testNodes': []})
        for field, value in [('passedTests', 0), ('totalTestCount', 0), ('failedTests', 1), ('result', 'unknown')]:
            s = copy.deepcopy(self.summary); s[field] = value
            with self.assertRaises(ValueError): v.validate_result(s, self.tree)
        with self.assertRaises(ValueError): v.validate_result(self.summary, json.loads(json.dumps(self.tree).replace(v.TEST, 'X/y()')))

    def testRejectsProvenanceAndScopeMutation(self):
        self.mutate(lambda r: r.update(status='ACCEPTED'), 'status')
        self.mutate(lambda r: r['openItems'].pop(0), 'Open items')
        self.mutate(lambda r: r['openItems'].__setitem__(0, 'seamless'), 'Open items')
        self.mutate(lambda r: r['pavingSource'].update(sha256='0' * 64), 'provenance')
        self.mutate(lambda r: r['pavingSource'].update(tileUnits=64), 'provenance')
        self.mutate(lambda r: r['inputSHA256'].update({'whole-scene-muted-paving.png': '0' * 64}), 'Executed paving')
        self.mutate(lambda r: r['inputSHA256'].pop('tree.png'), 'Input hash scope')

    def testRejectsCensusLabelAndArmDivergence(self):
        self.mutate(lambda r: r['captures'].pop(), 'census')
        self.mutate(lambda r: r['captures'][0].update(mode='staged'), 'ordinary')
        self.mutate(lambda r: r['captures'][0].update(fieldVisible=False), 'ordinary')
        self.mutate(lambda r: r['captures'][0].update(name='paving-muted-ordinary-z999'), 'label')
        self.mutate(lambda r: r['captures'][0]['actors'][2].update(name='new-building'), 'Role')
        self.mutate(lambda r: r['captures'][0].update(hudHiddenByProduction=0), 'HUD hidden')
        def root(r): r['captures'][0]['actors'][0]['projectedRoot'][0] += 1
        self.mutate(root, 'roots differ')

    def testRejectsPlateAndPriorEvidenceMutation(self):
        plates, _ = v.attachments(self.exports)
        same = {**plates, 'paving-muted-ordinary-z125-native': plates['paving-plaza-ordinary-z125-native']}
        captures = copy.deepcopy(self.records['captures'])
        for c in captures:
            if c['name'] == 'paving-muted-ordinary-z125': c['pngSHA256']['-native'] = v.sha(plates['paving-plaza-ordinary-z125-native'])
        with self.assertRaisesRegex(ValueError, 'identical to plaza'): v.plate_facts(same, captures)
        real = v.sha
        with mock.patch.object(v, 'sha', lambda p: '0' * 64 if str(p).endswith('WholeSceneBenchmarkTests.swift') else real(p)), \
             self.assertRaisesRegex(ValueError, 'Prior WholeSceneBenchmarkTests'):
            v.verify(self.exports, RESULT, self.query())
        with mock.patch.object(v, 'sha', lambda p: '0' * 64 if str(p).endswith('whole-scene-muted-paving.png') else real(p)), \
             self.assertRaisesRegex(ValueError, 'paving'):
            v.verify(self.exports, RESULT, self.query())
        with mock.patch.object(v, 'sha', lambda p: '1' * 64 if 'whole-scene-benchmark-20261116/capture/wholescene-control-staged-z140-half' in str(p) else real(p)), \
             self.assertRaisesRegex(ValueError, 'Prior plate bytes'):
            v.verify(self.exports, RESULT, self.query())

    def testRejectsAttachmentMutation(self):
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); exports = temp / 'e'; shutil.copytree(self.exports, exports)
        manifest = v.load(exports / 'manifest.json')
        manifest[0]['attachments'] = [a for a in manifest[0]['attachments'] if 'z100-half' not in a['suggestedHumanReadableName']]
        (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, '18 plates'): v.attachments(exports)

    def testPreviewIsCssOnlyAndLabelled(self):
        html = (v.HERE / 'source-repeat-preview.html').read_text()
        self.assertIn('../../../AppTests/WholeSceneAssets/whole-scene-muted-paving.png', html)
        self.assertIn('background-repeat:repeat', html)
        self.assertIn('NOT mathematically seamless', html); self.assertIn('seam/repetition pending', html)
        self.assertNotIn('<canvas', html)

if __name__ == '__main__': unittest.main(verbosity=2)
