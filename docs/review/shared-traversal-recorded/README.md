# Recorded shared traversal review

Open normal-speed.html and quarter-speed.html separately. Each provides standard and Reduced Motion at 704×326 logical size plus a detail crop. These are real simulator pixels from the shared-renderer run, with no interpolated frames. The screen overlay at left belongs to the simulator/system.

Shared traversal passed in both modes: all 16 source textures and two wraps observed. Full recorded suite failed one test (115 named passed, one failed): the full-input, standard-motion distance-phase candidate observed only 15 frames. The earlier unrecorded suite passed 118 executions. Keep the recorded failure open; shared traversal success does not override it.

Exports retain 125 captured frames for standard mode and 136 for Reduced Motion in both speeds. Quarter-speed presentation timestamps equal four times normal offsets within 1 microsecond of ffprobe rounding. Final packet hold may differ; excerpt endpoints are not authored seams. Cuts were checked against actual visible player/scene transitions because MOV creation_time has only second precision. Initial incorrect title-screen cuts were replaced before delivery.

Scene is a filtered art composition using a real preflighted route and unchanged simulation rules. The existing front source is explicitly aliased for this SW-to-screen-down pilot; other facing/action art is not completed. Entry and exit idle use unsupported-source fallback and are excluded from movement clips; that gap remains open. No legal encounter, full-facing, occlusion or physical-device acceptance is claimed.

Static export checks confirm the hooded player remains visible at both endpoints without the added bright outline. Moving contact/seam/coat/arm quality still requires separate normal- and quarter-speed review. Unrecorded observation intervals reached p95 21–26 ms, so coverage is not steady-60-fps proof. Ground repetition, street composition and scale remain below the target reference.

Next: review these clips, investigate the recording-load frame miss without weakening coverage, complete shared-scene stop/start/action/facing presentation, and then continue the benchmark art/environment and device gates.
