# Daily seed

Read 2026-11-04 from `DailyRun` on `30a2cc6`. Placement was not changed.

The UTC day key is `year * 10000 + month * 100 + day`. The domain constant is `0x5353_4441_494C_5900`. A candidate is `SplitMix64.mix(dayKey ^ domain ^ salt)`, and the salt starts at 0. The seed is the first candidate whose camera placement selects and passes the runtime asserts `Simulation.make` uses. The player takes the first entity id before that selection.

The title line is `DAILY RUN · YYYY-MM-DD`. The simulation receives the seed. It does not receive the date.
