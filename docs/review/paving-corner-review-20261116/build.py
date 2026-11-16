"""Deterministic review-only paving material assembly and authored ground layout.
No runtime code, collision data, source PNGs or prior packets are modified.
"""
import hashlib
import json
import math
from pathlib import Path
import random
from PIL import Image, ImageOps, ImageDraw

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source():
    spec = json.loads((HERE / 'source.json').read_text())
    path = (HERE / spec['input']).resolve()
    if sha(path) != spec['inputSHA256']:
        raise ValueError('Immutable source digest changed')
    with Image.open(path) as image:
        source = image.convert('RGB')
    return spec, source


def material(spec, source):
    size, count = spec['slabPixels'], spec['slabsPerSupertile']
    grid = spec['sourceGrid']
    patches = []
    for y in range(4):
        for x in range(4):
            # Exclude the old painted joint. All new joints are authored once.
            box = (grid[x]+4, grid[y]+4, grid[x+1]-4, grid[y+1]-4)
            patches.append(source.crop(box).resize((size, size), Image.Resampling.LANCZOS))
    rng = random.Random(spec['seed'])
    pairs = [(a, b) for a in range(16) for b in range(16) if a != b]
    rng.shuffle(pairs)
    result = Image.new('RGB', (size*count, size*count))
    records = []
    low, high = spec['mixtureRange']
    for cell in range(count*count):
        a, b = pairs[cell]
        coarse = Image.new('L', (5, 5))
        coarse.putdata([round(255*rng.uniform(low, high)) for _ in range(25)])
        mask = coarse.resize((size, size), Image.Resampling.BICUBIC)
        slab = Image.composite(patches[b], patches[a], mask)
        pixels = slab.load()
        band = spec['jointBlendPixels']
        for y in range(size):
            for x in range(size):
                distance = min(x, y, size-1-x, size-1-y)
                if distance < band:
                    t = distance/band
                    t = t*t*(3-2*t)
                    pixels[x, y] = tuple(round(j*(1-t)+v*t) for j, v in zip(spec['jointRGB'], pixels[x,y]))
        x, y = cell % count, cell // count
        result.paste(slab, (x*size, y*size))
        records.append({'cell': [x, y], 'sourceSlabs': [a, b],
                        'mixtureMaskSHA256': hashlib.sha256(mask.tobytes()).hexdigest(),
                        'pixelsSHA256': hashlib.sha256(slab.tobytes()).hexdigest()})
    return result, records


def curb_distance(x, y, layout):
    """Signed authored distance near the convex rounded paving corner.
    Negative = paving. This is presentation geometry, not collision truth.
    """
    edge_x, edge_y, radius = layout['verticalEdgeX'], layout['horizontalEdgeY'], layout['radius']
    cx, cy = edge_x-radius, edge_y+radius
    if x > cx and y < cy:
        return math.hypot(x-cx, y-cy)-radius
    return max(x-edge_x, edge_y-y)


