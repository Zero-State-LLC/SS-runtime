"""Baggy south neutral PROPOSAL. Crop, uniform scale, translation only. No synthesis."""
from pathlib import Path
import hashlib, json, shutil
import numpy as np
from PIL import Image, ImageDraw, __version__ as pv

HERE = Path(__file__).resolve().parent
ORIG = Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs/SS-player-bounded-neutral')
GEN = Path('/Users/appliedalchemylabs/.jcode/generated-images/1794800681673-ig_07cd661172aa2162016afa7bf93ed087d0b1e945335a18112a.png')
NORTH = HERE.parent / 'player-north-source-20261116/attempts/01-uniform-0.4/north-neutral.png'
SOUTH = ORIG / 'frames/00.png'
SIZE = (384, 416)
ROOT = (192, 336)
BOOT_TOP = 318  # first row below the original trouser cuff where boot leather begins


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


UPPER = ['torso_coat_equipment', 'left_coat_tail', 'right_coat_tail',
         'left_shoulder_hidden', 'left_upper_arm', 'left_elbow_hidden', 'left_forearm_hand',
         'right_shoulder_hidden', 'right_upper_arm', 'right_elbow_hidden', 'right_forearm_hand', 'hood']

# name, sheet region (alpha-zero separated), anatomical side, uniform scale, resampled top-left
# South view: anatomical RIGHT is screen LEFT.
PARTS = [
    ('right_thigh', (208, 67, 529, 683), 'right', .15, (146, 200)),
    ('left_thigh', (614, 69, 943, 685), 'left', .15, (189, 200)),
    ('right_shin_kneepad', (221, 747, 487, 1295), 'right', .135, (150, 252)),
    ('left_shin_kneepad', (646, 747, 919, 1293), 'left', .135, (194, 252)),
]


def main():
    for d in ('source', 'components', 'layers'):
        (HERE / d).mkdir(exist_ok=True)
    for s, d in [(GEN, 'source/trouser-sheet.png'), (GEN.with_suffix('.json'), 'source/metadata.json'),
                 (SOUTH, 'source/south-neutral-original.png'), (NORTH, 'source/north-baggy-reference.png')]:
        shutil.copyfile(s, HERE / d)
    sheet = Image.open(GEN).convert('RGBA')
    south = Image.open(SOUTH).convert('RGBA')
    sa = np.array(south)
    canvas = Image.new('RGBA', SIZE)
    parts = []
    for name, region, side, s, xy in PARTS:
        comp = sheet.crop(region)
        comp.save(HERE / 'components' / f'{name}.png')
        size = (round(comp.width * s), round(comp.height * s))
        layer = Image.new('RGBA', SIZE)
        layer.alpha_composite(comp.resize(size, Image.Resampling.LANCZOS), xy)
        layer.save(HERE / 'layers' / f'{name}.png')
        canvas.alpha_composite(layer)
        parts.append(dict(name=name, anatomicalSide=side, sheetRegion=list(region), uniformScale=s,
                          translation=list(xy), resampledSize=list(size),
                          alphaBounds=list(layer.getchannel('A').getbbox()),
                          componentSHA256=sha(HERE / 'components' / f'{name}.png'),
                          layerSHA256=sha(HERE / 'layers' / f'{name}.png')))
    # Original approved boots: exact frame-00 pixels inside original boot-layer alpha, rows >= BOOT_TOP.
    bootmask = np.zeros(SIZE[::-1], bool)
    for side in ('right', 'left'):
        bootmask |= np.array(Image.open(ORIG / f'boot/frames/00-{side}.png'))[..., 3] > 0
    bootmask[:BOOT_TOP] = False
    boots = np.zeros_like(sa)
    boots[bootmask] = sa[bootmask]
    Image.fromarray(boots).save(HERE / 'layers/original_boots.png')
    canvas.alpha_composite(Image.fromarray(boots))
    # Original upper body/coat/hands/equipment layers; opaque pixels copied exactly from frame 00.
    up = Image.new('RGBA', SIZE)
    for n in UPPER:
        layer = Image.new('RGBA', SIZE)
        layer.paste(Image.open(ORIG / f'source/body-source/{n}.png').convert('RGBA'), (0, 0))
        up.alpha_composite(layer)
    ua = np.array(up)
    opaque = (ua[..., 3] == 255) & (sa[..., 3] == 255)
    ua[opaque] = sa[opaque]
    Image.fromarray(ua).save(HERE / 'layers/original_upper.png')
    canvas.alpha_composite(Image.fromarray(ua))
    canvas.save(HERE / 'south-baggy-neutral.png')

    north = Image.open(NORTH).convert('RGBA')
    facts = {k: measure(im) for k, im in [('originalSouth', south), ('proposedBaggySouth', canvas),
                                           ('preferredBaggyNorth', north)]}
    comparison(south, canvas, north)
    manifest = dict(
        status='PROPOSED_SOURCE_NOT_ADMISSION', facing='south', canvas=list(SIZE), groundRoot=list(ROOT),
        bootTopRow=BOOT_TOP,
        method='crop, per-part uniform Lanczos scale, translation; original boot/upper pixels copied exactly; '
               'no repainting, warping, mirroring or stretching of the old south bitmap',
        anatomical='south view: anatomical right on screen left; cloth patch on anatomical-left thigh (screen right)',
        provenance=dict(
            sheet=str(GEN), sheetSHA256=sha(GEN), metadataSHA256=sha(GEN.with_suffix('.json')),
            generator='native image_generation (openai), see source/metadata.json',
            south=str(SOUTH), southSHA256=sha(SOUTH), northReference=str(NORTH), northReferenceSHA256=sha(NORTH),
            originalUpperLayers={n: sha(ORIG / f'source/body-source/{n}.png') for n in UPPER},
            originalBootLayers={s: sha(ORIG / f'boot/frames/00-{s}.png') for s in ('right', 'left')}),
        tool=dict(name='Pillow', version=pv),
        layerOrderBottomToTop=[p['name'] for p in parts] + ['original_boots', 'original_upper'],
        parts=parts, retained=dict(bootPixels=int(bootmask.sum()), upperOpaquePixels=int(opaque.sum())),
        outputSHA256=sha(HERE / 'south-baggy-neutral.png'), measurements=facts,
        limits=['Neutral only, no animation', 'Trouser paint is generated, not original master paint',
                'North reference is an unaccepted generated sample; only its trouser silhouette is the stated preference',
                'No native, simulator, device or acceptance claim', 'Hip/knee/ankle pivots are 2D annotations'])
    (HERE / 'baggy-south.json').write_text(json.dumps(manifest, indent=1) + '\n')
    print(json.dumps(dict(out=manifest['outputSHA256'], facts=facts), indent=1))


