# The one upgrade accept

Read 2026-11-05 from `GameScene.chooseUpgrade` on `ef68565`. No upgrade was added.

The sheet's submit stays in [upgrade-choice-layout-2026-11-04.md](upgrade-choice-layout-2026-11-04.md).

`chooseUpgrade` returns true once. The upgrade must be pending, `session.pendingUpgradeChoice` must be nil, and `upgradeSelection.submit` must accept the index. It then resets the touch controller, stores move x 0, move y 0, and dodge clear, and stores the index on the session. A later call returns false.

While a redraw sees the upgrade pending and the sheet is not yet presented, the same input clear runs before the sheet synchronizes.

This does not add an upgrade.
