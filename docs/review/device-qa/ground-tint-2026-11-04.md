# Ground tint

Read 2026-11-04 from `WorldRenderer.renderGround` on `e4ff026`. No tile was changed.

The zone map stays in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). The kerb and the lip bands stay in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md).

The ground is built once, while the ground group is backed. Each tile takes a blend of `0.10` toward a white computed from its minimum corner. That corner is the world point the tile walk already uses. The mix is the wrapping product `x * 73_856_093` xor `y * 19_349_663`, then a shift-xor by 33, a multiply by `0xff51_afd7_ed55_8ccd`, and a second shift-xor by 33. The level is `0.42` plus `0.16` times `(hash % 5) / 4`. The value is not taken from a combat stream.

This does not change a tile.
