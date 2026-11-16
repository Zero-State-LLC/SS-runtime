"""Editable front-garment UV triangle renderer. Never consumes a flattened character as material."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent

def rgba(path):
    with Image.open(path) as im:
        return im.convert('RGBA')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sample(texture, uv):
    """Pixel-edge UVs, premultiplied bilinear sampling, no repainted source pixels."""
    h,w = texture.shape[:2]
    p = np.clip(uv * [w,h] - .5, [0,0], [w-1,h-1])
    # Stabilize exact registered pixel centers after triangle arithmetic.
    p = np.where(np.abs(p-np.rint(p)) < 1e-9, np.rint(p), p)
    lo = np.floor(p).astype(int)
    hi = np.minimum(lo+1,[w-1,h-1])
    f = p-lo
    tex = texture.astype(float)/255
    tex[:,:,:3] *= tex[:,:,3:4]
    a = tex[lo[:,1],lo[:,0]]*(1-f[:,0,None]) + tex[lo[:,1],hi[:,0]]*f[:,0,None]
    b = tex[hi[:,1],lo[:,0]]*(1-f[:,0,None]) + tex[hi[:,1],hi[:,0]]*f[:,0,None]
    c = a*(1-f[:,1,None])+b*f[:,1,None]
    np.divide(c[:,:3],c[:,3:4],out=c[:,:3],where=c[:,3:4]>0)
    return np.clip(np.rint(c*255),0,255).astype(np.uint8)

def panel(surface, model, base):
    width,height = model['canvas']
    root = np.array(model['groundRoot'])
    vertices = np.array([v['position'] for v in surface['vertices']],float)*[1,-1]+root
    uv = np.array([v['uv'] for v in surface['vertices']],float)
    texture = np.array(rgba(base/surface['material']).resize(tuple(surface['materialRasterSize']),Image.Resampling.LANCZOS))
    out = np.zeros((height,width,4),np.uint8)
    owner = np.full((height,width),-1,np.int32)
    for face_id, indices in enumerate(surface['triangles']):
        tri = vertices[indices]
        low = np.maximum(np.floor(tri.min(axis=0)).astype(int),0)
        high = np.minimum(np.ceil(tri.max(axis=0)).astype(int),[width,height])
        if np.any(high<=low):
            continue
        matrix = np.stack([tri[1]-tri[0],tri[2]-tri[0]],axis=1)
        if abs(np.linalg.det(matrix)) < 1e-8:
            raise ValueError('Degenerate garment triangle')
        yy,xx = np.mgrid[low[1]:high[1],low[0]:high[0]]
        points = np.stack([xx.ravel()+.5,yy.ravel()+.5],axis=1)
        bc = (points-tri[0]) @ np.linalg.inv(matrix).T
        weights = np.column_stack([1-bc.sum(axis=1),bc])
        inside = np.all(weights>=-1e-9,axis=1)
        x,y = xx.ravel()[inside],yy.ravel()[inside]
        out[y,x] = sample(texture,weights[inside]@uv[indices])
        owner[y,x] = face_id
    return Image.fromarray(out),owner

def render(model,base=HERE):
    if model['schema'] != 1:
        raise ValueError('Unsupported garment schema')
    out = Image.new('RGBA',tuple(model['canvas']))
    layers = {}
    owners = {}
    for s in model['surfaces']:
        layer,owner = panel(s,model,base)
        out.alpha_composite(layer)
        layers[s['id']] = layer
        owners[s['id']] = owner
    for name in model['retainedLayers']:
        out.alpha_composite(rgba(base/name))
    return out,layers,owners

def build(base=HERE):
    model = json.loads((base/'garment.json').read_text())
    image,layers,owners = render(model,base)
    image.save(base/'south-neutral.png')
    (base/'diagnostics').mkdir(exist_ok=True)
    for name,layer in layers.items():
        layer.save(base/'diagnostics'/f'{name}.png')
        np.save(base/'diagnostics'/f'{name}-triangle-owner.npy',owners[name],allow_pickle=False)
    wire = image.copy()
    d = ImageDraw.Draw(wire)
    for s in model['surfaces']:
        points = [(192+v['position'][0],336-v['position'][1]) for v in s['vertices']]
        for t in s['triangles']:
            d.line([points[i] for i in t+[t[0]]],fill=(60,230,180,160),width=1)
    d.ellipse((189,333,195,339),outline='yellow')
    wire.save(base/'mesh-overlay.png')
    plate = Image.new('RGB',(1152,544),'#283036')
    d = ImageDraw.Draw(plate)
    sources = [rgba(base/'inputs/source/south-neutral-original.png'),rgba(base/'inputs/south-baggy-neutral.png'),image]
    labels = ['Original neutral (control)','Tracked baggy front (target)','Explicit front UV mesh (pilot 01)']
    for i,(im,label) in enumerate(zip(sources,labels)):
        plate.paste(im,(384*i,24),im)
        d.text((384*i+8,6),label,fill='white')
        plate.paste(im.resize((64,69),Image.Resampling.LANCZOS),(384*i+24,454),im.resize((64,69),Image.Resampling.LANCZOS))
        plate.paste(im.resize((32,35),Image.Resampling.LANCZOS),(384*i+120,454),im.resize((32,35),Image.Resampling.LANCZOS))
    plate.save(base/'comparison.png')
    record = dict(status=model['status'],sourceOnly=True,visualAttempts=1,familyExpanded=False,
        modelSHA256=sha(base/'garment.json'),outputSHA256=sha(base/'south-neutral.png'),
        geometry='4 front panels, 140 independently editable vertices, 192 triangles',
        hiddenRecovered=False,groundRoot=model['groundRoot'])
    (base/'build.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base',type=Path,default=HERE)
    build(parser.parse_args().base)
