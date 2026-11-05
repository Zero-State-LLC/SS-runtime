# Line of fire

Read 2026-11-04 from `Collision.lineOfFireClear` and `segmentEntryTime` on `aaa7919`. No solid was changed. The body slide stays in [circle-slide-2026-11-04.md](circle-slide-2026-11-04.md).

A line of fire is clear when no solid box returns a segment entry time. The test is the zero-width segment from `from` to `to`.

`segmentEntryTime` clips that segment to the box slabs. Each box edge is the integer min or max times the Q8 scale. The window starts at t 0 and ends at the Q8 scale. A parallel component, `p == 0`, stays in the slab when `q >= 0` and rejects the segment when `q < 0`. A clip that keeps `t0 <= t1` returns `t0`. A segment that starts inside a box returns 0.

This does not change a solid.
