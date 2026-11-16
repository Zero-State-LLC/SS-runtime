"""Synthetic mutation tests for the independent coordinator audit. No native evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('preservation', HERE / 'verify_preservation.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class AuditTests(unittest.TestCase):
    def test_actual_crop_census_has_five_mesh_buildings(self):
        census = v.building_crop_census()
        for row in census['views']:
            self.assertEqual(len(row['possiblyVisible']), 5)
            self.assertEqual(len(row['entireCanvasOutside']), 9)
            self.assertIn('benchmark-building', [r['name'] for r in row['possiblyVisible']])

    def test_missing_protected_file_rejected(self):
        with tempfile.TemporaryDirectory() as d, patch.object(v, 'ROOT', Path(d)), patch.object(v.subprocess, 'check_output', return_value=b'100644 blob abc\tApp/f.swift\0'):
            with self.assertRaisesRegex(ValueError, 'Missing/aliased'):
                v.preserved()

    def test_changed_protected_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'App').mkdir()
            (root / 'App/f.swift').write_text('changed')
            with patch.object(v, 'ROOT', root), patch.object(v.subprocess, 'check_output', side_effect=[b'100644 blob abc\tApp/f.swift\0', b'def\n']):
                with self.assertRaisesRegex(ValueError, 'bytes changed'):
                    v.preserved()

    def test_empty_protected_census_rejected(self):
        with patch.object(v.subprocess, 'check_output', return_value=b''):
            with self.assertRaisesRegex(ValueError, 'Vacuous'):
                v.preserved()

    def pixel_fixture(self, root):
        old, new = root / 'v7', root / 'v8'
        old.mkdir()
        new.mkdir()
        for zoom in (100, 125, 140):
            for treatment in ('native', 'half', 'grayscale'):
                im = Image.new('RGBA', (4, 3), (22, 33, 44, 255))
                im.save(old / f'source-scene-candidate-ordinary-z{zoom}-{treatment}.png')
                im.save(new / f'source-scene-control-ordinary-z{zoom}-{treatment}.png')
        return old, new

    def test_exact_synthetic_pixels_pass(self):
        with tempfile.TemporaryDirectory() as d:
            old, new = self.pixel_fixture(Path(d))
            with patch.object(v, 'V7', old), patch.object(v, 'V8', new):
                self.assertEqual(len(v.baseline_pixels()), 9)

    def test_single_pixel_drift_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            old, new = self.pixel_fixture(Path(d))
            p = new / 'source-scene-control-ordinary-z125-half.png'
            with Image.open(p) as image:
                im = image.copy()
            im.putpixel((0, 0), (22, 33, 45, 255))
            im.save(p)
            with patch.object(v, 'V7', old), patch.object(v, 'V8', new):
                with self.assertRaisesRegex(ValueError, 'RGBA drift'):
                    v.baseline_pixels()

    def test_missing_actual_capture_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            old, new = self.pixel_fixture(Path(d))
            (new / 'source-scene-control-ordinary-z140-grayscale.png').unlink()
            with patch.object(v, 'V7', old), patch.object(v, 'V8', new):
                with self.assertRaises(FileNotFoundError):
                    v.baseline_pixels()


if __name__ == '__main__':
    unittest.main()
