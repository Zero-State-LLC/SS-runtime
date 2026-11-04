# Terminal seal

Read 2026-11-04 from `Simulation` on `30a2cc6`. No outcome was retuned.

`upgradeSelectionPending` is a choice, not a finished run. Success, failure, and invalid are finished. Integrity at or below 0 calls `fail(.playerDeath)` unless the outcome is already failure or invalid.

`fail` sets the outcome to failure, stores the reason, seals the terminal tick and digest once, and emits `runFailed` at phase 18. `succeed` leaves failure and invalid alone, seals the same way, and emits `runSucceeded` at phase 18. A second seal does not replace the stored tick or digest.

The failure reasons are `playerDeath` and `contentInvalid`. The diagnostic codes are `incompatibleIdentity`, `duplicateCommandTick`, `lateOrFutureCommand`, `digestMismatch`, `arenaValidation`, and `spawnFairnessTimeout`. The 300-tick spawn timeout stays in [encounter-waves-2026-11-04.md](encounter-waves-2026-11-04.md).
