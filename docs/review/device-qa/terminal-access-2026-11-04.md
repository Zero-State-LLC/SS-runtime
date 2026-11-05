# Terminal access

Read 2026-11-04 from `TerminalAccessibilityOverlay` on `d873e91`. No result row was added.

The panel rectangles stay in [terminal-surface-2026-11-04.md](terminal-surface-2026-11-04.md). The spoken sentences stay in [terminal-speech-2026-11-04.md](terminal-speech-2026-11-04.md).

The surface is absent until a run card and a terminal title both exist. A rehearsal omits Share. Rehearse is present only when the HUD offers it. The first time the surface appears, VoiceOver is sent `screenChanged`.

An accessibility text size replaces the drawn panel with a scrolling card. Its backdrop is red 0.035, green 0.05, blue 0.07. The title, each row, and the buttons reflow. Restart, Share, and Rehearse use the same actions as the drawn controls.

Any other text size leaves the panel drawn and lays clear buttons on its restart, share, and rehearse rectangles. The panel element reads the summary and takes sort priority 4. Restart is 3, Share is 2, and Rehearse is 1.

This does not add a result row.
