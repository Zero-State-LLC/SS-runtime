# Ghost silhouette

Read 2026-11-04 from `WorldRenderer` on `d873e91`. No fade was changed.

The fade stays in [ghost-replay-2026-11-04.md](ghost-replay-2026-11-04.md). The contour stays in [actor-silhouettes-2026-11-04.md](actor-silhouettes-2026-11-04.md).

The ghost is the player's blockout path. It has no clip and no reaction. The fill is white 0.92. The stroke is white 1 at alpha 0.7, line width 2. Its z is −0.5, under the live player in the same layer. The alpha is `0.35 * fade`. The position is the ghost's player point.

This does not move the live player.
