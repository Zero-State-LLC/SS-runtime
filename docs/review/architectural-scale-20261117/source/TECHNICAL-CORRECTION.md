# Technical correction record

The initial `attempt-01-ground-uv/output/` is a failed compositing result, not a second aesthetic option. All initial files and the passing-but-incomplete first test log are retained. Do not publish that output as the candidate.

## Ground UV defect

Both coordinator inspection at zoom1.4 and source-worker inspection at zoom1 exposed black aprons and misplaced small pavers. The initial compositor incorrectly mapped all4608 square source pixels into the2304x1536 ground node. That compressed source Y by two thirds.

Authority: `AppTests/BlockedBaseCurbSceneTests.swift:308-313` passes square `tileUnits=2304`, and `App/WorldRenderer.swift:461-464` selects texture rect `[0,0,1,2/3]` before constructing the arena-sized node. Correct source pixels are `u=2*worldX`, `v=4608-2*worldY`, not `v=4608*(1-worldY/1536)`.

The first correction changed only source sampling, raw frame packaging and proxy-omission disclosures. Its14-test result checked all ten mesh rasters against the initial failure. Those rasters still contained the separate context normal defect below. Geometry, proposal Z maps, flat color classes, actor transforms and depth authority remain unchanged across all three technical render states.

## Frame packaging defect

Initial named scene frames included a30-pixel external label band. Corrected `current-zNNN.png` and `proposed-zNNN.png` are raw2112x978 frames with exactly704:326 aspect. Labels live in `*-labeled.png` or comparison sheets, not in raw frames.

## Explicit context normal defect

Independent coordinator inspection at zoom1 and source-worker convention audit found context roofs missing. The context source stores explicit outward normals with clockwise face winding. All927 residential-west,881 residential-north,584 civic-west and310 dais faces have normals opposite their cross-product winding. `context/replay.py:57-58` uses `face['normal']` as authority. The generic adapter incorrectly applied the kiosk cross-product convention to context faces, culling roofs and exposing interiors.

The corrected-ground intermediate output, implementation and14-test log are retained in `attempt-02-face-normals/`. Final adapter uses explicit normal metadata whenever present, falling back to cross-product only for kiosk faces. No mesh coordinate, topology, map, flat material class or scene authority changes. Context pixels necessarily change because actual outward faces now render. Kiosk mesh rasters, all geometry documents, dimensions, registrations, Player/Camera layers and corrected ground remain byte-identical.

Independent roof-interior sample tests cover all five meshes in both arms, and every context face is checked for retained explicit-normal selection and culling. `tests-normal-regression-before.log` demonstrates the new roof test fails on the preserved intermediate. Issue255, filed by coordinator, records both validator gaps. This is a second distinct technical defect, not a second aesthetic proposal or failed repeat of the UV correction.

## Independent roof probe correction

The first final-normal test run passed15/16 checks. The remaining assertion incorrectly expected the proposed dais center pixel to show the platform. At source pixel `[284,207]`, the pixel-center projection is `u=1/6,v=53/6`. Intersecting that ray with top-rail plane `z=35` gives a point inside the unchanged south rail rectangle `x=-71..71,y=-39..-37`. The rendered cornice pixel is correct. The probe, not geometry or rendering, was defective.

The red test and log are preserved in `probe-failure/`. The roof sample moves to the independently clear platform point `[0,5,9]`. An additional analytic ray/rail intersection test now requires both the old occluded pixel to remain cornice and the clear pixel to remain roof. No image or renderer bytes change for this test-fixture correction. Coordinator was notified to include it in issue255.

## Proxy boundary

The source compositor omits native HUD/touch controls, runtime Player shadow and raster-only kiosk roof vent. HUD/control authority and native visibility remain in the record, not claimed to be reproduced visually. Camera field path uses retained inputs and clipping, while its fill/antialiasing is proxy-only. Source filtering is Pillow rather than SpriteKit. The immutable V9 native panes retain actual native rendering and controls.

## Coverage correction

The initial12 tests validated compositing self-consistency but not the independent square-ground UV contract. New direct tests require source pixels for five known world points and assert crop rectangle, raw scene aspect and retained authority. This strengthens checks rather than weakening assertions to match the defect. The initial test log remains evidence of the coverage gap.
