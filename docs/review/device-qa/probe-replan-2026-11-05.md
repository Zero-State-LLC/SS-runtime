# The probe's replan

Read 2026-11-05 from `ProbePilot.navigate` and `avoidingCones` on `ef68565`. No route was changed. When `decide` calls `navigate` stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The path stays in [probe-grid-2026-11-05.md](probe-grid-2026-11-05.md). The step stays in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md). The open test and the vector stay in [probe-sidestep-2026-11-05.md](probe-sidestep-2026-11-05.md). The content cone stays in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md).

`decide` stores `snapshot.patrolCones`. A point is a patrol member when some stored cone has that x and y. `inCone` is true when `PatrolSystem.inCone` with `wideCone` is true and the line of fire from that cone to the point is clear. `wideCone` is the content patrol with 48 added to `sightUnits` and the half-angle set to 60,000.

`navigate` adds one to its tick count, then builds a new path when the stored goal is missing, the new goal is more than two steps from that goal, the path is empty, or the count has reached 30. That call stores the goal and sets the count back to 0. A first waypoint within one step is dropped while another waypoint remains. An empty path steers toward the goal. A path steers toward its first waypoint. Both results pass through `avoidingCones`.

`avoidingCones` returns the command unless the profile is stealth, a cone is stored, and the command moves. The probed step is the command times `12 / 32767`, rounded. A step that stays outside every cone keeps the command. A step that enters a cone, from a position that is outside, returns the command's dodge and no move. From inside a cone, the first heading times 2 that is open and outside every cone becomes the vector. None of those returns the command.

This does not play a release build.
