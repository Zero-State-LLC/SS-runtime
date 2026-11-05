# Exposure fills

Read 2026-11-04 from `HUDPalette.exposure` and `HUDRenderer.meter` on `e4ff026`. No threshold was changed.

The ratio and the four notches stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The patterns and the tamper marker stay in [exposure-pattern-2026-11-04.md](exposure-pattern-2026-11-04.md).

The frame stroke is white 0.80 at alpha 0.75, line width `1` times the framing scale. The fill is a rectangle from the left of that frame, inset by 1 and shorter than the frame by 2. Its width is the clamped ratio times the frame width.

Hidden is white 0.55 at alpha 0.8. Observed is white 0.68 at alpha 0.85. Tracked is red 0.90, green 0.78, blue 0.35, alpha 0.9. Hunted is red 0.93, green 0.58, blue 0.30, alpha 0.92. Lockdown is red 0.95, green 0.40, blue 0.32, alpha 0.95.

This does not change a threshold.
