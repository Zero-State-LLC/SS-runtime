#!/usr/bin/env python3
"""Editable plan extraction. Reads immutable V7, writes only this directory."""
import hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
V7=ROOT/'docs/review/building-perspective-detail-20261116'
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def hull(points):
    p=sorted(set(map(tuple,points)))
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    halves=[]
    for seq in (p,p[::-1]):
        h=[]
        for q in seq:
            while len(h)>1 and cross(h[-2],h[-1],q)<=1e-7:h.pop()
            h.append(q)
        halves.append(h[:-1])
    return [list(p) for p in halves[0]+halves[1]]
def main():
    rec=load(V7/'scene/native-capture-v7/source-scene-records.json')
    c=next(c for c in rec['captures'] if c['arm']=='candidate' and c['zoom']==1)
    a=load(V7/'scene/assembly.json')
    geo=load(V7/'context/geometry.json')
    regs={r['solidID']:r for r in load(V7/'context/registration.json')}
    buildings=[]
    for s in c['solids']:
        if not s['id'].startswith('solid-'):continue
        lo,hi=s['minWorld'],s['maxWorld']; rect=[lo,[hi[0],lo[1]],hi,[lo[0],hi[1]]]
        b=dict(s,foundationWorld=rect,sidewalkOutsetWorld=24,curbWidthWorld=4,
               meshContactStatus='unavailable-retained-raster-no-mesh',actualContactWorld=[],contactLandmarks=[],virtualCorners=[],
               baseTreatment='solid-envelope mineral foundation, not an assertion of legacy mesh contact')
        if s['id'] in regs:
            g=next(g for g in geo['buildings'] if g['solidID']==s['id']);r=regs[s['id']]
            points=[[v[0]+g['worldPosition'][0],v[1]+g['worldPosition'][1]] for f in g['faces'] for v in f['vertices'] if abs(v[2])<1e-8]
            b['actualContactWorld']=hull(points);b['meshContactStatus']='actual-z0-face-vertices'
            b['meshEvidence']='context/geometry.json';b['baseTreatment']='retain actual full rectangular contact plinth, add ground foundation collar only'
            b['contactLandmarks']=[dict(world=p,sourcePixelsTopLeft=[r['rootPixelsTopLeft'][0]+4*((p[0]-r['worldPosition'][0])-(p[1]-r['worldPosition'][1]))/math.sqrt(2),r['rootPixelsTopLeft'][1]-4*((p[0]-r['worldPosition'][0])+(p[1]-r['worldPosition'][1]))/(2*math.sqrt(2))],provenance='actual-z0-mesh-vertex') for p in b['actualContactWorld']]
        elif s['id']=='solid-03-transit-kiosk':
            m=load(V7/'kiosk/output/mesh.json');r=load(V7/'kiosk/output/registration.json')
            points=[[v[0]+512,v[1]+640] for v in m['vertices'] if abs(v[2])<1e-8]
            b['actualContactWorld']=hull(points);b['meshContactStatus']='actual-z0-face-vertices';b['meshEvidence']='kiosk/output/mesh.json'
            b['virtualCorners']=[dict(world=[512,640],reason='omitted by actual chamfer39; blocked authoritative corner, NOT mesh vertex')]
            b['baseTreatment']='new mineral foundation fills blocked chamfer triangle; dark actual-contact seam separates existing mesh from infill; no door/path marking'
            b['contactLandmarks']=[dict(world=p,sourcePixelsTopLeft=[500+5*((p[0]-512)-(p[1]-640))/math.sqrt(2),1160-5*((p[0]-512)+(p[1]-640))/(2*math.sqrt(2))],provenance='actual-z0-mesh-vertex') for p in b['actualContactWorld']]
        buildings.append(b)
    protected={k:c[k] for k in ['solids','cameraRoot','cameraFieldOrigin','cameraFieldAngleMilli','cameraHeadingMilli','cameraRange','centerWorld','controlsRetained']}
    protected['actors']=[x for x in c['preprojectionInventory'] if not x['name'].startswith('benchmark-prop-')]
    p=dict(schema='footprint-ground-plan-008',status='FIRST_PREVIEW_NOT_VISUALLY_ACCEPTED',attempt=1,
        registration=dict(canvasPixels=[4608,4608],rootPixelsTopLeft=[0,4608],worldPosition=[0,0],drawSizeWorld=[2304,2304],kind='ground',coordinates='WORLD_X_RIGHT_Y_UP_SOURCE_TOP_LEFT'),
        arenaClipWorld=[0,0,2304,1536],protected=protected,buildings=buildings,
        layout=dict(rule='union-building-outsets-and-plaza; foundations win, then sidewalk, curb, road',plazas=[dict(name='transit-civic-apron',bounds=[456,600,980,752])],sidewalkOutsetWorld=24,curbWidthWorld=4,foundationCollarWorld=3,tileSizeWorld=[32,24]),
        props=[dict(name='benchmark-prop-0',oldWorldRoot=[691,639],worldRoot=[691,639],contactRadiusWorld=5,shadowRadiusWorld=8,shadowAlphaMax=.22,sourceArt='unchanged',groundMaterial='sidewalk'),dict(name='benchmark-prop-1',oldWorldRoot=[858,780],worldRoot=[858,716],contactRadiusWorld=8,shadowRadiusWorld=16,shadowAlphaMax=.22,sourceArt='unchanged',groundMaterial='sidewalk')],
        outputs=dict(ground='ground.png',materialIDs='material-ids.png',editable='ground.svg',preview='first-plan-preview.png'),
        materialIDs=dict(road=1,curb=2,sidewalk=3,foundation=4),
        limits=['Presentation material is not gameplay walkability.','No actual mesh contour can be recovered honestly from legacy raster bounds. Nine retained raster buildings explicitly have unknown actual contact; their envelopes still receive foundation/sidewalk/curb treatment.','No visual acceptance or native execution claimed.','Camera, Player, authoritative solids, framing and controls must remain V7.','Only ground mineral infill/contact seams and decorative tree root change; all existing source art bytes remain unchanged.'])
    save('plan.json',p)
    save('v7-immutable-sha256.json',{str(f.relative_to(ROOT)):sha(f) for f in sorted(V7.rglob('*')) if f.is_file() and '__pycache__' not in f.parts})
    print('plan.json ready:',len(buildings),'building envelopes;',sum(bool(b['actualContactWorld']) for b in buildings),'actual mesh contours')
if __name__=='__main__':main()
