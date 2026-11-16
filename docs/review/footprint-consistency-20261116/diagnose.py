#!/usr/bin/env python3
"""Read-only diagnosis of v7 footprint/ground semantics, not a new native capture."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
V7 = REVIEW / 'building-perspective-detail-20261116'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(x, y, layout):
    # Independent transcription of the retained signed-distance definition.
    # Classifies authored presentation material, not gameplay walkability.
    edge_x, edge_y, radius = (layout[k] for k in ('verticalEdgeX', 'horizontalEdgeY', 'radius'))
    cx, cy = edge_x - radius, edge_y + radius
    distance = math.hypot(x - cx, y - cy) - radius if x > cx and y < cy else max(x - edge_x, edge_y - y)
    return 'paving' if distance <= 0 else 'curb' if distance <= layout['curbWidth'] else 'road'


def diagnose():
    records_path = V7 / 'scene/native-capture-v7/source-scene-records.json'
    layout_path = REVIEW / 'paving-corner-review-20261116/source.json'
    assembly = load(V7 / 'scene/assembly.json')
    paving = next(s for s in assembly['sources'] if s['role'] == 'paving')
    root = HERE.parents[2]
    ground_path = root / paving['image']['path']
    if sha(ground_path) != paving['image']['sha256']:
        raise ValueError('Actual bound ground source drift')
    records = load(records_path)
    row = next(c for c in records['captures'] if c['arm'] == 'candidate' and c['zoom'] == 1)
    layout = load(layout_path)['corner']
    wanted = {b['solidID'] for b in assembly['buildings']}
    footprints = []
    for solid in row['solids']:
        if solid['id'] not in wanted:
            continue
        x0, y0 = solid['minWorld']
        x1, y1 = solid['maxWorld']
        counts = dict(paving=0, curb=0, road=0)
        for x in range(x0, x1):
            for y in range(y0, y1):
                counts[classify(x + .5, y + .5, layout)] += 1
        area = (x1 - x0) * (y1 - y0)
        footprints.append(dict(**solid, sampledWorldArea=area, materialArea=counts,
                               percent={k: 100 * v / area for k, v in counts.items()}))
    props = []
    for actor in row['actors']:
        if not actor['name'].startswith('benchmark-prop-'):
            continue
        x, y = actor['worldRoot']
        containing = [s['id'] for s in row['solids'] if s['minWorld'][0] < x < s['maxWorld'][0]
                      and s['minWorld'][1] < y < s['maxWorld'][1]]
        props.append(dict(name=actor['name'], worldRoot=[x, y], insideSolids=containing))
    kiosk = load(V7 / 'kiosk/output/registration.json')
    return dict(status='V7_FOOTPRINT_SEMANTIC_INCONSISTENCY_CONFIRMED_NOT_REPAIRED',
                scope='Whole authoritative footprints, including offcrop portions, sampled at one-world-unit cell centers',
                groundLayout=layout, footprints=footprints, props=props,
                kioskGroundCornerProvenance=kiosk['groundBoundaryProvenance'],
                inputSHA256={str(p.relative_to(root)): sha(p) for p in (records_path, layout_path, ground_path)},
                limits=['Ground material classification is not gameplay walkability.',
                        'Collision rectangles and visible architectural contact contours are different concepts.',
                        'V7 ground builder extends original world bounds only, retaining these curb semantics.',
                        'No source, capture, gameplay authority or historical validator was changed.'])


if __name__ == '__main__':
    print(json.dumps(diagnose(), indent=2))
