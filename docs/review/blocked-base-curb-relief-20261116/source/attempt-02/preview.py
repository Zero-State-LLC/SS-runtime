"""Synthetic preview with retained geometry-depth oracle and registered actor silhouettes.
No arbitrary paint masks: an actor occludes a supplement only when the joint
world-footprint ordering puts that actor in front. Original V8 pixels stay intact.
"""
import json, math, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageChops
import importlib.util
_spec=importlib.util.spec_from_file_location('v9_final_preview_renderer',Path(__file__).with_name('replay.py'))
_renderer=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_renderer)
HERE,SOURCE,ROOT,load,sha,module,project=(_renderer.HERE,_renderer.SOURCE,_renderer.ROOT,_renderer.load,_renderer.sha,_renderer.module,_renderer.project)
V8=ROOT/'docs/review/footprint-ground-repair-20261116/scene'
depth=module('v9_retained_depth_oracle',ROOT/'docs/review/scene-qa-repair-20261116/native.py')

def label(image,text):
    out=Image.new('RGB',(image.width,image.height+28),(30,33,34));out.paste(image,(0,28));ImageDraw.Draw(out).text((8,8),text,fill='white');return out

def scene_inputs(regs):
    baseline=load(V8/'native-capture-v8/source-scene-records.json');capture=next(c for c in baseline['captures'] if c['arm']=='candidate' and c['zoom']==1)
    items=list(capture['depthItems'])
    for r in regs:
        b=r['worldBoundsXYZ'];root=r['registration']['worldPosition']
        items.append(dict(name=r['id'],worldRoot=root,footprint=b['min'][:2]+b['max'][:2],projectedRootY=project(root+[0])[1]))
    ordered=depth.depth_order(items);ranks={name:i for i,name in enumerate(ordered['order'])}
    prepared=load(V8/'native-inputs-v8/native-inputs.json');sources={s['role']:s for s in prepared['sources']}
    assembly=load(V8/'assembly.json');roles={b['nodeName']:b['role'] for b in assembly['buildings']};roles.update({'sprite-camera-3':'camera','sprite-player':'player'})
    silhouettes=[];unmapped=[]
    for actor in capture['actors']:
        name=actor['name']
        if name in roles:
            s=sources[roles[name]];path=V8/'native-inputs-v8'/s['file'];assert sha(path)==s['sha256']
        elif name in ('benchmark-prop-0','benchmark-prop-1'):
            path=ROOT/'AppTests/BenchmarkAssets'/('newsbox.png' if name.endswith('0') else 'tree.png')
            assert sha(path)==baseline['controlSHA256'][path.name]
        else:unmapped.append(actor);continue
        silhouettes.append(dict(actor=actor,path=path,sha256=sha(path)))
    return capture,items,ordered,ranks,silhouettes,unmapped

def screen(root,zoom):
    p=project(root+[0]);c=project([684,724,0]);return [3*(352+zoom*(p[0]-c[0])),3*(163-zoom*(p[1]-c[1]))]

def actor_mask(row,zoom,size):
    a=row['actor'];image=Image.open(row['path']).convert('RGBA');target=[round(v*3*zoom) for v in a['size']]
    alpha=image.getchannel('A').resize(tuple(target),Image.Resampling.NEAREST)
    x,y=screen(a['worldRoot'],zoom);x=round(x-a['anchor'][0]*target[0]);y=round(y-(1-a['anchor'][1])*target[1])
    mask=Image.new('L',size);mask.paste(alpha,(x,y));return mask

def supplement_layer(r,zoom,size):
    reg=r['registration'];image=Image.open(ROOT/r['image']['path']).convert('RGBA');factor=3*zoom/4
    image=image.resize(tuple(max(1,round(n*factor)) for n in image.size),Image.Resampling.NEAREST)
    x,y=screen(reg['worldPosition'],zoom);x=round(x-reg['rootPixelsTopLeft'][0]*factor);y=round(y-reg['rootPixelsTopLeft'][1]*factor)
    layer=Image.new('RGBA',size);layer.alpha_composite(image,(x,y));return layer

