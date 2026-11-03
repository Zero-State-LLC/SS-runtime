# Shapes besides the projectile, mine, and telegraph

Read 2026-11-03 from `WorldRenderer` on `c573052`. The projectile, mine, and telegraph shapes are in [shape-hazards-2026-11-03.md](shape-hazards-2026-11-03.md). This note records the other shapes that function already draws. No color, width, or fill was changed. No rect moves. This does not close T1046, and it does not merge #167.

## Ground kerb

Where two ground tiles meet, the south edge and the west edge get a kerb and a shadow. The other two edges are left to the neighbour, so a shared boundary is drawn once. The kerb is 3 units thick (`kerbThickness`). The shadow is 2 units thick (`kerbShadowThickness`) and sits on the neighbour's side. Fill is `Palette.kerb` (white 0.62, alpha 0.55) and `Palette.kerbShadow` (white 0.10, alpha 0.35). Stroke is clear.

Three lip bands also cross that edge, each 5 units deep, at alpha 0.55, 0.32, and 0.14. Those bands are slices of the tile textures, not a new colour.

## Solid foundation

Each blocking solid draws a rectangle of its own box: width and height are `halfSize * 2`, centred on the solid. Fill `Palette.solidFill` (white 0.18), stroke `Palette.solidStroke` (white 0.32), line width 2. When the solid has upright art, that sprite is added on top of this rectangle at the same size. The rectangle is presentation of the box the simulation already uses.

## Extraction zone

`renderExtraction` draws one rectangle of the arena extraction box. `civic-seam-arena-004` places that box at center (2048, 192) with half-size (96, 64), so the drawn size is 192×128. Fill is `Palette.extractionArmed` (0.20, 0.45, 0.35, alpha 0.35) when armed, and `Palette.extractionLocked` (same RGB, alpha 0.12) otherwise. Stroke is `Palette.extractionStroke` (white 0.7, alpha 0.6). The function does not assign a line width.

## Cameras and fields

A backed camera draws its clip and, when the housing texture is present, the housing sprite. Both use a 64×96 box. The camera-frame note already records those frames. The radius-12 circle, filled with `Palette.cameraFill` for the presentation state and stroked clear, is the fallback `playCamera` uses when the clip is not backed.

A visible camera field is a solid-clipped path. Fill is `Palette.cameraField` (0.90, 0.70, 0.10, alpha 0.12), or `Palette.cameraFieldDetecting` (same RGB, alpha 0.28) while detecting. Stroke is clear. The Captain field uses the same path construction with fill `Palette.captainField` (white 0.75, alpha 0.18) and a clear stroke.

The bundle contains `env_camera_captain_idle` and `env_camera_captain_active`. `CaptainHousing.assetId` selects one of those, and the renderer draws it at 64×96 when the texture loads.

Damage notches, when integrity is 1 or 2, are a 13×10 badge with corner radius 2, fill white 0.08, stroke white 0.8, line width 0.75, and up to two 2×6 ticks.

## Patrol cone

Each unaware patrol cone is the snapshot outline. The fill node uses `Palette.patrolCone` (0.55, 0.75, 0.95, alpha 0.14) and a clear stroke. The edge is the same path dashed `[10, 8]`, fill clear, stroke `Palette.patrolConeEdge` (0.70, 0.85, 1.0, alpha 0.75), line width 2.

## Spawn sockets

Each socket is a filled circle of radius 3. Fill `Palette.spawnSocket` (white 0.45, alpha 0.5). Stroke is clear.

## Markers

An unaware enemy gets a `?` label in Menlo-Bold at 18 points, colour `Palette.unawareMarker` (white 0.92, alpha 0.95). It sits `radius + 10` above the enemy centre.

A daemon query ring is drawn while `improperSearchDaemon` is in `queryTelegraph` or `queryResolve`. The radius is `DaemonQuery.circleRadius`, 56. Fill is clear. Stroke is `Palette.queryMarker` (white 0.8, alpha 0.7). Line width is 2.

## Actor shadow and the unbacked silhouette

Every actor gets one shared shadow texture, a 64×32 ellipse at `ActorContrast.shadowOpacity` 0.35, feathered over the outer 0.3 of the radius, filtered linearly. The drawn size is `shadowSize`: width `1.4 × 2 × radius`, height half of that. For the player radius 18 that is 50.4 × 25.2. The shadow sits `0.3 × radius` below the actor.

When a clip is backed, the faction outline is the texture from `OutlineTextures`. When it is not, the fallback is a silhouette: player fill white 0.92 and stroke white 1 at alpha 0.7, line width 2. The contrast pass then clears that stroke and adds an outline child. Enemies dash that outline with lengths `[4, 3]`. The player, the five standard enemies, and `algorithmicModerate` have clips in the bundle, so this silhouette is the unbacked path.

A ghost, when one is passed in, is that same player silhouette at alpha `0.35 × fade`.

## Closed gate

An open gate draws nothing. A closed gate tiles `env_prop_barricade` through the gate box. That PNG is in the bundle, so the steel-and-hazard colour fallback is not the path this bundle takes. A rail 4 units thick (`GateBarrier.stripThickness`) sits on the open face, colour `Palette.barrierRail` (white 0.10, alpha 0.95). Amber lights (`Palette.barrierLight`, 1.0, 0.72, 0.18) run along it, length 10, gap 6, and one unit thinner than the rail. The tiles partition the collision box and the strip lies inside it. Collision is unchanged.
