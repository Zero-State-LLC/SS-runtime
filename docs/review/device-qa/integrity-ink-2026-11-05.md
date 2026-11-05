# Integrity ink

Read 2026-11-05 from `HUDRenderer.drawIntegrity` on `344ed78`. No integrity total was changed.

The quarter test stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The inset fill stays in [exposure-fills-2026-11-04.md](exposure-fills-2026-11-04.md). The label face stays in [control-chrome-2026-11-04.md](control-chrome-2026-11-04.md).

The drawn ratio divides by `max(1, playerMaxIntegrity)`. The healthy fill is white 0.88 at alpha 0.9. The quarter test uses the critical colour. The numeral is the integer, size 9, in the text colour, centred on the bar.

This does not change an integrity total.
