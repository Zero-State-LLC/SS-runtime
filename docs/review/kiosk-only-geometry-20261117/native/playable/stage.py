#!/usr/bin/env python3
"""Stage three exact review PNGs with a frozen manifest, never canonical assets."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent
ROOT = HERE.parents[4]
TEXTURED = NATIVE / 'textured/output'
V9 = ROOT / 'docs/review/blocked-base-curb-relief-20261116/scene/native-inputs-v9'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage():
    output = HERE / 'resources'
    if output.exists():
        raise ValueError('Preserve existing staged review resources')
    assert sha(TEXTURED / 'manifest.json') == '647ec749a5a87bb1e24135ebc758655a1ccd84ca003020e95b0c3a0f3e199953'
    assert sha(V9 / 'native-inputs.json') == '2c4c3f6a3ef48003291f1ca6421bc6731b4c385a5a17738403c5dcd7972aca88'
    bindings = json.loads((TEXTURED / 'bindings.json').read_text())
    source = json.loads((V9 / 'native-inputs.json').read_text())
    base = next(row for row in source['supplements'] if row['role'] == 'v9-blocked-kiosk-base')
    sources = []
    for role in ['current', 'candidate', 'base']:
        binding = base if role == 'base' else bindings[role]
        path = V9 / binding['file'] if role == 'base' else TEXTURED / binding['sourceFile']
        digest = binding['sha256'] if role == 'base' else binding['sourceSHA256']
        assert sha(path) == digest
        reg = binding['registration']
        sources.append(dict(role=role, file=role + '.png', sha256=digest,
                            canvasPixels=reg['canvasPixels'], rootPixelsTopLeft=reg['rootPixelsTopLeft'],
                            worldPosition=reg['worldPosition'], drawSizeWorld=reg['drawSizeWorld']))
    output.mkdir(parents=True)
    for row in sources:
        path = V9 / base['file'] if row['role'] == 'base' else TEXTURED / bindings[row['role']]['sourceFile']
        shutil.copyfile(path, output / row['file'])
    manifest = dict(schema='debug-playable-kiosk-review-001', solidID='solid-03-transit-kiosk',
                    authoritativeBounds=[512, 640, 640, 768], ownerAcceptance=False, productionAdmitted=False,
                    texturedManifestSHA256=sha(TEXTURED / 'manifest.json'), v9InputSHA256=sha(V9 / 'native-inputs.json'),
                    sources=sources)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Manifest SHA256:', sha(output / 'manifest.json'))
    for row in sources:
        print(row['file'], row['sha256'])


if __name__ == '__main__':
    stage()
