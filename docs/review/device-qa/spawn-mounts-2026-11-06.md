# The spawn mounts

Read 2026-11-06 from `Simulation.spawnEnemy` and `SpawnFairness.select` on `ef68565`. No socket was moved.

The fairness predicate stays in [spawn-socket-choice-2026-11-04.md](spawn-socket-choice-2026-11-04.md). The volumes stay in [spawn-lethal-volumes-2026-11-04.md](spawn-lethal-volumes-2026-11-04.md). The collision-time mount list stays in [live-solids-2026-11-05.md](live-solids-2026-11-05.md). `spawnsAware` stays in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md).

Every camera, including a destroyed one, becomes an AABB centered on `camera.position` with half-size `mountCollisionRadius` on both axes. That array is `extraSolids`. `select` passes those solids into `boxes` and into the flood. The closed gate ids are the gates whose `closed` flag is set.

`select` runs before `allocator.next()`. A miss returns false and takes no entity id. A hit starts in `pursue`, with `stateTicks` 0 and velocity zero.

This does not move a socket.
