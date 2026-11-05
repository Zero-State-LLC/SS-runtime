# Captain mark

Read 2026-11-05 from `VFXRenderer.captainAnticipation` on `c6da67e`. No telegraph length was changed.

The ground shape stays in [telegraph-shapes-2026-11-04.md](telegraph-shapes-2026-11-04.md). The boss ring stays in [telegraph-ring-2026-11-04.md](telegraph-ring-2026-11-04.md). The frame lifetime stays in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md).

`captainTelegraph` is drawn at the source actor, or at the boss, or at the player when neither position is known. It sits on the world effect layer.

Reduced motion or reduced flash draws a diamond at y 70, through (0, 10), (8, 0), (0, −10), and (−8, 0). The stroke is red 0.90, green 0.88, blue 0.80, alpha 0.95, at line width 2. The fill is that colour at alpha 0.4.

Otherwise a circle of radius 52, in that stroke, line width 3, starts at scale 1.4. It scales to 1 and fades to alpha 0.2 over the presentation lifetime.

This does not change a telegraph.
