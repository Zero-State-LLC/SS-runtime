# The camera array, already sorted

Read 2026-11-06 from `CameraPlacement.selectedSetPassesRuntimeAsserts` on `ef68565`. No camera was added.

The count of 8, the four families, the four return-visible sockets, the zone quotas, and the sort inside `materialize` stay in [camera-legal-set-2026-11-04.md](camera-legal-set-2026-11-04.md) and [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The pool check stays in [pool-rejects-2026-11-05.md](pool-rejects-2026-11-05.md). The UTF-8 comparator stays in [utf8-order-2026-11-05.md](utf8-order-2026-11-05.md). What makes two sockets incompatible stays in the legal-set note.

The assert returns false unless the socket ids are eight distinct ids and the array's order already equals those ids sorted by UTF-8 bytes. It does not sort a set that passes. Along that order, each entity id must be strictly greater than the one before it. An incompatible pair returns false.

This does not add a camera.
