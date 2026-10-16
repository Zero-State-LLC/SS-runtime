# Candidate device QA: failed

Build: 1135034 (b52b7fe adds baseline documentation only). Physical iPhone 17 Pro, iPhone18,1, iOS 26.3.1. User retest on 2026-10-13.

## Findings

1. **P1 — delivered camera animation frames contain separated fragments.** Visual inspection of actor_camera_operationalIdle_none_02@1x.png and frame 03 shows pieces at opposite image edges. The defect is present in the PNG files, before SpriteKit renders them. The renderer also layers a separate housing under the clip. The housing uses a centered anchor while the clip uses (32,88) in a 64x96 box. Composite registration and duplicated camera geometry require visual review. Do not claim smoothing fixes this.
2. **P1 — solid art leaves invisible blocking space.** renderSolids sizes each image to the authoritative AABB, but canvas dimensions are not the perceived solid base. env_solid_01_residential_west is 128x512 with nontransparent bounds (4,181)-(124,330); much of the blocking rectangle is visually empty. env_solid_13_phoenix_west is 64x256 with nontransparent bounds (5,102)-(59,153). This violates visual-assets.md section 6 (no transparent invitation into blocked space; footprint must not exceed perceived solid base). Preserve collision authority; repair presentation rather than deriving collision from alpha.
3. **P1 — asset readability and animation quality fail user acceptance.** User reports unrecognizable characters and broken animation. Static review confirms inconsistent fragments in several environment assets; temporal animation quality needs frame-sequence review. File coverage, hashes, dimensions, and attached actions are insufficient acceptance checks.
4. **Unresolved — hit detection.** User clarified the failure: taking damage when nothing visibly hits the player. Source review identifies contact overlap, armed mines, enemy/boss direct attacks, and swept projectiles as damage paths. No specific event or authority mismatch has yet been reproduced. Next reproduction must correlate playerDamaged sourceEntityId and tick with the visible source and warning; do not assume every hit should have a projectile or change combat rules without evidence.

## Measurement

Comparison Time Profiler Run 2 saved in local SS-baseline-device.trace: duration 3m17s, CPU weight approximately 1.28 min; main thread 1.11 min (86.9%); heaviest renderer stack 51.61s, flushRenderOps 35.55s. Different duration and uncontrolled gameplay prohibit a direct before/after performance claim. Rendering remains dominant.

Candidate console samples during gameplay reached p99 58.28ms and worst 591.83ms (startup included). A near-16.67ms p95 does not establish absence of visible hitches. Profile overhead and startup require separate reporting.

740 core tests in 104 suites passed. Physical QA remains failed regardless of automated results. PR #118 remains draft and issue #117 remains open.

## Required next work

Review complete frame sequences at gameplay scale; inspect asset delivery/source sheets and registration; establish readable solid footprints without changing authority; reproduce a reported hit event with visible authoritative geometry and event timing. Asset replacement is a separate content-quality decision from the camera-follow implementation. Do not mark existing art accepted solely because the ingestion script accepts PNG dimensions.
