# Seam checks

Read 2026-11-05 from `CivicSeamIdentity` on `ef68565`. No zone was moved.

The seven zone names stay in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). Bundle issues stay in [bundle-filter-2026-11-05.md](bundle-filter-2026-11-05.md).

`zoneNamesMatchContract` requires each of those ids to carry that table's name on the manifest. The spine landmarks are `Z-02`, `Z-03`, `Z-06`, and `Z-07`.

`threeGridCollision` requires the court to share the plaza's y and sit to its east, the service zone to sit north and east of the plaza, and the service zone to sit north and east of the spawn. `wedgeParcels` requires `Z-01` and `Z-04` each to have a half-size whose x differs from its y. `landmarkSightlines` requires the plaza east of transit, the court east of the plaza, the plaza north of transit, the court on the plaza's y, and Phoenix south of the court on the court's x.

The prohibited labels are `golden gate`, `sutro`, `karl`, `market street`, `civic center`, `soma`, `chinatown`, and `cable car`. The label check lowercases the tutorial copy, the supplied captions, and the zone names, and rejects a string that contains one of those labels. The default captions are `Phoenix Steps open`.

`catalogRejectsLiteralLandmarks` requires `legacy_san_francisco_landmark_bridge_distant_01` to be `rejected` with a nil runtime path. The content audit adds `literal-bridge-not-rejected` when that fails. It adds a token for each bundle issue. A runtime path whose id contains `_atlanta_` adds `non-sf-runtime-`. A runtime path whose id contains `landmark_bridge`, `_seal_`, or `_logo_` adds `prohibited-runtime-`. Notes that contain `copied artwork`, on a record with a runtime path, add `copied-artwork-runtime-`. The audit list is sorted.

This does not close T802 or T807.
