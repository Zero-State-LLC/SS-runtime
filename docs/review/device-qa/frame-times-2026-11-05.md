# Frame times

Read 2026-11-05 from `FrameTimeCollector.summarize` on `ef68565`. No threshold was changed.

The 300-frame QA log stays in [retest-checklist.md](retest-checklist.md). Where `passesGateC` is stored on a device run stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md).

`recordFrame` keeps a sample only when the delta from the previous timestamp is above 0 ms and below 1000 ms. The delta is `(timestamp - last) * 1000`. The first timestamp stores no sample. `reset` clears the samples and that timestamp.

An empty buffer summarizes as sample count 0, each percentile 0, worst 0, and `sustainedBelowFloorFps` false. Otherwise the samples are sorted. The index for p 0.50, 0.95, and 0.99 is `(p * (count - 1))` rounded down, then clamped to the buffer. Worst is the last sorted sample.

The sustained floor is `1000 / sustainedPresentationFloorFps`, and that constant is 55. A sample above the floor adds one to a streak. Three in a row set `sustainedBelowFloorFps`, and that flag stays set for the summary. A sample at or under the floor sets the streak back to 0.

`passesGateC` requires a sample count above 0, p50 at most `16.67`, p95 at most `16.67`, p99 at most `25.0`, worst at most `50.0`, and the sustained flag clear. Those four limits are `frameTimeP50Ms`, `frameTimeP95Ms`, `frameTimeP99Ms`, and `frameTimeWorstMs`. `targetPresentationFps` is 60.

This does not change a threshold.
