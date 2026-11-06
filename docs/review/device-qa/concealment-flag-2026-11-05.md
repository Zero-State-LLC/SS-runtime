# The concealment flag

Read 2026-11-05 from `PresentationSnapshot` on `ef68565`. No window was changed.

The mark stays in [combat-feedback-marks-2026-11-04.md](combat-feedback-marks-2026-11-04.md). The until-tick write stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md).

`ghostConcealmentActive` is set when Ghost Step is selected, the tick is above 0, the tick is at or before `cameraInvisibleUntilTick`, and the outcome is not terminal.

This does not change the dodge.
