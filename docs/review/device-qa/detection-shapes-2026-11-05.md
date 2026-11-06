# The detection shapes

Read 2026-11-05 from `DetectionPresentation.carrier` on `ef68565`. No state was added. The bar patterns stay in [exposure-pattern-2026-11-04.md](exposure-pattern-2026-11-04.md). The drawn label stays in [detection-ink-2026-11-05.md](detection-ink-2026-11-05.md).

The icon beside each pattern is `openEye` for hidden, `halfEye` for observed, `bracketEye` for tracked, `boxedEye` for hunted, and `sealedEye` for lockdown. [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md) calls the detection mark a glyph and names the upgrade glyphs. It does not name these icon shapes.

`criticalStatesRemainDistinct` returns false when any `icon|pattern` key repeats. The five pairs differ, so it returns true. `reducedPresentationCarriers` stores `carrier(for:)` for each ordered state. It does not substitute a different carrier.

This does not add a state.
