# Replay commands

Read 2026-11-04 from `ReplayEnvelope.load` on `fcab4e5`. No command was rewritten.

The four identity strings are [replay-identity-2026-11-04.md](replay-identity-2026-11-04.md). The ghost fade and the replace rule are [ghost-replay-2026-11-04.md](ghost-replay-2026-11-04.md).

A missing incoming command becomes `PlayerCommand.neutral`: move `(0, 0)`, dodge clear, upgrade index omitted. An incoming command whose tick is not the tick just advanced invalidates `lateOrFutureCommand`.

`load` rejects an identity that is not compatible, and a seed whose number has a negative `doubleValue` (`invalidSeed`). A tick below 1 after the uint64 conversion is `invalidCommandRange`. A duplicate tick is rejected. After the first command, each tick must be strictly greater than the previous one. Move axes must sit inside `axisMinimum` and `axisMaximum`, −32,767 and 32,767. An `upgradeChoiceIndex` that arrives as an integer is stored when it is 0, 1, or 2, and rejected outside that. An absent index stays nil. A value that is not an integer is left unread, so the index stays nil. `expectedFinalDigest`, when present, must have count 64 or the load returns `invalidJSON`. The check is that count. An absent digest stays nil.

`isNeutral` is move x 0, move y 0, dodge clear, and no upgrade index. `GhostRecord` stores the commands for which `isNeutral` is false. A missing command and a neutral command step the simulation the same way, so the stored ghost omits those steps.
