# Current runtime baseline — BP-001 / BP-006

Status: CAPTURED. Visual benchmark: FAILED. This is the current shipping-art baseline, not the revised shared sample.

Capture code runs the real GameScene, WorldRenderer and HUD. It skips the intro using the existing scene method, advances the simulation once, and renders the camera's 704×326 scene-coordinate viewport. A second attachment adds magenta outlines directly from the snapshot's authoritative solid AABBs. It does not infer collision from image bounds. SpriteKit actions are paused: these images cannot demonstrate animation fidelity.

Runtime base: ffa1132a6085430e129c6aea8cea8619e66b9a33 plus the new AppTests/BenchmarkCaptureTests.swift capture harness. Specification pin: 790676242b0761e6d4c9a3f78af6768fc0a41693. Xcode result: Test-SSRuntime-2026.10.14_08-41-20--0700.xcresult. Simulator: iPhone 17 Pro, iOS 26.5, device ID in manifest.json. Reproduce by running BenchmarkCaptureTests/testCaptureCurrentRuntimeBaseline in the SSRuntime scheme.

Local validation: capture XCTest passed; all 82 Swift Testing tests in 13 suites also passed. The previous runtime commit's CI passed all four jobs. These checks establish capture execution and regression coverage, not visual acceptance.

## Observed defects

- Player appears as a narrow side profile, inconsistent with the elevated environment and selected hooded benchmark.
- Ground utility-cover/stripe details visibly repeat in a grid.
- Haze reads as horizontal bands of repeated source forms.
- The camera silhouette is disproportionately large and reads as layered pieces near the top-right. The magenta mount box is much smaller than its artwork; these represent different things and must not be collapsed into one measurement.
- Ground rails change direction/overlap abruptly in the visible composition.
- The opening tutorial card occupies substantial lower-screen area; any benchmark composition must include this actual HUD rather than hide it for an attractive still.

## Export measurements

Logical crop: 704×326. SKView reports contentScaleFactor 1.0, but SpriteKit produced 2112×978 image pixels (3× each axis). Both observations are retained; no assumption that these values are interchangeable. Files suffixed 704 and 352 are explicit display-size derivatives. Grayscale derivatives use luminance conversion. Original attachments are unchanged and hashes are recorded.

## Next evidence

The accepted benchmark requires revised player, complete municipal camera, representative building and prop using one projection and apparent scale. This opening baseline does not satisfy that asset set. Candidate-source injection into the real renderer, quiet and dense encounter comparison, full animation capture, traversal/hit evidence and physical-device profiling remain outstanding.

Capture API basis: https://developer.apple.com/documentation/spritekit/skview/texture(from:crop:). Apple's API renders the requested node tree within a crop in that node's coordinate system. The harness converts camera viewport corners into scene coordinates before capture.
