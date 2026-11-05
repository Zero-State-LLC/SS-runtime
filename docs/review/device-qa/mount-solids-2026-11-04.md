# Mount solids

Read 2026-11-04 from `WorldRenderer.renderSolids` on `e4ff026`. No collision box was changed.

The foundation colours stay in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). A closed gate stays in [gate-barrier-2026-11-04.md](gate-barrier-2026-11-04.md).

The draw rebuilds when the solid count, a centre, or a half-size changes. An unchanged signature returns. A solid whose id starts with `mount-` is omitted from this draw. A gate id is handed to the barrier. Any other solid draws the foundation, and, when the upright texture loads, that sprite on top at the same box.

This does not change a collision box.
