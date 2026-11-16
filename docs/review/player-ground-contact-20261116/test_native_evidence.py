#!/usr/bin/env python3
"""Portable offline mutation tests for verify_native.py. No xcrun, simulator or external scratch:
exports are reconstructed in a temp dir from retained native/ files and the retained attachment manifest.
The live CLI (verify_native.py --exports --xcresult) separately compares against the real bundle."""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock
from PIL import Image
import verify_native as v

OLD = v.HERE / 'attempts/01-fixed-time-clamped/native/native-records.json'
RESULT = Path('offline-retained.xcresult')  # never opened; offline_query supplies retained JSON

def rebuild_exports(target):
    """Recreate xcresult export layout from retained, byte-verified files."""
    manifest = v.load(v.NATIVE / 'attachment-manifest.json'); target.mkdir()
    for case in manifest:
        for item in case['attachments']:
            name = item['suggestedHumanReadableName']
            source = v.NATIVE / ('native-records.json' if name.startswith('groundcontact-native-records')
                                 else name.split('_')[0] + '.png')
            shutil.copy(source, target / item['exportedFileName'])
    (target / 'manifest.json').write_text(json.dumps(manifest))
    return target

class NativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR'))); cls.exports = rebuild_exports(cls.temp / 'exports')
        cls.summary = v.offline_query('summary'); cls.tree = v.offline_query('tests')
        cls.records = v.load(v.NATIVE / 'native-records.json')
        cls.traces = v.load(v.HERE / 'core-traces.json')['traces']
        cls.poses = v.load(v.ROOT / 'AppTests/BenchmarkAssets/player-source-s-poses.json')

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp)

    def query(self, summary=None, tree=None):
        return lambda kind: copy.deepcopy(summary or self.summary) if kind == 'summary' else copy.deepcopy(tree or self.tree)

    def copied_exports(self):
        temp = Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR'))); self.addCleanup(shutil.rmtree, temp)
        shutil.copytree(self.exports, temp / 'e'); return temp / 'e'

    def manifest_path(self, exports, prefix):
        for case in v.load(exports / 'manifest.json'):
            for item in case['attachments']:
                if item['suggestedHumanReadableName'].startswith(prefix): return exports / item['exportedFileName']

    def testActualEvidenceVerifies(self):
        report = v.verify(self.exports, RESULT, self.query())
        self.assertEqual((report['samples'], report['segments'], report['captures']), (2400, 116, 76))
        self.assertEqual((report['changedPairs'], report['unchangedPairs']), (33, 5))
        self.assertTrue(report['fixedTimeValid']); self.assertEqual(report['runtimeBundledSources'], 24)

    def testOldClampedRunRejectedBySelectionNotOnlyCount(self):
        old = v.load(OLD)
        # Pad metadata so only the frozen frame selection can fail.
        old['captureCount'] = 76; old['fixedTimeLoop'] = 'runtime#238 corrected'
        segments = [r for r in old['records'] if r['kind'] == 'segment']
        old['records'] += segments[:116 - len(segments)] + segments[:max(0, 116 - 2 * len(segments))]
        with self.assertRaisesRegex(ValueError, 'fixed-time selection mismatch'):
            v.validate_records(old, self.traces, self.poses)

    def testRejectsFrozenFixedTimeAndMissingLoop(self):
        def freeze(r):
            for row in self.samples(r, 'quarter', 'fixed-time'):
                if row['frame'] < 15 and row['sample'] > 40:
                    row['frame'] = 15; row['texturePath'] = f"groundcontact-{row['family']}-15"
        self.mutate(freeze, 'fixed-time selection mismatch')
        self.mutate(lambda r: r.update(fixedTimeLoop='clamped'), 'loop declaration')
        self.mutate(lambda r: r.update(captureCount=75), 'Capture count')

    def testRejectsZeroFailedSkippedAndWrongIdentity(self):
        for field, value in [('passedTests', 0), ('failedTests', 1), ('skippedTests', 1), ('expectedFailures', 1), ('result', 'Failed')]:
            summary = copy.deepcopy(self.summary); summary[field] = value
            with self.assertRaises(ValueError): v.validate_result(summary, self.tree)
        tree = copy.deepcopy(self.tree); text = json.dumps(tree).replace(v.TEST, 'Other/testOther()')
        with self.assertRaises(ValueError): v.validate_result(self.summary, json.loads(text))
        tree = json.loads(json.dumps(self.tree).replace('"result" : "Passed"', '"result":"Failed"').replace('"Passed"', '"Failed"'))
        with self.assertRaises(ValueError): v.validate_result(self.summary, tree)

    def testRejectsAttachmentEvidenceMutation(self):
        exports = self.copied_exports()
        record = self.manifest_path(exports, 'groundcontact-native-records')
        record.write_bytes(record.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'Retained records differ'): v.verify(exports, RESULT, self.query())
        exports = self.copied_exports(); image = self.manifest_path(exports, 'groundcontact-quarter-distance-phase-baseline')
        Image.new('RGBA', (480, 330), (1, 2, 3, 255)).save(image)
        with self.assertRaisesRegex(ValueError, 'Retained capture differs'): v.verify(exports, RESULT, self.query())

    def testRejectsMissingOrDuplicateCapture(self):
        exports = self.copied_exports(); manifest = v.load(exports / 'manifest.json')
        manifest[0]['attachments'] = [a for a in manifest[0]['attachments'] if 'sample-30' not in a['suggestedHumanReadableName']]
        (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, '76 captures'): v.attachments(exports)
        exports = self.copied_exports(); manifest = v.load(exports / 'manifest.json')
        first = next(a for a in manifest[0]['attachments'] if a['suggestedHumanReadableName'].startswith('groundcontact-quarter'))
        manifest[0]['attachments'].append(dict(first)); (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'Duplicate'): v.attachments(exports)

    def testRejectsPathEscape(self):
        exports = self.copied_exports(); manifest = v.load(exports / 'manifest.json')
        manifest[0]['attachments'][0]['exportedFileName'] = '../../etc/hosts'
        (exports / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'escape'): v.attachments(exports)

    def testRejectsRetainedSummaryTreeAndRuntimeByteMutation(self):
        summary = copy.deepcopy(self.summary); summary['passedTests'] = 1; summary['finishTime'] = 0
        with self.assertRaisesRegex(ValueError, 'Retained summary'): v.verify(self.exports, RESULT, self.query(summary=summary))
        real = v.sha
        def fake(path):
            return '3' * 64 if str(path).endswith('BenchmarkAssets/player-source-s-09.png') else real(path)
        with mock.patch.object(v, 'sha', fake), self.assertRaisesRegex(ValueError, 'Executed bundled bytes'):
            v.verify(self.exports, RESULT, self.query())

    def testOfflineQueryUsesRetainedResultNoXcrun(self):
        with mock.patch.object(v.subprocess, 'check_output', side_effect=AssertionError('xcrun used')):
            report = v.verify(self.exports, RESULT, v.offline_query)
        self.assertEqual(report['captures'], 76)

    def testRejectsRootContactAndSegmentNumericMutation(self):
        def root(r):
            row = self.samples(r, 'half', 'distance-phase')[20]; row['projectedRoot'][0] += 0.01
        self.mutate(root, 'Projected root')
        def whole(r):
            row = self.samples(r, 'quarter', 'fixed-time')[40]; row['snapshotWhole'][1] += 1
            row['q8MinusSnapshot'][1] -= 1
        self.mutate(whole, 'quantization|Projected root')
        def contact(r):
            row = next(x for x in self.samples(r, 'full', 'fixed-time') if x['contacts'])
            side = next(iter(row['contacts'])); row['contacts'][side][1] += 0.5
        self.mutate(contact, 'Contact point')
        def span(r):
            seg = next(x for x in r['records'] if x['kind'] == 'segment' and x['trace'] == 'quarter')
            seg['nativeSceneSpanLogical'] -= 0.5
        self.mutate(span, 'Segment span')
        def census(r):
            seg = next(x for x in r['records'] if x['kind'] == 'segment' and x['trace'] == 'half')
            seg['samples'] += 1
        self.mutate(census, 'Segment census')
        def swap(r):
            segs = [x for x in r['records'] if x['kind'] == 'segment' and x['trace'] == 'full' and x['policy'] == 'fixed-time']
            segs[0]['side'], segs[1]['side'] = segs[1]['side'], segs[0]['side']
        self.mutate(swap, 'Segment census')

    def testRejectsSourceHashMutation(self):
        real = v.sha
        def fake(path):
            return '0' * 64 if str(path).endswith('player-source-s-04.png') else real(path)
        with mock.patch.object(v, 'sha', fake), self.assertRaisesRegex(ValueError, '5/13'): v.check_sources()
        def fake_candidate(path):
            return '1' * 64 if 'GroundContactAssets/player-groundcontact-candidate-06' in str(path) else real(path)
        with mock.patch.object(v, 'sha', fake_candidate), self.assertRaisesRegex(ValueError, 'Bundled candidate'): v.check_sources()
        def fake_trace(path):
            return '2' * 64 if str(path).endswith('player-groundcontact-core-traces.json') else real(path)
        with mock.patch.object(v, 'sha', fake_trace), self.assertRaisesRegex(ValueError, 'core traces'): v.check_sources()

    def mutate(self, change, pattern):
        records = copy.deepcopy(self.records); change(records)
        with self.assertRaisesRegex(ValueError, pattern): v.validate_records(records, self.traces, self.poses)

    def samples(self, records, trace, policy):
        return [r for r in records['records'] if r['kind'] == 'sample' and r['trace'] == trace and r['policy'] == policy]

    def testRejectsCountAndCensusMutation(self):
        self.mutate(lambda r: r['records'].pop(), 'Expected2400')
        self.mutate(lambda r: r['records'].append(dict(r['records'][-1])), '2400|116')
        self.mutate(lambda r: r['excludedInvalidSouthFacingDodgeOrStationaryTraces'].pop('dodge'), 'Excluded')
        self.mutate(lambda r: r.update(threshold=3.0), 'threshold')
        self.mutate(lambda r: r.update(status='DISPLAYED'), 'status')

    def testRejectsSelectionAndIdentityMutation(self):
        def distance(r):
            row = self.samples(r, 'quarter', 'distance-phase')[10]; row['frame'] = (row['frame'] + 1) % 16
            row['texturePath'] = f"groundcontact-{row['family']}-{row['frame']:02d}"
        self.mutate(distance, 'distance-phase selection mismatch')
        def fixed(r):
            row = self.samples(r, 'half', 'fixed-time')[5]; row['frame'] = (row['frame'] + 1) % 16
            row['texturePath'] = f"groundcontact-{row['family']}-{row['frame']:02d}"
        self.mutate(fixed, 'fixed-time selection mismatch')
        self.mutate(lambda r: self.samples(r, 'full', 'distance-phase')[3].update(texturePath='groundcontact-baseline-99'), 'Texture')
        self.mutate(lambda r: self.samples(r, 'full', 'distance-phase')[3].update(authoritativeRaw=[0, 0]), 'authoritative')
        self.mutate(lambda r: self.samples(r, 'half', 'distance-phase')[3].update(tick=999), 'tick')
        self.mutate(lambda r: self.samples(r, 'half', 'distance-phase')[3].update(contacts={}), 'contacts')
        self.mutate(lambda r: self.samples(r, 'half', 'distance-phase')[3].update(q8MinusSnapshot=[0, 0]), 'quantization')

    def testRejectsChangedUnchangedPairMutation(self):
        captures, _ = v.attachments(self.exports)
        temp = Path(tempfile.mkdtemp(dir=os.environ.get('JCODE_SCRATCH_DIR'))); self.addCleanup(shutil.rmtree, temp)
        mutated = dict(captures)
        unchanged = next(k for k in captures if '-baseline-' in k and int(k.rsplit('frame-', 1)[1]) not in v.CHANGED)
        target = temp / 'x.png'; shutil.copy(captures[unchanged], target)
        with Image.open(target) as im:
            im = im.convert('RGBA'); im.putpixel((0, 0), (255, 0, 0, 255)); im.save(target)
        mutated[unchanged] = target
        with self.assertRaisesRegex(ValueError, 'Pair difference'): v.image_facts(mutated)
        changed = next(k for k in captures if '-baseline-' in k and int(k.rsplit('frame-', 1)[1]) in v.CHANGED)
        mutated = dict(captures); mutated[changed] = captures[changed.replace('-baseline-', '-weight-transfer-')]
        with self.assertRaisesRegex(ValueError, 'Pair difference'): v.image_facts(mutated)
        blank = temp / 'blank.png'; Image.new('RGBA', (480, 330), (9, 9, 9, 255)).save(blank)
        with self.assertRaisesRegex(ValueError, 'Blank'): v.image_facts({**captures, changed: blank})
        small = temp / 'small.png'; Image.new('RGBA', (160, 110)).save(small)
        with self.assertRaisesRegex(ValueError, 'PNG160'): v.image_facts({**captures, changed: small})

if __name__ == '__main__':
    unittest.main(verbosity=2)
