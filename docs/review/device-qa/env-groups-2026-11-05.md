# Environment groups

Read 2026-11-05 from `EnvironmentLibrary.isBacked` on `ef68565`. No texture was replaced.

Nearest filtering stays in [env-filter-2026-11-05.md](env-filter-2026-11-05.md). The ground ids stay in [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md). Clip backing stays in [frame-backing-2026-11-05.md](frame-backing-2026-11-05.md).

The groups are `env_ground_`, `env_solid_`, `env_camera_`, `env_camera_captain_`, `env_prop_`, `env_motif_`, and `env_fog_`. The group of an id is the longest matching prefix, so a captain id is `captain` rather than `camera`. `isBacked` is true when the group has at least one declared id and every one of them has a delivered path. `path` returns nil unless that group is backed.

A solid id `solid-04-civic-west` becomes `env_solid_04_civic_west`, by prefixing `env_` and replacing each `-` with `_`. The housing ids are `env_camera_municipal_dome`, `env_camera_storefront`, `env_camera_traffic_reader`, `env_camera_ornamental_civic`, and `env_camera_temporary_mast`.

`bundled` reads `environmentAssetIds` from `presentation-assets-003`, or an empty list when that array is absent. It stores a path only for a declared id whose decision is `adaptedAdmitted` or `originalAccepted` and which has a runtime path. `coverage` counts delivered keys that are also declared, over the declared count.

This does not replace a texture.
