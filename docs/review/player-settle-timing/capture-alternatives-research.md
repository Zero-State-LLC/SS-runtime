# Capture alternatives — 2026-10-19

Status: researched recommendation, not implemented or accepted evidence. No production timing, geometry, art, or acceptance gate changes.

## Evidence and decision

The matched recorded/unrecorded experiment in recording-control-review.md shows movie gaps up to101.667ms and incomplete callback pose coverage in one recorded release. The unrecorded midpoint runs observed17/17 poses. This suggests capture/system load contributes, but does not establish causation or physical presentation. QuickTime/Screenshot is inaccessible through the current UI route, including after manual assistance.

Recommendation: separate visual correctness from live presentation measurement. Prefer extending the existing native SpriteKit export fixture over writing a new desktop recorder or replacing the production renderer.

1. Export a deterministic full-scene sequence from the actual renderer at explicit test timestamps. Reuse the source textures, animation selection, registration, camera transforms and ground; retain the full idle tail. Apple's SKView texture(from:crop:) renders node content into a texture. Existing node-local34-pose captures establish feasibility but do not yet include complete world-space motion/contact context. First verify camera/crop/scale parity against native screenshots at selected matching states. If SKView snapshot semantics cannot preserve that context, investigate SKRenderer as a test-only offscreen backend; do not migrate production rendering for capture convenience.
2. Produce separate normal and quarter-speed reviews from those native rendered frames. Preserve the accepted0.375s timeline and its endpoint semantics. Include a manifest of simulation time, animation state, pose index, world/camera transform and image hash. Evaluate the 60Hz sampled sequence separately from an exhaustive authored-pose plate: not every possible timeline sample implies an actual displayed frame. No optical-flow interpolation. Label exports as deterministic renderer playback, not live screen recordings.
3. Profile the unchanged live SKView run with recording disabled. Use Instruments to inspect frame lifetimes/hitches; first confirm the available tracks actually cover this SpriteKit workload. Callback timing remains supplementary. Apple recommends real-device profiling for realistic hitch results; simulator evidence must not close device performance gates. If Instruments lacks presentation evidence for this workload, keep the live cadence gate open rather than substituting callback counts.
4. Optional independent live video: OBS Studio's modern macOS Screen Capture source, Window Capture mode, selecting only Simulator, cursor/audio disabled. This bypasses the Screenshot toolbar, but still requires macOS recording permission and can add load. Compare recorder-on/off runs and inspect timestamp gaps/visible pose IDs. A nominal60fps export may repeat frames; frame rate alone is not proof. Stop if the same capture distortion recurs rather than cycling through recorders.

## Alternatives compared

| Approach | Useful evidence | Limitation / disposition |
| --- | --- | --- |
| Existing SKView native export extended to whole scene | Art, registration, overlap, world-space contact and intended timing | Cannot prove live presentation; recommended first |
| Instruments without video | Live render/presentation timing where supported | No visual anatomy proof; pair with exports |
| OBS ScreenCaptureKit window source | Independent live video, no Screenshot toolbar | Permission, install and recorder overhead; fallback |
| Custom ScreenCaptureKit helper | Window filtering and timestamped sample buffers | Adds maintenance and permissions; unnecessary first step |
| SKRenderer + Metal presentation callbacks | Explicit rendering and drawable presentation telemetry | Changes the rendering host; does not validate unchanged production SKView by itself; defer |

## Review and completion conditions

Start with accepted midpoint releases5/13, Standard and Reduced Motion. Review normal speed for weight transfer/cadence as authored; quarter speed for knee-pad orientation, heel/tongue ownership, boot/calf detail, coat overlap and arm motion. Inspect release-to-settle, settle-to-idle and full walk16→1 boundaries. Verify no automatic outline reappears. Expand phase/facing/action coverage only after this pilot passes.

A deterministic movie may unblock art/contact review, but does not silently waive the existing live-cadence gate before shared-scene advancement. Record visual and live-timing results separately. Current779 core tests remain prior regression evidence; this research introduces no executable change and reruns none.

## Primary sources

- Apple, node snapshot rendering: https://developer.apple.com/documentation/spritekit/creating-a-new-node-by-rendering-to-a-texture
- Apple, SKRenderer (scene into a Metal command buffer): https://developer.apple.com/documentation/spritekit/skrenderer
- Apple, explicit renderer time: https://developer.apple.com/documentation/spritekit/skrenderer/update(attime:)
- Apple, Instruments frame lifetimes and device guidance: https://developer.apple.com/documentation/xcode/improving-app-responsiveness
- Apple, presented drawable handler (only when owning the drawable): https://developer.apple.com/documentation/metal/mtldrawable/addpresentedhandler(_:)
- Apple, ScreenCaptureKit sample and permissions: https://developer.apple.com/documentation/screencapturekit/capturing-screen-content-in-macos
- OBS, modern macOS Screen Capture source and window selection: https://obsproject.com/kb/macos-screen-capture-source
- OBS, deprecated window capture comparison: https://obsproject.com/kb/window-capture-sources

These APIs support the proposed mechanisms. End-to-end suitability on this host is untested; the workflow choice is an engineering recommendation, not an Apple guarantee of lossless capture.
