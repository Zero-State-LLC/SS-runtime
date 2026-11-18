#!/usr/bin/env python3
"""Reuse baseline export/audit, add synchronized source-only comparison pages."""
import argparse
import json
from pathlib import Path
from PIL import Image
import variation as v
import verify_packet
import export_review as baseline_export
import audit as baseline_audit


def comparison_html(speed, profiles):
    fps={'normal':128,'quarter':32}[speed]
    options=''.join(f'<option value="{p}">{p:02d}'+(' preserved' if p in v.b.PRESERVED else ' proposed')+'</option>' for p in range(1,17))
    return (v.HERE/'comparison-template.html').read_text().replace('SPEED',speed).replace('FPS',str(fps)).replace('SCHEDULE',json.dumps(baseline_export.timeline())).replace('PROFILES',json.dumps(profiles)).replace('OPTIONS',options)


def export(output,source_root,ffmpeg,ffprobe):
    verify_packet.verify(output,source_root)
    v.portable.verify(v.BASE/'artifacts',v.BASE/'fixtures')
    v.check_state(source_root,output)
    baseline_export.export(output,ffmpeg)
    baseline_audit.audit(output,source_root,ffprobe)
    profiles=v.load(output/'profiles.json')
    for speed in ('normal','quarter'):
        path=output/f'{speed}-speed.html'
        (output/f'{speed}-allphases.html').write_text(path.read_text())
        path.write_text(comparison_html(speed,profiles))
    overview=Image.new('RGB',(1152,232*16),'#283036')
    for p in range(1,17):
        with Image.open(output/f'phase-{p:02d}/contact-plate.png') as image:
            overview.paste(image.resize((1152,232),Image.Resampling.LANCZOS),(0,(p-1)*232))
    overview.save(output/'contact-overview.png')
    changes=[]
    for p in range(1,17):
        candidate=v.load(output/f'phase-{p:02d}/samples.json')
        base=v.load(v.BASE/'artifacts'/f'phase-{p:02d}/samples.json')
        differences={key:max(v.b.np.linalg.norm(v.b.np.array(v.b.legs(candidate[k])[side][key])-v.b.np.array(v.b.legs(base[k])[side][key])).item() for k in range(17) for side in ('left','right')) for key in ('hip','knee','toe')}
        changes.append({'phase':p,'maxSourceCoordinateDelta':differences,
            'changedRGBAPoses':[k for k in range(17) if v.b.rgba(output/f'phase-{p:02d}/frames/{k:02d}.png')!=v.b.rgba(v.BASE/'artifacts'/f'phase-{p:02d}/frames/{k:02d}.png')]})
    v.b.save(output/'comparison.json',{'status':'PROPOSED_NOT_VISUAL_ACCEPTANCE','baselineCommit':v.COMMIT,'phases':changes,'sourceNativeOrLiveCadenceClaim':False})
    paths=['normal-speed.html','quarter-speed.html','normal-allphases.html','quarter-allphases.html','contact-overview.png','comparison.json']
    v.b.save(output/'comparison-export.json',{'files':{p:v.b.sha(output/p) for p in paths},'preloadedComparisonFrames':544,'selectedPhaseSynchronized':True,'manualReadyBeforeRAF':True})
    print(json.dumps({'status':'EXPORTED_REMAINS_PROPOSED','comparePages':2,'allPhasePages':2,'contactPlates':16,'contactOverview':1,'exactPTS':294}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=v.HERE/'artifacts')
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--ffmpeg',default='/opt/homebrew/bin/ffmpeg')
    parser.add_argument('--ffprobe',default='/opt/homebrew/bin/ffprobe')
    args=parser.parse_args();export(args.output.resolve(),args.source_root.resolve(),args.ffmpeg,args.ffprobe)
