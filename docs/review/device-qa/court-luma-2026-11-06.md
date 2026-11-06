# The court luma

Read 2026-11-06 from `CourtMultiplier`, `CourtPalette.saturation`, `CourtPalette.lerp`, and `CourtLightTracker.update` on `ef68565`. No palette was changed.

The four RGB triples, the 60-tick crossfade, the 0.60 reduced-flash fraction, and the fade from the light already on screen stay in [court-light-2026-11-04.md](court-light-2026-11-04.md).

`luma` is `0.2126 * red + 0.7152 * green + 0.0722 * blue`. `maxChannel` is the largest of the three channels. `spread` is that largest minus the smallest. `saturation` sets each channel to `l + (channel − l) * fraction`, where `l` is that luma. `CourtPalette.saturation` does this to the center and to the edge.

`lerp` clamps `t` to 0…1. It uses `u = 1 − t`, so `t = 0` is `a` and `t = 1` is `b`. Each channel is `a * u + b * t`. `CourtPalette.lerp` does this on the center and on the edge. The neutral multiplier is red 1, green 1, blue 1.

In the tracker, elapsed is 0 when `tick` is below `changedAt`. Otherwise elapsed is the difference.

This does not change a palette.
