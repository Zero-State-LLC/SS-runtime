"""One untextured architectural Z proposal. Offline source proxy, never native pixels.
See DESIGN.md for reuse decisions and immutable aesthetic budget.
"""
import argparse
from array import array
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = ROOT / 'docs/review/building-perspective-detail-20261116'
V9 = ROOT / 'docs/review/blocked-base-curb-relief-20261116/scene'
ZOOMS = (1, 1.25, 1.4)
SIZE = (2112, 978)
PPU = 3
SOURCE_PPU = 3
INPUTS = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    INPUTS[str(path.relative_to(ROOT))] = sha(path)
    return json.loads(path.read_text())


def image(path):
    INPUTS[str(path.relative_to(ROOT))] = sha(path)
    return Image.open(path).convert('RGBA')


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def module(name, path):
    INPUTS[str(path.relative_to(ROOT))] = sha(path)
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def project(p):
    x, y, z = p
    return [(x-y)/math.sqrt(2), (x+y)/(2*math.sqrt(2))+z]


def screen(p, zoom):
    q, center = project(p), project([684,724,0])
    return [PPU*(352+zoom*(q[0]-center[0])), PPU*(163-zoom*(q[1]-center[1]))]


def extract():
    kiosk = read(OLD/'kiosk/output/mesh.json')
    context = read(OLD/'context/geometry.json')
    faces = []
    for f in kiosk['faces']:
        color = 'wall'
        if f['material'] == 'roof':
            color = 'roof'
        if f['name'].startswith('parapet'):
            color = 'cornice'
        if '-panel-' in f['name']:
            col, row = map(int, f['name'].split('-panel-')[1].split('-'))
            if row <= 3:
                color = 'cornice'
            if f['material'] == 'door' and 3 <= col <= 5 and 6 <= row <= 10:
                color = 'opening'
            if f['material'] != 'door' and col in (3,4,5,9,10,11) and row in (6,7):
                color = 'opening'
        faces.append(dict(name=f['name'], vertices=[kiosk['vertices'][i] for i in f['indices']], material=f['material'], flatClass=color))
    buildings = [dict(solidID='solid-03-transit-kiosk', nodeName='benchmark-building', worldPosition=kiosk['worldRoot'], footprintWorld=dict(minWorld=[512,640],maxWorld=[640,768]), contactLocal=[[39,0,0],[128,0,0],[128,128,0],[0,128,0],[0,39,0]], faces=faces, authoredHeight=132)]
    for b in context['buildings']:
        b = copy.deepcopy(b)
        for f in b['faces']:
            f['flatClass'] = ('opening' if f['material']=='window' else 'roof' if f['material'] in ('roof','metal') else 'cornice' if f['material'] in ('cornice','frieze') else 'wall')
        buildings.append(b)
    return buildings


def mapping(b):
    role = b['solidID']
    if 'kiosk' in role:
        old = sorted({v[2] for f in b['faces'] for v in f['vertices']})
        new = [0,5,10,18,21,25,32,60,80,82,88,94,99,100,101,104]
        assert len(old)==len(new)==16
        return list(zip(old,new))
    if 'residential' in role:
        return list(zip([0,5,7,10,11,13,15,50,53,55,57,58,59,61,96,99,108,112,113,119,121,134,136], [0,5,7,10,16,18,20,60,63,70,72,73,84,86,126,129,146,150,151,155,157,170,172]))
    if 'civic-west' in role:
        return list(zip([0,5,7,10,11,13,15,111,113,114,119,138,142,143,146,149,151,156], [0,5,7,10,16,18,20,84,86,87,94,116,120,121,124,125,127,134]))
    return list(zip([0,5,9,13,16,31,34], [0,3,6,9,12,32,35]))


