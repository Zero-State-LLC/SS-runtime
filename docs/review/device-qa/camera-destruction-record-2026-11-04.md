# Camera destruction record

Read 2026-11-04 from `destroyCamera` on `93f6d67`. No camera was added.

Each destruction stores the camera id, the tick, the housing family, whether the camera was detecting, the source string `ricochet` or `baseProjectile`, the exposure before the destruction, and `min(1000, before + tamperSpike)` as the after value. `triggeredLockdown` is set when that sum is at least 1000 and lockdown has not been entered.

When the record count reaches 8 and `networkBlackout` is still false, the run sets `networkBlackout` and emits `allCamerasDestroyed` at phase 10 with destroyed count 8 and total count 8.

The same tick's spikes are the records whose tick is the current tick, sorted by camera id, each contributing one tamper spike. The spike of 150 stays in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md). The HUD copy stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The mix duck stays in [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md).
