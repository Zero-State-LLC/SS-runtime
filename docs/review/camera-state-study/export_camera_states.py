from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,shutil,sys
root=Path('/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can');out=root/'outputs/SS-camera-state-study'
src=Path('/Users/appliedalchemylabs/.codex/generated_images/01a137ae-17b7-7103-897c-17913923752e/exec-11dca7e6-b87d-4957-95d0-24fe2a4b074e.png')
if len(sys.argv)>1: src=Path(sys.argv[1])
if len(sys.argv)>2: out=Path(sys.argv[2])
out.mkdir(parents=True,exist_ok=True)
if src.resolve() != (out/'source.png').resolve(): shutil.copy2(src,out/'source.png')
sheet=Image.open(src).convert('RGBA')
frames=[];records=[];scale=312/658
for i,name in enumerate(['intact','damaged','critical','destroyed']):
 cell=sheet.crop((i*512,0,(i+1)*512,768));alpha=cell.getchannel('A').point(lambda a:0 if a<=32 else 255 if a>=240 else round((a-32)*255/208));cell.putalpha(alpha)
 base=alpha.point(lambda a:255 if a>=128 else 0).crop((0,500,350,768)).getbbox();assert base
 anchor=((base[0]+base[2])/2,500+base[3])
 dx=128-scale*anchor[0];dy=352-scale*anchor[1]
 frame=cell.transform((256,384),Image.Transform.AFFINE,(1/scale,0,-dx/scale,0,1/scale,-dy/scale),Image.Resampling.BICUBIC)
 frame.save(out/(name+'.png'));frames.append(frame)
 records.append({'state':name,'sourceCell':[i*512,0,(i+1)*512,768],'sourceBaseAnchor':anchor,'scale':scale,'canvasPixels':[256,384],'logicalCanvas':[64,96],'logicalAnchor':[32,88],'alphaRemap':'<=32 zero, >=240 opaque, linear between','sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()})
plate=Image.new('RGB',(1024,464),'#343a3c');d=ImageDraw.Draw(plate)
for i,(frame,record) in enumerate(zip(frames,records)):
 d.text((i*256+12,8),record['state'],fill='white');plate.paste(frame,(i*256,32),frame)
 d.line((i*256,384,i*256+256,384),fill='#678b91');d.ellipse((i*256+125,381,i*256+131,387),fill='#f2bb6a')
 small=frame.resize((64,96),Image.Resampling.LANCZOS);plate.paste(small,(i*256+180,355),small)
plate.save(out/'registered-states.png')
# Compare alpha silhouettes of the permanent lower pole/base after registration.
base0=frames[0].getchannel('A').crop((0,220,256,384)).point(lambda a:255 if a>=128 else 0)
for frame,record in zip(frames,records):
 mask=frame.getchannel('A').crop((0,220,256,384)).point(lambda a:255 if a>=128 else 0)
 diff=ImageChops.difference(base0,mask)
 record['lowerPoleBaseDifferentMaskPixels']=sum(v>0 for v in diff.get_flattened_data())
(out/'registration.json').write_text(json.dumps({'status':'CANDIDATE_STATES_ONLY','sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'states':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
