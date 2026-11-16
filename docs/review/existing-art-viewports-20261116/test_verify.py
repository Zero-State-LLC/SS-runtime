"""Synthetic verifier regressions plus read-only retained actual0653 validation."""
import copy
import hashlib
import io
from PIL import Image
import struct
import unittest
import tempfile
import json
from pathlib import Path
import verify_export as v


def fixture():
    captures, plates = [], {}
    for name in sorted(v.EXPECTED):
        dimensions = [667, 375] if '-se-' in name else [844, 390]
        buffer = io.BytesIO()
        with Image.new('RGB', tuple(dimensions), color=(30, 40, 50)) as image:
            image.save(buffer, format='PNG')
        data = buffer.getvalue()
        plates[name] = data
        record = dict(attachment=name, pixels=dimensions, logicalSize=dimensions,
                      sha256=hashlib.sha256(data).hexdigest())
        if name.startswith('viewport-'):
            inset = name.startswith('viewport-inset-')
            reduced = name.endswith('xl-reduced')
            record.update(syntheticInsetsTLBR=[0,47,8,47] if inset else [0,0,0,0],
                          safeSize=[750,382] if inset else dimensions,
                          hudScale=1300 if reduced else 1000, reducedMotion=reduced,
                          hudChildCount=1, kind='GameScene-offscreen-aspectFit')
        else:
            record.update(kind='hosted-production-UpgradeSelectionView',
                          dynamicType='accessibility3' if name.endswith('ax3') else 'large',
                          requestedSize=dimensions, logicalSizeRole='requested-output-canvas-not-host',
                          hostViewBounds=[0,0,*dimensions], windowBounds=[0,0,*dimensions],
                          captureMapping='drawHierarchy at host bounds into requested-size canvas, clipped if larger, no resize')
        captures.append(record)
    return dict(schema='existing-art-viewports-001', captures=captures,
                resourceInventory=[dict(assetID='fixture', path='fixture.png', sha256='a'*64, bytes=1)],
                resourceScope='synthetic regression only',
                unsupported=['physical-device operation','coherent-source acceptance']), plates


class VerifierTests(unittest.TestCase):
    def test_valid_metadata(self):
        packet, plates = fixture()
        self.assertEqual(v.validate_packet(packet, plates)['captures'], 10)

    def test_missing_duplicate_hash_dimension_settings(self):
        for mutation in ('missing','duplicate','hash','dimension','settings','inventory'):
            with self.subTest(mutation=mutation):
                packet, plates = fixture()
                if mutation == 'missing': packet['captures'].pop()
                if mutation == 'duplicate': packet['captures'][0] = copy.deepcopy(packet['captures'][1])
                if mutation == 'hash': plates[next(iter(plates))] += b'changed'
                if mutation == 'dimension': packet['captures'][0]['pixels'] = [1,1]
                if mutation == 'settings':
                    next(c for c in packet['captures'] if c['attachment'].startswith('viewport-'))['hudScale'] = 42
                if mutation == 'inventory': packet['resourceInventory'] = []
                with self.assertRaises(ValueError): v.validate_packet(packet, plates)

    def test_retained_actual0653_and_gallery(self):
        root = Path(__file__).resolve().parent / 'capture-0653'
        summary = json.loads((root / 'summary.json').read_text())
        tree = json.loads((root / 'tests.json').read_text())
        report = v.verify(summary, tree, root / 'exports')
        self.assertEqual(report['captures'], 10)
        self.assertEqual(report['inventoryRecords'], 1030)
        self.assertTrue(all(c['requestedViewportObserved'] for c in report['hostedBounds']))
        for relative, digest in json.loads((root / 'files-sha256.json').read_text()).items():
            self.assertEqual(hashlib.sha256((root / relative).read_bytes()).hexdigest(), digest)
        page = (root / 'index.html').read_text()
        self.assertEqual(page.count('<img '), 10)
        self.assertIn('classList.toggle', page)
        self.assertIn('visual acceptance UNREVIEWED', page)

    def test_real_export_suffix_and_wrong_manifest_identity(self):
        packet, plates = fixture()
        summary = dict(result='Passed',totalTestCount=1,passedTests=1,failedTests=0,skippedTests=0,expectedFailures=0)
        tree = dict(testNodes=[dict(nodeType='Test Case',nodeIdentifier=v.TEST,result='Passed')])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            items = []
            for index, (name, data) in enumerate(plates.items()):
                filename = f'{index}.png'
                (root / filename).write_bytes(data)
                items.append(dict(exportedFileName=filename,
                    suggestedHumanReadableName=name+'_0_949E365E-2BFB-4D05-92C4-57C65ADEA4A6.png'))
            (root / 'record.json').write_text(json.dumps(packet))
            items.append(dict(exportedFileName='record.json', suggestedHumanReadableName=
                'existing-art-viewports-records_0_DB7AA347-25B2-4F5F-A0AB-912869D33E8D.json'))
            manifest = [dict(testIdentifier=v.TEST, attachments=items)]
            (root / 'manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(v.verify(summary, tree, root)['captures'], 10)
            manifest[0]['testIdentifier'] = 'Wrong/test()'
            (root / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): v.verify(summary, tree, root)

    def test_host_bounds_required_and_normalization_reported(self):
        packet, plates = fixture()
        host = next(c for c in packet['captures'] if c['attachment'].startswith('upgrade-reference-'))
        host['hostViewBounds'] = [0,0,852,393]
        host['windowBounds'] = [0,0,852,393]
        report = v.validate_packet(packet, plates)
        observed = next(c for c in report['hostedBounds'] if c['attachment'] == host['attachment'])
        self.assertFalse(observed['requestedViewportObserved'])
        self.assertEqual(observed['hostViewBounds'], [0,0,852,393])
        for field in ('hostViewBounds', 'windowBounds'):
            for invalid in (None, [0,0,0,390], [0,0,float('nan'),390]):
                with self.subTest(field=field, invalid=invalid):
                    bad = copy.deepcopy(packet)
                    next(c for c in bad['captures'] if c['attachment'] == host['attachment'])[field] = invalid
                    with self.assertRaises(ValueError): v.validate_packet(bad, plates)

    def test_truncated_png_rejected_even_with_updated_hash(self):
        packet, plates = fixture()
        name = packet['captures'][0]['attachment']
        plates[name] = plates[name][:24]
        packet['captures'][0]['sha256'] = hashlib.sha256(plates[name]).hexdigest()
        with self.assertRaises((ValueError, OSError)):
            v.validate_packet(packet, plates)

    def test_zero_failed_skipped_wrong_identity(self):
        good = dict(result='Passed',totalTestCount=1,passedTests=1,failedTests=0,skippedTests=0,expectedFailures=0)
        tree = dict(testNodes=[dict(nodeType='Test Case',nodeIdentifier=v.TEST,result='Passed')])
        v.validate_result(good, tree)
        for key, value in [('totalTestCount',0),('failedTests',1),('skippedTests',1),('expectedFailures',1)]:
            bad = dict(good, **{key:value})
            with self.assertRaises(ValueError): v.validate_result(bad, tree)
        tree['testNodes'][0]['nodeIdentifier'] = 'Wrong/test()'
        with self.assertRaises(ValueError): v.validate_result(good, tree)

if __name__ == '__main__': unittest.main(verbosity=2)
