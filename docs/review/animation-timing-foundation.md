# BP-003 exact timing foundation

Spec: c07ea6d3a9e2f3916fc69b73bf38bc8176911c3f. Runtime changes in the commit containing this record.

ClipTiming stores positive integer holds and timebase, validates selection order and checked arithmetic, and converts a selected cycle into ceiling-rounded 60 Hz lifetime. The existing v1 frame-rate delivery adapts into this model. SpriteLibrary consumes those holds at the SpriteKit seconds boundary; ReactionClipTracker uses the same duration model. The renderer has a variable-hold sequence construction path, tested independently from asset loading.

This is the shared timing foundation, not the v2 metadata migration or 16-frame art delivery. ClipRecord and ClipFrameLibrary still expose and decode v1 framesPerSecond; production files remain clip-metadata-001. The proposed v2 strict decoder, exporter round-trip, catalog owner migration and direction-specific reaction lifetime changes remain pending. Variable holds are not reachable from current production metadata. No duplicated source frames have been added.

The spec pin changes in all four identity sources. All 21 bundled contracts/fixtures match the exact local spec Git commit, with only the documented D-065 catalog pin exception. Ruleset/content/arena and all non-pin JSON remain unchanged. Remote-fetch CI parity is not claimed.

New tests cover 16-frame half-second and 3/7-second vectors, variable holds, directional selection, malformed values, sum/product overflow, and every existing clip/facing's equality to the independent legacy cadence. A direct SpriteKit action test verifies the elite 3/7-second and variable 1/4-second action durations and rejects mismatched texture/hold counts. These action-duration checks do not prove pose fidelity or every texture's visible residence under device load.

Validation (2026-10-14): full core suite passed, 764 tests / 108 suites in 475.309 seconds (workspace clip-timing-core.log). Xcode iPhone 17 Pro iOS 26.5 simulator passed 82 Swift Testing tests / 13 suites in 35.403 seconds plus three XCTest checks (two benchmark captures and the timing action construction check). Remote `scripts/spec_parity.sh` passed at c07ea6d. `git diff --check` passed.

The new test initially assumed Double precision for SKAction duration and failed. Defect [#120](https://github.com/Zero-State-LLC/SS-runtime/issues/120) records the observed exact Float representation. The corrected assertion requires Double(Float(3/7)) exactly; no widened tolerance or changed core rational expectation. Variable-quarter-second duration remains an exact 0.25 assertion.
