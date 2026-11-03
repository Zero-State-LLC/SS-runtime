# Placed decorations against blocking rectangles

Compared 2026-11-03 from the boxes already published on `c700b82`. No rectangle moved. No collision changed. This does not close T1046.

The solid rectangles are the fourteen "rectangle runs" lines in `solid-footprint-2026-11-01.md` and `solid-footprint-twelve-2026-11-02.md`. The decoration boxes are the canvas boxes in `decoration-placement-2026-11-02.md`. Those boxes are edges: the far edge is the near edge plus the size. The two rail strips stay in their unrotated boxes. The phoenix box stays at the 153.6 draw size.

An overlap here means the two boxes share area. Sharing only an edge is not an overlap.

None of the 21 placed canvas boxes shares area with a blocking rectangle.

`dec-17` and `solid-10-grid-island-b` meet at x 1856. The decoration box is x 1856–1904, y 808–952. The solid runs x 1728–1856, y 896–1024. Their y ranges meet from 896 to 952. The shared x edge has no area.
