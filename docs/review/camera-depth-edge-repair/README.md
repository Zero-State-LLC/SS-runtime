# BP-007/BP-009 Camera-post and exterior repair

Authorized by the user on 2026-10-16. Implemented in reusable review presentation (`BenchmarkProjectionFinishing`), exercised through real SpriteKit rendering. Production projection/art admission remains pending.

## Change

Ground-anchored actors sort by projected root Y, with stable name ties within the actor layer. A nearer Camera no longer draws behind a farther Player. An overlapping nearer Camera uses the existing proposed 0.35 occlusion treatment; a 16×6 contact ellipse marks Player ground position. Full opacity restores immediately on clearance or when the Player is nearer. Conservative canvas overlap is used, not pixel occlusion. Captures restore original node depth/opacity and remove temporary presentation nodes.

The inverse-projected viewport is covered outside the arena with existing 128-unit asphalt tiles, cropped at constant density and world-grid alignment. One tile of overscan avoids a clear-colour edge. An eight-unit outward curb and two-unit highlight mark the unchanged arena boundary. No gameplay state, movement bounds, collision, targeting, or field geometry changes.

## Evidence

- iPhone 17 Pro / iOS 26.5 Simulator: `testMovingCameraFixedReservationReview` passed in 128.991 s, 1 test / 0 failures. Result `Test-SSRuntime-2026.10.16_11-43-03--0700.xcresult`.
- Same 60 frames, ticks 4181–4299, fixed reservation, 1x zoom, 120-tick presentation warm-up. All focus coordinates match the preceding warmed capture exactly. Per-capture authoritative digest unchanged; player canvas stays inside the safe region without HUD overlap.
- Front/behind/clear/tie probes pass: correct ordering, 0.35 alpha during obscuration and full-alpha restoration. Camera 5 fades for frames 4–38 (35 samples), clears at frame 39 / tick 4259.
- Host SpriteKit inverse geometry: 6,732 exterior coverage probes across edges/corners/four zooms; exterior strips do not overlap the legal arena or each other. Existing 784 inverse corners and 36 HUD-safe placements also pass.
- Core: 779 tests / 110 suites passed in 593.697 s (`work/depth-edge-core-tests.log` at workspace level).
- Specs validator passed: 23 JSON artifacts, 7 schemas, 33 contracts, 55 indexed files. `git diff --check` passed.

## Visual inspection and limits

Start, overlap and exit frames show filled exterior street, visible boundary, and post fade/restore. Frame 30's formerly exposed upper-left region is filled. Remaining dark rectangular foundations are interior legacy solid presentation, not exterior world gaps. Building depth, mixed enemy/art scale, diagnostic outlines and complete animation remain open.

Normal video uses 30 capture frames/sec (2 s); quarter video uses 7.5 (8 s). These are 60 tick-sampled renders with paused SKActions and neutral facing poses; not continuous displayed animation, pixel-accurate occlusion, all-settings admission or physical-device evidence. Videos intentionally reset at the loop boundary. No device testing performed.

Research: https://developer.apple.com/documentation/spritekit/sknode/zposition and https://developer.apple.com/documentation/spritekit/skspritenode/anchorpoint establish draw-order/registration mechanisms. SS opacity, contact-cue and curb dimensions remain authored review choices.
