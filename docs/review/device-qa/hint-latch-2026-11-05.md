# The hint latch

Read 2026-11-05 from `AwarenessHintProjector` on `ef68565`. No hint was added.

The copy stays in [tutorial-line-offer-2026-11-04.md](tutorial-line-offer-2026-11-04.md). The row that is drawn stays in [takedown-streak-2026-11-04.md](takedown-streak-2026-11-04.md) and [streak-type-2026-11-05.md](streak-type-2026-11-05.md). The card's 300-tick cap stays in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). The heat row stays in [heat-caption-2026-11-04.md](heat-caption-2026-11-04.md). The quiet caption at this y stays in [quiet-approach-tag-2026-11-04.md](quiet-approach-tag-2026-11-04.md).

`project` stores `shownAt` on the first tick the query is visible. It then returns the copy while `tick` is at or after `shownAt` and fewer than `visibleTicks` have passed. `visibleTicks` is 300. `reset` replaces the projector. `project` does not read `tutorialsEnabled`.

`referenceRect` is `HUDRect(x: 422 - 180, y: 108, width: 360, height: 24)`.

The snapshot query keeps an enemy whose `unaware` flag is set and whose absolute deltas from the camera centre are at most half the visible width and half the visible height. The state query keeps a living `isUnaware` enemy whose truncated position `PresentationCamera.contains` reports inside a follow camera of the truncated player. That contains test stays in [view-contains-2026-11-05.md](view-contains-2026-11-05.md). The visible size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).

This does not draw the hint.
