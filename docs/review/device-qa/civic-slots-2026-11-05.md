# The civic slots

Read 2026-11-05 from `ProjectilePool` and `Simulation.retireProjectile` on `ef68565`. No cap was changed. The live cap stays in [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md). The continuation's checkout stays in [ricochet-continuation-2026-11-04.md](ricochet-continuation-2026-11-04.md). The retire rules for a shot that leaves the arena stay in [projectile-step-2026-11-04.md](projectile-step-2026-11-04.md).

The capacity constant is `Targeting.activeCeiling`. `PerformanceThresholds.civicPoolCapacity` is that same constant, and so is `ProjectilePool.civicPulseCapacity`. Slots start nil.

`liveCount` counts alive bodies. `checkout` takes the first slot that is nil or not alive, forces age 1, clears `hitEntityIds`, and marks the body alive. It returns false when every slot is a live body.

`release` of a missing id, or of a slot that is not alive, sets `doubleReturn` true and leaves the slots. A live match is set to nil. `replace` writes the body when the id is present and returns when it is absent. `live` is the alive bodies in slot order.

`retireProjectile` marks the shot dead. It releases a civic pulse or a ricochet id into this pool.

This does not change the cap.
