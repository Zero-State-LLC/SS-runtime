"""Attempt 02: municipal Camera first sample extracted from the approved MIDPOINT concept.

Pixels come from the fixed SS-specs midpoint concept, which has the selected elevation and proportions.
Steps: a crop, an authored silhouette mask (contour-walled fill, see MASK), one uniform Lanczos scale and
a translation onto the existing 256x384 canvas with the base centre at the ground anchor.
No image generation, repainting or non-uniform flattening. The attempt 01 recovered candidate stays as the control.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageOps, __version__ as pv
from scipy import ndimage, __version__ as sv
import build as A1

HERE = Path(__file__).resolve().parent
OUT = HERE / 'attempts/02-midpoint-concept-extraction'
CROP = (880, 60, 1080, 420)            # concept pixels holding the complete device
BASE_BOTTOM_Y = 401                    # last full base row before leaf debris (concept px)
BASE_CENTRE_X = 947                    # midpoint of base rows 377-401 (concept px)
TOP_Y = 67                             # top of finial (concept px)
TARGET_HEIGHT = 313                    # attempt-01 opaque height, keeps world draw size unchanged
SCALE = TARGET_HEIGHT / (BASE_BOTTOM_Y - TOP_Y + 1)
MASK = dict(dark='mean RGB < 45', ivory='mean RGB > 150 and max-min < 60', closingIterations=3,
            fill='binary_fill_holes', opening=1, keep='largest component', clipBelowY=BASE_BOTTOM_Y)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def silhouette(rgb):
    lum = rgb.mean(2); sat = rgb.max(2) - rgb.min(2)
    m = ndimage.binary_fill_holes(ndimage.binary_closing((lum < 45) | ((lum > 150) & (sat < 60)), iterations=3))
    m = ndimage.binary_opening(m, iterations=1)
    lab, n = ndimage.label(m)
    m = lab == (np.argmax(ndimage.sum(m, lab, range(1, n + 1))) + 1)
    m[BASE_BOTTOM_Y - CROP[1] + 1:] = False
    return m


def main():
    for d in ('layers', 'review'):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    rgb = np.array(Image.open(A1.MIDPOINT).convert('RGB').crop(CROP))
    m = silhouette(rgb)
    cut = np.dstack([rgb, m * 255]).astype(np.uint8)
    cut_img = Image.fromarray(cut)
    cut_img.save(OUT / 'concept-cutout.png')
    size = (round(cut_img.width * SCALE), round(cut_img.height * SCALE))
    scaled = cut_img.resize(size, Image.Resampling.LANCZOS)
    # Translate so concept (BASE_CENTRE_X, BASE_BOTTOM_Y) lands at pixel (128, 351).
    ox = round(128 - (BASE_CENTRE_X - CROP[0]) * SCALE)
    oy = round(351 - (BASE_BOTTOM_Y - CROP[1]) * SCALE)
    canvas = Image.new('RGBA', A1.CANVAS)
    canvas.alpha_composite(scaled, (ox, oy))
    a = np.array(canvas); a[a[..., 3] == 0] = 0
    canvas = Image.fromarray(a)
    canvas.save(OUT / 'camera-midpoint-intact.png')
    # Editable layers: disjoint partition by authored polygons in output pixels.
    polys = layer_polygons()
    taken = np.zeros(a.shape[:2], bool); recs = []
    for name, poly in polys:
        mk = Image.new('L', A1.CANVAS); ImageDraw.Draw(mk).polygon(poly, fill=255)
        mk = (np.array(mk) > 0) & ~taken; taken |= mk
        la = np.zeros_like(a); la[mk] = a[mk]
        p = OUT / 'layers' / f'{name}.png'; Image.fromarray(la).save(p)
        recs.append(dict(name=name, polygon=poly, sha256=sha(p), opaquePixels=int((la[..., 3] > 0).sum())))
    ys = np.where((a[..., 3] > 128).any(1))[0]
    head_cols = int((a[ys.min():ys.max() + 1, 160:, 3] > 128).any(0).sum())
    record = dict(
        status='ATTEMPT_02_REJECTED_OWNER_2026-11-16T04:22:37Z_MIDPOINT_CONCEPT_NOT_AUTHORITY',
        honestLabel='EXTRACTED_FROM_APPROVED_MIDPOINT_CONCEPT_NOT_GENERATED_NOT_ORIGINAL_MASTER',
        source=dict(path=str(A1.MIDPOINT), sha256=sha(A1.MIDPOINT), crop=list(CROP), mask=MASK,
                    baseCentre=[BASE_CENTRE_X, BASE_BOTTOM_Y], topY=TOP_Y),
        transform=dict(uniformScale=SCALE, resampledSize=list(size), translation=[ox, oy], resample='Lanczos'),
        registration=dict(canvasPixels=list(A1.CANVAS), logicalCanvas=list(A1.LOGICAL), logicalGroundAnchor=list(A1.ANCHOR_LOGICAL),
                          groundAnchorPixels=list(A1.ANCHOR_PX), opaqueRows=[int(ys.min()), int(ys.max())]),
        control=dict(path='camera-midpoint-intact.png (attempt 01)', sha256=sha(HERE / 'camera-midpoint-intact.png')),
        tool=dict(pillow=pv, scipy=sv), layerOrder=[r['name'] for r in recs][::-1], layers=recs,
        outputSHA256=sha(OUT / 'camera-midpoint-intact.png'),
        measurements=dict(opaqueHeight=int(ys.max() - ys.min() + 1), opaqueColumnsRightOfX160=head_cols),
        integrityRequirements=A1.INTEGRITY_REQUIREMENTS,
        limits=['Concept pixels include baked scene lighting and some ground/leaf contamination at mask edges',
                'Mask is a deterministic contour-fill, not hand-authored alpha; edge pixels may carry pavement colour',
                'Downscale 0.937 keeps world draw size equal to attempt 01; concept-to-Player relative scale not yet checked in a shared scene',
                'No hidden underpaint behind arm/head; layers are a visual partition only',
                'Intact only; no damaged/critical/destroyed or clip frames'])
    (OUT / 'source-record.json').write_text(json.dumps(record, indent=1) + '\n')
    review(Image.open(HERE / 'camera-midpoint-intact.png').convert('RGBA'), canvas)
    print(json.dumps(dict(out=record['outputSHA256'], transform=record['transform'], reg=record['registration'],
                          layers=[(r['name'], r['opaquePixels']) for r in recs]), indent=1))


def layer_polygons():
    s = SCALE; ox = round(128 - (BASE_CENTRE_X - CROP[0]) * s); oy = round(351 - (BASE_BOTTOM_Y - CROP[1]) * s)
    def P(pts): return [(round(ox + (x - CROP[0]) * s), round(oy + (y - CROP[1]) * s)) for x, y in pts]
    # Concept-pixel polygons (see midpoint concept grid), converted to output pixels.
    return [
        ('head', P([(1000, 140), (1065, 140), (1065, 215), (1000, 215)])),
        ('arm', P([(968, 108), (1000, 108), (1000, 140), (1065, 140), (1065, 100), (1000, 100), (985, 175), (968, 175)])),
        ('junction_box', P([(966, 176), (1000, 176), (1000, 230), (966, 230)])),
        ('base', P([(900, 330), (995, 330), (995, 410), (900, 410)])),
        ('pole', [(0, 0), (256, 0), (256, 384), (0, 384)]),
    ]


def review(control, proposal):
    bg = (74, 74, 72, 255)
    crop = Image.open(A1.MIDPOINT).convert('RGBA').crop(CROP)
    h = 420
    def fit(im): return im.resize((round(im.width * h / im.height), h), Image.Resampling.LANCZOS)
    tiles = [('midpoint concept (benchmark)', fit(crop)), ('attempt 01 control', fit(control)), ('attempt 02 proposal', fit(proposal))]
    W = sum(t.width for _, t in tiles) + 30 * len(tiles)
    img = Image.new('RGBA', (W, h + 30), bg); d = ImageDraw.Draw(img); x = 10
    for label, t in tiles:
        img.alpha_composite(t, (x, 26)); d.text((x, 6), label, fill='white'); x += t.width + 30
    img.save(OUT / 'review/three-way.png')
    plates = []
    for label, im in [('01 native', control), ('02 native', proposal)]:
        n = im.resize((192, 288), Image.Resampling.LANCZOS)
        hf = im.resize((96, 144), Image.Resampling.LANCZOS)
        g = ImageOps.grayscale(n).convert('RGBA'); g.putalpha(n.getchannel('A'))
        plates += [(label + ' 64x96@3x', n), (label[:2] + ' half', hf), (label[:2] + ' gray', g)]
    W = sum(p.width for _, p in plates) + 20 * len(plates)
    img = Image.new('RGBA', (W, 330), bg); d = ImageDraw.Draw(img); x = 10
    for label, p in plates:
        img.alpha_composite(p, (x, 30)); d.text((x, 8), label, fill='white')
        k = p.width / 64; ax, ay = x + 32 * k, 30 + 88 * k
        d.line([(ax - 5, ay), (ax + 5, ay)], fill='yellow'); x += p.width + 20
    img.save(OUT / 'review/native-half-grayscale.png')


if __name__ == '__main__':
    main()
