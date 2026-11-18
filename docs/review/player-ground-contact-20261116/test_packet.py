#!/usr/bin/env python3
"""Independent artifact and geometry checks, not visual acceptance."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import unittest
from PIL import Image
import analyze_contacts as analysis

HERE = Path(__file__).resolve().parent
ORIGINAL = Path(os.environ.get('SS_ORIGINAL_SOURCE_ROOT', '/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs'))

def load(name): return json.loads((HERE/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rgba(path):
    with Image.open(path) as image:
        if image.size != (384,416): raise ValueError('Unexpected source canvas')
        return image.convert('RGBA').tobytes()

class GroundContactPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = load('baseline-poses.json')
        cls.candidate = load('candidate-poses.json')
        cls.traces = load('core-traces.json')['traces']

    def testOriginalInputsUnchanged(self):
        if not ORIGINAL.is_dir():
            self.skipTest('External original masters unavailable. Portable copied-byte checks run separately.')
        inventory = load('original-input-hashes.json')
        self.assertEqual(len(inventory),1012)
        for path,digest in inventory.items():
            self.assertEqual(sha(ORIGINAL/path),digest,path)

    def testArchivedInventoryMatchesPublishedBaseline(self):
        prior = HERE.parent/'player-all-release-source-20261116/artifacts/input-inventory.json'
        self.assertEqual(load('original-input-hashes.json'),json.loads(prior.read_text()))

    def testExactBaselineAndReviewedKeys(self):
        for index in range(16):
            name = f'{index:02d}.png'
            self.assertEqual(sha(HERE/'baseline-frames'/name),load('original-input-hashes.json')[f'SS-player-bounded-proportions/frames/{name}'])
        for index in (0,4,8,12):
            self.assertEqual(rgba(HERE/'baseline-frames'/f'{index:02d}.png'),rgba(HERE/'editable-candidate/frames'/f'{index:02d}.png'))
            self.assertEqual(self.baseline[index]['legs'],self.candidate[index]['legs'])

    def testExactlySixChangedRecoveryKeys(self):
        changed = [index for index in range(16) if rgba(HERE/'baseline-frames'/f'{index:02d}.png') != rgba(HERE/'editable-candidate/frames'/f'{index:02d}.png')]
        self.assertEqual(changed,[5,6,7,13,14,15])

    def testFixedLimbLengthsAndFiniteCoordinates(self):
        for pose in self.candidate:
            for leg in pose['legs']:
                for key in ('hip','knee','ankle','heel','toe'):
                    self.assertTrue(all(math.isfinite(x) for x in leg[key]))
                self.assertAlmostEqual(math.dist(leg['hip'],leg['knee']),12.5,places=8)
                self.assertAlmostEqual(math.dist(leg['knee'],leg['ankle']),14.5,places=8)

    def testFootTargetsContactTimingAndNoAddedBounce(self):
        for before,after in zip(self.baseline,self.candidate):
            self.assertEqual(before['time'],after['time'])
            for old,new in zip(before['legs'],after['legs']):
                for field in ('side','toe','heel','ankle','contact','contactWorld','angle'):
                    self.assertEqual(old[field],new[field])
                self.assertLessEqual(new['hip'][2],old['hip'][2])
                if new['contact']: self.assertEqual(new['toe'][2],0)

    def testCostumeAndAssemblyRetained(self):
        inventory = load('original-input-hashes.json')
        prefix = 'SS-player-bounded-proportions/'
        work = HERE/'editable-candidate'
        body = {p[len(prefix):]: digest for p,digest in inventory.items()
                if p.startswith(prefix + 'source/body-source/') and p.endswith('.png')}
        self.assertGreater(len(body), 10)
        for relative,digest in body.items():
            self.assertEqual(sha(work/relative),digest,relative)
        for relative in ('assemble.py','thigh.py','source/body-rig.json','boot/source.png','boot/four-facing-source.png','boot/registration.json'):
            self.assertEqual(sha(work/relative),inventory[prefix+relative])

    def testSourceManifestHasNoDrift(self):
        manifest=load('source-proposal.json')
        self.assertEqual(manifest['cycleSeconds'],.5)
        self.assertEqual(manifest['settleSecondsUnchanged'],.375)
        for path,digest in manifest['sourceFiles'].items(): self.assertEqual(sha(HERE/path),digest,path)

    def testCoreMatrixCoversActualStopSlideAndPause(self):
        cases={t['name']:t for t in self.traces}
        self.assertEqual(len(cases),12)
        for trace in self.traces:
            rows=trace['rows']
            for previous,row in zip(rows,rows[1:]):
                self.assertEqual(row['xRaw']-previous['xRaw'],row['dxRaw'])
                self.assertEqual(row['yRaw']-previous['yRaw'],row['dyRaw'])
                self.assertEqual(row['tick']-previous['tick'],0 if row['paused'] else 1)
        self.assertTrue(any(r['commandX'] and r['dxRaw']==0 for r in cases['collision-stop']['rows']))
        self.assertTrue(any(r['dxRaw']==0 and r['dyRaw']!=0 for r in cases['wall-slide']['rows']))
        self.assertTrue(any(r['dodgeRemaining']>0 for r in cases['dodge']['rows']))
        self.assertEqual(len([r for r in cases['pause']['rows'] if r['paused']]),15)

    def testSamplingNeverClaimsNativeAndBothVariantsSameContacts(self):
        packet=load('contact-comparison.json')
        self.assertIsNone(packet['threshold'])
        self.assertEqual(packet['visualAcceptance'],'UNREVIEWED')
        for trace in self.traces:
            for policy in ('fixed-time','distance-phase'):
                self.assertEqual(analysis.analyze(trace,self.baseline,policy),analysis.analyze(trace,self.candidate,policy))
        for name,digest in packet['sourceHashes'].items(): self.assertEqual(sha(HERE/name),digest)

    def testProjectionInverseAndRejectedFalseContact(self):
        row={'xRaw':256*100,'yRaw':256*200}
        leg={'toe':[4,15,0]}
        point=analysis.contact(row,leg)
        projected=analysis.project(*point['world'])
        for actual,expected in zip(projected,point['viewLogical']): self.assertAlmostEqual(actual,expected,places=10)
        leg['toe'][2]=1
        with self.assertRaises(ValueError): analysis.contact(row,leg)

    def testStationaryAndDodgeDoNotFabricateWalkContacts(self):
        for trace in self.traces:
            result=analysis.analyze(trace,self.baseline,'fixed-time')
            for row in result['rows']:
                if row['dodgeRemaining'] or row['dodgePressed'] or trace['name']=='stationary':
                    self.assertIsNone(row['frame'])

    def testExportedPagesContainAllMatrixRowsAndSeparateSpeed(self):
        for name,rate in [('normal-speed.html','1'),('quarter-speed.html','0.25')]:
            html=(HERE/name).read_text()
            self.assertIn(f', rate={rate};',html)
            self.assertIn('Not SpriteKit capture or live cadence',html)
            self.assertNotIn('PAYLOAD',html)
            payload=html.split('const records=',1)[1].split(', rate=',1)[0]
            records=json.loads(payload)
            self.assertEqual(len(records),24)
            for record in records:
                original=next(t for t in self.traces if t['name']==record['scenario'])
                self.assertEqual(len(record['rows']),len(original['rows']))
                for row,source in zip(record['rows'],original['rows']):
                    for field in ('tick','xRaw','yRaw','sample','paused','dodgeRemaining'):
                        self.assertEqual(row[field],source[field])

if __name__=='__main__': unittest.main(verbosity=2)
