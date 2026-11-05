# Control chrome

Read 2026-11-04 from `HUDRenderer.drawControls` on `e4ff026`. No control was moved.

The circles and the pause rectangle stay in [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md). The dead zone and the one dodge edge stay in [touch-command-2026-11-04.md](touch-command-2026-11-04.md). Pause still adds no tick, as [pause-2026-11-04.md](pause-2026-11-04.md) records.

The stick's accessibility label is `Movement stick`. Its fill is white 0.55 at alpha 0.20. Its stroke is white 0.85 at alpha 0.55, at line width `2` times the framing scale. The knob uses that same white 0.85 at alpha 0.55, and it sits at the stick centre plus the controller's knob offset.

Dodge reads `Dodge`, and its drawn word is `DODGE` at size 7. While a dodge touch is held, the fill is the knob colour. Otherwise it is the stick fill. The stroke matches the stick.

Pause reads `Resume` while the run is paused and `Pause` otherwise. The drawn mark is `>` while paused and `||` otherwise, at size 10. A paused run also draws `PAUSED` at the camera origin, size 20. Labels are Menlo Bold, and the size is multiplied by the framing scale.

This does not move a control.
