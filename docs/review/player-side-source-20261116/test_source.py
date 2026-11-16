import json, os, subprocess, sys, unittest
from pathlib import Path
from PIL import Image
import assemble

HERE = Path(__file__).resolve().parent
SIDES = ('east', 'west')
def load(s): return json.loads((HERE / s / f'{s}-extension.json').read_text())
def image(p):
  with Image.open(p) as im: return im.convert('RGBA')
def equal(a, b): return a.size == b.size and a.tobytes() == b.tobytes()

OUTPUTS = {'east': '4be91d1db958938de2fbbc403279345ebfd2c45363beb0829bed2c35d20948af',
           'west': '9d06aa548271ed8249dd59087a8ea0d293d7b3dc9dad23cc0ee7d5526211b744'}

class SideSourceGuards(unittest.TestCase):
  def test_reproducible_build(self):
    subprocess.run([sys.executable, '-B', '-W', 'error::ResourceWarning', str(HERE / 'assemble.py')], check=True, capture_output=True)
    for s in SIDES:
      self.assertEqual(assemble.sha(HERE / s / f'{s}-neutral.png'), OUTPUTS[s])
      self.assertEqual(load(s)['outputSHA256'], OUTPUTS[s])

  def test_inputs_and_originals_unchanged(self):
    # Portable: packet-local copies against hard-coded immutable hashes.
    pinned = {k: v[0] for k, v in assemble.PINNED.items()}
    self.assertEqual(pinned['north-neutral-active.png'], '0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb')
    self.assertEqual(pinned['south-neutral-original.png'], '2076f61c8d3b92a49d842f16eb6a043662dda84953f549a77884344cc3f1cb8e')
    self.assertEqual(json.loads((HERE / 'inputs.json').read_text()), pinned)
    for name, digest in pinned.items(): self.assertEqual(assemble.sha(HERE / 'source' / name), digest, name)
    for s in SIDES:
      p = load(s)['provenance']
      self.assertEqual(p['sheetSHA256'], pinned[f'{s}-sheet.png'])
      self.assertEqual(p['metadataSHA256'], pinned[f'{s}-metadata.json'])

  @unittest.skipUnless(os.environ.get('SIDE_FULL_AUDIT') == '1', 'optional external-original audit')
  def test_external_originals_match_pins(self):
    for name, (digest, path) in assemble.PINNED.items(): self.assertEqual(assemble.sha(path), digest, str(path))

  def test_exact_component_identity_and_uniform_transform(self):
    for s in SIDES:
      sheet = image(HERE / 'source' / f'{s}-sheet.png')
      for p in load(s)['parts']:
        comp = image(HERE / s / 'components' / f"{p['name']}.png")
        self.assertTrue(equal(comp, sheet.crop(p['alphaBounds'])), p['name'])
        self.assertEqual(p['uniformScale'], 0.4)
        size = (round(comp.width * .4), round(comp.height * .4))
        layer = Image.new('RGBA', (384, 416)); layer.paste(comp.resize(size, Image.Resampling.LANCZOS), p['translation'])
        self.assertTrue(equal(layer, image(HERE / s / 'layers' / f"{p['name']}.png")), p['name'])
        self.assertEqual(assemble.sha(HERE / s / 'layers' / f"{p['name']}.png"), p['layerSHA256'])

  def test_complete_composite_no_duplicate_parts(self):
    for s in SIDES:
      m = load(s); names = m['layerOrderBottomToTop']
      self.assertEqual(len(names), 13); self.assertEqual(len(set(names)), 13)
      self.assertEqual(len({p['componentSHA256'] for p in m['parts']}), 13)
      out = Image.new('RGBA', (384, 416))
      for n in names: out = Image.alpha_composite(out, image(HERE / s / 'layers' / f'{n}.png'))
      self.assertTrue(equal(out, image(HERE / s / f'{s}-neutral.png')))

  def test_distinct_facings_not_mirrors(self):
    east, west = image(HERE / 'east/east-neutral.png'), image(HERE / 'west/west-neutral.png')
    self.assertFalse(equal(east, west))
    self.assertFalse(equal(east.transpose(Image.Transpose.FLIP_LEFT_RIGHT), west))
    self.assertNotEqual(load('east')['provenance']['sheetSHA256'], load('west')['provenance']['sheetSHA256'])
    eh = {p['componentSHA256'] for p in load('east')['parts']}; wh = {p['componentSHA256'] for p in load('west')['parts']}
    self.assertFalse(eh & wh)

  def test_anatomical_side_binding(self):
    for s, near, far in [('east', 'right', 'left'), ('west', 'left', 'right')]:
      m = load(s); parts = {p['name']: p for p in m['parts']}; order = m['layerOrderBottomToTop']
      self.assertEqual(m['nearAnatomicalSide'], near)
      for limb in ('thigh', 'shin_boot', 'upper_arm', 'forearm_hand', 'coat_tail'):
        n, f = f'near_{near}_{limb}', f'far_{far}_{limb}'
        self.assertEqual(parts[n]['bone'].split('_')[0], near); self.assertEqual(parts[f]['bone'].split('_')[0], far)
        self.assertGreater(order.index(n), order.index(f), f'{s} {limb}: near side must draw over far side')
      self.assertEqual(parts['right_satchel']['bone'], 'right_hip')
      # Satchel depth is a documented open limitation, not asserted here.

  def test_registration(self):
    for s in SIDES:
      m = load(s); b = m['alphaBounds']
      self.assertEqual(m['groundRoot'], [192, 336]); self.assertEqual(m['canvas'], [384, 416])
      self.assertLessEqual(abs(b[1] - 39), 2, s)          # hood top shared with south/north
      self.assertTrue(b[0] < 192 < b[2], s)               # root inside silhouette span
      self.assertGreater(b[3], 336)                        # boots may extend below anchor

  def test_gallery_strip_uses_unchanged_inputs(self):
    strip = image(HERE / 'four-facing-source.png')
    for i, p in enumerate([HERE / 'source/south-neutral-original.png', HERE / 'east/east-neutral.png', HERE / 'source/north-neutral-active.png', HERE / 'west/west-neutral.png']):
      self.assertTrue(equal(strip.crop((384 * i, 0, 384 * i + 384, 416)), image(p)), str(p))
    for n, size, mode in [('native', (256, 69), None), ('half', (128, 35), None), ('grayscale', (1536, 416), 'L')]:
      with Image.open(HERE / f'four-facing-{n}.png') as im:
        self.assertEqual(im.size, size)
        if mode: self.assertEqual(im.mode, mode)

  def test_proposal_labels(self):
    for s in SIDES:
      m = load(s)
      self.assertEqual(m['status'], 'PROPOSED'); self.assertIn('NOT_ADMISSION', m['kind'])
      self.assertTrue(m['provenance']['generatedHiddenSurfaces'])
      self.assertIn('not original master paint', m['provenance']['paintStatus'])

if __name__ == '__main__': unittest.main(verbosity=2)
