# Share sheet

Read 2026-11-04 from `GameScene.presentShare` on `d873e91`. No share line was changed.

The text stays in [share-text-2026-11-04.md](share-text-2026-11-04.md).

The sheet is presented when the run card has share text and the scene has a window. The presenter is the furthest view controller already presented from the root. If that presenter is already an activity view, the call returns.

The activity items are that one string. The popover, when the presentation has one, uses the scene view and a 1 by 1 rectangle at its centre.

This does not change the share text.
