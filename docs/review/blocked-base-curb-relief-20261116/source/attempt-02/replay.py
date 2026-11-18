"""Bounded material-only replay. Reuses frozen first renderer and exact geometry."""
import argparse, copy, importlib.util, json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=SOURCE.parents[3]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
first=module('v9_first_frozen_renderer',SOURCE/'replay.py')
project=first.project

def textures():
    s=load(HERE/'materials.json');sample=Image.open(ROOT/s['input']).convert('L').crop(s['crop']).resize(tuple(s['tilePixels']),Image.Resampling.NEAREST)
    mean=ImageStat.Stat(sample).mean[0]
    def stone(rgb):
        out=Image.new('RGBA',sample.size);out.putdata([tuple(max(0,min(255,round(c+(v-mean)*s['textureContrast']))) for c in rgb)+(255,) for v in sample.getdata()]);return out
    masonry=stone(s['masonryMeanRGB']);d=ImageDraw.Draw(masonry);w,h=masonry.size
    # Two rows per 36x18 world texture, broad36world stone lengths and half-block stagger.
    for row,y in enumerate((0,h//2)):
        d.line((0,y,w,y),fill=tuple(s['mortarRGB'])+(255,),width=2)
        d.line((0,y+2,w,y+2),fill=tuple(s['highlightRGB'])+(255,),width=1)
        x=0 if row==0 else w//2
        d.line((x,y,x,y+h//2),fill=tuple(s['mortarRGB'])+(255,),width=2)
    return dict(masonry=masonry,curb=stone(s['curbMeanRGB']),cap=stone(s['capMeanRGB']),curbcap=stone(s['curbMeanRGB']))

def build(out):
    if out.exists() and any(out.iterdir()):raise RuntimeError('Immutable attempt02 output exists')
    out.mkdir(parents=True,exist_ok=True);(out/'sprites').mkdir();(out/'textures').mkdir()
    geometry=load(HERE/'geometry.json');materials=load(HERE/'materials.json');tex=textures();regs=[]
    oldregs={r['id']:r for r in load(SOURCE/'attempt-01/registration.json')}
    for name,image in tex.items():image.save(out/'textures'/f'{name}.png')
    for original in geometry['sprites']:
        sprite=copy.deepcopy(original)
        for face in sprite['faces']:
            # Material UV transform only. Frozen authored geometry/UV source stays byte-identical.
            if face['material']=='masonry':face['uv']=[[u*materials['uvScale'][0],v*materials['uvScale'][1]] for u,v in face['uv']]
            if original['kind']=='curb-relief' and face['material']=='cap':face['material']='curbcap'
        image,anchor,visible=first.render(sprite,geometry,tex)
        path=out/'sprites'/f"{original['id']}.png";image.save(path)
        reg=copy.deepcopy(oldregs[original['id']]);assert reg['registration']['canvasPixels']==list(image.size) and reg['registration']['rootPixelsTopLeft']==anchor and reg['visibleFaceCount']==visible
        reg['image']=dict(path=str((HERE/'output/sprites'/path.name).relative_to(ROOT)),sha256=sha(path));regs.append(reg)
    (out/'registration.json').write_text(json.dumps(regs,indent=2)+'\n');print(json.dumps(dict(sprites=len(regs),output=str(out),geometryChanged=False)))
    return regs
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);build(p.parse_args().out)
