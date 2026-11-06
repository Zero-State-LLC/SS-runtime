# The tutorial flags this tick

Read 2026-11-05 from `Simulation.step` and `TutorialState.noteCameraInViewport` on `ef68565`. No card was added. The card copy and the phase counts stay in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). The objective sentences stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The lethal-warning predicate stays in [lethal-warning-2026-11-04.md](lethal-warning-2026-11-04.md). The rules viewport stays in [spawn-socket-choice-2026-11-04.md](spawn-socket-choice-2026-11-04.md). The contact sample stays in [camera-contact-2026-11-04.md](camera-contact-2026-11-04.md).

After that sample, `noteContact` receives whether the contact list is non-empty. The lethal-warning flag is assigned in the same stretch. `lockdownPreempts` is `lockdownEntered` while the tutorial phase is not `complete`. `extractionPreempts` is `.armed` when extraction is armed. Otherwise a player position truncated to units that lies inside the extraction aabb is `.lockedContact`. Otherwise it is nil. `notePresentedTick` then runs.

The same step builds `RulesViewport.box` from that truncated position and the facing. A camera whose position lies in that box calls `noteCameraInViewport`. That call counts only during the field phase.

This does not add a card.
