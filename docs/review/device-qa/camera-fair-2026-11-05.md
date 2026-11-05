# The camera sets, checked

Read 2026-11-05 from `CameraFairness.evaluate` on `ef68565`. No socket was moved. The comment says this is never called from `ArenaManifest.bundled()` or `Simulation.make`. The legal-set enumeration stays in [camera-legal-set-2026-11-04.md](camera-legal-set-2026-11-04.md). The zone quotas stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The pulse range stays in [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md). The grid step stays in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md).

For each enabled socket the check stores whether the truncated origin is inside a solid, whether a circle of `mountCollisionRadiusUnits` penetrates Z-01, a field grid, and a pulse grid. A field cell is inside the cone at half the socket's field angle, with a clear line of fire. A pulse cell is walkable, within `Targeting.civicPulseRange` squared in Q8 of `targetAnchor`, with a clear line of fire from the cell to that anchor.

A leaking socket is one whose mount penetrates Z-01, or whose field meets a walkable Z-01 cell. An unhittable socket has an empty pulse intersection with the spawn-reachable grid. Origin-in-solid sockets are listed on their own.

Each legal set is keyed with `CameraPlacement.setKey`. Protected Z-01 is recorded when any selected mount penetrates Z-01, or the union field meets a walkable Z-01 cell. A choke is every gate box plus each consecutive-zone overlap. The key is recorded when any cell of a choke is covered by more than two fields. Pulse-stand and accessibility are both recorded when any selected pulse misses the reachable grid.

`zeroContactMissing` walks the consecutive zones. The start is that zone's walkable cells outside the union field. An empty start is a miss. The flood stays on walkable cells outside the field, and a miss is when it does not meet the next zone's walkable cells outside the field.

The branch flood starts at the M-B trigger cell, or at (1280, 1088) when that trigger is missing. Its blocked grid is empty, so the union field is not removed. The key is recorded when that cell is not walkable, or when the flood misses (1216, 1024) or (1600, 1152).

Captain-safe is recorded when the boss corridor is not clear, or when no walkable court cell sits outside the union field. A missing court records the key. Extraction is recorded when the spawn flood does not contain the extraction center. That flood is computed once. Field-origin is recorded when a selected origin is inside a solid. Overlap is recorded when any pair overlaps at the mount radius or at the hit radius. That test is `dx² + dy² < (ra + rb)²`.

This does not place a camera.
