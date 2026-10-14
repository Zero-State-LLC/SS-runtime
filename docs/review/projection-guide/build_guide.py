"""BP-007 review-only projection experiment. No game resources are modified."""
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

parser=argparse.ArgumentParser()
parser.add_argument('--arena',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
arena=json.loads(args.arena.read_text())
solid=next(s for s in arena['permanentSolids'] if s['id']=='solid-03-transit-kiosk')
cx,cy=solid['center']['x'],solid['center']['y'];hx,hy=solid['halfSize']['x'],solid['halfSize']['y']
corners=[(cx-hx,cy-hy),(cx+hx,cy-hy),(cx+hx,cy+hy),(cx-hx,cy+hy)]
root=math.sqrt(0.5)
matrices={'current-ground':(1,0,0,-1),'elevated-candidate':(root,-root,-root/2,-root/2)}
im=Image.new('RGB',(1408,530),'#171d25');d=ImageDraw.Draw(im)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',16)
small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',12)
records={}
for idx,(name,(a,b,c,e)) in enumerate(matrices.items()):
 ox,oy=idx*704+352,300;det=a*e-b*c
 def project(x,y):
  x-=cx;y-=cy
  return (a*x+b*y,c*x+e*y)
 def screen(x,y):
  u,v=project(x,y);return (ox+u,oy+v)
 def inverse(u,v):return (cx+(e*u-b*v)/det,cy+(-c*u+a*v)/det)
 errors=[]
 for x in range(cx-400,cx+401,25):
  for y in range(cy-400,cy+401,25):
   q=inverse(*project(x,y));errors.append(math.hypot(q[0]-x,q[1]-y))
 assert max(errors)<1e-10
 for n in range(-256,257,32):
  d.line([screen(cx+n,cy-256),screen(cx+n,cy+256)],fill='#34414d')
  d.line([screen(cx-256,cy+n),screen(cx+256,cy+n)],fill='#34414d')
 pts=[screen(*p) for p in corners]
 d.polygon(pts,fill='#283c42',outline='#66e0d5',width=3)
 # A diagrammatic upright guide only; height is not an arena/gameplay value.
 top=[(x,y-110) for x,y in pts]
 for p,q in zip(pts,top):d.line([p,q],fill='#d9c9aa',width=2)
 d.line(top+[top[0]],fill='#d9c9aa',width=2)
 for j,p in enumerate(pts):
  d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),fill='#66e0d5');d.text((p[0]+6,p[1]+5),chr(65+j),font=font,fill='white')
 viewport=[inverse(u,v) for u,v in [(-352,-163),(352,-163),(352,163),(-352,163)]]
 projected=[project(*p) for p in corners]
 bbox=[max(p[k] for p in projected)-min(p[k] for p in projected) for k in [0,1]]
 records[name]={'matrixScreenYDown':[a,b,c,e],'determinant':det,'groundVertices':projected,'groundBoundingSize':bbox,'viewportWorldCorners':viewport,'worldAreaVisibleIgnoringOcclusion':704*326/abs(det),'roundTripMaxError':max(errors),'uprightGuideHeight':110,'heightStatus':'illustrative art guide only, not inferred building height'}
 d.rectangle((idx*704,0,idx*704+704,76),fill='#171d25')
 d.text((idx*704+22,16),name.upper(),font=font,fill='white')
 d.text((idx*704+22,43),f'Same 128 x 128 world obstacle; screen base {bbox[0]:.1f} x {bbox[1]:.1f}',font=small,fill='#c0d0dc')
 d.rectangle((idx*704,450,idx*704+704,530),fill='#171d25')
 d.text((idx*704+22,464),f'Visible world area at 704 x 326: {704*326/abs(det):,.0f} units squared',font=small,fill='white')
 d.text((idx*704+22,488),'Cyan: authoritative ground. Ivory: illustrative upright guide, not production art.',font=small,fill='#c0d0dc')
d.line((704,0,704,530),fill='#677583',width=2)
im.save(args.out/'comparison.png')
record={'status':'PROPOSED_REVIEW_GUIDE_NOT_RUNTIME_RENDER','arenaSHA256':hashlib.sha256(args.arena.read_bytes()).hexdigest(),'solid':solid,'worldCorners':corners,'candidates':records,'source':'Analytic rotation/vertical-compression experiment; no Tiled source copied.'}
(args.out/'projection.json').write_text(json.dumps(record,indent=2)+'\n')
print('Two candidates generated; 2178 world/screen round trips verified. No runtime geometry changed.')
