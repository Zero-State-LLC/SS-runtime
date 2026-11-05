# Corner pursuit

Read 2026-11-04 from `CornerPursuit` and `EnemySystem.think` on `fcab4e5`. No corner was moved. The Captain's search stays in [captain-path-2026-11-04.md](captain-path-2026-11-04.md).

An aware enemy with a clear line to the player steers at the player. A blocked line takes one corner, recomputed every tick from the current position. The enemy stores no path.

Corners sit 4 units outside the blocking box, past the enemy radius. The blocking solids are those the straight line meets, in UTF-8 id order. Each box offers four corners, in order: low x and low y, high x and low y, low x and high y, high x and high y. A corner within 8 units of the enemy is skipped. The corner must itself have a clear line from the enemy.

A corner that can see the player ranks ahead of one that cannot. Within that, the shorter path wins: the integer distance to the corner plus the distance from the corner to the player. An equal rank keeps the earlier solid and the earlier corner. When no corner qualifies, the enemy steers at the player.

The live step calls this with body clearance left off, so the reached distance is those 8 units.

This does not add a path.
