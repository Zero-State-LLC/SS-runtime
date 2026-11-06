# The patrol spawn

Read 2026-11-06 from `Simulation.spawnPatrols` on `ef68565`. No route was added.

The first waypoint, tick 1, the integrity percent, and the encounter id stay in [patrol-sight-2026-11-04.md](patrol-sight-2026-11-04.md).

The loop is `arena.patrols` in order. A route with no standard stats is skipped and takes no entity id. The call does not use `SpawnFairness`. Each accepted route takes `allocator.next()`, then `PatrolSystem.member`.

This does not add a route.
