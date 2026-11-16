# Final roof completeness pass, November 16 09:52 UTC

**Current status at10:00 UTC: local technical checks PASS, final actual-image coordinator review pending.** The chronological red findings below remain evidence, not the current result. Coordinator opened runtime#246 and authorized the bounded repair at09:57 UTC. Final evidence is `final-roof-246-clean-copy.log` and `alpha-final-evidence.json`.

Coordinator authorized one final independent roof-prop layer at 09:50:58 UTC. No facade or building geometry change, no extra aesthetic pass. The first complete packet and preview are preserved under `attempt-01/`, with the earlier honest mesh-sampler failure still preserved separately under `attempt-01-before-sampler-fix/`.

## Editable source and limits

`inputs/roof-vent.png` and `inputs/roof-vent-provider.json` are byte-identical supplied originals. The actual PNG is 1254x1254 RGBA. It is a complete isolated **2.5D painted prop**, not a full 3D vent. No hidden vent faces, inferred volume or gameplay authority are claimed. `roof-layer.json` is its independently editable placement source. The building-only OBJ is intentionally unchanged and does not contain the painted layer. Layer export is `output/roof-layer-alpha.png`, registered on the common building canvas, with `output/roof-layer-registration.json`. Replay composites it over `output/building-alpha.png` for the fixed front projection. Reverse building diagnostic excludes the view-dependent prop.

Explicit authored registration, not alpha bounds:

| Field | Value |
| --- | --- |
| Vent source canvas | 1254x1254 |
| Vent source root | [684,1110], visually authored front-foot contact |
| Local world anchor | [78,85,132] |
| World anchor | [590,725,132] |
| Roof mesh z | 132 exactly |
| Uniform source-to-building pixel scale | 0.17 on both axes |
| Uniform source-pixel-to-world scale | 0.034 |
| Projected building root | [475.25126265847086,211.8539866664819] |
| Building-pixel layer origin | [358.97126265847083,23.15398666648187] |

The original building canvas1000x1200/root500,1160/scale5 remains sufficient without clipping this layer. Original foundation z0, world origin512,640, collider128x128, building mesh, OBJ/MTL, building-only pixels and registration are byte-identical to the pre-vent first sample. The vent's contact is on roof z132, not ground z0. No inferred gameplay footprint is added.

## Honest alpha findings awaiting resolution

The raw image has actual transparency: 1,025,198 pixels at alpha0 and substantial near-opaque paint, including 86,412 pixels at alpha252 and 431,845 at alpha253. Only256 pixels are alpha255. The new test premise requiring more than10% of the image to be exactly alpha255 is therefore not a valid test of true transparency. This assumption has **not** been silently relaxed. The coordinator was asked to record a defect before correction under the repository escalation contract.

Separately, the source contains three real alpha1 magenta residues at source(512,213), (873,919), (821,965), each RGBA(255,0,255,1). Premultiplied resampling leaves one output magenta pixel at(444,60), also alpha1. The strict no-magenta guard honestly fails. `inspect_alpha.py` produces exact full histograms and pixel coordinates in `alpha-first-evidence.json`. No geometry or root is inferred from these observations.

`roof-before-alpha-resolution/` retains the first layered output, renderer, config, tests, red log and alpha evidence. The initial clean-copy run passes all13 building tests and4/6 roof tests. It does **not** certify the final layer yet. Pending resolution is an explicit documented derivative-material residue correction with raw bytes preserved, plus an evidence-backed defect resolution for the incorrect exact255-opacity test. Do not call this initial layered output fully green.

The final source preview has been inspected at native/half logical size. Remaining visual limits are baked rather than geometric facade/steps, repeated facade paint, simple roof without parapet depth, and a small independently painted view-dependent vent rather than hidden complete geometry. No native scene, owner acceptance or production admission is claimed.

## 09:56 UTC diagnosis checkpoint, not green

An explicit derivative-material repair now replaces only the RGB channels of the three enumerated source residues with neutral127, leaving their alpha1 untouched and checking expected source bytes first. The derivative is `output/roof-vent-material.png`; the raw source remains byte-identical. `alpha-repair-evidence.json` independently confirms zero magenta in this derivative and an identical alpha histogram to the raw source. However, the 8-bit premultiplied Pillow bicubic sampler recreates the same alpha1 magenta output pixel. The unchanged strict guard still fails, retained in `roof-material-repair.log`. No further retry is made after this repeated failure without coordinator authorization. A floating-point premultiplied sampler is the proposed actual renderer repair, rather than dropping low-alpha pixels or weakening the no-magenta check. The separately incorrect exact255 test assumption still requires the recorded defect resolution.

## Issue246 authorized resolution, 10:00 UTC

Coordinator opened runtime#246 for the false exact255 premise and separate three-texel contamination, then explicitly authorized repair. The final normalization changes **only** these raw source texels in a derivative, never the immutable input PNG:

| Source coordinate | Before RGBA | Derived RGBA |
| --- | --- | --- |
| (512,213) | (255,0,255,1) | (0,0,0,0) |
| (873,919) | (255,0,255,1) | (0,0,0,0) |
| (821,965) | (255,0,255,1) | (0,0,0,0) |

Every other raw pixel is byte-identical. Normalization rejects unexpected residue count/coordinates, changed expected source values, or unapproved replacement values. `alpha-final-evidence.json` independently enumerates the exact three-texel diff. There is no blanket tolerance, alpha cutoff, inferred silhouette or geometry cleanup. The original and metadata pass direct byte comparison against the supplied files.

Separately, the layer sampler now uses floating-point premultiplied channels and bilinear convex interpolation instead of quantized8-bit RGBa bicubic interpolation. This prevents the renderer from manufacturing saturated alpha1 magenta through quantization/ringing. Ordinary final PNG alpha quantization is not a source-material cleanup threshold. No registration or building geometry changed. The output's strict no-magenta guard remains exactly the same and now passes. A mutation putting alpha1 magenta back into the output is rejected by that same strict predicate.

The invalid raw exact255-opacity premise is replaced, under issue246, by fixed raw SHA256 plus independently observed histogram counts, actual transparent background and near-opaque coverage. Mutations reject no-alpha RGB, flattened opaque RGBA, uniform alpha128, and uniform translucent paint with preserved transparent exterior. This corrects a false test assumption rather than relaxing a product threshold. No source pixel was made more opaque to satisfy the test.

`final-roof-246-clean-copy.log` records **13/13 base tests,9/9 roof-layer tests and actual OBJ/MTL roundtrip/mutation checks passing**, with no skips. The standalone replay reproduces all final export bytes. Tests verify actual roofZ132/root projection, uniform scale and live root/scale/z/material/removal mutations, exact3source-texel changes, no-magenta, genuine alpha, final composition, bounds and unchanged collider/building-only pixel/OBJ/MTL/registration hashes. Existing Pillow deprecation warnings are retained and are not hidden test failures. Final native/half plate was inspected after the repair. No native or production claim follows, and issue246 closure is left to the coordinator.

Open `output/comparison.png` for the final actual-image review. Remaining deficits: baked facade/step relief, repeated facade source, planar roof without parapet depth, view-dependent2.5D ventilator without hidden mesh, and no coherent native scene evidence. The building-only OBJ intentionally excludes the prop. The source layer/config and full registered layer export are delivered separately. Stop visual edits here.
