# Recorded shadow placement comparison

Two tests passed during native Simulator recording: zero failures, 38.104 seconds. Records and summary accompany this note. Isolated control and candidate preserve the source, root, motion, camera configuration and shadow appearance parameters; candidate changes shadow placement only.

Workspace deliverables: outputs/SS-shadow-placement-review/{grounded,control}-{normal,quarter}.mp4. Both are 1.25× tracked scenes with walking and the terminal held neutral. Clips are independent runs, not phase-aligned comparisons. Contact sheets confirm scene content. Static inspections do not establish subjective normal-speed gait acceptance.

Recording seek-index discrepancy: input-side fast seeking produced title-screen pixels inconsistent with sequential decoding at the same timestamps. Final exports therefore decode from the beginning and trim by decoded timestamps (grounded 46.8–48.25s; control 61.75–63.35s), rotate counterclockwise, crop the 2112×978 SKView and reset PTS. Quarter versions preserve every exported frame and multiply timestamps by four; no interpolation. Source movie and probe files retained in workspace. Movie timestamps must not be equated to test wall-clock timestamps or exact pose IDs.

Production default remains control. Grounded candidate and moving contact still require visual assessment before admission; no device testing yet.
