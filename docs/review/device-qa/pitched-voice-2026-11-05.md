# Pitched voice

Read 2026-11-05 from `PitchedVoice.play` on `5a71391`. No pitch was retuned.

The pool of eight, and the choice of this voice for a nonzero `pitchCents`, stay in [effect-voice-ceiling-2026-11-03.md](effect-voice-ceiling-2026-11-03.md). The takedown's −400 stays in [takedown-streak-2026-11-04.md](takedown-streak-2026-11-04.md). The `master * effects` product stays in [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md).

`AVAudioPlayer.rate` changes speed. The shift goes through `AVAudioUnitTimePitch` on an engine of its own, started on the first pitched cue. `file` caches an `AVAudioFile` by URL and returns nil when the URL cannot be opened, and `play` returns.

When the file's `processingFormat` differs from `connectedFormat`, `play` stops the engine, disconnects the player output and the pitch output, connects the player to the pitch unit and the pitch unit to the main mixer in that format, and stores the format. It sets `pitch.pitch` to `Float(cents)` and the player volume to the caller's volume. It starts the engine when the engine is stopped, and returns if that start throws. It schedules the file at nil, and plays when the player is not already playing. `stop` stops the player.

`AudioEngine.play`, for a nonzero `pitchCents` whose template has a URL, appends `(audioId, pitchCents)` and calls `pitchedVoice.play` with that URL, those cents, and volume `mix.master * mix.effects`, then returns.

This does not retune a pitch.
