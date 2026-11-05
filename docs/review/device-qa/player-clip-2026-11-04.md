# Player clip

Read 2026-11-04 from `PresentationSnapshot.playerClip` and `GameSession.snapshot` on `006304e`. No player clip was added.

Failure presents `player_defeat`. Success presents `player_complete`. A dodge with `dodgeActiveRemaining` above 0 presents `player_dodge`. Armed extraction, with the truncated player point inside the extraction box, presents `player_extraction`. That box test is [extraction-presence-2026-11-04.md](extraction-presence-2026-11-04.md). Otherwise `movedUnitsLastTick` of 0 presents `player_idle`, and any other count presents `player_move`.

`movedUnitsLastTick` is `IsolatedKernel.distanceUnits` of the position before `Movement.apply` and the position after it. That distance is the integer square root of the squared Q8 distance, divided by `Q8.scale`. The division truncates.

`GameSession.snapshot` keeps defeat, success, dodge, and extraction. When `playerMovedLastStep` is set and the clip is idle or move, a changed Q8 position presents `player_move` and an unchanged position presents `player_idle`. The flag is set on a tick that advanced, from that position comparison. A tick that stays put leaves the previous flag. `restartRun` and `beginRehearsal` call `resetPresentation`, which clears the flag. While the flag is clear, the snapshot's `movedUnitsLastTick` rule is the clip.

The renderer tries `playerReactionClipId` first and `playerClipId` second. The reaction rule is [reaction-clips-2026-11-04.md](reaction-clips-2026-11-04.md). Frame timing stays in [clip-frame-clock-2026-11-04.md](clip-frame-clock-2026-11-04.md).
