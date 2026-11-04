# Intro sequence

Read 2026-11-04 from `IntroSequence` on `93f6d67`. The intro produces no tick and consumes no command. No control was added.

The full sequence is 120 frames. The title holds for 48. The cameras then power on over 72. Reduced motion is one 30-frame fade. It chirps never, and every camera is powered at frame 0.

Otherwise the cameras are sorted by stable id. Camera `index` of `count` powers on at frame `48 + index * 72 / count`. `advance` returns the cameras whose scheduled frame is the frame just shown. Each of those is owed the existing cue `extraction_tick`.

The title copy is `THE CIVIC SEAM`. During the hold the title alpha is 1 and the veil is 0.55. Both then fade across the 72 frames. Reduced motion fades the title from 1 and the veil from 0.85 across the 30 frames.

The first touch that resolves to a point calls `skipIntroIfRunning`, which sets `skipped` and consumes that touch. The intro is finished when it was skipped or the frame has reached the duration. While it runs, the simulation does not step.
