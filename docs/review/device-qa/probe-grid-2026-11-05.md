# The probe's grid

Read 2026-11-05 from `ProbePilot.plan` and `breadthFirst` on `ef68565`. No route was changed. When `decide` calls `navigate` stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The step and the walkable test stay in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md). The line of fire stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md).

The bounds are `arena.boundsUnits.aabb`. The column count is `(maxX - minX) / step + 1`, and the row count is the same on Y. `step` is `ArenaReachability.gridStep`. A cell point is the minimum plus the index times that step. `cell` adds half a step, divides, and clamps to the grid.

`rebuildGrid` marks a cell walkable when `isWalkable` at radius 22. `neighbours` are the eight adjacent cells that are walkable and outside a hazard. A diagonal also needs both side cells walkable. `nearestWalkable` searches chebyshev radii 0 through 7 and returns on the first radius that contains a walkable cell. A clear line of fire beats a blocked one. The same clarity keeps the smaller distance. An equal distance keeps the earlier cell, scanned in increasing y then x. No cell in those radii returns nil.

`plan` takes `nearestWalkable` of the start and of the goal, and returns an empty path when either is nil. A stealth profile whose field grid has one entry per cell uses the bucket queue. Every other call uses `breadthFirst`. In the bucket queue a step into a field costs 12 and any other step costs 1. A neighbour is written when the new cost is strictly lower. The search stops when the goal is taken from its bucket. `breadthFirst` records the first visit. Both rebuild the path from the goal back to the start, leave the start off, and reverse it. An unreached goal returns an empty path.

This does not play a release build.
