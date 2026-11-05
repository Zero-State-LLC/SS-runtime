# Alert mark

Read 2026-11-05 from `VFXRenderer.alertPop` on `c6da67e`. No awareness rule was changed.

The unaware marker and its lift stay in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The alert event stays in [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md).

`enemyAlerted` draws `!` at the source actor, or at the player when that actor has no known position. The lift is the unaware marker's lift for the enemy's radius, or for 18 when the snapshot has no radius for that enemy. The label is Menlo Bold, size 20, red 0.98, green 0.62, blue 0.18, alpha 0.95, centred, with its bottom on that point. It sits on the world effect layer.

Reduced motion or reduced flash leaves the mark still. Otherwise it starts at scale 0.4, scales to 1.25 over 0.08 seconds and to 1 over the next 0.06 seconds, then waits. The wait is the presentation lifetime minus those 0.14 seconds and minus the 0.12 second fade, and it is never negative. The fade follows the wait.

This does not change an awareness rule.
