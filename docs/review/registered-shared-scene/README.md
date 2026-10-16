# Registered shared camera scene — BP-001/BP-004/BP-007

## Scope and authority

Specification d859658 already requires shared projection, separate ground/upright transforms, source registration and native-scale comparisons. This work repairs a regression in the newer shared camera fixture relative to the earlier constrained-building study; it does not select a production projection or admit new artwork. Runtime baseline 0404685. Issues #128 (fixture mapping) and #129 (coordinate assertion precision) retain the defects.

## Change

The old control uses the 1254×1254 building source in a 190×217 box with a bottom-center anchor. Each new registered capture instead uses the documented uniform scale, square canvas, and source near-corner (653,1152), mapped to the existing 128×128 obstacle's minimum-x/minimum-y corner. It reuses the earlier 45-degree ground rotation with one-half vertical compression at unchanged zoom. Ground, field path and contact shadows share that transform; upright Player, complete Camera, building and two props preserve their form. HUD and view camera remain outside the world transform. Every capture restores the tree before another state is rendered.

This is an explicitly placed, paused composition fixture. The camera's field origin/heading are fixture placements; it is not the authoritative seed-1 encounter and must not be cited as detection-registration proof. The separate camera-registration evidence supplies that proof. Control and registered images cover integrity 3, 2, 1 and 0 with existing/dark/paired contours. No collider, replay, controller, shipping art or projection changed.

## Observed visual result

The registered building and paving now share the projected direction, and the source is no longer stretched. Upright sources retain their shape. The complete municipal Camera remains a single device across damage states. Remaining shortcomings include harsh Player outline, repetitive plain paving, no continuous curb/road/rail composition, scale/framing review, and the previously documented small building-source/base mismatch. The scene is not final benchmark acceptance. Live traversal, encounters, occlusion, full animation and device performance remain required.

## Research basis

Apple's [About SpriteKit Coordinate Systems](https://developer.apple.com/documentation/spritekit/about-spritekit-coordinate-systems) and [SKNode](https://developer.apple.com/documentation/spritekit/sknode) describe parent-relative positions and inherited transforms. Accessed 2026-10-14. These support the implementation mechanism, not the aesthetic angle: the projection is the existing BP-007 authored comparison candidate.

## Verification

The initial run exposed exact comparison of Float-rounded SKNode positions with unrounded Double arithmetic. Its exported evidence is preserved under failed-precision; it is not a passing run. The corrected assertion retains exact equality after explicit conversion to the observed stored precision, alongside separate 0.0001 ground-coordinate checks. No authoritative geometry is altered to satisfy it.

Final run: Test-SSRuntime-2026.10.14_23-15-22--0700.xcresult, 106 executions, no failures, one existing EnvironmentLibrary nonthrowing-try warning. Focused CameraPresentationTests: 3 passed, exit 0. No core implementation changes; no fresh full-core claim. Source and output resolution remain unchanged.
