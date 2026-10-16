# Registered service-building revision

2026-10-15. Original generated source preserved; register_source.py reauthors it using recorded continuous left/right transforms, shared vertical scale, and alpha threshold 16. Source/deformation hashes and mapping are in registration-v3.json.

Focused App test BenchmarkCaptureTests/testCaptureCameraFieldsInReplayableEncounter passed (1 test, 0 failures), Xcode 22-28-11. It checks actual SpriteKit mapping of three base points to unchanged authoritative solid corners and unchanged simulation/replay digest, at 1×/1.25× in both motion settings. Numeric 0.002-unit tolerance is transform/rounded-landmark precision, not an art-quality threshold.

Visual inspection: service-yard-B base now covers its projected footprint. Existing neighboring buildings remain misregistered. Source height cuts the roof off at this edge-encounter view; complete roof review, depth/occlusion, boundary framing and moving contact remain open. This is test-only substitution, not production asset admission. Neutral outlined Player and legacy enemy art remain diagnostic limitations.

Specs validator and Swift syntax check passed. No new full-suite or device-performance claim. CLI test attempt failed on simulator/cache permissions before execution; successful evidence is the GUI-triggered focused test.
