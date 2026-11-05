# Captain path

Read 2026-11-04 from `CaptainPath` and `BossSystem.applyLocomotion` on `fcab4e5`. No path weight was changed. Phase numerators stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md).

The search runs every tick from the current position. The Captain stores no path. Solids are ordered by UTF-8 id. Positions are truncated to whole units. Corner nodes sit `radius + 4` outside each box corner, and a node within 2 units of the truncated start is skipped as the first step. A node outside the bounds, shrunk by the radius, is dropped. A node whose squared distance to any box is under the radius squared is dropped.

A body-clear straight line to the player returns that point with routing off. Otherwise the waypoint is the first node of the shortest clear path, with routing on. A shorter distance replaces the stored one, and an equal distance keeps the lower node index. When no path exists, the Captain steers straight at the player with routing off.

A leg is clear when, for every box, the squared distance from the segment to the box is at least the smaller of the radius squared and the two endpoints' own squared distances to that box.

While routing, the orbit numerator is 0. Otherwise the perpendicular is `(cy, -cx)` when the boss id is even and `(-cy, cx)` when it is odd. A negative orbit flips that pair. The added part is a half-away division of that component times the absolute numerator, over 100. The combined direction is then scaled to `speedQ8` of a half-away division of the base speed times the phase speed numerator, over 100. The live step passes the content boss speed.

This does not change the search.
