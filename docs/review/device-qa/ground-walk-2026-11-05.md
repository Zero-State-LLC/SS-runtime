# Ground walk

Read 2026-11-05 from `WorldRenderer.renderGround` on `87ab159`. No tile size was changed.

The tile and the zone map stay in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). The brightness mix stays in [ground-tint-2026-11-04.md](ground-tint-2026-11-04.md).

The walk starts at the arena's minimum corner. Each sprite is centred half a tile up and right of its cell's minimum, and the next cell starts one tile further. The loop stops at the arena's maximum. The zone is sampled at the sprite's centre.

This does not change a tile size.
