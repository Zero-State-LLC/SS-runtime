# Enemy spark

Read 2026-11-04 from `VFXRenderer.spark` on `e4ff026`. No hit amount was changed.

The frame lifetime stays in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md). The angle step stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

`enemyHit` is drawn at the source actor, or at the player when that actor has no known position. Reduced motion or reduced flash draws one circle of radius 20, white 0.96 at alpha 0.9, line width 2.

Otherwise each of the variant's particles is a 3 by 3 square of that colour. Its direction is the shake note's angle step times the index, plus the point's x times 0.01. It travels 16 along that direction and fades over the presentation lifetime.

This does not change a hit amount.
