# The probe's ambush cell

Read 2026-11-05 from `ProbePilot.ambushPosition` on `ef68565`. No route was changed. When `decide` navigates there stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The standoff stays in that note. The shot test stays in [probe-firing-2026-11-05.md](probe-firing-2026-11-05.md). The nearest cell stays in [probe-grid-2026-11-05.md](probe-grid-2026-11-05.md).

Targets leave out an unaware enemy whose point is a patrol member. Every target uses `fireRange`. The unaware list leaves patrol members out as well. The cache key is each target's coordinates divided by the step.

The call adds one to its tick count and returns the cached cell when the key matches and that count is still below 30. Otherwise the count returns to 0. A missing walkable start returns nil and leaves the cache. The search stops at 6,000 cells. A cell is hidden when no unaware enemy is within the standoff with a clear line, and `inCone` is false. It also needs some target inside its reach with `clearShot`. A filled field grid takes the first hidden cell that no field covers, and keeps the first covered cell as the fallback. The result, including none, is stored under that key.

This does not play a release build.
