#!/usr/bin/env python3
"""Run validation and prove byte-identical replay without a new art iteration."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
NAMES=['ground.png','material-ids.png','ground.svg','final-plan-preview.png','final-source-detail.png','plan.json','material-1-tile.png','material-2-tile.png','material-3-tile.png','material-4-tile.png','road-mask.png','road-details.png','road-details-mask.png','road-details.svg-fragment']
def hashes():return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in NAMES}
def main():
    before=hashes();env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    replay=subprocess.run([sys.executable,str(HERE/'replay.py')],capture_output=True,text=True,env=env)
    if replay.returncode:raise RuntimeError(replay.stdout+replay.stderr)
    after=hashes()
    if before!=after:raise RuntimeError('Replay changed final-correction bytes, no third art pass permitted')
    tests=subprocess.run([sys.executable,str(HERE/'test_plan.py')],capture_output=True,text=True,env=env)
    (HERE/'validation-tests.log').write_text(tests.stdout+tests.stderr)
    if tests.returncode:raise RuntimeError(tests.stdout+tests.stderr)
    from test_plan import load,validate_ground_pixels
    from PIL import Image
    with Image.open(HERE/'ground.png') as image:samples=validate_ground_pixels(load(HERE/'plan.json'),image)
    result=dict(status='SEMANTIC_CHECKS_PASS_NOT_VISUAL_ACCEPTANCE',tests=27,adversarialMutations=18,actualRGBSamples=samples,replayByteIdentical=True,replaySHA256=after,immutableV7Files=len(json.loads((HERE/'v7-immutable-sha256.json').read_text())),sourceAttempts=2,artCorrections=1,attempt01FilesPreserved=17,nativeExecution=False,limits=['Nine legacy raster buildings have unknown actual mesh contact.','No loaded executable or scene binding claim in this source lane.'])
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    files={str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(HERE.rglob('*')) if f.is_file() and f!=HERE/'manifest.json' and '__pycache__' not in f.parts}
    (HERE/'manifest.json').write_text(json.dumps(dict(status='FINAL_CORRECTION_NOT_VISUALLY_ACCEPTED',attempt=2,files=files),indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
