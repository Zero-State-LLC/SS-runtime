#!/usr/bin/env python3
"""Read-only evidence report for actual alpha and assembled canvas support."""
import json
from pathlib import Path
from PIL import Image
import replay as r
HERE=Path(__file__).resolve().parent

def audit():
    model=json.loads((HERE/'assembly.json').read_text())
    _,layers,crops,inspection=r.render(model)
    origins={
        'components.png':'/Users/appliedalchemylabs/.jcode/generated-images/1794822023576-ig_047e2f0bb16e8096016afacf5567b887d090eea898c287cd7e.png',
        'components-generation.json':'/Users/appliedalchemylabs/.jcode/generated-images/1794822023576-ig_047e2f0bb16e8096016afacf5567b887d090eea898c287cd7e.json',
        'junction-box.png':'/Users/appliedalchemylabs/.jcode/generated-images/1794822224739-ig_047e2f0bb16e8096016afad01fdcb487d08ef0f78bc5f1e9bb.png',
        'junction-box-generation.json':'/Users/appliedalchemylabs/.jcode/generated-images/1794822224739-ig_047e2f0bb16e8096016afad01fdcb487d08ef0f78bc5f1e9bb.json',
        'reference.png':'docs/review/camera-surface-authored-20261116/inputs/reference.png at e90b2361bcd80f4a15dd5c39335b2fc69f7be993',
        'paving.png':'AppTests/WholeSceneAssets/whole-scene-muted-paving.png at e90b2361bcd80f4a15dd5c39335b2fc69f7be993'}
    provenance={name:dict(origin=origin,sha256=r.sha(HERE/'inputs'/name)) for name,origin in origins.items()}
    boundaries={}
    for spec in model['layers']:
        name=spec['name']
        image=layers[name]
        a=image.getchannel('A')
        width,height=a.size
        edge=list(a.crop((0,0,1,height)).tobytes())+list(a.crop((width-1,0,width,height)).tobytes())
        edge+=list(a.crop((0,0,width,1)).tobytes())+list(a.crop((0,height-1,width,height)).tobytes())
        alpha=crops[name].getchannel('A')
        box=alpha.point(lambda v:255 if v>=16 else 0).getbbox()
        s=spec['uniformScale']
        x,y=spec['position']
        bounds=[box[0]*s+x,box[1]*s+y,box[2]*s+x,box[3]*s+y]
        boundaries[name]=dict(sourceVisibleBoundsTransformed=bounds,canvasBorderMaxAlpha=max(edge),
            sourcePaintGeometricBoundsInsideCanvas=0<=bounds[0] and 0<=bounds[1] and bounds[2]<=width and bounds[3]<=height,
            antialiasPaddingSatisfied=max(edge)==0)
    return dict(status=r.STATUS,provenance=provenance,actualSources='Both1254x1254 RGBA; real transparent pixels, mostly252-254 interior alpha; no matte removal.',
        sourceInspection=inspection,assemblyBoundary=boundaries,
        geometryCompletenessScope='All pixels with alpha>=16 in each independent subject region are retained in padded source crops. This is not 3D/backface completeness. Rendered pole touches left canvas edge; antialias fringe margin is not certified.',
        priorPilot='Parent pilot-01, inputs, model and renderer remain unchanged.',
        ownerAccepted=False,productionAdmitted=False)

if __name__=='__main__':
    r.dump(HERE/'source-audit.json',audit())
    print(json.dumps(audit(),indent=2))