def proposed(current):
    result = copy.deepcopy(current)
    for a,b in zip(current,result):
        m = dict(mapping(a))
        assert set(m)=={v[2] for f in a['faces'] for v in f['vertices']}
        for f in b['faces']:
            for v in f['vertices']:
                v[2] = m[v[2]]
        b['authoredHeight'] = m[a['authoredHeight']]
    return result


def normal(vs):
    a,b,c = vs[:3]
    u=[b[i]-a[i] for i in range(3)]
    v=[c[i]-a[i] for i in range(3)]
    return [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]


def render(b):
    """ADAPT kiosk/replay.py triangle coverage and context/replay.py geometric depth.
    No UV or raster facade input is consulted. Face classes are constant colors.
    """
    pts=[project(v) for f in b['faces'] for v in f['vertices']]+[[0,0]]
    left=math.floor(min(v[0] for v in pts)*SOURCE_PPU)-12
    right=math.ceil(max(v[0] for v in pts)*SOURCE_PPU)+12
    bottom=math.floor(min(v[1] for v in pts)*SOURCE_PPU)-12
    top=math.ceil(max(v[1] for v in pts)*SOURCE_PPU)+12
    w,h=right-left,top-bottom
    out=Image.new('RGBA',(w,h))
    pixels=out.load()
    depths=array('f',[-1e30])*(w*h)
    palette={'wall':(188,188,181),'roof':(161,164,163),'opening':(78,90,93),'cornice':(213,211,201)}
    for f in b['faces']:
        vs=f['vertices']
        n=normal(vs)
        if -n[0]-n[1]+math.sqrt(2)*n[2]<=1e-8:
            continue
        shade=1 if n[2]>0 else (.88 if abs(n[1])>=abs(n[0]) else .75)
        color=tuple(round(x*shade) for x in palette[f['flatClass']])+(255,)
        ps=[(project(v)[0]*SOURCE_PPU-left,top-project(v)[1]*SOURCE_PPU) for v in vs]
        ds=[-v[0]-v[1]+math.sqrt(2)*v[2] for v in vs]
        for j in range(1,len(vs)-1):
            ids=(0,j,j+1)
            (ax,ay),(bx,by),(cx,cy)=[ps[i] for i in ids]
            bx,by,cx,cy=bx-ax,by-ay,cx-ax,cy-ay
            determinant=bx*cy-by*cx
            if abs(determinant)<1e-9:
                continue
            bounds=[ps[i] for i in ids]
            x0=max(0,math.floor(min(p[0] for p in bounds)))
            x1=min(w,math.ceil(max(p[0] for p in bounds)))
            y0=max(0,math.floor(min(p[1] for p in bounds)))
            y1=min(h,math.ceil(max(p[1] for p in bounds)))
            for y in range(y0,y1):
                for x in range(x0,x1):
                    dx,dy=x+.5-ax,y+.5-ay
                    u=(dx*cy-dy*cx)/determinant
                    v=(dy*bx-dx*by)/determinant
                    if u < -1e-8 or v < -1e-8 or u+v > 1+1e-8:
                        continue
                    d=ds[0]+u*(ds[j]-ds[0])+v*(ds[j+1]-ds[0])
                    index=y*w+x
                    if d>=depths[index]-.0001:
                        depths[index]=d
                        pixels[x,y]=color
    return out, dict(canvasPixels=[w,h],rootPixelsTopLeft=[-left,top],worldPosition=b['worldPosition'],drawSizeWorld=[w/SOURCE_PPU,h/SOURCE_PPU])


def registered_layer(im, reg, zoom):
    target=tuple(round(v*PPU*zoom) for v in reg['drawSizeWorld'])
    resized=im.resize(target,Image.Resampling.BILINEAR)
    root=screen(reg['worldPosition']+[0],zoom)
    origin=[round(root[k]-reg['rootPixelsTopLeft'][k]*target[k]/reg['canvasPixels'][k]) for k in (0,1)]
    layer=Image.new('RGBA',SIZE)
    layer.alpha_composite(resized,tuple(origin))
    return layer


