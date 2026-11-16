#!/usr/bin/env python3
"""Padding-only adapter around the byte-exact archived painted renderer."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageOps
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archived_painted_renderer',HERE/'control/replay.py')
r=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
STATUS='PADDING_CORRECTED_TECHNICAL_SOURCE_ONLY_NOT_ACCEPTED'

def border_alpha(im):
    a=im.getchannel('A')
    w,h=a.size
    return max(a.crop((0,0,w,1)).tobytes()+a.crop((0,h-1,w,h)).tobytes()+a.crop((0,0,1,h)).tobytes()+a.crop((w-1,0,w,h)).tobytes())

def invariants(model,master,layers):
    old=json.loads((HERE/'control/assembly.json').read_text())
    expected=json.loads(json.dumps(old))
    expected['canvas'][0]+=24
    expected['root'][0]+=12
    for layer in expected['layers']:
        layer['position'][0]+=12
    if model!=expected:
        raise ValueError('Changes exceed authorized symmetric padding')
    with Image.open(HERE/'control/preview-01/camera-master.png') as prior:
        prior=prior.convert('RGBA')
    if border_alpha(prior)!=215:
        raise ValueError('Archived failure evidence changed')
    if border_alpha(master)!=0 or any(border_alpha(im)!=0 for im in layers.values()):
        raise ValueError('Padded outer border is not fully transparent')
    # The prior edge clipped the 3-source-pixel LANCZOS support. Everything
    # outside those three columns must be exactly an integer translation.
    if master.crop((15,0,192,450)).tobytes()!=prior.crop((3,0,180,450)).tobytes():
        raise ValueError('Previously unclipped subject pixels changed')
    for name,image in layers.items():
        with Image.open(HERE/'control/preview-01/layers'/f'{name}.png') as old_layer:
            if image.crop((15,0,192,450)).tobytes()!=old_layer.crop((3,0,180,450)).tobytes():
                raise ValueError('Unclipped layer pixels changed: '+name)
    fringe=master.crop((0,0,12,450)).getchannel('A')
    restored=sum(v>0 for v in fringe.tobytes())
    if restored==0:
        raise ValueError('No clipped fringe restored: padding old composite is insufficient')
    changed_old_cols=set()
    a=prior.load()
    b=master.load()
    for y in range(450):
        for x in range(180):
            if a[x,y]!=b[x+12,y]:
                changed_old_cols.add(x)
    if not changed_old_cols.issubset({0,1,2}):
        raise ValueError('Differences outside previous clipping support')
    return dict(archivedBorderMaxAlpha=215,paddedBorderMaxAlpha=0,allLayerBordersTransparent=True,
        restoredLeftFringePixels=restored,restoredLeftFringeAlphaSum=sum(fringe.tobytes()),
        changedPriorColumns=sorted(changed_old_cols),unclippedExactComparisonColumns=[3,180],
        preservedUnclippedPixels=177*450,sourceRootTranslation=[12,0],
        sourceGeometryMaterialAndLogicalScaleUnchanged=True)

def registration(model,master_path,native,half):
    w,h=model['canvas']
    x,y=model['root']
    s=model['logicalScale']
    return dict(status=STATUS,kind='upright',canvasPixels=[w,h],sourceCanvas=[w,h],
        rootPixelsTopLeft=[x,y],sourceRoot=[x,y],uniformDrawScale=s,
        drawSizeWorld=[w*s,h*s],spriteSizeScenePoints=[w*s,h*s],
        spriteAnchorBottomLeft=[x/w,1-y/h],
        rootPixelsNativeTopLeft=[x*s,y*s],nativeRasterSize=list(native.size),halfRasterSize=list(half.size),
        image='final/camera-master.png',sourceSHA256=r.sha(master_path),
        originalLogicalScaleUnchanged=True,
        mapping='worldDelta=(sourceX-58, 427-sourceY)*(96/418). Padding translates sourceX and rootX equally. Use the204x450 source master at uniformDrawScale, not nonuniform fit to rounded native pixels.',
        registrationScope='Inherited review projection anchor only. No new world position, collision, field or production-admission claim.',
        ownerAccepted=False,productionAdmitted=False)

def comparison(model,master,native,half,out):
    with Image.open(HERE/'inputs/reference.png') as im:
        reference=im.convert('RGB')
    with Image.open(HERE/'inputs/paving.png') as im:
        context=im.convert('RGB').resize((352,352),Image.Resampling.LANCZOS).crop((0,0,352,200))
    context.paste(native,(160,55),native)
    context.save(out/'ordinary-background-context.png')
    plate=Image.new('RGB',(1100,630),'#303334')
    d=ImageDraw.Draw(plate)
    d.text((14,12),'UNCHANGED ORIGINAL / full reference / uniform fit',fill='white')
    plate.paste(reference.resize((660,371),Image.Resampling.LANCZOS),(14,34))
    d.text((700,12),'PADDING-ONLY FINAL / no aesthetic changes',fill='white')
    d.text((700,45),'Native47x104 / Half24x52',fill='white')
    plate.paste(native,(720,70),native)
    plate.paste(half,(810,70),half)
    d.text((700,195),'Offline background context, not native scene',fill='white')
    plate.paste(context,(700,215))
    d.text((14,430),'Archived clipped control / final source, both40% construction scale',fill='white')
    with Image.open(HERE/'control/preview-01/camera-master.png') as im:
        control=r.scaled(im.convert('RGBA'),.4)
    final=r.scaled(master,.4)
    plate.paste(control,(30,448),control)
    plate.paste(final,(140,448),final)
    d.text((290,456),'Canvas180->204. Root46->58. All layer origins+12X.',fill='white')
    d.text((290,482),'Source paint, geometry, uniform scales and world-relative mapping unchanged.',fill='white')
    d.text((290,508),'Outer border alpha0. Previously clipped left fringe restored from source.',fill='white')
    d.text((290,534),'All prior pixels outside3-column clipped filter support identical after translation.',fill='white')
    d.text((290,560),'Three neutral raster layers. No new source/owner/production acceptance.',fill='white')
    plate.save(out/'comparison.png')
    ImageOps.grayscale(plate).save(out/'comparison-grayscale.png')

def build(out):
    model=json.loads((HERE/'assembly.json').read_text())
    master,layers,crops,inspection=r.render(model,HERE/'inputs')
    evidence=invariants(model,master,layers)
    native=r.scaled(master,model['logicalScale'])
    half=r.scaled(master,model['logicalScale']/2)
    if border_alpha(native)!=0 or border_alpha(half)!=0:
        raise ValueError('Native/half border not transparent')
    out.mkdir(parents=True,exist_ok=True)
    for name,image in [('camera-master',master),('camera-native',native),('camera-half',half)]:
        image.save(out/f'{name}.png')
    for folder,images in [('layers',layers),('source-layers',crops)]:
        (out/folder).mkdir(exist_ok=True)
        for name,image in images.items():
            image.save(out/folder/f'{name}.png')
    comparison(model,master,native,half,out)
    r.dump(out/'registration.json',registration(model,out/'camera-master.png',native,half))
    r.dump(out/'padding-evidence.json',evidence)
    r.dump(out/'source-inspection.json',inspection)
    record=dict(status=STATUS,python=sys.version.split()[0],pillow=Image.__version__,
        sources={str(p.relative_to(HERE)):r.sha(p) for p in [HERE/'assembly.json',HERE/'replay.py',HERE/'author.py',*sorted((HERE/'inputs').iterdir()),*sorted((HERE/'control').rglob('*'))] if p.is_file() and '__pycache__' not in p.parts},
        exports={str(p.relative_to(out)):r.sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'},
        ownerAccepted=False,productionAdmitted=False,technicalPaddingOnly=True)
    r.dump(out/'manifest.json',record)
    print(json.dumps(dict(out=str(out),sizes=dict(source=list(master.size),native=list(native.size),half=list(half.size)),evidence=evidence)))
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=HERE/'final')
    args=parser.parse_args()
    build(args.out)
