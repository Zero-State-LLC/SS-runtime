# The rehearsal card

Read 2026-11-05 from `GameScene.rehearseCourt` on `ef68565`. No court was added.

The snapshot stays in [court-capture-2026-11-05.md](court-capture-2026-11-05.md). The receipt guard stays in [receipt-archive-2026-11-04.md](receipt-archive-2026-11-04.md). The ghost store stays in [ghost-file-2026-11-04.md](ghost-file-2026-11-04.md). The clock stays in [run-card-2026-11-04.md](run-card-2026-11-04.md). The titles stay in [terminal-surface-2026-11-04.md](terminal-surface-2026-11-04.md).

`beginRehearsal` returns false when there is no court snapshot. `rehearseCourt` then returns false. Otherwise it calls `resetForNewSimulation`, sets the ghost to nil, increments `ghostGeneration`, sets `terminalEvidenceStored` true, and redraws.

`resetForNewSimulation` clears the spoken HUD, the run card, the rehearsal offer, the sound engine, the renderer, combat feedback, camera follow, the last display time, the lockdown tint, the court, the effects, the near-miss edges, the intro, and the instrumentation. It also resets the touch controller, so a held stick does not enter the new run.

`finishRunIfNeeded` offers rehearsal when the outcome is failure, the court was reached, and a court snapshot exists. A rehearsal card is one row, label `REHEARSAL`, value the clock of the tick minus `courtStartTick`, or of the tick when that start is nil. The card's outcome is nil, and it is marked a rehearsal. The function returns before the ghost store and the medal store. The accessibility surface omits the share rect on that card.

This does not store a rehearsal.
