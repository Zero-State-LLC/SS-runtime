# Patrol cone outline

Read 2026-11-04 from `PatrolConeProjection` on `86c05bb`. No cone was changed.

The content range and half-angle stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). The integer cone stays in [patrol-sight-2026-11-04.md](patrol-sight-2026-11-04.md). `isUnaware` stays in [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md). The heading unit stays in [millidegree-2026-11-04.md](millidegree-2026-11-04.md).

`project` keeps living enemies with `isUnaware` and a patrol, sorted by id. A zero facing is omitted. The origin is the truncated position. `headingMilli` is `Cordic.atan2Milli` of the facing raw y and raw x. Range and half-angle are the content fields `sightUnits` and `sightHalfAngleMilliDegrees`.

The outline is a separate double cast. Its base is `atan2` of those same raw components. Its half-angle is `halfAngleMilli / 1000 * π / 180`. `rays` is 24, and the loop is `0...24`, so the arc has 25 samples. Each ray starts at `Double(rangeUnits)` and stops at the nearest solid entry among `liveSolids`. A ray that starts inside a box stops at once, because the entry is `max(0, near)`. Each point is `Int` of the rounded coordinate. The outline begins with the origin.

This does not replace `PatrolSystem.inCone`.
