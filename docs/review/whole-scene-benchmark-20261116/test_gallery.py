#!/usr/bin/env python3
"""Portable tests for the whole-scene gallery and coverage matrix. No browser or xcrun required."""
import hashlib
import re
import unittest
from pathlib import Path
import build_gallery as g
import verify_capture as v

class GalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        g.build()
        cls.html = (g.HERE / 'index.html').read_text(); cls.matrix = (g.HERE / 'coverage.md').read_text()

    def testAll36PlatesReachableAndRecordHashesPreserved(self):
        template = re.search(r'`capture/wholescene-\$\{arm\}-\$\{m\}-z\$\{z\}-\$\{s\}\.png`', self.html)
        self.assertIsNotNone(template)
        for option in ('ordinary', 'staged', '100', '125', '140', 'native', 'half', 'grayscale'):
            self.assertIn(f'>{option}' if option.isdigit() else f'value="{option}"', self.html)
        records = v.load(v.CAPTURE / 'wholescene-records.json')
        seen = 0
        for capture in records['captures']:
            for suffix, digest in capture['pngSHA256'].items():
                path = v.CAPTURE / f"{capture['name']}{suffix}.png"
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest); seen += 1
        self.assertEqual(seen, 36)

    def testOrdinaryPrimaryStagedSecondaryAndStatus(self):
        self.assertIn('<option value="ordinary" selected>ORDINARY (primary)', self.html)
        self.assertIn('STAGED (secondary)', self.html)
        self.assertIn('do not judge legibility from this view', self.html.lower())
        self.assertIn('HUD hidden (isHidden), Camera field hidden', self.html)
        self.assertIn('NOT A CORRECTION, NOT VISUAL ACCEPTANCE', self.html)
        for name, _ in g.UNSOLVED: self.assertIn(f'<b>{name}:</b>', self.html)
        for word in ('Building:</b> NOT SOLVED', 'Paving material:</b> NOT SOLVED', 'shadows:</b> ABSENT', 'HUD prominence:</b> OPEN', 'field prominence:</b> OPEN'):
            self.assertIn(word, self.html)
        self.assertNotIn('solved', self.html.replace('NOT SOLVED', '').lower().replace('unsolved', ''))

    def testFixedBenchmarkIsReadOnlyApprovedConcept(self):
        self.assertIn(g.BENCHMARK, self.html)
        self.assertEqual(hashlib.sha256((g.HERE / g.BENCHMARK).resolve().read_bytes()).hexdigest(), v.REFERENCE_SHA)
        self.assertIn('normalized reference', self.html); self.assertIn('different aspect, not identical framing', self.html)
        self.assertIn("grayscale(1)", self.html)

    def testDisplaySizesScrollAndContract(self):
        self.assertIn('native:[704,326],half:[352,163],grayscale:[704,326]', self.html)
        self.assertIn('.panel{overflow:auto', self.html); self.assertIn('body{overflow-x:hidden}', self.html)
        self.assertIn('../visual-acceptance-20261116/CONTRACT.md', self.html)
        self.assertTrue((g.HERE / '../visual-acceptance-20261116/CONTRACT.md').resolve().is_file())

    def testCoverageRowsHonest(self):
        required = ['Quiet', 'Dense legal', 'Occlusion: front/rear/corner', 'movement', 'release', 'facings', 'Camera integrity',
                    'field-off', 'Enemy roles', 'Combat effects', 'UI states', 'Screen sizes', 'Accessibility', 'Live cadence', 'Physical device']
        for word in required: self.assertIn(word, self.matrix)
        rows = [l for l in self.matrix.splitlines() if l.startswith('| ') and not l.startswith('| Row') and not l.startswith('|---')]
        self.assertEqual(len(rows), len(g.COVERAGE))
        for line, (name, captured, technical, path, note) in zip(rows, g.COVERAGE):
            self.assertIn('NOT ACCEPTED', line)
            if captured:
                self.assertTrue(path and (g.REVIEW / path).exists(), name)
            else:
                self.assertIn('NOT CAPTURED', line); self.assertIsNone(path); self.assertIsNone(technical)
        self.assertNotIn('| ACCEPTED', self.matrix)
        quiet_only = [r for r in g.COVERAGE if r[3] and r[3].startswith('whole-scene-benchmark')]
        self.assertEqual({r[0] for r in quiet_only}, {'Quiet street, control vs diagnostic', 'Camera field-off'})

    def testBuildRejectsMissingEvidence(self):
        original = g.COVERAGE
        try:
            g.COVERAGE = original + [('Fake', True, 'x', 'does-not-exist', '')]
            with self.assertRaises(AssertionError): g.build()
        finally:
            g.COVERAGE = original; g.build()

if __name__ == '__main__': unittest.main(verbosity=2)
