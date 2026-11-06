# The probe's camera walk

Read 2026-11-05 from `ProbePilot.cameraToDestroy` and `shotClear` on `ef68565`. No camera was added. When loud walks at that point stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The rules' mount skip stays in [target-order-2026-11-04.md](target-order-2026-11-04.md). The segment test stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md). Truncation stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

`shotClear` is false when any solid whose id is not that camera's mount meets the segment from the point to the anchor.

`cameraToDestroy` keeps a live camera whose squared distance to the anchor is at most `360 * Q8.scale`, squared, and whose shot is clear. The nearest squared distance wins. An equal distance keeps the earlier camera. The returned point is that anchor truncated to units.

This does not play a release build.
