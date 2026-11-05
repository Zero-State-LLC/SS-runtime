# Unbacked body

Read 2026-11-05 from `WorldRenderer.renderActors` on `344ed78`. No silhouette was added.

The player blockout stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The outline that replaces the stroke stays in [faction-outline-2026-11-04.md](faction-outline-2026-11-04.md). The contour stays in [actor-silhouettes-2026-11-04.md](actor-silhouettes-2026-11-04.md).

An enemy whose reaction, state clip, and fallback clip all fail to draw gets the silhouette. `algorithmicModerate` fills white 0.30. `improperSearchDaemon` fills white 0.42. Any other role fills white 0.55. The same pass clears that shape's stroke and adds the faction outline.

A defeated body plays its defeat clip where that clip is backed. That loop builds no silhouette.

This does not add a silhouette.
