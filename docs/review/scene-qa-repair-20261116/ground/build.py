#!/usr/bin/env python3
"""Extend the pinned authored context, not its finite raster or curb motif.
ADAPT by direct import: paving-corner-review-20261116/build.py:16-142.
The original context evaluator receives new bounds only. No original writes.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REVIEW = HERE.parents[1]
ORIGINAL = REVIEW / 'paving-corner-review-20261116'
SCENE = REVIEW / 'scene-source-assembly-20261116'
PINS = {
    'paving-corner-review-20261116/source.json': '3fabc473f8469241fb928c7dc7b8281c6e6e8e304d6789f7e9387eaf66ea6f1b',
    'paving-corner-review-20261116/build.py': 'a5dedc85a67ba91d85efccea6be7bb2d0e9d46e31da7be33659f92bd15f0c061',
    'paving-corner-review-20261116/corner-topdown.png': 'a0d937657b5f975246951213168cdeb715871412f7c4c402040228cc570a4e6c',
    'paving-corner-review-20261116/paving-supertile.png': '1b864486f0859262c4e851a95e3fe3c3b0210ee5ec3306ada5ee066a05319c7a',
    'paving-repeat-repair-20261116/revision02/paving-muted-candidate.png': '7a1f29c7b0f1a0a96e12484de84da21e7ab4ebee10cab2e829ed19309ca17d35',
    'scene-source-assembly-20261116/authoritative-placement-1014.json': 'b112b8685dd03c1cd1fd0214f7b010e33dbde3e714c5f21e4e48c4e342238e07',
    'scene-source-assembly-20261116/native-capture-1040/source-scene-records.json': '20ca37e2ce48a24b03d5d313a1605c62cacded73c36687a8a1e30fb5d6bc0138',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dependencies():
    for path, digest in PINS.items():
        if sha(REVIEW / path) != digest:
            raise ValueError('Immutable dependency changed: ' + path)
    return dict(PINS)

def original():
    dependencies()
    loader = importlib.util.spec_from_file_location('original_paving', ORIGINAL / 'build.py')
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    return module

def bounds():
    placement = json.loads((SCENE / 'authoritative-placement-1014.json').read_text())
    return placement['arenaMinWorld'] + placement['arenaMaxWorld']

def rows():
    record = json.loads((SCENE / 'native-capture-1040/source-scene-records.json').read_text())
    return [r for r in record['captures'] if r['arm'] == 'candidate']

def inverse(row, sx, sy):
    # sx right, sy UP, relative to actual 704x326 capture center.
    x, y = sx / row['zoom'], sy / row['zoom']
    cx, cy = row['centerWorld']
    return (cx + (x + 2*y)/math.sqrt(2), cy + (-x + 2*y)/math.sqrt(2))

def coverage(rect):
    result = []
    for row in rows():
        points = [list(inverse(row, x, y)) for x,y in [(-352,-163), (352,-163), (352,163), (-352,163)]]
        inside = [rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3] for x,y in points]
        result.append({'zoom': row['zoom'], 'inverseCropCornersWorld': points,
                       'cornersCovered': inside, 'covered': all(inside)})
    return {'boundsWorld': rect, 'passed': all(r['covered'] for r in result), 'results': result}

def preview(image, output, old_bounds):
    # One diagnostic sheet, not a native screenshot or benchmark image.
    sheet = Image.new('RGB', (1056, 390), '#222222')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 8), 'OFFLINE GROUND ONLY: v4 crop inverses, red = old finite patch boundary', fill='white')
    scale = 2
    for index, row in enumerate(rows()):
        cx, cy = row['centerWorld']
        z = row['zoom']
        a = scale / (z*math.sqrt(2))
        # At half-size preview: sx=2*u-352, sy=163-2*v.
        affine = (2*a, -4*a, scale*cx+a*(-352+326),
                  2*a, 4*a, scale*(bounds()[3]-cy)+a*(-352-326))
        crop = image.transform((352,163), Image.Transform.AFFINE, affine, resample=Image.Resampling.BICUBIC)
        sheet.paste(crop, (index*352, 42))
        d = ImageDraw.Draw(sheet)
        pts = []
        for x,y in [(old_bounds[0],old_bounds[1]),(old_bounds[2],old_bounds[1]),(old_bounds[2],old_bounds[3]),(old_bounds[0],old_bounds[3])]:
            sx = z*((x-cx)-(y-cy))/math.sqrt(2)
            sy = z*((x-cx)+(y-cy))/(2*math.sqrt(2))
            pts.append((round((sx+352)/2), round((163-sy)/2)))
        annotated = crop.copy()
        ImageDraw.Draw(annotated).line(pts+[pts[0]], fill='#ff5555', width=1)
        sheet.paste(annotated, (index*352, 222))
        d.text((index*352+8, 25), f"zoom {row['zoom']:.2f} / unannotated then boundary overlay", fill='white')
    sheet.save(output / 'diagnostic-preview.png')

def build(output=HERE):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    old = original()
    spec, source = old.read_source()
    tile, mixtures = old.material(spec, source)
    extended = copy.deepcopy(spec)
    extended['corner']['worldBounds'] = bounds()
    assert extended['corner']['pixelsPerWorldUnit'] == 2
    image = old.context(extended, tile)
    image.save(output / 'ground-arena.png')
    # GroundPatch assumes a SQUARE tileUnits denominator for both UV axes.
    # Place arena in bottom part, padding above only. No squashing or motif repeat.
    side = max(image.size)
    adapter = Image.new('RGB', (side, side))
    adapter.paste(image.crop((0,0,image.width,1)).resize((side,side-image.height)), (0,0))
    adapter.paste(image, (0,side-image.height))
    adapter.save(output / 'ground-patch-square.png')
    preview(image, output, spec['corner']['worldBounds'])
    manifest = {
        'status': 'REVIEW_SOURCE_READY_NOT_NATIVE_OR_OWNER_ACCEPTED',
        'dependenciesSHA256': dependencies(), 'builderSHA256': sha(Path(__file__)),
        'algorithm': 'Pinned original material() and context(), changing worldBounds only. Signed corner distance and world-coordinate road grain evaluated across arena. Material modulo 256 world units applies only where distance <= 0. Decorative features drawn once.',
        'registration': {'boundsWorld': bounds(), 'worldOriginBottomLeft': bounds()[:2],
                         'canvasPixels': list(image.size), 'pixelsPerWorldUnit': 2,
                         'pixelToWorld': 'x=px/2, y=1536-py/2 (original edge-sample convention retained)',
                         'drawSizeWorld': [2304,1536], 'anchor': [0,0]},
        'groundPatches': {'file': 'ground-patch-square.png', 'canvasPixels': [side,side],
                          'bounds': [0,0,2304,1536], 'tileUnits': 2304,
                          'normalizedTextureRect': [0,0,1,2/3],
                          'paddingTopPixels': side-image.height,
                          'note': 'Replace finite patch and conflicting groundLines. Exactly one patch node. Do not use rectangular ground-arena.png with square tileUnits.'},
        'oldCoverage': coverage(spec['corner']['worldBounds']), 'fixedCoverage': coverage(bounds()),
        'outputsSHA256': {name: sha(output/name) for name in ['ground-arena.png','ground-patch-square.png','diagnostic-preview.png']},
        'limits': spec['limits'] + ['No native run, whole-scene lighting/contact or owner acceptance.', 'Arena-wide extrapolation preserves authored geometry, not certified street semantics around every other building.', 'Square adapter uses 4608-square RGB texture, GPU cost not measured.']
    }
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE)
    parser.add_argument('--probe', choices=['v4','fixed'])
    args = parser.parse_args()
    if args.probe:
        dependencies()
        rect = json.loads((ORIGINAL/'source.json').read_text())['corner']['worldBounds'] if args.probe == 'v4' else bounds()
        report = coverage(rect)
        print(json.dumps(report, indent=2))
        raise SystemExit(0 if report['passed'] else 1)
    print(json.dumps(build(args.output), indent=2))
