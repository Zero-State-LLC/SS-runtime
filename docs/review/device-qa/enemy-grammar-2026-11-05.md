# The enemy block, loaded

Read 2026-11-05 from `CombatContent.parseEnemies` through `decodeArray` on `ef68565`. No enemy was added. The stat table stays in [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md). The wave numbers stay in [encounter-waves-2026-11-04.md](encounter-waves-2026-11-04.md). The elite and boss blocks stay in [content-bands-2026-11-05.md](content-bands-2026-11-05.md).

`standardEnemies` must be an object. A missing object or array is `missingField`. A present value of the wrong type is `wrongType`. The keys are walked in sorted order. An unknown name throws `unknownArchetype`.

Each enemy requires `hp`, `radius`, `speed`, and `contactDps` through the dictionary `int` cast. The enemy `range` is `[Int]` when present and nil when absent. `pulse`, `charge`, `shot`, and `mine` are nil when the key is absent. A present block is an object. Pulse requires `first`, `cooldown`, `telegraph`, `range`, and `exposure`. Charge requires `first`, `cooldown`, `telegraph`, `ticks`, `speed`, and `recover`. Shot requires `first`, `cooldown`, `telegraph`, `speed`, `radius`, `lifetime`, and `damage`. Mine requires `first`, `cooldown`, `telegraph`, `maximum`, `arm`, `lifetime`, `radius`, and `damage`.

`encounters` must be an object. Its keys are stored as written, walked in sorted order, with no closed set of names. Each encounter requires `zone` and `totals`. `activationExposure` and `initialDelay` are optional integers. `waves` is a required array. Each wave requires `id` and `interval`. A missing `delay` is 0. `members` is an object, walked in sorted key order. An unknown name throws `unknownArchetype`. The count is an `Int`.

Those integer fields use the dictionary `int` cast. [content-bands-2026-11-05.md](content-bands-2026-11-05.md) records that the cast does not call `JSONScalar.isBool`.

This does not add an enemy.
