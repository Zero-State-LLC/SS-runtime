# Patrol near miss

Read 2026-11-04 from `PatrolNearMiss` on `86c05bb`. No cone was changed.

The content range and half-angle stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). `inCone` and `sees` stay in [patrol-sight-2026-11-04.md](patrol-sight-2026-11-04.md). The drawn outline stays in [patrol-cone-outline-2026-11-04.md](patrol-cone-outline-2026-11-04.md).

A member is living, has a patrol, has a nonzero facing, and its awareness is not `.aware`. The wide spec is a copy of the content patrol with `sightUnits` set to `sightUnits * 5 / 4`, integer multiply then divide. The id qualifies when `PatrolSystem.inCone` with that wide spec is true and `PatrolSystem.sees` with the content spec and `liveSolids` is false. The ids are sorted.

`edgeIntensity` returns 1 when reduced motion is on. Otherwise it is `0.8 + 0.2 * cos((frame % 60) / 60 * 2π)`. `NearMissEdgeLayer` strokes the member's outline at line width 3, colour red 0.85, green 0.95, blue 1, and sets the alpha from that intensity. Its z position is the camera-field layer plus 0.5.

This does not change the content cone.
