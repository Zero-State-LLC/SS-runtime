# Pacing window

Read 2026-11-05 from `PacingTimeline.observe` on `ef68565`. No window was changed.

The zone names stay in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). The tick rate stays on `SimulationClock.ticksPerSecond`, which is 60.

This type does not write simulation state. `spawnAlley` starts at tick 0. A later observe records a segment only on its first start. `cameraCorridor` starts when the player zone is `Z-02`. `civicPlaza` starts on `waveStarted` for `M-A`, `pressureRoute` on `M-B`, and `lockdownRing` on `M-C`. `captainCourt` starts on `bossActivated`. `extraction` starts on `extractionArmed`. `endTick` is the first `runSucceeded`.

Start seconds are the start tick divided by 60. `segmentsOffTarget` includes a segment that never started, and a segment whose start second, after `rounded()`, is outside its window. The windows are `spawnAlley` 0 through 5, `cameraCorridor` 5 through 30, `civicPlaza` 30 through 65, `pressureRoute` 65 through 110, `lockdownRing` 110 through 240, `captainCourt` 240 through 330, and `extraction` 330 through 360. `runWithinTarget` is nil until `runSucceeded`, and then it is whether that end second, after `rounded()`, is inside 300 through 480.

This does not close T903 or T904.