def build(out):
    if out.exists():raise RuntimeError('Final preview is immutable. No third art pass.')
    out.mkdir();regs=load(HERE/'output/registration.json');capture,items,order,ranks,actors,unknown=scene_inputs(regs)
    records=[];composites=[]
    for zoom in [1,1.25,1.4]:
        code=round(zoom*100);im=Image.open(V8/f'native-capture-v8/source-scene-candidate-ordinary-z{code}-native.png').convert('RGBA')
        masks={a['actor']['name']:actor_mask(a,zoom,im.size) for a in actors}
        all_relief=Image.new('L',im.size)
        for r in regs:all_relief=ImageChops.lighter(all_relief,supplement_layer(r,zoom,im.size).getchannel('A'))
        for actor in unknown:
            x,y=screen(actor['worldRoot'],zoom);w,h=[v*3*zoom for v in actor['size']];left=round(x-actor['anchor'][0]*w);top=round(y-(1-actor['anchor'][1])*h)
            # Unknown legacy silhouette cannot be used to erase source. Fail if any relief could overlap it.
            box=(left,top,left+round(w),top+round(h))
            assert all_relief.crop(box).getbbox() is None,'Unknown retained silhouette overlaps relief: '+actor['name']
        layers=[]
        for r in sorted(regs,key=lambda r:ranks[r['id']]):
            layer=supplement_layer(r,zoom,im.size);raw=layer.getchannel('A');occlusion=Image.new('L',im.size);occluders=[]
            for actor in actors:
                name=actor['actor']['name']
                if ranks[name]<=ranks[r['id']]:continue
                overlap=ImageChops.multiply(raw,masks[name])
                if overlap.getbbox() is not None:
                    occlusion=ImageChops.lighter(occlusion,masks[name]);occluders.append(name)
            visible=ImageChops.multiply(raw,ImageOps.invert(occlusion));layer.putalpha(visible);im=Image.alpha_composite(im,layer)
            raw_count=sum(v for k,v in enumerate(raw.histogram()) if k);visible_count=sum(v for k,v in enumerate(visible.histogram()) if k)
            layers.append(dict(id=r['id'],rank=ranks[r['id']],occludingActors=occluders,rawPixels=raw_count,visiblePixels=visible_count,occlusionMaskSHA256=hashlib.sha256(occlusion.tobytes()).hexdigest(),visibleAlphaSHA256=hashlib.sha256(visible.tobytes()).hexdigest()))
        im=im.convert('RGB');composites.append(im)
        title=f'SYNTHETIC SOURCE PREVIEW attempt02 zoom {zoom}: actual V8 context + geometry-depth registered relief. NOT native evidence.'
        label(im,title).save(out/f'context-z{code}.png');label(im.resize((1056,489),Image.Resampling.NEAREST),title).save(out/f'context-z{code}-half.png');label(ImageOps.grayscale(im).convert('RGB'),title).save(out/f'context-z{code}-grayscale.png')
        records.append(dict(zoom=zoom,layers=layers))
    detail=composites[0].crop((660,540,1120,900)).resize((920,720),Image.Resampling.NEAREST)
    label(detail,'SYNTHETIC SOURCE PREVIEW attempt02: final bounded material correction, geometry depth').save(out/'base-curb-detail.png')
    ref=Image.open(ROOT/'docs/review/building-perspective-detail-20261116/kiosk/inputs/benchmark.png').convert('RGB');ref.thumbnail((1056,720),Image.Resampling.NEAREST)
    sheet=Image.new('RGB',(2112,780),(30,33,34));sheet.paste(ref,(0,40));sheet.paste(composites[0].resize((1056,489),Image.Resampling.NEAREST),(1056,40));d=ImageDraw.Draw(sheet)
    d.text((12,12),'ORIGINAL FULL UNCROPPED BENCHMARK (scaled to fit)',fill='white');d.text((1068,12),'SYNTHETIC SOURCE PREVIEW attempt02: final bounded correction',fill='white');d.text((1068,550),'Geometry-ordered registered silhouettes. Native rendering still independently required.',fill='white');d.text((1068,575),'Same53sprites, contacts, roots, height18/3, projection and all baseline source bytes.',fill='white');sheet.save(out/'full-benchmark-comparison.png')
    evidence=dict(schema='synthetic-relief-depth-preview-009',attempt=2,kind='SYNTHETIC_SOURCE_PREVIEW',nativeEvidence=False,zooms=[1,1.25,1.4],depthItems=items,depthOrder=order['order'],depthConstraints=order['constraints'],silhouetteSources=[dict(name=a['actor']['name'],path=str(a['path'].relative_to(ROOT)),sha256=a['sha256'],actor=a['actor']) for a in actors],unknownSilhouettes=[a['name'] for a in unknown],unknownSilhouetteOverlap=False,captures=records,rule='Only registered alpha of actors ranked in front by retained world-footprint depth may occlude supplemental pixels. No masks authored by hand.')
    (out/'preview-metadata.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Final preview generated, geometry-ranked silhouettes:',len(actors))
if __name__=='__main__':build(HERE/'output/preview')
