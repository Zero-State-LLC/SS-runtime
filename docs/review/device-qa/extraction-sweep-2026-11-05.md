# Extraction sweep

Read 2026-11-05 from `HUDRenderer.drawExtraction` on `c6da67e`. No countdown was changed.

The remaining ratio and the seconds formula stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The ring's stroke and radius stay in [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md).

The ring is drawn while extraction is armed. The arc starts at π/2 and runs clockwise through a full turn times the remaining ratio. The numeral is `extractionSeconds`, Menlo Bold, size 18, white 0.95, at the ring's centre. The size is multiplied by the framing scale.

This does not change the countdown.
