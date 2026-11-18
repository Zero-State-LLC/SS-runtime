"""Bounded authored elevation relief. Pillow only, no image generation or random texture."""
import argparse, copy, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw
import baseline_renderer as base
HERE=Path(__file__).resolve().parent

def load(p): return json.loads(p.read_text())
def dump(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def author(config):
    old=load(HERE/'inputs/baseline-mesh.json')
    mesh={'schema':2,'vertices':[],'faces':[], 'height':132,'chamfer':39,
          'projection':'D108 unchanged: (x-y)/sqrt2, (x+y)/(2sqrt2), upright z',
          'footprint':[128,128], 'worldRoot':[512,640], 'authoring':'Piecewise planar relief with explicit painted-elevation UV correspondence'}
    def face(name,verts,uv,material):
        n=len(mesh['vertices'])
        mesh['vertices'].extend(verts)
        mesh['faces'].append(dict(name=name,indices=list(range(n,n+len(verts))),uv=uv,material=material,hidden=False))
    # Each panel's world endpoints are authoritative original footprint edges.
    for wall in old['faces']:
        if wall['material']=='roof': continue
        a,b=[old['vertices'][i] for i in wall['indices'][:2]]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        inward=(-dy/length,dx/length)
        door=wall['material']=='door'
        xs=config['doorX'] if door else config['facadeX']
        ys=config['rows']
        width=320 if door else 523
        def point(u,v,depth):
            return [a[0]+dx*u+inward[0]*depth,a[1]+dy*u+inward[1]*depth,132*(1-v)]
        def depth(x,y):
            # Top painted cornice becomes genuine stepped profile, kept inside bounds.
            if y<30: return 0.0
            if y<54: return 1.1
            if y<142:
                centers=([45,160,275] if door else [48,158,268,378,488])
                return .65 if any(abs(x-c)<18 for c in centers) else 2.4
            if y<174: return .25
            if y<230: return .65
            if door:
                if x<66 or x>254: return .6 if y<590 else 0.0
                if y<615: return config['doorRecess']
                if y<670: return 5.5
                if y<729: return 2.8
                return 0.0
            pilaster=x<72 or 220<x<305 or x>452
            if y<518: return .6 if pilaster else config['windowRecess']
            if y<590: return .1 if pilaster else 1.0
            return 0.0
        cells={}
        for j,(y0,y1) in enumerate(zip(ys,ys[1:])):
            for i,(x0,x1) in enumerate(zip(xs,xs[1:])):
                d=depth((x0+x1)/2,(y0+y1)/2)
                cells[i,j]=d
                u0,u1=x0/width,x1/width
                v0,v1=y0/774,y1/774
                # Vertex order gives the original outward normal.
                uv=[[u0,v1],[u1,v1],[u1,v0],[u0,v0]]
                face(f'{wall["name"]}-panel-{i}-{j}',[point(u,v,d) for u,v in uv],uv,wall['material'])
        # Explicit returns between every differing depth, rather than floating overlays.
        for (i,j),d in cells.items():
            x0,x1=xs[i]/width,xs[i+1]/width
            y0,y1=ys[j]/774,ys[j+1]/774
            if i+1<len(xs)-1:
                e=cells[i+1,j]
                if d!=e:
                    verts=[point(x1,y1,d),point(x1,y1,e),point(x1,y0,e),point(x1,y0,d)]
                    uv=[[x1,y1],[min(1,x1+.008),y1],[min(1,x1+.008),y0],[x1,y0]]
                    # Winding naturally follows the signed depth step.
                    face(f'{wall["name"]}-jamb-{i}-{j}',verts,uv,wall['material'])
            if j+1<len(ys)-1:
                e=cells[i,j+1]
                if d!=e:
                    verts=[point(x0,y1,d),point(x1,y1,d),point(x1,y1,e),point(x0,y1,e)]
                    uv=[[x0,y1],[x1,y1],[x1,min(1,y1+.008)],[x0,min(1,y1+.008)]]
                    # Below protrudes => visible upward tread, above protrudes => underside.
                    verts.reverse();uv.reverse()
                    face(f'{wall["name"]}-ledge-{i}-{j}',verts,uv,wall['material'])
    outer=[old['vertices'][i][:2] for i in range(5)]
    inset=config['parapetWidth']
    # Exact offset of x=0,y=0,x=128,y=128,x+y=39, not centroid scaling.
    k=39+inset*math.sqrt(2)
    inner=[[k-inset,inset],[128-inset,inset],[128-inset,128-inset],[inset,128-inset],[inset,k-inset]]
    for i in range(5):
        j=(i+1)%5
        cap=[outer[i]+[132],outer[j]+[132],inner[j]+[132],inner[i]+[132]]
        # Authored stone strip, not roof tile texture, on horizontal coping.
        face(f'parapet-cap-{i}',cap,[[0,0],[1,0],[1,.038],[0,.038]],'facade')
        verts=[inner[i]+[config['roofZ']],inner[j]+[config['roofZ']],inner[j]+[132],inner[i]+[132]]
        verts.reverse()
        face(f'parapet-inner-{i}',verts,[[0,.038],[1,.038],[1,.07],[0,.07]],'facade')
    face('recessed-roof',[p+[config['roofZ']] for p in inner],[[x/128,y/128] for x,y in inner],'roof')
    face('floor',[p+[0] for p in reversed(outer)],[[x/128,y/128] for x,y in reversed(outer)],'roof')
    return mesh

def render(mesh,textures):
    """Triangle rasterization with per-pixel depth, affine UV, analytic geometry coverage."""
    from array import array
    reg=base.registration(mesh)
    w,h=reg['sourceCanvas'];root=reg['sourceRoot']
    image=Image.new('RGBA',(w,h));pixels=image.load()
    depth=array('f',[-float('inf')])*(w*h)
    for f in mesh['faces']:
        vs=[mesh['vertices'][i] for i in f['indices']]
        n=base.normal(*vs[:3])
        if -n[0]-n[1]+math.sqrt(.5)*n[2]<=1e-8: continue
        ps=[tuple(base.raw(v)[k]+root[k] for k in (0,1)) for v in vs]
        source=textures[f['material']]
        texture,pad=base.clamped_texture(source)
        uv=[(pad+u*(source.width-1),pad+v*(source.height-1)) for u,v in f['uv']]
        ds=[-x-y+math.sqrt(.5)*z for x,y,z in vs]
        for j in range(1,len(vs)-1):
            ids=[0,j,j+1];points=[ps[i] for i in ids]
            if abs((points[1][0]-points[0][0])*(points[2][1]-points[0][1])-(points[2][0]-points[0][0])*(points[1][1]-points[0][1]))<1e-8:continue
            left=max(0,math.floor(min(p[0] for p in points)));top=max(0,math.floor(min(p[1] for p in points)))
            right=min(w,math.ceil(max(p[0] for p in points))+1);bottom=min(h,math.ceil(max(p[1] for p in points))+1)
            local=[(x-left,y-top) for x,y in points]
            c=base.coefficients(local,[uv[i][0] for i in ids])+base.coefficients(local,[uv[i][1] for i in ids])
            tile=texture.transform((right-left,bottom-top),Image.Transform.AFFINE,c,Image.Resampling.BICUBIC)
            mask=Image.new('1',tile.size);ImageDraw.Draw(mask).polygon(local,fill=1)
            tc=tile.load();mc=mask.load()
            aa,bb,cc=base.coefficients(local,[ds[i] for i in ids])
            for yy in range(bottom-top):
                for xx in range(right-left):
                    if not mc[xx,yy]:continue
                    d=aa*xx+bb*yy+cc;idx=(top+yy)*w+left+xx
                    if d>=depth[idx]-1e-5:
                        depth[idx]=d;pixels[left+xx,top+yy]=tc[xx,yy]
    return image

def add_ground_boundary(reg):
    corners=[[512,640],[640,640],[640,768],[512,768]]
    root=reg['rootPixelsTopLeft']
    reg['groundPixelsTopLeft']=[[root[0]+5*((x-512)-(y-640))/math.sqrt(2),root[1]-5*((x-512)+(y-640))/(2*math.sqrt(2))] for x,y in corners]
    reg['groundBoundaryWorld']=corners
    reg['groundBoundaryProvenance']=['virtual authoritative rectangle corner, omitted by visible chamfer39; not visible mesh contact','authored footprint corner','authored footprint corner','authored footprint corner']
    return reg

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    config=load(HERE/'geometry-controls.json')
    mesh=author(config);dump(out/'mesh.json',mesh)
    spec=load(HERE/'materials.json');tex=base.textures(spec)
    (out/'textures').mkdir(exist_ok=True)
    for name,im in tex.items():im.save(out/'textures'/f'{name}.png')
    reg=base.registration(mesh)
    reg.update(canvasPixels=reg['sourceCanvas'],rootPixelsTopLeft=reg['sourceRoot'],worldPosition=[512,640],drawSizeWorld=[v*.2 for v in reg['sourceCanvas']],status='FIRST_SAMPLE_AWAITING_COORDINATOR_VISUAL_REVIEW')
    add_ground_boundary(reg)
    dump(out/'registration.json',reg)
    image=render(mesh,tex);image.save(out/'building-alpha.png')
    roof=load(HERE/'roof-layer.json');roof['localWorldAnchor'][2]=config['roofZ']
    dump(out/'roof-layer-registration.json',base.roof_layer_registration(roof,reg))
    layer=base.render_roof_layer(roof,reg);layer.save(out/'roof-layer-alpha.png')
    image=Image.alpha_composite(image,layer);image.save(out/'source-full.png')
    native=image.resize(tuple(round(v*.2) for v in image.size),Image.Resampling.LANCZOS)
    half=image.resize(tuple(round(v*.1) for v in image.size),Image.Resampling.LANCZOS)
    native.save(out/'native-alpha.png');half.save(out/'half-alpha.png')
    plate=Image.new('RGB',(1100,480),'#383b3c');d=ImageDraw.Draw(plate)
    with Image.open(HERE/'inputs/benchmark.png') as ref:
        ref=ref.convert('RGB');ref.thumbnail((620,400));plate.paste(ref,(0,50))
    plate.paste(native,(650,50),native);plate.paste(half,(940,50),half)
    d.text((10,15),'FULL BENCHMARK, uncropped',fill='white')
    d.text((650,15),'FIRST SAMPLE: native / half',fill='white')
    d.text((650,410),'Source preview, NOT native capture or acceptance',fill='white')
    plate.save(out/'first-sample-comparison.png')
    base.export_obj(mesh,out)
    paths=['geometry-controls.json','materials.json','roof-layer.json','replay.py','baseline_renderer.py']+[str(p.relative_to(HERE)) for p in sorted((HERE/'inputs').glob('*'))]
    dump(out/'manifest.json',dict(status='FIRST_SAMPLE_NOT_ACCEPTED',inputs={p:sha(HERE/p) for p in paths},outputs={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'}))
    print(json.dumps({'faces':len(mesh['faces']),'canvas':reg['canvasPixels'],'root':reg['rootPixelsTopLeft'],'drawSizeWorld':reg['drawSizeWorld'],'output':str(out)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE/'output');a=p.parse_args();build(a.out)
