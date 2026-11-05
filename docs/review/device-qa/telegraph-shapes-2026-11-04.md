# Telegraph shapes

Read 2026-11-04 from `TelegraphProjection` and `WorldRenderer.renderTelegraphs` on `006304e`. No telegraph length was changed. The attack table stays in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md).

Boss shapes are projected while a runtime exists, `currentAttack` is set, `telegraphRemaining` is above 0, and a living `algorithmicModerate` exists. The origin is the boss position truncated to units. The heading is `Cordic.atan2Milli` of the player position minus that origin, in raw Q8, computed on the call. Safety Rationale, Narrow Tailoring, and Independent Review set `locked` when `telegraphRemaining` is 1. The heading stored on that call is the heading just computed.

Safety Rationale is one cone. The half-angle literal is 35_000, the range literal is 260, the width is 0, the total is the literal 45, and the key is `boss-safetyRationale`. The renderer draws a cone with field angle `half * 2`.

Narrow Tailoring is three lanes. The offsets are the literals −12_000, 0, and 12_000, added to the heading and then normalized. The width is the radius literal 7 times 2. The range is `projectileReach(420, 72)`, a half-away of speed times lifetime over 60. `CombatVisibilityTests` expects 504. The total is the literal 30.

Temporary Order sets `locked` true. An empty emitter list produces no shape. Otherwise the shape is `emitters[emitterIndex % count]`: the emitter's position, heading, and range, and the half-angle is that emitter's field angle divided by 2. The preview reads the index. The total is the literal 48. The key includes the emitter id. The renderer draws it with the cone path, so the drawn field angle is that half times 2.

Independent Review draws one lane per heading `BossSystem.independentReviewLanes` returns for the player heading. The width is the radius literal 7 times 2. The range is `projectileReach(360, 90)`. The same test expects 540. The total is the literal 60.

Elite shapes are living enemies in `dashTelegraph`, sorted by raw id. Query telegraph has no shape here. Each lane heads toward the player, with width literal 72, remaining `stateTicks`, and total literal 36. `locked` is `stateTicks` at or below 1. The range is `projectileReach` of `dashSpeed` and `dashTicks` 30. `dashSpeed` is the literal named in [daemon-query-2026-11-04.md](daemon-query-2026-11-04.md). The same test expects that reach to be 144.

`progressPermille` is 1000 when the total is 0. Otherwise it is a half-away of the elapsed ticks times 1000 over the total. Elapsed is the total minus the remaining, and a negative elapsed is 0. The fill alpha is 0.42 when locked, and `0.10 + 0.22 * progress` otherwise. The line width is 4 when locked and 2 otherwise. Half-away stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).
