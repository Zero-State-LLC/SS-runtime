"""Direct replay of explicit mesh and authored UV paint. No procedural geometry/noise.
Raster math adapted from ../stone-editable-master-20261116/build.py:173-224.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REFERENCE=ROOT/'docs/review/bp001-decision-20261116/street-corner-approved-concept.png'
R=math.sqrt(.5)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def project(p,m):
    x,y,z=p
    s=m['sourcePixelsPerWorldUnit']
    u,v=m['sourceRoot']
    return (u+s*(x-y)*R,v-s*((x+y)*R/2+z))
def normal(a,b,c):
    u=[b[i]-a[i] for i in range(3)]
    v=[c[i]-a[i] for i in range(3)]
    n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
    mag=math.sqrt(sum(k*k for k in n))
    if mag<1e-9: raise ValueError('Degenerate mesh face')
    return [k/mag for k in n]

def paint_surfaces(spec,out=None):
    surfaces=spec['surfaces']
    def resolve(name,seen=()):
        if name in seen: raise ValueError('Paint inheritance cycle')
        item=surfaces[name]
        parent=resolve(item['parent'],seen+(name,)) if 'parent' in item else {'polygons':[],'lines':[]}
        return {'base':item.get('base',parent.get('base')),
                'polygons':parent['polygons']+item.get('polygons',[]),
                'lines':parent['lines']+item.get('lines',[])}
    result={}
    if out: out.mkdir(parents=True,exist_ok=True)
    for name in surfaces:
        item=resolve(name)
        im=Image.new('RGB',(512,512),tuple(item['base']))
        d=ImageDraw.Draw(im)
        svg=['<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">',
             f'<title>{name}: authored surface paint</title>',f'<rect width="512" height="512" fill="rgb{tuple(item["base"])}"/>']
        for index,(points,color) in enumerate(item['polygons']):
            xy=[(round(x*511),round(y*511)) for x,y in points]
            d.polygon(xy,fill=tuple(color))
            coords=' '.join(f'{x},{y}' for x,y in xy)
            svg.append(f'<polygon id="paint-{index}" points="{coords}" fill="rgb{tuple(color)}"/>')
        for index,(a,b,color,width) in enumerate(item['lines']):
            xy=[(round(x*511),round(y*511)) for x,y in (a,b)]
            w=max(1,round(width*512))
            d.line(xy,fill=tuple(color),width=w)
            svg.append(f'<path id="edge-{index}" d="M {xy[0][0]} {xy[0][1]} L {xy[1][0]} {xy[1][1]}" stroke="rgb{tuple(color)}" stroke-width="{w}"/>')
        svg.append('</svg>')
        result[name]=im
        if out:
            im.save(out/(name+'.png'))
            (out/(name+'.svg')).write_text('\n'.join(svg)+'\n')
    return result

def render(m,parts,textures,groups=None,reverse=False):
    width,height=m['canvas']
    image=Image.new('RGBA',(width,height))
    pix=image.load()
    depth=[-1e30]*(width*height)
    light=m['light']
    mag=math.sqrt(sum(v*v for v in light['direction']))
    light_direction=[v/mag for v in light['direction']]
    for part in parts:
        if groups and part['group'] not in groups:continue
        vertices=part['vertices']
        if reverse:vertices=[[128-x,128-y,z] for x,y,z in vertices]
        texture=textures[part['material']]
        tex=texture.load()
        for face in part['faces']:
            poly=[vertices[i] for i in face]
            n=normal(*poly[:3])
            lambert=max(0,sum(n[i]*light_direction[i] for i in range(3)))
            shade=light['ambient']+light['diffuse']*lambert
            axis=max(range(3),key=lambda i:abs(n[i]))
            uvaxes=[i for i in range(3) if i!=axis]
            low=[min(p[j] for p in poly) for j in uvaxes]
            span=[max(p[j] for p in poly)-low[k] for k,j in enumerate(uvaxes)]
            if min(span)<1e-9: raise ValueError('Degenerate UV surface')
            for k in range(1,len(poly)-1):
                xyz=[poly[0],poly[k],poly[k+1]]
                a,b,c=[project(p,m) for p in xyz]
                den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(den)<1e-8:continue
                left=max(0,math.floor(min(a[0],b[0],c[0])))
                right=min(width-1,math.ceil(max(a[0],b[0],c[0])))
                top=max(0,math.floor(min(a[1],b[1],c[1])))
                bottom=min(height-1,math.ceil(max(a[1],b[1],c[1])))
                ds=[-p[0]-p[1]+p[2]*R for p in xyz]
                for y in range(top,bottom+1):
                    for x in range(left,right+1):
                        aa=((b[1]-c[1])*(x+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))/den
                        bb=((c[1]-a[1])*(x+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))/den
                        cc=1-aa-bb
                        if min(aa,bb,cc)<-1e-8:continue
                        z=aa*ds[0]+bb*ds[1]+cc*ds[2]
                        index=y*width+x
                        if z<depth[index]-1e-7:continue
                        depth[index]=z
                        coord=[aa*xyz[0][j]+bb*xyz[1][j]+cc*xyz[2][j] for j in uvaxes]
                        u=(coord[0]-low[0])/span[0]
                        v=(coord[1]-low[1])/span[1]
                        # Paint uses top-down vertical UVs, never a repeated world-space tile.
                        if uvaxes[1]==2:v=1-v
                        rgb=tex[min(511,max(0,round(u*511))),min(511,max(0,round(v*511)))]
                        pix[x,y]=(*[min(255,round(c*shade)) for c in rgb],255)
    return image

def resized(im,size):
    out=im.resize(size,Image.Resampling.LANCZOS)
    out.paste((0,0,0,0),(0,0),out.getchannel('A').point(lambda a:255 if a==0 else 0))
    return out

def build(out=HERE,quick=False):
    out.mkdir(parents=True,exist_ok=True)
    model=load(HERE/'model.json')
    mesh=load(HERE/'mesh.json')
    paint=load(HERE/'surface-paint.json')
    textures=paint_surfaces(paint,out/'surfaces')
    im=render(model,mesh,textures)
    im.save(out/'preview-alpha.png')
    native=resized(im,(224,192))
    half=resized(im,(112,96))
    native.save(out/'native-alpha.png')
    half.save(out/'half-alpha.png')
    plate=Image.new('RGB',(1408,530),'#333638')
    with Image.open(REFERENCE) as ref:plate.paste(ref.convert('RGB').resize((704,396),Image.Resampling.LANCZOS),(0,44))
    plate.paste(native,(920,70),native)
    zoom=resized(im,(314,269))
    plate.paste(zoom,(870,253),zoom)
    plate.paste(half,(1170,92),half)
    d=ImageDraw.Draw(plate)
    d.text((12,14),'UNCHANGED ORIGINAL / uniform fit / no crop',fill='white')
    d.text((716,14),'SURFACE-AUTHORED MESH / source preview only / not native runtime',fill='white')
    d.text((716,52),'1x logical scale',fill='white')
    d.text((1170,70),'Half',fill='white')
    d.text((716,235),'1.4x diagnostic / complete roof retained',fill='white')
    plate.save(out/'comparison.png')
    ImageOps.grayscale(plate).save(out/'comparison-grayscale.png')
    print('FIRST SAMPLE READY',out/'comparison.png',flush=True)
    if not quick:
        render(model,mesh,textures,{'building'}).save(out/'building-alpha.png')
        render(model,mesh,textures,{'stairs'}).save(out/'stairs-alpha.png')
        render(model,mesh,textures,reverse=True).save(out/'hidden-surfaces.png')
    old=load(HERE.parent/'stone-editable-master-20261116/registration.json')
    reg={key:old[key] for key in ('solidID','authoritativeBounds','worldRoot','sourceRoot','sourcePixelsPerWorldUnit','uniformDrawScale','sourceCanvas','spriteSizeScenePoints','spriteAnchorBottomLeft','screenProjection','landmarks','measuredReferenceGeometry','collision','referenceSHA256','arenaSHA256')}
    reg.update(status='SURFACE_AUTHORED_REVIEW_ONLY',sourceSHA256={n:sha(HERE/n) for n in ('model.json','mesh.json','surface-paint.json','replay.py')},
               landmarkSupport='registered-foundation closed base, not old upper shell',
               hiddenGeometry='Explicitly authored closed geometry, not measured reference',ownerAccepted=False,productionAdmitted=False,readyForNative=False)
    (out/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
    return im

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE)
    parser.add_argument('--quick',action='store_true')
    args=parser.parse_args()
    build(args.out,args.quick)
