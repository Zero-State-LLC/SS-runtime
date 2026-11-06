# The socket lists

Read 2026-11-06 from `SpawnFairness.socketsBlockedByPermanentSolids` and `socketsOutsideEncounterZone` on `ef68565`. No coordinate was rewritten.

`authoredSolidOverlaps` stays in [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md). These two lists do not reject a spawn.

`socketsBlockedByPermanentSolids` lists each enemy spawn socket whose point lies inside a permanent-solid AABB. The label is `socket.id`, or `"x,y"` when the id is nil. The list is sorted by UTF-8 bytes.

`socketsOutsideEncounterZone` walks each encounter. When content names a zone and the arena has that zone, a socket outside that zone's AABB is labeled the same way. A missing encounter zone is skipped. The list is sorted by UTF-8 bytes.

This does not reject a spawn.
