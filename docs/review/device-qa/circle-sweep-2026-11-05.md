# The circle sweep

Read 2026-11-05 from `Collision.sweepCircleTime` and `Simulation.resolveDamage` on `ef68565`. No radius was changed. The hit sort stays in [hit-order-2026-11-04.md](hit-order-2026-11-04.md). Wall entry stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md). Half-away stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md). The discriminant and `isqrt` stay in [integer-roots-2026-11-05.md](integer-roots-2026-11-05.md).

The move is `to − from`. The offset is `from − target`. The combined radius is `(radius + targetRadius) * Q8.scale`. `a` is `mx² + my²`, `b` is `2 * (dx * mx + dy * my)`, and `c` is `dx² + dy² − r²`.

`c <= 0` returns 0. `a == 0` returns nil. A nil discriminant returns nil.

The first numerator is `-b − isqrt`. When that numerator is negative, the other root `-b + isqrt` is used. If that other numerator is negative, the function returns nil: `c` already returned when it was at most 0, and `c` is not written again. Otherwise the time is `mulDivHalfAway` of that numerator, `Q8.scale`, and `2 * a`. A time inside `0...Q8.scale` is returned. A time outside that range returns nil for the same reason.

When the first numerator is not negative, the time uses that numerator. A time below 0 returns nil. A time above `Q8.scale` returns nil. A time inside the range is returned.

`resolveDamage` records a civic pulse or a ricochet against a living enemy at the enemy radius, and against a damageable camera at `targetAnchor` with `hitRadius`, skipping an id already in `hitEntityIds`. A sutro bolt or a boss bolt records a player hit at `PlayerBody.radiusUnits`.

This does not change a radius.
