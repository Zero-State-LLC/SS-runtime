# The view contains a point

Read 2026-11-05 from `PresentationCamera.contains` on `ef68565`. No view was resized. The visible size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The rules box stays in [spawn-socket-choice-2026-11-04.md](spawn-socket-choice-2026-11-04.md).

A point is inside when the absolute x delta from the centre is at most `visibleWidth / 2` and the absolute y delta is at most `visibleHeight / 2`.

This does not move the camera.
