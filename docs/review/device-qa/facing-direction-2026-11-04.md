# Facing direction

Read 2026-11-04 from `ClipFrameLibrary.direction(forFacing:)` and `ClipAlignment.cardinalDirection` on `006304e`. No facing letter was added.

The snapshot stores a letter. The player's letter is `direction(forFacing:)` of `player.facing`. An enemy's letter is `ActorClipProjection.direction`, which calls the same function on that enemy's velocity.

A velocity whose raw x and raw y are both 0 is `s`. When `abs(x)` is greater than or equal to `abs(y)`, positive x is `e` and any other x is `w`. Otherwise positive y is `n` and any other y is `s`. An equal-absolute diagonal takes `e` or `w`. World `+y` is north: a velocity of `(0, 3)` is `n`.

`cardinalDirection` is a second function. The sector is `((MilliDeg.normalize(heading) + 45_000) / 90_000) % 4`. Sector 0 is `e`, 1 is `s`, 2 is `w`, and the remaining sector is `n`. Heading 45_000 is sector 1, so `s`.

`ClipAlignment.project` uses `cardinalDirection` when the clip lists directions. `PresentationSnapshot` and the renderer use `direction(forFacing:)`. `ClipAlignmentTests` checks that the two functions agree at headings 0, 90_000, 180_000, and 270_000.
