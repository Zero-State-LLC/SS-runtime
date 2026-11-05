# Peak density

Read 2026-11-05 from `PeakDensityProfiler.profile` on `ef68565`. No ceiling was changed.

The digest prefix on the release-candidate filename stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md). `totalLive` on a phone sample stays in [device-sample-2026-11-05.md](device-sample-2026-11-05.md).

`profile` runs one complete-run scenario for each upgrade, under the key `complete-run-<rawValue>`, then `civic-pool-stress`. The report schema is `peak-density-001`. Each scenario keeps the max of cameras, enemies, projectiles, mines, civic-pool live, allocator next, and `totalLive`. Those maxes are independent. The aggregate is the same field-wise max across the scenarios. Canonical scenario keys are sorted.

A complete run uses `Simulation.make(seed: 1)`. It samples, completes encounter `M-A`, samples, arms upgrade selection, samples, steps a command whose axes are 0 and whose upgrade index is that upgrade, samples, completes the combat graph, samples, steps a neutral command, samples, places the player on the extraction center, and samples after every later neutral step while the outcome is `playing`.

The stress run uses seed 1, completes `M-A`, selects `ricochetPulse`, completes the combat graph, and fills the civic pool to `PerformanceThresholds.civicPoolCapacity`. It then takes 120 steps with `moveX` 32767, `moveY` 0, and dodge clear, and samples after each step. The full-stick limit stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md).

Ordinary play does not call `profile`.

This does not change a pool.
