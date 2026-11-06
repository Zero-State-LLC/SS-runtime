# The display interval

Read 2026-11-05 from `GameScene.update` on `ef68565`. No camera gain was changed.

The follow cap, the dead zone, and the look-ahead stay in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). Clearing the stored time stays in [pause-2026-11-04.md](pause-2026-11-04.md).

The stored interval starts at 1/60. Each update replaces it before the pause guard. A missing last time uses 1/60. A stored time uses the greater of 0 and the raw difference, and the current time is then kept. When the redraw runs, it passes that interval to `CameraFollow.update`.

This does not change the follow gain.
