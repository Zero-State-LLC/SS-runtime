# Visual gate

Read 2026-11-05 from `VisualLanguageLoader.decode` on `5a71391`. No box was resized.

The measured boxes stay in [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md), [unplaced-images-2026-11-03.md](unplaced-images-2026-11-03.md), [boss-sprite-bounds-2026-11-03.md](boss-sprite-bounds-2026-11-03.md), and [camera-frame-bounds-2026-11-02.md](camera-frame-bounds-2026-11-02.md). The ground tile stays in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). Nearest filtering on a loaded texture stays in [clip-playback-2026-11-04.md](clip-playback-2026-11-04.md) and [env-filter-2026-11-05.md](env-filter-2026-11-05.md).

The loader accepts schema `visual-language-001` and version `visual-civic-seam-001`. The authoring grid is 64. The actor footprint min is 28 and the max is 36. Salience has 9 rows. Each rank is `index + 1`, and surface and distinction are non-empty. The palette has at least 11 rows. Each row has a non-empty role, family, and non-color carrier, and the roles include `player` and `hunted`.

The sprite boxes must be `playerAndStandardEnemy` at 64×64, `improperSearchDaemon` at 80×80, `algorithmicModerate` at 96×96, and `cameraPole` at 64×96. Inside that object, `environmentModuleMultiple` must be 64. The atlases number 8. `deliveryNamePattern` is non-empty. `colorIsNotSoleCarrier`, `collisionNeverFromSpriteBounds`, and `groundContactMustBeStable` are true. `filtering` is `nearestNeighbor`.

This does not resize a box.
