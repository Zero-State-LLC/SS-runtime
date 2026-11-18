#!/usr/bin/env python3
"""Final packet verification, including complete archived inventory and review claims."""
import argparse
import json
from pathlib import Path
import variation as v


def verify(output, source_root=None):
    result=v.verify(output)
    # Validate baseline frame AND sample hashes before using it for comparison.
    v.portable.verify(v.BASE/'artifacts',v.BASE/'fixtures')
    v.b.require(v.load(output/'input-inventory.json')==v.load(v.BASE/'artifacts/input-inventory.json'),'Complete1012-file archived inventory differs from locked baseline')
    manifest=v.load(output/'manifest.json')
    v.b.require(manifest['variation']=='Deterministic stance/phase easing and support lift, no new body warp','Variation identity changed')
    v.b.require(manifest['nativeVariationVerified'] is False,'Variation native acceptance claim changed')
    v.b.require(manifest['ownerDirectionUTC']=='2026-11-16T02:36:26Z','Owner direction provenance changed')
    if source_root is not None:
        v.check_state(source_root,output)
        result['originalMastersReopened']=True
        result['originalFilesRehashed']=1012
    baseline=v.load(v.BASE/'artifacts/manifest.json')
    pixel_changes={}
    for candidate,original in zip(manifest['phases'],baseline['phases']):
        phase=candidate['phase']
        changed=[k for k,(a,b) in enumerate(zip(candidate['frames'],original['frames'])) if a['rgbaSHA256']!=b['rgbaSHA256']]
        v.b.require(not changed if phase in v.b.PRESERVED else bool(changed),f'Phase{phase} variation/preservation pixels absent')
        v.b.require(0 not in changed and 16 not in changed,f'Phase{phase} endpoint pixels changed')
        pixel_changes[phase]=changed
    result['changedRGBAPosesFromBaseline']=pixel_changes
    result['fullArchivedInventoryMatchesBaseline']=True
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=v.HERE/'artifacts')
    parser.add_argument('--source-root',type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.output.resolve(),args.source_root.resolve() if args.source_root else None),indent=2))
