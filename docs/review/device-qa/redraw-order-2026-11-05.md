# Redraw order

Read 2026-11-05 from `GameScene.redraw` on `5a71391`. No layer was added.

Shake stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md). The intro timing stays in [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md). The spoken lines stay in [spoken-hud-2026-11-04.md](spoken-hud-2026-11-04.md). The caption board stays in [caption-board-2026-11-04.md](caption-board-2026-11-04.md).

`redraw` adds one to `presentationFrame`. While an upgrade is pending and the overlay is not presented, it clears gameplay input. It synchronizes the upgrade selection and the terminal accessibility.

While an intro exists and is unfinished, each camera that `isPowered` reports as false gets `fieldVisible` false on a copy of the snapshot. The simulation state stays as the step left it. `cameraFollow.update` runs, then `cameraNode.position` becomes `vfx.cameraPosition` of that base. `nearMissEdges.update` takes `presentationFrame` and the reduced-motion flag. The intro overlay takes the daily label and the flavour headline.

The HUD objective is the feel copy. The tutorial line is nil while the intro is unfinished, and the feel tutorial line after that. The streak copy is the feel copy. `renderer.render` takes the ghost and the reduced-motion flag. Combat feedback, `vfx.render`, the lockdown tint, and the court follow. The HUD then takes the knob offset, whether dodge is pressed, the caption board's visible lines, the reinforcement, the quiet frame, and the awareness hint, and `hud.render` runs. `announceForVoiceOver` posts only while VoiceOver is running.

This does not add a layer.
