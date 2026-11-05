# Clip interrupt

Read 2026-11-05 from `ClipAlignment` on `5a71391`. No clip was replaced.

The facing letters and `cardinalDirection` stay in [facing-direction-2026-11-04.md](facing-direction-2026-11-04.md). The camera clip ids stay in [camera-clip-states-2026-11-04.md](camera-clip-states-2026-11-04.md). `ReactionClipTracker.mayInterrupt` stays in [reaction-clips-2026-11-04.md](reaction-clips-2026-11-04.md). The cancel-window contract stays in [clip-gate-2026-11-05.md](clip-gate-2026-11-05.md).

`interruptTokens` are `hurt`, `defeat`, and `dodge`. `canInterrupt` returns false when the current clip is terminal. Otherwise it is true when that clip's `cancelWindows` contain the incoming clip id or the incoming state. `alignsCommit` is true when the current blend is `telegraph`, the incoming blend is `cutOnEvent`, both clips share an actor role, and the incoming clip has an event type.

`project` walks the events in order. A missing current clip uses the first clip of that role. When the role has none, the playback keeps the query's clip id, an empty direction, empty frame ids, anchor (0, 0), `mirrored` false, `interrupted` false, `eventAligned` false, `fieldOffClipId` nil, and `housingTransformLocked` only for role `camera`.

A `cameraDestroyed` event on role `camera` sets `fieldOffClipId` from `CameraPresentation.clipId(for: .fieldOff)` and sets `eventAligned`. The clip for an event is the clip of that role whose event type is the event. No such clip leaves the playing clip in place. One such clip is that clip. More than one: `cameraIntegrityChanged` selects `camera_critical_enter` when payload `after` is 1, and `camera_hit` otherwise; `cameraDestroyed` selects `camera_destroy`; any other event selects the first marked clip.

The same clip id sets `eventAligned` from whether that clip has an event type, and the playing clip stays. `canInterrupt` replaces the clip, sets `interrupted`, and sets `eventAligned` from the incoming event type. `alignsCommit` replaces the clip and sets `eventAligned`. `interrupted` stays as the earlier events left it.

The direction is empty when the clip lists no directions. Otherwise it is `cardinalDirection` of the query heading. Returned `mirrored` is false. West uses the authored `_w_` frames. `housingTransformLocked` is true when the role is `camera`.

This does not replace a clip.
