# Enemy separation

Read 2026-11-04 from `Steering.applySeparation` on `fcab4e5`. No speed was changed. Patrol arrival and drift stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md).

Two living enemies separate when the distance between them is inside the sum of their radii plus 8. The comparison is on squared distance. A distance of 0, and a distance at that combined radius, are left alone.

The push is applied to the enemy with the lower id. That enemy adds the raw offset away from each higher-id neighbor. The added step is a half-away move of one quarter of its full speed, with that quarter truncated, along the combined offset. The velocity is then clamped to that full speed.

An aware enemy does this after it has chosen a velocity, and before the circle slide. An unaware enemy that is still moving toward a goal does this as well, and then clamps again to the scaled patrol speed it was already using. An unaware enemy that is holding still does not separate.

This does not add a steering rule.
