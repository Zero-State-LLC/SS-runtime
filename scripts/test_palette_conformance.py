#!/usr/bin/env python3
"""Self-test for palette_conformance.py: python3 scripts/test_palette_conformance.py"""
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import palette_conformance as pc  # noqa: E402


class PaletteConformanceTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)

    def tearDown(self):
        self.dir.cleanup()

    def plate(self, name, colour, size=(600, 300)):
        path = self.root / name
        Image.new("RGB", size, colour).save(path)
        return path

    def test_flat_palette_colour_is_measured_exactly(self):
        asphalt = pc.PALETTE_RGB["asphaltBlueGray"]
        result = pc.measure(self.plate("asphalt.png", asphalt))
        expected = 0.2126 * asphalt[0] + 0.7152 * asphalt[1] + 0.0722 * asphalt[2]
        self.assertAlmostEqual(result["meanLuminance"], round(expected, 1))
        self.assertEqual(result["meanChroma"], max(asphalt) - min(asphalt))
        self.assertEqual(result["paletteShares"], {"asphaltBlueGray": 100.0})

    def test_bright_saturated_plate_is_flagged_not_rejected(self):
        reference = pc.measure(self.plate("ref.png", (80, 85, 90)))
        bright = pc.measure(self.plate("bright.png", (230, 190, 120)))
        found = pc.flags(bright, reference, None)
        self.assertTrue(any("meanLuminance" in f for f in found))
        self.assertTrue(any("meanChroma" in f for f in found))

    def test_reference_is_within_its_own_band(self):
        reference = pc.measure(self.plate("ref.png", (80, 85, 90)))
        self.assertEqual(pc.flags(reference, reference, None), [])

    def test_civic_plaza_allowance_widens_only_the_upper_luminance_bound(self):
        reference = pc.measure(self.plate("ref.png", (80, 80, 80)))
        lighter = pc.measure(self.plate("light.png", (108, 108, 108)))
        self.assertTrue(pc.flags(lighter, reference, None))
        self.assertEqual(pc.flags(lighter, reference, "civicPlaza"), [])

    def test_excluded_hud_rows_are_not_measured(self):
        path = self.root / "hud.png"
        image = Image.new("RGB", (600, 300), (52, 61, 67))
        image.paste((255, 255, 255), (0, 0, 600, 100))
        image.save(path)
        self.assertEqual(pc.measure(path, exclude_top=100)["paletteShares"], {"asphaltBlueGray": 100.0})


if __name__ == "__main__":
    unittest.main()
