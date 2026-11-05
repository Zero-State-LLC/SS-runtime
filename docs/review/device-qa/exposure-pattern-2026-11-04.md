# Exposure bar pattern

Read 2026-11-04 from `HUDRenderer.barPattern` and `HUDLayout.tamperFloor` on `86c05bb`. No threshold was changed.

The glyphs and the notches at 200, 450, 700, and 1000 stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). `tamperSpike` and `tamperFloorPerCamera` stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

`DetectionPresentation.carrier` pairs each state with a pattern: `hidden` is `slackDotted`, `observed` is `diagonalFill`, `tracked` is `crossFill`, `hunted` is `denseChevron`, and `lockdown` is `solidSegmented`. The pattern node is `exposure-pattern`. Its stroke is `HUDPalette.patternInk` and its line width is `1 * framingScale`. The path height is the bar height minus 4.

Marks start at `step / 2` and advance by `step` while `x` is below the width. `slackDotted` steps 16 and draws a vertical stub from y −1 to 1. `diagonalFill` steps 10 and draws from `(x, -half)` to `(x + half, half)`. `crossFill` steps 12 and draws both diagonals. `denseChevron` steps 6 and draws `(x, -half)` to `(x + step / 2, 0)` to `(x, half)`. `solidSegmented` uses the default step 8 and adds a rectangle of width `step / 2` and the path height.

`tamperFloor` returns nil when no camera is destroyed. Otherwise it is `min(1000, tamperFloorPerCamera * camerasDestroyed)`. The marker stroke is `HUDPalette.text` at line width `3 * framingScale`, from `2 * framingScale` above the bar to the same distance below it. The cap is a filled triangle of size `5 * framingScale`, sitting under the bar with its apex toward the bar.

This does not move a notch.
