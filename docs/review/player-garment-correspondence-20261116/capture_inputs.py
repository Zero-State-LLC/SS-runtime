"""One-time exact tracked-input capture and explicit front-panel correspondence authoring."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = 'docs/review/player-baggy-south-source-20261116'

def main():
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    manifest = {}
    names = ['baggy-south.json', 'source/metadata.json', 'source/trouser-sheet.png',
             'south-baggy-neutral.png', 'source/south-neutral-original.png',
             'layers/original_upper.png', 'layers/original_boots.png']
    parts = json.loads(subprocess.check_output(['git', 'show', f'{commit}:{BASE}/baggy-south.json'], cwd=REPO))['parts']
    names += [f"components/{p['name']}.png" for p in parts]
    for name in names:
        source = f'{BASE}/{name}'
        data = subprocess.check_output(['git', 'show', f'{commit}:{source}'], cwd=REPO)
        target = HERE / 'inputs' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest[f'inputs/{name}'] = dict(commit=commit, path=source, sha256=hashlib.sha256(data).hexdigest(), decision='COPY_EXACT')
    surfaces = []
    for p in parts:
        w, h = p['resampledSize']
        x, y = p['translation']
        vertices = []
        # Pixel-edge mesh. Root-relative source-pixel coordinates, not recovered world geometry.
        for row in range(7):
            for col in range(5):
                u, v = col / 4, row / 6
                vertices.append(dict(position=[x + u*w - 192, 336 - y - v*h], uv=[u, v]))
        faces = []
        for row in range(6):
            for col in range(4):
                a = row*5 + col
                faces.extend([[a,a+1,a+6], [a,a+6,a+5]])
        surfaces.append(dict(id=p['name'], anatomicalSide=p['anatomicalSide'],
            material=f"inputs/components/{p['name']}.png", materialRasterSize=[w,h],
            sheetRegion=p['sheetRegion'], vertices=vertices, triangles=faces,
            correspondence='authored front-panel UV registration to generated component, not hidden texture recovery'))
    model = dict(schema=1, status='SOUTH_PILOT_AWAITING_COORDINATOR', canvas=[384,416],
        groundRoot=[192,336], sourcePixelsPerLogicalPoint=6,
        projection='front panel x=root.x+position.x; y=root.y-position.y',
        surfaces=surfaces, retainedLayers=['inputs/layers/original_boots.png','inputs/layers/original_upper.png'],
        hiddenSurfaces=[], authoredRegions='All mesh vertices/triangles and UV registration are newly authored. Paint is exact existing generated front material. No hidden sides/back authored or recovered.')
    (HERE/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (HERE/'garment.json').write_text(json.dumps(model,indent=2)+'\n')

if __name__ == '__main__':
    main()
