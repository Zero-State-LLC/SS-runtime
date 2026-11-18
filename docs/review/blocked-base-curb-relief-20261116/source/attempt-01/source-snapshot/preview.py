"""First synthetic source preview over immutable V8 native context. Not native evidence."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
from replay import HERE, ROOT, load, project
V8=ROOT/'docs/review/footprint-ground-repair-20261116/scene/native-capture-v8'
def label(image,text):
    sheet=Image.new('RGB',(image.width,image.height+28),(30,33,34));sheet.paste(image,(0,28));ImageDraw.Draw(sheet).text((8,8),text,fill='white');return sheet

def build(out):
    if out.exists():raise RuntimeError('Preview already exists. No second aesthetic attempt without bounded coordinator correction.')
    out.mkdir();regs=load(HERE/'attempt-01/registration.json');center=project([684,724,0]);composites=[]
    for zoom in [1,1.25,1.4]:
        code=round(100*zoom);im=Image.open(V8/f'source-scene-candidate-ordinary-z{code}-native.png').convert('RGBA')
        for reg in sorted(regs,key=lambda r:sum(r['registration']['worldPosition']),reverse=True):
            r=reg['registration'];p=project(r['worldPosition']+[0]);factor=3*zoom/4
            src=Image.open(ROOT/reg['image']['path']).convert('RGBA');src=src.resize(tuple(max(1,round(n*factor)) for n in src.size),Image.Resampling.NEAREST)
            x=round(3*(352+zoom*(p[0]-center[0]))-r['rootPixelsTopLeft'][0]*factor)
            y=round(3*(163-zoom*(p[1]-center[1]))-r['rootPixelsTopLeft'][1]*factor)
            im.alpha_composite(src,(x,y))
        im=im.convert('RGB');composites.append(im)
        title=f'SYNTHETIC SOURCE PREVIEW attempt01 zoom {zoom}: V8 native context + XYZ relief overlay. NOT native depth evidence.'
        label(im,title).save(out/f'context-z{code}.png')
        label(im.resize((1056,489),Image.Resampling.NEAREST),title).save(out/f'context-z{code}-half.png')
        label(ImageOps.grayscale(im).convert('RGB'),title).save(out/f'context-z{code}-grayscale.png')
    detail=composites[0].crop((660,540,1120,900)).resize((920,720),Image.Resampling.NEAREST)
    label(detail,'SYNTHETIC SOURCE PREVIEW: blocked base + curb detail, nearest enlargement').save(out/'base-curb-detail.png')
    ref=Image.open(ROOT/'docs/review/building-perspective-detail-20261116/kiosk/inputs/benchmark.png').convert('RGB')
    ref.thumbnail((1056,720),Image.Resampling.NEAREST)
    current=composites[0].resize((1056,489),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(2112,780),(30,33,34));sheet.paste(ref,(0,40));sheet.paste(current,(1056,40));d=ImageDraw.Draw(sheet)
    d.text((12,12),'ORIGINAL FULL UNCROPPED BENCHMARK (scaled to fit)',fill='white');d.text((1068,12),'SYNTHETIC SOURCE PREVIEW attempt01, actual retained V8 context',fill='white')
    d.text((1068,550),'Not a native capture, source recommendation, visual acceptance or depth proof.',fill='white')
    d.text((1068,575),'53 separately registered supplemental sprites. All V8 sources remain unchanged.',fill='white')
    sheet.save(out/'full-benchmark-comparison.png')
    (out/'preview-metadata.json').write_text(json.dumps(dict(schema='synthetic-relief-preview-009',attempt=1,zooms=[1,1.25,1.4],kind='SYNTHETIC_SOURCE_PREVIEW',centerWorld=[684,724],nativeEvidence=False,occlusion='Source overlays sorted by contact-root projection only. Native geometry-depth ordering must be verified by scene lane.',benchmark='Full original uncropped, uniformly scaled',sourceRegistration='attempt-01/registration.json'),indent=2)+'\n')
if __name__=='__main__':build(HERE/'attempt-01/preview')
