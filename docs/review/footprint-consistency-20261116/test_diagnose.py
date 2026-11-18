import unittest
import diagnose


class DiagnosisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = diagnose.diagnose()
        cls.rows = {r['id']: r for r in cls.report['footprints']}

    def test_exact_straight_boundary_area(self):
        # Analytical rectangle/half-plane intersections, not renderer reuse.
        self.assertEqual(self.rows['solid-01-residential-west']['materialArea'],
                         dict(paving=128 * (896 - 600), curb=128 * 6, road=128 * (594 - 384)))
        self.assertEqual(self.rows['solid-04-civic-west']['materialArea'],
                         dict(paving=(800 - 736) * 384, curb=6 * 384, road=(928 - 806) * 384))
        self.assertEqual(self.rows['solid-05-civic-dais']['materialArea']['road'], 160 * 96)

    def test_kiosk_and_north_on_paving(self):
        for name in ('solid-02-residential-north', 'solid-03-transit-kiosk'):
            row = self.rows[name]
            self.assertEqual(row['materialArea']['paving'], row['sampledWorldArea'])

    def test_tree_inside_civic_footprint(self):
        tree = next(p for p in self.report['props'] if p['name'] == 'benchmark-prop-1')
        self.assertEqual(tree['worldRoot'], [858, 780])
        self.assertEqual(tree['insideSolids'], ['solid-04-civic-west'])

    def test_curved_corner_and_boundary_semantics(self):
        layout = self.report['groundLayout']
        self.assertEqual(diagnose.classify(800, 700, layout), 'paving')
        self.assertEqual(diagnose.classify(803, 700, layout), 'curb')
        self.assertEqual(diagnose.classify(807, 700, layout), 'road')
        self.assertEqual(diagnose.classify(799, 601, layout), 'road')
        self.assertEqual(diagnose.classify(752, 648, layout), 'paving')


if __name__ == '__main__':
    unittest.main(verbosity=2)
