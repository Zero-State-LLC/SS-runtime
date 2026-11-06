# The daemon expiry

Read 2026-11-05 from `EnemySystem.stepDaemon` on `ef68565`. No elite timing was changed.

The content cycle stays in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). The markers, the damage, and the steering while ticks remain stay in [daemon-query-2026-11-04.md](daemon-query-2026-11-04.md).

While `stateTicks` is above 0 the function returns after that steering. On expiry the switch writes the next remaining count as a literal. Those counts match the content cycle. The switch does not read the content fields.

Pursue stores the markers, then sets `queryTelegraph`, remaining 45, and velocity zero. Query telegraph sets `queryResolve`, remaining 0, and calls `stepDaemon` again, so the resolve case runs before the outer call returns. Resolve adds `DaemonQuery.damage`, then sets `dashTelegraph`, remaining 36, and velocity zero. Dash telegraph sets `dash`, remaining 30, and velocity toward the player at `Steering.speedQ8` of 288. That 288 stays in the daemon-query note. Dash sets `recover`, remaining 60, and velocity zero. Any other state sets `pursue`, remaining 120, and steers toward the player at the speed argument.

This does not change the elite cycle.
