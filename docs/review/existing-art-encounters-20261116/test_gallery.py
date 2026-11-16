"""Synthetic gallery tests, never native evidence or a successful imported artifact."""
import unittest
from unittest.mock import patch

import build_gallery as g
import test_validator as fixtures


class GalleryTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.EvidenceReaderTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.packet, self.files = fixture.packet, fixture.files
        for row in self.packet['captures']:
            row.update(sceneWidth=704, sceneHeight=326)

    def test_output_uses_only_ledger_images_and_actual_labels(self):
        html = g.render(self.packet, self.files)
        self.assertEqual(html.count('<section>'), 2)
        self.assertEqual(html.count('data:image/png;base64,'), 4)
        self.assertIn('Tick 1 | tags: camera-integrity-3', html)
        self.assertIn('Tick 2 | tags: dense', html)
        self.assertIn('width="704" height="326"', html)
        self.assertIn('width="352" height="163"', html)
        self.assertIn('NOT A COHERENT BENCHMARK', html)
        self.assertIn('Not observed: ', html)
        self.assertIn('fieldOcclusion', html)
        self.assertIn('Grayscale inspection (display only)', html)
        self.assertNotIn('<script', html)

    def test_labels_are_escaped(self):
        self.packet['observed'] = ['<script>alert(1)</script>']
        html = g.render(self.packet, self.files)
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_changed_image_and_invalid_dimensions_are_red(self):
        self.packet['captures'][0]['sceneWidth'] = float('inf')
        with self.assertRaises(ValueError):
            g.render(self.packet, self.files)
        self.packet['captures'][0]['sceneWidth'] = 704
        self.files['existing-art-tick-1'].write_bytes(b'changed')
        with self.assertRaises(ValueError):
            g.render(self.packet, self.files)

    def test_loader_checks_native_result_before_loading_files(self):
        with patch.object(g.v, 'attachments') as attachments:
            with self.assertRaises(ValueError):
                g.load_verified('absent', 'absent', query=lambda path, kind: {})
            attachments.assert_not_called()

    def test_loader_runs_full_packet_validation(self):
        summary = dict(result='Passed', passedTests=1, failedTests=0, skippedTests=0, expectedFailures=0)
        tree = {'testNodes': [dict(nodeType='Test Case', nodeIdentifier=g.v.TEST, result='Passed')]}
        def query(path, kind):
            return summary if kind == 'summary' else tree
        with patch.object(g.v, 'attachments', return_value=self.files), \
                patch.object(g.v, 'load', return_value=self.packet), \
                patch.object(g.v, 'validate_packet', side_effect=ValueError('resource mismatch')) as validate:
            with self.assertRaisesRegex(ValueError, 'resource mismatch'):
                g.load_verified('exports', 'result', query=query)
            validate.assert_called_once_with(self.packet, self.files)


if __name__ == '__main__':
    unittest.main()
