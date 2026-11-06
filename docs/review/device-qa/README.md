# Device presentation QA — issue #117

Intent accepted 2026-10-13. Baseline main: `6e42cb47e8be10cffcc8398cbf9e2fff5fbe7dac`.
Spec: `2377b99c6b6d1654e2cb976ee1b7e07b75c77e1a`. No gameplay, content, arena, or replay identity change.

## Checks required

| Area | Automated coverage | Physical check |
|---|---|---|
| Camera follow | CameraFollowTests: turn continuity, dead zone, vertical facing, bounds/reset | Turn in place, reverse while moving, arena edge |
| Surveillance fields | DevicePresentationRegressionTests: emitter position, clockwise convention, narrow occluders, cover changes | Approach cover; compare field boundary and Exposure |
| Animation lifecycle | Removed camera sprite reappears with action attached | Movement/idle/hurt/defeat and camera damage states |
| Performance | Frame timeline streak classification; core suite | Record frame percentiles with `-SSQA`, repeat baseline opening and full run |
| Controls | Existing SceneInputIntegrationTests in Debug and Release | Movement, Dodge, pause/resume, restart |
| Visual clipping | Geometry coverage; broader visual review pending | Cameras, walls, gates, actors, HUD and safe-area edges |
| Authority | Full core/replay golden suite | No claim that visual QA substitutes for deterministic tests |

## Evidence and status

- Baseline user playtest: FAIL (immediate stutter/jumps and rendering defects).
- [Baseline profile](baseline.md): renderer and name lookup dominate; outline generation is not the primary observed cost.
- Candidate core checks: 740 tests across 104 suites passed (528.067 seconds). Debug/Release app CI still running.
- Candidate physical playtest: FAIL. User reports broken camera and character animation, jumbled/unrecognizable assets, collision problems, and suspected hit-detection problems. See candidate-findings.md.
- C-003 p95 <=16.67 ms remains unproven. The connected iPhone 17 Pro is not the baseline iPhone 12; report actual hardware rather than relabel it.

No release or full-QA pass is claimed. Further animation/clipping symptoms require reproduction on the candidate; issues remain open until verified.

## Measurement notes

Each note records one fact about bytes or draw calls already on main. None of them closes a parent task.

