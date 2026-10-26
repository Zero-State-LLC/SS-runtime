# Knee material boundary correction — source candidate

The preceding projected-knee trial sampled the original near-black pad border and adjacent cloth onto the curved face. Pixel tracing records source locations, including right-pad (166,264)=(21,15,9) and (166,269)=(17,18,17). The new manually authored source region maps the face to y249–263, centered on each anatomical knee. This is a material ownership correction, not a lighting brightening filter.

All 16 source alpha masks are identical to the preceding 2.8-radius trial. Pose samples, gait, torso, arm controls, boots and registration are unchanged. The 2.8 cap radius itself remains proposed. Normal/quarter videos use freshly composited frames at 32/8 fps, duration 0.5/2 seconds; they are source previews, not renderer footage.

The inspected four-pose comparison removes the broad black band and makes the face read as a closed pad. Full-speed cadence, seam, idle correspondence, anatomy/proportion, boot fidelity and production admission remain open. No runtime textures replaced. Prior copied reports are historical and are not evidence for this change. Relevant evidence: boundary-change.json, verification.json, boundary-comparison.png and the freshly exported MP4s.

Renderer reconciliation 2026-10-19: candidate installed only in AppTests assets with prior fixture preserved. DisplayedPlaybackTests passed: 15 tests, zero failures, 203.221 seconds. All 27 exported coverage metrics report 16 frames and coveragePassed=true. Six shared traversals retain tick 0–90 and missing-idle records. All 16 built textures match alpha and opaque RGB after reversing Xcode PNG optimization. No new recording or visual/contact acceptance is claimed.
