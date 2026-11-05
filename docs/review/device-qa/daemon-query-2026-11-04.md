# Daemon query

Read 2026-11-04 from `DaemonQuery` on `fcab4e5`. No elite timing was changed.

The cycle lengths stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). This note is the markers and the damage taken from them.

`circleRadius` is 56, `lateralOffset` is 96, and `resolveDamage` is 14. Markers are taken from the player position and facing on the tick pursue's remaining time reaches 0. A zero facing is replaced with the unit +X. The perpendicular is `clockwisePerpendicular`, `(y, −x)`. The three points are the player position, that position plus 96 along the perpendicular, and that position minus 96. The offset scale is `mulDivHalfAway`.

`damage` adds 14 for each stored marker whose circle contains the player. Contains is squared distance at most 56² × `Q8.scale`², so the circle edge counts. Query resolve adds that total from the markers stored at the end of pursue.

While ticks remain, pursue steers toward the player, dash keeps its velocity, and every other daemon state sets velocity to zero. The live dash assignment is `Steering.speedQ8(288)`. `TelegraphProjection.dashSpeed` is the same literal 288.
