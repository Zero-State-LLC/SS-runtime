#!/usr/bin/env python3
"""Import/verify exact BP001 native-trial attachments. Never creates review art."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess
from PIL import Image, ImageChops
from palette_conformance import measure, flags

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/review/bp001-reference-trial-20261116'
SOURCE = ['AppTests/ReferenceProjectionCaptureTests.swift','AppTests/ReferenceProjectionTrial.swift',
          'App/WorldRenderer.swift','App/BenchmarkReviewArt.swift','App/GameScene.swift',
          'scripts/palette_conformance.py']
FIXTURES = ['quiet-street','legal-ghost-step-4976']
MAPPINGS = ['reference-fit','midpoint']
ZOOMS = [100,125,140]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected():
    result={}
    for fixture,mapping,zoom in itertools.product(FIXTURES,MAPPINGS,ZOOMS):
        base=f'BP001-trial-{fixture}-{mapping}-z{zoom}'
        result[base+'-metrics']='json'
        for geometry,rendition in itertools.product(['','-geometry'],['native','half','grayscale']):
            result[f'{base}{geometry}-{rendition}']='png'
    result['BP001-trial-same-world-commands']='json'
    return result


def import_attachments(exports, result_bundle):
    summary=json.loads(subprocess.check_output(['xcrun','xcresulttool','get','test-results','summary','--path',str(result_bundle)]))
    if summary.get('failedTests',1)!=0 or summary.get('passedTests',0)<3 or summary.get('skippedTests',0)!=0:
        raise ValueError(f'Need successful complete trial suite, observed {summary}')
    names=expected()
    found={}
    manifest_path=exports/'manifest.json'
    for test in json.loads(manifest_path.read_text()):
        for item in test.get('attachments',[]):
            human=item['suggestedHumanReadableName']
            name=re.split(r'_\d+_',human,maxsplit=1)[0]
            if name not in names:
                continue
            if item.get('isAssociatedWithFailure'):
                raise ValueError(f'Failure-associated evidence: {name}')
            if name in found:
                raise ValueError(f'Duplicate attachment: {name}')
            source=exports/item['exportedFileName']
            extension=names[name]
            destination=PACK/('plates' if extension=='png' else 'metrics')/(name+'.'+extension)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,destination)
            found[name]=dict(path=str(destination.relative_to(PACK)),sha256=digest(source),
                             exportedFileName=item['exportedFileName'],timestamp=item['timestamp'],
                             deviceName=item.get('deviceName'),deviceId=item.get('deviceId'))
    if set(found)!=set(names):
        raise ValueError(f'Missing attachments: {sorted(set(names)-set(found))}')
    prior=json.loads((PACK.parent/'bp001-decision-20261116/capture-provenance.json').read_text())
    for name,sha in prior['sourceSHA256'].items():
        assert digest(ROOT/name)==sha, f'Existing fixture/source drift: {name}'
    record=dict(status='NATIVE_STATIC_TRIAL_NOT_PROJECTION_SELECTION',
                preservedSourceHashes=prior['sourceSHA256'],
                xcresultPath=str(result_bundle),xcresultSummary=summary,
                exportManifestSHA256=digest(manifest_path),
                sourceHashes={name:digest(ROOT/name) for name in SOURCE},
                fitSHA256=digest(PACK/'ground-fit.json'),landmarksSHA256=digest(PACK/'landmarks.json'),
                referenceSHA256=digest(PACK.parent/'bp001-decision-20261116/street-corner-approved-concept.png'),
                ownerChoice='UNRECORDED',shippingMappingChanged=False,attachments=found)
    (PACK/'capture-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    (PACK/'palette-report.json').write_text(json.dumps(palette_report(),indent=2)+'\n')


def palette_report():
    reference=measure(PACK.parent/'bp001-decision-20261116/street-corner-approved-concept.png')
    reference['file']='../bp001-decision-20261116/street-corner-approved-concept.png'
    result=dict(method='BP-011',excludeTopNativePixels=240,zoneAllowance=None,
                lowerTouchControlsRetained=True,referenceUncropped=True,reference=reference,plates=[])
    for fixture,mapping,zoom in itertools.product(FIXTURES,MAPPINGS,ZOOMS):
        name=f'BP001-trial-{fixture}-{mapping}-z{zoom}-native.png'
        row=measure(PACK/'plates'/name,240)
        row['file']='plates/'+name
        row['flags']=flags(row,reference,None)
        result['plates'].append(row)
    return result


def verify():
    record=json.loads((PACK/'capture-manifest.json').read_text())
    assert set(record['attachments'])==set(expected()), 'Attachment census drift'
    for name,sha in record['sourceHashes'].items():
        assert digest(ROOT/name)==sha, f'Capture source drift: {name}'
    assert digest(PACK/'ground-fit.json')==record['fitSHA256']
    assert digest(PACK/'landmarks.json')==record['landmarksSHA256']
    assert digest(PACK.parent/'bp001-decision-20261116/street-corner-approved-concept.png')==record['referenceSHA256']
    fit=json.loads((PACK/'ground-fit.json').read_text())
    assert record['referenceSHA256']==fit['referenceSHA256']
    for name,item in record['attachments'].items():
        path=PACK/item['path']
        assert digest(path)==item['sha256'], f'Attachment bytes drift: {name}'
        if path.suffix=='.png':
            with Image.open(path) as image:
                target=(1056,489) if name.endswith('-half') else (2112,978)
                assert image.size==target, (name,image.size,target)
                if name.endswith('-grayscale'):
                    r,g,b=image.convert('RGB').split()
                    assert ImageChops.difference(r,g).getextrema()[1]<=1
                    assert ImageChops.difference(g,b).getextrema()[1]<=1
    for name,sha in record['preservedSourceHashes'].items():
        assert digest(ROOT/name)==sha, f'Existing fixture/source drift: {name}'
    prior=json.loads((PACK.parent/'bp001-decision-20261116/capture-provenance.json').read_text())
    metrics=[]
    for fixture,mapping,zoom in itertools.product(FIXTURES,MAPPINGS,ZOOMS):
        path=PACK/'metrics'/f'BP001-trial-{fixture}-{mapping}-z{zoom}-metrics.json'
        row=json.loads(path.read_text())
        assert row['mapping']==mapping and row['fixture']==fixture
        assert row['zoom']==zoom/100 and row['viewportPoints']==[704,326]
        assert row['nativePixels']==[2112,978] and row['backingScale']==3
        assert row['hudExcludedFromProjection'] is True
        assert row['buildingRegistrationChangedBetweenMappings'] is False
        assert row['rotationDegrees']==(fit['sceneRotationDegrees'] if mapping=='reference-fit' else 45)
        assert row['yScale']==(fit['groundYScale'] if mapping=='reference-fit' else .5)
        if fixture.startswith('legal'):
            assert row['tick']==4976 and row['enemies']>=2 and row['projectiles']>=1
            assert row['digest']==prior['encounter']['digest'], 'Existing legal encounter changed'
        assert row['referenceImageSHA256']==record['referenceSHA256']
        assert row['landmarksSHA256']==record['landmarksSHA256']
        metrics.append(row)
    for fixture in FIXTURES:
        rows=[r for r in metrics if r['fixture']==fixture]
        assert len({r['digest'] for r in rows})==1
        assert len({tuple(r['worldFocus']) for r in rows})==1
        reference=rows[0]['actors']
        for row in rows:
            for a,b in zip(reference,row['actors']):
                for key in ['name','worldRoot','anchor','logicalSize','sourceTexturePixels','sourceAlphaOccupiedRows']:
                    assert a[key]==b[key], (fixture,key,a['name'])
            assert len(row['actors'])==len(reference)
    assert json.loads((PACK/'palette-report.json').read_text())==palette_report(), 'Palette recomputation drift'
    return dict(status='VERIFIED_NATIVE_STATIC_TRIAL_NOT_ACCEPTANCE',plates=72,metrics=12,
                referenceUnchanged=True,sourceHashesVerified=len(record['sourceHashes']),
                ownerChoice='UNRECORDED',shippingMappingChanged=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports',type=Path)
    parser.add_argument('--xcresult',type=Path)
    args=parser.parse_args()
    if bool(args.exports)!=bool(args.xcresult):
        parser.error('--exports and --xcresult must be provided together')
    if args.exports:
        import_attachments(args.exports,args.xcresult)
    result=verify()
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
