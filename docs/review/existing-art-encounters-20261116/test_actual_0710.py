"""Regress retained real0710 v2 packet. These checks do not rerun native gameplay."""
import copy
from pathlib import Path
import unittest

import verify_capture as v
import build_gallery as g


class Actual0710Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parent / 'capture-0710'
        cls.files = v.attachments(cls.root / 'exports')
        cls.packet = v.load(cls.files['existing-art-encounter-records'])

    def test_exact_native_result_and_actual_packet(self):
        v.validate_result(v.load(self.root / 'native-summary.json'), v.load(self.root / 'native-tests.json'))
        result = v.validate_packet(self.packet, self.files)
        self.assertEqual(result['captures'], 9)
        self.assertEqual(result['resources'], 1073)
        self.assertEqual(result['notObserved'], ['playerDamaged', 'telegraphs'])
        self.assertEqual(result['status'], 'STATIC_EXISTING_ART_NOT_ACCEPTANCE')

    def test_actual_dense_has_player_two_nearby_enemies_and_projectile(self):
        dense = [row for row in self.packet['captures'] if 'dense' in row['tags']]
        self.assertEqual(len(dense), 1)
        self.assertEqual(dense[0]['tick'], 459)
        v.validate_framing(dense[0])
        included = [n for n in dense[0]['renderNodes'] if n['rootInCrop'] and n['boundsIntersectCrop'] and n['nodeVisible']]
        self.assertEqual({n['id'] for n in included if n['kind'] == 'enemy' and n['nearby']}, {10, 12})
        self.assertTrue(any(n['kind'] == 'player' for n in included))
        self.assertTrue(any(n['kind'] == 'projectile' and n['id'] == 27 for n in included))

    def test_actual_dense_cannot_regress_to_stale_or_hidden_framing(self):
        dense = next(row for row in self.packet['captures'] if 'dense' in row['tags'])
        for mutate in [lambda r: r.update(cameraX=352),
                       lambda r: r['crop'].update(x=0, y=0),
                       lambda r: r['renderNodes'][0].update(nodeVisible=False),
                       lambda r: r['renderNodes'].clear()]:
            row = copy.deepcopy(dense)
            mutate(row)
            with self.assertRaises(ValueError):
                v.validate_framing(row)

    def test_retained_gallery_rebuild_exact_and_scope_disclosed(self):
        actual = (self.root / 'gallery.html').read_text()
        self.assertEqual(g.render(self.packet, self.files), actual)
        self.assertIn('STAGED SNAPSHOT PLAYER-CENTER FRAMING, NOT LIVE CAMERA FOLLOW', actual)
        self.assertIn('NOT A COHERENT BENCHMARK', actual)
        self.assertEqual(actual.count('<section>'), 9)

    def test_actual_runner_session_loads_current_container(self):
        sessions = list((self.root / 'runner-diagnostics').rglob('Session-*.log'))
        self.assertEqual(len(sessions), 1)
        text = sessions[0].read_text()
        loading = [line for line in text.splitlines() if 'Loading test bundle at:' in line]
        self.assertEqual(len(loading), 1)
        self.assertIn('/Containers/Bundle/Application/5CF8FE91-EF42-44C2-9C5B-EDB5A248CF8E/', loading[0])
        self.assertNotIn('/Dead/', loading[0])


if __name__ == '__main__':
    unittest.main()
