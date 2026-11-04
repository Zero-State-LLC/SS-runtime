# Camera follow

Read 2026-11-03 from the runtime sources on `3e32d76`. No follow number was changed. Shipping projection stays `(x, -y)`.

`GameScene` moves `cameraNode` with `CameraFollow`. The first update snaps to the player. After that, the anchor stays inside a dead zone of 76 by 50 world units, so half-widths are 38 and 25. Look-ahead is 48 units along the player's facing when that facing has length. The target eases toward the anchor plus that look-ahead. The gain is `1 - exp(-dt / 0.12)`. `dt` is the display interval, clamped to the range 0 through `1/30`. A non-finite interval contributes 0. The result is clamped so the 704 by 326 view stays inside the arena bounds.

The presentation snapshot frames the HUD with `PresentationCamera.follow`. That path has no dead zone and no easing. Look-ahead is 48 on the facing's x sign, and 0 when the facing is zero. Y is the player's y. The same 704 by 326 view is then clamped inside the arena. `visibleWidth` is 704 and `visibleHeight` is 326. `maxLookAhead` is 76, and the applied look-ahead is the minimum of 76 and 48.

The camera node position is that follow position plus this frame's screen shake. Shake lasts 12 display frames. The offset amplitude is `peak * remaining / 12`. A new shake takes the larger of the current amplitude and the requested one, and it does not add them. The cap is 6. Reduced motion clears the shake.

| Recipe | Amplitude |
|---|---:|
| `playerHit` | 3 |
| unlisted recipe | 3 |
| `cameraDestroyed` | 4 |
| `lockdown` | 5 |
| `bossPhaseBreak` | 6 |

The offset direction is `frame * 2.399963` radians. The HUD is a child of the camera node, so the shake does not move the HUD on screen.

This does not change the camera, and it does not record BP-001.
