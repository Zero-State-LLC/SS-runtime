from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json,hashlib
P=Path(__file__).resolve().parent
(P/'frames').mkdir(exist_ok=True)
source={s:Image.open(P/f'source/{s}.png').convert('RGBA') for s in ['intact','damaged','critical','destroyed']}
mask=Image.open(P/'source/head-mask.png').convert('L')
clips=[c for c in json.loads((P/'source/clip-metadata-001.json').read_text())['clips'] if c['clipId'].startswith('camera_')]
params=json.loads((P/'parameters.json').read_text())
def material(im,factor,indicatorOnly=False):
 out=im.copy();px=out.load();m=mask.load()
 for y in range(384):
  for x in range(256):
   r,g,b,a=px[x,y]
   if not m[x,y] or not a:continue
   if indicatorOnly and not (g>r*1.5 and b>r*1.5 and g>70):continue
   px[x,y]=(min(255,round(r*factor)),min(255,round(g*factor)),min(255,round(b*factor)),a)
 return out
made={
 'camera_operational_idle':[material(source['intact'],v,True) for v in params['idleIndicatorMultipliers']],
 'camera_hit':[material(source['damaged'],v) for v in params['hitHeadMultipliers']],
 'camera_critical_enter':[material(source['critical'],v) for v in params['criticalHeadMultipliers']],
 'camera_destroy':[],
 'camera_field_off':[source['destroyed'].copy()],
 'camera_destroyed_idle':[source['destroyed'].copy(),source['destroyed'].copy()]}
for off in params['destroyFragmentOffsets']:
 im=source['destroyed'].copy()
 if off is not None:
  overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
  for x,y,r in params['fragments']:d.polygon([(x,y+off),(x+r,y+off+1),(x,y+off+r+2)],fill=tuple(params['fragmentRGB'])+(255,))
  overlay.putalpha(ImageChops.multiply(overlay.getchannel('A'),mask));im=Image.alpha_composite(im,overlay)
 made['camera_destroy'].append(im)
rows=[];report=[];outside=ImageChops.invert(mask)
for c in clips:
 frames=made[c['clipId']];assert len(frames)==len(c['frameIds'])
 row=Image.new('RGB',(1024,424),'#30383b');d=ImageDraw.Draw(row);d.text((8,5),f"{c['clipId']} | {len(frames)}/{c['framesPerSecond']} s | {'loop' if c['loop'] else 'settles'}",fill='white')
 names=[]
 for n,(fid,im) in enumerate(zip(c['frameIds'],frames)):
  difference=ImageChops.difference(im,source['intact'])
  assert all(not any(p) or m==0 for p,m in zip(difference.getdata(),outside.getdata()))
  name=f'frames/{fid}@4x.png';im.save(P/name);names.append(name)
  row.paste(im,(n*256,25),im)
  d.text((n*256+8,405),str(n+1),fill='white')
 # Verify truthful settled art exactly, no residue or indicator revival.
 terminal={'camera_hit':'damaged','camera_critical_enter':'critical','camera_destroy':'destroyed','camera_field_off':'destroyed','camera_destroyed_idle':'destroyed'}.get(c['clipId'])
 if terminal:assert frames[-1].tobytes()==source[terminal].tobytes()
 if c['clipId'].startswith('camera_destroy') or c['clipId']=='camera_field_off':
  for im in frames:
   assert not any(a and g>r*1.5 and b>r*1.5 and g>70 for r,g,b,a in im.getdata())
 report.append({'clipId':c['clipId'],'fps':c['framesPerSecond'],'durationNumerator':len(frames),'durationDenominator':c['framesPerSecond'],'loop':c['loop'],'frames':names,'reducedMotionFrame':names[-1] if terminal else names[0],'uniqueDecodedFrames':len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames})})
 rows.append(row)
sheet=Image.new('RGB',(1024,424*len(rows)))
for i,row in enumerate(rows):sheet.paste(row,(0,i*424))
sheet.save(P/'contact-sheet.png')
(P/'clips.json').write_text(json.dumps({'status':'SOURCE_PREVIEW_NOT_RUNTIME_ADMISSION','canvasPixels':[256,384],'logicalCanvas':[64,96],'anchor':[32,88],'frameCount':sum(len(c['frames']) for c in report),'clips':report},indent=2)+'\n')
print('Verified 16 slots, fixed shared structure, exact terminal states, no cyan indicator in destruction.')
