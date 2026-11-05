# Actor silhouettes

Read 2026-11-04 from `ActorSilhouette` on `5d954be`. No contour was moved.

The drawn sprite boxes stay in [enemy-sprite-bounds-2026-11-02.md](enemy-sprite-bounds-2026-11-02.md), [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md), and [boss-sprite-bounds-2026-11-03.md](boss-sprite-bounds-2026-11-03.md). The CORDIC unit stays in [millidegree-2026-11-04.md](millidegree-2026-11-04.md).

These polygons are the blockout. Collision, targeting, and camera fields do not read them. `WorldRenderer` strokes one when the actor node is a shape rather than a sprite.

`fogAnalyticsCloud` is `clusteredMass`, `cableCarCorrelator` is `longChassis`, `sutroSignalWitch` is `tallMast`, `autonomousInformant` is `forwardLean`, and `victorianVendor` is `broadTorso`. Those five boxes are 64 by 64. `improperSearchDaemon` is `queryApertures`, 80 by 80. `algorithmicModerate` is `officialInsignia`, 96 by 96. The player ring is a separate case.

The player ring is eight points. Point `i` uses heading `i * MilliDeg.circle / 8` and `Cordic.sinCos`. Each coordinate is that component times 18, divided by `Cordic.q15`. The other contours, relative to the entity centre, are:

`clusteredMass` is (−16, 8), (−6, 18), (8, 16), (18, 4), (14, −12), (0, −18), (−14, −10), (−18, 0).

`longChassis` is (−22, −8), (22, −8), (26, 0), (22, 8), (−22, 8), (−26, 0).

`tallMast` is (−6, −24), (6, −24), (8, 8), (0, 28), (−8, 8).

`forwardLean` is (−10, −16), (18, −4), (18, 4), (−10, 16), (−16, 0).

`broadTorso` is (−20, −12), (20, −12), (16, 16), (0, 20), (−16, 16).

`queryApertures` is (−18, −18), (18, −18), (24, 0), (18, 18), (0, 26), (−18, 18), (−24, 0).

`officialInsignia` is (−12, −28), (12, −28), (20, −8), (28, 8), (12, 28), (−12, 28), (−28, 8), (−20, −8).

This does not change a hit test.
