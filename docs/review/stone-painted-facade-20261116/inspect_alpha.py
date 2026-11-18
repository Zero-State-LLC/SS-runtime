"""Read-only exact alpha evidence. No cleanup, thresholding or geometry inference."""
import json
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
result={}
for name in ('inputs/roof-vent.png','output/roof-vent-material.png','output/roof-layer-alpha.png','output/preview-alpha.png'):
    with Image.open(P/name) as image:
        alpha=image.getchannel('A')
        bad=[]
        for y in range(image.height):
            for x in range(image.width):
                r,g,b,a=image.getpixel((x,y))
                if a>0 and r>180 and b>180 and g<100:
                    bad.append(dict(x=x,y=y,rgba=[r,g,b,a]))
        result[name]=dict(mode=image.mode,size=list(image.size),alphaHistogram={str(i):n for i,n in enumerate(alpha.histogram()) if n},magentaPixels=bad)
with Image.open(P/'inputs/roof-vent.png') as raw, Image.open(P/'output/roof-vent-material.png') as material:
    result['exactMaterialDiff']=[dict(x=i%raw.width,y=i//raw.width,before=list(a),after=list(b))
        for i,(a,b) in enumerate(zip(raw.getdata(),material.getdata())) if a!=b]
print(json.dumps(result,indent=2))
