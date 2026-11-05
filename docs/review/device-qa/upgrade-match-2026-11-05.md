# The upgrade block, matched

Read 2026-11-05 from `CombatContent.validateUpgrades` on `ef68565`. No upgrade was added. The shipped numbers stay in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). The continuation test stays in [ricochet-continuation-2026-11-04.md](ricochet-continuation-2026-11-04.md).

`JSONScalar.isBool` is true when the value is an `NSNumber` whose CoreFoundation type is a boolean. `strictInts` rejects an unknown key, a missing key, a JSON boolean, a non-integer, and a value below that key's minimum.

`validateUpgrades` runs after the rest of `decode` and is not stored. A key outside `signalJammer`, `ricochetPulse`, and `ghostStep` is `wrongType`. Each compared integer must equal the simulation constant named at that field.

The jammer pulse ratio must be two integers, not booleans, with a denominator above 0. It is compared to `ExposureState.jammerPulseRatio`. The other jammer fields are compared to that type's contact reduction, minimum contact, heat-reinforcement reduction, and to `UpgradeID.signalJammer.selectionIndex`.

`continuationRequiresEnemyKill` must be a boolean equal to `Targeting.ricochetContinuationRequiresEnemyKill`. Continuations must equal the literal 1. Range, enemy damage, and camera damage are compared to `Targeting.ricochetRange`, `Targeting.enemyDamage`, and `Targeting.cameraDamage`.

Ghost dodge speed is compared to `PlayerBody.ghostDodgeSpeedUnitsPerTick` times 60. Dodge ticks and cooldown are compared to `PlayerBody.dodgeDurationTicks` and `PlayerBody.ghostDodgeCooldownTicks`. Post-dodge camera immunity is compared to `PlayerBody.ghostCameraImmunityTicks + 1 - PlayerBody.dodgeDurationTicks`.

This does not add a fourth upgrade.