def context(spec, tile):
    layout = spec['corner']
    x0, y0, x1, y1 = layout['worldBounds']
    scale = layout['pixelsPerWorldUnit']
    width, height = round((x1-x0)*scale), round((y1-y0)*scale)
    image = Image.new('RGB', (width, height))
    dest, texture = image.load(), tile.load()
    texscale = spec['slabPixels']/spec['slabWorldUnits']
    for py in range(height):
        y = y1-py/scale
        for px in range(width):
            x = x0+px/scale
            d = curb_distance(x, y, layout)
            # Stable source-authored road grain, no runtime RNG or wall clock.
            grain = (((int(x*4)*73856093) ^ (int(y*4)*19349663)) & 15)-7
            if d <= 0:
                value = texture[int(x*texscale) % tile.width, int(-y*texscale) % tile.height]
            elif d <= layout['curbWidth']:
                shade = 130 if d < layout['curbWidth']-1.2 else 69
                # Curb blocks follow the authored straight/rounded boundary.
                cx, cy = layout['verticalEdgeX']-layout['radius'], layout['horizontalEdgeY']+layout['radius']
                if x > cx and y < cy:
                    along = layout['radius']*math.atan2(cy-y, x-cx)
                elif x >= layout['verticalEdgeX']:
                    along = y-cy
                else:
                    along = x-cx
                if abs(along % 16) < .55:
                    shade -= 26
                value = (shade+grain//3, shade-4+grain//3, shade-10+grain//3)
            else:
                shade = 63+grain
                value = (shade, shade+1, shade+2)
                for rail in layout['railX']:
                    if abs(x-rail) < 2.2:
                        value = (29, 29, 29)
                    if abs(x-rail+.8) < .4:
                        value = (124, 120, 108)
                if layout['crossingX'][0] <= x <= layout['crossingX'][1]:
                    if any(abs(y-line) < 4 for line in layout['crossingY']):
                        if ((int(x*2)*31 ^ int(y*2)*53) % 19) > 3:
                            value = (147+grain, 141+grain, 129+grain)
            dest[px, py] = value
    # Explicitly authored decorative street surfaces, never collision features.
    draw = ImageDraw.Draw(image)
    def point(x, y):
        return (round((x-x0)*scale), round((y1-y)*scale))
    def box(rect):
        a,b,c,d = rect
        return (*point(a,d), *point(c,b))
    drain = layout['drain']
    draw.rectangle(box(drain), fill=(33,34,32), outline=(94,90,80), width=max(1,round(scale)))
    for y in range(drain[1]+3, drain[3]-1, 4):
        draw.line([point(drain[0]+2,y),point(drain[2]-2,y)], fill=(106,101,88), width=max(1,round(scale)))
    tactile = layout['tactile']
    draw.rectangle(box(tactile), fill=(143,113,64), outline=(89,76,55), width=max(1,round(scale)))
    for y in range(tactile[1]+3, tactile[3]-1, 4):
        for x in range(tactile[0]+3,tactile[2]-1,4):
            draw.ellipse(box((x-.8,y-.8,x+.8,y+.8)), fill=(182,151,95), outline=(104,85,55))
    mx,my,r = layout['manhole']
    draw.ellipse(box((mx-r,my-r,mx+r,my+r)), fill=(45,45,42), outline=(22,23,22), width=max(1,round(scale)))
    for dy in range(-8,9,4):
        for dx in range(-8,9,4):
            if dx*dx+dy*dy < (r-2)**2:
                draw.rectangle(box((mx+dx-.8,my+dy-.8,mx+dx+.8,my+dy+.8)), fill=(81,77,67))
    return image


def midpoint(image):
    """Orthographic ground-only preview, not a native capture or art acceptance."""
    # x'=(x-y)/sqrt(2), y'=(x+y)/(2sqrt(2)); inverse for Pillow sampling.
    r = math.sqrt(2)
    width = math.ceil((image.width+image.height)/r)
    height = math.ceil((image.width+image.height)/(2*r))
    offset = image.height/r
    return image.convert('RGBA').transform((width, height), Image.Transform.AFFINE,
        (1/r, r, -offset/r, -1/r, r, offset/r),
        resample=Image.Resampling.BICUBIC)


def build(output=HERE):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    spec, source = read_source()
    tile, records = material(spec, source)
    tile.save(output/'paving-supertile.png')
    repeat = Image.new('RGB', (tile.width*2, tile.height*2))
    for y in range(2):
        for x in range(2):
            repeat.paste(tile, (x*tile.width, y*tile.height))
    repeat.resize((1024, 1024), Image.Resampling.LANCZOS).save(output/'repeat-2x2.png')
    corner = context(spec, tile)
    corner.save(output/'corner-topdown.png')
    projected = midpoint(corner)
    projected.thumbnail((704, 352), Image.Resampling.LANCZOS)
    projected.save(output/'corner-midpoint-preview.png')
    gray = ImageOps.grayscale(projected).convert('RGBA')
    gray.putalpha(projected.getchannel('A'))
    gray.save(output/'corner-midpoint-grayscale.png')
    outputs = ['paving-supertile.png', 'repeat-2x2.png', 'corner-topdown.png',
               'corner-midpoint-preview.png', 'corner-midpoint-grayscale.png']
    manifest = {'status': spec['status'], 'sourceSHA256': sha(HERE/'source.json'),
                'builderSHA256': sha(Path(__file__)),
                'inputSHA256': spec['inputSHA256'], 'slabWorldUnits': spec['slabWorldUnits'],
                'tileWorldUnits': spec['slabWorldUnits']*spec['slabsPerSupertile'],
                'sourceMixtures': records, 'outputs': {f: sha(output/f) for f in outputs},
                'limits': spec['limits']}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'Built {len(records)} material mixtures and authored corner; NOT native or accepted')
    return manifest


if __name__ == '__main__':
    build()
