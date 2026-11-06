# The probe's hide

Read 2026-11-05 from `ProbePilot.hideAbove` and `hide` on `ef68565`. No threshold was changed. When `decide` calls `hide` stays in [probe-order-2026-11-05.md](probe-order-2026-11-05.md). The per-camera floor stays in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md). The notches stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The field grid stays in [probe-fields-2026-11-05.md](probe-fields-2026-11-05.md). A hazard stays in [probe-sidestep-2026-11-05.md](probe-sidestep-2026-11-05.md). The path stays in [probe-replan-2026-11-05.md](probe-replan-2026-11-05.md).

`hideAbove` multiplies `tamperFloorPerCamera` by the cameras destroyed. A floor below 200 is returned as it is. A floor below 450 returns the greater of that floor plus 24 and 400. Any higher floor returns `Int.max`.

`hide` stands with an empty command when the player's cell is outside every field and `seen` is false. Otherwise it searches from the nearest walkable cell. The first cell outside every field and outside every hazard is the goal. The call then navigates there. No such cell returns an empty command.

This does not play a release build.
