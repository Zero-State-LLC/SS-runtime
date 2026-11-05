# Audio interruption

Read 2026-11-04 from `AudioEngine.handleInterruption` on `d873e91`. No bed was changed.

The session category, the crossfades, and the blackout drop stay in [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md). The eight slots stay in [effect-voice-ceiling-2026-11-03.md](effect-voice-ceiling-2026-11-03.md). The empty lethal id stays in [lethal-warning-2026-11-04.md](lethal-warning-2026-11-04.md).

An interruption begins by stopping every effect voice, every bed, and the ambience. The drop in flight is cancelled. While the flag is set, `apply` stores the projected music state and bed id and plays nothing. A presentation cue plays nothing.

When the interruption ends, the session is made active again and the stored bed is started for the stored state. The stopped one-shots are not started again.

A phase bed id with no delivered file uses `music_boss`.

This does not change a bed.
