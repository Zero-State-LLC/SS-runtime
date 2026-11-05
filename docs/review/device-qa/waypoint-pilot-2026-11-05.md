# The waypoint pilot

Read 2026-11-05 from `DebugAutopilot` on `ef68565`. No route was changed. The launch flag stays in [shell-host-2026-11-04.md](shell-host-2026-11-04.md). The probe stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md).

The type sits inside `#if DEBUG`. `run` and `tour` set mode `fullRun` and a `ProbePilot` at the competent profile, and `command` returns that pilot's command. Those two scenarios do not run the wall-follow.

`mobA`, `mobB`, `mobC`, `elite`, and `boss` use the trigger centre whose id is `trigger-` plus the encounter. A missing trigger returns nil. `extraction` uses `arena.extraction.center`. An unknown scenario returns nil.

`-SSAutopilotUpgrade` parses `UpgradeID`. An unknown raw value leaves the default `ricochetPulse`.

When the objective node changes, the tick count, the failed-detour count, and the best distance reset. With a probe, `stalled` is the probe's `stalled`. With no probe, `stalled` is `ticksOnObjective >= 60 * 180`.

Stuck is movement of at most 3 units for 20 ticks, and only while no detour remains. A new detour increments `failedDetours`, flips the sign when that count is even, and stores `min(70 * failedDetours, 420)`. The stored length then loses one tick. A distance more than 24 under the stored best clears `failedDetours`.

Holding extraction, armed and with the position inside the extraction aabb, skips kiting. The kite range is 180, or 340 when integrity is at most 45. Arrival is 40. Engage is 460. The nearest enemy is the smallest integer distance. That distance is a `Double` square root truncated by `Int()`. An equal distance keeps the earlier enemy.

The command kites unless extraction is being held. It steers away, and it dodges when the distance is below half the kite range. Otherwise it travels toward the target when farther than arrival. Otherwise it closes on the nearest enemy when that enemy is beyond engage. Otherwise it orbits perpendicular, away from the nearest. Otherwise it is idle.

A detour still above 0 replaces that command. A nonzero command turns a quarter turn, `(-moveY * sign, moveX * sign)`. A zero command turns the bearing toward the target. When both are zero, `moveX` is `32767 * detourSign` and `moveY` is 0.

A vector command uses full magnitude, `32767 / magnitude`, rounded, and clamped to ±32767. Distance and that normalize are `Double`, not Q8.

This does not play a release build.
