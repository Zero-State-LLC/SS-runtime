# Encounter completion

Read 2026-11-04 from `Simulation.advanceEncounters` on `006304e`. No wave total was changed.

Queuing the next wave stays in [encounter-waves-2026-11-04.md](encounter-waves-2026-11-04.md). This note is the tick that finishes the encounter.

When the spawn queue is empty and `living` is 0, and a later wave exists, that wave is queued. When no later wave exists, `spawned >= spec.totals` sets `completed` and emits `mobEncounterCompleted` at phase 15 with `encounterId`. A short `spawned` leaves the encounter incomplete.

For `M-A`, that completion also sets `upgrade.pending`, sets the outcome to `upgradeSelectionPending`, and calls `tutorial.noteMobAComplete`. That call sets the tutorial phase to `upgrade`. The card that phase shows is [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). `applyUpgrade` is [upgrade-cards-2026-11-04.md](upgrade-cards-2026-11-04.md). The elite and boss spawn gates stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md).
