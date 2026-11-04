# Extraction and one tick

Read 2026-11-04 from `Simulation.step`, `EncounterDirector.extractionArmed`, and `civic-seam-arena-004` on `49759ab`. No countdown was changed. The drawn box stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md).

## Extraction

Extraction arms when M-A, M-B, and M-C are complete, the elite is defeated, the boss is defeated, the player is alive, and the outcome is not failure. Camera count, network blackout, exposure, and the upgrade are not inputs. The arm event is phase 16.

The arena countdown is 300 ticks, and `leaveRule` is `reset`. While armed and the outcome is playing or upgrade selection, a player inside the box decreases `remaining` by 1 (phase 17). At 0, with the player alive, the run succeeds. Leaving after having been inside sets `remaining` back to 300 and emits `extractionReset` on phase 17.

## The tick

While an upgrade choice is pending, a command that is not a legal index with both axes at 0 and dodge clear returns before the clock advances.

After the clock advances, the order is:

1. `Movement.apply`. `dodgeStarted` is phase 4.
2. `resolveAwareness`.
3. `EnemySystem.step`, then each enemy damage amount.
4. `BossSystem.step` while an `algorithmicModerate` is alive, then its damage amount.
5. `Detection.sampleContacts`.
6. `fireCivicPulseIfNeeded`. `weaponFired` is phase 7.
7. `moveProjectilesAndCollectHits`.
8. `resolveDamage`.
9. `resolvePlayerDeathAndContact`. `playerDamaged` is phase 12.
10. `advanceEncounters`, unless the outcome is already failure. `waveStarted` is phase 15. M-C's activation sets `forceLockdown` for the exposure resolve on this tick.
11. `ExposureState.resolveTick`, then `resolveQuietApproach`.
12. When the outcome is failure, the tick returns here.
13. `openEliteGateIfDue`, `resolveObjectives`, `resolveExtraction`.

This does not reorder the step.
