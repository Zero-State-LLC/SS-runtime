# Court capture

Read 2026-11-05 from `GameSession` on `5a71391`. No court was written to disk.

Restart and Rehearse Court stay in [restart-and-rehearsal-2026-11-04.md](restart-and-rehearsal-2026-11-04.md).

`CourtSnapshot` holds the seed, the `Simulation`, and the command log. On the step where `bossRuntime` is present and `courtReached` is still false, the session sets `courtReached` and stores `courtStartTick` as that tick. The command log already holds the command that advanced the tick. A run that is not a rehearsal stores the snapshot. A rehearsal leaves the stored snapshot as it was. The session comment says a rehearsal is not a run: it is never archived, stored as a best, or awarded medals. The snapshot stays in memory for its seed.

This does not write the court to disk.
