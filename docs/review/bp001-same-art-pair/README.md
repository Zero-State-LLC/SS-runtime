# BP-001 same-art pair

Captured from the runtime renderer on a branch of `b141154`. Local Debug runs under Xcode 26.5, iPhone 17 simulator. The quiet plates, including their geometry, come from the run of both capture tests. The encounter geometry plates come from a later run of `testCaptureCameraFieldsInReplayableEncounter`. Both runs passed. This does not select a projection and it does not change the shipping mapping.

Viewport: 704×326 points. Native plates: 2112×978 pixels. Half sheets: 1056×489 pixels, a box downsample of the native plate. Gray sheets: the same native plate with saturation 0. The HUD stays in every plate.

## Quiet street

Uniform constrained building, street fixture, paired field, camera integrity 3.

| Plate | File |
|---|---|
| Shipping ground | `BP001-quiet-street-current.png` |
| Midpoint, 45° then half height | `BP001-quiet-street-midpoint.png` |

The building registration is the same in both. The older sheet in `docs/review/registered-shared-scene/comparison.png` changes that registration on the projected side.

| Geometry | File |
|---|---|
| Shipping ground | `BP001-quiet-street-current-geometry.png` |
| Midpoint | `BP001-quiet-street-midpoint-geometry.png` |

## Encounter

Seed 1, Ghost Step autopilot, tick 4976. Seven enemies, eight cameras. `registerServiceBuilding` is false, so the projected plate keeps the production building art. The visibility record is `BP001-encounter-visibility-100-same-art.json`.

| Plate | File |
|---|---|
| Shipping ground | `BP001-encounter-current.png` |
| Midpoint | `BP001-encounter-projected-100-same-art.png` |

| Geometry | File |
|---|---|
| Shipping ground | `BP001-encounter-current-geometry.png` |
| Midpoint | `BP001-encounter-projected-100-same-art-geometry.png` |

## Geometry

Magenta strokes are the solid rectangles. The cyan stroke is the player body circle (`PlayerBody.radiusUnits`). Shipping plates keep those rectangles axis-aligned. Midpoint plates run the same corners through the existing 45° then half-height mapping, so a rectangle reads as a diamond and the body circle reads as an ellipse.

On the encounter midpoint the strokes are drawn in scene space, above the actors. The upright sprites sit on `world`, over the ground chain, and would cover a stroke parented there. The visibility record is `BP001-encounter-visibility-100-same-art-geometry.json`.

Half sheets are 1056×489. Gray sheets are the same native plate with saturation 0.

## Still open

No recorded choice in `decisions.md`. World-south on the midpoint still reads down-right. Enemy sheets stay deferred.
