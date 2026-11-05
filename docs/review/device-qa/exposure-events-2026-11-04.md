# Exposure events

Read 2026-11-04 from `Simulation.emitExposure` on `006304e`. No exposure band was changed.

The band edges, the jammer, the decay, and the floor stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md). This note is the events that resolution emits.

Each entry in `resolution.changes` emits `exposureChanged` at phase 13, in list order. The payload is `before`, `after`, and `reason`. The reason string is `ExposureReason.rawValue`: `cameraContact`, `recovery`, `cameraTamper`, `fogPulse`, `observationPulse`, or `forcedLockdown`.

When `stateAfter` differs from `stateBefore`, one `detectionStateChanged` is emitted at phase 14. The payload is both states' raw values. When `lockdownEnteredThisTick` is set, one `lockdownEntered` is emitted at phase 14. Its reason is `resolution.reason`, the resolution's reason, after the detection event when both fire.
