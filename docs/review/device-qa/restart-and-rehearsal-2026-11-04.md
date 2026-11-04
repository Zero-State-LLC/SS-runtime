# Restart and rehearsal

Read 2026-11-04 from `GameScene` and `GameSession` on `93f6d67`. No control was added.

The Restart control calls `GameScene.restartRun` with no seed, so the new run keeps the seed of the run that just ended. The intro does not play again. The touch controller is reset, the pending upgrade choice is cleared, and a stored court snapshot is dropped when its seed differs.

Rehearse Court restores the court snapshot. It sets the rehearsal flag, skips the intro, clears the ghost, and marks the terminal receipt stored so the rehearsal is not archived as a device run. It does nothing when no court snapshot is stored.
