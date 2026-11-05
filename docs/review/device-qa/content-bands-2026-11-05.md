# The bands, the angle, and the percents

Read 2026-11-05 from `CombatContent.decode` on `ef68565`. No band was moved. The phase table stays in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). The court floor stays in [player-integrity-2026-11-04.md](player-integrity-2026-11-04.md). The upgrade match stays in [upgrade-match-2026-11-05.md](upgrade-match-2026-11-05.md).

A payload that is not a JSON object throws `invalidJSON`. A `CombatContentError` is rethrown. Any other parse failure is `invalidJSON`.

The load reads elite, boss, standard enemies, encounters, heat, awareness, patrol, and player. `validateUpgrades` runs last and is not stored. The elite and boss integer fields use the dictionary `int` cast. That cast does not call `JSONScalar.isBool`.

`parseBossBands` requires the phase count to equal `BossPhase.receiptOrder.count`. Each id must match that order. Each `minHp` is an integer, not a boolean, in 1 through the boss hp, and strictly below the previous floor. The last floor must be 1, or the error is `wrongType` at `boss.phases[3].minHp`.

`parsePatrol` requires `sightHalfAngleMilliDegrees` to be a key of `PatrolSpec.exactCosineSquared`. Integrity, speed, sight, that half-angle, and arrival must be at least 1. Dwell must be at least 0. A JSON boolean fails those fields.

`parsePlayer` requires integrity at least 1. `damageTakenPercent`, `courtThresholdRestorePercent`, and `courtQuietRestorePercent` must be at least 0 and at most 100.

This does not change a floor.
