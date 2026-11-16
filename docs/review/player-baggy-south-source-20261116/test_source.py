"""Source guards for the baggy south neutral proposal."""
import hashlib, json, unittest
from pathlib import Path
import numpy as np
from PIL import Image
import assemble as A

H = A.HERE
M = json.loads((H / 'baggy-south.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arr(p):
    with Image.open(p) as image:
        return np.array(image.convert('RGBA'))


class Guards(unittest.TestCase):
    def test_provenance_hashes(self):
        p = M['provenance']
        for path, digest in [
            ('source/trouser-sheet.png', p['sheetSHA256']),
            ('source/metadata.json', p['metadataSHA256']),
            ('source/south-neutral-original.png', p['southSHA256']),
            ('source/north-baggy-reference.png', p['northReferenceSHA256']),
        ]:
            self.assertEqual(sha(H / path), digest)
        for n, h in p['originalUpperLayers'].items():
            self.assertEqual(sha(H / f'source/original-upper/{n}.png'), h)
        for s, h in p['originalBootLayers'].items():
            self.assertEqual(sha(H / f'source/original-boots/00-{s}.png'), h)
        inventory = json.loads((H.parent / 'player-all-release-source-20261116/artifacts/input-inventory.json').read_text())
        self.assertEqual(p['southSHA256'], inventory['SS-player-bounded-neutral/frames/00.png'])
        for n, digest in p['originalUpperLayers'].items():
            self.assertEqual(digest, inventory[f'SS-player-bounded-neutral/source/body-source/{n}.png'])
        for s, digest in p['originalBootLayers'].items():
            self.assertEqual(digest, inventory[f'SS-player-bounded-neutral/boot/frames/00-{s}.png'])

    def test_canvas_and_output(self):
        with Image.open(H / 'south-baggy-neutral.png') as out:
            self.assertEqual(out.size, (384, 416))
        self.assertEqual(sha(H / 'south-baggy-neutral.png'), M['outputSHA256'])

    def test_parts_are_exact_crops_with_uniform_scale(self):
        with Image.open(H / 'source/trouser-sheet.png') as source:
            sheet = source.convert('RGBA')
        self.assertEqual([p['name'] for p in M['parts']], [q[0] for q in A.PARTS])
        for p in M['parts']:
            self.assertTrue(np.array_equal(arr(H / 'components' / f"{p['name']}.png"),
                                           np.array(sheet.crop(tuple(p['sheetRegion'])))))
            w, h = sheet.crop(tuple(p['sheetRegion'])).size
            self.assertEqual(p['resampledSize'], [round(w * p['uniformScale']), round(h * p['uniformScale'])])
            self.assertEqual(sha(H / 'layers' / f"{p['name']}.png"), p['layerSHA256'])

    def test_anatomical_sides_and_patch(self):
        sides = {p['name']: p for p in M['parts']}
        # South view: anatomical right is screen left.
        self.assertLess(sides['right_thigh']['translation'][0], sides['left_thigh']['translation'][0])
        self.assertLess(sides['right_shin_kneepad']['translation'][0], sides['left_shin_kneepad']['translation'][0])
        # Patch (ochre, high R-B) present on left-thigh sheet crop, absent on right.
        def ochre(name):
            a = arr(H / 'components' / f'{name}.png').astype(int)
            return int(((a[..., 3] > 200) & (a[..., 0] - a[..., 2] > 40) & (a[..., 0] > 140)).sum())
        self.assertGreater(ochre('left_thigh'), 20 * max(1, ochre('right_thigh')))

    def test_retained_upper_and_boot_pixels_exact(self):
        out = arr(H / 'south-baggy-neutral.png'); src = arr(H / 'source/south-neutral-original.png')
        up = arr(H / 'layers/original_upper.png'); bt = arr(H / 'layers/original_boots.png')
        for layer, key in [(up, 'upperOpaquePixels'), (bt, 'bootPixels')]:
            m = (layer[..., 3] == 255) & (src[..., 3] == 255)
            self.assertEqual(int(m.sum()) if key == 'upperOpaquePixels' else int((layer[..., 3] > 0).sum()), M['retained'][key])
            self.assertTrue(np.array_equal(out[m], src[m]))
        b = bt[..., 3] > 0
        self.assertTrue(np.array_equal(out[b & (bt[..., 3] == 255)], src[b & (bt[..., 3] == 255)]))
        self.assertFalse(b[:A.BOOT_TOP].any())

    def test_no_old_leg_pixels(self):
        # Every opaque output pixel in the leg band comes from new parts, boots or upper layers.
        out = arr(H / 'south-baggy-neutral.png')
        cover = np.zeros(out.shape[:2], bool)
        for n in [p['name'] for p in M['parts']] + ['original_boots', 'original_upper']:
            cover |= arr(H / 'layers' / f'{n}.png')[..., 3] > 0
        self.assertFalse(((out[..., 3] > 0) & ~cover).any())

    def test_exact_layer_composition(self):
        canvas = Image.new('RGBA', A.SIZE)
        for name in M['layerOrderBottomToTop']:
            with Image.open(H / 'layers' / f'{name}.png') as layer:
                canvas.alpha_composite(layer.convert('RGBA'))
        self.assertTrue(np.array_equal(np.array(canvas), arr(H / 'south-baggy-neutral.png')))

    def test_original_layer_reconstruction(self):
        src = arr(H / 'source/south-neutral-original.png')
        upper = Image.new('RGBA', A.SIZE)
        for name in A.UPPER:
            with Image.open(H / 'source/original-upper' / f'{name}.png') as original:
                layer = Image.new('RGBA', A.SIZE)
                layer.paste(original.convert('RGBA'), (0, 0))
                upper.alpha_composite(layer)
        upper_pixels = np.array(upper)
        opaque = (upper_pixels[..., 3] == 255) & (src[..., 3] == 255)
        upper_pixels[opaque] = src[opaque]
        self.assertTrue(np.array_equal(upper_pixels, arr(H / 'layers/original_upper.png')))
        mask = np.zeros(A.SIZE[::-1], bool)
        for side in ('right', 'left'):
            mask |= arr(H / 'source/original-boots' / f'00-{side}.png')[..., 3] > 0
        mask[:A.BOOT_TOP] = False
        boots = np.zeros_like(src)
        boots[mask] = src[mask]
        self.assertTrue(np.array_equal(boots, arr(H / 'layers/original_boots.png')))

    def test_ground_root_and_bottom(self):
        out = arr(H / 'south-baggy-neutral.png'); src = arr(H / 'source/south-neutral-original.png')
        self.assertEqual(M['groundRoot'], [192, 336])
        self.assertEqual(np.where(out[..., 3].any(1))[0].max(), np.where(src[..., 3].any(1))[0].max())


if __name__ == '__main__':
    unittest.main(verbosity=2)
