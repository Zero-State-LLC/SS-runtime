# Upright environment diagnostic — 2026-10-15

Focused BenchmarkCaptureTests/testCaptureCameraFieldsInReplayableEncounter passed (1 test, 0 failures), Xcode result 21-57-18. Specs validation passed; runtime diff whitespace check passed.

Building and physical-prop sprites are lifted out of the ground squash in the proposed projection capture. Existing sizes, anchors and depth are preserved to isolate the transformation. Source ground-plane art remains projected.

Visual inspection: buildings now stand upright, but visible bases disagree with ground footprints; registration, depth/occlusion, arena-edge framing and legacy enemy source art remain unresolved. No shipping projection or art admission is established. Production outlines remain in this diagnostic. A paused encounter does not establish moving threat lead time or device performance.

## Registration measurement

The service-yard-B canvas is centered on the AABB and sized to its width/height. Hand-observed slab corners suggest this cannot be corrected by translation alone: a front-corner anchored uniform-scale fit has endpoint errors of approximately 47 and 72 logical units. These are provisional observations, not accepted ground anchors; the hidden rear and potentially clipped right side remain unverified. The slab perimeter also needs distinction from the wall footprint. See service-building-registration.json and service-building-landmarks.png.

Next implementation must use an explicitly authored footprint-compatible base, not stretch the existing image or change collision. The new spec records these admission rules. The diagnostic script verifies its fit algebra against an exact synthetic case and never modifies source art or simulation.