def measure(im):
    a = np.array(im)[..., 3] > 0
    r = {}
    for y in (215, 235, 255, 275, 295, 310):
        xs = np.where(a[y, 140:245])[0] + 140
        runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1) if len(xs) else []
        r[f'row{y}'] = [[int(q[0]), int(q[-1]), int(q[-1] - q[0] + 1)] for q in runs]
    ys = np.where(a.any(1))[0]
    r['alphaYRange'] = [int(ys.min()), int(ys.max())]
    return r


def comparison(south, prop, north):
    S = 2
    W = 384 * S
    img = Image.new('RGB', (W * 3, 416 * S + 40), '#2b3238')
    d = ImageDraw.Draw(img)
    for i, (t, im) in enumerate([('ORIGINAL SOUTH (unchanged)', south), ('PROPOSED BAGGY SOUTH', prop),
                                 ('PREFERRED BAGGY NORTH ref (attempt 01)', north)]):
        big = im.resize((W, 416 * S), Image.Resampling.NEAREST)
        img.paste(big, (i * W, 40), big)
        d.text((i * W + 10, 12), t, fill='white')
        for y, lab in [(200, 'hip y200'), (265, 'knee y265'), (BOOT_TOP, f'boot top y{BOOT_TOP}'),
                       (ROOT[1], 'ground root y336')]:
            d.line([(i * W, 40 + y * S), (i * W + W, 40 + y * S)], fill=(255, 80, 80))
            d.text((i * W + 4, 40 + y * S - 12), lab, fill=(255, 140, 140))
        x, y = i * W + ROOT[0] * S, 40 + ROOT[1] * S
        d.ellipse([x - 4, y - 4, x + 4, y + 4], outline='yellow')
    img.save(HERE / 'three-way-comparison.png')


if __name__ == '__main__':
    main()
