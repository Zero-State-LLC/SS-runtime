# Fog thinning

Read 2026-11-04 from `FogThinning` on `93f6d67`. The opacity was not changed.

An aware enemy inside the presentation view thins both fog layers. The boss and the elite count, because they are never unaware. The thinned multiplier is 0.50 of the authored opacity. Progress moves toward 1 while such an enemy is in view, and back toward 0 when none is. Each tick of elapsed time moves progress by `elapsed / 30`, clamped to 0…1.

The drawn multiplier eases that progress with `p² × (3 − 2p)`, then returns `1 − 0.50 × eased`. The clock is the simulation tick, so the fade holds still under pause and hit-stop. The view size stays in [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md).