def actor_reg(a, im):
    return dict(canvasPixels=list(im.size),rootPixelsTopLeft=[im.width*a['anchor'][0],im.height*(1-a['anchor'][1])],worldPosition=a['worldRoot'],drawSizeWorld=a['size'])


def offscreen(a,zoom):
    root=screen(a['worldRoot']+[0],zoom)
    w,h=[v*PPU*zoom for v in a['size']]
    x=root[0]-a['anchor'][0]*w
    y=root[1]-(1-a['anchor'][1])*h
    return x+w<0 or y+h<0 or x>SIZE[0] or y>SIZE[1]


def field_polygon(c):
    """ADAPT App/CameraFieldGeometry.swift:22-72, same clipped rays and sign."""
    raw=list(map(int,re.findall(r'raw: (\d+)',c['cameraFieldOrigin'])))
    assert len(raw)==2
    origin=[v/256 for v in raw]
    base=-c['cameraHeadingMilli']*math.pi/180000
    half=c['cameraFieldAngleMilli']*math.pi/360000
    count=max(1,math.ceil(c['cameraFieldAngleMilli']/1000))
    angles=[-half+2*half*i/count for i in range(count+1)]
    boxes=[s['minWorld']+s['maxWorld'] for s in c['solids']]
    for box in boxes:
        for x in (box[0],box[2]):
            for y in (box[1],box[3]):
                a=math.atan2(y-origin[1],x-origin[0])-base
                relative=math.atan2(math.sin(a),math.cos(a))
                angles.extend(relative+off for off in (-1e-7,0,1e-7) if abs(relative+off)<=half)
    result=[origin]
    for a in sorted(angles):
        dx,dy=math.cos(base+a),math.sin(base+a)
        reach=c['cameraRange']
        for box in boxes:
            near,far=-math.inf,math.inf
            valid=True
            for o,d,lo,hi in [(origin[0],dx,box[0],box[2]),(origin[1],dy,box[1],box[3])]:
                if abs(d)<1e-12:
                    if o<lo or o>hi:
                        valid=False
                else:
                    u,v=(lo-o)/d,(hi-o)/d
                    near=max(near,min(u,v))
                    far=min(far,max(u,v))
            if valid and near<=far and far>=0:
                reach=min(reach,max(0,near))
        result.append([origin[0]+dx*reach,origin[1]+dy*reach])
    return result


def ground_source_uv(world, canvas, tile_units):
    """WorldRenderer.swift:461-464 crops the SQUARE tile, never stretches to arena."""
    return [world[0]*canvas[0]/tile_units, (1-world[1]/tile_units)*canvas[1]]


def ground_layer(ground,c,zoom,tile_units=2304):
    # Invert D108 and sample the square texture with its square tileUnits denominator.
    def uv(x,y):
        u=(x/PPU-352)/zoom
        v=(163-y/PPU)/zoom
        wx=684+(u+2*v)/math.sqrt(2)
        wy=724+(-u+2*v)/math.sqrt(2)
        return ground_source_uv([wx,wy],ground.size,tile_units)
    p,a,b=uv(0,0),uv(1,0),uv(0,1)
    coeff=tuple([a[0]-p[0],b[0]-p[0],p[0],a[1]-p[1],b[1]-p[1],p[1]])
    out=ground.transform(SIZE,Image.Transform.AFFINE,coeff,Image.Resampling.BILINEAR)
    field=Image.new('RGBA',SIZE)
    ImageDraw.Draw(field).polygon([tuple(screen(p+[0],zoom)) for p in field_polygon(c)],fill=(199,183,91,40))
    return Image.alpha_composite(out,field)


def labeled(im,text):
    out=Image.new('RGB',(im.width,im.height+30),(31,34,35))
    out.paste(im,(0,30))
    ImageDraw.Draw(out).text((8,9),text,fill='white')
    return out


