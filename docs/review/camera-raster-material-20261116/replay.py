#!/usr/bin/env python3
"""Editable raster-material mapper. No random/procedural texture generation.

ADAPT: inputs/prior-build.py:32-59 cubic path evaluation, recorded in provenance.
Only inputs/iron.png supplies material variation. Analytic illumination is shading,
not a noise/dab texture. The original reference is read only by comparison().
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
SS = 3

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def paths(source):
    tokens = re.findall(r'[MLCZ]|-?\d+(?:\.\d+)?', source)
    result, points, i = [], [], 0
    while i < len(tokens):
        command = tokens[i]
        i += 1
        if command == 'M':
            if points:
                result.append(points)
            points = [(float(tokens[i]), float(tokens[i+1]))]
            i += 2
        elif command == 'L':
            points.append((float(tokens[i]), float(tokens[i+1])))
            i += 2
        elif command == 'C':
            p0 = points[-1]
            p1, p2, p3 = [(float(tokens[i+j]), float(tokens[i+j+1])) for j in (0,2,4)]
            i += 6
            for step in range(1,33):
                t = step/32
                points.append(tuple((1-t)**3*p0[k]+3*(1-t)**2*t*p1[k]+3*(1-t)*t*t*p2[k]+t**3*p3[k] for k in (0,1)))
        elif command == 'Z':
            points.append(points[0])
        else:
            raise ValueError(command)
    if points:
        result.append(points)
    return result

def polygons(part, contour=None):
    sx, sy, tx, ty = part['transform']
    return [[((x*sx+tx)*SS, (y*sy+ty)*SS) for x,y in poly] for poly in paths(contour or part['contour'])]

def mask_for(size, part, contour=None):
    mask = Image.new('L', size)
    draw = ImageDraw.Draw(mask)
    for polygon in polygons(part, contour):
        draw.polygon(polygon, fill=255)
    return mask

def clean(image):
    image.paste((0,0,0,0), (0,0), image.getchannel('A').point(lambda a: 255 if a == 0 else 0))
    return image

def down(image, size):
    return clean(image.resize(size, Image.Resampling.LANCZOS))

def validate(model):
    if model['schema'] != 1 or model['status'] != 'FIRST_PILOT_REVIEW_ONLY':
        raise ValueError('Unsupported model/status')
    names = [p['name'] for p in model['parts']]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate component')
    for p in model['parts']:
        if p['material'] != 'iron.png':
            raise ValueError('Only packet-local independent iron material allowed')
        u,v,w,h = p['uv']
        if min(u,v) < 0 or min(w,h) <= 0 or u+w > 1254 or v+h > 1254:
            raise ValueError('UV outside inspected material extent')

def render(model, inputs=None, omit=()):
    validate(model)
    inputs = inputs or HERE/'inputs'
    with Image.open(inputs/'iron.png') as im:
        material = im.convert('L')
    size = tuple(n*SS for n in model['canvas'])
    result = Image.new('RGBA', size)
    layers, samples = {}, {}
    for part in model['parts']:
        mask = mask_for(size, part)
        box = mask.getbbox()
        if not box:
            raise ValueError('Empty component '+part['name'])
        x0,y0,x1,y1 = box
        w,h = x1-x0,y1-y0
        u,v,uw,vh = part['uv']
        # Explicit per-component UV window, no sampling from benchmark or prior master.
        sample = material.transform((w,h), Image.Transform.EXTENT, (u,v,u+uw,v+vh), Image.Resampling.BICUBIC)
        samples[part['name']] = sample
        pixels = sample.load()
        face_masks = [(mask_for(size, part, f['contour']).crop(box).load(), f['gain']) for f in part['faces']]
        shade = part['shading']
        rgb = Image.new('RGBA', (w,h))
        dst = rgb.load()
        for y in range(h):
            vv = y/max(1,h-1)
            for x in range(w):
                uu = x/max(1,w-1)
                light = shade['ambient'] + shade['roundness']*max(0, math.cos((uu-shade['light_u'])*math.pi)) + shade['vertical']*(1-vv)
                for fm,gain in face_masks:
                    if fm[x,y]:
                        light *= gain
                variation = 1 + part['texture_strength']*(pixels[x,y]-70)/70
                dst[x,y] = tuple(max(0,min(255,round(c*light*variation))) for c in part['tint'])+(255,)
        layer = Image.new('RGBA', size)
        layer.paste(rgb, (x0,y0))
        layer.putalpha(mask)
        edge = part['edge']
        if edge['width']:
            draw = ImageDraw.Draw(layer)
            for poly in polygons(part):
                draw.line(poly, fill=tuple(edge['color'])+(255,), width=max(1,round(edge['width']*SS)), joint='curve')
        layers[part['name']] = down(layer, tuple(model['canvas']))
        if part['visible'] and part['name'] not in omit:
            result.alpha_composite(layer)
    return down(result, tuple(model['canvas'])), layers, samples

def comparison(model, master, out):
    scale = model['scale']
    native_size = tuple(math.ceil(n*scale) for n in model['canvas'])
    half_size = tuple(math.ceil(n*scale/2) for n in model['canvas'])
    native, half = down(master, native_size), down(master, half_size)
    native.save(out/'camera-native.png')
    half.save(out/'camera-half.png')
    with Image.open(HERE/'inputs/reference.png') as im:
        reference = im.convert('RGB')
    with Image.open(HERE/'inputs/rejected-master.png') as im:
        rejected = im.convert('RGBA')
    with Image.open(HERE/'inputs/paving.png') as im:
        ground = im.convert('RGB').resize((352,352), Image.Resampling.LANCZOS)
    context = ground.crop((0,0,352,200))
    context.paste(native, (166,55), native)
    context.save(out/'ordinary-background-context.png')
    plate = Image.new('RGB', (1100,630), '#303334')
    draw = ImageDraw.Draw(plate)
    draw.text((14,12), 'UNCHANGED ORIGINAL: full image, uniformly fitted. Review only, not source acceptance.', fill='white')
    plate.paste(reference.resize((660,371), Image.Resampling.LANCZOS), (14,34))
    draw.text((700,12), 'ONE raster-material pilot | native / half', fill='white')
    # Crop is comparison only, never a render input, and is not an editable master.
    ref_crop = reference.crop((889,19,1069,469)).convert('RGBA')
    for col,(label,image) in enumerate([('Reference crop',ref_crop),('Rejected prior',rejected),('Pilot',master)]):
        xx = 700+col*125
        draw.text((xx,45), label, fill='white')
        plate.paste(down(image,native_size), (xx+10,70), down(image,native_size))
        plate.paste(down(image,half_size), (xx+65,70), down(image,half_size))
    draw.text((700,195), 'Ordinary paving context: offline, no HUD/field', fill='white')
    plate.paste(context,(700,215))
    draw.text((14,430), 'Contour diagnostic at 40% construction scale: rejected / corrected (not game size)', fill='white')
    plate.paste(down(rejected,(72,180)), (50,450), down(rejected,(72,180)))
    plate.paste(down(master,(72,180)), (170,450), down(master,(72,180)))
    draw.text((300,460), 'Editable: 16 complete contours, local iron material, UV windows,', fill='white')
    draw.text((300,480), 'tint, continuous illumination, broad face gains and draw order.', fill='white')
    draw.text((300,505), 'Head depth -15%; base width -8%; narrower bracket return.', fill='white')
    draw.text((300,530), 'Cream enamel uses tinted iron microstructure: a disclosed approximation.', fill='white')
    draw.text((300,555), 'No native capture, collision/registration validation or visual acceptance.', fill='white')
    plate.save(out/'comparison.png')
    ImageOps.grayscale(plate).save(out/'comparison-grayscale.png')
    return dict(native=list(native_size),half=list(half_size),source=list(master.size),context=[352,200])

def build(out, model_path=None):
    model_path = model_path or HERE/'model.json'
    model = json.loads(model_path.read_text())
    out.mkdir(parents=True, exist_ok=True)
    master,layers,samples = render(model)
    master.save(out/'camera-master.png')
    for sub in ('components','uv-samples'):
        (out/sub).mkdir(exist_ok=True)
    for name,image in layers.items():
        image.save(out/'components'/f'{name}.png')
        samples[name].save(out/'uv-samples'/f'{name}.png')
    sizes = comparison(model,master,out)
    record = dict(status='FIRST_PILOT_REVIEW_ONLY', ownerAccepted=False, productionAdmitted=False,
                  nativeCapture=False, visualAttempt=1, python=sys.version.split()[0], pillow=Image.__version__,
                  modelSHA256=sha(model_path), rendererSHA256=sha(Path(__file__)), sizes=sizes,
                  inputs={p.name:sha(p) for p in sorted((HERE/'inputs').iterdir()) if p.is_file()},
                  exports={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*.png'))})
    (out/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(output=str(out),components=len(layers),exports=len(record['exports']),sizes=sizes)))
    return record

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=HERE/'pilot-01')
    parser.add_argument('--model', type=Path, default=HERE/'model.json')
    args = parser.parse_args()
    build(args.out,args.model)
