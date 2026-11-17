#!/usr/bin/env python3
"""Native-only integration of the two frozen flat kiosk sources into retained V9.
No simulator launcher, recommendation, texture authoring or acceptance authority.
ADAPT V9 native.py:105-115,130-170 and V6 native.py:204-253 for xcresult imports.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import types
from PIL import Image, ImageChops, ImageDraw

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PACKET=HERE.parent
V9=ROOT/'docs/review/blocked-base-curb-relief-20261116/scene'
HARNESS='AppTests/KioskOnlyGeometrySceneTests.swift'
TEST='KioskOnlyGeometrySceneTests/testQuietSouthNeutralOrdinaryScene()'
FIXTURE_VERSION='source-scene-kiosk-only-010-flat-geometry'
INPUT_SCHEMA='kiosk-only-native-input-010'
RECORD_SCHEMA='source-scene-kiosk-only-records-010'
STATUS='NATIVE_FLAT_KIOSK_COMPARISON_NOT_ACCEPTANCE'
BASELINE_SHA='3227d31730f1b9bea25d42e14ace7e0906439213b1efc690f25826e3c41eaa55'
V9_INPUT_SHA='2c4c3f6a3ef48003291f1ca6421bc6731b4c385a5a17738403c5dcd7972aca88'
SOURCE_MANIFEST_SHA='ea13512b2db1cf0975c7daf386c38ce3aa5a1eb0ffc6c1f5da4a4f6bdbb67b1d'
ORDER=[(arm,z) for arm in ('control','candidate') for z in (1,1.25,1.4)]


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v9=module('kiosk_native_retained_v9',V9/'native.py')
need,load,sha=v9.a.need,v9.load,v9.sha
exact=v9.v8.plan_adapter.exact_tree


def dependency(path):
    path=path.absolute()
    need(path.resolve()==path and path.is_file(),'Missing/symlinked input: '+str(path))
    return dict(path=str(path.relative_to(ROOT)),sha256=sha(path))


def frozen():
    input_path=V9/'native-inputs-v9/native-inputs.json'
    record_path=V9/'native-capture-v9/source-scene-records.json'
    need(sha(input_path)==V9_INPUT_SHA and sha(record_path)==BASELINE_SHA,'Frozen V9 input/record drift')
    need(sha(PACKET/'output/manifest.json')==SOURCE_MANIFEST_SHA,'Frozen source comparison manifest drift')
    source=load(PACKET/'output/manifest.json')
    for path,digest in source['inputs'].items():
        need(dependency(ROOT/path)['sha256']==digest,'Frozen source input drift: '+path)
    for path,digest in source['outputs'].items():
        need(dependency(PACKET/'output'/path)['sha256']==digest,'Frozen source output drift: '+path)
    prepared,record=load(input_path),load(record_path)
    need(sha(V9/'assembly.json')==record['assemblySHA256']==prepared['assemblySHA256'],'Frozen V9 assembly drift')
    need(sha(ROOT/'AppTests/BlockedBaseCurbSceneTests.swift')==prepared['harnessSourceSHA256'],'Frozen V9 harness drift')
    v9.validate_prepared_files(prepared,input_path.parent)
    return prepared,record


def pixel(world,reg):
    x,y=[world[i]-reg['worldPosition'][i] for i in range(2)]
    q=[(x-y)/math.sqrt(2),(x+y)/(2*math.sqrt(2))]
    return [reg['rootPixelsTopLeft'][0]+q[0]*reg['canvasPixels'][0]/reg['drawSizeWorld'][0],reg['rootPixelsTopLeft'][1]-q[1]*reg['canvasPixels'][1]/reg['drawSizeWorld'][1]]


def expected_input():
    base,record=frozen()
    regs=load(PACKET/'output/kiosk-registrations.json')
    arms=[]
    for arm,source_arm in [('control','current'),('candidate','proposed')]:
        reg=regs[source_arm]
        source=dict(role='kiosk',file=arm+'-kiosk.png',sha256=sha(PACKET/f'output/{source_arm}-kiosk.png'),registration=reg,recommendation='review-only-not-accepted')
        buildings=copy.deepcopy(base['buildings'])
        binding=next(b for b in buildings if b['role']=='kiosk')
        binding['groundPixelsTopLeft']=[pixel(p,reg) for p in [[512,640],[640,640],[640,768],[512,768]]]
        plan=copy.deepcopy(base['scenePlan'])
        kiosk=next(b for b in plan['buildings'] if b['id']=='solid-03-transit-kiosk')
        for landmark in kiosk['contactLandmarks']:
            landmark['sourcePixelsTopLeft']=pixel(landmark['world'],reg)
        arms.append(dict(arm=arm,source=source,buildings=buildings,scenePlan=plan,geometrySHA256=sha(PACKET/f'output/{source_arm}-geometry.json')))
    paths=[ROOT/HARNESS,HERE/'native.py',V9/'native.py',V9/'assembly.json',V9/'native-inputs-v9/native-inputs.json',V9/'native-capture-v9/source-scene-records.json',PACKET/'output/manifest.json',PACKET/'output/kiosk-registrations.json',PACKET/'z-map.json']
    paths += [PACKET/f'output/{arm}-{suffix}' for arm in ('current','proposed') for suffix in ('kiosk.png','geometry.json')]
    return dict(schema=INPUT_SCHEMA,fixtureVersion=FIXTURE_VERSION,harnessSourceSHA256=sha(ROOT/HARNESS),v9InputSHA256=V9_INPUT_SHA,baselineRecordSHA256=BASELINE_SHA,sourceManifestSHA256=SOURCE_MANIFEST_SHA,dependencies=[dependency(p) for p in paths],arms=arms,nativeEvidence=False,ownerAcceptance=False)


def validate_prepared(prepared,directory):
    need(prepared==expected_input(),'Exact native preparation drift')
    need(directory.resolve()==directory.absolute(),'Prepared directory alias')
    manifest=directory/'native-inputs.json'
    dependency(manifest)
    need(load(manifest)==prepared,'On-disk preparation drift')
    for arm in prepared['arms']:
        s=arm['source']
        need(Path(s['file']).name==s['file'],'Prepared path escape')
        need(dependency(directory/s['file'])['sha256']==s['sha256'],'Prepared kiosk bytes drift')
        with Image.open(directory/s['file']) as im:
            need(im.mode=='RGBA' and list(im.size)==s['registration']['canvasPixels'],'Kiosk canvas/mode drift')


def prepare(output=HERE/'prepared'):
    need(not output.exists(),'Preserve existing native preparation')
    prepared=expected_input()
    output.mkdir(parents=True)
    for arm,source in [('control','current'),('candidate','proposed')]:
        shutil.copyfile(PACKET/f'output/{source}-kiosk.png',output/f'{arm}-kiosk.png')
    (output/'native-inputs.json').write_text(json.dumps(prepared,indent=2)+'\n')
    validate_prepared(prepared,output)
    return dict(status='PREPARED_NOT_EXECUTED',inputSHA256=sha(output/'native-inputs.json'),harnessSourceSHA256=prepared['harnessSourceSHA256'],sources=2,retainedV9InputSHA256=V9_INPUT_SHA)


def arm_prepared(prepared,arm):
    base,_=frozen()
    selected=next(x for x in prepared['arms'] if x['arm']==arm)
    base['sources']=[selected['source'] if s['role']=='kiosk' else s for s in base['sources']]
    base['buildings']=selected['buildings']
    base['scenePlan']=selected['scenePlan']
    return base,selected


def validate_result(summary,tree):
    return types.FunctionType(v9.v5.validate_result.__code__,dict(v9.v5.validate_result.__globals__,TEST=TEST))(summary,tree)


def validate_attachment_manifest(manifest):
    return types.FunctionType(v9.v7.validate_attachment_manifest.__code__,dict(v9.v7.validate_attachment_manifest.__globals__,TEST=TEST))(manifest)


def attachments(exports):
    validate_attachment_manifest(load(exports/'manifest.json'))
    return v9.v6.attachments(exports)


def validate_records(record,prepared,input_sha):
    base,old=frozen()
    need(prepared==expected_input(),'Prepared binding forged')
    need(record.get('schema')==RECORD_SCHEMA and record.get('fixtureVersion')==FIXTURE_VERSION and record.get('status')==STATUS,'Wrong native kiosk schema/fixture/status')
    need('syntheticFixture' not in record,'Synthetic fixture is not native evidence')
    need(set(record)==set(old)|{'v9InputSHA256','sourceManifestSHA256'},'Exact native envelope fields required')
    fixed={'baselineRecordSHA256':BASELINE_SHA,'sourceManifestSHA256':SOURCE_MANIFEST_SHA,'v9InputSHA256':V9_INPUT_SHA,'harnessSourceReadSHA256':prepared['harnessSourceSHA256'],'inputSHA256':input_sha}
    for key,value in fixed.items():need(record.get(key)==value,'Stale native metadata: '+key)
    for key in ('fixture','cameraSourceFrames','playerSourceFrames','assemblySHA256','planSHA256','supplementalManifestSHA256','controlSHA256','runtimeSHA256','sourceSHA256'):
        need(record.get(key)==old[key],'Frozen V9 metadata drift: '+key)
    executable=record.get('loadedTestExecutable',{})
    path,digest=executable.get('path'),executable.get('sha256')
    need(isinstance(path,str) and Path(path).is_absolute() and Path(path).name=='SSRuntimeTests' and Path(path).parent.name=='SSRuntimeTests.xctest','Actual loaded test executable required')
    need(isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest) and digest!=old['loadedTestExecutable']['sha256'],'Fresh loaded binary required')
    rows=record.get('captures',[])
    need([(r.get('arm'),r.get('zoom')) for r in rows]==ORDER,'Exactly six ordered captures required')
    mutable={'arm','name','comparisonRole','pngSHA256','buildingSourceSHA256','preprojectionInventory','actors','groundFootprints','visibleBuildingContacts'}
    for row in rows:
        previous=next(r for r in old['captures'] if r['arm']=='candidate' and r['zoom']==row['zoom'])
        need(set(row)==set(previous)|{'kioskSourceSHA256','kioskGeometrySHA256'},'Exact capture fields required')
        for key in previous.keys()-mutable:
            need(row[key]==previous[key],'Frozen V9 capture drift: '+key)
        effective,selected=arm_prepared(prepared,row['arm'])
        source=selected['source']
        reg=source['registration']
        need(row['kioskSourceSHA256']==source['sha256'] and row['kioskGeometrySHA256']==selected['geometrySHA256'],'Wrong arm source/geometry')
        need(row['name']==f"source-scene-{row['arm']}-ordinary-z{round(row['zoom']*100)}",'Wrong capture name')
        need(row['comparisonRole']==('CURRENT_FLAT_KIOSK_NATIVE_V9_CONTEXT' if row['arm']=='control' else 'PROPOSED_FLAT_KIOSK_NATIVE_V9_CONTEXT'),'Wrong arm meaning')
        hashes=dict(previous['buildingSourceSHA256'],**{'benchmark-building':source['sha256']})
        need(row['buildingSourceSHA256']==hashes,'Neighbor texture drift')
        for cohort in ('actors','preprojectionInventory'):
            need(len(row[cohort])==len(previous[cohort]),'Actor census drift')
            for actor,original in zip(row[cohort],previous[cohort]):
                if original['name']!='benchmark-building':
                    need(actor==original,'Non-kiosk actor drift: '+original['name'])
                else:
                    need(set(actor)==set(original),'Kiosk actor schema drift')
                    for key in original.keys()-{'size','anchor'}:need(actor[key]==original[key],'Kiosk authority/transform drift: '+key)
                    exact(actor['size'],reg['drawSizeWorld'],'kiosk native size')
                    exact(actor['anchor'],[reg['rootPixelsTopLeft'][0]/reg['canvasPixels'][0],1-reg['rootPixelsTopLeft'][1]/reg['canvasPixels'][1]],'kiosk anchor')
        semantic=dict(row,arm='candidate')
        expected_footprints=v9.v7.footprint_expected(semantic,effective)
        exact(row['groundFootprints'],expected_footprints,'native ground footprint correspondence')
        v9.v8.validate_contacts(semantic,effective)
        v9.validate_joint_depth(row,base['supplements'])
        v9.v6.validate_framing(row)
        need(set(row['pngSHA256'])=={'-native','-half','-grayscale'} and all(isinstance(d,str) and re.fullmatch('[0-9a-f]{64}',d) for d in row['pngSHA256'].values()),'Exactly18bound images required')
    return rows


def verify_images(found,rows):
    for row in rows:
        for suffix,digest in row['pngSHA256'].items():
            path=found[row['name']+suffix]
            need(sha(path)==digest,'Captured attachment hash drift')
            with Image.open(path) as im:
                expected=tuple(v//2 for v in row['nativePixels']) if suffix=='-half' else tuple(row['nativePixels'])
                need(im.format=='PNG' and im.size==expected,'Native image dimensions drift')
                im.verify()
    # Same-zoom full native pixels outside the union of the two kiosk canvases must match.
    # Conservative canvas mask tolerates native texture filtering, not actor/ground mutation.
    for zoom in (1,1.25,1.4):
        pair=[next(r for r in rows if r['arm']==arm and r['zoom']==zoom) for arm in ('control','candidate')]
        images=[Image.open(found[r['name']+'-native']).convert('RGB') for r in pair]
        diff=ImageChops.difference(*images)
        need(diff.getbbox() is not None,'Native kiosk arms must actually differ')
        mask=Image.new('L',images[0].size)
        scale=images[0].width/704
        for row in pair:
            actor=next(p for p in row['actors'] if p['name']=='benchmark-building')
            center=row['centerWorld']
            root=actor['projectedRoot']
            left=(root[0]-(center[0]-352)-actor['anchor'][0]*actor['size'][0]*zoom)*scale
            top=((center[1]+163)-root[1]-(1-actor['anchor'][1])*actor['size'][1]*zoom)*scale
            right=left+actor['size'][0]*zoom*scale
            bottom=top+actor['size'][1]*zoom*scale
            ImageDraw.Draw(mask).rectangle((math.floor(left)-2,math.floor(top)-2,math.ceil(right)+2,math.ceil(bottom)+2),fill=255)
        outside=Image.composite(Image.new('RGB',diff.size),diff,mask)
        need(outside.getbbox() is None,'Non-kiosk native pixels changed')


def import_result(result,output,expected_executable):
    need(not output.exists(),'Preserve prior native result evidence')
    prepared=expected_input()
    validate_prepared(prepared,HERE/'prepared')
    inputs=HERE/'prepared/native-inputs.json'
    def query(kind):
        return json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results',kind,'--path',str(result)],text=True))
    summary,tree=query('summary'),query('tests')
    validate_result(summary,tree)
    with tempfile.TemporaryDirectory(prefix='kiosk-native-import-',dir=HERE) as temp:
        exports=Path(temp)/'exports'
        subprocess.run(['xcrun','xcresulttool','export','attachments','--path',str(result),'--output-path',str(exports)],check=True)
        found=attachments(exports)
        record=load(found['source-scene-records'])
        rows=validate_records(record,prepared,sha(inputs))
        executable=v9.validate_executable(record,expected_executable)
        verify_images(found,rows)
        output.mkdir(parents=True)
        for name,path in found.items():shutil.copyfile(path,output/(name+('.json' if name.endswith('records') else '.png')))
        shutil.copyfile(exports/'manifest.json',output/'attachment-manifest.json')
    for name,value in [('summary',summary),('tests',tree)]:
        (output/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
    report=dict(status=STATUS,fixtureVersion=FIXTURE_VERSION,nativeTests=1,captures=6,images=18,xcresult=str(result.resolve()),inputSHA256=sha(inputs),testExecutable=executable,ownerAcceptance=False,physicalDeviceEvidence=False,files={p.name:sha(p) for p in sorted(output.iterdir())})
    (output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','check','import'])
    parser.add_argument('--output',type=Path)
    parser.add_argument('--xcresult',type=Path)
    parser.add_argument('--test-executable',type=Path)
    args=parser.parse_args()
    if args.action=='prepare':answer=prepare(args.output or HERE/'prepared')
    elif args.action=='check':
        prepared=expected_input()
        validate_prepared(prepared,HERE/'prepared')
        answer=dict(status='PREPARATION_VALID_NOT_NATIVE_EVIDENCE',inputSHA256=sha(HERE/'prepared/native-inputs.json'))
    else:
        need(args.output is not None and args.xcresult is not None and args.test_executable is not None,'Actual xcresult, new output and fresh executable required')
        answer=import_result(args.xcresult,args.output,args.test_executable)
    print(json.dumps(answer,indent=2))
