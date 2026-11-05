# The probe's order

Read 2026-11-05 from `ProbePilot.decide` and the app target in `project.yml` on `ef68565`. No route was changed. The launch flag stays in [shell-host-2026-11-04.md](shell-host-2026-11-04.md). The wall-follow stays in [waypoint-pilot-2026-11-05.md](waypoint-pilot-2026-11-05.md). The player radius stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md). Patrol sight and awareness sight stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). The pulse range stays in [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md). The close-enemy constant stays in [target-order-2026-11-04.md](target-order-2026-11-04.md).

`project.yml` excludes `ProbePilot.swift` from the Release app target. A Debug build compiles it. The pilot reads only `PresentationSnapshot`.

`competent` stores dodge on and a camera style of indifferent. `firstRun` stores `perceptionDelayTicks` 15 and `usesDodge` false. `stealth` and `loud` store dodge on and those camera styles. `decide` and `steer` do not read `perceptionDelayTicks`. The file comment says route knowledge is perfect.

`stalled` is `60 * 180` ticks on one objective node. `command` calls `steer`, then stores whether the returned move is nonzero. `steer` calls `decide`.

For stealth outside lockdown, a stored override returns the unfiltered command and spends one override tick. A filter that changes the command and stays at a distance below 12 from `lastDetourPosition` counts a stuck tick. At 15 of those ticks it sets `detourOverrideTicks` to 60 and returns the unfiltered command. A distance of at least 12 clears that stuck count.

`decide` rebuilds the grid when the solids change. A mine's hazard radius is the mine radius plus `PlayerBody.radiusUnits` plus 8. Movement of at most 2 for more than 20 ticks clears the path and flips `orbitSign`. Staying closer than 16 to the rock anchor, with enemies alive and the last command moved, counts. Past 240 of those ticks, close-in is set to 120.

The stored contact distance subtracts 100 for roles `improperSearchDaemon` and `algorithmicModerate`. Reach is patrol `sightUnits` minus 16 when the enemy is unaware and `isPatrolMember` is true, and otherwise the pulse range minus 24. The stealth standoff is awareness `sightRangeUnits` plus 32. A shot is a contact that is clear and whose stored distance is at most its reach.

Stealth drops unaware patrol members from the contact list. Its threats are the aware contacts only.

A mine closer than its hazard radius returns `escape`, unless extraction is being held. A telegraph or bolt from `evasion` returns the open steer along that vector, unless extraction is being held, and sets dodge only when `usesDodge` is true and the evasion is urgent. Armed extraction then holds with an empty command inside the zone, and otherwise navigates to the extraction centre.

A clear threat whose stored distance is below the kite range flees toward the objective, and dodges when `usesDodge` is true and that distance is below half the kite range. The kite range is 180, or 300 when integrity is at most 45.

While close-in ticks remain and a nearest contact exists, one tick is spent. A stored distance above `Targeting.closeEnemyRange` navigates to that contact.

Loud walks straight at `cameraToDestroy`. Stealth with no contacts, detection neither hidden nor lockdown, and exposure above `hideAbove(camerasDestroyed:)` returns `hide`.

Stealth with an unaware contact treats the player as seen when `inCone(position)` is true, or when an unaware non-patrol contact is clear and its stored distance is at most the standoff. When the player is not seen and a shot exists, the command is empty. Otherwise a non-nil `ambushPosition` is navigated to.

A nearest contact with no shot navigates to `firingPosition`, or to that contact when the firing position is nil. A nearest contact with a shot orbits. Farther than arrival 40 from the objective navigates there. Otherwise the command is empty.

This does not play a release build.
