from PIL import Image, ImageDraw
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
src=Image.open(ROOT/'source.png').convert('RGBA')
# User-authorized deterministic alpha cleanup; RGB and costume content stay unchanged.
alpha=src.getchannel('A').point(lambda v:0 if v<=32 else 255 if v>=240 else round((v-32)*255/208))
src.putalpha(alpha)
regions={'south':(0,0,768,512),'east':(768,0,1536,512),'north':(0,512,768,1024),'west':(768,512,1536,1024)}
# Approximate image-space ground roots, manually read from the soles; not contact proof.
roots={'south':(464,477),'east':(1078,491),'north':(462,971),'west':(1079,985)}
scale=312/459
records=[]
for direction,region in regions.items():
 crop=src.crop(region)
 root=(roots[direction][0]-region[0],roots[direction][1]-region[1])
 # Inverse affine sampling keeps the same exact scale and destination ground root.
 canvas=crop.transform((384,384),Image.Transform.AFFINE,(1/scale,0,root[0]-192/scale,0,1/scale,root[1]-336/scale),Image.Resampling.BICUBIC)
 canvas.save(ROOT/(direction+'.png'))
 records.append({'direction':direction,'region':region,'sourceRoot':roots[direction],'scale':scale,'canvas':[384,384],'anchor':[192,336],'alphaBounds':canvas.getchannel('A').getbbox(),'sha256':hashlib.sha256((ROOT/(direction+'.png')).read_bytes()).hexdigest()})
plate=Image.new('RGB',(1536,480),(42,44,47));draw=ImageDraw.Draw(plate)
for i,record in enumerate(records):
 im=Image.open(ROOT/(record['direction']+'.png'))
 plate.paste(im,(384*i,0),im)
 draw.text((384*i+12,8),record['direction']+' — source study',fill=(230,230,230))
 native=im.resize((64,64),Image.Resampling.LANCZOS)
 plate.paste(native,(384*i+160,400),native)
 draw.text((384*i+12,465),'64px logical preview / not admitted',fill=(180,180,180))
plate.save(ROOT/'registered-review.png')
(ROOT/'exports.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((ROOT/'source.png').read_bytes()).hexdigest(),'alphaRule':'<=32 zero; >=240 opaque; linear between; RGB unchanged','scalePolicy':'single scale across all views; no individual body normalization','rootStatus':'manual approximate; not measured contact landmarks','exports':records},indent=2)+'\n')
