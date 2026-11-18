"""Deterministic D108 triangle rasterization. ADAPT citations in ADAPT.md."""
import argparse, importlib.util, json, math, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
context=module('v9_adapt_context',ROOT/'docs/review/building-perspective-detail-20261116/context/replay.py')
base=module('v9_adapt_triangle',ROOT/'docs/review/building-perspective-detail-20261116/kiosk/baseline_renderer.py')
project=context.project

def textures():
    spec=load(HERE/'materials.json')
    image=Image.open(ROOT/spec['input']).convert('RGB').crop(spec['crop']).resize(tuple(spec['tilePixels']),Image.Resampling.NEAREST)
    def tint(im,factors):return Image.merge('RGB',tuple(ch.point(lambda v,f=f:round(v*f)) for ch,f in zip(im.split(),factors)))
    cap=tint(image,spec['capTint']);curb=tint(image,spec['curbTint'])
    masonry=image.copy();d=ImageDraw.Draw(masonry);w,h=masonry.size
    d.line((0,0,w,0),fill=tuple(spec['mortar']),width=2);d.line((0,0,0,h),fill=tuple(spec['mortar']),width=2)
    d.line((2,2,w,2),fill=(164,151,124),width=1)
    dc=ImageDraw.Draw(curb);dc.line((0,0,0,h),fill=tuple(spec['mortar']),width=2)
    return {k:v.convert('RGBA') for k,v in dict(masonry=masonry,cap=cap,curb=curb).items()}

def render(sprite,spec,tex):
    scale=spec['pixelsPerWorldUnit'];points=[v for f in sprite['faces'] for v in f['vertices']]
    projected=[project(v) for v in points]+[[0,0]];pad=spec['paddingPixels']
    left=math.floor(min(p[0] for p in projected)*scale)-pad;right=math.ceil(max(p[0] for p in projected)*scale)+pad
    bottom=math.floor(min(p[1] for p in projected)*scale)-pad;top=math.ceil(max(p[1] for p in projected)*scale)+pad
    image=Image.new('RGBA',(right-left,top-bottom));pix=image.load();depth=[-1e30]*(image.width*image.height)
    visible=0
    for face in sprite['faces']:
        nx,ny,nz=face['normal']
        if -nx-ny+math.sqrt(2)*nz<=0:continue
        visible+=1;texture=ImageEnhance.Brightness(tex[face['material']]).enhance(1 if nz else (.92 if ny else .78));tp=texture.load()
        verts=face['vertices'];uv=face['uv'];screen=[(project(v)[0]*scale-left,top-project(v)[1]*scale) for v in verts]
        for j in range(1,len(verts)-1):
            ii=[0,j,j+1];triangle=[screen[i] for i in ii]
            bary=[base.coefficients(triangle,[int(k==n) for k in range(3)]) for n in range(3)]
            x0=max(0,math.floor(min(p[0] for p in triangle)));x1=min(image.width,math.ceil(max(p[0] for p in triangle)))
            y0=max(0,math.floor(min(p[1] for p in triangle)));y1=min(image.height,math.ceil(max(p[1] for p in triangle)))
            for y in range(y0,y1):
                for x in range(x0,x1):
                    weights=[a*(x+.5)+b*(y+.5)+c for a,b,c in bary]
                    if min(weights)<-1e-8:continue
                    xyz=[sum(weights[k]*verts[ii[k]][axis] for k in range(3)) for axis in range(3)]
                    z=-xyz[0]-xyz[1]+math.sqrt(2)*xyz[2];index=y*image.width+x
                    if z<depth[index]:continue
                    u,v=[sum(weights[k]*uv[ii[k]][axis] for k in range(3)) for axis in range(2)]
                    color=tp[math.floor(u*texture.width)%texture.width,math.floor(v*texture.height)%texture.height]
                    # Narrow face-local contact weathering, no ground repaint or shadow spill.
                    if nz==0 and xyz[2]<.75:color=tuple(round(c*.65) for c in color[:3])+(255,)
                    pix[x,y]=color;depth[index]=z
    return image,[-left,top],visible

def registration(sprite,spec,image,anchor,visible):
    root=sprite['worldPosition'];scale=spec['pixelsPerWorldUnit'];vertices=[v for f in sprite['faces'] for v in f['vertices']]
    world=lambda v:[v[0]+root[0],v[1]+root[1],v[2]]
    unique=sorted(set(tuple(v) for v in vertices));path=HERE/'attempt-01/sprites'/f"{sprite['id']}.png"
    return dict(id=sprite['id'],kind=sprite['kind'],image=dict(path=str(path.relative_to(ROOT)),sha256=''),registration=dict(canvasPixels=list(image.size),rootPixelsTopLeft=anchor,worldPosition=root,drawSizeWorld=[v/scale for v in image.size]),pixelsPerWorldUnit=scale,contactWorldXYZ=[world(v) for v in sprite['contactLocal']],heightWorld=sprite['heightWorld'],worldBoundsXYZ=dict(min=[min(world(v)[k] for v in vertices) for k in range(3)],max=[max(world(v)[k] for v in vertices) for k in range(3)]),geometryLandmarks=[dict(worldXYZ=world(v),sourcePixelsTopLeft=[anchor[0]+scale*project(v)[0],anchor[1]-scale*project(v)[1]]) for v in unique],geometryFile='geometry.json',geometryID=sprite['id'],visibleFaceCount=visible)

def build(out):
    if out.exists() and any(out.iterdir()):raise RuntimeError('Refusing overwrite: outputs are immutable, choose empty replay directory')
    out.mkdir(parents=True,exist_ok=True);(out/'sprites').mkdir();(out/'textures').mkdir()
    spec=load(HERE/'geometry.json');tex=textures();regs=[]
    for key,im in tex.items():im.save(out/'textures'/f'{key}.png')
    for sprite in spec['sprites']:
        im,anchor,visible=render(sprite,spec,tex);path=out/'sprites'/f"{sprite['id']}.png";im.save(path)
        reg=registration(sprite,spec,im,anchor,visible);reg['image']['sha256']=sha(path);regs.append(reg)
    (out/'registration.json').write_text(json.dumps(regs,indent=2)+'\n')
    print(json.dumps(dict(sprites=len(regs),output=str(out))))
    return regs
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();build(args.out)
