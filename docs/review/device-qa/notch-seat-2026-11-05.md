# Notch seat

Read 2026-11-05 from `HUDRenderer.drawCameraNotches` on `344ed78`. No notch was added.

The count, the fill rule, and the 90-tick window stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md) and [camera-notch-window-2026-11-04.md](camera-notch-window-2026-11-04.md). The step stays in [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md). The accolade colour stays in [title-chrome-2026-11-04.md](title-chrome-2026-11-04.md). The text colour stays in [tutorial-plate-2026-11-04.md](tutorial-plate-2026-11-04.md).

Each notch's centre is the camera-objective centre plus `index * step` in x and minus `1.6 * step` in y. A filled notch uses the text colour. An empty notch has a clear fill. Both use the frame stroke, and the function does not assign a line width. The tamper label is size 11, in the accolade colour.

This does not add a notch.
