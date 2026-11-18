# Live midpoint adapter implementation

Owner-approved scope: `intent/2026-11-17-live-world-projection.md`. No source-art or authority edits. This is DEBUG-only, opt-in, unaccepted presentation.

## Design

`LiveWorldProjection` wraps renderer root and VFX world root in a45degree rotation followed by0.5vertical scale. This is the existing midpoint map about world origin. Projecting camera follow through the same map makes screen-relative positions equivalent to projection around the followed center. Screen-space camera children, including HUD and screen effects, are excluded.

Renderer explicitly lists upright cohorts: actor and housing roots, audited upright decorations, static building textures, the whole kiosk source group, gate tile artwork, and unaware markers. Ground surfaces, retained foundations, fields, telegraphs, shadows, query markers, projectile paths, gate strips, combat-feedback geometry, court rings and world VFX remain under the one ground chain. Damage/unaware badges preserve local screen offsets from their registered actor root. Existing upright textures, anchor points, sizes, rotations, scales and child offsets are unchanged. Kiosk base remains inside its already-composed source group and is not projected twice.

At update entry, restore upright parents/positions/depth and camera to authoring coordinates and set the chain to identity. Renderer and SpriteKit actions execute there. Post-action outline synchronization and existing playback observation run before applying projection. Then lift the explicit uprights to an untransformed sibling layer, project their registered root once, project the camera once. Redraws outside the update/action interval restore and reapply immediately, including paused redraw. Restart restores before clearing nodes. Toggle/remove and view teardown restore the original tree. No action or animation is intentionally reset by the adapter.

Manual touch commands only are inverse-mapped and normalized to their incoming magnitude, after existing deadzone processing. Dodge and touch layout are unchanged. The existing autopilot branch supplies world commands directly and bypasses this mapping.

## Launch route

Use the fresh built Debug app and the canonical absolute existing kiosk resource directory. Add `-SSKioskProjection midpoint` to the existing valid current/candidate review flags. Absence keeps the previous ordinary playable mode. Malformed/duplicate projection flags or projection without a review request reject before installing art. Loaded resource validation still verifies all existing source hashes and authority bounds.

```sh
xcrun simctl launch --terminate-running-process CACB3927-A76E-43A5-9ACA-C389EB38C0C3 com.zer0state.surveillancesurvivor -SSMute -SSAutopilot run -SSKioskReview candidate -SSKioskReviewRoot "$PWD/docs/review/kiosk-only-geometry-20261117/native/playable/resources" -SSKioskProjection midpoint
```

The ordinary legal pilot route is not a seeded screenshot shortcut. Keep visible NOT ACCEPTED and MIDPOINT status. Asynchronous current/candidate screenshots are not matched-tick image equivalence. Original art may still have registration or occlusion defects, and projection tests are not visual acceptance.

## Validation plan

New `LiveWorldProjectionTests` independently checks analytic geometry, inverse input direction/magnitude, flag gating, unchanged upright local shapes/source identities, retained foundations, world effects versus HUD, exact120tick digest/snapshot parity, pause/redraw/restart/toggle/removal, and real SKView update/action/post-action callbacks with changing delivered textures. Prior8`KioskPlayableReviewTests` remain byte-unchanged. Build/native/Release results are recorded separately as executed, never inferred from this plan.
