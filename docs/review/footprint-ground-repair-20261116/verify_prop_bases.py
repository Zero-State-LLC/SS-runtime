#!/usr/bin/env python3
"""Conservative retained-raster base clearance, separate from authored shadow radii.
Source regions were visually identified by coordinator, not mesh-derived contours.
The complete rectangular region is tested, including transparent pixels, so this
cannot certify base shape or 3D geometry but conservatively bounds these bases.
"""
import hashlib
import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def verify():
    plan = json.loads((HERE / 'plan/plan.json').read_text())
    # Coordinates are inclusive conservative source-pixel rectangles enclosing
    # the visible tree grate and newsbox plinth in the immutable source PNGs.
    regions = [('benchmark-prop-0', 'newsbox.png', [45, 595, 356, 767], [20, 40]),
               ('benchmark-prop-1', 'tree.png', [65, 540, 372, 767], [50, 85])]
    results = []
    with Image.open(HERE / 'plan/material-ids.png') as material:
        for name, filename, region, draw in regions:
            source = ROOT / 'AppTests/BenchmarkAssets' / filename
            with Image.open(source) as image:
                width, height = image.size
            root = next(p['worldRoot'] for p in plan['props'] if p['name'] == name)
            points = []
            for px in (region[0], region[2]):
                for py in (region[1], region[3]):
                    sx, sy = (px / width - .5) * draw[0], (1 - py / height) * draw[1]
                    points.append([root[0] + (sx + 2 * sy) / math.sqrt(2),
                                   root[1] + (-sx + 2 * sy) / math.sqrt(2)])
            count = 0
            min_clearance = float('inf')
            for py in range(region[1], region[3] + 1):
                for px in range(region[0], region[2] + 1):
                    sx, sy = (px / width - .5) * draw[0], (1 - py / height) * draw[1]
                    x, y = root[0] + (sx + 2 * sy) / math.sqrt(2), root[1] + (-sx + 2 * sy) / math.sqrt(2)
                    for solid in plan['protected']['solids']:
                        lo, hi = solid['minWorld'], solid['maxWorld']
                        if lo[0] <= x <= hi[0] and lo[1] <= y <= hi[1]:
                            raise ValueError('Retained prop base intersects solid: ' + name + '/' + solid['id'])
                        dx, dy = max(lo[0] - x, 0, x - hi[0]), max(lo[1] - y, 0, y - hi[1])
                        min_clearance = min(min_clearance, math.hypot(dx, dy))
                    # Source is two pixels per world unit, top-left raster.
                    pixel = material.getpixel((int(x * 2), int((2304 - y) * 2)))
                    if pixel != plan['materialIDs']['sidewalk']:
                        raise ValueError('Retained prop base not entirely on sidewalk: ' + name)
                    count += 1
            results.append(dict(name=name, source=str(source.relative_to(ROOT)),
                                sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                registeredFrontRoot=root, sourceBaseConservativeRect=region,
                                transformedRegionWorld=points, testedSourceSamples=count,
                                minimumSolidClearanceWorld=min_clearance,
                                entireRegionOnSidewalk=True))
    return {'status': 'CONSERVATIVE_RASTER_BASE_CLEARANCE_VERIFIED',
            'method': 'Manual visual base-region identification, full-region sampling with independent inverse D108',
            'limits': 'Not mesh-derived contacts, exact alpha contour, canopy clearance, native visibility or owner acceptance. Registered front vertex differs from physical trunk center.',
            'props': results}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
