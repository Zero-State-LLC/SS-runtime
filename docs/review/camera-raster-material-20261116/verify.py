#!/usr/bin/env python3
"""Focused packet evidence checks, not art acceptance."""
import json
from pathlib import Path
from PIL import Image
from replay import sha
HERE = Path(__file__).resolve().parent
EXPECTED_EXPORTS = {'camera-master.png','camera-native.png','camera-half.png','comparison.png','comparison-grayscale.png','ordinary-background-context.png'}

def verify(root=HERE):
    provenance = json.loads((root/'provenance.json').read_text())
    model = json.loads((root/'model.json').read_text())
    record = json.loads((root/'pilot-01/manifest.json').read_text())
    def need(value,message):
        if not value:
            raise ValueError(message)
    need(record['status']=='FIRST_PILOT_REVIEW_ONLY' and record['visualAttempt']==1, 'Status/attempt')
    need(not record['ownerAccepted'] and not record['productionAdmitted'] and not record['nativeCapture'], 'Acceptance scope')
    need(record['modelSHA256']==sha(root/'model.json'), 'Model changed')
    need(record['rendererSHA256']==sha(root/'replay.py'), 'Renderer changed')
    need(set(record['inputs'])==set(provenance['files']), 'Input census')
    for name,info in provenance['files'].items():
        p = root/'inputs'/name
        need(sha(p)==info['sha256']==record['inputs'][name], 'Input hash '+name)
        if p.suffix=='.png':
            with Image.open(p) as im:
                need(list(im.size)==info['size'] and im.mode==info['mode'], 'Input dimensions/mode '+name)
    names = {p['name'] for p in model['parts']}
    need(len(names)==16, 'Component census')
    expected = EXPECTED_EXPORTS | {f'{folder}/{name}.png' for folder in ('components','uv-samples') for name in names}
    need(set(record['exports'])==expected, 'Export census')
    for name,digest in record['exports'].items():
        need(sha(root/'pilot-01'/name)==digest, 'Export hash '+name)
    for name,size in [('camera-native.png',[42,104]),('camera-half.png',[21,52]),('camera-master.png',[180,450])]:
        with Image.open(root/'pilot-01'/name) as im:
            need(list(im.size)==size and im.mode=='RGBA', 'Output dimensions '+name)
            pixels = im.tobytes()
            need(all(pixels[i:i+3]==b'\x00\x00\x00' for i in range(0,len(pixels),4) if pixels[i+3]==0), 'Transparent RGB '+name)
    return dict(inputs=len(record['inputs']), components=16, exports=len(expected), status='TECHNICAL_ONLY_NOT_VISUAL_ACCEPTANCE')

if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
