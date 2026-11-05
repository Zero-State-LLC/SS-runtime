# Exposure brackets

Read 2026-11-04 from `VFXRenderer.edgeBrackets` on `e4ff026`. No threshold was changed.

The notches stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The patterns stay in [exposure-pattern-2026-11-04.md](exposure-pattern-2026-11-04.md). The visible size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The frame lifetime stays in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md).

The projector emits `exposureThreshold` when a detection-state event's after value is tracked, hunted, or lockdown. The brackets sit on the screen effect layer. Each side is the visible size minus 24. Each arm is 34. The stroke is red 0.98, green 0.62, blue 0.18, alpha 0.95, at line width 3.

Reduced motion or reduced flash holds alpha at 1, then sets alpha 0.35 at half the presentation lifetime. Otherwise alpha starts at 0.25, rises to 1 over 0.35 of the lifetime, then falls to 0 over 0.65 of the lifetime.

This does not change a threshold.
