"""Diagnostic source-pixel/landmark correspondence; never a collision or slip test."""
from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
ASSETS=ROOT/'AppTests/BenchmarkAssets'
OUT=Path(__file__).resolve().parent
record=json.loads((ASSETS/'player-source-s-record.json').read_text())
for name,digest in record['sourceFiles'].items():
    assert hashlib.sha256((ASSETS/name).read_bytes()).hexdigest()==digest,name
poses=json.loads((ASSETS/'player-source-s-poses.json').read_text())
scale=record['sourceCanvas'][0]/record['logicalSize'][0]
rx,ry=record['rootPixels']
def project(v):
    x,y,z=v
    return rx+scale*x,ry+scale*(0.5*y-z)
canvas=Image.new('RGB',(528*4,334*4),'#181b1e')
rows=[]
for index,pose in enumerate(poses):
    im=Image.open(ASSETS/f'player-source-s-{index:02}.png').convert('RGBA')
    base=Image.new('RGBA',im.size,'#70757a');base.alpha_composite(im)
    marked=base.copy();draw=ImageDraw.Draw(marked)
    for leg in pose['legs']:
        toe=project(leg['toe']);heel=project(leg['heel'])
        color='#62e6eb' if leg['contact'] else '#ffca68'
        draw.line([heel,toe],fill=color,width=1)
        for x,y in [heel,toe]:
            draw.line([(x-3,y),(x+3,y)],fill=color,width=1)
            draw.line([(x,y-3),(x,y+3)],fill=color,width=1)
        if leg['contact']:
            # Small center-column band near the authored toe. No sole segmentation claim.
            x,y=toe;pixel_rows=[]
            for py in range(max(0,math.floor(y)-12),min(im.height,math.ceil(y)+13)):
                if any(im.getpixel((px,py))[3]>=128 for px in range(round(x)-2,round(x)+3)):
                    pixel_rows.append(py)
            bottom=max(pixel_rows) if pixel_rows else None
            rows.append({'frame':index,'side':leg['side'],'toeSourcePixels':toe,
                         'opaqueBandBottomRow':bottom,
                         'bottomMinusToePixels':None if bottom is None else bottom-y})
    for j,src in enumerate([base,marked]):
        crop=src.crop((126,250,258,400)).resize((264,300),Image.Resampling.NEAREST)
        canvas.paste(crop.convert('RGB'),((index%4)*528+j*264,(index//4)*334))
    ImageDraw.Draw(canvas).text(((index%4)*528+5,(index//4)*334+303),
        f'Frame {index+1:02} | original / landmarks | cyan=support, amber=lift',fill='white')
canvas.save(OUT/'source-contact-plate.png')
(OUT/'source-contact-observations.json').write_text(json.dumps({'status':'DIAGNOSTIC_NOT_ACCEPTANCE',
 'sourcePoseSHA256':record['sourceFiles']['player-source-s-poses.json'],
 'sourcePixelsPerLogicalUnit':scale,'alphaThreshold':128,'xBandRadiusPixels':2,
 'ySearchRadiusPixels':12,'warning':'Alpha occupancy is not material/sole ownership or world contact tracking.',
 'supportObservations':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
