# The probe's camera fields

Read 2026-11-05 from `ProbePilot.refreshCameras` and `seen` on `ef68565`. No field was changed. The mount prefix stays in [patrol-fair-2026-11-05.md](patrol-fair-2026-11-05.md). The cone test stays in [boss-attack-resolve-2026-11-04.md](boss-attack-resolve-2026-11-04.md). The line of fire stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md). The offset stays in [anchor-offset-2026-11-05.md](anchor-offset-2026-11-05.md).

An indifferent profile returns before it stores cameras. Each live camera is a snapshot camera whose integrity is above 0 and whose x, y, and heading match a socket. The first matching socket is kept. The stored origin and anchor come from `CameraPlacement` on that socket. The half-angle is the sprite's field angle divided by 2. The range is the sprite's range. The mount id is `mountSolidPrefix` plus the socket id.

Stealth rebuilds the field grid when the live ids change or the walkable solids change. The grid starts clear. A walkable cell is marked when `seen` is true. `seen` is `pointInCone` from the camera origin, at the stored heading, half-angle, and range, with a clear line from that origin to the point.

This does not play a release build.
