# Patrol sight

Read 2026-11-04 from `PatrolSystem.inCone`, `sees`, and `member` on `aaa7919`. No route was added. The content half-angle and the 45000 pair stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). The first special tick stays in [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md). The line of fire stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md).

A zero facing sees nothing. The range is inclusive: squared distance at most the cone range squared. The facing dot the offset must be above 0. The angle test is `denominator · dot² ≥ numerator · |f|² · |d|²` on exact 128-bit products. The pair is `cosineSquared`. Decode accepts 30_000 as (3, 4), 45_000 as (1, 2), and 60_000 as (1, 4). Any other half-angle is refused. Line of sight is a separate test.

`sees` requires a patrol state, then `inCone` from the member position along `patrol.facing`, and a clear line of fire.

`member` places the body at the first waypoint, in Q8, with velocity zero. The target index is `1 %` the waypoint count, and dwell is 0. Facing is the integer vector from the first waypoint to the second, stored as Q8. Equal waypoints give a zero facing. Awareness starts unaware. Integrity is `hp * integrityPercent / 100`, truncating. The encounter id is `patrol:` plus the route id. No encounter, heat rule, or completion count names that id. `nextSpecialTick` uses `firstSpecialTick`.

On tick 1, each arena patrol route whose archetype has standard stats spawns one member at the content integrity percent. A tick whose outcome is already failure skips `advanceEncounters`, so that tick spawns none.

This does not add a route.
