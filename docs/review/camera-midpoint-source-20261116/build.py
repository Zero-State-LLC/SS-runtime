"""Municipal Camera midpoint FIRST SAMPLE. Editable layer partition of the recovered intact device.

No image generation, repainting, warping or resampling of source pixels. Layers are a disjoint
partition by authored polygons; their composite must equal the recovered intact image exactly.
"""
from pathlib import Path
import hashlib, json, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageOps, __version__ as pv

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
INTACT = REVIEW / 'camera-shared-source/intact.png'
STATES = {n: REVIEW / f'camera-shared-source/{n}.png' for n in ('intact', 'damaged', 'critical', 'destroyed')}
STUDY = REVIEW / 'camera-state-study/registration.json'
SPECS = Path('/Users/appliedalchemylabs/.jcode/scratch/ss-specs-audit-pr-20261114/docs/review/phase4')
CONCEPT = SPECS / 'street-corner-approved-concept.png'
MIDPOINT = SPECS / 'street-corner-midpoint-concept.png'
CONTRACT = REVIEW.parent.parent / 'Sources/SurveillanceCore/Resources/contracts/clip-metadata-001.json'
CONCEPT_CROP = (860, 0, 1100, 470)  # municipal camera region in both 1672x941 concepts

CANVAS = (256, 384)
LOGICAL = (64, 96)
ANCHOR_LOGICAL = (32, 88)
ANCHOR_PX = (128, 352)

# Authored layer polygons in 256x384 canvas pixels. Earlier entries claim pixels first.
# The head polygon is reused verbatim from camera-shared-source/source-record.json.
HEAD = [(164, 155), (172, 143), (185, 133), (199, 137), (218, 137), (227, 127), (241, 139), (255, 154), (256, 226), (163, 226)]
LAYERS = [
    ('head', HEAD),
    ('arm', [(128, 92), (160, 92), (165, 98), (230, 98), (230, 137), (199, 137), (185, 133), (172, 143), (164, 155), (163, 185), (128, 185)]),
    ('junction_box', [(134, 192), (162, 192), (162, 260), (134, 260)]),
    ('base', [(80, 276), (176, 276), (176, 360), (80, 360)]),
    ('pole', [(0, 0), (256, 0), (256, 384), (0, 384)]),  # remainder: finial, shaft, collars
]
ORDER_BOTTOM_TO_TOP = ['base', 'pole', 'junction_box', 'arm', 'head']

