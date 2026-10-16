"""Measure a proposed source-base correspondence; never modifies art or collision."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Sources/SurveillanceCore/Resources/RuntimeAssets/env_solid_07_service_yard_b@1x.png'
ARENA = ROOT / 'Sources/SurveillanceCore/Resources/contracts/civic-seam-arena-004.json'


def projected(x, y):
    r = math.sqrt(0.5)
    return (r * (x - y), r * (x + y) / 2)


def fit(source, target):
    # Front-corner anchored fit: only uniform positive scale is permitted.
    scale = sum(a*b for p,q in zip(source,target) for a,b in zip(p,q)) / sum(a*a for p in source for a in p)
    residuals = [math.dist(tuple(scale*a for a in p), q) for p,q in zip(source,target)]
    return {'uniformScale':scale, 'edgeEndpointErrorsLogical':residuals,
            'rmsEndpointErrorLogical':math.sqrt(sum(e*e for e in residuals)/len(residuals))}


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    arena=json.loads(ARENA.read_text())
    # Locate the authoritative record without substituting image dimensions.
    def records(value):
        if isinstance(value,dict):
            yield value
            for v in value.values(): yield from records(v)
        elif isinstance(value,list):
            for v in value: yield from records(v)
    solid=next(r for r in records(arena) if r.get('id')=='solid-07-service-yard-b')
    hx,hy=solid['halfSize']['x'],solid['halfSize']['y']
    front=projected(-hx,-hy)
    targets=[tuple(a-b for a,b in zip(projected(x,y),front)) for x,y in [(-hx,hy),(hx,-hy)]]
    # Hand-observed provisional slab edges, NOT auto-derived from alpha.
    points={'front':[145,172], 'left':[60,120], 'right':[201,133]}
    sf=points['front']
    vectors=[(points[k][0]-sf[0],sf[1]-points[k][1]) for k in ('left','right')]
    cases=[]
    for label,edges in [('front-SW_left-NW_right-SE',targets)]:
        result=fit(vectors,edges)
        # Robustness envelope: perturb every observed edge vector by up to 4px
        # (two endpoints each with provisional +/-2px coordinate uncertainty).
        alternatives=[]
        import itertools
        for d in itertools.product((-4,4),repeat=4):
            perturbed=[(vectors[i][0]+d[2*i], vectors[i][1]+d[2*i+1]) for i in range(2)]
            alternatives.append(fit(perturbed,edges)['rmsEndpointErrorLogical'])
        result.update(correspondence=label,targetEdgeVectors=edges,
                      cornerPerturbationRMSRange=[min(alternatives),max(alternatives)])
        cases.append(result)
    # Numerical method check uses an exact known scale, separate from art evidence.
    check=fit([(-3,2),(4,2)],[(-9,6),(12,6)])
    assert check['uniformScale']==3 and check['rmsEndpointErrorLogical']==0
    report={'status':'PROVISIONAL_LANDMARK_DIAGNOSTIC_NOT_ADMITTED',
            'assetId':'env_solid_07_service_yard_b','sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'authoritativeSolid':solid,'sourcePixelConvention':'top-left origin, x right, y down',
            'provisionalVisibleSlabLandmarks':points,'landmarkUncertaintyPixels':2,
            'unverified':['rear ground corner hidden','right edge may be source-clipped','source yaw not documented'],
            'fits':cases,'limitations':['Perturbation range samples uncertainty-box corners, not a proven bound',
              'Slab perimeter may differ from wall footprint; no collision fit inferred',
              'Source and renderer contact require visual review; no universal acceptance tolerance'],
            'decision':'Do not treat center-to-base translation as a complete fix; resolve base semantics and source orientation before runtime admission.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(cases,indent=2))


if __name__=='__main__': main()
