# Target class order

Read 2026-11-04 from `Targeting` on `93f6d67`. The order was not changed.

`Targeting.select` keeps a living enemy inside the range [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md) records, when the line of fire is clear. It keeps a damageable camera that is chosen, inside that same range, when the line of fire is clear. A close enemy is one whose distance is within 96 units. The comparison is on squared distance, against 96 squared. Class order is close enemy, then chosen camera, then other enemy. A tie on class takes the smaller squared distance. A tie on distance takes the lower stable id.

A camera is chosen when the player's velocity is nonzero, the dot with the direction to the anchor is positive, and `4 · dot² ≥ 3 · |v|² · |d|²`. That is within 30 degrees of travel. The two sides are compared as 128-bit products. That camera's own mount does not block the shot. Every other solid does.

An unaware patrol member is a candidate only within the patrol sight [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md) records, and only while the same chosen test faces it.

`ricochetTarget` takes the nearest living enemy or damageable camera other than the origin, then the lower id, inside the range [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md) records, with a clear line of fire. The continuation rule stays in that upgrade note. Cadence, speed, radius, lifetime, travel, the live ceiling, and the two damage numbers stay in the Civic Pulse note.
