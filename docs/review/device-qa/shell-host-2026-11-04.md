# Shell host

Read 2026-11-04 from `GameContainerView` on `d873e91`. The title still starts no tick.

The pause gate stays in [pause-2026-11-04.md](pause-2026-11-04.md). The daily seed stays in [daily-seed-2026-11-04.md](daily-seed-2026-11-04.md).

The title covers the scene until Start. A debug launch with `-SSAutopilot` or `-SSSeed` starts without that cover. Start builds `DailyRun` from the UTC date at the press. A failed build leaves the title up. Settings is a sheet. The scene pauses while that sheet is up or the title is still up.

When the scene phase is not active and `pausesOnInterruption` is true, the host pauses the scene and presents Settings. The gameplay view is a `SpriteView` at 60 frames a second. It ignores the safe area. Its label is `Surveillance Survivor gameplay`. The view hides that element from assistive access while an upgrade choice or a terminal surface is up, and it refuses hits while the upgrade choice is up.

This does not start a tick.
