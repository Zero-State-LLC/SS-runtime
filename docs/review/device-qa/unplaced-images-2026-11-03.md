# Images the civic-seam draw path does not place

Measured 2026-11-03 from the runtime asset bytes on `c700b82`. No image was placed, deleted, or made runtime-eligible.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

## Motifs the arena does not place

Phoenix is the motif `civic-seam-arena-004` places. These three are in the bundle. `EnvironmentLibraryTests` lists them, and `projectionPlane` for `env_motif_repair` is unresolved. No renderer samples the files.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `env_motif_repair@1x.png` | 1024×1024 | x 32–991, y 197–825 | 960×629 | `3ea59425896705822aaab310234e462ae9d228174fbd3ef54988fd0f472489f1` |
| `env_motif_counter_signal@1x.png` | 1024×1024 | x 65–958, y 32–991 | 894×960 | `dd0756a98a26f5ca654354b6efca982e9a9f6eb75789c5b7b500c02aecf40052` |
| `env_motif_broadcast_glyph@1x.png` | 1024×1024 | x 189–834, y 32–991 | 646×960 | `3603244843e9f6b61d1e37c792d753f24f8498c55f2dcde7ca6fc48f5fb2fda8` |

## Telegraph PNGs

`RuntimeAssetRegistry.Telegraph` requires these six files. No `App` renderer reads that enum. `renderTelegraphs` draws shapes, as recorded in the shape-hazard note. The asset catalog already says the daemon telegraph files are evidence only.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `telegraph_daemon_query@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `cacf1edae74c2693cc6dbcf5d48f879a78bc2546bc244c5f53f90980271a8216` |
| `telegraph_daemon_dash@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `4381bf1837e95ffd1868e568a921f0203a50749b3645de7fe65ffbdf2d263f73` |
| `telegraph_safety_rationale@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `16f2b6db5b83243b18f910bdb272a6b54280dc485062a3ba3b6b6bbd53d114eb` |
| `telegraph_narrow_tailoring@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `f83e874d0303822aa72d9c8a07b68ae7f78322d5e7ffc960e119445301b70554` |
| `telegraph_temporary_order@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `03cdc90c6e910980719155a1cddacb7fede9278ce4334601ff5a5854bbc0eac5` |
| `telegraph_independent_review@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `02ba0c573105af49a9b844bb4e79a616f53d652c9b8aa19a1478b0721739e9f8` |

## Objective PNGs

`RuntimeAssetRegistry.Objective` requires `objective_phoenix_steps_locked`, `objective_phoenix_steps_armed`, and `objective_network_blackout`. No renderer reads that enum. The camera objective on the HUD is the text `CAM n/8` and `NETWORK BLACKOUT 8/8`.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `objective_phoenix_steps_locked@1x.png` | 128×128 | x 4–122, y 4–123 | 119×120 | `bf077c606b3b18f0a70a14541396bc48618de0e3c02c0743a63fb296870f5987` |
| `objective_phoenix_steps_armed@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `18a2db3912470dc60e31152f1e357244cac9aa417a6a99a6fa35d279bc1da0d2` |
| `objective_network_blackout@1x.png` | 128×128 | x 4–123, y 4–123 | 120×120 | `fc3772097b73c35fb7457d5b2533bf3147d35c89c5e01bc1fb8b73feea38992e` |

## Elite frames, not the boss

`improperSearchDaemon` is not `algorithmicModerate`. The bundle has 156 frames of it, and every canvas is 80×80. Every clip anchor is (40, 70). On the 80×80 `spriteBox`, that is SpriteKit (0.5, 10/80). Content radius is 26.

`civic-seam-arena-004` already has `trigger-elite` with `encounterId` `improperSearchDaemon`, and `gate-elite-forward` owned by that id. This note does not add a spawn and does not tabulate those frames.
