# The patrol proof

Read 2026-11-05 from `PatrolFairness.evaluate` on `ef68565`. No patrol was moved. The zone quotas stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The grid step stays in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md).

The header says the player takes no part in the motion. `passes` is all five lists empty: waypoint violations, unreached waypoints, unproven, protected coverage, and blocked ticks.

`evaluate` starts with the waypoint list. Empty patrols return that report. More than three members appends `more than three members: the joint key does not fit` to unproven and returns.

The Z-02 subset size is that zone's `requiredByZone` count, or the literal 2 when the zone is absent. Each such subset must contain a `tutorialEligible` socket and be compatible. The Z-03 size is that count, or the literal 1. Each such subset must be compatible. Compatible is false when any socket lists another's id in `incompatibleSocketIds`.

Base solids are the permanent solids plus gates whose `initiallyClosed` is true. A mount id is `SelectedCamera.mountSolidPrefix` plus the socket id, and its half-size is `mountCollisionRadiusUnits`. A missing standard-enemy stat appends `a member's archetype has no content`. `cycles` stores that subset's tick count and period. A member whose states come within that member's radius plus 2 of a mount outside Z-02 is unproven.

Each waypoint must lie inside its zone and outside every permanent solid, every gate, and every encounter trigger.

`jointOrbit` steps the members with `EnemySystem.moveUnaware`. The joint key packs 21 bits per member. A repeated key returns, and the period is the distance back to the first sighting. The cap is the literal 36_000. Reaching the cap returns period 0. An interned id at or above `1 << 21` returns period 0 with the timeline so far.

When `dwellTicks` is above 0, a waypoint counts as arrived where a stored state still names that target and `dwellRemaining` equals `dwellTicks` minus 1. When `dwellTicks` is 0, the arrived set is each stored state's previous target, wrapping around the waypoint count.

`check` records protected coverage when a stored state sees the player spawn, or a Z-01 point on a lattice of half the grid step. The lattice includes the edges, walkable or not. Sight is `PatrolSystem.inCone` and a clear line of fire. The route grid is the union of Z-01, Z-02, and Z-03. A tick whose route still exists after one member's cone is widened to its whole-orbit union passes. Otherwise the exact cones decide. A failing tick is a blocked tick. The first three are named, and a count above 3 adds one summary line.

This does not move a member.
