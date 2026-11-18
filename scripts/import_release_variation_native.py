#!/usr/bin/env python3
"""Import paired actual SpriteKit variation evidence. ADAPT import_allrelease_native.py:20-128."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
from PIL import Image
import prepare_release_variation_native as source

ROOT=source.ROOT
PHASES=source.PHASES
FAMILIES=source.FAMILIES
ORDER=[(f,p,k) for p in PHASES for f in FAMILIES for k in range(17)]
EXPECTED=set(ORDER)
TESTS={f'ReleaseVariationSourceTests/{name}()' for name in (
    'testPairedAllPosesUseExactSourceTexturesAndTiming',
    'testBothFamiliesBypassAndCancelReducedMotion',
    'testBothFamiliesInterruptAndRestartWithoutStalePose')}
STATUS='STATIC_NATIVE_VARIATION_COMPARISON_NOT_ADMISSION'

def need(ok,message):
    if not ok:raise ValueError(message)

def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def filename(f,p,k):return f'{f}-phase-{p:02d}-pose-{k:02d}.png'

def validate_result(summary,tree):
    need(summary.get('passedTests')==3 and summary.get('totalTestCount')==3 and summary.get('failedTests')==0 and summary.get('skippedTests')==0 and summary.get('expectedFailures')==0 and summary.get('result')=='Passed','Expected3 actual passing native tests, no zero/failed/skipped/expected failures')
    cases=[]
    def walk(node):
        if node.get('nodeType')=='Test Case':cases.append(node)
        for child in node.get('children',[]):walk(child)
    for node in tree['testNodes']:walk(node)
    need(len(cases)==3 and {c['nodeIdentifier'] for c in cases}==TESTS and all(c['result']=='Passed' for c in cases),'Wrong focused test identities/results')
    return cases

def validate_records(rows):
    need([(r['family'],r['phase'],r['pose']) for r in rows]==ORDER,'Expected476 ordered paired pose records')
    for row in rows:
        f,p,k=row['family'],row['phase'],row['pose']
        need(row['tickOffset']==(k*180+127)//128,'Wrong exact3/128 tick sampling')
        need(row['source']==source.name(f,p,k),'Wrong paired source identity')
        need(row['capture']==f'releasevariation-{f}-{p:02d}-pose-{k:02d}','Wrong paired capture name')
        need(re.fullmatch('[0-9a-f]{64}',row['sourceSHA256']) is not None,'Invalid actual source SHA')

def attachments(exports):
    images={};records=[]
    for case in load(exports/'manifest.json'):
        for item in case['attachments']:
            name=item.get('suggestedHumanReadableName','')
            path=(exports/item['exportedFileName']).resolve()
            need(path.is_relative_to(exports.resolve()),'Export path escape')
            match=re.match(r'releasevariation-(baseline|variation)-(\d+)-pose-(\d+)(?:_|\.|$)',name)
            if match:
                family,p,k=match.groups();key=(family,int(p),int(k))
                need(key not in images,'Duplicate paired native image')
                images[key]=path
            elif name.startswith('releasevariation-pose-records'):records.append(path)
    need(set(images)==EXPECTED and len(records)==1,'Expected exactly476 native images and one record attachment')
    rows=load(records[0]);validate_records(rows)
    return images,records[0],rows

def source_files(rows):
    names={'AppTests/ReleaseVariationSourceTests.swift','project.yml',
           'AppTests/ReleaseVariationAssets/release-variation-resource-hashes.json',
           'docs/review/player-release-variation-20261116/artifacts/manifest.json',
           'docs/review/player-all-release-source-20261116/artifacts/manifest.json',
           'scripts/prepare_release_variation_native.py','scripts/import_release_variation_native.py'}
    names.update(str(source.resource(r['family'],r['phase'],r['pose']).relative_to(ROOT)) for r in rows)
    return names

def check_sources(rows):
    catalog=source.verify_resources()
    for row in rows:
        need(row['sourceSHA256']==catalog[row['source']],'Actual bundled PNG bytes differ from verified frozen source resource')
    return {name:sha(ROOT/name) for name in sorted(source_files(rows))}

def image_facts(images):
    digests={}
    for key,path in images.items():
        with Image.open(path) as im:
            need(im.format=='PNG' and im.size==(576,432),'Native crop must be PNG576x432')
            digests[key]=hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()
    for family in FAMILIES:
        for p in PHASES:
            need(len({digests[(family,p,k)] for k in range(17)})==17,'Native phase must contain17 distinct selected poses')
    for p in PHASES:
        for k in (0,16):need(digests[('baseline',p,k)]==digests[('variation',p,k)],'Paired native endpoint RGBA differs')
    return {'dimensions':[576,432],'distinctPosesPerFamilyPhase':17,'pairedEndpointRGBAEqualities':28,
            'changedNativePosesByPhase':{str(p):[k for k in range(17) if digests[('baseline',p,k)]!=digests[('variation',p,k)]] for p in PHASES}}

def verify_capture(target):
    report=load(target/'verification.json')
    need(report['status']==STATUS and report['poses']==476 and report['phases']==PHASES and report['families']==list(FAMILIES),'Published native census/status changed')
    need(report['liveCadenceVerified'] is False and report['artAdmission'] is False,'Native acceptance scope lifted')
    need(report['authoredNeutralBoundarySeconds']==0.375 and report['firstEligibleNeutralTickOffset']==23,'Native timing declaration changed')
    validate_result(report['summary'],load(target/'tests.json'))
    rows=load(target/'pose-records.json');validate_records(rows)
    expected={filename(*key) for key in EXPECTED}|{'pose-records.json','tests.json'}
    need(set(report['attachmentHashes'])==expected,'Published attachment hash census changed')
    need({p.name for p in target.glob('*.png')}=={filename(*key) for key in EXPECTED},'Published PNG census changed')
    for name,digest in report['attachmentHashes'].items():need(sha(target/name)==digest,f'Native attachment hash drift:{name}')
    hashes=check_sources(rows)
    need(report['sourceHashes']==hashes,'Native source/configuration hash drift')
    facts=image_facts({key:target/filename(*key) for key in EXPECTED})
    need(report['imageFacts']==facts,'Native image facts changed')
    return {'status':STATUS,'verifiedPoses':476,'verifiedSourceFiles':len(hashes),'nativeEndpointEqualities':28,
            'passedActualTests':3,'changedNativePoses':sum(len(x) for x in facts['changedNativePosesByPhase'].values()),'liveCadenceVerified':False}

def import_capture(exports,result,target):
    need(not target.exists(),'Use a fresh output path, preserve previous evidence')
    def query(kind):return json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results',kind,'--path',str(result)],text=True))
    summary,tree=query('summary'),query('tests');validate_result(summary,tree)
    images,record,rows=attachments(exports)
    hashes=check_sources(rows);facts=image_facts(images)
    target.mkdir(parents=True)
    for key,path in sorted(images.items()):shutil.copy2(path,target/filename(*key))
    shutil.copy2(record,target/'pose-records.json')
    (target/'tests.json').write_text(json.dumps(tree,indent=2)+'\n')
    names={filename(*key) for key in EXPECTED}|{'pose-records.json','tests.json'}
    report={'status':STATUS,'poses':476,'phases':PHASES,'families':list(FAMILIES),'summary':summary,
            'xcresult':str(result.resolve()),'sourceHashes':hashes,'attachmentHashes':{n:sha(target/n) for n in sorted(names)},
            'imageFacts':facts,'authoredNeutralBoundarySeconds':0.375,'firstEligibleNeutralTickOffset':23,
            'liveCadenceVerified':False,'artAdmission':False,
            'limits':['Actual isolated static WorldRenderer capture, not live callback timing','Source neutral boundary0.375s, first whole60Hz tick offset23','No shared-scene/four-facing/physical-device or family acceptance','Original5/13 unchanged and excluded','No shipping selection, mapping/input or production art changes']}
    (target/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    options=''.join(f'<option value="{p:02d}">{p:02d}</option>' for p in PHASES)
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Native release variation comparison</title>
<style>body{font:16px system-ui;background:#20272c;color:#eee;margin:24px}a{color:#bddfff}.pair{display:flex;gap:20px;flex-wrap:wrap}img{width:576px;max-width:100%}button,select,input{font:inherit}</style>
<h1>Actual SpriteKit baseline / variation</h1><p>476 static captures,14phases ×17poses ×2families. PROPOSED source art, not admission. Original05/13 unchanged and excluded. This is not live cadence, normal-speed playback, full shared-scene or physical-device evidence.</p>
<p>Exact source neutral boundary0.375s, first eligible whole60Hz tick offset23. Crop192×144points,576×432pixels. Both columns select the same phase and pose.</p><p><a href="../README.md">Evidence and reproduction</a> | <a href="verification.json">Provenance</a> | <a href="pose-records.json">Actual texture/tick records</a></p>
<label>Phase <select id="phase">OPTIONS</select></label><label> Pose <input id="pose" type="range" min="0" max="16" value="0"></label><output id="status"></output>
<div class="pair"><section><h2>Baseline</h2><img id="baseline" alt="Actual baseline native crop"></section><section><h2>Variation</h2><img id="variation" alt="Actual variation native crop"></section></div>
<script>const phase=document.getElementById('phase'),pose=document.getElementById('pose'),status=document.getElementById('status');function show(){const suffix=`phase-${phase.value}-pose-${String(pose.value).padStart(2,'0')}.png`;status.textContent=`Phase${phase.value}, pose${pose.value}/16, static source selection`;for(const family of ['baseline','variation']){const im=document.getElementById(family);im.onerror=()=>status.textContent='Missing native capture';im.src=family+'-'+suffix}}phase.onchange=show;pose.oninput=show;show();</script></html>'''
    (target/'index.html').write_text(html.replace('OPTIONS',options))
    return verify_capture(target)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports',type=Path);parser.add_argument('--xcresult',type=Path);parser.add_argument('--output',type=Path)
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    if args.verify:answer=verify_capture(args.verify)
    elif args.exports and args.xcresult and args.output:answer=import_capture(args.exports,args.xcresult,args.output)
    else:parser.error('Use --verify PATH or --exports/--xcresult/--output')
    print(json.dumps(answer,indent=2))
