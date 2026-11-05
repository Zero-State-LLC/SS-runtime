# Camera reticle

Read 2026-11-04 from `VFXRenderer.acquireReticle` on `e4ff026`. No detection band was changed.

The pool and the frame lifetime stay in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md). The effect layers stay in [world-layer-order-2026-11-03.md](world-layer-order-2026-11-03.md). Detection bands stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

The projector emits `cameraAcquire` when a detection-state event moves from hidden to observed. The reticle is drawn at the player, on the world effect layer. It is four corners of a 56 by 56 square, each arm 12, in red 0.95, green 0.78, blue 0.20, alpha 0.95, at line width 2.

Reduced motion or reduced flash holds the reticle at alpha 0.9, then sets alpha 0.4 at 0.6 of the presentation lifetime. Otherwise the reticle scales from 1.6 to 1 over 0.7 of that lifetime, and a bar 52 by 1.5, in that colour at alpha 0.6, travels from y 26 to y −26 over the lifetime.

This does not change a detection band.
