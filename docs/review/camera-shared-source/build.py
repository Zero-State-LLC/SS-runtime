from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageChops
ROOT=Path(__file__).resolve().parent
STATES=['intact','damaged','critical','destroyed']
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Authored source boundary around the changing dome; the suspension arm stays shared.
polygon=[(164,155),(172,143),(185,133),(199,137),(218,137),(227,127),(241,139),(255,154),(256,226),(163,226)]
mask=Image.new('L',(256,384));ImageDraw.Draw(mask).polygon(polygon,fill=255)
mask.save(ROOT/'head-mask.png')
intact=Image.open(ROOT/'source/intact.png').convert('RGBA')
shared=intact.copy();shared.putalpha(ImageChops.multiply(shared.getchannel('A'),ImageChops.invert(mask)))
shared.save(ROOT/'shared-mount.png')
report=[];sheet=Image.new('RGB',(1024,480),'#30383b');draw=ImageDraw.Draw(sheet)
for i,s in enumerate(STATES):
 source=Image.open(ROOT/f'source/{s}.png').convert('RGBA')
 head=source.copy();head.putalpha(ImageChops.multiply(head.getchannel('A'),mask));head.save(ROOT/f'{s}-head.png')
 assembled=Image.alpha_composite(shared,head);assembled.save(ROOT/f'{s}.png')
 # Hard partition reconstructs original intact and keeps every exterior RGBA pixel fixed.
 outside=ImageChops.invert(mask)
 diff=ImageChops.difference(assembled,intact)
 changed=sum(any(c for c in p) and m>0 for p,m in zip(diff.getdata(),outside.getdata()))
 assert changed==0
 if s=='intact': assert assembled.tobytes()==intact.tobytes()
 sheet.paste(assembled,(i*256,25),assembled)
 native=assembled.resize((64,96),Image.Resampling.LANCZOS);sheet.paste(native,(i*256+96,380),native)
 draw.text((i*256+12,8),s,fill='white')
 report.append({'state':s,'sourceSha256':digest(ROOT/f'source/{s}.png'),'deliverySha256':digest(ROOT/f'{s}.png'),'outsideHeadChangedRGBApixels':changed,'alphaBounds':assembled.getbbox()})
sheet.save(ROOT/'comparison.png')
(ROOT/'source-record.json').write_text(json.dumps({'status':'REVIEW_SOURCE_NOT_ADMITTED','canvasPixels':[256,384],'logicalCanvas':[64,96],'logicalGroundAnchor':[32,88],'headPolygon':polygon,'polygonStatus':'authored mask, not collision geometry','states':report},indent=2)+'\n')
