# Boss attack clock

Read 2026-11-04 from `BossSystem.step` on `aaa7919`. No telegraph was changed. The recovery literals and the phase table stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). Locomotion stays in [captain-path-2026-11-04.md](captain-path-2026-11-04.md). Half-away stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

The live step runs only while a living `algorithmicModerate` exists. It passes the content boss speed and the content base contact. `courtLockdown` is `exposure.lockdownEntered`.

A phase change, while the boss is alive, marks every boss bolt dead and emits `bossPhaseChanged` at phase 16 with the before phase, the after phase, and the remaining integrity. The bolts stay in the list. `syncPhase` takes the first receipt-order band whose minimum the current hp still meets, or the last phase when none still meets. One hit can skip bands. It zeroes the sequence index, the telegraph, the attack timer, the cooldown, the current attack, the locked heading, and the field, clears the active emitter, and sets recovery to the literal 45. The emitter index stays.

Locomotion runs next. Contact damage per second is a half-away division of base contact times the phase contact numerator, over 100.

While a field is stored, its remaining count decreases by 1 before any recovery return. Recovery, a telegraph, and a cooldown leave that countdown running. A remaining count that is a multiple of 30, including the tick it reaches 0, can report an observation pulse while the emitter is still stored. The cone is in [boss-attack-resolve-2026-11-04.md](boss-attack-resolve-2026-11-04.md). The amount is in [observation-pulse-2026-11-04.md](observation-pulse-2026-11-04.md). Reaching 0 then clears the emitter.

Recovery above 0 then decreases by 1 and returns. The attack timers stay where they are on that tick.

Otherwise an attack timer above 0 decreases by 1, and reaching 0 clears the current attack. That branch falls through. Reaching 0 clears the attack before the telegraph check. The four resolves store no positive attack timer.

Otherwise a telegraph above 0 decreases by 1. At 0, with a current attack still set, `resolve` runs and then `bossAttackStarted` is emitted at phase 16 with that attack id and the phase id. The event is the resolve tick. The tick returns, so a cooldown stored by the resolve waits until a later tick. A telegraph that reaches 0 with no current attack returns without resolving.

Otherwise a cooldown above 0 decreases by 2 while court lockdown is entered, and by 1 otherwise, and it stops at 0. The tick returns. The faster step is the cooldown. The telegraph length stays the literal set when the attack was chosen.

Otherwise the step takes `sequence[sequenceIndex % count]`, increments the index, stores that attack, and sets the telegraph to the literal 45, 30, 48, or 60 for safety, narrow, temporary, and independent. Those match the content table. This tick does not resolve.

`bossPhase` stores the phase raw value. `phasesReached` appends that raw value the first tick it is current, in first-seen order. The snapshot order is in [combat-authority-node-2026-11-04.md](combat-authority-node-2026-11-04.md).

A boss death clears the field, the emitter, the current attack, the telegraph, and the attack timer, and marks boss bolts dead.

This does not change a telegraph.
