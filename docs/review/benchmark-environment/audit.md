# Environment disposition audit — BP-005

Status: source inspection complete; runtime geometry and visual acceptance pending.

All 46 delivered file hashes match the current catalog. This establishes identity, not quality. Contact sheets preserve source aspect ratio but fit each image into a review cell; they are not world-scale comparisons.

The dispositions below are proposed production actions based on visible source defects and the adopted benchmark contract. “Retain” means reuse candidate, not benchmark acceptance. “Exclude” applies to visible first-release art only; logical camera families remain intact. No shipping files are removed by this report.

| # | Asset | Disposition | Observation / required work |
|---|---|---|---|
| 1 | `env_ground_asphalt` | retain | Coherent asphalt surface; verify tile seams and contrast beneath combat. |
| 2 | `env_ground_sidewalk` | repair | Utility covers and curb-like vertical stripe are baked into repeating ground; isolate landmark detail or prove repeat looks natural. |
| 3 | `env_ground_plaza` | retain | Coherent plaza paving; verify tiling and shared scale. |
| 4 | `env_ground_service` | repair | Large circular/grate landmark is baked into a ground tile; compare repeat against the shared street sample. |
| 5 | `env_ground_steps` | repair | Frontal stair bands need a deliberate top-down stair placement and height reading. |
| 6 | `env_solid_01_residential_west` | repair | Small building occupies little of a tall 128x512 canvas; recalculate visible ground anchor and mapping without deriving collision from alpha. |
| 7 | `env_solid_02_residential_north` | repair | Detached building fragment at left edge; remove fragment and register main building base. |
| 8 | `env_solid_03_transit_kiosk` | repair | Detached fragment at right edge of kiosk; clean and register the complete kiosk. |
| 9 | `env_solid_04_civic_west` | repair | Building occupies only part of tall canvas; establish common scale and ground anchor. |
| 10 | `env_solid_05_civic_dais` | repair | Detached triangular fragment above dais; clean and register base. |
| 11 | `env_solid_06_service_yard_a` | repair | Tall canvas surrounds a smaller building; compare visible base with authoritative footprint. |
| 12 | `env_solid_07_service_yard_b` | retain | Complete service building silhouette; retain as a candidate pending shared projection and traversal checks. |
| 13 | `env_solid_08_service_divider` | repair | Detached fragments above and left of divider; remove and register continuous wall base. |
| 14 | `env_solid_09_grid_island_a` | repair | Detached fleck below utility island; clean and verify boundary. |
| 15 | `env_solid_10_grid_island_b` | retain | Complete utility island; verify common scale and authoritative base placement. |
| 16 | `env_solid_11_court_column_a` | repair | Column very small in tall canvas; register visible base and verify apparent scale. |
| 17 | `env_solid_12_court_column_b` | repair | Column very small in tall canvas; register visible base and verify apparent scale. |
| 18 | `env_solid_13_phoenix_west` | repair | Short wall inside tall narrow canvas; register base rather than scaling from canvas dimensions. |
| 19 | `env_solid_14_phoenix_east` | repair | Short wall inside tall narrow canvas; register base rather than scaling from canvas dimensions. |
| 20 | `env_camera_municipal_dome` | replace | Retain municipal construction as reference; replace static image with complete-device six-clip delivery under BP-004. |
| 21 | `env_camera_storefront` | exclude | Alternate visible family excluded from first-release camera rendering by BP-004; preserve logical family placement data. |
| 22 | `env_camera_traffic_reader` | exclude | Alternate visible family excluded from first-release camera rendering by BP-004; preserve logical family placement data. |
| 23 | `env_camera_ornamental_civic` | exclude | Alternate visible family excluded from first-release camera rendering by BP-004; preserve logical family placement data. |
| 24 | `env_camera_temporary_mast` | exclude | Alternate visible family excluded from first-release camera rendering by BP-004; preserve logical family placement data. |
| 25 | `env_prop_newsbox` | repair | Two boxes plus disconnected shapes above; isolate a coherent newsbox object and clean fragments. |
| 26 | `env_prop_hydrant_meters` | repair | Hydrant/meter group has detached strip above; clean and register intended group. |
| 27 | `env_prop_utility_covers` | repair | Four separate utility covers in one texture; decide explicit authored group versus separately registered ground details in sample. |
| 28 | `env_prop_vent_grate` | retain | Single readable grate; verify ground projection and scale. |
| 29 | `env_prop_street_tree` | retain | Tree and planter form a coherent unit; verify occlusion and visible base in traversal. |
| 30 | `env_motif_repair` | replace | Large frontal wall illustration conflicts with elevated shared viewpoint; preserve repair motif in a correctly projected wall/decal. |
| 31 | `env_motif_counter_signal` | replace | Frontal wall/window vignette conflicts with shared viewpoint; preserve counter-signal motif on the scene architecture. |
| 32 | `env_motif_broadcast_glyph` | replace | Freestanding dimensional emblem reads as an object, not a grounded broadcast marking; rebuild within accepted motif usage after scene comparison. |
| 33 | `env_ground_railbed` | retain | Ground cobble surface can support rail setting; verify tile seams and pairing with rail strip. |
| 34 | `env_prop_trolley_pole` | repair | Pole occupies a small part of tall canvas; register base and compare height with municipal camera. |
| 35 | `env_prop_signal_mast` | retain | Complete traffic signal silhouette; verify height, scale and depth handling. |
| 36 | `env_prop_bus_shelter` | retain | Complete shelter with visible roof; verify shared viewpoint and foreground occlusion. |
| 37 | `env_prop_parklet` | retain | Complete parklet; verify shared scale and authoritative placement semantics. |
| 38 | `env_prop_bike_rack` | retain | Readable rack group; verify ground contact and scale. |
| 39 | `env_prop_barricade` | repair | Barricade reads mostly frontally; match elevated ground plane and base before adoption. |
| 40 | `env_prop_seismic_brace` | retain | Complete brace; verify mounting context and base alignment. |
| 41 | `env_motif_phoenix` | repair | Circular emblem reads face-on; project it consistently if used on ground, preserving motif. |
| 42 | `env_fog_low` | replace | Two separated cloud-like groups on transparent canvas; not a continuous haze tile. Produce a continuous bounded fog layer and verify seams in runtime. |
| 43 | `env_fog_high` | replace | Repeated small cloud-like groups in a row; visible source layout risks repeated strip pattern. Produce a continuous bounded haze tile. |
| 44 | `env_camera_captain_idle` | replace | Separate ornate camera family; rebuild using shared municipal materials with persistent boss-owned non-color distinction. |
| 45 | `env_camera_captain_active` | replace | Active ornate camera family; pair with rebuilt Captain source and retain non-color identity across states. |
| 46 | `env_prop_rail_strip` | repair | Rail strip is horizontally presented; map to actual street plane and verify continuity at joins. |

## Evidence still required

Each solid/upright prop needs its visible ground base, render anchor and intended world draw size recorded separately from the authoritative AABB. The inventory records current image hashes and alpha bounds; alpha bounds are not a collision boundary. Front/rear/corner traversal and projectile contact remain NOT_PRODUCED for this audit.

Source identities, hashes, dimensions and alpha bounds: inventory.json. Visual inspection: contact-1.png and contact-2.png. Runtime source commit: 981dbb48a6ccf7071715a877bfdf89c0ebf0e78f.

Method follows SS-specs benchmark-production.md BP-001/BP-002/BP-005 and its existing researched design basis. Exact repair mappings and any new design choices require the shared runtime sample; this report does not invent them.
