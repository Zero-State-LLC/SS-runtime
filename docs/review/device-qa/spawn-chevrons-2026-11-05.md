# Spawn chevrons

Read 2026-11-05 from `VFXRenderer.reinforcementChevrons` on `c6da67e`. No reinforcement count was changed.

The count and the 300-tick caption stay in [heat-caption-2026-11-04.md](heat-caption-2026-11-04.md). The sockets stay in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The visible size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

The projector emits `heatReinforcements` when that tick's reinforcement count is above 0. The marks sit on the screen effect layer. They use the snapshot's spawn sockets, up to six. A socket at the camera centre is skipped.

Each mark is the path (−8, 10), (4, 0), (−8, −10). The stroke is red 0.98, green 0.62, blue 0.18, alpha 0.95, at line width 4. Its rotation is the direction from the camera centre to the socket. Its place is that offset, pulled in so it stays 22 inside the visible frame, and never enlarged past the offset itself.

Reduced motion or reduced flash leaves the mark still. Otherwise it travels 6 points along its rotation over a quarter of the presentation lifetime, returns over the next quarter, and does that pair twice.

This does not change a count.
