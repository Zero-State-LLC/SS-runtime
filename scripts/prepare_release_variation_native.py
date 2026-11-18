#!/usr/bin/env python3
"""Prepare/verify new test-only variation PNGs. Never modify either frozen source packet."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/review/player-release-variation-20261116'
sys.path.insert(0,str(SOURCE))
import verify_packet
import variation as v

ASSETS=ROOT/'AppTests/ReleaseVariationAssets'
PHASES=v.NEW
FAMILIES=('baseline','variation')

def name(family,p,k):
    if k==0:return f'player-source-s-{p-1:02d}'
    if k==16:return 'player-source-s-neutral'
    return f'player-{"allrelease" if family=="baseline" else "releasevariation"}-{p:02d}-{k:02d}'

def resource(family,p,k):
    folder=ASSETS if family=='variation' and 0<k<16 else ROOT/'AppTests/BenchmarkAssets'
    return folder/(name(family,p,k)+'.png')

def verify_resources():
    verify_packet.verify(SOURCE/'artifacts')
    expected={name('variation',p,k)+'.png' for p in PHASES for k in range(1,16)}
    v.b.require({f.name for f in ASSETS.glob('*.png')}==expected,'Expected exactly210 isolated variation resources')
    hashes={}
    for family in FAMILIES:
        source=(v.BASE if family=='baseline' else SOURCE)/'artifacts'
        for p in PHASES:
            for k in range(17):
                original=source/f'phase-{p:02d}/frames/{k:02d}.png';path=resource(family,p,k)
                if k in (0,16):
                    v.b.require(v.b.rgba(path)==v.b.rgba(original),'Endpoint RGBA differs from frozen source')
                else:
                    v.b.require(v.b.sha(path)==v.b.sha(original),'Intermediate PNG differs from frozen source')
                hashes[name(family,p,k)]=v.b.sha(path)
    v.b.require(json.loads((ASSETS/'release-variation-resource-hashes.json').read_text())==hashes,'Bundled resource hash catalog drift')
    return hashes

def prepare():
    verify_packet.verify(SOURCE/'artifacts')
    v.b.require(not ASSETS.exists(),'Keep prior resources, use --verify to recheck')
    ASSETS.mkdir(parents=True)
    for p in PHASES:
        for k in range(1,16):
            shutil.copy2(SOURCE/'artifacts'/f'phase-{p:02d}/frames/{k:02d}.png',resource('variation',p,k))
    hashes={name(f,p,k):v.b.sha(resource(f,p,k)) for f in FAMILIES for p in PHASES for k in range(17)}
    v.b.save(ASSETS/'release-variation-resource-hashes.json',hashes)
    verify_resources()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    if not args.verify:prepare()
    print(json.dumps({'status':'TEST_RESOURCES_VERIFIED','isolatedVariationPNGs':210,'uniqueBaselineAndVariationResources':len(verify_resources())}))
