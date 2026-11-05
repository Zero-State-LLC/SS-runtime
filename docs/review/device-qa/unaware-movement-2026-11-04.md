# Unaware movement

Read 2026-11-04 from `EnemySystem.moveUnaware` on `aaa7919`. No speed was changed. Dwell, arrival, the stop distance, and the drift percent stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). Separation stays in [enemy-separation-2026-11-04.md](enemy-separation-2026-11-04.md). The slide stays in [circle-slide-2026-11-04.md](circle-slide-2026-11-04.md). Half-away stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

A patrol with a missing route index, or an empty route, sets velocity to zero and returns. Arrival is a squared distance to `route[target]` at most `arrivalUnits` times the Q8 scale, squared. When dwell is 0 and the member has arrived, a positive dwell sets `dwellRemaining` to that dwell, and a zero dwell advances the target modulo the route count. A zero dwell can still move on that tick. A remaining dwell then decreases by 1. The tick that decrease reaches 0 advances the target modulo the route count, stores the patrol, sets velocity to zero, and returns. The arrival tick both sets the dwell and decreases it. A dwell already in progress runs out on its own while the member is still inside the arrival radius.

With no patrol, a missing trigger centre sets velocity to zero. A squared distance to the centre at most the stop distance times the scale, squared, sets velocity to zero. Otherwise the goal is the centre and the percent is the drift percent.

The speed is one half-away of `unitsPerSecond * percent * Q8.scale / (60 * 100)`. The step steers toward the goal at that speed, applies separation, clamps to that speed, and slides. A patrol whose slid travel is nonzero stores that travel as its facing. The position becomes the slid point.

The enemy step calls this when `isUnaware` is still true and the movement data is present, then continues, so the outer separation and slide run only inside this call. The alert pass has already turned a `struck` enemy into `aware`. An enemy alerted this tick sets velocity to zero and skips the state machine. Without the movement data, an enemy still on this branch holds.

This does not change a speed.
