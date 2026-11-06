# The probe's heading

Read 2026-11-05 from `ProbePilot.withoutChosenCamera` and `choosesCamera` on `ef68565`. No heading was changed. The chosen test and the range stay in [target-order-2026-11-04.md](target-order-2026-11-04.md). The displacement stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md). The shot to an anchor stays in [probe-loud-2026-11-05.md](probe-loud-2026-11-05.md). The vector stays in [probe-sidestep-2026-11-05.md](probe-sidestep-2026-11-05.md).

A command that does not move is returned as it is. An enemy whose integer x and y deltas, squared and added, are at most `closeEnemyRange` squared keeps the command. A command that chooses no camera keeps the command.

Otherwise each heading is tried. The candidate is that heading's vector. The probed cell is the position plus the heading times 3, and it must be walkable at the player radius. The candidate must choose no camera. The score is the heading times the command's components. A strictly higher score replaces the best. A best score above 0 is returned, with the original dodge. None returns the dodge and no move.

`choosesCamera` builds `Movement.displacement` from the command with tick 1, dodge clear, and ghost step clear. A live camera counts when `isChosen` faces its anchor, `inRange` accepts the squared distance to that anchor, and `shotClear` is true.

This does not play a release build.
