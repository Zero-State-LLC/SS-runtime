# The touch route

Read 2026-11-05 from `GameScene.beginTouch` on `ef68565`. No control was added.

The intro skip stays in [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md). Pause stays in [pause-2026-11-04.md](pause-2026-11-04.md). Share stays in [share-sheet-2026-11-04.md](share-sheet-2026-11-04.md).

A missing projector returns false, and the rest of the batch continues. A skip that is still running returns true and consumes the rest of the batch.

A terminal outcome returns true. A restart hit calls `restartRun`. A rehearse hit calls `rehearseCourt`. A share hit calls `presentShare`. A terminal tap that misses those controls is still consumed.

An upgrade that is pending, or a paused run, returns true and does not call the controller. Otherwise a stick or dodge touch is handed to the controller. A pause result calls `onPauseRequested`. That path returns false, so a later touch in the same batch still runs.

`moveTouch` returns immediately while an upgrade is pending or the run is paused. `endTouch` ends that token.

This does not add a control.
