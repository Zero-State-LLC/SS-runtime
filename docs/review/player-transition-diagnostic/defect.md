# Defect: shared traversal diagnostic omits absent Player sprites

Status: diagnostic repair awaiting focused renderer validation; GitHub issue publication pending (api.github.com unavailable).

Prior six recorded traversals ended at tick 75 although authority reached tick 90. SharedTraversalScene.didEvaluateActions skipped warm-up and returned before recording whenever sprite-player was absent. All 16 movement textures could pass without any idle entry/exit evidence.

Repair retains every post-action callback, including warm-up; adds spritePresent, texturePresent and requestedClip; omits unavailable screen geometry rather than fabricating coordinates. Assertions require tick 0, tick 90, initial/final requested idle and presence flags. Existing movement/frame/authority assertions remain unchanged. This does not supply missing idle art or assert visual acceptance.

Spec authority: BP-008 transition evidence in benchmark-production.md and acceptance.md, under accepted visual-coherence intent. No gameplay or source animation change.

Verified 2026-10-19: focused Xcode test passed, 1 test / 0 failures, 20.544 seconds. All six attachments now span tick 0 through 90, retain missing-sprite/idle records and retain all 16 movement textures. Targeted core Clip tests: 66 tests / 11 suites passed. Missing idle artwork remains open; diagnostic repair is verified.
