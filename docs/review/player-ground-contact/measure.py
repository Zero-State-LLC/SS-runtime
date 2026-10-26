"""Offline pixel registration of the recorded held neutral; not motion acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
root=Path(__file__).resolve().parents[5]
source=root/'outputs/SS-player-bounded-neutral/frames/00.png'
capture=root/'outputs/SS-bounded-idle-renderer-review/final-frame.png'
src=Image.open(source).convert('RGBA').resize((240,260),Image.Resampling.BILINEAR)
a=np.asarray(src); actual=np.asarray(Image.open(capture).convert('RGB'))
y,x=np.where(a[:,:,3]>250); rgb=a[y,x,:3].astype(float)
# Match a broad interval around terminal telemetry; no claim of frame synchronization.
best=None
for top in range(285,355):
 for left in range(825,890):
  score=np.mean(np.abs(actual[y+top,x+left,:].astype(float)-rgb))
  if best is None or score<best[0]:best=(float(score),left,top)
score,left,top=best
out=Image.open(capture).convert('RGB'); draw=ImageDraw.Draw(out)
rootxy=(left+120,top+210)
draw.line((rootxy[0]-30,rootxy[1],rootxy[0]+30,rootxy[1]),fill='cyan',width=2)
soles=[]
for sx in (168,216):
 for sy in (328.5,358.5):
  px=left+sx*.625;py=top+sy*.625;soles.append([px,py]);draw.ellipse((px-3,py-3,px+3,py+3),outline='yellow',width=2)
out.crop((left-40,top+140,left+280,top+300)).resize((960,480)).save(Path(__file__).parent/'contact-overlay.png')
result={'method':'opaque RGB template mean absolute error; resized source; broad translation search','meanAbsoluteRGBError':score,'estimatedSourceTopLeft':[left,top],'estimatedRoot':rootxy,'modelGroundHeelToe':soles,'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'captureSHA256':hashlib.sha256(capture.read_bytes()).hexdigest(),'limits':['Estimated pixel match, not timestamp-linked telemetry','Model landmarks are not sole segmentation','Static neutral only; cannot prove moving support contact']}
record=json.loads((root/'work/SS-runtime/docs/review/player-bounded-idle-recording/484281BA-C222-43BC-B2EB-95AC2E6F3A7D.json').read_text())[-1]
expected=[record['playerScreenX']*3,978-record['playerScreenY']*3]
result['terminalTelemetryRootPixels']=expected
result['estimatedRootDeltaPixels']=[rootxy[i]-expected[i] for i in range(2)]
original=Image.open(source).convert('RGBA')
result['sourceSoleOpaqueRows']={str(sx):max(yy for yy in range(300,416) if any(original.getpixel((xx,yy))[3]>127 for xx in range(sx-8,sx+9))) for sx in [168,216]}
(Path(__file__).parent/'measurement.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
