# Enemy burst

Read 2026-11-04 from `VFXRenderer.burst` on `e4ff026`. No defeat rule was changed.

The defeat clip stays in [reaction-clips-2026-11-04.md](reaction-clips-2026-11-04.md). The angle step stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

`enemyDefeat` is drawn at the source actor, or at the player when that actor has no known position. Each of the variant's particles is a square of white 0.70 at alpha 0.9. Reduced motion or reduced flash uses size 5 and a reach of 8. Otherwise the size is 4 and the reach is 34. The direction is the shake note's angle step times the index. The square travels that reach and fades over the presentation lifetime.

This does not change a defeat rule.
