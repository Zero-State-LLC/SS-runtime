# Camera shatter

Read 2026-11-04 from `VFXRenderer.cameraShatter` on `e4ff026`. No camera integrity was changed.

The destruction record stays in [camera-destruction-record-2026-11-04.md](camera-destruction-record-2026-11-04.md). The angle step stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

`cameraDestroyed` is drawn at the camera, or at the player when that camera has no known position. Reduced motion or reduced flash draws a crack through (−10, 9), (−2, 1), (−5, −4), and (6, −11), plus a branch from (−2, 1) to (9, 6). The stroke is red 0.70, green 0.88, blue 0.98, at line width 2. A bar 34 by 3, red 0.9, green 0.7, blue 0.1, alpha 0.8, is rotated by −π/5.

Otherwise a broken ring of radius 12, 5 segments, in the crack colour, line width 3, scales to 3.4 and fades over the lifetime. The caps are round. Each segment draws 0.62 of its share of the circle. Six triangles, filled with that colour and unstroked, travel 46 along the angle step plus 0.4, spin one full turn, and fade over the second half. Each of the variant's particles is a 2.5 square, red 1, green 0.80, blue 0.35. Its reach is 40 plus `(index % 3) * 14`, over 0.8 of the lifetime.

This does not change a camera's integrity.
