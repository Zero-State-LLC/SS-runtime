# Telegraph ring

Read 2026-11-04 from `TelegraphRing` and `BossCourtRenderer` on `5d954be`. No telegraph length was changed.

The preview shapes stay in [telegraph-shapes-2026-11-04.md](telegraph-shapes-2026-11-04.md). The phase colours and the 60-tick crossfade stay in [court-light-2026-11-04.md](court-light-2026-11-04.md).

A ring is drawn for a telegraph whose owner is the boss. The radius starts at 72 and ends at 18. Progress is `(total - remaining) / max(1, total)`, with remaining clamped from 0 to that total. The stroke starts at width 3 and alpha `0.55 + 0.45 * progress`. In the last third of the telegraph, and when reduced motion is off, a cosine pulse of period 12 ticks adds up to 2 to the width and up to 0.15 to the alpha, and the alpha stays at most 1. The ring is an unfilled ellipse at the telegraph's point. Its colour is red 1, green 0.86, blue 0.62. The layer is half a step above the telegraph layer.

The court light is a multiply sprite at z 790, sized at 1.4 times the visible width and height. Its shader mixes the centre multiplier into the edge multiplier with `smoothstep(0.20, 0.72, length(q) * 0.70710678)`, where `q` is the texture coordinate stretched from the centre to ±1. A neutral palette hides the sprite.

This does not change a phase colour.
