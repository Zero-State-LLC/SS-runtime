# Objective ink

Read 2026-11-05 from `HUDRenderer.drawObjectives` on `344ed78`. No objective sentence was changed.

The sentences stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). When a label is present stays in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). The accolade colour stays in [title-chrome-2026-11-04.md](title-chrome-2026-11-04.md). The label face stays in [control-chrome-2026-11-04.md](control-chrome-2026-11-04.md).

The combat label is size 10, in the text colour, aligned to the left edge of its mapped rect. The camera label is size 9, aligned the same way. It uses the accolade colour while `networkBlackout` is set, and the text colour otherwise. The camera label is drawn while the counter is visible or pinned.

This does not change an objective sentence.
