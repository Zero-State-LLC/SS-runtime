# BP-003 v2 decoding and frame-duration pairing

Runtime base: 0d5fac0. Spec pin: 9a87f95ae52f3f174392418e333573a56c04100a.

The shared clip decoder now accepts the explicit clip-metadata-002 target representation. Version 1 requires fps and rejects timing; version 2 requires timing and rejects fps. Unknown schema/animation identities, unknown/missing timing keys, noninteger/boolean/invalid holds, parallel-array count mismatch, sum overflow and selected-facing tick-numerator overflow fail closed. Existing semantic validation remains in force.

V2 records carry no fps value. ClipRecord and ClipFrameLibrary preserve the complete validated integer timing, selecting frame indices and duration indices together. Interleaved frame IDs preserve the authored order and the correct facing's holds. V1 continues through the uniform-duration adapter. Renderer action construction already consumes ClipTiming rather than fps; each SpriteLibrary instance owns an immutable frame library, so its per-clip/facing action cache cannot mix timing definitions across libraries.

Tests mechanically convert every current clip and compare all record fields after normalizing representation, all authored frame lists and all facing durations. A technical interleaved fixture gives north/east/south/west independently expected 10/20/30/40-tick durations. Malformed v2 cases are tested through both catalog and delivery loading. Existing v1 timing assertions still explicitly require fps rather than substituting a default.

## Not yet production-ready

Bundled metadata, active clip version, asset owner references, exporters and shipped assets remain v1. No v2 clip is admitted by this change. ReactionClipTracker still calculates its lifetime from the first facing, so clips with unequal facing durations cannot be adopted until reaction selection and playback are reconciled. Direction changes during a one-shot also need an explicit phase/lifetime policy and renderer tests, not an assumption that restarting an action preserves elapsed time.

Research: Apple's [named action control](https://developer.apple.com/documentation/spritekit/controlling-actions-precisely-by-using-names) documents replacement by key; [Godot's transition documentation](https://docs.godotengine.org/en/stable/classes/class_animationnodetransition.html) makes reset/restart behavior an explicit setting. These establish that transition behavior is a decision; neither selects SS's design. Next work must define and compare phase retention or event-facing retention, verify selected-facing reaction lifetime, pause/resume, interruption and final texture retention, then migrate resources and versions together. New source animation and visual/device gates remain open.

## Validation

- Full core suite: 770 tests / 109 suites passed in 617.936 seconds, final source state. Command: `swift test --disable-sandbox --cache-path ../swift-cache --config-path ../swift-config --security-path ../swift-security`.
- iOS Simulator: 87 tests passed, 0 failed, 0 skipped (84 Swift Testing + 3 XCTest); iPhone 17 Pro iOS 26.5, UUID CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Xcode result Test-SSRuntime-2026.10.14_14-06-17--0700.xcresult. Existing app playback/interrupt/pause checks exercise active v1 plus the shared ClipTiming action constructor; they do not establish complete v2 lifecycle acceptance.
- No physical-device test. No active resource or gameplay identity changed.
