# Lockdown frame

Read 2026-11-04 from `VFXRenderer.lockdownPulse` on `e4ff026`. No tint was changed.

The world tint stays in [lockdown-tint-2026-11-04.md](lockdown-tint-2026-11-04.md). The visible size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The effect layers stay in [world-layer-order-2026-11-03.md](world-layer-order-2026-11-03.md).

Four bars of thickness 6 cover the edges of the visible frame, on the screen effect layer. The fill is red 0.85, green 0.20, blue 0.18, alpha 0.55, and the stroke is clear.

Reduced motion or reduced flash holds those bars at alpha 1. Otherwise they start at alpha 0 and fade in over 0.3 of the presentation lifetime. A broken ring at the player, on the world effect layer, uses the same colour, radius 20, 6 segments, and line width 4. The caps are round. Each segment draws 0.62 of its share of the circle. The ring scales to 12 and fades out over the lifetime.

This does not change the tint.
