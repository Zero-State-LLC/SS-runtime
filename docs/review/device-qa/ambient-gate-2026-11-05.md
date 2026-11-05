# Ambient gate

Read 2026-11-05 from `AmbientMotionLoader.decode` on `ef68565`. No recipe was changed.

The shipped periods and the caps of 12 and 1 stay in [ambient-motion-2026-11-04.md](ambient-motion-2026-11-04.md). The roll, the drop, and the hash stay in [ambient-roll-2026-11-05.md](ambient-roll-2026-11-05.md).

The schema is `ambient-motion-001`. The animation version is `animation-civic-seam-001`. A wrong animation version throws `schemaVersion`, the same error as a wrong schema. An unexpected catalog key or recipe key throws `unexpectedKey`. A missing recipe key throws `missingKey`. `maxConcurrentAmbient` and `maxConcurrentRare` must be integers, the recipe array must be non-empty, or the file throws `invalidJSON`. Either budget below 1, or a max ambient below the persistent id count, throws `budget` with the string `maxConcurrentAmbient`.

A repeated recipe id throws `missingRecipe` with that id. Each required id must be present, or the loader throws `missingRecipe` with the missing id. The persistent ids are `fogDrift`, `trolleyWireSway`, `rooftopFans`, `cameraStatus`, `trafficSignals`, `pigeonsScatter`, `blinds`, `windChannels`, and `transitDisplay`. The rare ids are `greenParrotCrossing`, `autonomousVehicleHesitation`, `streetcarShadow`, `towerLightSync`, `phoenixBlink`, `occupantBlinds`, and `fogRevealNetwork`.

A recipe's kind is `persistent` or `rare`. Its tier is `p0`, `p1`, or `p2`. `periodTicks` is above 0. `durationTicks` is above 0 and at most the period. `chancePercent` is from 0 through 100. `impliesGameplay`, `impliesCollision`, `impliesReward`, `impliesEnemy`, and `impliesObjective` must all be false, or the recipe throws `gameplayImplication`. `salience` must be `belowGameplay`. `cameraStatus` must keep its housing locked, and must not translate or rotate that housing. A rare recipe must set `pausesWhenCaptainTelegraph`.

This does not change a recipe.
