# The probe's firing cell

Read 2026-11-05 from `ProbePilot.clearShot` and `firingPosition` on `ef68565`. No route was changed. When `decide` navigates there stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The line of fire stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md). The nearest cell stays in [probe-grid-2026-11-05.md](probe-grid-2026-11-05.md). The unwounded kite stays in the probe-order note.

`clearShot` tries the five offsets `(0, 0)`, `(2, 2)`, `(-2, 2)`, `(2, -2)`, and `(-2, -2)`. Each start is the first point plus that offset. Each end is the second point plus `(-dx, dy)`. Every one of those segments must be clear.

`firingPosition` adds one to its tick count and returns the cached cell when the target is within two steps and that count is still below 30. Otherwise the count returns to 0. A missing walkable start returns nil. The search is the first visit of each neighbour. A cell counts when its distance to the target is at most the reach and at least `min(kiteRange, reach / 2)`, and `clearShot` is true. Stealth with a filled field grid takes the first such cell that no field covers. A covered cell is kept once as the fallback, and the search stops once it has walked more than 400 cells past that fallback. The result is that cell, or the fallback. A result is cached with the target. No result stores no cache.

This does not play a release build.
