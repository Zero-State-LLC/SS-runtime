# Tutorial timing

Read 2026-11-04 from `TutorialState`, `TutorialLineQueue`, and `EncounterLabelGate` on `93f6d67`. No card was added.

The tutorial starts at move. The copy is `MOVE` until displacement reaches 96, then `CAMERA FIELDS RAISE EXPOSURE` until 60 in-view ticks or a contact, then `BREAK LINE OF SIGHT TO RECOVER` until 30 ticks without contact, then `MOVE TOWARD A CAMERA TO SHOOT IT • DESTRUCTION ADDS EXPOSURE` until 300 eligible ticks or a camera impact, then `CHOOSE ONE COUNTERMEASURE`. Completing M-A also forces the upgrade phase. Selecting the upgrade completes it, and the copy is empty. A card stops being drawn after 300 presented ticks. The phase stays.

Safety copy is drawn before that cap. Turning tutorials off leaves it up. The lethal-warning card is `LETHAL THREAT`. Lockdown copy is `LOCKDOWN`. The locked box uses `DEFEAT THE CURRENT AUTHORITY`, and the armed extraction uses `PHOENIX STEPS OPEN`. Those two sentences stay in [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md).

The line queue shows one line. A card leaves the queue when it is no longer current. A one-shot hint, once it is showing and the queue is not blocked, lasts 300 ticks. While an encounter label or the upgrade prompt is up, the line waits and that time does not run. Each string is offered once.

The patrol hint is `PATROL • STAY OUT OF THE CONES • WALK PAST OR STRIKE`. It is offered when a cone origin lies inside the presentation view.

An encounter label waits until that encounter has activated. A mob label waits on the encounter's activated flag. The elite label waits until the elite is alive or already defeated. The boss label waits until the boss runtime exists or the boss is defeated. For 150 ticks after a label first shows, tutorial lines stay back. Extraction copy is not an encounter label, and it shows as soon as the HUD has it.
