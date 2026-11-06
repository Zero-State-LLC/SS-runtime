# The selected frames

Read 2026-11-05 from `ClipTiming.selecting` on `ef68565`. No frame was dropped.

The 60 Hz walk, the round-up, and the last frame's hold stay in [clip-frame-clock-2026-11-04.md](clip-frame-clock-2026-11-04.md). The delivered paths stay in [frame-backing-2026-11-05.md](frame-backing-2026-11-05.md).

`selecting` throws `Failure.index` unless the index list is non-empty, every index is inside `frameUnits`, and each index is strictly greater than the one before it. The result is a new timing at the same `unitsPerSecond`, with `frameUnits` taken from those indices.

`init` throws `Failure.invalid` when the rate is not positive, the unit list is empty, or a unit is not positive. It throws `Failure.overflow` when the running sum overflows.

`frameIndex` compares full-width products. The elapsed product is the offset times `unitsPerSecond`. Each frame's end is the cumulative units times 60. The index is the first frame whose end is strictly above that elapsed product: a lower high word, or equal high words and a lower low word. The boundary belongs to the following frame.

`ClipFrameLibrary.timing` calls `selecting` when the clip has authored timing, a direction was asked, and the direction list is non-empty and contains that direction. The indices are the frame ids that contain `_<direction>_`. An asked direction missing from a non-empty list returns nil. Authored timing with no asked direction, or an empty direction list, returns that timing. With no authored timing, a clip that has `framesPerSecond` builds `uniform` from that direction's frame count and that rate. No rate returns nil.

This does not change a rate.
