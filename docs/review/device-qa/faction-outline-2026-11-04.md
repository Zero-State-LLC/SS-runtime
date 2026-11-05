# Faction outline

Read 2026-11-04 from `ActorContrast` on `5d954be`. No outline weight was changed.

The ground shadow stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The blockout path stays in [actor-silhouettes-2026-11-04.md](actor-silhouettes-2026-11-04.md).

The player colour is red 0.86, green 0.94, blue 1. The enemy colour is red 1, green 0.42, blue 0.20. A player outline pixel is always drawn. An enemy pixel at `(x, y)` is drawn when `(x + y) % 5 < 3`.

`syncOutlines` from the render and from `didEvaluateActions` uses sampling scale 1, so that test sees the texture pixel. The outline sprite is a child named `faction-outline`. Its line weight on a blockout shape is `visibleWidth / 844`. A blockout enemy dashes that path with lengths 4 and 3. A blockout player does not dash it.

This does not select another sampling scale.
