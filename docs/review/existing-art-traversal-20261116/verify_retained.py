#!/usr/bin/env python3
"""Offline actual-evidence verification, no xcrun or external exports.
Fails closed when no retained capture exists. Not part of synthetic pre-capture guard tests.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import verify_capture as v

def verify_retained(capture):
    capture=Path(capture)
    v.need((capture/'eat-records.json').is_file(),'Native capture pending: no retained actual evidence')
    manifest=v.load(capture/'attachment-manifest.json')
    with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as directory:
        exports=Path(directory).resolve()
        for case in manifest:
            for item in case['attachments']:
                name=item['suggestedHumanReadableName'].split('_')[0]
                if not name.startswith('eat-'): continue
                source=capture/(name+('.json' if name=='eat-records' else '.png'))
                dest=(exports/item['exportedFileName']).resolve()
                v.need(dest.is_relative_to(exports),'Retained export path escape')
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source,dest)
        (exports/'manifest.json').write_text(json.dumps(manifest))
        allowed=v.load(capture/'run-scope.json')['allowedTests']
        return v.verify(exports,v.load(capture/'summary.json'),v.load(capture/'tests.json'),allowed_tests=allowed)[0]

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('capture',type=Path)
    args=parser.parse_args()
    try: print(json.dumps(verify_retained(args.capture),indent=2))
    except (ValueError,FileNotFoundError) as error: parser.exit(1,str(error)+'\n')
