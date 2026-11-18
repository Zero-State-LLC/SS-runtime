"""Author attempt 01 explicit geometry. Writes NEW output only, never historical sources."""
import json, math, hashlib
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
V8=ROOT/'docs/review/footprint-ground-repair-20261116'
V7=ROOT/'docs/review/building-perspective-detail-20261116'
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    data=json.dumps(v,indent=2)+'\n'
    if p.exists() and p.read_text()!=data: raise RuntimeError('Immutable authored output exists: '+str(p))
    p.write_text(data)
def prism(name,kind,polygon,height):
    root=[sum(p[k] for p in polygon)/len(polygon) for k in (0,1)]
    points=[[p[0]-root[0],p[1]-root[1],0] for p in polygon]
    faces=[]
    faces.append(dict(name='cap',vertices=[[p[0],p[1],height] for p in points],normal=[0,0,1],uv=[[p[0]/39,p[1]/39] for p in polygon],material='cap'))
    for i,a in enumerate(points):
        b=points[(i+1)%len(points)];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        # CCW polygon: outside normal is right of edge. Horizontal courses and world-unit block widths.
        faces.append(dict(name='wall-'+str(i),vertices=[a,b,[b[0],b[1],height],[a[0],a[1],height]],normal=[dy/length,-dx/length,0],uv=[[0,height/9],[length/18,height/9],[length/18,0],[0,0]],material='masonry' if kind=='blocked-base' else 'curb'))
    return dict(id=name,kind=kind,worldPosition=root,contactLocal=points,heightWorld=height,faces=faces)
def build():
    plan=load(V8/'plan/plan.json')
    sprites=[prism('v9-blocked-kiosk-base','blocked-base',[[512,640],[551,640],[512,679]],18)]
    # Partition existing semantic strip into short axis-aligned blocks. Exact half-world raster cells.
    bounds=[452,572,984,796]
    ids=Image.open(V8/'plan/material-ids.png');px=ids.load();used=set();rects=[]
    xlo,ylo,xhi,yhi=[int(v*2) for v in bounds]
    for y in range(ylo,yhi):
        for x in range(xlo,xhi):
            if (x,y) in used or px[x,4607-y]!=2:continue
            width=1
            while width<48 and x+width<xhi and (x+width,y) not in used and px[x+width,4607-y]==2: width+=1
            height=1
            limit=48 if width<=8 else 8
            while height<limit and y+height<yhi and all((xx,y+height) not in used and px[xx,4607-y-height]==2 for xx in range(x,x+width)):height+=1
            used.update((xx,yy) for yy in range(y,y+height) for xx in range(x,x+width))
            rects.append([x/2,y/2,(x+width)/2,(y+height)/2])
    for i,(x0,y0,x1,y1) in enumerate(rects):
        sprites.append(prism('v9-curb-'+str(i).zfill(3),'curb-relief',[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],3))
    geom=dict(schema='blocked-base-curb-geometry-009',attempt=1,pixelsPerWorldUnit=4,paddingPixels=4,curbRegionWorld=bounds,baseEnvelopeWorld=[512,640,640,768],baseTriangleWorld=[[512,640],[551,640],[512,679]],sprites=sprites,props=plan['props'],presentationOnly=True)
    dump(HERE/'geometry.json',geom)
    dump(HERE/'materials.json',dict(schema='blocked-base-curb-materials-009',input=str((V7/'context/inputs/facade.png').relative_to(ROOT)),crop=[0,605,523,774],tilePixels=[72,36],mortar=[74,70,59],capTint=[0.90,0.89,0.84],curbTint=[0.84,0.85,0.82],pixelSampling='nearest',courseHeightWorld=9,blockWidthWorld=18))
    paths=[p for p in V8.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [V7/'context/replay.py',V7/'kiosk/baseline_renderer.py',V7/'context/inputs/facade.png',V7/'kiosk/inputs/benchmark.png']
    assembly=load(V8/'scene/assembly.json')
    paths += [ROOT/s['image']['path'] for s in assembly['sources']]
    dump(HERE/'baseline-sha256.json',{str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))})
    print('Authored',len(sprites),'supplemental sprites, semantic curb rectangles',len(rects))
if __name__=='__main__':build()
