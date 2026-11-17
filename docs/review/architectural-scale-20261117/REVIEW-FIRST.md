# Initial source-view technical inspection

November17,2026 01:25UTC. Coordinator inspected the actual `source/output/comparison-z140.png` from the first renderer run, plus the full original benchmark and retained actual V9z140half image.

The architectural proposal was visible, but the reconstructed ground was technically wrong: black road-like aprons appeared around buildings and a small-paver patch appeared where the native V9 showed shared sidewalk slabs. Inspection of `source/build.py:234-244` found the source texture mapped to `groundPlanWitness.size`. The retained producer `AppTests/BlockedBaseCurbSceneTests.swift:308-313` uses a2304x2304square source/tile domain clipped to the2304x1536arena, not a full-texture stretch to the arena's height.

The raw current/proposed view files also included a30-pixel title strip, so their aspect was not the retained704:326frame. Labels belong outside those six scene images, in the sheet/gallery.

Worker was instructed to preserve the complete first output and renderer, correct only these technical presentation defects, add an independent ground-UV regression, and keep the exact same single geometry proposal. This is not an aesthetic retry. Runtime controls/shadow rendering absent from the source proxy must be disclosed, not described as visually reproduced. No native execution or production change was requested.

Do not use the initial ground-mismapped output as the final comparison. The retained first-attempt directory and final validation report identify the concrete artifacts after the technical correction.
