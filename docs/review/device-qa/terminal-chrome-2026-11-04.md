# Terminal chrome

Read 2026-11-04 from `HUDRenderer.drawTerminal` on `e4ff026`. No result row was added.

The panel rectangles stay in [terminal-surface-2026-11-04.md](terminal-surface-2026-11-04.md). The outcome lines stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). `NEW BEST` stays in [run-card-2026-11-04.md](run-card-2026-11-04.md).

A scrim of white 0.04 at alpha 0.72 covers the safe rectangle. The panel fill is white 0.16 at alpha 0.92. Its stroke is white 0.80 at alpha 0.75, and the corner radius is 4. The title is size 18, white 0.95. A row label is size 11, white 0.68, aligned left. A row value is size 12. The value uses red 0.55, green 0.85, blue 0.70 when the text is `NEW BEST`, or when the medals row contains `NEW`. Any other value is white 0.95.

The medals value shrinks by half a point while it is wider than the row's room and the size is still above 6. That room is the panel width, minus twice the card inset, minus 64. Restart and Share use size 13. Rehearse uses size 10. Each button has corner radius 3 and the same panel fill and frame stroke. The labels are Menlo Bold, and the size is multiplied by the framing scale.

This does not add a result row.
