"""Canonical identity correction over unchanged explicit front garment meshes."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import garment_renderer as garment

HERE=Path(__file__).resolve().parent
rgba=garment.rgba
sha=garment.sha
sample=garment.sample

def identity_inputs(model,base):
    policy=json.loads((base/model['identityPolicy']).read_text())
    if policy['schema']!=1:
        raise ValueError('Unsupported identity policy')
    for key in ['source','mask','derivative','ownershipSource']:
        if sha(base/policy[key])!=policy[key+'SHA256']:
            raise ValueError('Canonical identity input changed: '+key)
    original=np.array(rgba(base/policy['source']))
    upper=np.array(rgba(base/policy['ownershipSource']))
    with Image.open(base/policy['mask']) as image:
        mask=np.array(image.convert('L'))
    expected=upper[:,:,3]>0
    expected[:200] |= original[:200,:,3]>0
    if not np.array_equal(mask,expected.astype(np.uint8)*255):
        raise ValueError('Ownership differs from declared source support')
    owned=mask==255
    derivative=np.array(rgba(base/policy['derivative']))
    predicted=np.zeros_like(original)
    predicted[owned]=original[owned]
    if not np.array_equal(derivative,predicted):
        raise ValueError('Derivative differs from canonical source RGBA')
    return owned,derivative

def render(model,base=HERE):
    owned,derivative=identity_inputs(model,base)
    image,layers,owners=garment.render(model,base)
    pixels=np.array(image)
    # Replacement preserves canonical partial alpha and RGB. Alpha-over is wrong.
    pixels[owned]=derivative[owned]
    return Image.fromarray(pixels),layers,owners

def build(base=HERE):
    model=json.loads((base/'garment.json').read_text())
    image,_,_=render(model,base)
    image.save(base/'south-neutral.png')
    original=rgba(base/'inputs/source/south-neutral-original.png')
    pilot=rgba(base/'pilot01.png')
    plate=Image.new('RGB',(1152,444),'#283036')
    draw=ImageDraw.Draw(plate)
    labels=['Canonical original neutral','Preserved pilot01 (identity defect)','Canonical identity02 (exact replacement)']
    for i,(im,label) in enumerate(zip([original,pilot,image],labels)):
        plate.paste(im,(i*384,28),im)
        draw.text((i*384+6,8),label,fill='white')
    plate.save(base/'comparison.png')
    # SVG preserves fractional logical heights instead of distorting to64x69/32x35.
    sources=['inputs/source/south-neutral-original.png','pilot01.png','south-neutral.png']
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1152" height="560" viewBox="0 0 1152 560"><rect width="1152" height="560" fill="#283036"/>']
    for i,(src,label) in enumerate(zip(sources,labels)):
        x=i*384
        svg.append(f'<text x="{x+6}" y="18" fill="white" font-size="12">{label}</text><image href="{src}" x="{x}" y="28" width="384" height="416"/>')
        svg.append(f'<text x="{x+8}" y="464" fill="white" font-size="11">Native64 x69.333 / Half32 x34.667</text><image href="{src}" x="{x+24}" y="476" width="64" height="{416/6}"/><image href="{src}" x="{x+120}" y="476" width="32" height="{416/12}"/>')
    svg.append('</svg>')
    (base/'comparison.svg').write_text('\n'.join(svg)+'\n')
    owned,_=identity_inputs(model,base)
    before=np.array(pilot)
    actual=np.array(image)
    canonical=np.array(original)
    changed=np.any(before!=actual,axis=2)
    expected=before.copy()
    expected[owned]=canonical[owned]
    record=dict(status=model['status'],issue=245,preview=2,modelSHA256=sha(base/'garment.json'),
        outputSHA256=sha(base/'south-neutral.png'),policySHA256=sha(base/'identity-policy.json'),
        ownedPixels=int(owned.sum()),changedPixels=int(changed.sum()),changedOutsideOwnership=int((changed & ~owned).sum()),
        exactPredictedComposition=bool(np.array_equal(actual,expected)),
        exactCanonicalOwned=bool(np.array_equal(actual[owned],canonical[owned])),
        exactBaggyOutsideOwned=bool(np.array_equal(actual[~owned],before[~owned])),
        familyExpanded=False,hiddenRecovered=False)
    (base/'build.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':
    build()
