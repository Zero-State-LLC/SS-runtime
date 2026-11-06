# The camera event overlay

Read 2026-11-05 from `CameraPresentation.project` on `ef68565`. No camera clip was added.

The persistent state and the clip for each state stay in [camera-clip-states-2026-11-04.md](camera-clip-states-2026-11-04.md). The live snapshot uses that persistent state. Playback alignment stays in [clip-interrupt-2026-11-05.md](clip-interrupt-2026-11-05.md).

Hit ids are the `cameraIntegrityChanged` events that carry a primary id. Destroyed ids are the `cameraDestroyed` events that carry one. A camera in the destroyed set is `destroying`. Otherwise integrity at or below 0 is `dormant`. Otherwise a hit id whose integrity is still above 0 is `hit`. Any other camera keeps the persistent state. `fieldVisible` is integrity above 0 and not destroyed in this call. The clip is the clip for the chosen state. `fieldOffClipId` is the field-off clip when the camera was destroyed in this call, and nil otherwise. The heading is copied. `housingTransformLocked` is true. `reducedMotionImmediateSwap` copies the argument, and that argument defaults to false.

This does not change the snapshot's persistent state.
