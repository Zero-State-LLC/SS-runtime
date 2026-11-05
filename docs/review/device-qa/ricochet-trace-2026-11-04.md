# Ricochet trace

Read 2026-11-04 from `VFXRenderer.ricochetTrace` on `e4ff026`. No continuation rule was changed.

Who continues stays in [ricochet-continuation-2026-11-04.md](ricochet-continuation-2026-11-04.md). One world unit stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

The projector skips the `ricochet` recipe on the event walk. It emits one presentation when a projectile has exactly two hits on the tick, the first kind `civicPulse` and the second kind `ricochet`, the same projectile id, and two different targets. The trace points are those two impact points, the civic-pulse impact and then the ricochet impact, raw divided by the Q8 scale.

When reduced motion and reduced flash are both off, and there are at least two points, the path is those points dashed with lengths 8 and 6. The stroke is white 0.92 at alpha 0.85, line width 2, and it fades over the presentation lifetime.

Each point, up to the variant's particle count and at least one, draws an X from (−4, −4) to (4, 4) and from (−4, 4) to (4, −4), in that same stroke. When the motion is not reduced, marker `i` waits `i * 0.03` seconds and then fades over the lifetime.

This does not change a continuation.
