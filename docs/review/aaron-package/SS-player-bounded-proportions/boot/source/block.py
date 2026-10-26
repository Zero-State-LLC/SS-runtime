"""BP-002 source-space pose experiment. Not production art or runtime motion."""
from pathlib import Path
import json, math
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
C=P['cycleSeconds']; S=P['supportSeconds']; V=P['nominalTravelUnitsPerSecond']
L1,L2=P['segmentLengths']; E=math.radians(P['cameraElevationDegrees'])
def smooth(x): return x*x*(3-2*x)
def foot_rotation(y,z,a):
    a=math.radians(a)
    return y*math.cos(a)+z*math.sin(a), -y*math.sin(a)+z*math.cos(a)
def leg(t,side):
    offset=0 if side=='right' else C/2
    phase=(t-offset)%C
    sign=-1 if side=='right' else 1
    x=sign*P['halfAnkleWidth']
    half=t%(C/2)
    hipz=P['hipHeight']-P['supportCompression']*math.sin(math.pi*half/S)**2 if half<=S else P['hipHeight']+P['flightRise']*math.sin(math.pi*(half-S)/(C/2-S))**2
    angle=P['pushOffDegrees']*smooth(min(phase/S,1))
    if phase<=S:
        toe=(x,P['toeLandingForward']-V*phase,0)
        dy,dz=foot_rotation(-P['ankleBehindToe'],P['ankleAboveSole'],angle)
        ankle=(x,toe[1]+dy,dz)
        contact=True
    else:
        u=(phase-S)/(C-S)
        enddy,endz=foot_rotation(-P['ankleBehindToe'],P['ankleAboveSole'],P['pushOffDegrees'])
        starty=P['toeLandingForward']-V*S+enddy
        endy=P['toeLandingForward']-P['ankleBehindToe']
        ankle=(x,starty+(endy-starty)*smooth(u)-V*(C-S)*(u*(1-u)**P['velocityBlendPower']-(1-u)*u**P['velocityBlendPower']),endz+(P['ankleAboveSole']-endz)*smooth(u)+P['recoveryLift']*math.sin(math.pi*u)**2)
        angle=P['pushOffDegrees']*(1-smooth(u))
        dy,dz=foot_rotation(-P['ankleBehindToe'],P['ankleAboveSole'],angle)
        toe=(x,ankle[1]-dy,ankle[2]-dz)
        contact=False
    hy,hz=foot_rotation(-P['footLength'],0,angle)
    heel=(x,toe[1]+hy,toe[2]+hz)
    hip=(sign*P['halfHipWidth'],0,hipz)
    delta=[ankle[i]-hip[i] for i in range(3)]
    d=math.sqrt(sum(v*v for v in delta))
    if not abs(L1-L2)<d<L1+L2: raise ValueError(f'unreachable {t} {side}: {d}')
    along=(L1*L1-L2*L2+d*d)/(2*d)
    bend=math.sqrt(max(0,L1*L1-along*along))
    # Forward pole projected perpendicular to hip-ankle axis.
    axis=[v/d for v in delta]
    pole=[(1 if i==1 else 0)-axis[i]*axis[1] for i in range(3)]
    norm=math.sqrt(sum(v*v for v in pole))
    if norm<1e-10: raise ValueError('Forward pole is singular')
    knee=tuple(hip[i]+along*axis[i]+bend*pole[i]/norm for i in range(3))
    return {'side':side,'phase':phase,'contact':contact,'angle':angle,'hip':hip,'knee':knee,'ankle':ankle,'heel':heel,'toe':toe,'contactWorld':(x,V*t+toe[1],toe[2]) if contact else None}
def pose(t): return {'time':t,'nominalActorTravel':V*t,'legs':[leg(t,s) for s in ['right','left']]}
def project(p,origin=(160,290),scale=6,side=False):
    x,y,z=p
    return (origin[0]+scale*(y if side else x),origin[1]+scale*(-z if side else y*math.sin(E)-z*math.cos(E)))
def panel(t,side=False):
    im=Image.new('RGB',(320,360),'#20272b'); d=ImageDraw.Draw(im)
    for n in range(-30,31,10):
        if not side:
            d.line([project((-20,n,0)),project((20,n,0))],fill='#364148')
            d.line([project((n,-30,0)),project((n,30,0))],fill='#364148')
    if side: d.line([(5,290),(315,290)],fill='#66757c')
    d.text((12,12),f'{t:.3f}s | '+('SIDE DIAGNOSTIC' if side else 'ELEVATED FRONT'),fill='white')
    q=pose(t)
    for l in sorted(q['legs'],key=lambda l:l['ankle'][1]):
        color='#e9af69' if l['side']=='right' else '#79bfcd'
        pts=[project(l[k],side=side) for k in ['hip','knee','ankle']]
        d.line(pts,fill=color,width=9)
        for px,py in pts: d.ellipse((px-4,py-4,px+4,py+4),fill='white')
        # Sole plane uses actual authored heel and toe, not a rotated screen oval.
        h=l['heel']; a=l['toe']; w=P['footWidth']/2
        corners=[(h[0]-w,h[1],h[2]),(h[0]+w,h[1],h[2]),(a[0]+w,a[1],a[2]),(a[0]-w,a[1],a[2])]
        d.polygon([project(c,side=side) for c in corners],fill=color,outline='white')
        d.line([project(l['ankle'],side=side),project(l['toe'],side=side)],fill=color,width=3)
        px,py=project(l['toe'],side=side)
        if l['contact']: d.ellipse((px-6,py-6,px+6,py+6),outline='#a9f79a',width=2)
    support='/'.join(l['side'] for l in q['legs'] if l['contact']) or 'FLIGHT'
    d.text((12,325),'Support: '+support,fill='#bde7b0')
    return im
