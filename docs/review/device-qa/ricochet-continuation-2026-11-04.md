# Ricochet continuation

Read 2026-11-04 from `resolveDamage` on `fcab4e5`. No damage number was changed.

Hit order is [hit-order-2026-11-04.md](hit-order-2026-11-04.md). The upgrade's range, damages, and single continuation are [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). This note is who continues, and when that continuation is resolved.

`Targeting.ricochetContinuationRequiresEnemyKill` is true. An enemy hit continues only when Ricochet Pulse is on, the projectile kind is still `civicPulse`, and that hit left the enemy at integrity 0 or below. A damageable camera continues whenever Ricochet Pulse is on and the kind is still `civicPulse`, including when the camera still has integrity. That camera path subtracts the literal 1. A wall, the player, or a camera that is not damageable retires the shot. A hit whose enemy is already dead is skipped and leaves the shot in play.

Continuations are queued through the first hit loop and spawned after it. The enemy origin is the enemy position. The camera origin is `targetAnchor`. The excluded id is the target just hit.

`ricochetTarget` keeps a living enemy other than the excluded id when the squared distance from the origin to the enemy is at most `ricochetRange` squared, in Q8, and `Collision.lineOfFireClear` from the origin to the enemy. It keeps a damageable camera other than the excluded id on the same distance test against `targetAnchor`, using `Targeting.lineOfFireClear`, which skips that camera's own `mountSolidId`. The list is sorted by squared distance, then by the lower entity id.

The spawned body keeps the projectile id. Its kind is `ricochet`, its position is the chosen anchor, its previous position is the impact origin, its age is 1, and its distance travelled is 0. `maxTravelQ8` is `ricochetRange` times `Q8.scale`. Velocity is `Targeting.direct` from the origin to the anchor at `projectileSpeedPerTick` times `Q8.scale`. A zero-length direct is `(speed, 0)`. `targetCameraId` is set when the chosen id is a camera. The hit list is the source list, with the excluded id appended when it was missing.

The projectile is still in the array, so the pool `replace` writes that body and keeps the hit list. `checkout` runs only when the id is absent: it forces age 1, clears `hitEntityIds`, and marks the slot alive. No candidate retires the source.

When any continuation was queued, `resolveDamage` runs again on the same tick. That sweep goes from the impact to the chosen anchor and skips an id already in the hit list. The kind is `ricochet`, so a second hit queues no further continuation.