| Note | Fact |
|---|---|
| [solid-footprint-2026-11-01.md](solid-footprint-2026-11-01.md) | Two blocking solids: canvas, ink, and the blocking rectangle |
| [solid-footprint-twelve-2026-11-02.md](solid-footprint-twelve-2026-11-02.md) | The other twelve blocking solids, same three facts |
| [camera-frame-bounds-2026-11-02.md](camera-frame-bounds-2026-11-02.md) | Camera head frames and the five housings, at anchor (32, 88) |
| [enemy-sprite-bounds-2026-11-02.md](enemy-sprite-bounds-2026-11-02.md) | Five standard enemies, canvas 64×64, anchor (32, 56), body radii |
| [retest-checklist.md](retest-checklist.md) | Human rows, plus the device-sitting bot column |
| [decoration-placement-2026-11-02.md](decoration-placement-2026-11-02.md) | Twenty-one placed decoration canvases and their draw boxes |
| [tiled-planes-2026-11-02.md](tiled-planes-2026-11-02.md) | Six ground tiles and the two fog bands |
| [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md) | Shipped player frames, canvas 64×64, anchor (32, 56), radius 18 |
| [boss-sprite-bounds-2026-11-03.md](boss-sprite-bounds-2026-11-03.md) | Shipped `algorithmicModerate` frames, canvas 96×96, anchor (48, 84), radius 30 |
| [shape-hazards-2026-11-03.md](shape-hazards-2026-11-03.md) | Projectile, mine, and telegraph shapes the renderer already draws |
| [unplaced-images-2026-11-03.md](unplaced-images-2026-11-03.md) | Motif, telegraph, and objective PNGs the draw path does not place |
| [hud-shapes-2026-11-03.md](hud-shapes-2026-11-03.md) | HUD and control PNGs, and the shapes the HUD draws instead |
| [decoration-solid-overlap-2026-11-03.md](decoration-solid-overlap-2026-11-03.md) | No placed decoration canvas shares area with a blocking rectangle |
| [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md) | South dodge, recover, hurt, defeat, extraction, and complete frames |
| [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md) | Kerb, solid foundation, extraction, fields, cones, sockets, markers, shadow, and gate |
| [player-facing-frame-01-2026-11-03.md](player-facing-frame-01-2026-11-03.md) | Idle and move frame 01 in each direction; the other directions are not copies of south |
| [south-state-frame-01-2026-11-03.md](south-state-frame-01-2026-11-03.md) | South frame 01 of the non-idle enemy states and of the elite |
| [player-direction-copies-2026-11-03.md](player-direction-copies-2026-11-03.md) | Hurt, defeat, and extraction reuse the south bytes in every direction |
| [direction-distinct-2026-11-03.md](direction-distinct-2026-11-03.md) | Outside those three clips, no two directions share a PNG hash |
| [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md) | Dodge, recover, and complete frame 01 in north, east, and west |
| [enemy-idle-frame-01-2026-11-03.md](enemy-idle-frame-01-2026-11-03.md) | Idle frame 01 in north, east, and west for the five standard enemies |
| [boss-facing-frame-01-2026-11-03.md](boss-facing-frame-01-2026-11-03.md) | Boss frame 01 in north, east, and west of the seven states |
| [elite-facing-frame-01-2026-11-03.md](elite-facing-frame-01-2026-11-03.md) | Elite frame 01 in north, east, and west of the eight states |
| [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md) | Non-idle frame 01 in north, east, and west for the five standard enemies |
| [player-action-rest-frames-2026-11-03.md](player-action-rest-frames-2026-11-03.md) | Dodge 02–04, recover 02, and complete 02–04 in north, east, and west |
| [clip-lengths-2026-11-03.md](clip-lengths-2026-11-03.md) | Every shipped actor clip has the same frame count in all four directions |
| [player-idle-rest-frames-2026-11-03.md](player-idle-rest-frames-2026-11-03.md) | Idle frames 02–04 in north, east, and west |
| [player-move-rest-frames-2026-11-03.md](player-move-rest-frames-2026-11-03.md) | Move frames 02–06 in north, east, and west |
| [enemy-idle-rest-frames-2026-11-03.md](enemy-idle-rest-frames-2026-11-03.md) | Idle frames 02–04 in north, east, and west for the five standard enemies |
| [enemy-south-move-rest-2026-11-03.md](enemy-south-move-rest-2026-11-03.md) | South move frames 02–06 for the four enemies that have a move clip |
| [enemy-move-rest-frames-2026-11-03.md](enemy-move-rest-frames-2026-11-03.md) | Move frames 02–06 in north, east, and west for those four enemies |
| [boss-south-rest-frames-2026-11-03.md](boss-south-rest-frames-2026-11-03.md) | Boss south frames after 01 |
| [boss-six-rest-frames-2026-11-03.md](boss-six-rest-frames-2026-11-03.md) | Boss frames 02–06 in north, east, and west |
| [boss-long-rest-frames-2026-11-03.md](boss-long-rest-frames-2026-11-03.md) | Boss stagger and long frames in north, east, and west |
| [elite-south-rest-frames-2026-11-03.md](elite-south-rest-frames-2026-11-03.md) | Elite south frames after 01 |
| [elite-six-rest-frames-2026-11-03.md](elite-six-rest-frames-2026-11-03.md) | Elite frames 02–06 in north, east, and west |
| [elite-short-rest-frames-2026-11-03.md](elite-short-rest-frames-2026-11-03.md) | Elite short frames in north, east, and west |
| [enemy-south-hurt-defeat-rest-2026-11-03.md](enemy-south-hurt-defeat-rest-2026-11-03.md) | Standard-enemy hurt and defeat, south, after frame 01 |
| [enemy-hurt-defeat-rest-frames-2026-11-03.md](enemy-hurt-defeat-rest-frames-2026-11-03.md) | Standard-enemy hurt and defeat in north, east, and west |
| [enemy-south-action-rest-2026-11-03.md](enemy-south-action-rest-2026-11-03.md) | South frames 02–03 of pursuit, charge, recover, pulse, cast, and throw |
| [enemy-south-commit-rest-2026-11-03.md](enemy-south-commit-rest-2026-11-03.md) | South frame 02 of the five commit clips |
| [informant-action-rest-frames-2026-11-03.md](informant-action-rest-frames-2026-11-03.md) | Informant pursuit frames 02–03 and pursuitCommit 02 in north, east, and west |
| [cable-charge-rest-frames-2026-11-03.md](cable-charge-rest-frames-2026-11-03.md) | Cable charge frames 02–03 and chargeCommit 02 in north, east, and west |
| [cable-recover-rest-frames-2026-11-03.md](cable-recover-rest-frames-2026-11-03.md) | Cable recover frames 02–03 in north, east, and west |
| [fog-pulse-rest-frames-2026-11-03.md](fog-pulse-rest-frames-2026-11-03.md) | Fog pulse frames 02–03 and pulseCommit 02 in north, east, and west |
| [witch-cast-rest-frames-2026-11-03.md](witch-cast-rest-frames-2026-11-03.md) | Witch cast frames 02–03 and castCommit 02 in north, east, and west |
| [vendor-throw-rest-frames-2026-11-03.md](vendor-throw-rest-frames-2026-11-03.md) | Vendor throw frames 02–03 and throwCommit 02 in north, east, and west |
| [player-copied-direction-rows-2026-11-03.md](player-copied-direction-rows-2026-11-03.md) | North, east, and west hurt, defeat, and extraction files, which match the south bytes |
| [shell-image-bounds-2026-11-03.md](shell-image-bounds-2026-11-03.md) | Title backdrop, wordmark, plates, launch mark, and app icon |
| [captain-housing-bounds-2026-11-03.md](captain-housing-bounds-2026-11-03.md) | The two Captain housing PNGs, idle and active |
| [audio-file-bytes-2026-11-03.md](audio-file-bytes-2026-11-03.md) | The 34 shipped m4a files |
| [catalog-png-digests-2026-11-03.md](catalog-png-digests-2026-11-03.md) | Catalog digests against the 1030 shipped PNG files |
| [world-layer-order-2026-11-03.md](world-layer-order-2026-11-03.md) | World layers 0 through 14, and the roots above that stack |
| [layer-offsets-2026-11-03.md](layer-offsets-2026-11-03.md) | Foundation, gate, ghost, and camera-badge offsets inside a layer |
| [haptic-patterns-2026-11-03.md](haptic-patterns-2026-11-03.md) | The six haptic patterns and the UIKit call each one makes |
| [player-weapon-cues-2026-11-03.md](player-weapon-cues-2026-11-03.md) | Civic Pulse, impact, player damage, and dodge cues |
| [camera-cues-2026-11-03.md](camera-cues-2026-11-03.md) | Camera hit, critical, destroy, field-off, and tamper cues |
| [run-state-cues-2026-11-03.md](run-state-cues-2026-11-03.md) | Detection, lockdown, extraction, blackout, and terminal cues |
| [boss-upgrade-cues-2026-11-03.md](boss-upgrade-cues-2026-11-03.md) | Boss telegraph and phase cues, the three upgrades, and the lethal warning |
| [effect-voice-ceiling-2026-11-03.md](effect-voice-ceiling-2026-11-03.md) | Eight effect voices, and which cue is dropped first |
| [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md) | Mix defaults, crossfades, music beds, and the blackout drop |
| [camera-follow-2026-11-03.md](camera-follow-2026-11-03.md) | The scene follow, the snapshot framing, and the shake added to the camera node |
| [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md) | Detection bands and the exposure added or removed on a tick |
| [medal-predicates-2026-11-03.md](medal-predicates-2026-11-03.md) | The five medals a successful run can earn |
| [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md) | Signal Jammer, Ricochet Pulse, and Ghost Step as shipped |
| [player-movement-2026-11-04.md](player-movement-2026-11-04.md) | Walk, dodge, and the slide of the player circle |
| [player-integrity-2026-11-04.md](player-integrity-2026-11-04.md) | The 50 percent loss scale, contact, and the court floor |
| [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md) | Civic Pulse cadence, travel, and damage |
| [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md) | The five standard enemies and the one special each has |
| [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md) | The elite cycle and the four boss attacks |
| [encounter-waves-2026-11-04.md](encounter-waves-2026-11-04.md) | M-A, M-B, and M-C waves, triggers, and totals |
| [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md) | Heat counts, awareness, and the Transit Patrol |
| [extraction-and-tick-2026-11-04.md](extraction-and-tick-2026-11-04.md) | Extraction arm and countdown, and the order of one tick |
| [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md) | Eight placed cameras, integrity 3, and the shared geometry |
| [hud-bindings-2026-11-04.md](hud-bindings-2026-11-04.md) | The numbers and labels the HUD draws on the existing shapes |
| [hit-order-2026-11-04.md](hit-order-2026-11-04.md) | Earliest hit, then a wall, then the lower ids |
| [target-order-2026-11-04.md](target-order-2026-11-04.md) | Close enemy, chosen camera, then other enemy |
| [projectile-step-2026-11-04.md](projectile-step-2026-11-04.md) | A projectile steps after its first tick, then retires |
| [forward-gates-2026-11-04.md](forward-gates-2026-11-04.md) | Encounter gates, the elite gate at plus 60, and the boss gate |
| [camera-destruction-record-2026-11-04.md](camera-destruction-record-2026-11-04.md) | The destruction record and the blackout latch at eight |
| [spawn-socket-choice-2026-11-04.md](spawn-socket-choice-2026-11-04.md) | Farthest fair socket, offscreen first, on the 896×414 rules view |
| [intro-sequence-2026-11-04.md](intro-sequence-2026-11-04.md) | The title hold, the field power-on, and the reduced-motion fade |
| [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md) | Tutorial cards, one line at a time, and the encounter-label hold |
| [control-rects-2026-11-04.md](control-rects-2026-11-04.md) | Stick, dodge, and pause on the reference canvas |
| [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md) | Local settings, and what the receipt may declare |
| [touch-command-2026-11-04.md](touch-command-2026-11-04.md) | The stick dead zone, the remap, and the one dodge edge |
| [pause-2026-11-04.md](pause-2026-11-04.md) | Pause stops the step and clears the held touch |
| [hit-stop-2026-11-04.md](hit-stop-2026-11-04.md) | The 50 ms and 90 ms freezes, and the 15-tick coalesce |
| [lockdown-tint-2026-11-04.md](lockdown-tint-2026-11-04.md) | The world tint from 6 percent to 10 percent |
| [caption-board-2026-11-04.md](caption-board-2026-11-04.md) | Three captions, safety first, for 150 ticks |
| [fog-thinning-2026-11-04.md](fog-thinning-2026-11-04.md) | Fog eases to half opacity while an aware enemy is in view |
| [upgrade-cards-2026-11-04.md](upgrade-cards-2026-11-04.md) | The three card sentences and their selection indexes |
| [terminal-surface-2026-11-04.md](terminal-surface-2026-11-04.md) | The results panel, Restart, Share, and Rehearse Court |
| [player-spawn-2026-11-04.md](player-spawn-2026-11-04.md) | The player spawn at (160, 192), heading 0 |
| [restart-and-rehearsal-2026-11-04.md](restart-and-rehearsal-2026-11-04.md) | Restart keeps the seed; rehearsal restores the court snapshot |
| [clip-frame-clock-2026-11-04.md](clip-frame-clock-2026-11-04.md) | Frame selection at 60 Hz, rounded up, last frame held |
| [ghost-replay-2026-11-04.md](ghost-replay-2026-11-04.md) | The best ghost, verified, fading over 30 ticks |
| [run-card-2026-11-04.md](run-card-2026-11-04.md) | The m:ss clock, NEW BEST, and the incident report |
| [terminal-speech-2026-11-04.md](terminal-speech-2026-11-04.md) | What VoiceOver reads on the results surface |
| [daily-seed-2026-11-04.md](daily-seed-2026-11-04.md) | The UTC day key and the first placement that passes |
| [daily-flavour-2026-11-04.md](daily-flavour-2026-11-04.md) | The day's grade, fog percent, and headline |
| [court-light-2026-11-04.md](court-light-2026-11-04.md) | The four boss-phase lights and the 60-tick crossfade |
| [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md) | The sealed tick and digest when a run ends |
| [replay-identity-2026-11-04.md](replay-identity-2026-11-04.md) | The four version strings a replay must match |
| [ambient-motion-2026-11-04.md](ambient-motion-2026-11-04.md) | Twelve ambient slots, one rare slot, and each recipe's period |
| [enemy-separation-2026-11-04.md](enemy-separation-2026-11-04.md) | The lower id is pushed inside radii plus 8 |
| [camera-contact-2026-11-04.md](camera-contact-2026-11-04.md) | The cone, the live solids, and the sorted contacts |
| [state-digest-2026-11-04.md](state-digest-2026-11-04.md) | The fields in the SHA-256 state digest |
| [share-text-2026-11-04.md](share-text-2026-11-04.md) | The incident-report lines Share sends |
| [rng-streams-2026-11-04.md](rng-streams-2026-11-04.md) | The combat stream and the cosmetic stream |
| [captain-path-2026-11-04.md](captain-path-2026-11-04.md) | The corner search, and the orbit while the line is clear |
| [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md) | One world unit is 256 raw |
| [circle-slide-2026-11-04.md](circle-slide-2026-11-04.md) | X then Y, and a touch is not a penetration |
| [corner-pursuit-2026-11-04.md](corner-pursuit-2026-11-04.md) | One corner, recomputed, reached at 8 |
| [arena-bounds-2026-11-04.md](arena-bounds-2026-11-04.md) | The arena from (0, 0) to (2304, 1536) |
| [ricochet-continuation-2026-11-04.md](ricochet-continuation-2026-11-04.md) | A defeated enemy or any damageable camera continues once, then resolves the same tick |
| [replay-commands-2026-11-04.md](replay-commands-2026-11-04.md) | Load checks, a missing command is neutral, and the ghost omits neutral steps |
| [millidegree-2026-11-04.md](millidegree-2026-11-04.md) | Clockwise millidegrees, the CORDIC table, and the heading unit |
| [run-receipt-2026-11-04.md](run-receipt-2026-11-04.md) | The `run-receipt-001` fields |
| [mine-resolution-2026-11-04.md](mine-resolution-2026-11-04.md) | Arm and life countdowns, then one detonation inside the radius |
| [enemy-bands-2026-11-04.md](enemy-bands-2026-11-04.md) | The five steering bands and the orbit perpendicular |
| [canonical-json-2026-11-04.md](canonical-json-2026-11-04.md) | Sorted keys, decimal integers, and the string escapes |
| [daemon-query-2026-11-04.md](daemon-query-2026-11-04.md) | Three query markers, 14 per circle, and the dash literal |
| [spawn-lethal-volumes-2026-11-04.md](spawn-lethal-volumes-2026-11-04.md) | The volumes a fair socket must sit strictly outside |
| [extraction-presence-2026-11-04.md](extraction-presence-2026-11-04.md) | The truncated player point against the inclusive extraction box |
| [boss-attack-clock-2026-11-04.md](boss-attack-clock-2026-11-04.md) | Recovery consumes the tick; the attack resolves when the telegraph hits zero |
| [boss-attack-resolve-2026-11-04.md](boss-attack-resolve-2026-11-04.md) | The four resolves, the dropped lane, and the field pulse |
| [observation-pulse-2026-11-04.md](observation-pulse-2026-11-04.md) | The phase ratio and the jammer, applied before the exposure add |
| [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md) | Surveillance, then damage, sight, and one ally hop |
| [patrol-sight-2026-11-04.md](patrol-sight-2026-11-04.md) | The patrol cone, and the spawn pose |
| [unaware-movement-2026-11-04.md](unaware-movement-2026-11-04.md) | The drift, the dwell, and the hold at a waypoint |
| [camera-legal-set-2026-11-04.md](camera-legal-set-2026-11-04.md) | Four housings, four return-visible, and the Z-02 tutorial socket |
| [combat-authority-node-2026-11-04.md](combat-authority-node-2026-11-04.md) | The current node, and the receipt order of the phases |
| [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md) | The zero-width segment against a solid box |
| [lethal-warning-2026-11-04.md](lethal-warning-2026-11-04.md) | The sixty-tick contact copy, and a telegraph that would exhaust |
| [actor-clip-choice-2026-11-04.md](actor-clip-choice-2026-11-04.md) | Idle while unaware, then the state clip |
| [facing-direction-2026-11-04.md](facing-direction-2026-11-04.md) | The velocity letter, and the heading sector |
| [player-clip-2026-11-04.md](player-clip-2026-11-04.md) | Defeat, extraction, dodge, then idle or move |
| [reaction-clips-2026-11-04.md](reaction-clips-2026-11-04.md) | Hurt, defeat, and the held commit |
| [camera-clip-states-2026-11-04.md](camera-clip-states-2026-11-04.md) | The clip follows integrity |
| [telegraph-shapes-2026-11-04.md](telegraph-shapes-2026-11-04.md) | The preview cone, the lanes, and the emitter field |
| [encounter-completion-2026-11-04.md](encounter-completion-2026-11-04.md) | The last wave, and M-A's upgrade gate |
| [exposure-events-2026-11-04.md](exposure-events-2026-11-04.md) | Phase 13 for the amount, phase 14 for the state |
| [medal-record-2026-11-04.md](medal-record-2026-11-04.md) | The sampling call, and today's stored set |
| [boss-bar-2026-11-04.md](boss-bar-2026-11-04.md) | The bar, the transition fill, and the short phase name |
| [hud-anchors-2026-11-04.md](hud-anchors-2026-11-04.md) | Top-left, top-centre, top-right, and centre |
| [combat-feedback-marks-2026-11-04.md](combat-feedback-marks-2026-11-04.md) | The shot marks, the jammer arcs, and the concealment corners |
| [telegraph-ring-2026-11-04.md](telegraph-ring-2026-11-04.md) | The boss ring from 72 to 18, and the court shader |
| [receipt-archive-2026-11-04.md](receipt-archive-2026-11-04.md) | Fifty receipts, the UTC name, and the rehearsal skip |
| [settings-persistence-2026-11-04.md](settings-persistence-2026-11-04.md) | The defaults file, and Reduce Motion until the player chooses |
| [actor-silhouettes-2026-11-04.md](actor-silhouettes-2026-11-04.md) | The eight blockout contours |
| [faction-outline-2026-11-04.md](faction-outline-2026-11-04.md) | The player stroke, and the enemy dash |
| [gate-barrier-2026-11-04.md](gate-barrier-2026-11-04.md) | Tiles, the open-face strip, and the lights |
| [vfx-pool-2026-11-04.md](vfx-pool-2026-11-04.md) | The recipe pool, the rank, and the frame lifetime |
| [upgrade-choice-layout-2026-11-04.md](upgrade-choice-layout-2026-11-04.md) | One column or three, and the spoken card |
| [heat-caption-2026-11-04.md](heat-caption-2026-11-04.md) | The last wave's count, for 300 ticks, in the boss-bar slot |
| [quiet-approach-tag-2026-11-04.md](quiet-approach-tag-2026-11-04.md) | The tag, the lost caption, and the paid caption |
| [spoken-hud-2026-11-04.md](spoken-hud-2026-11-04.md) | Tutorial, reinforcements, then safety captions, each once |
| [exposure-pattern-2026-11-04.md](exposure-pattern-2026-11-04.md) | The five bar patterns, and the tamper-floor marker |
| [camera-field-polygon-2026-11-04.md](camera-field-polygon-2026-11-04.md) | Display rays, corner offsets, and the slab reach |
| [patrol-cone-outline-2026-11-04.md](patrol-cone-outline-2026-11-04.md) | Twenty-four rays, clipped, from the content cone |
| [takedown-streak-2026-11-04.md](takedown-streak-2026-11-04.md) | An unaware kill, the streak reset, and the pitched impact |
| [patrol-near-miss-2026-11-04.md](patrol-near-miss-2026-11-04.md) | The wide cone, the true sight test, and the edge pulse |
| [tutorial-line-offer-2026-11-04.md](tutorial-line-offer-2026-11-04.md) | The patrol line, the awareness line, and what blocks them |
| [camera-notch-window-2026-11-04.md](camera-notch-window-2026-11-04.md) | Live notches, the hit window, and the tamper window |
| [ghost-file-2026-11-04.md](ghost-file-2026-11-04.md) | One daily file, replaced only when it is the best |
| [settings-surface-2026-11-04.md](settings-surface-2026-11-04.md) | The five sliders, the pickers, and Resume |
| [shell-host-2026-11-04.md](shell-host-2026-11-04.md) | The title, the settings sheet, and the 60-frame view |
| [intro-card-2026-11-04.md](intro-card-2026-11-04.md) | The veil, the title, and the two lines under it |
| [fog-drift-2026-11-04.md](fog-drift-2026-11-04.md) | The density split, and the two drift speeds |
| [terminal-access-2026-11-04.md](terminal-access-2026-11-04.md) | The clear buttons, and the reflowed card |
| [title-chrome-2026-11-04.md](title-chrome-2026-11-04.md) | The scrim, the pressed plate, and the medal colours |
| [audio-interruption-2026-11-04.md](audio-interruption-2026-11-04.md) | Silence while interrupted, then the stored bed |
| [share-sheet-2026-11-04.md](share-sheet-2026-11-04.md) | One string, on the system sheet |
| [ghost-silhouette-2026-11-04.md](ghost-silhouette-2026-11-04.md) | The blockout under the live player |
| [ground-tint-2026-11-04.md](ground-tint-2026-11-04.md) | One blend per tile, from the corner |
| [hud-fit-2026-11-04.md](hud-fit-2026-11-04.md) | The safe canvas, and the control floor |
| [control-chrome-2026-11-04.md](control-chrome-2026-11-04.md) | The stick label, DODGE, and PAUSED |
| [tutorial-plate-2026-11-04.md](tutorial-plate-2026-11-04.md) | The card behind the one line |
| [clip-playback-2026-11-04.md](clip-playback-2026-11-04.md) | Nearest frames, and the running action |
| [heading-draw-2026-11-04.md](heading-draw-2026-11-04.md) | The negated heading, and the plain span |
| [exposure-fills-2026-11-04.md](exposure-fills-2026-11-04.md) | Five fills, inset inside the frame |
| [terminal-chrome-2026-11-04.md](terminal-chrome-2026-11-04.md) | The scrim, the rows, and the accolade |
| [scene-frame-2026-11-04.md](scene-frame-2026-11-04.md) | The scene colour, and aspect fit |
| [mount-solids-2026-11-04.md](mount-solids-2026-11-04.md) | A mount is omitted from the solid draw |
| [camera-reticle-2026-11-04.md](camera-reticle-2026-11-04.md) | The corners when detection leaves hidden |
| [exposure-brackets-2026-11-04.md](exposure-brackets-2026-11-04.md) | The screen corners for tracked, hunted, or lockdown |
| [damage-impact-2026-11-04.md](damage-impact-2026-11-04.md) | The ring or the arc, and the two-frame circle |
| [enemy-spark-2026-11-04.md](enemy-spark-2026-11-04.md) | The reduced circle, and the traveling squares |
| [enemy-burst-2026-11-04.md](enemy-burst-2026-11-04.md) | The debris squares, and the short reduced reach |
| [step-echo-2026-11-04.md](step-echo-2026-11-04.md) | The silhouette echo every three frames |
| [ricochet-trace-2026-11-04.md](ricochet-trace-2026-11-04.md) | The dashed pair, and the impact marks |
| [lockdown-frame-2026-11-04.md](lockdown-frame-2026-11-04.md) | The edge bars, and the broken ring |
| [camera-shatter-2026-11-04.md](camera-shatter-2026-11-04.md) | The crack, the shards, and the sparks |
| [blackout-card-2026-11-04.md](blackout-card-2026-11-04.md) | The title, the dim, and the field cascade |
| [takedown-ring-2026-11-05.md](takedown-ring-2026-11-05.md) | The grey wash, and the pale ring |
| [unbacked-body-2026-11-05.md](unbacked-body-2026-11-05.md) | The role fill when the clip is missing |
| [camera-fallback-2026-11-05.md](camera-fallback-2026-11-05.md) | Four whites for a missing camera clip |
| [integrity-ink-2026-11-05.md](integrity-ink-2026-11-05.md) | The healthy fill, and the numeral |
| [objective-ink-2026-11-05.md](objective-ink-2026-11-05.md) | Left labels, and the blackout colour |
| [decoration-turn-2026-11-05.md](decoration-turn-2026-11-05.md) | The milli-degree turn, counter-clockwise |
| [outline-seat-2026-11-05.md](outline-seat-2026-11-05.md) | The grown mask, and the shifted anchor |
| [title-type-2026-11-05.md](title-type-2026-11-05.md) | The headline size, and the button type |
| [grade-margin-2026-11-05.md](grade-margin-2026-11-05.md) | One fog tile past the arena, each side |
| [notch-seat-2026-11-05.md](notch-seat-2026-11-05.md) | Beside the camera line, one step down |
| [captain-mark-2026-11-05.md](captain-mark-2026-11-05.md) | The diamond, or the contracting ring |
| [extraction-brackets-2026-11-05.md](extraction-brackets-2026-11-05.md) | The zone corners, and the inward bits |
| [phase-slam-2026-11-05.md](phase-slam-2026-11-05.md) | The phase words, and the broken ring |
| [spawn-chevrons-2026-11-05.md](spawn-chevrons-2026-11-05.md) | Up to six marks, aimed at the sockets |
| [alert-mark-2026-11-05.md](alert-mark-2026-11-05.md) | The exclamation above the enemy |
| [caption-column-2026-11-05.md](caption-column-2026-11-05.md) | Safety with a bar, routine without |
| [outline-cache-2026-11-05.md](outline-cache-2026-11-05.md) | 128 entries, and the byte cap |
| [extraction-sweep-2026-11-05.md](extraction-sweep-2026-11-05.md) | The clockwise arc, and the numeral |
| [detection-ink-2026-11-05.md](detection-ink-2026-11-05.md) | Lockdown in the critical colour |
| [upgrade-badge-2026-11-05.md](upgrade-badge-2026-11-05.md) | The panel, the frame, and the glyph |
| [mix-readout-2026-11-05.md](mix-readout-2026-11-05.md) | The percent, and the spoken value |
| [title-access-2026-11-05.md](title-access-2026-11-05.md) | The hidden art, and the spoken lines |
| [lip-seat-2026-11-05.md](lip-seat-2026-11-05.md) | The quarter strip, and the band centres |
| [camera-badge-seat-2026-11-05.md](camera-badge-seat-2026-11-05.md) | Thirteen left, and eighteen up |
| [fog-grid-2026-11-05.md](fog-grid-2026-11-05.md) | One tile outside the arena |
| [ground-walk-2026-11-05.md](ground-walk-2026-11-05.md) | Tiles from the arena corner |
| [env-filter-2026-11-05.md](env-filter-2026-11-05.md) | Nearest pixels, cached by asset |
| [phase-seat-2026-11-05.md](phase-seat-2026-11-05.md) | The phase word, one bar down |
| [marker-align-2026-11-05.md](marker-align-2026-11-05.md) | The question mark, from its bottom |
| [stick-zone-2026-11-05.md](stick-zone-2026-11-05.md) | The thumb half, below the top band |
| [settings-footnotes-2026-11-05.md](settings-footnotes-2026-11-05.md) | The four footers under the sections |
| [settings-hints-2026-11-05.md](settings-hints-2026-11-05.md) | Captions, scale, handedness, and the ghost |
| [heat-type-2026-11-05.md](heat-type-2026-11-05.md) | The reinforcement label at size 11 |
| [quiet-type-2026-11-05.md](quiet-type-2026-11-05.md) | The tag at 10, and the caption at 11 |
| [streak-type-2026-11-05.md](streak-type-2026-11-05.md) | The streak label at size 11 |
| [extraction-numeral-2026-11-05.md](extraction-numeral-2026-11-05.md) | The seconds, and the clockwise arc |
| [medal-type-2026-11-05.md](medal-type-2026-11-05.md) | The seal at 11, and the name at 10 |
| [upgrade-plate-2026-11-05.md](upgrade-plate-2026-11-05.md) | The card padding, and the corner |
| [terminal-type-2026-11-05.md](terminal-type-2026-11-05.md) | The reflowed type, and the button plate |
| [pattern-ink-2026-11-05.md](pattern-ink-2026-11-05.md) | A clear fill, and the pale stroke |
| [clip-interrupt-2026-11-05.md](clip-interrupt-2026-11-05.md) | The cancel window, and the commit cut |
| [pitched-voice-2026-11-05.md](pitched-voice-2026-11-05.md) | The pitch node, reconnected |
| [ambient-roll-2026-11-05.md](ambient-roll-2026-11-05.md) | The rare roll, and who is dropped |
| [visual-gate-2026-11-05.md](visual-gate-2026-11-05.md) | The visual contract, refused |
| [clip-gate-2026-11-05.md](clip-gate-2026-11-05.md) | The clip contract, refused |
| [redraw-order-2026-11-05.md](redraw-order-2026-11-05.md) | The frame, from the intro to the HUD |
| [present-pass-2026-11-05.md](present-pass-2026-11-05.md) | The tick, from the command to the caption |
| [court-capture-2026-11-05.md](court-capture-2026-11-05.md) | The court, stored on the first boss tick |
| [damage-log-2026-11-05.md](damage-log-2026-11-05.md) | The damage log, last 512 |
| [field-cache-2026-11-05.md](field-cache-2026-11-05.md) | The field polygon, cached |
| [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md) | The evidence file names |
| [run-streak-2026-11-05.md](run-streak-2026-11-05.md) | A success adds one |
| [playtest-load-2026-11-05.md](playtest-load-2026-11-05.md) | The playtest file, loaded |
| [catalog-gate-2026-11-05.md](catalog-gate-2026-11-05.md) | The asset catalog, refused |
| [ambient-gate-2026-11-05.md](ambient-gate-2026-11-05.md) | The ambient contract, refused |
| [frame-backing-2026-11-05.md](frame-backing-2026-11-05.md) | A direction, fully backed |
| [frame-times-2026-11-05.md](frame-times-2026-11-05.md) | The frame sample, and gate C |
| [expansion-gate-2026-11-05.md](expansion-gate-2026-11-05.md) | The expansion gate, computed |
| [draw-pass-2026-11-05.md](draw-pass-2026-11-05.md) | The world pass, in call order |
| [device-sample-2026-11-05.md](device-sample-2026-11-05.md) | The phone sample, beside the frames |
| [playtest-gates-2026-11-05.md](playtest-gates-2026-11-05.md) | The playtest gates, five and four |
| [device-run-gates-2026-11-05.md](device-run-gates-2026-11-05.md) | The device-run gates, and the nil atlas |
| [peak-density-2026-11-05.md](peak-density-2026-11-05.md) | The peak the profiler keeps |
| [ceiling-status-2026-11-05.md](ceiling-status-2026-11-05.md) | The ceiling, measured then settled |
| [replay-matrix-2026-11-05.md](replay-matrix-2026-11-05.md) | The replay matrix, three times |
| [asset-intake-2026-11-05.md](asset-intake-2026-11-05.md) | The intake, against the files |
| [bundle-filter-2026-11-05.md](bundle-filter-2026-11-05.md) | The bundle, reachable ids |
| [pacing-window-2026-11-05.md](pacing-window-2026-11-05.md) | The pacing windows |
| [env-groups-2026-11-05.md](env-groups-2026-11-05.md) | A group, fully backed |
| [seam-checks-2026-11-05.md](seam-checks-2026-11-05.md) | The seam checks |
| [event-order-2026-11-05.md](event-order-2026-11-05.md) | The published order |
| [upgrade-match-2026-11-05.md](upgrade-match-2026-11-05.md) | The upgrade block, matched |
| [content-bands-2026-11-05.md](content-bands-2026-11-05.md) | The bands, the angle, and the percents |
| [awareness-heat-2026-11-05.md](awareness-heat-2026-11-05.md) | The awareness block, and the heat table |
| [arena-reach-2026-11-05.md](arena-reach-2026-11-05.md) | The walk, and the spine |
| [patrol-fair-2026-11-05.md](patrol-fair-2026-11-05.md) | The patrol proof |
| [camera-fair-2026-11-05.md](camera-fair-2026-11-05.md) | The camera sets, checked |
| [camera-receipt-2026-11-05.md](camera-receipt-2026-11-05.md) | The destruction totals |
| [gate-spans-2026-11-05.md](gate-spans-2026-11-05.md) | The gate ids, and the unmapped ones |
| [candidate-collect-2026-11-05.md](candidate-collect-2026-11-05.md) | The candidate the collector builds |
| [integer-roots-2026-11-05.md](integer-roots-2026-11-05.md) | The integer roots |
| [circle-sweep-2026-11-05.md](circle-sweep-2026-11-05.md) | The circle sweep |
| [lead-aim-2026-11-05.md](lead-aim-2026-11-05.md) | The lead on a shot |
| [enemy-grammar-2026-11-05.md](enemy-grammar-2026-11-05.md) | The enemy block, loaded |
| [waypoint-pilot-2026-11-05.md](waypoint-pilot-2026-11-05.md) | The waypoint pilot |
| [probe-order-2026-11-05.md](probe-order-2026-11-05.md) | The probe's order |
| [layout-check-2026-11-05.md](layout-check-2026-11-05.md) | The layout check |
| [civic-slots-2026-11-05.md](civic-slots-2026-11-05.md) | The civic slots |
| [detection-shapes-2026-11-05.md](detection-shapes-2026-11-05.md) | The detection shapes |
| [tutorial-flags-2026-11-05.md](tutorial-flags-2026-11-05.md) | The tutorial flags this tick |
| [sha-padding-2026-11-05.md](sha-padding-2026-11-05.md) | The hash padding |
| [bundle-load-2026-11-05.md](bundle-load-2026-11-05.md) | The bundled lookup |
| [telemetry-sample-2026-11-05.md](telemetry-sample-2026-11-05.md) | The telemetry sample |
| [q8-offset-2026-11-05.md](q8-offset-2026-11-05.md) | The offset along a direction |
| [live-solids-2026-11-05.md](live-solids-2026-11-05.md) | The solids this tick |
| [box-edges-2026-11-05.md](box-edges-2026-11-05.md) | The box edges |
| [vfx-budgets-2026-11-05.md](vfx-budgets-2026-11-05.md) | The effect budgets |
| [vfx-project-2026-11-05.md](vfx-project-2026-11-05.md) | The effect projection |
| [probe-sidestep-2026-11-05.md](probe-sidestep-2026-11-05.md) | The probe's sidestep |
| [probe-grid-2026-11-05.md](probe-grid-2026-11-05.md) | The probe's grid |
| [probe-replan-2026-11-05.md](probe-replan-2026-11-05.md) | The probe's replan |
| [probe-firing-2026-11-05.md](probe-firing-2026-11-05.md) | The probe's firing cell |
| [probe-ambush-2026-11-05.md](probe-ambush-2026-11-05.md) | The probe's ambush cell |
| [probe-fields-2026-11-05.md](probe-fields-2026-11-05.md) | The probe's camera fields |
| [probe-loud-2026-11-05.md](probe-loud-2026-11-05.md) | The probe's camera walk |
| [probe-hide-2026-11-05.md](probe-hide-2026-11-05.md) | The probe's hide |
| [probe-heading-2026-11-05.md](probe-heading-2026-11-05.md) | The probe's heading |
| [anchor-offset-2026-11-05.md](anchor-offset-2026-11-05.md) | The camera offset |
| [view-contains-2026-11-05.md](view-contains-2026-11-05.md) | The view contains a point |
| [utf8-order-2026-11-05.md](utf8-order-2026-11-05.md) | The byte order |
| [hint-latch-2026-11-05.md](hint-latch-2026-11-05.md) | The hint, shown once |
| [offscreen-sector-2026-11-05.md](offscreen-sector-2026-11-05.md) | The offscreen sector |
| [clip-select-2026-11-05.md](clip-select-2026-11-05.md) | The selected frames |
| [upgrade-accept-2026-11-05.md](upgrade-accept-2026-11-05.md) | The one upgrade accept |
| [touch-route-2026-11-05.md](touch-route-2026-11-05.md) | The touch route |
| [court-rehearse-2026-11-05.md](court-rehearse-2026-11-05.md) | The rehearsal card |
| [intro-frame-2026-11-05.md](intro-frame-2026-11-05.md) | The intro frame |
| [concealment-flag-2026-11-05.md](concealment-flag-2026-11-05.md) | The concealment flag |
| [body-clearance-2026-11-05.md](body-clearance-2026-11-05.md) | The body clearance |
| [ghost-verify-2026-11-05.md](ghost-verify-2026-11-05.md) | The ghost's second check |
| [camera-overlay-2026-11-05.md](camera-overlay-2026-11-05.md) | The camera event overlay |
| [daemon-expiry-2026-11-05.md](daemon-expiry-2026-11-05.md) | The daemon expiry |
| [pool-rejects-2026-11-05.md](pool-rejects-2026-11-05.md) | The pool rejects |
| [captain-field-2026-11-05.md](captain-field-2026-11-05.md) | The captain field sprite |
| [outline-weight-2026-11-05.md](outline-weight-2026-11-05.md) | The outline weight |
| [display-delta-2026-11-05.md](display-delta-2026-11-05.md) | The display interval |
| [view-clamp-2026-11-05.md](view-clamp-2026-11-05.md) | The view clamp |
| [closest-point-2026-11-05.md](closest-point-2026-11-05.md) | The closest point |
| [defeat-count-2026-11-05.md](defeat-count-2026-11-05.md) | The defeat count |
| [diagnostic-seal-2026-11-05.md](diagnostic-seal-2026-11-05.md) | The diagnostic seal |
| [court-luma-2026-11-06.md](court-luma-2026-11-06.md) | The court luma, and the exact lerp ends |
| [fog-clock-2026-11-06.md](fog-clock-2026-11-06.md) | The fog clock, on the first sample |
| [fog-unbacked-2026-11-06.md](fog-unbacked-2026-11-06.md) | Fog steps, then draws nothing |
| [camera-assert-2026-11-06.md](camera-assert-2026-11-06.md) | The camera array, already sorted |
| [spawn-mounts-2026-11-06.md](spawn-mounts-2026-11-06.md) | The spawn mounts, in the flood |
| [socket-lists-2026-11-06.md](socket-lists-2026-11-06.md) | The socket lists, not a rejection |
| [medal-directory-2026-11-06.md](medal-directory-2026-11-06.md) | The medal directory, DailyMedals |
| [patrol-spawn-2026-11-06.md](patrol-spawn-2026-11-06.md) | The patrol spawn, without fairness |

Next session: follow [retest-checklist.md](retest-checklist.md) (D-105 allows device checks on any build).
