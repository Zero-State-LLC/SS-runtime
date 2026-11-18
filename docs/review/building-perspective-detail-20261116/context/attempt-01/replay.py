"""Portable Pillow renderer of explicit editable D108 geometry and UVs.
Uses per-pixel geometric depth, not sprite sorting or whole-sprite distortion.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance

HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def dump(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def project(v):
    x,y,z=v
    return [(x-y)/math.sqrt(2),(x+y)/(2*math.sqrt(2))+z]

def materials(root):
    result={}
    for name,spec in load(root/'materials.json').items():
        with Image.open(root/spec['input']) as im: image=im.convert('RGB').crop(spec['crop'])
        if 'tint' in spec:
            image=Image.merge('RGB',tuple(channel.point(lambda v,f=f: round(v*f)) for channel,f in zip(image.split(),spec['tint'])))
        if spec.get('brickCourses'):
            image=image.resize((256,256),Image.Resampling.BICUBIC)
            draw=ImageDraw.Draw(image)
            for row,y in enumerate(range(0,256,16)):
                draw.line((0,y,256,y),fill=(89,78,66),width=2)
                for x in range(-32 if row%2 else 0,256,64): draw.line((x,y,x,y+16),fill=(89,78,66),width=2)
        result[name]=image.convert('RGBA')
    return result

def render(building,spec,textures):
    scale=spec['pixelsPerWorldUnit']
    vertices=[v for f in building['faces'] for v in f['vertices']]
    projected=[project(v) for v in vertices]
    pad=spec['paddingPixels']
    left=math.floor(min(v[0] for v in projected)*scale)-pad
    right=math.ceil(max(v[0] for v in projected)*scale)+pad
    bottom=math.floor(min(v[1] for v in projected)*scale)-pad
    top=math.ceil(max(v[1] for v in projected)*scale)+pad
    width,height=right-left,top-bottom
    canvas=Image.new('RGBA',(width,height))
    pixels=canvas.load()
    depthbuffer=array('f',[-1e30])*(width*height)
    visible=0
    for face in building['faces']:
        if len(face['vertices']) != 4 or len(face['uv']) != 4:
            raise ValueError('Expected an editable affine quad: '+face['name'])
        for key in ('vertices','uv'):
            points=face[key]
            if any(abs(points[2][i]-(points[1][i]+points[3][i]-points[0][i]))>1e-7 for i in range(len(points[0]))):
                raise ValueError('Non-affine '+key+' must be split into affine quads: '+face['name'])
        nx,ny,nz=face['normal']
        if -nx-ny+math.sqrt(2)*nz <= 0: continue
        visible+=1
        screen=[(project(v)[0]*scale-left,top-project(v)[1]*scale) for v in face['vertices']]
        x0=max(0,math.floor(min(p[0] for p in screen)))
        y0=max(0,math.floor(min(p[1] for p in screen)))
        x1=min(width,math.ceil(max(p[0] for p in screen))+1)
        y1=min(height,math.ceil(max(p[1] for p in screen))+1)
        ax,ay=screen[0]
        bx,by=screen[1][0]-ax,screen[1][1]-ay
        cx,cy=screen[3][0]-ax,screen[3][1]-ay
        determinant=bx*cy-by*cx
        if abs(determinant)<1e-10: raise ValueError('Degenerate face '+face['name'])
        ia,ib=cy/determinant,-cx/determinant
        ja,jb=-by/determinant,bx/determinant
        ic=ia*(x0-ax)+ib*(y0-ay)
        jc=ja*(x0-ax)+jb*(y0-ay)
        uv=face['uv']
        du=[uv[1][i]-uv[0][i] for i in (0,1)]
        dv=[uv[3][i]-uv[0][i] for i in (0,1)]
        texture=textures[face['material']]
        shade=1 if nz else (.92 if ny else .78)
        texture=ImageEnhance.Brightness(texture).enhance(shade)
        tw,th=texture.size
        coeff=(tw*(du[0]*ia+dv[0]*ja),tw*(du[0]*ib+dv[0]*jb),tw*(uv[0][0]+du[0]*ic+dv[0]*jc),th*(du[1]*ia+dv[1]*ja),th*(du[1]*ib+dv[1]*jb),th*(uv[0][1]+du[1]*ic+dv[1]*jc))
        tile=texture.transform((x1-x0,y1-y0),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
        src=tile.load()
        depths=[-v[0]-v[1]+math.sqrt(2)*v[2] for v in face['vertices']]
        for yy in range(y0,y1):
            sy=yy-y0+.5
            for xx in range(x0,x1):
                sx=xx-x0+.5
                u=ia*sx+ib*sy+ic
                v=ja*sx+jb*sy+jc
                if not(-1e-8<=u<=1+1e-8 and -1e-8<=v<=1+1e-8): continue
                depth=depths[0]+u*(depths[1]-depths[0])+v*(depths[3]-depths[0])
                index=yy*width+xx
                if depth >= depthbuffer[index]-.0001:
                    color=src[xx-x0,yy-y0]
                    if color[3]:
                        pixels[xx,yy]=color
                        depthbuffer[index]=depth
    return canvas,[-left,top],visible

def main(root=HERE):
    spec=load(root/'geometry.json')
    tex=materials(root)
    output=root/'output'
    output.mkdir(exist_ok=True)
    regs=[]
    for building in spec['buildings']:
        image,rootpixel,visible=render(building,spec,tex)
        role=building['solidID']
        target=output/(role+'.png')
        image.save(target)
        scale=spec['pixelsPerWorldUnit']
        drawsize=[v/scale for v in image.size]
        native=image.resize(tuple(round(v) for v in drawsize),Image.Resampling.LANCZOS)
        native.save(output/(role+'-native.png'))
        native.resize(tuple(max(1,round(v/2)) for v in native.size),Image.Resampling.LANCZOS).save(output/(role+'-half.png'))
        landmarks=[]
        # Every exact original footprint corner, not alpha bounds, drives alignment witnesses.
        for i,local in enumerate(building['contactLocal']):
            p=project(local)
            landmarks.append({'name':'footprint-'+str(i),'localXYZ':local,'worldXYZ':[local[0]+building['worldPosition'][0],local[1]+building['worldPosition'][1],local[2]],'sourcePixelsTopLeft':[rootpixel[0]+scale*p[0],rootpixel[1]-scale*p[1]]})
        reg={'nodeName':building['nodeName'],'solidID':role,'source':'output/'+target.name,'sha256':sha(target),'canvasPixels':list(image.size),'rootPixelsTopLeft':rootpixel,'worldPosition':building['worldPosition'],'drawSizeWorld':drawsize,'pixelsPerWorldUnit':scale,'footprintWorld':building['footprintWorld'],'geometryLandmarks':landmarks,'alignmentCheck':{'method':'Independent inverse matrix and authority checks in test_context.py','evidence':'alignment-verification.json','binding':'Evidence must match this registration.json SHA256'},'visibleFaceCount':visible,'faceCount':len(building['faces'])}
        regs.append(reg)
        witness=native.convert('RGBA')
        draw=ImageDraw.Draw(witness)
        pts=[(p['sourcePixelsTopLeft'][0]/scale,p['sourcePixelsTopLeft'][1]/scale) for p in landmarks]
        draw.line(pts+[pts[0]],fill=(255,95,68,255),width=1)
        rx,ry=[v/scale for v in rootpixel]
        draw.line((rx-4,ry,rx+4,ry),fill=(80,230,255,255),width=1)
        draw.line((rx,ry-4,rx,ry+4),fill=(80,230,255,255),width=1)
        witness.save(output/(role+'-footprint-witness.png'))
    dump(root/'registration.json',regs)
    for size in ('native','half'):
        thumbs=[Image.open(output/(r['solidID']+'-'+size+'.png')).convert('RGBA') for r in regs]
        widths=[im.width+24 for im in thumbs]
        sheet=Image.new('RGB',(sum(widths),max(im.height for im in thumbs)+64),(53,54,54))
        draw=ImageDraw.Draw(sheet)
        xx=12
        for image,r,w in zip(thumbs,regs,widths):
            sheet.paste(image,(xx,38),image)
            draw.text((xx,10),r['solidID'].replace('solid-',''),fill='white')
            xx+=w
        sheet.save(output/('first-preview-'+size+'.png'))
    tracked=[p for p in sorted(root.rglob('*')) if p.is_file() and (p.relative_to(root).parts[0] in ('inputs','output') or str(p.relative_to(root)) in ('geometry.json','materials.json','registration.json','provenance.json'))]
    dump(root/'manifest.json',{'schema':'context-source-manifest-001','status':'FIRST_SAMPLE_REVIEW_ONLY','files':{str(p.relative_to(root)):sha(p) for p in tracked},'projection':'D108 exact, upright z','sourceAuthoring':'geometry.json plus materials.json and retained local inputs','implementationSHA256':{name:sha(root/name) for name in ('author.py','replay.py','test_context.py')},'noNativeCapture':True})
    print(json.dumps({'assets':len(regs),'faces':sum(r['faceCount'] for r in regs),'sourceRoot':str(root),'registration':str(root/'registration.json')}))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=HERE)
    main(parser.parse_args().root.resolve())