def dimensions(current,proposal,player):
    alpha=player.getchannel('A').getbbox()
    ref=(336-alpha[1])/6
    rows=[]
    for a,b in zip(current,proposal):
        role=a['solidID']
        if 'kiosk' in role:
            measures={'facadeTop':[132,104],'roofDeck':[125,100],'parapetHeight':[7,4],'corniceZoneHeight':[132-107.7829457364341,10],'doorThreshold':[27.116279069767447,18],'doorHead':[92.77519379844962,80],'doorClearance':[92.77519379844962-27.116279069767447,62],'windowSill':[43.65891472868216,32],'windowHead':[92.77519379844962,80],'windowHeight':[92.77519379844962-43.65891472868216,48],'storeyHeight':[132,104],'doorRecessDepth':[8.2,8.2],'windowRecessDepth':[3.2,3.2]}
            door='Recessed entry aperture only, not gameplay traversal. Preserved blocked rectangle.'
        elif 'residential' in role:
            measures={'facadeTop':[112,150],'roofDeck':[112,150],'corniceZoneHeight':[13,11],'copingTop':[121,157],'chimneyTop':[136,172],'windowHeight':[35,40],'storeyPitch':[46,66],'groundWindowSill':[15,20],'groundWindowHead':[50,60],'upperWindowSill':[61,86],'upperWindowHead':[96,126]}
            door='NO EXPLICIT DOORWAY IN BASELINE MESH. Clearance cannot be inferred from windows. None invented.'
        elif 'civic-west' in role:
            measures={'facadeTop':[142,120],'roofDeck':[142,120],'corniceZoneHeight':[13,11],'copingTop':[151,127],'lanternTop':[156,134],'windowSill':[15,20],'windowHead':[111,84],'windowHeight':[96,64],'storeyHeight':[142,120]}
            door='NO EXPLICIT DOORWAY IN BASELINE MESH. Clearance unmeasurable. None invented.'
        else:
            measures={'platformHeight':[13,9],'railTop':[34,35],'railAbovePlatform':[21,26],'topRailThickness':[3,3],'firstStepHeight':[5,3],'secondStepRise':[4,3]}
            door='Not applicable: open dais, no facade, doorway, windows, story or roof.'
        lo,hi=a['footprintWorld']['minWorld'],a['footprintWorld']['maxWorld']
        measures['footprintWidth']=[hi[0]-lo[0]]*2
        measures['footprintDepth']=[hi[1]-lo[1]]*2
        rows.append(dict(solidID=role,doorwayQualification=door,dimensions={k:dict(current=v[0],proposed=v[1],delta=v[1]-v[0],currentPlayerRatio=v[0]/ref,proposedPlayerRatio=v[1]/ref) for k,v in measures.items()},verticalSubdivisionMap=[dict(current=x,proposed=y) for x,y in mapping(a)],xyUnchanged=True,root=a['worldPosition']))
    return dict(playerReference=dict(sourceAlphaBounds=list(alpha),rootToAlphaTopWorld=ref,fullAlphaHeightWorld=(alpha[3]-alpha[1])/6,qualification='Visual scale only, not physical human height or collision geometry.'),buildings=rows)


