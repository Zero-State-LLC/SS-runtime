# The effect budgets

Read 2026-11-05 from `ProceduralVFXLoader.decode` on `ef68565`. No budget was changed. The hit-stop caps, the coalesce window, the emitter ceiling, and the forbidden flash stay in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). The integer cast that skips `JSONScalar.isBool` stays in [content-bands-2026-11-05.md](content-bands-2026-11-05.md).

The schema string must equal `ContractVersions.proceduralVFX`. `visualVersion` must be `visual-civic-seam-001`. `atlas` must be `combat_vfx.atlas`. The emitter count must be an int above 0 and within the ceiling in the hit-stop note. The two hit-stop fields, the coalesce field, and `forbidFullScreenWhiteFlash` must match that note, and `forbidFullScreenWhiteFlash` must be the JSON bool `true`. A miss on that guard throws `invalidJSON`. A wrong schema or visual version throws `schemaVersion`.

An unexpected catalog, recipe, or variant key throws `unexpectedKey` of the first sorted extra key. A missing required key throws `missingKey`. A repeated recipe id throws `missingRecipe` of that id. A required id that never appears throws `missingRecipe` of that id. The required ids, in order, are `cameraAcquire`, `exposureThreshold`, `playerHit`, `enemyHit`, `enemyDefeat`, `ghostStep`, `ricochet`, `lockdown`, `captainTelegraph`, `extraction`, `cameraDestroyed`, `networkBlackout`, `bossPhaseBreak`, `heatReinforcements`, and `enemyAlerted`.

`intValue` returns `as? Int`, then `NSNumber.intValue`, then nil. An empty id, shape, or event list, or a variant that is not an object, throws `invalidJSON`. `poolSize` must be at least 1. An event name that is not an `EventType` raw value throws `budget`. A variant needs a non-empty language, a particle count of at least 0, a lifetime above 0, a hit-stop of at least 0, and bools for shake and flash. Either variant with `fullScreenFlash` true throws `fullScreenFlash`. A reduced variant with `screenShake` true throws `reducedShake`. A hit-stop above the recipe's cap throws `budget`. The captain-class ids are `captainTelegraph` and `bossPhaseBreak`.

`validateBudgets` throws `budget` when `enemyHit`'s default lifetime is above 120, when `enemyDefeat`'s default particle count is outside 4 through 8, its default lifetime is above 350, or its reduced particle count is above 2, when `ghostStep`'s default lifetime is above 300 or its reduced particle count is above 1, or when either `networkBlackout` lifetime is not 1500. Every other id skips that switch.

This does not change a budget.
