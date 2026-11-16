"""Material-only bounded correction. All masks come from unchanged shared plan."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def load():return json.loads((HERE/'materials.json').read_text())
def tiles():
    spec=load()
    for key in ('retainedPaving','retainedOriginal'):
        row=spec[key]
        if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Retained paving input changed')
    if hashlib.sha256((HERE/'plan.json').read_bytes()).hexdigest()!=spec['sharedPlanSHA256']:raise ValueError('Shared plan changed during material correction')
    with Image.open(ROOT/spec['retainedPaving']['path']) as src:
        paving=src.convert('RGB').resize(tuple(spec['pavingTilePixels']),Image.Resampling.LANCZOS)
        stone=src.crop((6,6,122,122)).convert('L').resize((192,192),Image.Resampling.BICUBIC)
    result={3:paving}
    for kind,base in ((1,(57,57,56)),(2,(164,156,139)),(4,(111,103,88))):
        image=Image.new('RGB',(192,192));pixels=[]
        for y in range(192):
            for x in range(192):
                natural=(stone.getpixel((x,y))-125)//(5 if kind==1 else 3)
                grit=((x*31+y*43+x*y%71)%11-5)//(2 if kind==1 else 3)
                if kind==2:
                    # Warm worn limestone, joints every24 world units in both axes.
                    joint=24 if x%48<2 or y%48<2 else 0
                    bevel=5 if x%48 in (2,47) or y%48 in (2,47) else 0
                elif kind==4:
                    # Foundation block courses differ visibly from the walkable slabs.
                    joint=17 if y%24<2 or (x+(24 if (y//24)%2 else 0))%48<2 else 0;bevel=0
                else:joint=0;bevel=0
                pixels.append(tuple(max(0,min(255,v+natural+grit-joint+bevel)) for v in base))
        image.putdata(pixels);result[kind]=image
    return result

def paint(ids):
    spec=load();n=ids.width;image=Image.new('RGB',ids.size)
    for key,tile in tiles().items():
        tile.save(HERE/f'material-{key}-tile.png')
        layer=Image.new('RGB',ids.size)
        for y in range(0,n,tile.height):
            for x in range(0,n,tile.width):layer.paste(tile,(x,y))
        image.paste(layer,(0,0),ids.point(lambda v:255 if v==key else 0))
    # Semantic masks are retained as editable inputs and independent clipping witnesses.
    roadmask=ids.point(lambda v:255 if v==1 else 0);roadmask.save(HERE/'road-mask.png')
    details=Image.new('RGBA',ids.size);draw=ImageDraw.Draw(details)
    svg=[]
    def box(r):return [int(2*r[0]),int(n-2*r[3]),int(2*r[2])-1,int(n-2*r[1])-1]
    for detail in spec['roadDetails']:
        q=box(detail['bounds']);kind=detail['kind']
        if kind in ('crossing','lane'):
            color=(181,172,139,190) if kind=='crossing' else (170,153,111,130)
            draw.rectangle(q,fill=color)
            # Restrained paint loss, never more than one pixel per17; fixed material origin.
            for yy in range(q[1],q[3]+1):
                for xx in range(q[0],q[2]+1):
                    if (xx*19+yy*37)%17==0:draw.point((xx,yy),fill=(0,0,0,0))
            svg.append(f'<rect x="{q[0]}" y="{q[1]}" width="{q[2]-q[0]+1}" height="{q[3]-q[1]+1}" fill="rgb{color[:3]}" opacity="{color[3]/255}"/>')
        elif kind=='drain':
            draw.rectangle(q,fill=(31,34,33,255),outline=(107,103,89,255),width=2)
            for xx in range(q[0]+4,q[2],6):draw.line((xx,q[1]+3,xx,q[3]-3),fill=(101,102,91,255),width=2)
            svg.append(f'<rect x="{q[0]}" y="{q[1]}" width="{q[2]-q[0]+1}" height="{q[3]-q[1]+1}" fill="#252927" stroke="#6b6759"/>')
        else:
            draw.ellipse(q,fill=(63,64,59,255),outline=(115,108,90,255),width=3)
            draw.ellipse((q[0]+5,q[1]+5,q[2]-5,q[3]-5),outline=(38,41,38,255),width=2)
            for xx in range(q[0]+12,q[2]-10,8):draw.line((xx,q[1]+12,xx,q[3]-12),fill=(88,86,72,255),width=1)
            svg.append(f'<ellipse cx="{(q[0]+q[2])/2}" cy="{(q[1]+q[3])/2}" rx="{(q[2]-q[0])/2}" ry="{(q[3]-q[1])/2}" fill="#3f403b" stroke="#736c5a"/>')
    alpha=ImageChops.multiply(details.getchannel('A'),roadmask);details.putalpha(alpha)
    details.save(HERE/'road-details.png');alpha.save(HERE/'road-details-mask.png')
    image=Image.alpha_composite(image.convert('RGBA'),details).convert('RGB')
    (HERE/'road-details.svg-fragment').write_text('\n'.join(svg)+'\n')
    return image
