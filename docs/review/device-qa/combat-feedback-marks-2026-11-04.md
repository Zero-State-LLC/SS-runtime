# Combat feedback marks

Read 2026-11-04 from `CombatFeedbackRenderer` on `5d954be`. No upgrade number was changed.

The jammer's effect stays in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). The concealment window stays in [player-movement-2026-11-04.md](player-movement-2026-11-04.md). One world unit stays in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md).

The root sits at z 19. Every stroke is line width 2. A terminal outcome, or an upgrade waiting, hides all four shapes.

A shot shows when this tick's feedback has a shot, a `weaponFired` event this tick names that projectile, and the velocity is not zero. The aim mark is the polyline `(23, −5)`, `(31, 0)`, `(23, 5)`, coloured red 1, green 0.94, blue 0.78. Its rotation is `atan2` of the velocity's raw y and raw x, and it sits on the player. The discharge is a circle of radius 6 at the shot origin, raw divided by `Q8.scale`, filled at alpha 0.65. Both stay up while the tick is at or after the shot tick and fewer than 6 ticks have passed. Reduced motion or reduced flash clears the discharge fill.

The jammer mark shows when `jammerReducedExposure` is true. That flag is set, for an owned Signal Jammer, when this tick's exposure resolve is lower than the same inputs resolved with the jammer off. The mark is eight arcs on a radius of 27, each covering half of its eighth of the circle, coloured red 0.3, green 0.85, blue 0.9. It rotates by `(tick % 120) * π / 60`, and reduced motion or reduced flash holds that rotation at 0.

The concealment mark shows while `ghostConcealmentActive` is true. Its path is four corners, from `(±19, ±32)` to `(±32, ±32)` to `(±32, ±19)`, in white 0.95.

This does not add a meter.
