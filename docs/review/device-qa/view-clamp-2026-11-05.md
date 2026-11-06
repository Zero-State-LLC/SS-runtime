# The view clamp

Read 2026-11-05 from `CameraFollow.update` on `ef68565`. No framing was changed.

The dead zone, the look-ahead, the gain, and the view size stay in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

On each axis the low bound is the arena minimum plus half the view, and the high bound is the arena maximum minus that half. When low is at or below high, the coordinate stays inside that range. When low is above high, the coordinate is the midpoint of the two bounds.

This does not change the view size.
