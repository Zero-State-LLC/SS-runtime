# Heading draw

Read 2026-11-04 from `Geometry` on `e4ff026`. No heading was changed.

The clockwise system stays in [millidegree-2026-11-04.md](millidegree-2026-11-04.md). Telegraph colours stay in [telegraph-shapes-2026-11-04.md](telegraph-shapes-2026-11-04.md). The clipped patrol outline stays in [patrol-cone-outline-2026-11-04.md](patrol-cone-outline-2026-11-04.md).

`radians` is the negation of the millidegrees, divided by 1000, in radians. `spanRadians` is the same conversion without the negation. A cone or an emitter-field telegraph passes twice the stored half-angle into `conePath`. That function halves the span, so the arc's half-angle is the stored half-angle. The arc runs in SpriteKit's direction from the heading minus that half to the heading plus it, and the path closes through the origin. A lane telegraph uses `lanePath`: a corridor of the given width, with the perpendicular `(-dy, dx)`.

A stored outline is drawn with the coordinates it already has. A decoration's rotation is the positive conversion. It does not use `radians`.

This does not change a heading.
