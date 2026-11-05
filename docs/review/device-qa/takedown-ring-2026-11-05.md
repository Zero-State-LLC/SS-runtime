# Takedown ring

Read 2026-11-05 from `TakedownRing` on `344ed78`. No freeze was changed.

The 70 ms freeze stays in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). The streak string stays in [takedown-streak-2026-11-04.md](takedown-streak-2026-11-04.md).

`takedown` runs after the step and before the redraw. It places a ring at each target the previous frame still remembers. That frame stored the player, each enemy then in the snapshot, each camera, and each projectile. An id the table does not hold draws no ring.

The ring is named `takedown-ring`. A filled circle of radius 44 uses white 0.5 at alpha 0.55 and a clear stroke. A second circle of that radius has a clear fill, line width 3, and a stroke of white 0.92 at alpha 0.95. Reduced flash uses white 0.62 at alpha 0.9 for that stroke. Reduced motion leaves the scale at 1. Otherwise the node starts at scale 0.55 and scales to 1.15 over 0.35 seconds. The node fades out over 0.35 seconds and then leaves the scene.

This does not change the freeze.
