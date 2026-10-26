from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
R=Path(__file__).resolve().parent;O=R.parent
neutral=Image.open(O/'SS-player-bounded-neutral/frames/00.png').convert('RGBA')
walk=[Image.open(O/'SS-player-bounded-proportions/frames'/f'{i:02d}.png').convert('RGBA') for i in range(16)]
small=[im.resize((192,208),Image.Resampling.LANCZOS) for im in walk];still=neutral.resize((192,208),Image.Resampling.LANCZOS)
for tick in range(96):
 im=Image.new('RGB',(768,960),'#283036');d=ImageDraw.Draw(im)
 for phase in range(16):
  x=phase%4*192;y=phase//4*240;moving=16<=tick<=48+phase
  frame=(tick-16)%16 if moving else None
  pic=small[frame] if moving else still
  im.paste(pic,(x,y+24),pic)
  d.text((x+8,y+6),f'Stop after {phase+1:02d} | '+('walk' if moving else 'neutral'),fill='white')
 im.save(R/'frames'/f'{tick:03d}.png')
# Full-size neutral and four movement controls.
plate=Image.new('RGB',(1920,448),'#283036');d=ImageDraw.Draw(plate)
for i,(name,im) in enumerate([('Matching neutral',neutral)]+[(f'Movement {j+1:02d}',walk[j]) for j in [0,4,8,12]]):
 plate.paste(im,(i*384,32),im);d.text((i*384+10,10),name,fill='white')
plate.save(R/'source-correspondence.png')
np=json.loads((O/'SS-player-bounded-neutral/source/samples.json').read_text())[0]
wp=json.loads((O/'SS-player-bounded-proportions/source/samples.json').read_text());rows=[]
for phase,p in enumerate(wp):
 delta={}
 for q,n in zip(p['legs'],np['legs']):
  assert q['side']==n['side']
  delta[q['side']]={k:math.dist(q[k],n[k]) for k in ['knee','ankle','heel','toe']}
 rows.append({'stopAfterSourceFrame':phase+1,'releaseDisplayFrame':49+phase,'landmarkChangeSourceUnits':delta})
(R/'review-record.json').write_text(json.dumps({'status':'SOURCE_DIRECT_SWITCH_DIAGNOSTIC_NOT_AUTHORED_TRANSITION','frames':96,'normalFPS':32,'quarterFPS':8,'grid':'16 independent stops, one after each movement pose; shared neutral','neutralSha256':hashlib.sha256((O/'SS-player-bounded-neutral/frames/00.png').read_bytes()).hexdigest(),'limits':['Static source roots; no world travel','Direct switch intentionally exposes missing settling motion','No transition duration or extra animation adopted','No production facing mapping'], 'stops':rows},indent=2)+'\n')
