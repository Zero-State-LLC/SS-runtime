# Phase slam

Read 2026-11-05 from `VFXRenderer.phaseBreak` on `c6da67e`. No phase name was changed.

The four phase words stay in [boss-bar-2026-11-04.md](boss-bar-2026-11-04.md). The frame lifetime stays in [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md). The effect layers stay in [world-layer-order-2026-11-03.md](world-layer-order-2026-11-03.md).

The projector emits `bossPhaseBreak` when a phase-change event has a before value and an after value. The label splits that after string where an uppercase letter starts a new word, uppercases each word, and joins the words with a space. A change with no before is not drawn.

The label is Menlo Bold, size 30, red 0.90, green 0.88, blue 0.80, alpha 0.95, centred at y 70, on the screen effect layer. Reduced motion or reduced flash holds it at alpha 1 and draws no ring.

Otherwise it starts at scale 2.2 and alpha 0, scales to 1 and fades in over 0.09 seconds, waits 0.6 of the presentation lifetime, and fades out over 0.3 of the lifetime. When the boss position is known, a broken ring at that point uses the same colour, radius 40, 8 segments, and line width 4. The caps are round. Each segment draws 0.62 of its share of the circle. The ring scales to 5.5 and fades out over the lifetime.

This does not change a phase name.
