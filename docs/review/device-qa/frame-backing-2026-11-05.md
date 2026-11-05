# Frame backing

Read 2026-11-05 from `ClipFrameLibrary.deliveredFrames` on `ef68565`. No frame was added.

The catalog refusal this loader calls stays in [clip-gate-2026-11-05.md](clip-gate-2026-11-05.md). Nearest filtering, and an unbacked clip returning false, stay in [clip-playback-2026-11-04.md](clip-playback-2026-11-04.md). The facing letters stay in [facing-direction-2026-11-04.md](facing-direction-2026-11-04.md).

`make` runs `ClipCatalogLoader.decode`, then keeps a delivered path only for a catalog entry whose admission is `adaptedAdmitted` or `originalAccepted`, whose production status is `accepted`, whose kind is `sprite`, and which has a runtime path.

`deliveredFrames` returns nil when that direction's frame ids are empty. It returns nil when any of those ids has no delivered path. Otherwise it returns the paths in frame-id order. `isBacked` is that result being non-nil. A clip that lists directions, asked for a direction it does not list, has an empty id list and is unbacked. The ids themselves are the frame ids that contain `_<direction>_`. A clip that lists no directions returns every frame id for any direction argument.

`coverage` counts frame ids that have a path, over every frame id in the library. That count is a different number from all-or-nothing backing.

This does not add a frame.
