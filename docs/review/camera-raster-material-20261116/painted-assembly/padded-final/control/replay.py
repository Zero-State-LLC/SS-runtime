#!/usr/bin/env python3
"""Portable three-layer painted assembly. Only exact crop, uniform scale and translation.

All painted contour/material/illumination pixels come from the supplied provider
sources. No threshold cleanup, generated noise, new shading or inferred geometry.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
STATUS = 'PAINTED_ASSEMBLY_FIRST_PREVIEW_NOT_ACCEPTED'
SS = 3

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(p,data):
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def canonical(im):
    im.paste((0,0,0,0),(0,0),im.getchannel('A').point(lambda a:255 if a==0 else 0))
    return im

def scaled(im,scale):
    size=tuple(math.ceil(v*scale) for v in im.size)
    # Same coefficient on X and Y. Rounded canvas dimensions do not stretch content.
    return canonical(im.convert('RGBa').transform(size,Image.Transform.AFFINE,
        (1/scale,0,0,0,1/scale,0),Image.Resampling.BICUBIC).convert('RGBA'))

def inspect_source(im,layer):
    if im.mode!='RGBA' or im.size!=(1254,1254):
        raise ValueError('Expected actual1254-square RGBA source')
    region=layer['sourceRegion']
    crop=layer['crop']
    rx,ry,rr,rb=region
    x,y,r,b=crop
    if not (0<=rx<=x<r<=rr<=im.width and 0<=ry<=y<b<=rb<=im.height):
        raise ValueError('Crop outside component source region')
    alpha=im.getchannel('A')
    whole=alpha.crop(tuple(region))
    selected=alpha.crop(tuple(crop))
    hist=whole.histogram()
    selected_hist=selected.histogram()
    if hist[0]==0 or sum(hist[240:])<1000:
        raise ValueError('Not genuine transparent complete paint')
    if sum(hist[16:])!=sum(selected_hist[16:]):
        raise ValueError('Crop clips visible component paint')
    border=list(selected.crop((0,0,r-x,1)).tobytes())+list(selected.crop((0,b-y-1,r-x,b-y)).tobytes())
    border+=list(selected.crop((0,0,1,b-y)).tobytes())+list(selected.crop((r-x-1,0,r-x,b-y)).tobytes())
    if max(border,default=0)>=16:
        raise ValueError('Visible paint touches crop border')
    return dict(region=region,crop=crop,alphaExtrema=list(whole.getextrema()),
        regionTransparentPixels=hist[0],regionNearlyOpaquePixels=sum(hist[240:]),
        cropRetainedPaintPixels=sum(selected_hist[16:]),
        discardedAlpha1to15Pixels=sum(hist[1:16])-sum(selected_hist[1:16]),
        discardedAlphaMass=sum(i*(hist[i]-selected_hist[i]) for i in range(1,16)),
        discardedVisiblePixels=0,cropBorderMaxAlpha=max(border,default=0),
        thresholdIsDiagnosticOnly=True)

def load_sources(model,inputs):
    if model['schema']!=1 or model['status']!=STATUS:
        raise ValueError('Unsupported assembly schema/status')
    if len(model['layers'])!=3 or len({p['name'] for p in model['layers']})!=3:
        raise ValueError('Expected three independently editable layers')
    crops,inspections={},{}
    for layer in model['layers']:
        if layer['source'] not in {'components.png','junction-box.png'}:
            raise ValueError('Only local supplied painted sources allowed')
        if not isinstance(layer['uniformScale'],(int,float)) or not 0<layer['uniformScale']<=1:
            raise ValueError('One positive uniform scale required')
        if any(k in layer for k in ('scaleX','scaleY','warp','shader')):
            raise ValueError('Nonuniform transform or new shading prohibited')
        with Image.open(inputs/layer['source']) as raw:
            inspections[layer['name']]=inspect_source(raw,layer)
            crops[layer['name']]=raw.crop(tuple(layer['crop']))
    return crops,inspections

def render(model,inputs=None,omit=()):
    inputs=inputs or HERE/'inputs'
    crops,inspections=load_sources(model,inputs)
    canvas=tuple(n*SS for n in model['canvas'])
    composite=Image.new('RGBA',canvas)
    layers={}
    for spec in model['layers']:
        name=spec['name']
        scale=spec['uniformScale']
        x,y=spec['position']
        image=crops[name].convert('RGBa').transform(canvas,Image.Transform.AFFINE,
            (1/(scale*SS),0,-x/scale,0,1/(scale*SS),-y/scale),Image.Resampling.BICUBIC).convert('RGBA')
        layers[name]=canonical(image.resize(tuple(model['canvas']),Image.Resampling.LANCZOS))
        if spec['visible'] and name not in omit:
            composite.alpha_composite(image)
    master=canonical(composite.resize(tuple(model['canvas']),Image.Resampling.LANCZOS))
    return master,layers,crops,inspections

def comparisons(model,master,out):
    native=scaled(master,model['logicalScale'])
    half=scaled(master,model['logicalScale']/2)
    native.save(out/'camera-native.png')
    half.save(out/'camera-half.png')
    with Image.open(HERE/'inputs/reference.png') as im:
        reference=im.convert('RGB')
    with Image.open(HERE/'inputs/paving.png') as im:
        ground=im.convert('RGB').resize((352,352),Image.Resampling.LANCZOS).crop((0,0,352,200))
    ground.paste(native,(164,55),native)
    ground.save(out/'ordinary-background-context.png')
    plate=Image.new('RGB',(1100,630),'#303334')
    d=ImageDraw.Draw(plate)
    d.text((14,12),'UNCHANGED ORIGINAL / full image uniformly fitted / review only',fill='white')
    plate.paste(reference.resize((660,371),Image.Resampling.LANCZOS),(14,34))
    d.text((700,12),'FIRST PAINTED ASSEMBLY / native and half',fill='white')
    control=reference.crop((889,19,1069,469)).convert('RGBA')
    for x,label,image in [(700,'Reference crop',control),(890,'Painted assembly',master)]:
        d.text((x,45),label,fill='white')
        n=scaled(image,model['logicalScale'])
        h=scaled(image,model['logicalScale']/2)
        plate.paste(n,(x+10,70),n)
        plate.paste(h,(x+80,70),h)
    d.text((700,195),'Offline ordinary paving context, NOT native scene',fill='white')
    plate.paste(ground,(700,215))
    d.text((14,430),'Complete independent source layers / 40% source-canvas assembly diagnostic',fill='white')
    diagnostic=scaled(master,.4)
    plate.paste(diagnostic,(30,448),diagnostic)
    d.text((160,456),'Three complete raster components, real provider alpha.',fill='white')
    d.text((160,480),'Uniform scale + translation only. No relighting or contour warp.',fill='white')
    d.text((160,504),'Pole remains painted behind head and box. No inferred pan frames.',fill='white')
    d.text((160,528),'Generated base is wider than benchmark at equal pole height.',fill='white')
    d.text((160,552),'Not a 16-part or full-3D master. Owner/source/production acceptance absent.',fill='white')
    d.text((160,576),'Raw originals and metadata retained; only alpha1-15 dust outside padded crops omitted.',fill='white')
    plate.save(out/'comparison.png')
    ImageOps.grayscale(plate).save(out/'comparison-grayscale.png')
    # Diagnostic backgrounds expose actual semitransparency, not a new art sample.
    for name,color in [('alpha-on-white','white'),('alpha-on-black','black')]:
        bg=Image.new('RGB',master.size,color)
        bg.paste(master,(0,0),master)
        bg.save(out/f'{name}.png')
    return dict(native=list(native.size),half=list(half.size),canvas=model['canvas'])

def build(out,model_path=None):
    model_path=model_path or HERE/'assembly.json'
    model=json.loads(model_path.read_text())
    out.mkdir(parents=True,exist_ok=True)
    master,layers,crops,inspection=render(model)
    master.save(out/'camera-master.png')
    for sub,items in [('layers',layers),('source-layers',crops)]:
        (out/sub).mkdir(exist_ok=True)
        for name,image in items.items():
            image.save(out/sub/f'{name}.png')
    sizes=comparisons(model,master,out)
    inputs={}
    for p in sorted((HERE/'inputs').iterdir()):
        rec=dict(sha256=sha(p),bytes=p.stat().st_size)
        if p.suffix=='.png':
            with Image.open(p) as im:
                rec.update(actualSize=list(im.size),mode=im.mode,embeddedMetadata=im.info)
        inputs[p.name]=rec
    record=dict(status=STATUS,visualAttempt=1,ownerAccepted=False,productionAdmitted=False,nativeCapture=False,
        python=sys.version.split()[0],pillow=Image.__version__,modelSHA256=sha(model_path),rendererSHA256=sha(Path(__file__)),
        inputs=inputs,sourceInspection=inspection,sizes=sizes,
        exports={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*.png'))})
    dump(out/'manifest.json',record)
    print(json.dumps(dict(out=str(out),exports=len(record['exports']),sizes=sizes,inspection=inspection)))
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE/'preview-01')
    parser.add_argument('--model',type=Path,default=HERE/'assembly.json')
    args=parser.parse_args()
    build(args.out,args.model)