def build(out):
    if out.exists():
        raise RuntimeError('Output exists. Initial aesthetic proposal is immutable. Use no automatic rerender.')
    out.mkdir(parents=True)
    assembly=read(V9/'assembly.json')
    records=read(V9/'native-capture-v9/source-scene-records.json')
    c=next(c for c in records['captures'] if c['arm']=='candidate' and c['zoom']==1)
    depth=module('_architectural_retained_depth',ROOT/'docs/review/scene-qa-repair-20261116/native.py')
    order=depth.depth_order(c['depthItems'])
    assert order['order']==c['depthOrder'] and order['constraints']==c['depthConstraints']
    sources={s['role']:s for s in assembly['sources']}
    ground=image(ROOT/sources['ground-plan']['image']['path'])
    ground_registration=sources['ground-plan']['registration']
    assert ground_registration['drawSizeWorld']==[2304,2304]
    assert ground_registration['worldPosition']==[0,0]
    assert ground_registration['rootPixelsTopLeft']==[0,ground.height]
    assert sha(ROOT/sources['ground-plan']['image']['path'])==c['groundPlanWitness']['sourceSHA256']
    current=extract()
    proposal=proposed(current)
    dump(out/'current-geometry.json',current)
    dump(out/'proposed-geometry.json',proposal)
    building_names={b['nodeName'] for b in current}
    actor_sources={}
    omitted=[]
    for a in c['actors']:
        name=a['name']
        if name in building_names:
            continue
        if name in ('sprite-player','sprite-camera-3'):
            s=sources['player' if name=='sprite-player' else 'camera']
            path=ROOT/s['image']['path']
            assert sha(path)==s['image']['sha256']
        elif name in ('benchmark-prop-0','benchmark-prop-1'):
            path=ROOT/'AppTests/BenchmarkAssets'/('newsbox.png' if name.endswith('0') else 'tree.png')
            assert sha(path)==records['controlSHA256'][path.name]
        else:
            assert all(offscreen(a,z) for z in ZOOMS), 'Unmapped actor intersects crop: '+name
            omitted.append(a)
            continue
        im=image(path)
        actor_sources[name]=(im,actor_reg(a,im))
    for s in assembly['supplements']:
        path=V9/'native-inputs-v9'/s['file']
        assert sha(path)==s['sha256']
        actor_sources[s['nodeName']]=(image(path),s['registration'])
    rendered={}
    regs={}
    for arm,buildings in [('current',current),('proposed',proposal)]:
        rendered[arm]={}
        regs[arm]={}
        for b in buildings:
            im,reg=render(b)
            name=b['solidID']
            im.save(out/f'{arm}-{name}.png')
            rendered[arm][b['nodeName']]=(im,reg)
            regs[arm][b['nodeName']]=reg
            print('rendered',arm,name,im.size,flush=True)
    dump(out/'registrations.json',regs)
    report=dimensions(current,proposal,actor_sources['sprite-player'][0])
    dump(out/'dimensions.json',report)
    captures=[]
    benchmark=image(OLD/'kiosk/inputs/benchmark.png')
    benchmark.save(out/'original-full-benchmark.png')
    for zoom in ZOOMS:
        code=round(zoom*100)
        base=ground_layer(ground,c,zoom,ground_registration['drawSizeWorld'][0])
        base.save(out/f'nonbuilding-ground-proxy-z{code}.png')
        retained={name:registered_layer(im,reg,zoom) for name,(im,reg) in actor_sources.items()}
        layer_hashes={name:hashlib.sha256(im.tobytes()).hexdigest() for name,im in retained.items()}
        arms={}
        for arm in ('current','proposed'):
            layers=dict(retained)
            layers.update({name:registered_layer(im,reg,zoom) for name,(im,reg) in rendered[arm].items()})
            scene=base.copy()
            for name in order['order']:
                if name in layers:
                    scene=Image.alpha_composite(scene,layers[name])
            arms[arm]=scene
            scene.save(out/f'{arm}-z{code}.png')
            labeled(scene,f'{arm.upper()} GEOMETRY / SOURCE PROXY NOT NATIVE / z{zoom} / unchanged Player+Camera').save(out/f'{arm}-z{code}-labeled.png')
            # Per-arm retained layers permit exact reference equality checks, independent of occlusion.
            for name in ('sprite-player','sprite-camera-3'):
                retained[name].save(out/f'{arm}-{name}-z{code}.png')
        native=image(V9/f'native-capture-v9/source-scene-candidate-ordinary-z{code}-native.png')
        assert sha(V9/f'native-capture-v9/source-scene-candidate-ordinary-z{code}-native.png')==next(row for row in records['captures'] if row['arm']=='candidate' and row['zoom']==zoom)['pngSHA256']['-native']
        # All four panes are uniformly fitted, uncropped. Header text stays outside imagery.
        sheet=Image.new('RGB',(2112,1340),(31,34,35))
        panes=[(benchmark,'ORIGINAL FULL BENCHMARK, UNCROPPED',0,0),(native,f'IMMUTABLE V9 NATIVE BASELINE z{zoom}',1056,0),(arms['current'],f'CURRENT MESH / SOURCE PROXY z{zoom}',0,670),(arms['proposed'],f'PROPOSED MESH / SOURCE PROXY z{zoom}',1056,670)]
        for im,title,x,y in panes:
            fitted=im.copy()
            fitted.thumbnail((1056,600),Image.Resampling.LANCZOS)
            sheet.paste(fitted,(x+(1056-fitted.width)//2,y+35))
            ImageDraw.Draw(sheet).text((x+10,y+10),title,fill='white')
        ImageDraw.Draw(sheet).text((12,1320),'One proposal. SOURCE PROXY: HUD/controls and runtime shadow omitted; proxy field raster. No acceptance. Raster vent omitted in both arms.',fill='white')
        sheet.save(out/f'comparison-z{code}.png')
        captures.append(dict(zoom=zoom,retainedLayerSHA256=layer_hashes,groundProxyRGBA_SHA256=hashlib.sha256(base.tobytes()).hexdigest(),depthOrder=order['order']))
    dump(out/'scene-contract.json',dict(kind='SOURCE_PROXY_NOT_NATIVE',nativeEvidence=False,ownerAcceptance=False,attempt=1,zooms=list(ZOOMS),framing=c['framing'],centerWorld=c['centerWorld'],canvasPixels=list(SIZE),depthItems=c['depthItems'],depthOrder=order['order'],depthConstraints=order['constraints'],actors=c['actors'],supplementalActors=c['supplementalActors'],omittedOffscreenActors=omitted,cameraField={k:c[k] for k in ('cameraRoot','cameraFieldOrigin','cameraHeadingMilli','cameraFieldAngleMilli','cameraRange','fieldVisible')},fieldPolygonWorld=field_polygon(c),groundPlanWitness=c['groundPlanWitness'],groundSourceRegistration=ground_registration,groundTextureRect=[0,0,1,2/3],retainedControlAuthority=c['controlsRetained'],hudVisibleInNative=c['hudVisible'],hudAndControlsRendered=False,technicalCorrection='Square ground UV crop and raw frame packaging only. Initial failure preserved in attempt-01-ground-uv.',captures=captures,proxyLimitations=['HUD and touch controls omitted from source proxy, native comparison retains them','No native background pixels used in reconstructed arms','Native shadow omitted, no fabricated shadow substituted','Field path authority preserved but fill/antialiasing are proxy','Source actor sampling is Pillow, not native SpriteKit','Raster kiosk vent omitted from both untextured mesh arms','Unmapped legacy actors proven fully offscreen, retained in depth ordering','No inferred doorways on residential/civic meshes']))
    for path in [OLD/'kiosk/baseline_renderer.py',OLD/'kiosk/replay.py',OLD/'context/replay.py',OLD/'context/author.py',ROOT/'App/CameraFieldGeometry.swift',ROOT/'App/WorldRenderer.swift',ROOT/'AppTests/BlockedBaseCurbSceneTests.swift',ROOT/'AppTests/SceneQAReviewDepth.swift']:
        INPUTS[str(path.relative_to(ROOT))]=sha(path)
    dump(out/'manifest.json',dict(schema='architectural-source-comparison-001',attempt=1,nativeEvidence=False,acceptance=False,inputs=INPUTS,implementationSHA256=sha(Path(__file__)),outputs={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}))
    print('Complete: one geometry proposal, three zooms, source-proxy boundary explicit.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE/'output')
    build(parser.parse_args().out)
