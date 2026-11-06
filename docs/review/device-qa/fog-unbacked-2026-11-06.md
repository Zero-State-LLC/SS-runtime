# Fog, unbacked

Read 2026-11-06 from `WorldRenderer.renderFog` on `ef68565`. No fog tile was added.

Drift, the split, and the speeds 120 and 300 stay in [fog-drift-2026-11-04.md](fog-drift-2026-11-04.md). `isBacked` stays in [env-groups-2026-11-05.md](env-groups-2026-11-05.md). The thinning clock stays in [fog-clock-2026-11-06.md](fog-clock-2026-11-06.md).

`fogThinning.update` runs before the guard. When the fog group is not backed, the function returns and draws no tile. The thinning clock has already stepped.

This does not draw a fog tile.
