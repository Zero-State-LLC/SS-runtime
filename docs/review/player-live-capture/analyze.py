from pathlib import Path
import json,math
R=Path(__file__).resolve().parent
samples=json.loads((R/'records.json').read_text())
poses=json.loads((R/'samples.json').read_text())
groups=[]
for side in ['left','right']:
 group=[];previous=None
 for row in samples:
  if 'sourceFrameIndex' not in row:
   if group:groups.append({'side':side,'samples':group});group=[]
   previous=None
   continue
  frame=row['sourceFrameIndex'];leg=next(x for x in poses[frame]['legs'] if x['side']==side)
  wrapped=previous is not None and frame<previous
  if not leg['contact'] or wrapped:
   if group:groups.append({'side':side,'samples':group});group=[]
  if leg['contact']:
   toe=leg['toe'];localX=toe[0];localY=-.5*toe[1]+math.sqrt(.75)*toe[2]
   group.append({'time':row['displayTime'],'tick':row['tick'],'frame':frame,'toeViewX':row['renderedX']+localX,'toeViewY':row['renderedY']+localY})
  previous=frame
 if group:groups.append({'side':side,'samples':group})
for g in groups:
 a=g['samples'][0]
 for b in g['samples']:b['displacementFromFirstObservedContact']=math.hypot(b['toeViewX']-a['toeViewX'],b['toeViewY']-a['toeViewY'])
 g['maxObservedDisplacement']=max(b['displacementFromFirstObservedContact'] for b in g['samples']) if len(g['samples'])>1 else None
 g['coverage']='observed interval only' if len(g['samples'])>1 else 'insufficient: only one support sample'
report={'scope':'Observed frame identity plus source toe annotation at actual projected actor positions; not pixel tracking, video, complete contact phase coverage or a pass threshold','records':len(samples),'distinctFrames':sorted({r['sourceFrameIndex'] for r in samples if 'sourceFrameIndex' in r}),'ticks':[samples[0]['tick'],samples[-1]['tick']],'supportGroups':groups}
(R/'contact-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['records','distinctFrames','ticks']}));print('observed support displacement:',[g['maxObservedDisplacement'] for g in groups])
