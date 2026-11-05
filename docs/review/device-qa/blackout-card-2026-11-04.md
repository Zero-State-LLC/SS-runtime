# Blackout card

Read 2026-11-04 from `VFXRenderer.blackout` on `e4ff026`. No camera count was changed.

The HUD line stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The music drop stays in [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md). The display polygon stays in [camera-field-polygon-2026-11-04.md](camera-field-polygon-2026-11-04.md). A full-screen white flash stays forbidden in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md).

The title is the presentation label. The projector sets that label to `NETWORK BLACKOUT`. It is Menlo Bold, size 34, red 0.96, green 0.96, blue 0.96, centred, at y 40, on the screen effect layer.

Reduced motion or reduced flash draws a banner 420 by 52 behind that title. The banner fill is white 0.05 at alpha 0.85. Its stroke is the title colour at line width 1. No dim is added.

Otherwise a black sprite, 1.2 times the visible width and height, fades to alpha 0.5 over 0.3 of the lifetime, holds for 0.45 of the lifetime, and returns to 0 over 0.25 of the lifetime. The title fades in and scales from 1.25 to 1 over 0.12 seconds, waits 0.6 of the lifetime, and fades out over 0.25 of the lifetime.

Each cascade step whose camera is still in the snapshot draws `conePath` from that camera's range, heading, and field angle, at the camera's point. The fill is red 0.9, green 0.7, blue 0.1, alpha 0.16. The stroke is red 0.95, green 0.75, blue 0.15, alpha 0.7, at line width 1.5. The cameras are the unique ids, sorted by raw id. The wait, in milliseconds, is the lifetime in milliseconds times the index, divided by that count. The field then fades to 0 over 0.06 seconds. The first wait is 0.

This does not change the camera count.