INTEGRITY_REQUIREMENTS = {
    'source': 'SS-specs benchmark-production.md BP-004',
    'clips': {'operationalIdle': 4, 'hit': 2, 'criticalEnter': 3, 'destroy': 4, 'fieldOff': 1, 'destroyedIdle': 2},
    'settled': {'3': 'intact complete device, no positional or heading motion',
                '2': 'visible damage, single-notch runtime marker',
                '1': 'exposed damage, double-notch runtime marker',
                '0': 'dark broken head, unchanged mount/base, field off on authoritative event'},
    'status': 'REQUIREMENT_PRESERVED_NOT_EXPANDED_IN_FIRST_SAMPLE',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def visible(a):
    a = a.copy()
    a[a[..., 3] == 0] = 0
    return a


def masks():
    taken = np.zeros(CANVAS[::-1], bool)
    out = {}
    for name, poly in LAYERS:
        m = Image.new('L', CANVAS)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        m = (np.array(m) > 0) & ~taken
        taken |= m
        out[name] = m
    return out


def ellipse_facts(a):
    """Measure the visible base footprint from opaque base rows (alpha > 128)."""
    rows = np.where((a[..., 3] > 128).any(1))[0]
    bottom = int(rows.max())
    widths = {int(y): int((a[y, :, 3] > 128).sum()) for y in range(276, bottom + 1)}
    maxw = max(widths.values())
    return dict(bottomOpaqueRow=bottom, baseMaxOpaqueWidth=maxw,
                baseRowsAtMaxWidth=[y for y, w in widths.items() if w == maxw])


def main():
    for d in ('source', 'layers', 'review'):
        (HERE / d).mkdir(exist_ok=True)
    for src, dst in [(INTACT, 'source/recovered-intact.png'), (STUDY, 'source/camera-state-study-registration.json'),
                     (CONCEPT, 'source/approved-concept.png'), (MIDPOINT, 'source/midpoint-concept.png')]:
        shutil.copyfile(src, HERE / dst)
    for k, v in STATES.items():
        shutil.copyfile(v, HERE / 'source' / f'state-{k}.png')
    meta = json.loads(CONTRACT.read_text())
    cams = [dict(clipId=c['clipId'], frameIds=c['frameIds']) for c in meta['clips'] if c['actorRole'] == 'camera']
    (HERE / 'source/camera-clip-contract.json').write_text(json.dumps(dict(
        copiedFrom='Sources/SurveillanceCore/Resources/contracts/clip-metadata-001.json', sha256=sha(CONTRACT),
        schemaVersion=meta.get('schemaVersion'), cameraClips=cams), indent=1) + '\n')
    im = Image.open(INTACT).convert('RGBA')
    a = np.array(im)
    ms = masks()
    layer_records = []
    comp = Image.new('RGBA', CANVAS)
    for name in ORDER_BOTTOM_TO_TOP:
        la = np.zeros_like(a)
        la[ms[name]] = a[ms[name]]
        p = HERE / 'layers' / f'{name}.png'
        Image.fromarray(la).save(p)
        comp.alpha_composite(Image.fromarray(la))
        bb = Image.fromarray(la).getchannel('A').getbbox()
        layer_records.append(dict(name=name, sha256=sha(p), alphaBounds=list(bb) if bb else None,
                                  opaquePixels=int((la[..., 3] > 0).sum()),
                                  polygon=dict(LAYERS)[name], provenance='recovered pixels, exact partition'))
    comp.save(HERE / 'camera-midpoint-intact.png')
    review(comp)
    rec = dict(
        status='ATTEMPT_01_REJECTED_OWNER_2026-11-16T04:22:37Z_COMPARISON_HISTORY_ONLY',
        projection='D-108 midpoint: +45 deg ground rotation then half-height scaling; upright sprite at projected root',
        registration=dict(canvasPixels=list(CANVAS), logicalCanvas=list(LOGICAL), logicalGroundAnchor=list(ANCHOR_LOGICAL),
                          groundAnchorPixels=list(ANCHOR_PX), baseFootprint=ellipse_facts(a)),
        provenance=dict(
            recoveredIntact=str(INTACT), recoveredIntactSHA256=sha(INTACT),
            origin='camera-state-study: built-in image_gen output, alpha cleanup and registration; CAPTURED candidate, never accepted',
            honestLabel='GENERATED_PRIOR_CANDIDATE_RECOVERED_NOT_ORIGINAL_MASTER',
            otherStates={k: sha(v) for k, v in STATES.items()},
            concept=str(CONCEPT), conceptSHA256=sha(CONCEPT), midpointConcept=str(MIDPOINT), midpointConceptSHA256=sha(MIDPOINT)),
        tool=dict(name='Pillow', version=pv),
        layerOrderBottomToTop=ORDER_BOTTOM_TO_TOP, layers=layer_records,
        compositeEqualsRecoveredRGBA=bool(np.array_equal(np.array(comp), visible(a))),
        equalityNote='compared after zeroing RGB of alpha-0 pixels (53 such pixels carry hidden RGB in the recovered file)',
        outputSHA256=sha(HERE / 'camera-midpoint-intact.png'),
        integrityRequirements=INTEGRITY_REQUIREMENTS,
        limits=['First sample: intact state only; damaged/critical/destroyed and six clips not re-authored here',
                'Source pixels are a prior generated candidate, not an approved original master',
                'Layer polygons are authored visual boundaries, not collision, targeting or field geometry',
                'No hidden underpaint behind arm/head; layers are a partition, so moving a layer would expose holes',
                'Review plates are source previews, not real-renderer, native-device or encounter evidence'])
    (HERE / 'source-record.json').write_text(json.dumps(rec, indent=1) + '\n')
    print(json.dumps(dict(out=rec['outputSHA256'], exact=rec['compositeEqualsRecoveredRGBA'],
                          base=rec['registration']['baseFootprint'],
                          layers=[(l['name'], l['opaquePixels']) for l in layer_records]), indent=1))


def review(comp):
    bg = (74, 74, 72, 255)
    # 1. Benchmark: approved concept and midpoint concept crops beside the sample at matched height.
    crops = [Image.open(p).convert('RGBA').crop(CONCEPT_CROP) for p in (CONCEPT, MIDPOINT)]
    h = 470
    s = comp.resize((round(256 * h / 384), h), Image.Resampling.LANCZOS)
    bench = Image.new('RGBA', (240 * 2 + s.width + 40, h + 24), bg)
    d = ImageDraw.Draw(bench)
    for i, (t, c) in enumerate([('approved concept (benchmark)', crops[0]), ('midpoint concept', crops[1])]):
        bench.alpha_composite(c, (i * 260, 24)); d.text((i * 260 + 4, 6), t, fill='white')
    bench.alpha_composite(s, (520, 24)); d.text((524, 6), 'first sample (source)', fill='white')
    bench.save(HERE / 'review/benchmark-comparison.png')
    # 2. Native / half / grayscale at logical size with anchor and base marks.
    plates = []
    for label, scale in [('native 64x96 @3x', 3), ('half 32x48 @3x', 1.5)]:
        w, h2 = round(LOGICAL[0] * scale), round(LOGICAL[1] * scale)
        plates.append((label, comp.resize((w, h2), Image.Resampling.LANCZOS)))
    native = plates[0][1]
    def gray(p):
        g = ImageOps.grayscale(p).convert('RGBA')
        g.putalpha(p.getchannel('A'))
        return g
    plates.append(('grayscale native', gray(native)))
    plates.append(('grayscale half', gray(plates[1][1])))
    W = sum(p.width for _, p in plates) + 40 * len(plates)
    sheet = Image.new('RGBA', (W, 340), bg)
    d = ImageDraw.Draw(sheet)
    x = 20
    for label, p in plates:
        y = 30
        sheet.alpha_composite(p, (x, y))
        k = p.width / LOGICAL[0]
        ax, ay = x + ANCHOR_LOGICAL[0] * k, y + ANCHOR_LOGICAL[1] * k
        d.line([(ax - 6, ay), (ax + 6, ay)], fill='yellow'); d.line([(ax, ay - 6), (ax, ay + 6)], fill='yellow')
        d.text((x, 8), label, fill='white')
        x += p.width + 40
    sheet.save(HERE / 'review/native-half-grayscale.png')
    # 3. Layer breakdown with polygon outlines at 2x.
    big = Image.new('RGBA', (CANVAS[0] * 2, CANVAS[1] * 2), bg)
    big.alpha_composite(comp.resize((CANVAS[0] * 2, CANVAS[1] * 2), Image.Resampling.NEAREST))
    d = ImageDraw.Draw(big)
    colors = dict(head='cyan', arm='magenta', junction_box='orange', base='lime', pole='white')
    for name, poly in LAYERS:
        if name != 'pole':
            d.polygon([(px * 2, py * 2) for px, py in poly], outline=colors[name])
            d.text((poly[0][0] * 2 + 2, poly[0][1] * 2 + 2), name, fill=colors[name])
    d.line([(ANCHOR_PX[0] * 2 - 12, ANCHOR_PX[1] * 2), (ANCHOR_PX[0] * 2 + 12, ANCHOR_PX[1] * 2)], fill='yellow', width=2)
    d.text((ANCHOR_PX[0] * 2 + 14, ANCHOR_PX[1] * 2 - 6), 'ground anchor (32,88)', fill='yellow')
    big.save(HERE / 'review/layers-annotated.png')


if __name__ == '__main__':
    main()
