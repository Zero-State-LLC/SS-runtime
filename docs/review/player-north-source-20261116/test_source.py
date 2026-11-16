import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image
import assemble

HERE = Path(__file__).resolve().parent
M = json.loads((HERE/'north-extension.json').read_text())

def image(path): return Image.open(path).convert('RGBA')
def equal(a,b): return a.size == b.size and a.tobytes() == b.tobytes()

class NorthSourceGuards(unittest.TestCase):
 def test_source_hashes_and_readonly_originals(self):
  p=M['provenance']
  for original, local, digest in [(p['sheet'],'source/revised-sheet.png',p['sheetSHA256']),(p['south'],'source/south-neutral-unchanged.png',p['southSHA256']),(M['master']['path'],'source/original-body-rig.json',M['master']['sha256'])]:
   self.assertEqual(assemble.sha(HERE/local),digest)
   if Path(original).exists(): self.assertEqual(assemble.sha(original),digest)
  self.assertEqual(assemble.sha(HERE/'source/metadata.json'),p['metadataSHA256'])
 def test_exact_rgba_component_identity(self):
  sheet=image(HERE/'source/revised-sheet.png')
  for p in M['parts']:
   part=image(HERE/'components'/f"{p['name']}.png")
   self.assertTrue(equal(part,sheet.crop(p['alphaBounds'])),p['name'])
   region=sheet.crop(p['region']); b=region.getchannel('A').getbbox()
   self.assertEqual(p['alphaBounds'],[b[0]+p['region'][0],b[1]+p['region'][1],b[2]+p['region'][0],b[3]+p['region'][1]])
   self.assertGreater(p['alphaBounds'][0],550) # excludes flattened left guide
 def test_uniform_scale_translation_only(self):
  for p in M['parts']:
   part=image(HERE/'components'/f"{p['name']}.png")
   self.assertGreater(p['uniformScale'],0)
   size=tuple(round(v*p['uniformScale']) for v in part.size)
   layer=Image.new('RGBA',(384,416)); layer.paste(part.resize(size,Image.Resampling.LANCZOS),p['translation'])
   self.assertTrue(equal(layer,image(HERE/'layers'/f"{p['name']}.png")),p['name'])
 def test_complete_unique_layer_composite(self):
  names=[p['name'] for p in M['parts']]
  self.assertEqual(len(names),13); self.assertEqual(len(set(names)),13)
  self.assertEqual(names,M['layerOrderBottomToTop'])
  out=Image.new('RGBA',(384,416))
  for n in names: out=Image.alpha_composite(out,image(HERE/'layers'/f'{n}.png'))
  self.assertTrue(equal(out,image(HERE/'north-neutral.png')))
  self.assertEqual(assemble.sha(HERE/'north-neutral.png'),M['outputSHA256'])
 def test_layer_hashes(self):
  for p in M['parts']:
   for folder,key in [('layers','layerSHA256'),('components','componentSHA256')]: self.assertEqual(assemble.sha(HERE/folder/f"{p['name']}.png"),p[key])
 def test_asymmetric_binding(self):
  parts={p['name']:p for p in M['parts']}
  rig=json.loads((HERE/'source/original-body-rig.json').read_text())
  for suffix in ['upper_arm','forearm_hand','thigh','shin_boot','coat_tail']:
   left,right=parts['left_'+suffix],parts['right_'+suffix]
   self.assertLess(left['translation'][0],192); self.assertGreater(right['translation'][0],192)
   self.assertTrue(left['bone'].startswith('left_')); self.assertTrue(right['bone'].startswith('right_'))
   self.assertIn(right['bone'],rig['bones']); self.assertNotEqual(left['componentSHA256'],right['componentSHA256'])
  self.assertEqual(parts['right_satchel']['bone'],'right_hip')
  self.assertGreater(parts['right_satchel']['translation'][0],192)
  self.assertEqual(M['anatomicalRight'],'screen-right')
 def test_registration_and_unchanged_south_comparison(self):
  self.assertEqual(M['canvas'],[384,416]); self.assertEqual(M['groundRoot'],[192,336])
  self.assertEqual(M['logicalRoot'],[32,56])
  pair=image(HERE/'south-north.png')
  self.assertTrue(equal(pair.crop((0,0,384,416)),image(HERE/'source/south-neutral-unchanged.png')))
  self.assertTrue(equal(pair.crop((384,0,768,416)),image(HERE/'north-neutral.png')))
  self.assertEqual(list(image(HERE/'north-neutral.png').getchannel('A').getbbox()),M['alphaBounds'])
 def test_transparent_gap_samples_not_rgb(self):
  alpha=image(HERE/'source/revised-sheet.png').getchannel('A')
  for xy in [(900,400),(900,600),(1100,100),(1400,200),(550,100)]: self.assertEqual(alpha.getpixel(xy),0,xy)
 def test_proposal_not_original_paint_or_admission(self):
  self.assertEqual(M['status'],'PROPOSED')
  self.assertTrue(M['provenance']['generatedHiddenSurfaces'])
  self.assertIn('NOT_ADMISSION',M['kind'])
  self.assertEqual(M['facing'],'north')
  self.assertEqual(M['outputSHA256'],'0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb')
  self.assertTrue(all(p['activeAttempt']=='01-uniform-0.4' and p['uniformScale']==.4 for p in M['parts']))
  self.assertTrue(equal(image(HERE/'north-neutral.png'),image(HERE/'attempts/01-uniform-0.4/north-neutral.png')))

if __name__=='__main__': unittest.main(verbosity=2)
