# Extraction numeral

Read 2026-11-05 from `HUDRenderer.drawExtraction` on `344ed78`. No countdown was changed.

The seconds and the armed ratio stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The stroke and the radius stay in [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md). The text colour stays in [tutorial-plate-2026-11-04.md](tutorial-plate-2026-11-04.md). The label face stays in [control-chrome-2026-11-04.md](control-chrome-2026-11-04.md).

The arc clamps that ratio from 0 to 1. It starts at π/2 and ends at that angle minus a full turn times the clamped ratio. The path is clockwise. The numeral is size 18, in the text colour, centred on the ring.

This does not change a countdown.
