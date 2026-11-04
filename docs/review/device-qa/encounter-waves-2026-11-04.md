# Encounter waves

Read 2026-11-04 from `combat-content-009`, `civic-seam-arena-004`, and `Simulation.advanceEncounters` on `49759ab`. No wave was added.

An encounter activates when the player is inside its trigger. The first wave's first spawn is that tick plus the wave delay. A spawn that fits schedules the next one interval later. A spawn that does not fit goes back on the queue and retries after 30 ticks. At 300 defer ticks the run invalidates. The next wave is queued when the spawn queue is empty and nothing from the encounter is still alive, and its first spawn waits that wave's delay. A missing delay decodes as 0. `waveStarted` is phase 15. Member keys are sorted by archetype id, and the queue repeats each count in that order. Heat reinforcements are appended after them. M-C's activation sets `forceLockdown`. What that does to exposure stays in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

Triggers are half-size (96, 96). M-A is `trigger-M-A` at (960, 576), zone Z-03, total 14. M-B is `trigger-M-B` at (1280, 1088), zone Z-04, total 17. M-C is `trigger-M-C` at (1664, 832), zone Z-05, total 25, activation exposure 1000, initial delay 60.

| Wave | Delay | Interval | Members |
|---|---|---|---|
| A1 | 60 | 30 | informant 3, fog 2 |
| A2 | 60 | 30 | cable 2, informant 2 |
| A3 | 0 | 24 | informant 2, fog 2, witch 1 |
| B1 | 60 | 24 | informant 2, cable 2, witch 1 |
| B2 | 75 | 24 | informant 2, fog 2, vendor 2 |
| B3 | 0 | 20 | informant 2, cable 2, witch 2 |
| C1 | 45 | 20 | informant 3, cable 2 |
| C2 | 60 | 20 | fog 2, witch 2, vendor 1 |
| C3 | 75 | 18 | informant 2, cable 3, vendor 2 |
| C4 | 0 | 18 | informant 2, fog 2, witch 2, vendor 2 |

Totals are 5+4+5, 5+6+6, and 5+5+7+8.

This does not add a wave.
