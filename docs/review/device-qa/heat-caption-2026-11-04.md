# Heat caption

Read 2026-11-04 from `HeatCaptionProjector` on `86c05bb`. No count was changed.

The reinforcement table stays in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). The jammer reduction stays in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md).

The state read for a wave is the `before` string on the first `detectionStateChanged` event this tick, when that string decodes as a detection state. Otherwise it is the current state. Each `waveStarted` event whose `encounterId` is a string replaces the stored caption with that wave's own count from `HeatSpec.reinforcements`. The last such event is the one that stays. The companion total adds every wave's count and is stored as `lastHeatReinforcements`.

The string is `REINFORCEMENTS +<n> • <STATE>` when the count is above 0. A count of 0 stores no string, so a later empty wave clears an older caption. The caption is drawn while `tick` is at or after `shownAt` and fewer than 300 ticks have passed. The rectangle is the boss-integrity slot: x `422 - 180`, y 82, width 360, height 24. The label uses the critical colour.

`GameScene` passes the current detection state, `content.heat`, and `upgrade.signalJammer`.

This does not change a reinforcement count.
