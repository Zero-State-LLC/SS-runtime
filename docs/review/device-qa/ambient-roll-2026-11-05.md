# Ambient roll

Read 2026-11-05 from `AmbientMotion.project` on `5a71391`. No recipe was added.

The catalog table, the concurrent caps, and the salience labels stay in [ambient-motion-2026-11-04.md](ambient-motion-2026-11-04.md). The cosmetic stream constant stays in [rng-streams-2026-11-04.md](rng-streams-2026-11-04.md).

A `p1` recipe is skipped when `disableP1` is set, and a `p2` recipe when `disableP2` is set. A recipe that requires combat nearby is skipped without combat. A recipe that requires a beam crossing is skipped without a beam. A rare recipe is skipped under reduced motion, and, while the captain telegraph is active, when that recipe pauses for it.

`scheduled` takes `local` as `tick % periodTicks`. It is false when `local` is at least `durationTicks`. It is true when `chancePercent` is at least 100. Otherwise the roll is `SplitMix64.mix` of the run seed xor the cosmetic stream constant xor `fnv(recipe.id)` xor `tick / periodTicks`, and the recipe is in when `Int(roll % 100)` is below `chancePercent`.

The language is `reducedLanguage` under reduced motion and `language` otherwise. A language of `none` drops the recipe. The phase is `tick % periodTicks`. `housingTransformLocked` is copied from the recipe. The scheduler comment names the COSMET01 stream and says the roll is not the combat or placement RNG and writes no digest field.

`limitRare` drops the last rare recipe id until the rare count is within `maxConcurrentRare`. `steal` runs while the layer count is above `maxConcurrentAmbient`. It removes the layer with the highest priority number, and among those the lowest recipe id. Persistent `p0` is 1, persistent `p1` is 5, persistent `p2` is 6, rare `p1` is 7, and every other pair is 8.

`fnv` is FNV-1a. The hash starts at `0xcbf2_9ce4_8422_2325`. Each UTF-8 byte is xored in, then the hash is multiplied by `0x100_0000_01b3`.

This does not add a recipe.