if __name__=='__main__':
    samples=[pose(i*C/16) for i in range(16)]
    (ROOT/'sixteen-samples.json').write_text(json.dumps(samples,indent=2)+'\n')
    dense=[pose(i*C/1000) for i in range(1001)]
    errors=[]; clearance=[]; drift=[]
    for q in dense:
        for l in q['legs']:
            errors.extend([abs(math.dist(l['hip'],l['knee'])-L1),abs(math.dist(l['knee'],l['ankle'])-L2)])
            clearance.extend([l['toe'][2],l['heel'][2]])
            if l['contact']:
                step_start=q['time']-l['phase']
                expected=V*step_start+P['toeLandingForward']
                drift.append(abs(l['contactWorld'][1]-expected))
    seam=max(math.dist(leg(0,s)[k],leg(C,s)[k]) for s in ['right','left'] for k in ['hip','knee','ankle','heel','toe'])
    metrics={'status':'SOURCE_GEOMETRY_ONLY_NOT_RUNTIME_EVIDENCE','sampleCount':len(dense),'maxSegmentError':max(errors),'minimumSoleLandmarkHeight':min(clearance),'maxNominalSupportToeDrift':max(drift),'lastToFirstLocalPositionError':seam,'worldDisplacementPerCycle':V*C,'runtimePositionsUsed':False,'anatomyValidated':False,'paintedSourceIntegrated':False}
    (ROOT/'measurements.json').write_text(json.dumps(metrics,indent=2)+'\n')
    assert max(errors)<1e-9 and min(clearance)>-1e-9 and max(drift)<1e-9 and seam<1e-9
    keys=[0,.05,.1,.175,.25,.30,.35,.425]
    sheet=Image.new('RGB',(1280,1440),'#20272b')
    for i,t in enumerate(keys):
        sheet.paste(panel(t),(i%4*320,(i//4)*720))
        sheet.paste(panel(t,True),(i%4*320,(i//4)*720+360))
    sheet.save(ROOT/'key-poses.png')
    # GIF is slow diagnostic; exact .5-second timing stays in JSON, not GIF centiseconds.
    frames=[panel(i*C/16) for i in range(16)]
    frames[0].save(ROOT/'slow-block.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
    eps=1e-7
    jumps=[]
    for t in [0,S,C/2,C/2+S,C]:
        for side in ['right','left']:
            for point in ['hip','knee','ankle','heel','toe']:
                a=leg(t-eps,side)[point]; b=leg(t,side)[point]; c=leg(t+eps,side)[point]
                before=[(b[i]-a[i])/eps for i in range(3)]
                after=[(c[i]-b[i])/eps for i in range(3)]
                jumps.append({'time':t,'side':side,'point':point,'velocityDifference':math.dist(before,after)})
    (ROOT/'transition-diagnostics.json').write_text(json.dumps({'epsilonSeconds':eps,'boundaries':jumps},indent=2)+'\n')
    held_drift=[]
    for q in dense:
        held_time=math.floor((q['time']%C)/C*16)*C/16
        for l in q['legs']:
            held=leg(held_time,l['side'])
            if l['contact'] and held['contact']:
                held_drift.append(abs(held['toe'][1]-l['toe'][1]))
    metrics['maxSampledHeldFrameNominalToeDrift']=max(held_drift)
    metrics['heldFrameDurationSeconds']=C/16
    metrics['maxFiniteDifferenceVelocityMismatch']=max(v['velocityDifference'] for v in jumps)
    (ROOT/'measurements.json').write_text(json.dumps(metrics,indent=2)+'\n')
    if (ROOT/'retained-neutral.png').exists():
        comparison=Image.new('RGB',(1024,430),'#20272b'); draw=ImageDraw.Draw(comparison)
        neutral=Image.open(ROOT/'retained-neutral.png').convert('RGBA')
        comparison.paste(neutral,(0,35),neutral)
        draw.text((15,12),'RETAINED PAINTED NEUTRAL (384px canvas)',fill='white')
        comparison.paste(panel(0),(384,35)); comparison.paste(panel(S),(704,35))
        draw.text((15,410),'Geometry study only. Scale/camera are proposed. No painted pose integration.',fill='white')
        comparison.save(ROOT/'source-comparison.png')
    print(json.dumps(metrics,indent=2))
