# The outline weight

Read 2026-11-05 from `GameScene.configureHUD` on `ef68565`. No outline weight was retuned.

The property default stays in [faction-outline-2026-11-04.md](faction-outline-2026-11-04.md). `pointsPerSceneUnit` stays in [hud-fit-2026-11-04.md](hud-fit-2026-11-04.md).

After the projector is built, the scene stores `outlineWidthUnits` as 1 divided by `pointsPerSceneUnit`. A size change builds that projector again, so the stored width follows it. A blockout outline's line width is the stored value.

This does not select another sampling scale.
