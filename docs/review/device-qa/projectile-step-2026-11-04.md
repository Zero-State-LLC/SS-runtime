# Projectile step

Read 2026-11-04 from `moveProjectilesAndCollectHits` on `93f6d67`. No speed, radius, or lifetime was changed.

A live projectile advances only when its age is already greater than 1. The step stores the previous position, adds the velocity, and adds `isqrt` of the velocity's raw length squared to the distance travelled. Age then increases by 1.

The projectile is retired when an x or y raw coordinate is below 0 or past the arena max, when age exceeds its lifetime, or when the distance travelled exceeds its max travel. A Civic Pulse or a ricochet returns to the civic pool. Any other kind is marked dead.

The live Civic Pulse, the witch bolt from `spawnProjectile`, and the boss bolt from `BossSystem.fire` are created at age 1. Each is placed one velocity step ahead of its origin, and that placement step is already in `distanceTravelled`. The move runs after those spawns on the same tick, so the spawn tick does not add a second step. The witch bolt and the boss bolt use a max travel of 10,000 units. The Civic Pulse max travel stays in [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md).
