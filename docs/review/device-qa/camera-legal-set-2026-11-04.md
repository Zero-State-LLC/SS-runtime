# Camera legal set

Read 2026-11-04 from `CameraPlacement.choose` and `isLegal` on `aaa7919`. No camera was added. Zone counts, the placement seed, the housing shuffle, and integrity 3 stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md).

`select` returns nil unless the pool passes `manifestPoolIsValid`, a legal set exists, and the runtime assert after `materialize` passes. That pool check requires each ban to be listed both ways. The zone minimums stay in the placed-cameras note. The live search then uses enabled sockets, grouped by zone, and walks each zone's shuffled pool in `requiredByZone` order.

A socket is incompatible when either socket lists the other's id. A finished Z-02 pick is rejected unless it contains at least one `tutorialEligible` socket. The next candidate starts at the index after the last picked socket in that pool, and a socket id already picked is skipped, so each zone is a combination in pool order.

A set is legal when it has 8 sockets, at least 4 distinct housing families, and at least 4 `returnVisible` sockets. The exhaustive enumerator keeps a finished set when the count is 8 and return-visible is at least 4. The four-family requirement is the live `isLegal` check.

`materialize` sorts the chosen sockets by `socketId` UTF-8 bytes. A shorter id sorts first when one is a prefix of the other. Entity ids are assigned in that order.

This does not add a camera.
