from pathlib import Path
import json,shutil,math,copy
import numpy as np
base=Path('outputs/SS-player-bounded-proportions');out=Path('outputs/SS-player-settle-prototype');out.mkdir(exist_ok=True)
poses=json.loads((base/'source/samples.json').read_text());neutral=json.loads(Path('outputs/SS-player-bounded-neutral/source/samples.json').read_text())[0]
def solve(h,a):
 axis=a-h;d=np.linalg.norm(axis);assert abs(14.5-12.5)<d<27
 axis/=d;along=(12.5**2-14.5**2+d*d)/(2*d);height=math.sqrt(12.5**2-along**2)
 forward=np.array([0.,1.,0.]);forward-=axis*np.dot(forward,axis);forward/=np.linalg.norm(forward)
 return h+along*axis+height*forward
def foot(side,h,toe,angle,contact):
 r=math.radians(angle);ankle=toe+np.array([0,-7.5*math.cos(r)+3*math.sin(r),7.5*math.sin(r)+3*math.cos(r)])
 heel=toe+np.array([0,-10*math.cos(r),10*math.sin(r)])
 return {'side':side,'phase':0,'contact':contact,'angle':angle,'hip':h.tolist(),'knee':solve(h,ankle).tolist(),'ankle':ankle.tolist(),'heel':heel.tolist(),'toe':toe.tolist(),'contactWorld':toe.tolist() if contact else None}
checks=[]
for index in [4,12]:
 dst=out/f'phase-{index+1:02d}';dst.mkdir(exist_ok=True)
 for folder in ['source','boot']:
  shutil.copytree(base/folder,dst/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('frames','__pycache__'))
 (dst/'boot/frames').mkdir(exist_ok=True)
 shutil.copy2(base/'thigh.py',dst/'thigh.py')
 source=poses[index];support='right' if index==4 else 'left';samples=[]
 for k in range(17):
  if k==0:p=copy.deepcopy(source)
  else:
   p={'time':source['time'],'legs':[]}
   u=min(1,(k-1)/7);u=u*u*(3-2*u)
   v=max(0,(k-8)/8);v=v*v*(3-2*v)
   for q,n in zip(source['legs'],neutral['legs']):
    h=np.array(q['hip'])*(1-u)+np.array(n['hip'])*u
    if q['side']==support:
     toe=np.array(q['toe'])*(1-v)+np.array(n['toe'])*v;toe[2]=3*math.sin(math.pi*v) if k>8 else 0
     angle=q['angle']*(1-v);contact=k<=8 or k==16
    else:
     toe=np.array(q['toe'])*(1-u)+np.array(n['toe'])*u;angle=q['angle']*(1-u);contact=k>=8
    p['legs'].append(foot(q['side'],h,toe,angle,contact))
  p['settleProgress']=k/16;p['settleSeconds']=k/32;samples.append(p)
 for k,p in enumerate(samples):
  for q in p['legs']:
   h,a,n=map(np.array,[q['hip'],q['ankle'],q['knee']]);assert abs(np.linalg.norm(h-n)-12.5)<1e-8;assert abs(np.linalg.norm(a-n)-14.5)<1e-8
   assert min(q['toe'][2],q['heel'][2])>=-1e-8
   assert q['knee'][2]<=q['hip'][2]
 for k in range(1,9):
  q=next(q for q in samples[k]['legs'] if q['side']==support);assert q['toe'][:2]==next(q for q in source['legs'] if q['side']==support)['toe'][:2]
 for path in [dst/'source/samples.json',dst/'boot/samples.json']:path.write_text(json.dumps(samples,indent=2)+'\n')
 s=(base/'assemble.py').read_text();s=s.replace("t=pose['time'];phase=math.tau*t/.5;", "t=pose['time'];phase=math.tau*t/.5;settle_weight=1-pose['settleProgress'];")
 s=s.replace("4*math.sin(phase-math.pi/4)","4*settle_weight*math.sin(phase-math.pi/4)")
 s=s.replace('swing=sign*math.cos(phase)','swing=settle_weight*sign*math.cos(phase)')
 # Existing review sheet is fixed at 16; expand it for the terminal 17th sample.
 s=s.replace('(1536,1792)','(1536,2240)')
 s=s.replace("assert len(set(x['rgbaSHA256'] for x in metrics))==16","assert len(set(x['rgbaSHA256'] for x in metrics))==len(poses)")
 (dst/'assemble.py').write_text(s)
 checks.append({'phase':index+1,'frames':17,'durationSecondsProposed':.5,'liftUnitsProposed':3,'firstToeLandingFrame':1,'supportSide':support,'supportToeFixedFrames':[1,8],'otherFootFixedFrames':[8,16],'geometry':'all segment lengths/reach/ground clearance/knee height checks passed'})
(out/'proposal.json').write_text(json.dumps({'status':'SOURCE_EXPERIMENT_NOT_APPROVED','checks':checks,'limitations':['Preserves toe contact, not full-sole contact while heel is raised','Authored 0.5-second timing and 3-unit lift are proposals','No real-renderer integration','Not a complete idle/transition family']},indent=2)+'\n')
print(checks)
