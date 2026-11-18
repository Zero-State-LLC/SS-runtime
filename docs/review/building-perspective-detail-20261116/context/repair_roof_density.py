"""One bounded source correction: replace stretched roof UVs with 128-world-unit panels.
Reads immutable attempt-01 geometry. No ground/contact/height/material pixel change.
"""
import copy
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TILE = 128

def correct(original):
    result = copy.deepcopy(original)
    result['roofTileWorldUnits'] = TILE
    for building in result['buildings']:
        faces = []
        rx, ry = building['worldPosition']
        for face in building['faces']:
            if face['material'] != 'roof' or face['normal'] != [0, 0, 1]:
                faces.append(face)
                continue
            points = face['vertices']
            x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
            y0, y1 = min(p[1] for p in points), max(p[1] for p in points)
            z = points[0][2]
            assert all(p[2] == z for p in points)
            xs = [x0] + [k*TILE-rx for k in range(math.floor((x0+rx)/TILE)+1, math.ceil((x1+rx)/TILE))] + [x1]
            ys = [y0] + [k*TILE-ry for k in range(math.floor((y0+ry)/TILE)+1, math.ceil((y1+ry)/TILE))] + [y1]
            for i, (left, right) in enumerate(zip(xs, xs[1:])):
                for j, (bottom, top) in enumerate(zip(ys, ys[1:])):
                    tx = math.floor(((left+right)/2+rx)/TILE)*TILE
                    ty = math.floor(((bottom+top)/2+ry)/TILE)*TILE
                    uv = [[(x+rx-tx)/TILE, 1-(y+ry-ty)/TILE] for x,y in [(left,top),(right,top),(right,bottom),(left,bottom)]]
                    faces.append(dict(name=face['name']+f'/world-tile-{i}-{j}',
                        vertices=[[left,top,z],[right,top,z],[right,bottom,z],[left,bottom,z]],
                        normal=[0,0,1], uv=uv, material='roof'))
        building['faces'] = faces
    return result

if __name__ == '__main__':
    original = json.loads((HERE/'attempt-01/geometry.json').read_text())
    result = correct(original)
    (HERE/'geometry.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'roofTileWorldUnits':TILE,'buildings':len(result['buildings']),
        'beforeFaces':sum(len(b['faces']) for b in original['buildings']),
        'afterFaces':sum(len(b['faces']) for b in result['buildings'])}))
