# Player integrity

Read 2026-11-04 from `combat-content-009` and `Simulation.applyPlayerDamage` on `49759ab`. No integrity number was changed. Medal predicates stay in [medal-predicates-2026-11-03.md](medal-predicates-2026-11-03.md).

Content `player.integrity` is 150. That is the spawn value and the clamp ceiling. Every loss, from any source, goes through `scaleDamageTaken` at `damageTakenPercent` 50. The carried remainder stays in hundredths. A loss that removes no whole point publishes nothing. The applied loss is capped by the integrity still left.

| Call | `damageKind` |
|---|---|
| Projectile hit | `projectile` |
| Contact | `contact` |
| Mine | `mine` |
| Enemy and boss amounts | `attack`, the default |

Contact collects aware enemies whose circles overlap the player. An unaware enemy deals none. The list keeps at most three, highest `contactDps` first and lowest id on a tie. Their `contactDps` values sum into `contactAccumulator`. Each 60 in that accumulator is one point, and the remainder stays. Those points then take the same 50 percent scale.

On the `bossActivated` tick, `applyCourtThreshold` raises integrity to at least `courtThresholdIntegrity`. That is `150 * 50 / 100`, which is 75. While `quietApproach` is still true the floor is `courtQuietIntegrity`, `150 * 60 / 100`, which is 90. The floor is also capped by `maxIntegrity`. Integrity already at or above the floor is left alone. The restore adds to `integrityRestored`. It does not add to `damageTaken`, and it does not touch the damage remainder.

This does not add a second damage formula.
