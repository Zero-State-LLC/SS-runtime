# Tutorial line offer

Read 2026-11-04 from `FeelPassPresenter.observe` on `86c05bb`. No card was added.

The queue, the 300-tick latch, the patrol sentence, and the 150-tick hold stay in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). Objective copy stays in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md). The ambush multiplier stays in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md). `isUnaware` stays in [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md).

The camera is `PresentationCamera.follow` of the truncated player position. The patrol set is the living `isUnaware` enemies whose patrol facing is not zero. Each living `isUnaware` enemy whose truncated position `PresentationCamera.contains` marks the patrol hint when its id is in that set, and the awareness hint otherwise. The awareness string is `UNSEEN ENEMIES HOLD • STRIKE FIRST FOR TRIPLE DAMAGE`. The patrol string is appended first.

The card passed to the queue is nil when the tutorial copy is a safety message or empty. Otherwise it is that copy. The queue is blocked while an upgrade is pending, while that safety flag is set, or while `EncounterLabelGate.isFresh` is true for the current node.

While an intro exists and is unfinished, `GameScene` stores no tutorial line. `shownTutorialCopy` still returns a safety message. `AwarenessHintProjector.project` still runs, and its string is stored on `awarenessHintCopy`. The row at that projector's rectangle is where the takedown streak is drawn, in [takedown-streak-2026-11-04.md](takedown-streak-2026-11-04.md). The hint the card can show is the queued line.

This does not add a card.
