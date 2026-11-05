# Ghost file

Read 2026-11-04 from `GhostStore` on `d873e91`. No replace rule was changed.

The replace test stays in [ghost-replay-2026-11-04.md](ghost-replay-2026-11-04.md).

The file lives under Application Support, directory `DailyGhost`, named `\(seed).json`. `load` is absent when the URL, the bytes, the decode, or `record.seed == seed` fails.

`storeIfBest` stores when `GhostRecord.replaces` accepts the candidate. It creates the directory, encodes the record, and writes with `.atomic`. Every other name in the directory is then removed. A thrown write returns false and leaves the previous files.

A rehearsal finishes before any of this. A run stores only when it began as a daily run and was not scenario-seeded. The card's previous best is the loaded tick count, and only when that record's identity is the run's identity. The load for the ghost itself runs off the main thread. Attach keeps the ghost only when the generation still matches.

This does not store a second run.
