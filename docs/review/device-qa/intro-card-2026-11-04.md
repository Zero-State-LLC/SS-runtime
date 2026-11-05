# Intro card

Read 2026-11-04 from `IntroOverlay` on `d873e91`. No frame count was changed.

The hold, the fade, and the veil alpha stay in [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md). The subtitle line stays in [daily-seed-2026-11-04.md](daily-seed-2026-11-04.md). The headline stays in [daily-flavour-2026-11-04.md](daily-flavour-2026-11-04.md).

The card is a camera child at z 950. The veil is a black sprite, 4000 by 4000. Three labels sit on it, each centred, in white 0.94. The title is Menlo Bold at 26 points, y 18, and its text is `IntroSequence.titleCopy`. The subtitle is Menlo at 11 points, y −10. The headline is Menlo at 10 points, y −28.

The node hides when the intro is absent or finished. Otherwise the veil uses `veilAlpha` and the three labels use `titleAlpha`. The subtitle is the daily run's title label, or empty. The headline is the flavour headline, or empty.

This does not change the intro length.
