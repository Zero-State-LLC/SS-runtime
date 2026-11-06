# The layout check

Read 2026-11-05 from `HUDLayout.validate` on `ef68565`. No rectangle was moved. The map, the 44 floor, and the grow-about-centre stay in [hud-fit-2026-11-04.md](hud-fit-2026-11-04.md). The authored rectangles stay in [control-rects-2026-11-04.md](control-rects-2026-11-04.md).

`validate` takes `hudScale` and does not read it. It maps stick, dodge, and pause through `mapControlRect`. Informational rectangles are not in that loop.

A mapped rect with x or y below 0, or whose far edge passes the safe width or the safe height, appends that name. `clippedElements` is that list sorted. `controlsMeetTouchTarget` is false when any mapped control has width below 44 or height below 44. `allInsideSafeCanvas` is that clipped list empty.

`validate` does not read `seClassSafeWidth` (667) or `seClassSafeHeight` (375).

This does not move a control.
