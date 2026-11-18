#!/usr/bin/env python3
"""Deterministic renderer for explicitly painted Camera surfaces.

ADAPT: cubic sampler idea from camera-editable-master-20261116/build.py:18-53.
All geometry/material surfaces are new in surfaces.py. No old raster/shader reuse.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageOps, ImageFilter

HERE=Path(__file__).resolve().parent
INPUT_ROOT=next(p for p in [HERE,*HERE.parents] if (p/'inputs/reference.png').exists())
REF=INPUT_ROOT/'inputs/reference.png'
SS=4


def load_source(path):
    spec=importlib.util.spec_from_file_location('authored_surfaces',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(canvas=module.CANVAS,root=module.ROOT,scale=module.SCALE,
                landmarks=module.LANDMARKS,parts=module.PARTS,hidden=module.HIDDEN)


def paths(source):
    tokens=re.findall(r'[MLCZ]|-?\d+(?:\.\d+)?',source)
    result=[]
    points=[]
    i=0
    while i<len(tokens):
        command=tokens[i]
        i+=1
        if command=='M':
            if points:
                result.append(points)
            points=[(float(tokens[i]),float(tokens[i+1]))]
            i+=2
        elif command=='L':
            points.append((float(tokens[i]),float(tokens[i+1])))
            i+=2
        elif command=='C':
            p0=points[-1]
            p1,p2,p3=[(float(tokens[i+j]),float(tokens[i+j+1])) for j in (0,2,4)]
            i+=6
            for step in range(1,33):
                t=step/32
                points.append(tuple((1-t)**3*p0[k]+3*(1-t)**2*t*p1[k]+3*(1-t)*t*t*p2[k]+t**3*p3[k] for k in (0,1)))
        elif command=='Z':
            points.append(points[0])
        else:
            raise ValueError(command)
    if points:
        result.append(points)
    return result


def paint(size,path,color,width=0):
    image=Image.new('RGBA',size)
    draw=ImageDraw.Draw(image)
    for points in paths(path):
        points=[(round(x*SS),round(y*SS)) for x,y in points]
        if width:
            draw.line(points,fill=color,width=max(1,round(width*SS)),joint='curve')
        else:
            draw.polygon(points,fill=color)
    return image


def save(image,path,canvas):
    image=image.resize(tuple(canvas),Image.Resampling.LANCZOS)
    # Canonical transparent RGB is zero. Do not retain matte colors outside alpha.
    image.paste((0,0,0,0),(0,0),image.getchannel('A').point(lambda a:255 if a==0 else 0))
    image.save(path)
    return image


def render(model,out,omit=()):
    out.mkdir(parents=True,exist_ok=True)
    layerdir=out/'layers'
    layerdir.mkdir(exist_ok=True)
    width,height=model['canvas']
    size=(width*SS,height*SS)
    result=Image.new('RGBA',size)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<title>Individually authored Camera surfaces, review only</title>']
    census=[]
    for part in model['parts']:
        name=part['name']
        foundation=paint(size,part['contour'],ImageColor.getrgb(part['underpaint'])+(255,))
        mask=foundation.getchannel('A')
        component=foundation.copy()
        save(foundation,layerdir/f'{name}--underpaint.png',model['canvas'])
        svg.append(f'<defs><clipPath id="clip-{name}"><path d="{part["contour"]}"/></clipPath></defs>')
        svg.append(f'<g id="{name}"><path id="{name}--underpaint" d="{part["contour"]}" fill="{part["underpaint"]}"/>')
        for surface in part['surfaces']:
            sid=name+'--'+surface['name']
            rgba=ImageColor.getrgb(surface['color'])+(surface['opacity'],)
            layer=paint(size,surface['path'],rgba,surface['width'])
            feather=surface.get('feather',0)
            if feather:
                alpha=layer.getchannel('A').filter(ImageFilter.GaussianBlur(feather*SS))
                layer=Image.new('RGBA',size,rgba)
                layer.putalpha(alpha)
            layer.putalpha(ImageChops.multiply(layer.getchannel('A'),mask))
            component.alpha_composite(layer)
            save(layer,layerdir/f'{sid}.png',model['canvas'])
            if surface['width']:
                attrs=f'fill="none" stroke="{surface["color"]}" stroke-width="{surface["width"]}" stroke-linejoin="round"'
            else:
                attrs=f'fill="{surface["color"]}"'
            if feather:
                svg.append(f'<defs><filter id="brush-{sid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{feather}"/></filter></defs>')
                attrs+=f' filter="url(#brush-{sid})"'
            svg.append(f'<path id="{sid}" d="{surface["path"]}" {attrs} opacity="{surface["opacity"]/255}" clip-path="url(#clip-{name})"/>')
            census.append(dict(id=sid,path=surface['path'],color=surface['color'],width=surface['width'],feather=feather))
        if name!='cyan_lens':
            edge=paint(size,part['contour'],(22,27,27,220),.85)
            component.alpha_composite(edge)
            svg.append(f'<path d="{part["contour"]}" fill="none" stroke="#161b1b" stroke-width=".85" opacity="{220/255}"/>')
        svg.append('</g>')
        save(component,layerdir/f'{name}--complete.png',model['canvas'])
        if name not in omit:
            result.alpha_composite(component)
    svg.append('</svg>')
    (out/'camera-surfaces.svg').write_text('\n'.join(svg)+'\n')
    (out/'surface-census.json').write_text(json.dumps(census,indent=2)+'\n')
    (out/'model.json').write_text(json.dumps(model,indent=2)+'\n')
    (out/'model-data.js').write_text('window.cameraSurfaceModel='+json.dumps(model)+';\n')
    master=save(result,out/'camera-master.png',model['canvas'])
    for label,scale in [('native',model['scale']),('half',model['scale']/2)]:
        target=(math.ceil(width*scale),math.ceil(height*scale))
        image=master.transform(target,Image.Transform.AFFINE,(1/scale,0,0,0,1/scale,0),Image.Resampling.BICUBIC)
        image.paste((0,0,0,0),(0,0),image.getchannel('A').point(lambda a:255 if a==0 else 0))
        image.save(out/f'camera-{label}.png')
    return master


def comparisons(model,master,out):
    with Image.open(REF) as image:
        reference=image.convert('RGB').crop((890,20,1070,470))
    reference.save(out/'reference-window.png')
    board=Image.new('RGB',(890,550),'#706e66')
    d=ImageDraw.Draw(board)
    d.text((12,12),'UNCHANGED REFERENCE',fill='white')
    d.text((225,12),'FIRST SURFACE PASS / REJECTED',fill='white')
    d.text((440,12),'FINAL SURFACE PASS / 02',fill='white')
    board.paste(reference,(12,40))
    with Image.open(INPUT_ROOT/'inputs/first-surface-master.png') as previous:
        board.paste(previous,(225,40),previous)
    board.paste(master,(440,40),master)
    for label,y,factor in [('native',65,1),('half',235,2)]:
        scale=model['scale']/factor
        with Image.open(out/f'camera-{label}.png') as image:
            board.paste(image,(755,y),image)
        resized=reference.transform((math.ceil(180*scale),math.ceil(450*scale)),Image.Transform.AFFINE,(1/scale,0,0,0,1/scale,0),Image.Resampling.BICUBIC)
        board.paste(resized,(685,y))
        d.text((680,y-22),label+' / REF vs NEW',fill='white')
    d.text((12,510),'Uniform96/418 x/y. Authored root(46,427). No native runtime or acceptance claim.',fill='white')
    board.save(out/'comparison-color.png')
    ImageOps.grayscale(board).save(out/'comparison-grayscale.png')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(out,source):
    model=load_source(source)
    master=render(model,out)
    comparisons(model,master,out)
    archive=out/'source'
    archive.mkdir(exist_ok=True)
    (archive/'surfaces.py').write_bytes(source.read_bytes())
    (archive/'build.py').write_bytes(Path(__file__).read_bytes())
    (archive/'geometry.json').write_bytes((source.parent/'geometry.json').read_bytes())
    (archive/'inputs').mkdir(exist_ok=True)
    for name in ['reference.png','first-surface-master.png','prior-procedural-master.png']:
        (archive/'inputs'/name).write_bytes((INPUT_ROOT/'inputs'/name).read_bytes())
    record={'reference_sha256':digest(REF),'pillow':Image.__version__,
            'python':sys.version.split()[0], 'files':{}}
    for path in sorted(out.rglob('*')):
        if path.is_file() and path.name!='manifest.json' and '__pycache__' not in path.parts:
            record['files'][str(path.relative_to(out))]=digest(path)
    (out/'manifest.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(f'{len(model["parts"])} complete parts, {sum(len(p["surfaces"]) for p in model["parts"])} individually authored surfaces: {out}')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=HERE/'attempt-02')
    parser.add_argument('--source',type=Path,default=HERE/('surfaces-final.py' if (HERE/'surfaces-final.py').exists() else 'surfaces.py'))
    args=parser.parse_args()
    build(args.output,args.source)
