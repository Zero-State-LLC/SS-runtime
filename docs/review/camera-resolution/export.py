from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,sys
source=Path(sys.argv[1]); output=Path(sys.argv[2]); previous=Path(sys.argv[3]);output.mkdir(parents=True,exist_ok=True)
sheet=Image.open(source).convert('RGBA'); records=[];frames=[]
scale=468/658
for i,name in enumerate(['intact','damaged','critical','destroyed']):
 cell=sheet.crop((i*512,0,(i+1)*512,768))
 alpha=cell.getchannel('A').point(lambda a:0 if a<=32 else 255 if a>=240 else round((a-32)*255/208));cell.putalpha(alpha)
 base=alpha.point(lambda a:255 if a>=128 else 0).crop((0,500,350,768)).getbbox();assert base
 anchor=((base[0]+base[2])/2,500+base[3]);dx=192-scale*anchor[0];dy=528-scale*anchor[1]
 frame=cell.transform((384,576),Image.Transform.AFFINE,(1/scale,0,-dx/scale,0,1/scale,-dy/scale),Image.Resampling.BICUBIC)
 path=output/(name+'.png');frame.save(path);frames.append(frame)
 records.append({'state':name,'sourceCell':[i*512,0,(i+1)*512,768],'sourceAnchor':anchor,'sourceScale':scale,'canvas':[384,576],'logicalCanvas':[64,96],'anchor':[192,528],'logicalAnchor':[32,88],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
plate=Image.new('RGB',(1088,870),'#343a3c');d=ImageDraw.Draw(plate)
for i,(frame,record) in enumerate(zip(frames,records)):
 # Both exports sampled to the same rounded closer-view backing size.
 old=Image.open(previous/(record['state']+'.png')).convert('RGBA')
 for row,im in enumerate([old,frame]):
  sample=im.resize((272,408),Image.Resampling.BILINEAR);plate.paste(sample,(i*272,row*435+25),sample)
  d.text((i*272+8,row*435+8),record['state']+(' / current' if row==0 else ' / source re-export'),fill='white')
plate.save(output/'comparison.png')
(output/'registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'alphaRemap':'<=32 zero; >=240 opaque; linear between','status':'REVIEW_ONLY','states':records},indent=2))
assert all(im.size==(384,576) for im in frames)
assert scale<1 # source is downsampled, never interpolated upward
print('Exported four source-derived 384x576 states; common scale',scale)
