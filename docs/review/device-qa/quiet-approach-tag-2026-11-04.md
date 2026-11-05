# Quiet-approach tag

Read 2026-11-04 from `QuietApproachProjector` on `86c05bb`. No floor was changed.

The latch stays in [medal-predicates-2026-11-03.md](medal-predicates-2026-11-03.md). The tick that calls `resolveQuietApproach` stays in [extraction-and-tick-2026-11-04.md](extraction-and-tick-2026-11-04.md).

The tag copy is `QUIET`. The drawn label is `( ) QUIET`, in the accolade colour, in the rectangle at (610, 54), size 64 by 24. Its VoiceOver label is `Quiet approach: reach the Lockdown Ring without being tracked for a stronger restore at the Authority Court.` The lost caption is `QUIET APPROACH LOST`, drawn dim. The paid caption is `QUIET APPROACH • INTEGRITY` plus the player's integrity, drawn in the accolade colour. The caption rectangle is x `422 - 180`, y 108, width 360, height 22.

A stored quiet value of true, followed by a false latch, sets the lost caption at this tick. The first frame has no stored value, so it does not set that caption. `bossActivated` sets the projector's paid flag. When the latch is still true on that event, the paid caption replaces whatever caption was stored, using `state.player.integrity`. A caption is returned while `tick` is at or after `shownAt` and fewer than 150 ticks have passed.

The tag is visible while the latch is true, the paid flag is false, and the boss has not been reached. Reached means `bossDefeated`, or any enemy whose archetype is `algorithmicModerate`. A restart stores the tag visible and the caption empty, then the next `project` replaces that frame.

This does not change the latch.
