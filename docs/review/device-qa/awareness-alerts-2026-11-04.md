# Awareness alerts

Read 2026-11-04 from `AwarenessSystem.resolve` and `hitDamage` on `aaa7919`. No cause was added. Sight range, ally radius, the alert state, and the ambush multiplier stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). Patrol sight stays in [patrol-sight-2026-11-04.md](patrol-sight-2026-11-04.md). The line of fire stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md).

The pass takes living enemies for which `isUnaware` is true, in ascending entity id. That flag is every awareness other than `aware`, so it includes `struck`. An empty list returns no alerts.

When surveillance alerts, every such enemy takes the cause `surveillance`. Damage, sight, and ally stay unevaluated. Surveillance alerts when the detection rank is at or above the content alert state. The rank order is hidden, observed, tracked, hunted, lockdown.

Otherwise a `struck` enemy takes `damage`. A patrol member takes `sight` when `PatrolSystem.sees` passes. Any other enemy takes `sight` when the squared distance to the player is at most the sight range squared and the line of fire is clear.

Ally sources are the positions of this tick's damage and sight causes. An enemy that still has no cause, and whose squared distance to a source is at most the ally radius squared, takes `ally`. An ally cause is not a source for anyone else.

In that same id order, each caused enemy becomes `aware`, its velocity becomes zero, and the alert is appended.

`hitDamage` turns an unaware enemy into `struck` and multiplies the base by the content ambush multiplier. A struck or aware enemy returns the base unmultiplied. The next enemy phase reads `struck` as the damage cause.

This does not add a cause.
