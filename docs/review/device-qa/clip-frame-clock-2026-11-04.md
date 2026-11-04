# Clip frame clock

Read 2026-11-04 from `ClipTiming` on `30a2cc6`. No frame was added, and no rate was changed.

`durationTicks(at: 60)` multiplies the clip's total authored units by 60 and divides by that clip's units per second. When the product does not divide evenly, the duration rounds up by one tick. `frameIndex(atTickOffset:)` walks the same units at 60 Hz. Once the offset is past the last boundary, the index stays on the last frame.

A uniform clip is one authored unit per frame at that clip's own `framesPerSecond`. Each clip keeps the rate stored in `clip-metadata-001`.
