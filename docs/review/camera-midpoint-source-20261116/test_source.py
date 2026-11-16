"""Source guards for the camera midpoint first samples. Uses only files copied into this packet."""
import hashlib, json, unittest
from pathlib import Path
import numpy as np
from PIL import Image

H = Path(__file__).resolve().parent
SRC = H / 'source'
APPROVED_PIN = '49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb'
R = json.loads((H / 'source-record.json').read_text())
A2 = H / 'attempts/02-midpoint-concept-extraction'
R2 = json.loads((A2 / 'source-record.json').read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def arr(p, mode='RGBA'):
    with Image.open(p) as im:
        return np.array(im.convert(mode))


def size(p):
    with Image.open(p) as im:
        return im.size


def visible(a):
    a = a.copy()
    a[a[..., 3] == 0] = 0
    return a


def silhouette(rgb, base_bottom, crop_top):
    from scipy import ndimage
    lum = rgb.mean(2); sat = rgb.max(2) - rgb.min(2)
    m = ndimage.binary_fill_holes(ndimage.binary_closing((lum < 45) | ((lum > 150) & (sat < 60)), iterations=3))
    m = ndimage.binary_opening(m, iterations=1)
    lab, n = ndimage.label(m)
    m = lab == (np.argmax(ndimage.sum(m, lab, range(1, n + 1))) + 1)
    m[base_bottom - crop_top + 1:] = False
    return m


class Attempt01(unittest.TestCase):
    def test_copied_inputs_match_record(self):
        p = R['provenance']
        self.assertEqual(sha(SRC / 'recovered-intact.png'), p['recoveredIntactSHA256'])
        self.assertEqual(sha(SRC / 'approved-concept.png'), p['conceptSHA256'])
        self.assertEqual(sha(SRC / 'midpoint-concept.png'), p['midpointConceptSHA256'])
        for k, h in p['otherStates'].items():
            self.assertEqual(sha(SRC / f'state-{k}.png'), h)

    def test_honest_label(self):
        self.assertEqual(R['provenance']['honestLabel'], 'GENERATED_PRIOR_CANDIDATE_RECOVERED_NOT_ORIGINAL_MASTER')
        self.assertIn('REJECTED', R['status'])

    def test_registration(self):
        self.assertEqual(size(H / 'camera-midpoint-intact.png'), (256, 384))
        self.assertEqual(R['registration']['logicalCanvas'], [64, 96])
        self.assertEqual(R['registration']['logicalGroundAnchor'], [32, 88])
        self.assertEqual(R['registration']['groundAnchorPixels'], [128, 352])  # 4 px per logical unit
        self.assertEqual(R['registration']['baseFootprint']['bottomOpaqueRow'], 351)

    def test_layers_partition_and_reconstruct_exactly(self):
        src = visible(arr(SRC / 'recovered-intact.png'))
        seen = np.zeros(src.shape[:2], bool)
        comp = np.zeros_like(src)
        for rec in R['layers']:
            p = H / 'layers' / f"{rec['name']}.png"
            la = arr(p)
            self.assertEqual(sha(p), rec['sha256'])
            m = la[..., 3] > 0
            self.assertFalse((seen & m).any(), rec['name'])
            self.assertTrue(np.array_equal(la[m], src[m]))
            seen |= m
            comp[m] = la[m]
        self.assertTrue(np.array_equal(comp, src))
        self.assertTrue(np.array_equal(arr(H / 'camera-midpoint-intact.png'), src))

    def test_complete_device_layers_nonempty(self):
        names = {l['name']: l['opaquePixels'] for l in R['layers']}
        self.assertEqual(set(names), {'base', 'pole', 'junction_box', 'arm', 'head'})
        self.assertTrue(all(v > 500 for v in names.values()))

    def test_integrity_contract_matches_copied_contract(self):
        c = R['integrityRequirements']
        contract = json.loads((SRC / 'camera-clip-contract.json').read_text())
        self.assertEqual(sha(SRC / 'clip-metadata-001.json'), contract['sha256'])
        self.assertEqual(contract['sha256'], '21f734ddaf228e99c3624b8c0d1cbc9a2af252cba1bf15f67986ec649f2daf26')
        full = json.loads((SRC / 'clip-metadata-001.json').read_text())
        expected_subset = [{'clipId': x['clipId'], 'frameIds': x['frameIds']}
                           for x in full['clips'] if x['actorRole'] == 'camera']
        self.assertEqual(contract['cameraClips'], expected_subset)
        counts = {x['clipId']: len(x['frameIds']) for x in contract['cameraClips']}
        names = {'operationalIdle': 'camera_operational_idle', 'hit': 'camera_hit',
                 'criticalEnter': 'camera_critical_enter', 'destroy': 'camera_destroy',
                 'fieldOff': 'camera_field_off', 'destroyedIdle': 'camera_destroyed_idle'}
        self.assertEqual(counts, {names[name]: count for name,count in c['clips'].items()})
        self.assertEqual(sum(counts.values()), 16)
        self.assertEqual(set(c['settled']), {'3', '2', '1', '0'})


class Attempt02(unittest.TestCase):
    def test_source_and_control_hashes(self):
        self.assertEqual(sha(SRC / 'midpoint-concept.png'), R2['source']['sha256'])
        self.assertEqual(sha(H / 'camera-midpoint-intact.png'), R2['control']['sha256'])
        self.assertEqual(sha(A2 / 'camera-midpoint-intact.png'), R2['outputSHA256'])
        self.assertIn('NOT_GENERATED', R2['honestLabel'])

    def test_cutout_is_exact_concept_rgb(self):
        cut = arr(A2 / 'concept-cutout.png')
        with Image.open(SRC / 'midpoint-concept.png') as im:
            src = np.array(im.convert('RGB').crop(tuple(R2['source']['crop'])))
        m = cut[..., 3] > 0
        self.assertTrue(np.array_equal(cut[m][:, :3], src[m]))
        self.assertTrue(np.array_equal(m, silhouette(src.astype(int), R2['source']['baseCentre'][1], R2['source']['crop'][1])))

    def test_uniform_scale_and_registration(self):
        t = R2['transform']
        w, h = size(A2 / 'concept-cutout.png')
        self.assertEqual(t['resampledSize'], [round(w * t['uniformScale']), round(h * t['uniformScale'])])
        self.assertEqual(size(A2 / 'camera-midpoint-intact.png'), (256, 384))
        self.assertEqual(R2['registration']['logicalGroundAnchor'], [32, 88])
        self.assertLessEqual(R2['registration']['opaqueRows'][1], 351)
        with Image.open(A2 / 'concept-cutout.png') as cut:
            transformed = Image.new('RGBA', (256, 384))
            transformed.alpha_composite(cut.convert('RGBA').resize(tuple(t['resampledSize']), Image.Resampling.LANCZOS), tuple(t['translation']))
        self.assertTrue(np.array_equal(visible(np.array(transformed)), arr(A2 / 'camera-midpoint-intact.png')))

    def test_layers_partition(self):
        a = arr(A2 / 'camera-midpoint-intact.png')
        seen = np.zeros(a.shape[:2], bool)
        for r in R2['layers']:
            self.assertEqual(sha(A2 / 'layers' / f"{r['name']}.png"), r['sha256'])
            la = arr(A2 / 'layers' / f"{r['name']}.png")
            m = la[..., 3] > 0
            self.assertFalse((seen & m).any())
            self.assertTrue(np.array_equal(la[m], a[m]))
            seen |= m
        self.assertTrue(np.array_equal(seen, a[..., 3] > 0))


class Attempt03(unittest.TestCase):
    O = H / 'attempts/03-approved-concept-extraction'

    def setUp(self):
        self.R = json.loads((self.O / 'source-record.json').read_text())

    def test_authority_is_approved_concept_only(self):
        self.assertEqual(self.R['source']['file'], 'source/approved-concept.png')
        self.assertEqual(sha(SRC / 'approved-concept.png'), self.R['source']['sha256'])
        self.assertNotIn('midpoint-concept', json.dumps(self.R['source']))
        self.assertIn('NOT_ACCEPTED', self.R['status'])
        self.assertEqual(sha(self.O / 'camera-intact.png'), self.R['outputSHA256'])

    def test_cutout_is_exact_approved_rgb(self):
        cut = arr(self.O / 'concept-cutout.png')
        with Image.open(SRC / 'approved-concept.png') as im:
            src = np.array(im.convert('RGB').crop(tuple(self.R['source']['crop'])))
        m = cut[..., 3] > 0
        self.assertTrue(np.array_equal(cut[m][:, :3], src[m]))
        self.assertTrue(np.array_equal(m, silhouette(src.astype(int), self.R['source']['baseCentre'][1], self.R['source']['crop'][1])))

    def test_output_is_uniform_transform_of_cutout(self):
        t = self.R['transform']
        with Image.open(self.O / 'concept-cutout.png') as cut:
            self.assertEqual(t['resampledSize'], [round(cut.width * t['uniformScale']), round(cut.height * t['uniformScale'])])
            canvas = Image.new('RGBA', (256, 384))
            canvas.alpha_composite(cut.convert('RGBA').resize(tuple(t['resampledSize']), Image.Resampling.LANCZOS), tuple(t['translation']))
        self.assertTrue(np.array_equal(visible(np.array(canvas)), arr(self.O / 'camera-intact.png')))
        self.assertEqual(self.R['registration']['logicalGroundAnchor'], [32, 88])
        self.assertLessEqual(self.R['measurements']['outputOpaqueRows'][1], 351)

    def test_contamination_is_reported(self):
        c = self.R['contamination']
        for k in ('outputLeafPixels', 'outputPavementLikePixels'):
            self.assertIsInstance(c[k], int)

    def test_pinned_approved_original(self):
        # Pinned independently of the mutable record: SS-specs docs/review/phase4/street-corner-approved-concept.png.
        self.assertEqual(sha(SRC / 'approved-concept.png'), APPROVED_PIN)
        self.assertEqual(self.R['source']['sha256'], APPROVED_PIN)

    def test_recomputed_contamination_and_rows(self):
        from scipy import ndimage
        a = arr(self.O / 'camera-intact.png').astype(int)
        op = a[..., 3] > 0
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        lum = (r + g + b) / 3
        sat = a[..., :3].max(2) - a[..., :3].min(2)
        leaf = op & (sat > 60) & (r > g) & (g > b) & (r - b > 60)
        edge = op & ~ndimage.binary_erosion(op, iterations=3)
        pave = edge & (lum >= 85) & (lum <= 140) & (sat < 20)
        self.assertEqual(int(leaf.sum()), self.R['contamination']['outputLeafPixels'])
        self.assertEqual(int(pave.sum()), self.R['contamination']['outputPavementLikePixels'])
        rows128 = np.where((a[..., 3] > 128).any(1))[0]
        rows0 = np.where(op.any(1))[0]
        self.assertEqual([int(rows128.min()), int(rows128.max())], self.R['measurements']['outputOpaqueRows'])
        self.assertEqual([int(rows0.min()), int(rows0.max())], self.R['measurements']['outputAnyAlphaRows'])
        # Ground anchor (32,88) logical = px (128,352): nothing opaque on or below the anchor row.
        self.assertFalse((a[352:, :, 3] > 128).any())
        self.assertTrue((a[351, :, 3] > 128).any())


class Statuses(unittest.TestCase):
    def test_rejections_recorded(self):
        self.assertIn('REJECTED', R['status'])
        self.assertIn('REJECTED', R2['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
