# Circle slide

Read 2026-11-04 from `Collision.slideCircle` on `fcab4e5`. No radius was changed. The player radius stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md).

The move is resolved on X and then on Y. Solids are tested in UTF-8 id order. Each axis first clamps the center so the circle stays inside the bounds by its radius. If that circle penetrates any solid, the axis is put back.

Penetration is a squared distance strictly inside the radius. A circle that only touches the box keeps the move on that axis.

The player step, the aware enemy step, and the unaware patrol move all use this slide.

This does not change a solid.
