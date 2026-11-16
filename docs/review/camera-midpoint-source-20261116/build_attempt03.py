"""Attempt 03: municipal Camera first sample from the FIXED APPROVED street-corner concept.

Owner correction 2026-11-16 04:22:37 UTC: attempt 02 'does not match benchmark'. The approved concept is
the sole visual authority. The midpoint selection is a ground transform plus upright registration; it does not
change the source viewpoint, proportions or materials.

Pixels: an exact crop of street-corner-approved-concept.png. Alpha: a deterministic contour-walled fill.
Transform: one uniform Lanczos scale plus a translation that puts the base centre at the ground anchor.
No generation, repaint, warp or non-uniform scale. Contamination is measured and reported, not hidden.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageOps, __version__ as pv
from scipy import ndimage, __version__ as sv

HERE = Path(__file__).resolve().parent
SRC = HERE / 'source'
OUT = HERE / 'attempts/03-approved-concept-extraction'
APPROVED = SRC / 'approved-concept.png'
APPROVED_SHA256 = '49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb'  # pinned SS-specs phase4 original
CROP = (880, 20, 1060, 470)
TOP_Y = 31                # finial top (concept px)
BASE_BOTTOM_Y = 446       # last base row before the sliver/leaf tip (concept px)
BASE_CENTRE_X = 932       # midpoint of base rows 420-424: x 891-973
TARGET_TOP, TARGET_BOTTOM = 39, 351   # same occupied rows as the controls; 64x96 box and anchor unchanged
SCALE = (TARGET_BOTTOM - TARGET_TOP + 1) / (BASE_BOTTOM_Y - TOP_Y + 1)
CANVAS = (256, 384)
ANCHOR_PX = (128, 352)


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


def contamination(rgba):
    """Opaque pixels whose colour is pavement or leaf, not device paint (dark metal, ivory, cyan)."""
    a = rgba.astype(int); op = a[..., 3] > 0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3; sat = np.max(a[..., :3], 2) - np.min(a[..., :3], 2)
    # Leaf: saturated orange-brown, unlike the low-chroma ivory shell (chroma < 60 by the mask rule).
    leaf = op & (sat > 60) & (r > g) & (g > b) & (r - b > 60)
    # Pavement: mid-grey, low chroma, only within 3 px of the silhouette edge (interior grey is metal paint).
    edge = op & ~ndimage.binary_erosion(op, iterations=3)
    pavement = edge & (lum >= 85) & (lum <= 140) & (sat < 20)
    return leaf, pavement


def main():
    (OUT / 'review').mkdir(parents=True, exist_ok=True)
    if sha(APPROVED) != APPROVED_SHA256:
        raise SystemExit('approved concept hash mismatch; refusing to build')
    with Image.open(APPROVED) as im:
        rgb = np.array(im.convert('RGB').crop(CROP))
    m = silhouette(rgb.astype(int))
    cut = Image.fromarray(np.dstack([rgb, m * 255]).astype(np.uint8))
    cut.save(OUT / 'concept-cutout.png')
    size = (round(cut.width * SCALE), round(cut.height * SCALE))
    ox = round(ANCHOR_PX[0] - (BASE_CENTRE_X - CROP[0]) * SCALE)
    oy = round(TARGET_BOTTOM - (BASE_BOTTOM_Y - CROP[1]) * SCALE)
    canvas = Image.new('RGBA', CANVAS)
    canvas.alpha_composite(cut.resize(size, Image.Resampling.LANCZOS), (ox, oy))
    a = np.array(canvas); a[a[..., 3] == 0] = 0
    canvas = Image.fromarray(a); canvas.save(OUT / 'camera-intact.png')
    leaf, pave = contamination(a)
    cl, cp = contamination(np.array(cut))
    ys = np.where((a[..., 3] > 128).any(1))[0]
    ys0 = np.where((a[..., 3] > 0).any(1))[0]
    def width(row_concept):
        r = np.where(m[row_concept - CROP[1]])[0]; return int(r.max() - r.min() + 1)
    facts = dict(conceptPoleWidthAtY260=width(260), conceptBaseWidthAtY420=width(420),
                 conceptHeadSpanX=[int(np.where(m[100 - CROP[1]:170 - CROP[1]].any(0))[0].max() + CROP[0]), 'right edge'],
                 conceptDeviceHeight=BASE_BOTTOM_Y - TOP_Y + 1,
                 outputOpaqueRows=[int(ys.min()), int(ys.max())], outputOpaqueRowsThreshold='alpha > 128',
                 outputAnyAlphaRows=[int(ys0.min()), int(ys0.max())],
                 targetRowsNote='TARGET 39..351 sets the scale; Lanczos edge alpha extends the measured rows')
    rec = dict(
        status='ATTEMPT_03_PROPOSED_FOR_DIRECT_INSPECTION_NOT_ACCEPTED',
        honestLabel='EXTRACTED_FROM_FIXED_APPROVED_CONCEPT_NOT_GENERATED_NOT_ORIGINAL_MASTER',
        authority='street-corner-approved-concept.png only (owner correction 2026-11-16 04:22:37 UTC)',
        source=dict(file='source/approved-concept.png', sha256=sha(APPROVED), crop=list(CROP), topY=TOP_Y,
                    baseCentre=[BASE_CENTRE_X, BASE_BOTTOM_Y],
                    mask='dark (mean<45) or ivory (mean>150, chroma<60) walls; closing 3; fill holes; opening 1; largest component; clip below base row'),
        transform=dict(uniformScale=SCALE, resampledSize=list(size), translation=[ox, oy], resample='Lanczos'),
        registration=dict(canvasPixels=list(CANVAS), logicalCanvas=[64, 96], logicalGroundAnchor=[32, 88], groundAnchorPixels=list(ANCHOR_PX)),
        contamination=dict(method='opaque px: leaf = chroma>60, R>G>B, R-B>60; pavement = mean 85-140, chroma<20, within 3 px of silhouette edge (may also catch edge metal highlights)',
                           cutoutLeafPixels=int(cl.sum()), cutoutPavementLikePixels=int(cp.sum()),
                           outputLeafPixels=int(leaf.sum()), outputPavementLikePixels=int(pave.sum())),
        measurements=facts, outputSHA256=sha(OUT / 'camera-intact.png'), tool=dict(pillow=pv, scipy=sv),
        limits=['Concept lighting, wear and ground tint are baked in', 'Mask edges are deterministic, not hand-cut; contamination counts above are shown, not hidden',
                'Downscale loses contour weight; compare at the same scale in review/benchmark-same-scale.png',
                'No underpaint; no layers split yet; intact only; no state or clip expansion'])
    (OUT / 'source-record.json').write_text(json.dumps(rec, indent=1) + '\n')
    review(rgb, canvas, leaf | pave)
    print(json.dumps(dict(scale=SCALE, size=size, t=[ox, oy], c=rec['contamination'], f=facts), indent=1))


def review(rgb, out, cont):
    bg = (74, 74, 72, 255)
    # Same scale: concept crop resized by the identical uniform scale and placement, beside the proposal.
    crop = Image.fromarray(rgb).convert('RGBA')
    size = (round(crop.width * SCALE), round(crop.height * SCALE))
    ox = round(ANCHOR_PX[0] - (BASE_CENTRE_X - CROP[0]) * SCALE); oy = round(TARGET_BOTTOM - (BASE_BOTTOM_Y - CROP[1]) * SCALE)
    ref = Image.new('RGBA', CANVAS, bg); ref.alpha_composite(crop.resize(size, Image.Resampling.LANCZOS), (ox, oy))
    prop = Image.new('RGBA', CANVAS, bg); prop.alpha_composite(out)
    cmask = Image.new('RGBA', CANVAS, bg); cmask.alpha_composite(out)
    ca = np.array(cmask); ca[cont] = (255, 0, 255, 255); cmask = Image.fromarray(ca)
    tiles = [('APPROVED concept, same scale', ref), ('attempt 03 proposal', prop), ('contamination (magenta)', cmask)]
    for name, k in [('benchmark-same-scale', 2), ('benchmark-native-64x96-3x', 0.75)]:
        tw, th = round(CANVAS[0] * k), round(CANVAS[1] * k)
        img = Image.new('RGBA', (len(tiles) * (tw + 20) + 20, th + 40), bg); d = ImageDraw.Draw(img)
        for i, (t, im) in enumerate(tiles):
            x = 20 + i * (tw + 20)
            img.alpha_composite(im.resize((tw, th), Image.Resampling.NEAREST), (x, 30)); d.text((x, 10), t, fill='white')
            ay = 30 + ANCHOR_PX[1] * k; ax = x + ANCHOR_PX[0] * k
            d.line([(ax - 6, ay), (ax + 6, ay)], fill='yellow')
        img.save(OUT / 'review' / f'{name}.png')
    n = out.resize((192, 288), Image.Resampling.LANCZOS); h = out.resize((96, 144), Image.Resampling.LANCZOS)
    g = ImageOps.grayscale(n).convert('RGBA'); g.putalpha(n.getchannel('A'))
    img = Image.new('RGBA', (192 + 96 + 192 + 80, 320), bg); d = ImageDraw.Draw(img); x = 20
    for t, im in [('native 64x96@3x', n), ('half', h), ('grayscale', g)]:
        img.alpha_composite(im, (x, 26)); d.text((x, 6), t, fill='white'); x += im.width + 20
    img.save(OUT / 'review/native-half-grayscale.png')


if __name__ == '__main__':
    main()
