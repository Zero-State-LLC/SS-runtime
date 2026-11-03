# Effect voice ceiling

Read 2026-11-03 from `AudioProjector` and `AudioEngine` on `241c167`. No ceiling was changed.

Cues made by `cue` have `consumesEffectVoice` true. The lethal warning does not. `stealVoices` keeps at most eight of the cues that consume a voice. While more than eight remain, it removes the one with the largest priority number. If several share that number, it removes the oldest sequence.

The device pool is eight `AVAudioPlayer` slots. `play` stops the slot at the cursor, stores the new player, and advances the cursor by one, modulo 8. A cue with `pitchCents` other than 0 uses the pitched voice instead of a pool slot.

When effects are disabled, the projection omits the voice cues and still includes a cue whose audio id is empty and whose haptic is not `none`. Silencing effects does not silence that haptic.

Caption history appends the caption of each kept voice cue that has one, and it keeps the last eight captions.

This does not add a voice.
