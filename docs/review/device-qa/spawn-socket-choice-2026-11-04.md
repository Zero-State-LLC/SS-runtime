# Spawn socket choice

Read 2026-11-04 from `SpawnFairness` on `93f6d67`. No socket was rewritten, and no wave was added.

`rank` orders sockets farthest from the player first. An equal distance takes the lower socket id, compared with `utf8LessThan`. `select` walks that order.

A socket is fair when the point is walkable, the archetype body does not penetrate zone Z-01, the center is outside the summed player and archetype radii (the test is `<=`), the flood from the player at radius 18 contains the point, and the center is strictly outside every lethal volume.

The viewport is `RulesViewport`, 896 by 414. The presentation camera stays 704 by 326 in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The fairness test uses that rules box with no extra margin. Offscreen fair sockets win. An on-screen socket is used when no offscreen fair socket exists. `select` returns nil when none is fair, and the spawn waits. The retry of 30 and the timeout of 300 stay in [encounter-waves-2026-11-04.md](encounter-waves-2026-11-04.md).
