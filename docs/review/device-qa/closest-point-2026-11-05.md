# The closest point

Read 2026-11-05 from `Circle.penetrates` on `ef68565`. No radius was changed.

The slide and the strict compare stay in [circle-slide-2026-11-04.md](circle-slide-2026-11-04.md). The box edges stay in [box-edges-2026-11-05.md](box-edges-2026-11-05.md).

The closest point clamps each raw axis into the box. The axis is the minimum of the maximum of the center and the box minimum, and the box maximum. Those edges are the integer edges times the Q8 scale. A center already inside both ranges uses itself, so both deltas are 0. The radius in the compare is the radius in units times the Q8 scale.

This does not change a solid.
