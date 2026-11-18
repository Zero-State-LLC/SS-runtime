"""East/west neutral first-sample source assembly. No image synthesis.

Detached generated components are cropped by actual alpha inside authored
extraction regions and placed by hand-authored canvas translations with one
uniform scale (0.4, same as the active north sample). The sheets' flat
assembled guides are not composited and are used only for visual reference.
No mirroring, rotation, warping or repainting.
"""
from pathlib import Path
import hashlib, json, shutil, sys
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
GEN = Path('/Users/appliedalchemylabs/.jcode/generated-images')
ORIG = Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs')
SOUTH = ORIG / 'SS-player-bounded-neutral/frames/00.png'
RIG = ORIG / 'SS-player-bounded-proportions/source/body-rig.json'
NORTH = HERE.parent / 'player-north-source-20261116/north-neutral.png'
SRC = HERE / 'source'
# Packet-local immutable inputs. Default builds read only these copies, so the
# packet is portable. External paths are provenance and optional refresh only.
PINNED = {
 'south-neutral-original.png': ('2076f61c8d3b92a49d842f16eb6a043662dda84953f549a77884344cc3f1cb8e', SOUTH),
 'original-body-rig.json': ('c1d53f25495c4e17bd3f1f4df1b0e0e87bd047872420625642a88b8cdc26530b', RIG),
 'north-neutral-active.png': ('0a6e15bd2aa8cc486dd14521b60680bed6a2dd0833707972850e65d7991f4fbb', NORTH),
 'east-sheet.png': ('2955723de7fece615ff951aa1df5f9f4fc04475b0bcd5a2d6faeeaea45202a01', GEN / '1794799249061-ig_07cd661172aa2162016afa765bdbe887d0b785d913c0ab2a20.png'),
 'east-metadata.json': ('f8b197a5e1e92060dd2c4087b71e8cc0c29238fb79d4d9af79babb850df2ef2a', GEN / '1794799249061-ig_07cd661172aa2162016afa765bdbe887d0b785d913c0ab2a20.json'),
 'west-sheet.png': ('78ea555dfb9d6ea207c141ae3642269f22653f88cc1e90ae5a7847cfee2c9a40', GEN / '1794799386977-ig_07cd661172aa2162016afa76e6fc2087d0a633b2f0fce6aa30.png'),
 'west-metadata.json': ('6b3835ef846bac43d2f7c5e7529da35b5c21c49473b96072a36dd2946524a99f', GEN / '1794799386977-ig_07cd661172aa2162016afa76e6fc2087d0a633b2f0fce6aa30.json'),
}
ROOT = (192, 336)
SCALE = 0.4

