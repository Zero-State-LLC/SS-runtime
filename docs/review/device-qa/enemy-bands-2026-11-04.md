# Enemy steering bands

Read 2026-11-04 from `EnemySystem.think` on `fcab4e5`. No speed or range was changed.

Content speeds, ranges, and specials stay in [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md). The approach point is the player position when `Collision.lineOfFireClear` is true, and the corner waypoint otherwise. `think` decrements `stateTicks` first, floored at 0. While the state is `telegraph` and ticks remain, velocity is zero and the band below is not reached.

The informant always steers toward the approach point.

The fog cloud, when the telegraph count has reached 0, applies the pulse from the stats note when the player is inside that range and the line is clear, then enters cooldown either way. When the tick has reached `nextSpecialTick` and the state is not telegraph, it enters telegraph and leaves velocity as it stood. Otherwise, squared distance greater than 210² × `Q8.scale`² pursues the approach point, and the remaining distance orbits the player. 210 is a code literal.

The cable correlator starts a telegraph when the tick has reached `nextSpecialTick`, squared distance is within 240² × `Q8.scale`², and the line is clear. 240 is a code literal. That branch sets velocity to zero. When the telegraph reaches 0, `lockPosition` becomes the player position and the charge steers toward the player at `charge.speed`. Later charge ticks keep that velocity. A charge whose slide stays on the same point, with velocity still set, enters recover, uses the content recover length or 45 when the charge record is absent, and sets velocity to zero. A recover that finishes sets the state to pursue and schedules the next telegraph after the cooldown. Otherwise the correlator pursues the approach point.

The witch uses the content range. Distance is the integer square root of the squared distance. Outside the max, or when the line is blocked, it steers toward the approach point. Inside the min, with the line clear, it retreats: toward the enemy from the player. Between the two, with the line clear, it orbits. A telegraph starts only with a clear line, and that branch sets velocity to zero. The bolt itself stays in the stats note.

The vendor uses the content range, with the same square-root distance. Outside the max it steers toward the approach point. Inside the min it retreats. Between the two, the bounds included, velocity is zero. A telegraph does not require a clear line. The mine it places is [mine-resolution-2026-11-04.md](mine-resolution-2026-11-04.md).

Orbit is `Steering.orbitVelocity` around the player. An even id is clockwise: the perpendicular of the vector from the enemy toward the player is `(dy, −dx)`. An odd id uses `(−dy, dx)`. Magnitude 0 returns zero. The scale step is `mulDivHalfAway`.
