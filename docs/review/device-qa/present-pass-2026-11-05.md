# Present pass

Read 2026-11-05 from `GameSession.step` on `5a71391`. No tick was added.

`willStep` before the step and `didStep` after it stay in [medal-record-2026-11-04.md](medal-record-2026-11-04.md). The court snapshot on this step stays in [court-capture-2026-11-05.md](court-capture-2026-11-05.md). Caption ranking stays in [caption-board-2026-11-04.md](caption-board-2026-11-04.md). The command that passes an upgrade gate stays in [upgrade-cards-2026-11-04.md](upgrade-cards-2026-11-04.md). The damage list filled here stays in [damage-log-2026-11-05.md](damage-log-2026-11-05.md). The receipt store stays in [receipt-archive-2026-11-04.md](receipt-archive-2026-11-04.md).

`feel.willStep` runs before `simulation.step`. While an upgrade is pending, a waiting choice becomes the command, with both axes at 0 and dodge clear, and the pending choice is cleared. With no waiting choice the command stays nil. Otherwise the command is the stick: `moveX`, `moveY`, and `dodgePressed`.

When the tick advanced, `playerMovedLastStep` records whether the player position changed. The command log appends only a command that advanced the tick. Then `reactions.ingest`, `applyCameraHUD`, and `HeatCaptionProjector.reinforcements` into `lastHeatReinforcements`. Then the reinforcement caption, the quiet frame, and `feel.didStep`. Then `applyAudio`, `feel.decorate` of that audio, `captionBoard.ingest`, and the awareness hint. `persistTerminalReceiptIfNeeded` runs when the outcome is terminal and the receipt flag is still false, and sets the flag when the store returns a receipt.

`GameScene.update` records the frame time. A paused scene returns. Hit-stop returns before a step, with the camera at the frozen position; that consumption stays in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). An intro frame returns before a step; that advance stays in [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md). The controller is applied, or a debug autopilot writes the command in its place, and then `session.step` runs. After the step come the takedown, VFX ingest when the step's events are non-empty, the ghost advancing to the live tick, the run finish, the sound engine, the device evidence, and `redraw`. That redraw stays in [redraw-order-2026-11-05.md](redraw-order-2026-11-05.md).

This does not add a tick.
