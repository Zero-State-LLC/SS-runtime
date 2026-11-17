# Corrected project facts

## November 17, 2026: V9 architectural scale is still awkward

At00:53:58UTC the owner identified the building with the Camera in front as awkwardly sized, explicitly as an example. Treat architectural scale/proportion as a scene-level review concern, not merely the already-recorded base/curb material defect. V9 is not accepted.

The owner did not specify a shrink/enlarge percentage or say whether the whole building should be uniformly smaller or larger. Do not invent that instruction. Coordinator inspection of the actual V9 zoom1.4 half capture confirms the relevant kiosk has a substantial roof/cornice mass, a tall doorway and large facade panels immediately beside the Camera pole. Their shared visual scale requires review against the Player and surrounding frontage. This is a visual assessment, not a measured real-world scale claim.

The kiosk remains bound to the128x128 authoritative rectangle in `building-perspective-detail-20261116/kiosk/baseline_renderer.py:17-26`; `building-perspective-detail-20261116/scene/native.py:100-132` checks projected ground correspondence. Those checks do not establish believable architectural proportions. Uniformly shrinking the existing sprite would break its current contact registration. Recommend an untextured architectural proportion comparison before more detail, changing source geometry rather than stretching the image. Any required footprint/collision or Camera/Player authority change remains separately gated. No new art attempt or wider work order is approved by this feedback alone.

## November 16, 2026: V7 footprints remain inconsistent

At22:50UTC the owner corrected the V7 review: footprints are inconsistent. V7 is not accepted. Do not describe the building footprints as corrected or coherent based on registration tests alone.

Those tests validate declared authoritative rectangle corners under D108. They do not establish consistent visible architectural contact contours, setbacks, pavement/road relationships or prop placement. Kiosk registration explicitly includes one virtual chamfer-omitted corner, not a visible contact vertex. Context uses full rectangular plinths. The distinction must remain explicit.

Read-only diagnosis in `docs/review/footprint-consistency-20261116/` confirms the retained ground layout is independently authored at curb x800/y600. Whole canonical footprints overlap painted road: residential-west41.015625%, civic-west63.5416667%, civic-dais100%. Percentages include offcrop portions and describe decorative ground material, not changed gameplay walkability. Retained tree root[858,780] lies inside civic-west bounds[736,768]..[928,1152]. These concrete mismatches do not claim to explain every perceptual footprint problem.

Preserve V7 sources/captures/validators unchanged. The prior pass's requirement to keep non-building sources and prop roots fixed prevents a complete ground/prop consistency repair within that same scope. A coordinated presentation-only building/ground/prop work order must be explicitly approved before that broader repair. Collision, Camera field/root, Player root, controls and production admission remain separately gated.
