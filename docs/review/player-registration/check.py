from pathlib import Path
import json,math
R=Path(__file__).resolve().parent
poses=json.loads((R/'samples.json').read_text())
rows=[]
for side in ['right','left']:
 support=[(p['time'],next(q for q in p['legs'] if q['side']==side)) for p in poses]
 support=[(t,q) for t,q in support if q['contact']]
 t0,q0=support[0]
 for t,q in support:
  local_y=.5*(q['toe'][1]-q0['toe'][1])-math.sqrt(.75)*(q['toe'][2]-q0['toe'][2])
  travel=240*(t-t0)
  rows.append({'side':side,'time':t,'nominalWorldTravel':travel,'projectedLocalToeDelta':local_y,'unprojectedRootResidual':travel+local_y,'consistentProjectedRootResidual':.5*travel+local_y})
report={'status':'REGISTRATION_PREDICTION_NOT_DISPLAYED_PLAYBACK','sourceCanvas':[384,416],'sourceRootPixels':[192,336],'sourcePixelsPerModelUnit':6,'proposedDrawSize':[64,416/6],'spriteKitAnchor':[.5,1-336/416],'square64VerticalCompression':(64/416)/(64/384),'sourceProjection':'screen x=6*x; screen down=6*(0.5*y-sqrt(0.75)*z)','comparison':'Full-input nominal travel only; no collision, Q8 quantization, displayed frame holds or action phase included','samples':rows,'maxUnprojectedResidual':max(abs(x['unprojectedRootResidual']) for x in rows),'maxConsistentProjectedResidual':max(abs(x['consistentProjectedRootResidual']) for x in rows)}
(R/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['proposedDrawSize','spriteKitAnchor','square64VerticalCompression','maxUnprojectedResidual','maxConsistentProjectedResidual']},indent=2))
