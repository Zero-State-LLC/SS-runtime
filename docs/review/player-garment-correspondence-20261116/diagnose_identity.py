"""Record inherited identity discrepancy without changing pixels or weakening assertions."""
import json
from pathlib import Path
import numpy as np
import render

HERE = Path(__file__).resolve().parent
original = np.array(render.rgba(HERE/'inputs/source/south-neutral-original.png'))
upper = np.array(render.rgba(HERE/'inputs/layers/original_upper.png'))
target = np.array(render.rgba(HERE/'inputs/south-baggy-neutral.png'))
pilot = np.array(render.rgba(HERE/'south-neutral.png'))
opaque = upper[:,:,3]==255
mask = opaque & np.any(pilot!=original,axis=2)
rows = []
for y,x in np.argwhere(mask):
    rows.append(dict(x=int(x),y=int(y),original=original[y,x].tolist(),copiedUpper=upper[y,x].tolist(),trackedBaggy=target[y,x].tolist(),pilot=pilot[y,x].tolist()))
pre200 = np.any(pilot[:200]!=original[:200],axis=2)
report = dict(status='STRICT_ORIGINAL_FRAME_IDENTITY_FAIL_PRESERVED',opaqueUpperMismatchPixels=len(rows),
    pixels=rows,aboveGarmentRow200MismatchPixels=int(pre200.sum()),
    aboveGarmentMismatches=[dict(x=int(x),y=int(y),original=original[y,x].tolist(),copiedUpper=upper[y,x].tolist(),pilot=pilot[y,x].tolist()) for y,x in np.argwhere(pre200)],
    exactTrackedBaggy=bool(np.array_equal(pilot,target)),
    exactCopiedOpaqueUpper=bool(np.array_equal(pilot[opaque],upper[opaque])),
    bothOpaqueOriginalIdentity=bool(np.array_equal(pilot[opaque & (original[:,:,3]==255)],original[opaque & (original[:,:,3]==255)])),
    cause='Inherited copied upper composition differs from original frame at 157 pixels above garment row200, including two opaque-layer coordinates whose original alpha is 254. Not a UV-rasterizer change.',
    resolution='No original, test, or pilot pixel changed. Coordinator issue/review required before any new sample.')
(HERE/'identity-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
