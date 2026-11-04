# Civic Pulse

Read 2026-11-04 from `Targeting` and `Simulation.fireCivicPulseIfNeeded` on `49759ab`. No weapon number was changed. The presentation cue stays in [player-weapon-cues-2026-11-03.md](player-weapon-cues-2026-11-03.md).

| Field | Value |
|---|---|
| Range | 512 |
| First tick | 30 |
| Cadence | every 30 ticks, when `tick % 30 == 0` |
| Speed | 12 units per tick |
| Radius | 4 |
| Lifetime | 45 |
| Max travel | 540 |
| Live cap | 32 |
| Enemy damage | 10 |
| Camera damage | 1 |

The shot is skipped when the tick is before 30, the cadence misses, the pool is full, or `Targeting.select` returns no target. The body is placed one velocity step ahead of the player, with age 1. A camera target is stored on the shot. An enemy target aims with that enemy's velocity.

A placed camera starts at integrity 3, so camera damage 1 destroys it on the third hit. Placement counts are in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md).

The cue note's gap of 6 ticks is the voice gap. The 30 above is the fire cadence.

This does not add a weapon.
