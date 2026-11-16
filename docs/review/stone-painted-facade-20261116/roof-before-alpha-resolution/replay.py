"""Portable Pillow-only orthographic mesh/UV renderer. No external paths or old masters."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
HERE=Path(__file__).resolve().parent

def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def raw(p,reverse=False):
    x,y,z=p
    if reverse: x,y=128-x,128-y
    return ((x-y)*math.sqrt(.5)*5,-((x+y)*math.sqrt(.5)/2+z)*5)
def registration(mesh):
    points=[raw(v) for v in mesh['vertices']]+[(0,0)]
    lo=[math.floor(min(p[k] for p in points)/10)*10-40 for k in (0,1)]
    hi=[math.ceil(max(p[k] for p in points)/10)*10+40 for k in (0,1)]
    root=[-v for v in lo]
    size=[hi[k]-lo[k] for k in (0,1)]
    def landmark(name,v,kind):
        q=raw(v)
        return dict(id=name,local=v,world=[512+v[0],640+v[1],v[2]],source=[q[k]+root[k] for k in (0,1)],provenance=kind)
    return dict(solidID='solid-03-transit-kiosk',authoritativeBounds=[512,640,640,768],worldRoot=[512,640,0],sourceRoot=root,sourceCanvas=size,sourcePixelsPerWorldUnit=5,uniformDrawScale=.2,spriteSizeScenePoints=[x/5 for x in size],spriteAnchorBottomLeft=[root[0]/size[0],1-root[1]/size[1]],screenProjection='u=rootU+5*(x-y)/sqrt(2), v=rootV-5*((x+y)/(2*sqrt(2))+z)',landmarks=[landmark('virtual-origin',[0,0,0],'collision-only virtual corner')]+[landmark('vertex-'+str(i),v,'explicit authored mesh vertex') for i,v in enumerate(mesh['vertices'])],collision='UNCHANGED original 128x128 blocked rectangle. Chamfer and painted stairs remain blocked.',contactZ=0,ownerAccepted=False,productionAdmitted=False,readyForNative=False,status='FIRST_SAMPLE_COORDINATOR_REVIEW',referenceSHA256=sha(HERE/'inputs/benchmark.png'))
def textures(spec):
    with Image.open(HERE/spec['atlas']) as im:
        assert im.size==(1536,1024)
        return {name:im.crop(rect).convert('RGBA') for name,rect in spec['rects'].items()}
def normal(a,b,c):
    u=[b[k]-a[k] for k in range(3)]
    v=[c[k]-a[k] for k in range(3)]
    return [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
def coefficients(points,values):
    (x0,y0),(x1,y1),(x2,y2)=points
    v0,v1,v2=values
    det=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0)
    if abs(det)<1e-8: raise ValueError('Degenerate projected triangle')
    a=((v1-v0)*(y2-y0)-(v2-v0)*(y1-y0))/det
    b=((x1-x0)*(v2-v0)-(x2-x0)*(v1-v0))/det
    return a,b,v0-a*x0-b*y0

def clamped_texture(texture):
    # Replicated edge texels implement clamp-to-edge for triangle borders.
    # Alpha coverage still comes from the mesh, never an inferred image contour.
    pad=8
    w,h=texture.size
    result=Image.new('RGBA',(w+2*pad,h+2*pad))
    xs=[(0,1,0,pad),(0,w,pad,w),(w-1,w,w+pad,pad)]
    ys=[(0,1,0,pad),(0,h,pad,h),(h-1,h,h+pad,pad)]
    for x0,x1,dx,dw in xs:
        for y0,y1,dy,dh in ys:
            result.paste(texture.crop((x0,y0,x1,y1)).resize((dw,dh),Image.Resampling.NEAREST),(dx,dy))
    return result,pad

def render(mesh,tex,reverse=False):
    reg=registration(mesh)
    size=tuple(reg['sourceCanvas'])
    root=reg['sourceRoot']
    image=Image.new('RGBA',size)
    faces=sorted(mesh['faces'],key=lambda f:sum(sum(mesh['vertices'][i][:2]) for i in f['indices'])/len(f['indices']),reverse=not reverse)
    for face in faces:
        verts=[mesh['vertices'][i] for i in face['indices']]
        n=normal(*verts[:3])
        direction=(1,1,1) if reverse else (-1,-1,1)
        if sum(n[k]*direction[k] for k in range(3))<=0: continue
        projected=[tuple(raw(v,reverse)[k]+root[k] for k in (0,1)) for v in verts]
        source=tex[face['material']]
        texture,pad=clamped_texture(source)
        uv=[(pad+u*(source.width-1),pad+v*(source.height-1)) for u,v in face['uv']]
        for j in range(1,len(verts)-1):
            ids=[0,j,j+1]
            triangle=[projected[i] for i in ids]
            coeff=coefficients(triangle,[uv[i][0] for i in ids])+coefficients(triangle,[uv[i][1] for i in ids])
            warped=texture.transform(size,Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
            mask=Image.new('L',size)
            ImageDraw.Draw(mask).polygon(triangle,fill=255)
            image.paste(warped,(0,0),mask)
    return image

def roof_layer_registration(spec,reg):
    anchor=spec['localWorldAnchor']
    projected=[reg['sourceRoot'][k]+raw(anchor)[k] for k in (0,1)]
    scale=spec['uniformSourceToBuildingPixels']
    origin=[projected[k]-scale*spec['sourceRoot'][k] for k in (0,1)]
    return dict(**spec,projectedBuildingRoot=projected,buildingPixelOrigin=origin,
                worldAnchor=[512+anchor[0],640+anchor[1],anchor[2]],
                buildingCanvas=reg['sourceCanvas'],sourceSHA256=sha(HERE/spec['image']))

def render_roof_layer(spec,reg,source=None):
    info=roof_layer_registration(spec,reg)
    if source is None:
        with Image.open(HERE/spec['image']) as image: source=image.convert('RGBA')
    assert source.size==tuple(spec['sourceCanvas'])
    scale=spec['uniformSourceToBuildingPixels']
    ox,oy=info['buildingPixelOrigin']
    # Premultiplied alpha avoids dark fringes. Original material alpha is retained.
    return source.convert('RGBa').transform(tuple(reg['sourceCanvas']),Image.Transform.AFFINE,
        (1/scale,0,-ox/scale,0,1/scale,-oy/scale),Image.Resampling.BICUBIC).convert('RGBA')

def export_obj(mesh,out):
    lines=['# Authored world-unit solid, OBJ v increases upward','mtllib building.mtl']
    lines += ['v '+' '.join(map(str,v)) for v in mesh['vertices']]
    for face in mesh['faces']:
        lines += [f'vt {u} {1-v}' for u,v in face['uv']]
    offset=1
    for face in mesh['faces']:
        lines += ['g '+face['name'],'usemtl '+face['material'],'f '+' '.join(f'{i+1}/{offset+j}' for j,i in enumerate(face['indices']))]
        offset+=len(face['indices'])
    (out/'building.obj').write_text('\n'.join(lines)+'\n')
    (out/'building.mtl').write_text('\n'.join(f'newmtl {m}\nKd 1 1 1\nmap_Kd textures/{m}.png\n' for m in ('facade','door','roof')))

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    mesh=load(HERE/'mesh.json')
    spec=load(HERE/'materials.json')
    tex=textures(spec)
    (out/'textures').mkdir(exist_ok=True)
    for name,t in tex.items(): t.save(out/'textures'/f'{name}.png')
    reg=registration(mesh)
    image=render(mesh,tex)
    image.save(out/'building-alpha.png')
    layer_spec=load(HERE/'roof-layer.json')
    layer=render_roof_layer(layer_spec,reg)
    layer.save(out/'roof-layer-alpha.png')
    dump(out/'roof-layer-registration.json',roof_layer_registration(layer_spec,reg))
    image=Image.alpha_composite(image,layer)
    image.save(out/'preview-alpha.png')
    native=image.resize(tuple(int(v) for v in reg['spriteSizeScenePoints']),Image.Resampling.LANCZOS)
    half=image.resize(tuple(int(v/2) for v in reg['spriteSizeScenePoints']),Image.Resampling.LANCZOS)
    native.save(out/'native-alpha.png')
    half.save(out/'half-alpha.png')
    render(mesh,tex,True).save(out/'hidden-surfaces.png')
    plate=Image.new('RGB',(1280,500),'#333638')
    with Image.open(HERE/'inputs/benchmark.png') as reference:
        reference=reference.convert('RGB')
        reference.thumbnail((704,420),Image.Resampling.LANCZOS)
        plate.paste(reference,(0,50))
    plate.paste(native,(760,65),native)
    plate.paste(half,(1080,65),half)
    d=ImageDraw.Draw(plate)
    d.text((10,12),'FULL IMMUTABLE BENCHMARK / uniformly fit, uncropped',fill='white')
    d.text((730,12),'FINAL SOURCE + 2.5D VENT / NOT native runtime capture',fill='white')
    d.text((760,45),'1x logical source',fill='white')
    d.text((1080,45),'0.5x source',fill='white')
    d.text((730,360),'Painted relief + separate 2.5D vent. No acceptance.',fill='white')
    plate.save(out/'comparison.png')
    ImageOps.grayscale(plate).save(out/'comparison-grayscale.png')
    export_obj(mesh,out)
    dump(out/'registration.json',reg)
    dump(out/'manifest.json',dict(inputs={n:sha(HERE/n) for n in ['mesh.json','materials.json','roof-layer.json','author.py','replay.py','inputs/atlas.png','inputs/provider.json','inputs/benchmark.png','inputs/roof-vent.png','inputs/roof-vent-provider.json']},outputs={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'},status='TECHNICAL_SOURCE_ONLY_NOT_VISUAL_ACCEPTANCE'))
    print('Final source completeness sample written:',out)
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE/'output')
    build(parser.parse_args().out)
