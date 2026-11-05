# Spoken HUD

Read 2026-11-04 from `SpokenHUD` on `86c05bb`. No sentence was added.

`TerminalSpeech.sentence` stays in [terminal-speech-2026-11-04.md](terminal-speech-2026-11-04.md). The safety class and the 150-tick board stay in [caption-board-2026-11-04.md](caption-board-2026-11-04.md). The line that is drawn stays in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md).

`announcements` speaks three groups, in order. A tutorial string is spoken when it differs from the stored one and is not empty. A reinforcement string uses the same rule. A safety caption is spoken when its `sequence` is not in the announced set. After that pass, the announced set becomes the sequences of the safety captions still on the board. A caption that leaves the board is forgotten, so a later return of that sequence can be spoken again. Routine captions are not in this list.

`sentences` splits on ` • `, runs each piece through `TerminalSpeech.sentence`, joins the pieces with `. `, and appends `.`. The camera card becomes `Move toward a camera to shoot it. Destruction adds exposure.`

`GameScene` calls this only while VoiceOver is running. The tutorial argument is `shownTutorialCopy`: a safety message uses the tutorial copy, and any other line uses the queued tutorial line when tutorials are enabled. The reinforcement argument is the heat caption. The caption argument is the board's visible list. The spoken lines are joined with a space and posted as a queued announcement.

This does not add a caption.
