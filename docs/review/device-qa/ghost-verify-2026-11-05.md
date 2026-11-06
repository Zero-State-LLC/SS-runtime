# The ghost's second check

Read 2026-11-05 from `GhostRun` on `ef68565`. No record was rewritten.

The build, the fade, and the lead stay in [ghost-replay-2026-11-04.md](ghost-replay-2026-11-04.md). The envelope's upgrade index stays in [replay-commands-2026-11-04.md](replay-commands-2026-11-04.md).

`commandsAreOrdered` returns false when a command carries an upgrade index and `UpgradeID.from` returns nil.

`replay` returns nil when a step leaves the tick unchanged. After a replay whose tick and digest match the record, the ghost that is kept is a new `Simulation.make` of that seed. `advance` steps while the tick is below the minimum of the live tick plus the lead and the recorded length, and it stops when that simulation is already terminal.

This does not change a ghost.
