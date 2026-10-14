# Device QA baseline — 2026-10-13

Runtime main 6e42cb47e8be10cffcc8398cbf9e2fff5fbe7dac, Release, debugger disabled.
Physical target confirmed by Instruments: iPhone 17 Pro, iOS 26.3.1 (23D8133).
User: immediate heavy stutter, animation defects, object clipping, surveillance cameras glitching, whole view jumps. Opening recorded, user played until death.

Time Profiler recorded ~53 seconds, SSRuntime process only. Saved SS-baseline-device.trace under work/.
- Total sampled CPU weight: 24.24 s.
- Main thread: 21.53 s (88.8% of sampled CPU weight).
- SpriteKit renderer on heaviest stack: 15.63 s; flushRenderOps: 10.58 s.
- Filter GameScene.update: 4.63 s, redraw 3.09 s; SKNode name-search enumeration 1.94 s.
- Filter OutlineTextures: 23 ms total, outline method 20 ms; not the dominant baseline cost.
These are sampled CPU weights, not wall-frame times or p95 FPS measurements. No frame-time acceptance claimed from this trace.

Source defects: camera smoothing/dead-zone missing; camera display used mount position, not fieldOrigin; camera cones had no solid occlusion; active clip token survived node removal; frame collector detected streaks after sorting the sample timeline.
