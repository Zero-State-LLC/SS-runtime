# BP-001 same-art pair

Captured from the runtime renderer on a branch of `b141154`. Local Debug run of `BenchmarkCaptureTests` under Xcode 26.5, iPhone 17 simulator. Both tests passed. This does not select a projection and it does not change the shipping mapping.

Viewport: 704×326 points. Native plates: 2112×978 pixels. Half sheets: 1056×489 pixels, a box downsample of the native plate. Gray sheets: the same native plate with saturation 0. The HUD stays in every plate.

## Quiet street

Uniform constrained building, street fixture, paired field, camera integrity 3.

| Plate | File |
|---|---|
| Shipping ground | `BP001-quiet-street-current.png` |
| Midpoint, 45° then half height | `BP001-quiet-street-midpoint.png` |

The building registration is the same in both. The older sheet in `docs/review/registered-shared-scene/comparison.png` changes that registration on the projected side.

## Encounter

Seed 1, Ghost Step autopilot, tick 4976. Seven enemies, eight cameras. `registerServiceBuilding` is false, so the projected plate keeps the production building art. The visibility record is `BP001-encounter-visibility-100-same-art.json`.

| Plate | File |
|---|---|
| Shipping ground | `BP001-encounter-current.png` |
| Midpoint | `BP001-encounter-projected-100-same-art.png` |

## Still open

No authoritative-geometry overlay. No recorded choice in `decisions.md`. World-south on the midpoint still reads down-right. Enemy sheets stay deferred.
