# BP-002 / BP-008 boot attachment study

Status: REJECTED_FOR_SOURCE_INTEGRATION. Not runtime artwork.

## Current authority

Reviewed SS-specs 492d921027c11d809ff18e3a35f520118e13de84, especially controlled-character-source.md and benchmark-production.md BP-002/BP-008. These already require elevated key poses, authored heel/toe contacts, source-space versus projected-space distinctions and actual world-travel evidence. No further product behavior is needed to attempt this source study. Runtime is a325cad; production sprites and contracts are unchanged.

## Research

Animation Mentor, [Animating Dynamic Run Cycles](https://www.animationmentor.com/blog/animating-dynamic-run-cycles/), retrieved 2026-10-14, recommends motion reference and blocking stride, down, mid-stride and push-off poses, distinguishing running by airborne intervals. This supports reviewing support and flight separately. It does not establish SS's camera elevation, support duration, stride length, contact geometry or an acceptable slip threshold. No video was inspected in this turn.

## Experiment and disposition

Built-in imagegen, using the retained south neutral as the sole costume/view reference. Requested one anatomical right boot in planted, toe-supported push-off and lifted recovery poses, from one elevated front camera. Exact prompt is in prompt.txt. Raw generation is retained in candidate.png.

OBSERVED visual review: the first two boots retain nearly the same front silhouette, without a sufficiently legible heel-lift relationship. The third is substantially smaller and lacks lower-leg context to distinguish perspective foreshortening from scale drift. All three show open cuffs; they are isolated boot illustrations, not evidence of coherent ankle attachment. The output cannot establish planted or lifted ground contact. No automatic image metric was used to overrule this visual failure.

Disposition: do not crop, normalize or stretch these into approved attachment variants. Do not update rig.json, active textures, animation metadata, or admission records. Preserve the original source and its boot overlap work.

## Next source action

Block the SOUTH lower-leg chain in contact, loaded support, push-off and recovery before painting more attachment variants. Show knees, ankles, a ground plane and explicit proposed contact points in the same view, with retained-character scale alongside. This is an authored geometry/pose experiment, not a reconstruction of hidden anatomy from the neutral raster. Verify the selected pose actually changes visible surfaces, then paint those surfaces using the original material. Compare both anatomical sides without mirroring asymmetric equipment.

Only after those keys preserve anatomy, costume and contact readability should the south 16-frame cycle be in-betweened. Maximum travel remains 240 units/second and the initial cycle remains 0.5 seconds; actual runtime positions, including stopped/colliding motion, remain the BP-008 authority. No new support interval, projection angle or gait policy was selected here.

## Verification scope

Original neutral SHA-256: see provenance.json. Candidate alpha and file hash recorded there; alpha is storage evidence only. This change contains a review image, prompt, provenance and this note. It does not change executable code or production resources. Existing core result: 773 tests passed at f724a50, documented in docs/review/projected-motion/core-tests.log; not rerun or claimed as art validation. Full benchmark, camera, environment, four-facing animation, world-travel and device gates remain open.
