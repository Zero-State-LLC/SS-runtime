# Decoration turn

Read 2026-11-05 from `WorldRenderer.renderDecorations` on `344ed78`. No decoration was moved.

The scale and the centre anchor stay in [decoration-placement-2026-11-02.md](decoration-placement-2026-11-02.md). The heading negation stays in [heading-draw-2026-11-04.md](heading-draw-2026-11-04.md).

A missing `rotationMilliDegrees` is 0. A zero turn leaves the sprite's rotation alone. Any other turn is that milli-degree value divided by 1000, in degrees, then converted to radians. Positive is counter-clockwise.

The group is built once. It latches when a sprite was added, or when the list is empty. A non-empty list whose textures all miss does not latch, so a later frame can try again.

This does not move a decoration.
