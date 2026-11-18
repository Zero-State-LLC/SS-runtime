"""One-time separately identified canonical identity derivative for runtime#245."""
import json
import hashlib
from pathlib import Path
import shutil
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
PILOT=HERE.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if (HERE/'identity-policy.json').exists():
        raise RuntimeError('Refusing to overwrite an existing correction derivative')
    before={str(p.relative_to(PILOT)):sha(p) for p in PILOT.rglob('*') if p.is_file() and HERE not in p.parents}
    shutil.copytree(PILOT/'inputs',HERE/'inputs')
    for source,target in [('render.py','garment_renderer.py'),('south-neutral.png','pilot01.png'),('tests.log','pilot01-tests.log'),('test_correspondence.py','pilot01-test_correspondence.py'),('provenance.json','source-provenance.json')]:
        shutil.copyfile(PILOT/source,HERE/target)
    with Image.open(HERE/'inputs/source/south-neutral-original.png') as image:
        original=np.array(image.convert('RGBA'))
    with Image.open(HERE/'inputs/layers/original_upper.png') as image:
        upper=np.array(image.convert('RGBA'))
    # Source ownership, never selected from output differences. Before row200 all
    # canonical visible paint is identity, since garment panels begin at row200.
    owned=upper[:,:,3]>0
    owned[:200] |= original[:200,:,3]>0
    Image.fromarray((owned*255).astype(np.uint8)).save(HERE/'canonical-upper-ownership.png')
    derivative=np.zeros_like(original)
    derivative[owned]=original[owned]
    Image.fromarray(derivative).save(HERE/'canonical-upper-derivative.png')
    policy=dict(schema=1,issue=245,authority='Coordinator09:47UTC: canonical original neutral identity wins',
        operation='exact RGBA assignment, never alpha-over',
        ownership='copied original_upper alpha>0 UNION canonical original alpha>0 above garment start row200',
        source='inputs/source/south-neutral-original.png',sourceSHA256=sha(HERE/'inputs/source/south-neutral-original.png'),
        mask='canonical-upper-ownership.png',maskSHA256=sha(HERE/'canonical-upper-ownership.png'),
        derivative='canonical-upper-derivative.png',derivativeSHA256=sha(HERE/'canonical-upper-derivative.png'),
        ownershipSource='inputs/layers/original_upper.png',ownershipSourceSHA256=sha(HERE/'inputs/layers/original_upper.png'),
        ownedPixelCount=int(owned.sum()),hiddenTextureRecovered=False)
    (HERE/'identity-policy.json').write_text(json.dumps(policy,indent=2)+'\n')
    model=json.loads((PILOT/'garment.json').read_text())
    model['status']='CANONICAL_IDENTITY_02_AWAITING_COORDINATOR'
    model['identityPolicy']='identity-policy.json'
    (HERE/'garment.json').write_text(json.dumps(model,indent=2)+'\n')
    (HERE/'pilot01-immutable-inventory.json').write_text(json.dumps(before,indent=2)+'\n')
    print(json.dumps(policy,indent=2))

if __name__=='__main__':
    main()
