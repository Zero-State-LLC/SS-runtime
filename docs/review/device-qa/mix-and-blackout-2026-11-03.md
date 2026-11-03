# Mix, crossfade, and the blackout drop

Read 2026-11-03 from `AudioEngine` and `BlackoutMusicDrop` on `241c167`. No level was changed. Specs #63 stays open.

`AudioEngine.Mix` defaults are master `1.00`, music `0.70`, effects `0.85`, voice `1.00`, and haptics `0.80`. Effect voices play at `master * effects`. Music beds play at `master * music`. Music and ambience fade out when music is disabled or reduced sensory is on.

The session category is `.ambient` with `.mixWithOthers`.

Music crossfade is `1.0` seconds. A bed whose state is `terminal` uses `0.08` seconds. A bed change crossfades even when the music state stays the same, which is how a boss phase change moves the file. Ambience is `ambience_civic_seam`. It loops, and it fades in at `master * music * 0.5` over the `1.0` second crossfade.

Music state is chosen in this order. The first match wins.

| Order | State | When |
|---:|---|---|
| 1 | `terminal` | outcome is success, failure, or invalid |
| 2 | `extraction` | extraction is armed |
| 3 | `boss` | `algorithmicModerate` is present |
| 4 | `lockdown` | lockdown has been entered |
| 5 | `observed` | detection is not hidden |
| 6 | `explore` | otherwise |

The bed id is `music_` plus the state raw value. When the state is `boss` and a phase is present, the bed id is `music_boss_` plus the phase raw value. The four phase beds are `music_boss_publicSafety`, `music_boss_civilLiberties`, `music_boss_temporarySafeguard`, and `music_boss_independentReview`. With no phase, the boss bed id is `music_boss`. Each bed loops.

The blackout drop ducks the playing beds to silence over `0.1` seconds, holds that silence for `1.0` second, and restores the current bed over `0.5` seconds. The restore starts at `1.1` seconds. The `network_blackout` file waits `0.1` seconds and plays at the start of the silence. Its haptic fires on the tick, before that wait. A newer drop cancels the pending play and the pending restore. The music state machine is not changed.

This does not regenerate a file.
