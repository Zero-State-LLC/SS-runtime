# Bounded player: native renderer recording

2026-10-19 recording run: one focused traversal test passed, zero failures. See test-summary.json and six trace records. The current candidate has not received a new full 15-test suite run; the earlier complete suite belongs to the preceding knee-material candidate. Targeted Clip tests passed 66 in the preceding integration step.

Native Simulator recording exported from 67.28 seconds for 1.70 seconds, rotated counterclockwise and cropped to the actual 2112×978 SKView. This selects the 1.25× tracking, standard-motion traversal and held neutral. 89 captured frames are retained. Quarter speed uses the same frames with timestamps multiplied by four, without interpolation. Detail exports crop 450×700 at (780,120). Source is outputs/SS-bounded-idle-renderer-review/bounded-idle-live.mov in the workspace.

Review files: outputs/SS-bounded-idle-renderer-review/{normal,quarter,normal-detail,quarter-detail}.mp4. Static contact sheet and last-frame inspection confirm scene content and held neutral at the end. They do not establish cadence or seam acceptance. The black left shape is the Simulator hardware cutout. Initial unsupported world-e, a held rather than animated idle, source-facing alias, and direct stop transition remain explicit limitations. Final still shows apparent boot/ground separation requiring contact review; do not admit to production or device testing on these checks alone.

Next: review normal cadence separately from quarter-speed contacts and stop; resolve apparent ground contact before widening to further facings/actions. Enemy production remains deferred until the player is accepted.
