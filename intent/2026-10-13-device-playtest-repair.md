# Device playtest repair intent

Date: 2026-10-13
Status: accepted

## Reported failure
User reports immediate heavy stuttering, broken animations, object clipping, glitching surveillance cameras, and whole-view jumps on the physical iPhone Release build from runtime main 6e42cb47e8be10cffcc8398cbf9e2fff5fbe7dac. Movement, Dodge, pause/resume, and restart passed the preceding manual checks. Device performance and presentation acceptance fail; no release-readiness claim is made.

## Verified source findings
- GameScene.redraw assigns the view camera directly to PresentationCamera.center. The center applies heading-dependent horizontal look-ahead without persistent smoothing or dead-zone state. This conflicts with animation.md section 9 and arena-layout.md camera framing.
- WorldRenderer.renderCameras builds an unoccluded conePath from range, heading and angle, with no solid geometry input. The displayed field can extend through cover even though authoritative LOS uses occlusion.
- OutlineTextures.outline synchronously reads texture.cgImage and generates outlined pixels on cache misses during rendering. This is a performance hypothesis, not a measured root cause.
- GameScene.update takes one simulation step per delivered frame while sprite clips use timed SKActions. Frame loss can desynchronize apparent motion; scheduling changes require preserving fixed-tick authority and pause/intro/hit-stop semantics.

## Proposed repair scope
1. Measure frame-time distribution and main-thread hot spots on the connected device before tuning. Preserve a reproducible seed and input sequence where possible.
2. Implement presentation-only camera dead zone, bounded look-ahead smoothing, and arena clamping per the pinned spec. Keep RulesViewport and simulation coordinates unchanged.
3. Project surveillance fields from authoritative camera/solid geometry; verify visible cover boundaries against detection. Investigate camera head/state animation separately.
4. Reproduce broken animation and object clipping, checking anchors, layer order, clip transitions, node lifetime, and outline synchronization. Fix demonstrated spec violations, not unspecified art redesign.
5. Remove measured runtime rendering stalls, with explicit bounded preload/cache behavior where appropriate. Do not sacrifice geometry truth or authored content to get a faster frame.
6. Add regression coverage for demonstrated gaps, file the required coverage defect, run core and Debug/Release app checks, then install the corrected Release build for the same device playtest.

## Acceptance
- Camera follows without direction-change snaps and honors the specified 76 x 50 dead zone and bounded look-ahead.
- Visible camera fields agree with solid occlusion and detection.
- Reproduced animation/clipping failures no longer occur in the same scenario.
- Record actual device/model, build, scenario and frame p95 against C-003 <=16.67 ms; do not label an unmeasured run passed.
- Replay golden states and identities remain unchanged for presentation-only fixes. Any necessary gameplay change requires a separate spec decision/version review.

## Authority and next step
Pinned spec 2377b99c6b6d1654e2cb976ee1b7e07b75c77e1a; constitution Articles III, IV, VII, VIII; animation.md section 9; arena-layout.md camera framing; C-003.
Runtime AGENTS.md requires human acceptance of a new non-trivial runtime-only intent before implementation. Accepted by the user on 2026-10-13: “ok approved. we may need a qa pass”. Include broader QA and device retest before claiming success.

## Expanded repair authorization

On 2026-10-13 the user requested: “go ahead and fix these issues, add the damage diagnostics and do a full qa pass before we test again”. This includes confirmed asset registration/fragment defects, visible collision footprint repair, and opt-in local damage-event/replay diagnostics. No further device retest is requested until automated and visual QA has been completed; remaining failures must be reported explicitly.

## Phases 1–2 authorization

User accepted spec deepening and combat fixes on 2026-10-13. D-103 versions collision/event changes as ruleset-008, with fixture review; this supersedes the original presentation-only constraint only for the specified combat repairs. Art and phase-3 effects remain deferred.
