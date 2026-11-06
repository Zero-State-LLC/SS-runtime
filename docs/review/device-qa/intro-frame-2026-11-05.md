# The intro frame

Read 2026-11-05 from `GameScene.introFrame` on `ef68565`. No frame was added.

The durations, the skip, and the rule that the simulation does not step while the intro runs stay in [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md).

No intro returns `mayStep` true and an empty chirp list. A finished intro is set to nil and returns the same. A hold at or past the current frame returns `mayStep` false, an empty chirp list, and `held` true. Otherwise the frame advances, the intro is stored, and `mayStep` stays false, with the chirps from that advance.

The production call passes no hold. `startIntro` builds the sequence from the camera entity ids and `settings.vfx.reducedMotion`.

This does not add a frame.
