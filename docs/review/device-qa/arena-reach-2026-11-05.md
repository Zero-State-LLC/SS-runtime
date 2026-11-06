# The walk, and the spine

Read 2026-11-05 from `ArenaReachability` on `ef68565`. No collision was changed. Presentation sprites never contribute. The live gate close stays in [forward-gates-2026-11-04.md](forward-gates-2026-11-04.md). The player radius stays in [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md). The viewport pair stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). [seam-checks-2026-11-05.md](seam-checks-2026-11-05.md) names `diagonalSpine`.

`gridStep` is 16. The critical radius is 64, the combat radius is 80, the boss-corridor radius is 96, and the camera-stand radius is 64. The consecutive zone ids are `Z-01` through `Z-07`.

`boxes` takes the permanent solids, then each gate whose id is in the closed set, then the extra solids. `isWalkable` is false when `Collision.clampCenter` moves the center. Otherwise it is true when the radius circle does not penetrate a solid.

`flood` is a four-direction walk of those cells. `containsPoint` on a grid point reads that cell. Off the step, it also accepts the ceil cell on each axis that is off the step. `originWalkable` is true when the start is walkable or the queue is non-empty.

`consecutiveZonesConnected` floods from the player spawn at the critical radius and requires every consecutive pair of zone boxes to intersect that flood. `bossCorridorClear` floods from the boss spawn at the boss-corridor radius and requires `Z-06`. `extractionReachable` uses the player radius from the spawn to the extraction center, and it closes `gate-boss-extraction` only when `bossGateClosed` is true.

`maEscapeOpen` floods from the spawn with `gate-ma-forward` closed and asks whether `Z-03` intersects. `escapeApertureOpen` floods from the encounter trigger with that encounter's forward gate closed. The previous zone is `Z-02` for M-A, `Z-03` for M-B, and `Z-04` for M-C. That box is inset by `cellSizeUnits` on each half-size, floored at 0, and the flood must intersect the inset.

`spawnAlleyProtected` is false when a socket's zone is `Z-01` or its position is inside `Z-01`, when an enemy socket, the elite, or the boss is inside `Z-01`, or when an enabled socket's cone contains the player spawn with a clear line of fire.

`geometryInBounds` requires inclusive bounds on the player, elite, and boss spawns, the extraction box, the zones, the permanent solids, the gates, the triggers, the camera sockets, the enemy sockets, the extraction-pressure sockets, and the captain emitters. `authoredSolidOverlaps` names a spawn, extract center, elite, boss, trigger, or socket inside a permanent solid, a gate overlap of the spawn or of a socket, and a solid overlap of extraction, then sorts. `fieldOriginsInsideSolids` tests the truncated field-origin units against `boxes`.

`viewportMatchesContract` requires the manifest viewport to equal the presentation camera on width, height, dead zone, and look-ahead, and the visible width and height to equal the pair in the camera-follow note. `diagonalSpine` requires `Z-01` through `Z-04`, each next center strictly greater in both x and y. `blockedCameraStands` returns the sockets that are not walkable at the supplied radius.

This does not move a zone.
