#!/usr/bin/env python3
"""Verify actual existing-art traversal attachments. No gameplay simulator or visual acceptance.
Live xcresult identity is mandatory for CLI import. Offline checks can reuse retained summary/tree.
The source manifest attests asset bytes and current files, not every executed build input.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNTIME = ROOT / 'Sources/SurveillanceCore/Resources/RuntimeAssets'
TEST = 'ExistingArtTraversalTests/testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion()'
COORDINATED_TESTS = frozenset((TEST, 'ExistingArtEncounterTests/testLegalPilotExistingArtEncounterEvidence()',
                              'ExistingArtViewportTests/testExistingArtViewportEvidence()'))
LEGS = [('quarter-west',20),('half-west',40),('approach-west',55),('reverse-east',75),
        ('collision-west',105),('slide-northwest',155),('rear-west',190),
        ('rear-south-collision',220),('return-east',265),('front-south',325),('front-west',355),('release',380)]
MAPPINGS = ('shipping', 'midpoint-post-action-still')
UNSUPPORTED = ['coherent repaired scene','source fidelity acceptance','all sixteen poses or all facings',
               'exhaustive front/rear/corner visible-pixel occlusion','dodge','physical device',
               'display scanout or performance acceptance','SwiftUI pause overlay']

def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def phase(tick): return next(name for name,end in LEGS if tick <= end)

def validate_result(summary, tree, allowed_tests=(TEST,)):
    allowed_tests=frozenset(allowed_tests)
    need(allowed_tests in (frozenset((TEST,)),COORDINATED_TESTS),'Unauthorized test-set scope')
    count=len(allowed_tests)
    need(summary.get('result') == 'Passed' and summary.get('totalTestCount') == count and
         summary.get('passedTests') == count and summary.get('failedTests') == 0 and
         summary.get('skippedTests') == 0 and summary.get('expectedFailures') == 0,
         'Expected exact authorized passing tests, no zero/failed/skipped/expected-failure runs')
    cases=[]
    def walk(node):
        if node.get('nodeType') == 'Test Case': cases.append(node)
        for child in node.get('children',[]): walk(child)
    for node in tree.get('testNodes',[]): walk(node)
    need(len(cases)==count and {c.get('nodeIdentifier') for c in cases}==allowed_tests and
         all(c.get('result')=='Passed' for c in cases), 'Exact focused test identity/result mismatch')

def attachments(exports):
    exports=Path(exports).resolve(); found={}
    for case in load(exports/'manifest.json'):
        for item in case['attachments']:
            name=item['suggestedHumanReadableName'].split('_')[0]
            if not name.startswith('eat-'): continue
            need(case.get('testIdentifier')==TEST, 'Traversal attachment belongs to wrong test case')
            need(item.get('isAssociatedWithFailure') is False, 'Failure-associated attachment rejected')
            need(re.fullmatch(r'eat-[a-z0-9-]+',name), 'Invalid attachment name')
            path=(exports/item['exportedFileName']).resolve()
            need(path.is_relative_to(exports) and path.is_file(), 'Missing attachment or path escape')
            need(name not in found, 'Duplicate attachment name')
            found[name]=path
    need('eat-records' in found, 'Missing records attachment')
    return found

def validate_resources(packet, runtime=RUNTIME):
    inventory=packet['resourceInventory']; need(bool(inventory),'Empty runtime resource inventory')
    ids=set(); paths={}
    for resource in inventory:
        need(resource['assetId'] not in ids, 'Duplicate inventory asset ID'); ids.add(resource['assetId'])
        path=(Path(runtime)/resource['path']).resolve()
        need(path.is_relative_to(Path(runtime).resolve()) and path.is_file(), 'Missing resource or source path escape')
        need(path.stat().st_size==resource['bytes'] and sha(path)==resource['sha256'], 'Resource bytes/hash mismatch')
        if resource['path'] in paths: need(paths[resource['path']]==resource['sha256'],'Conflicting resource identity')
        paths[resource['path']]=resource['sha256']
    return paths

def validate_root(row, previous):
    raw=(row['rawX'],row['rawY'])
    need(all(type(v) is int for v in raw), 'Q8 roots must be integers')
    need((row['deltaRawX'],row['deltaRawY'])==(raw[0]-previous[0],raw[1]-previous[1]), 'Independent root delta mismatch')
    snapshot=(row['snapshotX'],row['snapshotY'])
    expected=tuple((abs(value)//256)*(1 if value>=0 else -1) for value in raw)
    need(all(type(value) is int for value in snapshot) and snapshot==expected,
         'Snapshot root differs from Q8 truncation toward zero')
    need((row['renderedX'],row['renderedY'])==snapshot,
         'Actual rendered root differs from snapshot integer root')
    return raw

def validate_pause(paused):
    need(len(paused)==8 and len({(r['digest'],r['texturePNG_SHA256'],r['rawX'],r['rawY']) for r in paused})==1,
         'Eight-callback pause hold missing or texture/digest changed')

def validate_capture_image(capture, path):
    need(sha(path)==capture['sha256'],'Screenshot missing or hash mismatch')
    with Image.open(path) as image:
        need(list(image.size)==capture['nativePixels'],'Image dimensions differ from actual record')
        need(image.width>0 and image.width%704==0 and image.height%326==0 and image.width//704==image.height//326,
             'Image does not match logical viewport/backing scale')
        need(image.convert('RGB').getcolors(maxcolors=64) is None,'Blank screenshot')

def validate_rows(arm, resources):
    records=arm['records']; commands=arm['commands']; name=arm['arm']; reduced=name=='reduced'
    need(arm['reducedMotion'] is reduced, 'Reduced Motion arm identity mismatch')
    need(arm['expectedTerminalTick']==380 and len(commands)==380, 'Wrong command/terminal coverage')
    need([c['tick'] for c in commands]==list(range(1,381)), 'Command ticks missing/duplicate/out of order')
    for command in commands:
        route_name=phase(command['tick']); x,y=command['moveX'],command['moveY']
        expected = (0,0) if route_name=='release' else ((-1,1) if route_name=='slide-northwest' else
            ((1,0) if route_name in ('reverse-east','return-east') else ((0,-1) if route_name in ('rear-south-collision','front-south') else (-1,0))))
        sign=lambda value: (value>0)-(value<0)
        need((sign(x),sign(y))==expected and abs(x)<=32767 and abs(y)<=32767, 'Route command direction/range changed')
    magnitudes=[abs(commands[tick-1]['moveX']) for tick in (1,21,41)]
    need(0<magnitudes[0]<magnitudes[1]<magnitudes[2], 'Partial/full stick coverage absent')
    need(arm['finalDigest']==arm['replayDigest'] and bool(re.fullmatch('[0-9a-f]{64}',arm['finalDigest'])), 'Core replay digest mismatch')
    need(records and records[-1]['tick']==380 and records[-1]['digest']==arm['finalDigest'], 'No actual post-action completion records')
    previous=(736*256,654*256); previous_tick=0; paused=[]; phases=set(); used_textures={}; timestamps=[]
    collision=False; reversal=False; slide=False; relations=set()
    for ordinal,row in enumerate(records):
        tick=row['tick']; raw=(row['rawX'],row['rawY'])
        need(row['ordinal']==ordinal and previous_tick<=tick<=previous_tick+1, 'Callback/tick sequence mismatch')
        need(bool(re.fullmatch('[0-9a-f]{64}',row['digest'])), 'Missing authoritative digest')
        need(row['advanced']==(tick!=previous_tick), 'Recorded advancement mismatch')
        need(row['commandCount']==tick and row['commandTick']==tick, 'Command/sample tick binding mismatch')
        validate_root(row, previous)
        need(row['reducedMotion'] is reduced and row['bodyRadius']==18, 'Sample setting/radius mismatch')
        need(row['viewportPoints']==[704,326], 'Viewport changed')
        need(row['deliveredPath'] in resources and resources[row['deliveredPath']]==row['sourceSHA256'], 'Observed source not bound by inventory')
        need(row['clip']!='unidentified' and bool(row['facing']), 'Missing actual selection identity')
        key=row['textureAttachment']; digest=row['texturePNG_SHA256']
        need(key.startswith(f'eat-{name}-texture-') and re.fullmatch('[0-9a-f]{64}',digest), 'Invalid texture attachment identity')
        if key in used_textures: need(used_textures[key]==digest,'Texture identity changed')
        used_textures[key]=digest
        # Independent integer circle-vs-AABB check, not a movement/collision simulation.
        for x0,y0,x1,y1 in row['solidBounds']:
            qx=max(x0*256,min(raw[0],x1*256)); qy=max(y0*256,min(raw[1],y1*256))
            need((raw[0]-qx)**2+(raw[1]-qy)**2 >= (18*256)**2, 'Authoritative body penetrates solid')
        x0,y0,x1,y1=row['kioskBounds']
        relation='rear-side-world' if raw[1]>y1*256 else ('front-side-world' if raw[1]<y0*256 else 'side-world')
        need(row['kioskRelation']==relation,'Kiosk geometry relation mismatch'); relations.add(relation)
        if row['paused']:
            need(tick==55 and not row['advanced'] and raw==previous and row['phase']=='pause', 'Pause advanced authority or phase')
            paused.append(row)
        else:
            need(row['phase']==phase(tick),'Phase disagrees with command tick'); phases.add(row['phase'])
        if tick:
            command=commands[tick-1]
            need((row['moveX'],row['moveY'])==(command['moveX'],command['moveY']), 'Actual command data mismatch')
            need(command['dodge'] is False,'Unrequested dodge added')
        if row['phase']=='collision-west' and row['advanced'] and row['moveX']<0 and raw==previous: collision=True
        if row['phase']=='reverse-east' and row['deltaRawX']>0: reversal=True
        if row['phase']=='slide-northwest' and row['moveX']<0 and row['moveY']>0 and row['deltaRawX']==0 and row['deltaRawY']>0: slide=True
        timestamps.append(row['postActionUptime']); previous=raw; previous_tick=tick
    validate_pause(paused)
    need(all(a<=b for a,b in zip(timestamps,timestamps[1:])), 'Post-action clock regressed')
    need(phases=={n for n,_ in LEGS}, 'Missing route phase coverage')
    need(collision and reversal and slide, 'Actual collision/reversal/wall-slide coverage absent')
    need({'rear-side-world','front-side-world'}<=relations, 'Front/rear world-side traversal absent')
    need(len(used_textures)==arm['textureCount'],'Texture census mismatch')
    if not reduced:
        need(len({r['deliveredPath'] for r in records if r['requestedClip']=='player_move'})>1, 'Frozen normal moving selection')
    return used_textures

def validate_packet(packet, files, runtime=RUNTIME):
    need(packet['schema']=='existing-art-traversal-001' and packet['status']=='DIAGNOSTIC_NOT_ACCEPTANCE', 'Packet scope lifted')
    need(packet['testIdentity']==TEST and packet['viewportPoints']==[704,326], 'Test/viewport identity changed')
    need(packet['seed']==1 and packet['initialPosition']==[736,654] and packet['initialPositionIsTestFixture'] is True, 'Test-position fixture disclaimer changed')
    need(packet['unsupported']==UNSUPPORTED and 'not per-pixel' in packet['resourceScope'] and 'post-action still' in packet['captureSemantics'], 'Evidence scope/limitations weakened')
    resources=validate_resources(packet,runtime)
    need([a['arm'] for a in packet['arms']]==['normal','reduced'],'Two exact presentation arms required')
    need(packet['arms'][0]['commands']==packet['arms'][1]['commands'] and packet['arms'][0]['finalDigest']==packet['arms'][1]['finalDigest'], 'Same-command authority differs between settings')
    expected={'eat-records'}; count=0
    tick_maps=[]
    for arm in packet['arms']:
        ticks={}
        for row in arm['records']:
            value=(row['rawX'],row['rawY'],row['digest'])
            if row['tick'] in ticks: need(ticks[row['tick']]==value,'Authority changed without a tick')
            ticks[row['tick']]=value
        tick_maps.append(ticks)
    need(tick_maps[0]==tick_maps[1],'Per-tick authority differs between presentation settings')
    for arm in packet['arms']:
        textures=validate_rows(arm,resources)
        for key,digest in textures.items():
            need(key in files and sha(files[key])==digest,'Actual texture attachment missing or changed')
            with Image.open(files[key]) as image: need(image.width>0 and image.height>0,'Empty texture image')
        expected.update(textures)
        capture_rows=[(name,row) for row in arm['records'] for name in row.get('captureNames',[])]
        rows=dict(capture_rows)
        need(len(capture_rows)==26 and len(rows)==26, 'Duplicate or missing sample-to-capture bindings')
        captures=arm['captures']; names={c['name'] for c in captures}
        wanted={f'eat-{arm["arm"]}-{phase}-{mapping}' for phase in [n for n,_ in LEGS]+['pause'] for mapping in MAPPINGS}
        need(names==wanted and len(captures)==26 and set(rows)==wanted, 'Exact keypoint/mapping capture census mismatch')
        for capture in captures:
            key=capture['name']; row=rows[key]; mapping=capture['mapping']; expected.add(key)
            need(key.endswith('-'+mapping) and mapping in MAPPINGS and capture['captureKind']=='actual-post-action-renderer-still','Capture role mismatch')
            need(capture['tick']==row['tick'] and capture['digest']==row['digest'],'Image/sample authority binding mismatch')
            need(key in files and sha(files[key])==capture['sha256'],'Screenshot missing or hash mismatch')
            validate_capture_image(capture,files[key])
            x,y=row['snapshotX'],row['snapshotY']; cx,cy=capture['worldFocus']
            if mapping!='shipping': x,y=cx+math.sqrt(.5)*(x-cx-y+cy),cy+math.sqrt(.5)*(x-cx+y-cy)/2
            ax,ay=capture['observedPlayerSceneRoot']
            need(abs(ax-x)<.002 and abs(ay-y)<.002,'Independent midpoint/actual scene root mismatch')
            count+=1
    need(set(files)==expected,'Unreferenced or missing native attachment')
    return {'status':'VERIFIED_EXISTING_ART_DIAGNOSTIC_NOT_ACCEPTANCE','arms':2,'captures':count,
            'resources':len(packet['resourceInventory']), 'rows':sum(len(a['records']) for a in packet['arms']),
            'textures':sum(a['textureCount'] for a in packet['arms'])}

def verify(exports, summary, tree, runtime=RUNTIME, allowed_tests=(TEST,)):
    validate_result(summary,tree,allowed_tests); files=attachments(exports); packet=load(files['eat-records'])
    return validate_packet(packet,files,runtime),files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports',type=Path,required=True); parser.add_argument('--xcresult',type=Path,required=True)
    parser.add_argument('--import-to',type=Path)
    parser.add_argument('--coordinated-three',action='store_true',help='Exact authorized traversal/encounter/viewport set only')
    args=parser.parse_args()
    query=lambda kind: json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results',kind,'--path',str(args.xcresult)],text=True,timeout=45))
    summary,tree=query('summary'),query('tests')
    allowed=COORDINATED_TESTS if args.coordinated_three else (TEST,)
    report,files=verify(args.exports,summary,tree,allowed_tests=allowed)
    if args.import_to:
        need(not args.import_to.exists(),'Never overwrite prior native evidence')
        args.import_to.mkdir(parents=True)
        for name,path in files.items(): shutil.copyfile(path,args.import_to/(name+('.json' if name=='eat-records' else '.png')))
        for name,data in [('summary',summary),('tests',tree),('verification',report),('run-scope',{'allowedTests':sorted(allowed)})]:
            (args.import_to/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
        shutil.copyfile(args.exports/'manifest.json',args.import_to/'attachment-manifest.json')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,StopIteration) as error: print('VERIFICATION FAILED:',error,file=sys.stderr); sys.exit(1)
