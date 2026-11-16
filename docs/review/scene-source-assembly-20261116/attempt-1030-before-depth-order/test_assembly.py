"""SYNTHETIC FIXTURES ONLY. Tests do not establish visual/owner/native acceptance."""
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from PIL import Image
import assemble as a

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='SYNTHETIC-scene-', dir=os.environ.get('JCODE_SCRATCH_DIR'))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        # Synthetic Git index only. No commits, identity changes, or real repo writes.
        pixels = io.BytesIO()
        Image.new('RGBA', (8, 12), (40, 100, 200, 255)).save(pixels, format='PNG')
        (self.root / 'SYNTHETIC.png').write_bytes(pixels.getvalue())
        (self.root / 'SYNTHETIC-review.txt').write_text('SYNTHETIC coordinator recommendation fixture. NOT acceptance evidence.\n')
        self.git('add', 'SYNTHETIC.png', 'SYNTHETIC-review.txt')
        self.m = {'schema': a.SCHEMA, 'evidenceKind': 'OFFLINE_REVIEW_ONLY',
                  'gameplayAuthority': 'NONE_COLLISION_AND_FIELDS_UNCHANGED',
                  'projection': 'D108_X_MINUS_Y_Y_PLUS_X_HALF', 'canvasPixels': [704, 352],
                  'viewCenterWorld': [0, 0], 'pixelsPerWorldUnit': 1, 'sources': []}
        for role in sorted(a.ROLES):
            reg = {'canvasPixels': [8, 12], 'rootPixelsTopLeft': [4, 10],
                   'worldPosition': [0, 0], 'drawSizeWorld': [4, 6],
                   'kind': 'ground' if role == 'paving' else 'upright',
                   'coordinates': 'WORLD_X_RIGHT_Y_UP_SOURCE_TOP_LEFT'}
            self.m['sources'].append({'role': role, 'status': 'recommended',
                'image': self.record('SYNTHETIC.png'), 'registration': reg,
                'recommendation': {'reviewerRole': 'coordinator', 'decision': 'recommended',
                    'scope': 'bounded-material-layout' if role == 'paving' else 'isolated-ordinary-scene',
                    'sourceSHA256': self.record('SYNTHETIC.png')['sha256'],
                    'registrationSHA256': a.digest(a.canonical(reg)), 'evidence': self.record('SYNTHETIC-review.txt')}})

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)

    def record(self, name):
        return {'path': name, 'sha256': a.digest((self.root / name).read_bytes())}

    def rejected(self, message=None):
        with self.assertRaisesRegex((a.Invalid, OSError), message or '.'):
            a.render(self.m, self.root, self.root / 'SYNTHETIC-output.svg')
        self.assertFalse((self.root / 'SYNTHETIC-output.svg').exists())

    def test_synthetic_recommendation_not_owner_acceptance(self):
        self.assertEqual(a.validate(self.m, self.root)[0], [])
        output = self.root / 'SYNTHETIC-output.svg'
        a.render(self.m, self.root, output)
        text = output.read_text()
        self.assertIn(a.LABEL, text)
        self.assertEqual(text.count('data:image/png;base64,'), 4)
        self.assertNotIn('SYNTHETIC.png', text)  # no external runtime image fetch
        self.assertEqual(len(ET.fromstring(text).findall('{http://www.w3.org/2000/svg}image')), 4)

    def test_missing_recommendation(self):
        self.m['sources'][0]['recommendation'] = None
        self.rejected('Missing coordinator')

    def test_owner_acceptance_is_not_recommendation(self):
        self.m['sources'][0]['recommendation']['reviewerRole'] = 'owner'
        self.rejected('Coordinator recommendation required')

    def test_rejected_and_pending_never_render(self):
        original = copy.deepcopy(self.m)
        for state in ('pending', 'rejected'):
            self.m = copy.deepcopy(original)
            s = self.m['sources'][0]
            s.update(status=state, image=None, registration=None, recommendation=None, reason='SYNTHETIC blocked input')
            self.rejected('BLOCKED')

    def test_rejected_cannot_smuggle_image(self):
        self.m['sources'][0]['status'] = 'rejected'
        self.rejected('must not carry admitted art')

    def test_missing_required_role_and_duplicate_role(self):
        original = copy.deepcopy(self.m)
        self.m['sources'].pop()
        self.rejected('Exactly')
        self.m = original
        self.m['sources'][0]['role'] = self.m['sources'][1]['role']
        self.rejected('Exactly')

    def test_missing_dependency(self):
        (self.root / 'SYNTHETIC.png').unlink()
        self.rejected('Missing dependency')

    def test_untracked_existing_dependency(self):
        self.git('rm', '--cached', 'SYNTHETIC.png')
        self.rejected('Untracked')

    def test_mutated_source_bytes(self):
        (self.root / 'SYNTHETIC.png').write_bytes(b'changed')
        self.rejected('hash mismatch')

    def test_mutated_recommendation_evidence(self):
        (self.root / 'SYNTHETIC-review.txt').write_text('changed verdict')
        self.rejected('hash mismatch')

    def test_missing_untracked_recommendation_evidence(self):
        self.git('rm', '--cached', 'SYNTHETIC-review.txt')
        self.rejected('Untracked')

    def test_path_escape_aliases_and_absolute(self):
        for name in ('../escape.png', '/escape.png', 'x/../../escape.png', './SYNTHETIC.png', 'x//y', 'x\\y'):
            with self.subTest(name=name), self.assertRaises(a.Invalid):
                a.safe(self.root, name)

    def test_outward_and_internal_symlinks(self):
        for target in (self.root.parent, self.root):
            link = self.root / 'alias'
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(a.Invalid):
                a.safe(self.root, 'alias/SYNTHETIC.png')
            link.unlink()

    def test_root_alias_is_allowed(self):
        alias = self.root / 'root-alias'
        alias.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(a.validate(self.m, alias)[0], [])

    def test_missing_registration_and_fields(self):
        original = copy.deepcopy(self.m)
        for key in ('canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld', 'kind', 'coordinates'):
            self.m = copy.deepcopy(original)
            del self.m['sources'][0]['registration'][key]
            self.rejected()

    def test_stale_registration_recommendation(self):
        self.m['sources'][0]['registration']['worldPosition'][0] = 1
        self.rejected('Stale recommendation registration')

    def test_stale_source_recommendation(self):
        self.m['sources'][0]['recommendation']['sourceSHA256'] = '0' * 64
        self.rejected('Stale recommendation source')

    def test_invalid_geometry(self):
        original = copy.deepcopy(self.m)
        for key, value in (('rootPixelsTopLeft', [-1, 2]), ('rootPixelsTopLeft', [9, 2]),
                           ('drawSizeWorld', [0, 1]), ('worldPosition', [float('nan'), 0]),
                           ('worldPosition', [True, 0]), ('canvasPixels', [1, 2])):
            self.m = copy.deepcopy(original)
            self.m['sources'][0]['registration'][key] = value
            self.rejected()

    def test_unknown_version_and_gameplay_claim(self):
        original = copy.deepcopy(self.m)
        for key, value in (('schema', 'future'), ('gameplayAuthority', 'collision-from-art'), ('evidenceKind', 'NATIVE')):
            self.m = copy.deepcopy(original)
            self.m[key] = value
            self.rejected()

    def test_projection_and_upright_anchor(self):
        self.assertEqual(a.project([0, 0]), (0, 0))
        self.assertAlmostEqual(a.project([2, 0])[0], 2 ** .5)
        out = self.root / 'SYNTHETIC-output.svg'
        a.render(self.m, self.root, out)
        images = ET.fromstring(out.read_text()).findall('{http://www.w3.org/2000/svg}image')
        self.assertEqual(images[1].attrib['transform'], 'matrix(0.5 0 0 0.5 350.0 171.0)')
        ground = [float(v) for v in images[0].attrib['transform'][7:-1].split()]
        aa, b, c, d, tx, ty = ground
        self.assertAlmostEqual(aa * 4 + c * 10 + tx, 352)
        self.assertAlmostEqual(b * 4 + d * 10 + ty, 176)
        self.assertLess(b, 0)
        self.assertGreater(d, 0)

    def test_existing_output_is_preserved(self):
        out = self.root / 'SYNTHETIC-output.svg'
        out.write_text('prior evidence')
        with self.assertRaises(FileExistsError):
            a.render(self.m, self.root, out)
        self.assertEqual(out.read_text(), 'prior evidence')

    def test_real_manifest_blocked_and_portable_export(self):
        # Preserve the actual pre-binding pending state as a historical regression.
        m = json.loads((HERE / 'assembly-pending-v2.json').read_text())
        blockers, deps = a.validate(m, REPO)
        self.assertEqual([x.split(':')[0] for x in blockers], ['camera', 'player', 'stone'])
        out = self.root / 'real-blocked.svg'
        with self.assertRaisesRegex(a.Invalid, 'BLOCKED'):
            a.render(m, REPO, out)
        self.assertFalse(out.exists())
        export = self.root / 'portable'
        a.export_packet(m, REPO, export)
        self.assertEqual(a.validate(m, export)[0], blockers)
        proc = subprocess.run([os.sys.executable, '-B', str(export / 'assemble.py'), '--root', str(export)], cwd=export, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['status'], 'BLOCKED_NO_SCENE')
        self.assertFalse(list(export.glob('*.svg')))
        (export / deps[0]['path']).unlink()
        with self.assertRaisesRegex(a.Invalid, 'Missing dependency'):
            a.validate(m, export)

    def test_final_recommended_bindings_and_portability(self):
        # Real source validation, not native or visual acceptance evidence.
        m = json.loads((HERE / 'assembly.json').read_text())
        self.assertEqual(a.validate(m, REPO)[0], [])
        sources = {s['role']: s for s in m['sources']}
        expected = {
            'camera': ([204, 450], [58, 427], [496, 672], [204*96/418, 450*96/418]),
            'player': ([384, 416], [192, 336], [736, 654], [64, 416/6]),
            'stone': ([1000, 1200], [500, 1160], [512, 640], [200, 240]),
        }
        for role, values in expected.items():
            source = sources[role]
            self.assertEqual(source['status'], 'recommended')
            for key, value in zip(('canvasPixels', 'rootPixelsTopLeft', 'worldPosition', 'drawSizeWorld'), values):
                self.assertEqual(source['registration'][key], value)
            self.assertEqual(source['recommendation']['scope'], 'isolated-ordinary-scene')
        self.assertTrue(sources['camera']['image']['path'].endswith('/padded-final/final/camera-master.png'))
        self.assertTrue(sources['player']['image']['path'].endswith('/canonical-identity-02/south-neutral.png'))
        self.assertTrue(sources['stone']['image']['path'].endswith('/output/preview-alpha.png'))
        placement = json.loads((HERE / 'authoritative-placement-1014.json').read_text())
        self.assertEqual(placement['status'], 'AUTHORITATIVE_SEED1_PLACEMENT_ONLY_NOT_SCENE_EVIDENCE')
        self.assertEqual((placement['seed'], placement['tick']), (1, 0))
        self.assertEqual(placement['authorityBefore'], placement['authorityAfter'])
        selected = [c for c in placement['cameras'] if c['rootWorld'] == sources['camera']['registration']['worldPosition']]
        self.assertEqual(len(selected), 1)
        self.assertEqual((selected[0]['id'], selected[0]['integrity'], selected[0]['fieldVisible']), (3, 3, True))
        solid = next(s for s in placement['solids'] if s['id'] == 'solid-03-transit-kiosk')
        self.assertEqual(solid['minWorld'], sources['stone']['registration']['worldPosition'])
        self.assertEqual(solid['maxWorld'], [640, 768])
        self.assertEqual(placement['playerRootWorld'], [160, 192])
        self.assertNotEqual(placement['playerRootWorld'], sources['player']['registration']['worldPosition'])
        export = self.root / 'real-bound-portable'
        a.export_packet(m, REPO, export)
        self.assertEqual(a.validate(m, export)[0], [])
        self.assertFalse(list(export.glob('*.svg')))

    def test_export_receipt_cannot_admit_unlisted_file(self):
        m = json.loads((HERE / 'assembly.json').read_text())
        export = self.root / 'portable'
        a.export_packet(m, REPO, export)
        receipt_path = export / 'tracked-inputs.json'
        receipt = json.loads(receipt_path.read_text())
        del receipt['files'][m['sources'][0]['image']['path']]
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(a.Invalid, 'Untracked'):
            a.validate(m, export)

    def test_synthetic_standalone_render_and_receipt_mutation(self):
        standalone = self.root / 'SYNTHETIC-standalone'
        standalone.mkdir()
        files = {}
        for name in ('SYNTHETIC.png', 'SYNTHETIC-review.txt'):
            data = (self.root / name).read_bytes()
            (standalone / name).write_bytes(data)
            files[name] = a.digest(data)
        # All-zero origin is a labeled test fixture, never actual Git provenance.
        receipt = {'schema': 'tracked-scene-inputs-001', 'gitHead': '0' * 40,
                   'fixture': 'SYNTHETIC_NOT_PROVENANCE', 'files': files}
        path = standalone / 'tracked-inputs.json'
        path.write_text(json.dumps(receipt))
        output = standalone / 'SYNTHETIC-output.svg'
        a.render(self.m, standalone, output)
        self.assertIn(a.LABEL, output.read_text())
        receipt['files']['SYNTHETIC.png'] = 'f' * 64
        path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(a.Invalid, 'Export receipt mismatch'):
            a.validate(self.m, standalone)

    def test_wrong_recommendation_scope_and_decision(self):
        original = copy.deepcopy(self.m)
        for key, value in (('scope', 'production'), ('decision', 'rejected')):
            self.m = copy.deepcopy(original)
            self.m['sources'][0]['recommendation'][key] = value
            self.rejected()


if __name__ == '__main__':
    unittest.main(verbosity=2)
