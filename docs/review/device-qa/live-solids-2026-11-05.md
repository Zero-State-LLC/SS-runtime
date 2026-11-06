# The solids this tick

Read 2026-11-05 from `WorldState.liveSolids` on `ef68565`. No solid was changed. The slide stays in [circle-slide-2026-11-04.md](circle-slide-2026-11-04.md). The mount draw stays in [mount-solids-2026-11-04.md](mount-solids-2026-11-04.md). The reachability boxes stay in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md).

The list starts as `arena.solidsForCollision`, which is each permanent solid's id and aabb. Every camera then appends `mountSolidId` and a square centered on the camera position whose half-size is `mountCollisionRadius` on both axes. A destroyed camera stays in that loop. Each gate with `closed` appends its id and its box.

This does not change a solid.
