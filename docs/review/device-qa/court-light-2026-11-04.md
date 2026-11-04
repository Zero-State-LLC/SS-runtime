# Court light

Read 2026-11-04 from `CourtLighting` on `30a2cc6`. No palette was changed.

Each boss phase lights the world layer. The HUD is left alone. Public safety uses centre `(0.90, 0.95, 1.00)` and edge `(0.74, 0.84, 1.00)`. Civil liberties uses centre `(1.00, 0.88, 0.66)` and edge `(0.92, 0.70, 0.42)`. Temporary safeguard uses centre `(1.00, 0.66, 0.62)` and edge `(0.78, 0.34, 0.32)`. Independent review leaves the centre at `(1, 1, 1)` and uses edge `(0.62, 0.76, 1.00)`.

A phase change crossfades linearly over 60 ticks from the light already on screen. Reduced flash keeps 60 percent of each palette's saturation about its luma. No channel factor exceeds 1. The phase names stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The attacks stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md).
