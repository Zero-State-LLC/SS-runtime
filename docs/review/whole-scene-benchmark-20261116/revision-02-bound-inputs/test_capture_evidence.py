#!/usr/bin/env python3
"""Portable offline tests for revision 02. No xcrun or simulator; exports rebuilt from retained capture/."""
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
            shutil.copy(v.CAPTURE / (stem + ('.json' if stem == 'r02-records' else '.png')), target / item['exportedFileName'])
    (target / 'manifest.json').write_text(json.dumps(manifest))
    return target

class Revision02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = scratch(); cls.exports = rebuild_exports(cls.temp / 'exports')
        cls.summary, cls.tree = v.offline_query('summary'), v.offline_query('tests')
        cls.records = v.load(v.CAPTURE / 'r02-records.json')
        cls.plates, _ = v.attachments(cls.exports)

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp)

    def query(self, summary=None): return lambda k: copy.deepcopy(summary or self.summary) if k == 'summary' else copy.deepcopy(self.tree)
    def inputs(self, change, pattern):
        r = copy.deepcopy(self.records); change(r)
        with self.assertRaisesRegex(ValueError, pattern): v.validate_inputs(r)
    def captures(self, change, pattern):
        r = copy.deepcopy(self.records); change(r)
        with self.assertRaisesRegex(ValueError, pattern): v.validate_captures(r)

    def testActualEvidenceVerifiesWithoutXcrun(self):
        with mock.patch.object(v.subprocess, 'check_output', side_effect=AssertionError('xcrun used')):
            report = v.verify(self.exports, RESULT, v.offline_query)
        self.assertEqual((report['plates'], report['captures'], report['boundRuntimeAssets'], report['boundCameraFrames'],
                          report['boundUprightInputs'], report['r01PixelEqual']), (54, 18, 2, 16, 6, 54))

    def testRejectsResultAndIdentity(self):
        for f, val in [('passedTests', 0), ('totalTestCount', 0), ('failedTests', 1), ('result', 'unknown')]:
            s = copy.deepcopy(self.summary); s[f] = val
            with self.assertRaises(ValueError): v.validate_result(s, self.tree)
        with self.assertRaises(ValueError): v.validate_result(self.summary, json.loads(json.dumps(self.tree).replace(v.TEST, 'X/y()')))
        s = copy.deepcopy(self.summary); s['finishTime'] = 0
        with self.assertRaisesRegex(ValueError, 'Retained summary'): v.verify(self.exports, RESULT, self.query(s))

    def testRejectsBoundInputMutation(self):
        self.inputs(lambda r: r['runtimeAssets']['env_ground_plaza'].update(sha256='0' * 64), 'Runtime asset bytes')
        self.inputs(lambda r: r['runtimeAssets']['env_ground_asphalt'].update(path='other.png'), 'path changed')
        self.inputs(lambda r: r['runtimeAssets'].pop('env_ground_asphalt'), 'Runtime asset scope')
        self.inputs(lambda r: r['cameraFrameSHA256'].update({'actor_camera_hit_none_01@4x.png': '0' * 64}), 'Camera frame bytes')
        self.inputs(lambda r: r['cameraFrameSHA256'].pop('actor_camera_destroy_none_04@4x.png'), 'Camera frame census')
        self.inputs(lambda r: r['uprightInputSHA256'].update({'tree.png': '0' * 64}), 'Upright bytes')
        self.inputs(lambda r: r['uprightInputSHA256'].update({'whole-scene-muted-paving.png': '0' * 64}), 'Paving')

    def testRejectsScopeAndRetroactiveClaims(self):
        self.inputs(lambda r: r.update(status='ACCEPTED'), 'status')
        self.inputs(lambda r: r.update(revision=1), 'revision')
        self.inputs(lambda r: r.update(supersedesNothing='attests revision 01'), 'Retroactive')
        self.inputs(lambda r: r['openDeficits'].pop(), 'deficits')
        self.inputs(lambda r: r['openDeficits'].__setitem__(0, 'building solved'), 'deficits')

    def testRejectsCaptureCensusAndLabels(self):
        self.captures(lambda r: r['captures'].pop(), 'census')
        self.captures(lambda r: r['captures'][0].update(name='r02-wholescene-control-ordinary-z999'), 'label')
        self.captures(lambda r: r['captures'][0].update(hudVisible=not r['captures'][0]['hudVisible']), 'Visibility')
        self.captures(lambda r: r['captures'][0]['actors'][1].update(name='sprite-camera-9'), 'Role')
        self.captures(lambda r: r['captures'][0].update(nativePixels=[704, 326]), 'dimensions')
        self.captures(lambda r: r['captures'][0].update(hudHiddenByProduction=99), 'HUD hidden')
        muted = next(i for i, c in enumerate(self.records['captures']) if c['arm'] == 'muted')
        self.captures(lambda r: r['captures'][muted].update(paving='env_ground_plaza@1x.png'), 'Paving label')

    def testRejectsPlateAndR01Mismatch(self):
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); changed = temp / 'c.png'
        key = 'r02-paving-muted-ordinary-z125-native'
        shutil.copy(self.plates[key], changed)
        with Image.open(changed) as im:
            im = im.convert('RGBA'); im.putpixel((3, 3), (255, 0, 255, 255)); im.save(changed)
        caps = copy.deepcopy(self.records['captures'])
        for c in caps:
            if c['name'] == 'r02-paving-muted-ordinary-z125': c['pngSHA256']['-native'] = v.sha(changed)
        with self.assertRaisesRegex(ValueError, 'does not reproduce revision-01'): v.plate_facts({**self.plates, key: changed}, caps)
        with self.assertRaisesRegex(ValueError, 'Plate hash'): v.plate_facts({**self.plates, key: changed}, self.records['captures'])

    def testRejectsAttachmentAndPriorSwiftMutation(self):
        temp = scratch(); self.addCleanup(shutil.rmtree, temp); e = temp / 'e'; shutil.copytree(self.exports, e)
        m = v.load(e / 'manifest.json'); m[0]['attachments'] = [a for a in m[0]['attachments'] if 'z140-half' not in a['suggestedHumanReadableName']]
        (e / 'manifest.json').write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError, '54 plates'): v.attachments(e)
        real = v.sha
        with mock.patch.object(v, 'sha', lambda p: '0' * 64 if str(p).endswith('WholeSceneBenchmarkTests.swift') else real(p)), \
             self.assertRaisesRegex(ValueError, 'Revision-01 Swift'):
            v.verify(self.exports, RESULT, self.query())
        with mock.patch.object(v, 'sha', lambda p: '0' * 64 if str(p).endswith('WholeScenePavingTests.swift') else real(p)), \
             self.assertRaisesRegex(ValueError, 'WholeScenePavingTests'):
            v.verify(self.exports, RESULT, self.query())

if __name__ == '__main__': unittest.main(verbosity=2)
