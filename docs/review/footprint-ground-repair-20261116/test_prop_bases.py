"""Independent retained prop-base checks, with synthetic mutation cases."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prop_bases', HERE / 'verify_prop_bases.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class PropBaseTests(unittest.TestCase):
    def test_entire_source_regions_have_clearance(self):
        result = v.verify()
        self.assertEqual(len(result['props']), 2)
        self.assertEqual(sum(p['testedSourceSamples'] for p in result['props']), 124200)
        self.assertTrue(all(p['minimumSolidClearanceWorld'] > 0 for p in result['props']))

    def test_original_tree_root_rejected(self):
        plan = json.loads((HERE / 'plan/plan.json').read_text())
        plan['props'][1]['worldRoot'] = [858, 780]
        with patch.object(v.json, 'loads', return_value=plan):
            with self.assertRaisesRegex(ValueError, 'intersects solid'):
                v.verify()

    def test_road_root_rejected(self):
        plan = json.loads((HERE / 'plan/plan.json').read_text())
        plan['props'][0]['worldRoot'] = [700, 300]
        with patch.object(v.json, 'loads', return_value=plan):
            with self.assertRaisesRegex(ValueError, 'not entirely on sidewalk'):
                v.verify()


if __name__ == '__main__':
    unittest.main()