# East faces screen right, so the anatomical RIGHT side is toward the south
# viewer (near). West faces screen left, so anatomical LEFT is near.
# The satchel stays on the anatomical right hip: near side for east, far side
# (behind the torso) for west. The cloth patch thigh is anatomical left, as in
# the original south.
# Rows: name, authored extraction region (sheet px), canvas top-left, bone.
# Order is bottom-to-top draw order.
SIDES = {
 'east': dict(sheet='1794799249061-ig_07cd661172aa2162016afa765bdbe887d0b785d913c0ab2a20',
   screenForward='right', near='right', parts=[
   ('far_left_forearm_hand', (1175, 309, 1320, 525), (190, 168), 'left_elbow'),
   ('far_left_upper_arm', (1175, 55, 1320, 309), (184, 104), 'left_shoulder'),
   ('right_satchel', (1240, 540, 1430, 725), (130, 172), 'right_hip'),
   ('far_left_coat_tail', (1060, 520, 1230, 745), (168, 196), 'left_hip'),
   ('far_left_shin_boot', (1100, 740, 1260, 1015), (184, 262), 'left_knee'),
   ('far_left_thigh', (690, 725, 835, 970), (182, 220), 'left_hip'),
   ('near_right_shin_boot', (900, 740, 1070, 1015), (166, 258), 'right_knee'),
   ('near_right_thigh', (535, 725, 680, 970), (168, 220), 'right_hip'),
   ('torso_coat_equipment', (580, 265, 800, 555), (152, 101), 'torso'),
   ('near_right_coat_tail', (840, 520, 1010, 745), (146, 196), 'right_hip'),
   ('near_right_upper_arm', (900, 55, 1060, 305), (162, 104), 'right_shoulder'),
   ('near_right_forearm_hand', (900, 305, 1040, 525), (174, 170), 'right_elbow'),
   ('hood', (580, 10, 840, 266), (148, 39), 'head')]),
 'west': dict(sheet='1794799386977-ig_07cd661172aa2162016afa76e6fc2087d0a633b2f0fce6aa30',
   screenForward='left', near='left', parts=[
   ('right_satchel', (1300, 535, 1485, 730), (196, 176), 'right_hip'),
   ('far_right_forearm_hand', (1170, 324, 1300, 528), (152, 168), 'right_elbow'),
   ('far_right_upper_arm', (1170, 80, 1310, 324), (150, 104), 'right_shoulder'),
   ('far_right_coat_tail', (1105, 528, 1300, 740), (166, 196), 'right_hip'),
   ('far_right_shin_boot', (1105, 740, 1275, 1000), (150, 262), 'right_knee'),
   ('far_right_thigh', (560, 700, 700, 955), (156, 220), 'right_hip'),
   ('near_left_shin_boot', (880, 740, 1055, 1000), (168, 258), 'left_knee'),
   ('near_left_thigh', (705, 700, 845, 955), (170, 220), 'left_hip'),
   ('torso_coat_equipment', (585, 260, 830, 600), (146, 101), 'torso'),
   ('near_left_coat_tail', (840, 520, 1015, 745), (180, 196), 'left_hip'),
   ('near_left_upper_arm', (910, 80, 1070, 324), (172, 104), 'left_shoulder'),
   ('near_left_forearm_hand', (910, 324, 1070, 531), (168, 170), 'left_elbow'),
   ('hood', (585, 10, 830, 260), (146, 39), 'head')]),
}
# Regions where neighbouring components touch with a thin opaque bridge and
# are separated by a straight authored cut row rather than an alpha gap.
CUT_SPLITS = {
 'east': ['far_left_upper_arm/far_left_forearm_hand at y309 (4 opaque px)'],
 'west': ['hood/torso_coat_equipment at y260 (37 opaque px)',
          'near_left_upper_arm/near_left_forearm_hand at y324 (10 opaque px)',
          'far_right_forearm_hand/far_right_coat_tail at y528 (8 opaque px)'],
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def component(sheet, region):
  crop = sheet.crop(region); b = crop.getchannel('A').getbbox(); assert b, region
  return [b[0] + region[0], b[1] + region[1], b[2] + region[0], b[3] + region[1]]

def build_side(side, cfg):
  out = HERE / side
  for d in ('components', 'layers'): (out / d).mkdir(parents=True, exist_ok=True)
  src = GEN / (cfg['sheet'] + '.png')  # provenance path only
  local = SRC / f'{side}-sheet.png'
  with Image.open(local) as im: sheet = im.convert('RGBA')
  canvas = Image.new('RGBA', (384, 416)); entries = []
  for name, region, xy, bone in cfg['parts']:
    bounds = component(sheet, region); part = sheet.crop(bounds)
    part.save(out / 'components' / f'{name}.png')
    size = (round(part.width * SCALE), round(part.height * SCALE))
    layer = Image.new('RGBA', canvas.size); layer.paste(part.resize(size, Image.Resampling.LANCZOS), xy)
    layer.save(out / 'layers' / f'{name}.png'); canvas = Image.alpha_composite(canvas, layer)
    entries.append(dict(name=name, bone=bone, region=list(region), alphaBounds=bounds, translation=list(xy),
      uniformScale=SCALE, resampledSize=list(size), componentSHA256=sha(out / 'components' / f'{name}.png'),
      layerSHA256=sha(out / 'layers' / f'{name}.png')))
  canvas.save(out / f'{side}-neutral.png')
  m = dict(status='PROPOSED', kind='SAME_MASTER_EXTENSION_PROPOSAL_NOT_ADMISSION', facing=side,
    screenForward=cfg['screenForward'], nearAnatomicalSide=cfg['near'], canvas=[384, 416], groundRoot=list(ROOT),
    rootPolicy='registration anchor; visible boots may extend below it', contractIDs=['BP-002', 'BP-007', 'BP-012', 'T1045'],
    provenance=dict(sheet=str(src), localCopy=f'source/{side}-sheet.png', sheetSHA256=sha(local), metadataSHA256=sha(SRC / f'{side}-metadata.json'),
      generator='native image_generation, coordinator-authored', generatedHiddenSurfaces=True,
      paintStatus='generated proposed paint, not original master paint', cutSplits=CUT_SPLITS[side]),
    master=dict(path=str(RIG), localCopy='source/original-body-rig.json', sha256=sha(SRC / 'original-body-rig.json'), bindingType='semantic extension only, not validated anatomy'),
    tool=dict(name='Pillow', version=pillow_version), layerOrderBottomToTop=[e['name'] for e in entries],
    parts=entries, outputSHA256=sha(out / f'{side}-neutral.png'), alphaBounds=list(canvas.getchannel('A').getbbox()))
  (out / f'{side}-extension.json').write_text(json.dumps(m, indent=2) + '\n')
  return canvas

def gallery_images(views):
  loaded = []
  for n in ('south-neutral-original.png', 'north-neutral-active.png'):
    with Image.open(SRC / n) as im: loaded.append(im.convert('RGBA'))
  row = [loaded[0], views['east'], loaded[1], views['west']]
  strip = Image.new('RGBA', (384 * 4, 416))
  for i, im in enumerate(row): strip.alpha_composite(im, (384 * i, 0))
  strip.save(HERE / 'four-facing-source.png')
  bg = Image.new('RGBA', strip.size, (118, 118, 118, 255)); bg.alpha_composite(strip)
  bg.convert('L').save(HERE / 'four-facing-grayscale.png')
  bg.resize((64 * 4, 69), Image.Resampling.LANCZOS).save(HERE / 'four-facing-native.png')
  bg.resize((32 * 4, 35), Image.Resampling.LANCZOS).save(HERE / 'four-facing-half.png')

def verify_inputs():
  for name, (digest, _) in PINNED.items():
    got = sha(SRC / name)
    if got != digest: raise SystemExit(f'pinned input changed: source/{name} {got} != {digest}')

def refresh_from_originals():
  """Optional full audit: copy external originals after verifying pinned hashes."""
  SRC.mkdir(exist_ok=True)
  for name, (digest, path) in PINNED.items():
    if sha(path) != digest: raise SystemExit(f'external original changed: {path}')
    shutil.copyfile(path, SRC / name)

def build():
  if '--refresh-from-originals' in sys.argv: refresh_from_originals()
  verify_inputs()
  views = {s: build_side(s, c) for s, c in SIDES.items()}
  gallery_images(views)
  (HERE / 'inputs.json').write_text(json.dumps({k: v[0] for k, v in PINNED.items()}, indent=2) + '\n')
  print(json.dumps({s: json.loads((HERE / s / f'{s}-extension.json').read_text())['alphaBounds'] for s in SIDES}))

if __name__ == '__main__': build()
