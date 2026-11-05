# Arena bounds

Read 2026-11-04 from `civic-seam-arena-004` and `ArenaLoader.validate` on `fcab4e5`. No bound was moved.

The loaded arena runs from `(0, 0)` to `(2304, 1536)`. The cell is 64. The grid is 36 by 24. Validation requires that cell, that grid, and those two maxima.

A projectile whose raw x or y is below 0, or whose raw x is past `2304 * 256` or raw y past `1536 * 256`, is retired on that check. A projectile sitting on the maximum edge stays.

This does not resize the arena.
