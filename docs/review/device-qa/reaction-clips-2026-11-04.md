# Reaction clips

Read 2026-11-04 from `ReactionClipTracker` on `006304e`. No reaction clip was added.

The tracker sorts clips with `utf8LessThan` and keeps the first clip id for each marker. The comparator walks UTF-8 bytes, and the shorter string wins when the shared prefix matches. `entityDamaged` is hurt. `entityDied`, `eliteDefeated`, and `bossDefeated` are defeat. The player's hurt clip is the first player clip marked `playerDamaged`. A non-player clip marked `playerDamaged` is that role's contact commit. Fog, Witch, and Vendor also keep `role_commit`. An empty tracker reacts to nothing.

Duration is the selected direction's `durationTicks(at: 60)`. The round-up stays in [clip-frame-clock-2026-11-04.md](clip-frame-clock-2026-11-04.md). A duration of 0, or a start tick plus that duration that overflows, stores nothing. The reaction shows while `tick` is below `endTick`.

`ingest` drops held reactions, remains, and commits whose end tick has been reached. Enemy lookup prefers the current list, then the previous list. A body now in `cooldown` whose previous state was `telegraph`, for Fog, Witch, or Vendor, stores that role's commit when the clip has a duration. The direction is the velocity letter from [facing-direction-2026-11-04.md](facing-direction-2026-11-04.md).

`entityDied` clears that id's reaction and commit. When the defeat clip has a duration, the body stays in `remains` until the end tick, at its truncated position, with its radius and role. `entityDamaged` skips an id that also died and skips a body the lookup misses. Cameras publish that event and are skipped here. A stored hurt uses the velocity letter.

`playerDamaged` stores a contact commit when the secondary id is still in the lookup, did not die, and that role has a contact-commit clip. It also stores the player hurt clip. `GameSession` passes `direction(forFacing:)` of `player.facing`. The tracker's own default direction is `s`.

`apply` clears the snapshot's reaction fields. An active commit replaces the sprite clip and keeps the previous id as the fallback. A reaction is written when `mayInterrupt` passes: a missing or unknown base clip accepts it, and a known base clip accepts it when that clip's `cancelWindows` contain the reaction's state. Remains still inside their end tick become `snapshot.defeated`, sorted by id. The player reaction uses the same interrupt rule.

The player renderer tries the reaction, then the state clip. An enemy renderer tries the reaction, then the sprite clip, then the fallback. State clips stay in [actor-clip-choice-2026-11-04.md](actor-clip-choice-2026-11-04.md).
