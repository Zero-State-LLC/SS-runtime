# The effect projection

Read 2026-11-05 from `VFXProjector.project` on `ef68565`. No rank was changed. The renderer pass and the rank table stay in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md). The coalesce window stays in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). The reinforcement count stays in [heat-caption-2026-11-04.md](heat-caption-2026-11-04.md).

Stored damage ticks stay only while `tick` is at least the stored tick and the difference is below `playerDamageCoalesceTicks`. `reduced` is `reducedMotion` or `reducedFlash`.

For each event, each recipe whose `eventTypes` contain the event type is considered. `playerHit` skips a key already stored. The key is `payload["contributors"]?.serialize()`, otherwise the `sourceEntityId` string, otherwise `"unknown"`. A kept hit stores the tick and sets `lastPlayerDamageTick`. `cameraAcquire` continues only when detection rose from hidden to observed. `exposureThreshold` continues only when the after state is tracked, hunted, or lockdown. The `ricochet` recipe is skipped in this loop. `heatReinforcements` continues only when `context.heatReinforcements` is above 0. `bossPhaseBreak` continues only when the payload has both `before` and `after` strings, and the label is `phaseTitle` of `after`. The comment on that guard says an activation publishes `bossPhaseChanged` with no `before`, and that arrival is the Captain.

`present` copies the reduced or default variant's language, particle count, lifetime, hit-stop, and shake, plus the recipe shape, `primaryEntityId`, the sequence, the payload as evidence, and `reduced`. The sequence increments after each appended presentation. `networkBlackout` sets the label to `NETWORK BLACKOUT` and sets `cascade` from `context.cameraIds` over that presentation's lifetime.

After the events, projectile hits are grouped by `primaryEntityId`. For each id in sorted order, the group must contain exactly two hits, one `civicPulse` and one `ricochet`, both `projectileId` strings equal to `id.decimalString`, two different `targetEntityId` strings, and both impact points. An impact point is `impactXQ8` and `impactYQ8` as integers, built with `Q8(raw:)`. The ricochet recipe is then presented from the civic-pulse event, with `impactPoints` of those two points.

`VFXProjector.steal` runs while the count is above `maxConcurrentEmitters`. It removes the presentation whose rank is the maximum and, among that rank, the lowest sequence. An equal sequence keeps the earlier presentation. An id missing from the table has rank 9. `phaseTitle` starts a new word on an uppercase character when the current word is not empty, then uppercases each word and joins them with a single space. `cascade` unique-sorts camera ids by `raw`. An empty list returns an empty list. The offset is `lifetimeMs * index / ordered.count`. `reset` replaces the projector with a new one.

Nothing in the projection context is read back into the simulation.

This does not change a rank.
