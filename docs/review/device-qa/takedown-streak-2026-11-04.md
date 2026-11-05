# Takedown streak

Read 2026-11-04 from `TakedownTracker` and `StealthTexture.decorate` on `86c05bb`. No freeze was changed.

The 70 ms freeze stays in [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md). `isUnaware` stays in [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md). The ambush multiplier stays in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md).

A takedown id comes from `entityDied`. The previous body with that id was alive and its awareness was `.unaware`. An `enemyAlerted` event for that id this tick excludes it. The ids are sorted. `isUnaware` is the wider flag. This filter is the `.unaware` case.

`ingest` sets the streak to 0 when any living enemy is `.aware` after the tick and was not `.aware` before it, including an enemy that was not in the previous list. It then adds this tick's takedown count to the streak and to the total. The HUD string is `TAKEDOWN ×<n>` when the streak is at least 2.

`decorate` sets `pitchCents` to −400 on cues whose `audioId` is `impact_enemy` and whose `sourceEntityId` is one of those ids. It appends one caption cue: id `takedown`, text `Takedown`, priority 6, source the first takedown id, sequence one past the highest sequence already present, or 0 when the list is empty. `GameScene` draws `streakCopy` in `AwarenessHintProjector.referenceRect`, y 108.

This does not change the freeze.
