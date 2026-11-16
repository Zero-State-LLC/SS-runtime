#!/usr/bin/env python3
"""Small source-trajectory extension of published baseline15be131, never a paint fork."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'player-all-release-source-20261116'
sys.path.insert(0, str(BASE))
import build_source as b
import verify_artifacts as portable

COMMIT = '15be1316d3817604e751664d5167f1649db2fc6b'
NEW = [p for p in range(1,17) if p not in b.PRESERVED]
DEPENDENCIES = ['build_source.py','verify_artifacts.py','export_review.py','audit.py',
                'artifacts/manifest.json','artifacts/input-inventory.json','fixtures/provenance.json']

def load(path):
    return json.loads(path.read_text())

def provenance():
    actual={p:b.sha(BASE/p) for p in DEPENDENCIES}
    b.require(actual==load(HERE/'baseline-lock.json'),'Published baseline lock mismatch')
    return actual

def profile(source, phase, strength=1):
    b.require(math.isfinite(strength) and 0 <= strength <= 1, 'Variation strength outside [0,1]')
    b.require(phase in range(1,17), 'Invalid phase')
    support=b.support_side(source)
    legs=b.legs(source)
    other='left' if support=='right' else 'right'
    stance=math.tanh((legs[other]['toe'][2]-legs[support]['toe'][2])/8)
    angle=math.tau*(phase-1)/16 + (0.25 if support=='left' else -0.25)
    scale=strength*(0.75+0.25*stance)
    skew=0.12*math.sin(angle)*scale
    return {'phase':phase,'support':support,'stance':stance,'strength':strength,
            'transferSkew':skew,'recoverySkew':-0.75*skew,
            'lift':3+0.25*math.cos(angle)*scale}

def ease(t, skew):
    b.require(math.isfinite(t) and 0 <= t <= 1, 'Easing argument outside [0,1]')
    b.require(math.isfinite(skew) and abs(skew)<=0.12, 'Easing skew outside proposal domain')
    return b.smooth(t+skew*t*(1-t))

def generate(source, neutral, phase, strength=1):
    """Adapt baseline generate:103-131 only in its two easing functions and lift coefficient.
    Reuse baseline foot/IK, exact entry, assembly, paint, boot and all validators.
    Preserved phases must be read from original source, never passed here.
    """
    b.require(phase not in b.PRESERVED, 'Preserved phases cannot be regenerated')
    settings=profile(source,phase,strength)
    samples=b.generate(source,neutral)
    if strength==0:
        return samples
    support=settings['support'];neutral_legs=b.legs(neutral)
    q=b.legs(source)[support]
    origin=b.np.array(q['contactWorld'])-b.np.array(q['toe']) if q['contact'] else b.np.zeros(3)
    for k in range(1,17):
        u=ease(min(1,(k-1)/7),settings['transferSkew'])
        v=ease(max(0,(k-8)/8),settings['recoverySkew'])
        samples[k]['legs']=[]
        for q in source['legs']:
            n=neutral_legs[q['side']]
            hip=b.np.array(q['hip'])*(1-u)+b.np.array(n['hip'])*u
            w=v if q['side']==support else u
            toe=b.np.array(q['toe'])*(1-w)+b.np.array(n['toe'])*w
            if q['side']==support:
                toe[2]=settings['lift']*math.sin(math.pi*v) if k>8 else 0
                contact=k<=8 or k==16
            else:
                contact=k>=8
            samples[k]['legs'].append(b.foot(q['side'],hip,toe,q['angle']*(1-w),contact,origin))
    return samples

def expected(root):
    sources=load(root/b.NAMES[0]/'source/samples.json')
    neutral=load(root/b.NAMES[1]/'source/samples.json')[0]
    b.require(len(sources)==16,'Expected16 source phases')
    samples={p:(load(root/b.NAMES[2]/f'phase-{p:02d}/source/samples.json') if p in b.PRESERVED else generate(sources[p-1],neutral,p)) for p in range(1,17)}
    facts=[b.validate(samples[p],sources[p-1],neutral,p) for p in range(1,17)]
    return sources,neutral,samples,facts

def check_state(root, output):
    b.require(load(output/'dependencies.json')==provenance(),'Published baseline dependency changed')
    b.require(load(output/'input-inventory.json')==b.inventory(root),'Original source inventory changed')
    b.require(load(output/'implementation.json')==implementation(),'Variation implementation changed since preparation')

def implementation():
    return {'variation.py':b.sha(Path(__file__)), 'baselineCommit':COMMIT}

def prepare(root, output):
    b.require(not output.exists(),'Use a new output directory')
    b.require(not output.is_relative_to(root) and not root.is_relative_to(output),'Output/source overlap')
    before=b.inventory(root)
    b.require(before==load(BASE/'artifacts/input-inventory.json'),'Original inputs differ from published baseline')
    sources,neutral,samples,facts=expected(root)
    output.mkdir(parents=True)
    b.save(output/'input-inventory.json',before)
    b.save(output/'dependencies.json',provenance())
    b.save(output/'implementation.json',implementation())
    b.save(output/'profiles.json',[profile(sources[p-1],p) for p in NEW])
    b.save(output/'geometry-contact-checks.json',facts)
    b.require(b.inventory(root)==before,'Inputs changed during feasibility')
    print(json.dumps({'status':'FEASIBLE_REMAINS_PROPOSED','phases':14,'geometryRows':544,'inputsUnchanged':len(before)}),flush=True)

def batch(root,output,phases):
    b.require(1<=len(phases)<=2 and len(set(phases))==len(phases) and all(p in NEW for p in phases),'Batches must contain one or two distinct new phases')
    b.require(not (output/'manifest.json').exists(),'Published packet is immutable')
    check_state(root,output)
    _,_,samples,_=expected(root)
    def render(p):
        dst=output/'.work'/f'phase-{p:02d}'
        if dst.exists():
            b.require(b.completed_work(root,dst,samples[p]),f'Incomplete checkpoint phase{p}, preserve for diagnosis rather than overwrite')
            print(f'Validated checkpoint {p}',flush=True)
        else:
            print(f'Rendering phase {p}',flush=True)
            b.render_phase(root,output/'.work',samples[p],p)
        b.require(b.completed_work(root,dst,samples[p]),f'Incomplete phase{p}')
        b.endpoint_checks(dst/'frames',root/b.NAMES[0]/f'frames/{p-1:02d}.png',root/b.NAMES[1]/'frames/00.png',p)
        print(f'Checked phase {p}:17frames,2endpoints',flush=True)
    with ThreadPoolExecutor(max_workers=len(phases)) as pool:
        list(pool.map(render,phases))
    check_state(root,output)

def publish(root,output):
    check_state(root,output)
    b.require(not (output/'manifest.json').exists(),'Manifest already published')
    sources,neutral,samples,facts=expected(root)
    endpoints={}
    rendered={}
    for p in range(1,17):
        if p in b.PRESERVED:
            rendered[p]=root/b.NAMES[2]/f'phase-{p:02d}/frames'
        else:
            dst=output/'.work'/f'phase-{p:02d}'
            b.require(b.completed_work(root,dst,samples[p]),f'Missing validated phase {p}')
            rendered[p]=dst/'frames'
        endpoints[p]=b.endpoint_checks(rendered[p],root/b.NAMES[0]/f'frames/{p-1:02d}.png',root/b.NAMES[1]/'frames/00.png',p)
    records=[]
    for p in range(1,17):
        dst=output/f'phase-{p:02d}';(dst/'frames').mkdir(parents=True)
        if p in b.PRESERVED:
            shutil.copy2(root/b.NAMES[2]/f'phase-{p:02d}/source/samples.json',dst/'samples.json')
        else:
            b.save(dst/'samples.json',samples[p])
        frames=[]
        for k in range(17):
            path=dst/'frames'/f'{k:02d}.png';shutil.copy2(rendered[p]/path.name,path)
            frames.append({'pose':k,'path':str(path.relative_to(output)),'fileSHA256':b.sha(path),'rgbaSHA256':hashlib.sha256(b.rgba(path)).hexdigest()})
        records.append({'phase':p,'status':'PRESERVED' if p in b.PRESERVED else 'PROPOSED','samplesPath':str((dst/'samples.json').relative_to(output)),
                        'samplesSHA256':b.sha(dst/'samples.json'),'endpoints':endpoints[p],'frames':frames})
    check_state(root,output)
    b.save(output/'manifest.json',{'status':'PROPOSED_SOURCE_ONLY_NOT_LIVE_CADENCE','projectionDecision':'167171d89f9dfdad550e1b3b95510fc84514d0b1',
        'baselineCommit':COMMIT,'ownerDirectionUTC':'2026-11-16T02:36:26Z','timing':b.TIMING,'preservedPhases':list(b.PRESERVED),'newPhases':NEW,
        'inputsUnchanged':True,'inputFileCount':1012,'phases':records,'variation':'Deterministic stance/phase easing and support lift, no new body warp',
        'nativeVariationVerified':False})
    print(json.dumps(verify(output),indent=2),flush=True)

def verify(output):
    b.require(load(output/'dependencies.json')==provenance(),'Baseline provenance changed')
    b.require(load(output/'implementation.json')==implementation(),'Implementation provenance changed')
    b.require(load(output/'manifest.json')['baselineCommit']==COMMIT,'Baseline commit changed')
    result=portable.verify(output,BASE/'fixtures')
    sources,neutral,samples,facts=expected(BASE/'fixtures')
    b.require(load(output/'profiles.json')==[profile(sources[p-1],p) for p in NEW],'Profile provenance changed')
    b.require(load(output/'geometry-contact-checks.json')==facts,'Geometry facts changed')
    changed={}
    for p in range(1,17):
        b.require(load(output/f'phase-{p:02d}/samples.json')==samples[p],f'Phase{p} trajectory changed')
        base=load(BASE/'artifacts'/f'phase-{p:02d}/samples.json')
        changed[p]=sum(a['legs']!=c['legs'] for a,c in zip(base,samples[p]))
        b.require(changed[p]==0 if p in b.PRESERVED else changed[p]>0,f'Variation/preservation absent phase{p}')
    result.update({'variationChangedGeometryPoses':changed,'geometryRows':sum(len(f['measurements']) for f in facts),'variationNativeVerified':False})
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','batch','publish','verify'])
    parser.add_argument('--source-root',type=Path)
    parser.add_argument('--output',type=Path,default=HERE/'artifacts')
    parser.add_argument('--phases',type=int,nargs='+')
    args=parser.parse_args();output=args.output.resolve()
    if args.action=='verify':
        print(json.dumps(verify(output),indent=2));return
    b.require(args.source_root is not None,'--source-root is required')
    root=args.source_root.resolve()
    if args.action=='prepare':prepare(root,output)
    elif args.action=='batch':batch(root,output,args.phases or [])
    else:publish(root,output)

if __name__=='__main__':main()
