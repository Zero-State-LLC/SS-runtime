# The telemetry sample

Read 2026-11-05 from `RunTelemetrySnapshot` on `ef68565`. No ceiling was changed. The peak store stays in [device-sample-2026-11-05.md](device-sample-2026-11-05.md). Frame time stays in [frame-times-2026-11-05.md](frame-times-2026-11-05.md). The finished-run predicate stays in [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md). The civic slots stay in [civic-slots-2026-11-05.md](civic-slots-2026-11-05.md). Destroyed cameras stay in [camera-receipt-2026-11-05.md](camera-receipt-2026-11-05.md). The density scenarios stay in [peak-density-2026-11-05.md](peak-density-2026-11-05.md).

The schema is `run-telemetry-001`. `camerasLive` counts cameras whose integrity is above 0. `enemiesLive` counts enemies that are alive. `projectilesLive` counts projectiles that are alive. `minesLive` counts mines whose `lifeRemaining` is above 0. `civicPoolLive` is `liveCount`. `civicPoolCapacity` is `slots.count`. `allocatorNext` is `nextRaw`. `totalLive` is the sum named in the device-sample note.

Exposure stores the value, the peak, the detection state, and `lockdownEntered`. Damage stores player integrity, `damageTaken`, and `combat.damageDealt`. The outcome sample stores `destructions.count`, `networkBlackout`, whether extraction is armed, and `bossDefeated`. Its `terminal` flag is `outcome != .playing`.

`canonical` writes the tick and `allocatorNext` as unsigned, the counts as integers, the flags as bools, and the schema, the outcome, and the detection state as strings.

This does not settle a ceiling.
