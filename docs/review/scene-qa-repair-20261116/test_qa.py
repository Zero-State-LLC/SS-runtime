import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scene_qa_probe', HERE / 'qa.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


class PixelProbeTests(unittest.TestCase):
    def test_projected_root_is_not_zoomed_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source.png'
            Image.new('RGBA', (10, 10), (40, 50, 60, 255)).save(source)
            actor = {'size': [10, 10], 'anchor': [.5, 0], 'projectedRoot': [120, 100]}
            row = {'zoom': 1.4, 'centerWorld': [100, 100]}
            mask = q.actor_mask(actor, source, row, (704, 326))
            self.assertEqual(mask.getbbox(), (365, 149, 379, 163))

    def test_retained_v4_reproduces_both_defects(self):
        report = q.probe(q.OLD / 'native-capture-1040', q.OLD / 'native-inputs-v4')
        self.assertFalse(report['passed'])
        self.assertEqual([r['zoom'] for r in report['results']], [1, 1.25, 1.4])
        for row in report['results']:
            self.assertGreater(row['cameraCoveredByStoneFraction'], .8)
            self.assertFalse(row['cameraReadable'])
            self.assertGreater(row['playerExteriorPaleRatio'], .8)
            self.assertFalse(row['playerNoPaleHalo'])

    def test_claimed_depth_fix_without_new_pixels_still_fails(self):
        original = q.OLD / 'native-capture-1040'
        record = json.loads((original / 'source-scene-records.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            capture = Path(tmp)
            for row in record['captures']:
                if row['arm'] != 'candidate':
                    continue
                for actor in row['actors']:
                    if actor['name'] == 'sprite-camera-3':
                        actor['actualZ'] = 100  # Intentionally forged metadata, never native evidence.
                name = row['name'] + '-native.png'
                (capture / name).symlink_to(original / name)
            (capture / 'source-scene-records.json').write_text(json.dumps(record))
            report = q.probe(capture, q.OLD / 'native-inputs-v4')
            self.assertFalse(report['passed'])
            for row in report['results']:
                self.assertEqual(row['cameraCoveredByStoneFraction'], 0)
                self.assertFalse(row['cameraReadable'])


if __name__ == '__main__':
    unittest.main()
