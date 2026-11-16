import json
import unittest
from PIL import Image
import build

class SourceTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((build.HERE / 'source-record.json').read_text())

    def test_pinned_sources(self):
        for name, expected in build.EXPECTED.items():
            self.assertEqual(build.digest(build.HERE / 'source' / name), expected)

    def test_no_acceptance_or_integration(self):
        for key in ['ownerAccepted', 'productionAdmitted', 'readyForNative', 'editableMasterComplete', 'stateExpansionAllowed']:
            self.assertIs(self.record[key], False)
        self.assertEqual(self.record['status'], 'COORDINATOR_REJECTED_SOURCE_PROPOSALS')

    def test_actual_metadata_not_requested_transparency(self):
        for index in [1, 2]:
            with Image.open(build.HERE / 'source' / f'proposal-{index:02}.png') as image:
                self.assertEqual(image.size, (1024, 1536))
                self.assertEqual(image.mode, 'RGB')
                item = self.record['sources'][index]
                self.assertEqual(list(build.proposal_bounds(image)), item['diagnosticCrop'])
                self.assertFalse(item['nativeAlpha'])
            meta = json.loads((build.HERE / 'source' / f'proposal-{index:02}-provider.json').read_text())
            self.assertEqual(meta['response_item']['background'], 'opaque')

    def test_preview_dimensions_and_equal_height(self):
        for name, size in [('same-height.png', (750,510)), ('same-height-gray.png',(750,510)), ('same-height-half.png',(375,255))]:
            with Image.open(build.HERE / 'review' / name) as image:
                self.assertEqual(image.size, size)
        for item in self.record['sources'][1:]:
            box = item['diagnosticCrop']
            self.assertAlmostEqual((box[3] - box[1]) * item['uniformPreviewScale'], 416)

    def test_empty_threshold_rejected(self):
        with self.assertRaisesRegex(ValueError, 'No device pixels'):
            build.proposal_bounds(Image.new('RGB', (4,4), 'white'))

if __name__ == '__main__':
    unittest.main()
