# Stick zone

Read 2026-11-05 from `ControlLayout.make` on `87ab159`. No stick rectangle was moved.

The authored rectangles stay in [control-rects-2026-11-04.md](control-rects-2026-11-04.md). The dead zone stays in [touch-command-2026-11-04.md](touch-command-2026-11-04.md).

The drawn stick stays the mapped circle. A touch is accepted in a zone of the safe rectangle. The zone starts at 30 percent of the safe height and runs to the bottom. Right hand takes x 0 and half the safe width. Left hand takes the other half, starting at half the safe width. The zone is then clipped to the safe rectangle. Point y grows downward.

This does not move a stick rectangle.
