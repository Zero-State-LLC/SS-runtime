"""Project measured source alpha-edge proxy through existing archived root traces."""
from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent
source_path=here/'source-contact-observations.json'
source=json.loads(source_path.read_text())
prior_path=here.parent/'player-contact-audit/current-contact-audit.json'
prior=json.loads(prior_path.read_text())
assert source['sourcePoseSHA256']==prior['sourcePoseSHA256']
offsets={(r['frame'],r['side']):r['bottomMinusToePixels']/source['sourcePixelsPerLogicalUnit'] for r in source['supportObservations']}
results=[]
for trace in prior['results']:
    segments=[]
    for segment in trace['segments']:
        values=[o['modelToeY']-offsets[(o['pose'],segment['side'])] for o in segment['observations']]
        segments.append({'side':segment['side'],'startTick':segment['startTick'],'endTick':segment['endTick'],
                         'sourceAlphaEdgeRangeLogical':max(values)-min(values),
                         'modelToeRangeLogical':segment['rangeLogical']})
    results.append({k:trace[k] for k in ['trace','sha256','axis','reducedMotion','distancePhaseComparison']}|
        {'segments':segments,'maximumSourceAlphaEdgeRangeLogical':max(s['sourceAlphaEdgeRangeLogical'] for s in segments),
         'maximumModelToeRangeLogical':max(s['modelToeRangeLogical'] for s in segments)})
out={'status':'SOURCE_ALPHA_PROXY_NOT_NATIVE_SOLE_TRACKING',
     'inputsSHA256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [source_path,prior_path]},
     'method':'Existing rendered root plus source alpha bottom-row displacement; no video sampling or physical sole identification.',
     'results':results}
(here/'trace-contact-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
for r in results:
 print(r['axis'],r['reducedMotion'],r['distancePhaseComparison'],round(r['maximumModelToeRangeLogical'],4),round(r['maximumSourceAlphaEdgeRangeLogical'],4))
