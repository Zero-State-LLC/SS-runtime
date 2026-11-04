# Terminal surface

Read 2026-11-04 from `HUDLayout` on `93f6d67`. No control was added.

The panel is 460 by 262, centred on the safe rectangle. Restart is 200 by 52, centred on the panel, inset 20 from the panel's bottom. The gap between buttons is 12. Share sits to the right of Restart on that row. Rehearse Court sits to the left, with copy `REHEARSE COURT`. Neither button moves with handedness.

Title and settings copy are `START` and `SETTINGS`. The restart control copy is `RESTART`. A rehearsal titles `REHEARSAL COMPLETE` or `REHEARSAL DOWN`, and an invalid rehearsal still reads `RUN INVALID`. The live outcome lines stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md).

The title centre is 34 points below the panel's top. Six card rows begin 68 points below that top, each 20 points tall, inset 48. The surface is absent while the outcome is playing or an upgrade choice is pending.
