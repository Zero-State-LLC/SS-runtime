# Boss attack resolve

Read 2026-11-04 from `BossSystem.resolve` on `aaa7919`. No attack number was changed. The content table stays in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). The boss-bolt spawn shape stays in [projectile-step-2026-11-04.md](projectile-step-2026-11-04.md). Camera contact is a different cone, in [camera-contact-2026-11-04.md](camera-contact-2026-11-04.md).

`safetyRationale` stores `Cordic.atan2Milli` of the player-minus-boss raw delta and sets the cooldown to the literal 90. The cone test uses that same heading, half-field 35_000, and range 260, and it also requires a clear line of fire. When both pass, `playerDamage` is assigned 18. Init and a phase change clear the stored heading. The live step applies a `playerDamage` above 0 through `applyPlayerDamage`. The published kind for that call is the default already listed in [player-integrity-2026-11-04.md](player-integrity-2026-11-04.md).

`narrowTailoring` fires one bolt at each of the literals −12_000, 0, and 12_000 added to the player heading, then sets the cooldown to the literal 75. The calls pass the content speed, radius, lifetime, and damage as literals.

`temporaryOrder` sets the cooldown to the literal 120. When the emitter list is non-empty it takes `emitters[emitterIndex % count]`, advances the index modulo the count, and stores that emitter with field remaining set to the literal 180.

`independentReview` fires one bolt per lane from `independentReviewLanes`, then sets the cooldown to the literal 105. The six headings are `normalize(i * 60_000)` for `i` from 0 through 5. The lane with the smallest absolute delta to the player heading is dropped. An equal delta keeps the lower offset. Five bolts remain. Those calls pass the content speed, radius, lifetime, and damage as literals.

`fire` builds the boss bolt the projectile step already records. Its velocity is the heading unit scaled by a half-away division of each component times `speedQ8` of the attack speed, over the Q15 scale.

The field pulse uses `playerInField`: `pointInCone` from the emitter position to the player, along the emitter heading, with half the field angle in integer milli-degrees and the emitter range, plus a clear line of fire. A squared distance greater than the range squared is outside, so the range boundary is inside. The heading test passes when the absolute milli-degree difference is at most that half angle.

This does not change an attack number.
