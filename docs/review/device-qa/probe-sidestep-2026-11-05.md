# The probe's sidestep

Read 2026-11-05 from `ProbePilot.flee`, `evasion`, `steerOpen`, `escape`, and `orbit` on `ef68565`. No route was changed. When `decide` calls these stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The player radius stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md). `headingUnit` stays in [millidegree-2026-11-04.md](millidegree-2026-11-04.md).

The eight headings are every neighbour offset, including the diagonals, multiplied by 8. `isOpen` is walkable at the player radius and outside every hazard. A hazard contains a point when the stored distance is below its radius.

`flee` probes each heading times 3. An open probe scores the distance from the threat minus one tenth of the distance to the objective. A strictly higher score replaces the best. No open probe returns the vector from the threat back to the position. `steerOpen` probes each heading times 3 and keeps the open probe with the strictly higher dot against the requested direction. None returns an empty command. `escape` probes each heading times 2 through `ArenaReachability.isWalkable` at the player radius and keeps the probe with the strictly higher distance from the hazard. None returns the vector from the hazard back to the position.

`orbit` tries twice. The step is `(-(position.y - point.y) * orbitSign, (position.x - point.x) * orbitSign)`, scaled by 24 over `max(1, Int(sqrt))`. An open probe returns that vector. Otherwise the sign flips. Two failures return an empty command.

`evasion` skips an `emitterField`. A telegraph whose heading length is 0 is skipped. The player counts when the along distance is above `-body` and below the shape range plus `body`, and the absolute across distance is below the half-width plus `body`. `body` is the player radius plus 10. A lane's half-width is half its width. Any other shape uses `max(0, along) * tan` of the half-angle in radians, and that angle is capped at 1.4 before the tangent. The side is positive when across is at least 0. A shape with `remainingTicks` at most 3 sets urgent. A hostile bolt whose speed is above 0 counts when the closing parameter runs from 0 through 40 and the miss is below the bolt radius plus `body`. The added step is that bolt's perpendicular, on the side of the cross product. A parameter of at most 6 sets urgent. A zero sum returns nil.

`vector` of a zero length returns an empty command. Otherwise each component is the direction times `32767 / magnitude`, rounded, and clamped to ±32767. Dodge is false.

This does not play a release build.
