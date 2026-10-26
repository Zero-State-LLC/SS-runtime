# Player material candidate: recorded renderer review

OBSERVED: Native Simulator recording of the current material-detail test fixture, captured 2026-10-16. The focused `DisplayedPlaybackTests/testSharedProjectedPlayerTraversal` run passed: one test, zero failures, 19.490 seconds. Its six exported traversal records are retained in recorded-results. This is separate from the preceding 15-test suite recorded in ../player-material-detail/README.md.

## Separate playback speeds

- [Normal speed](normal.mp4), [normal detail](normal-detail.mp4).
- [Quarter speed](quarter.mp4), [quarter detail](quarter-detail.mp4).

Both versions contain the same 57 captured frames. Quarter speed changes timestamps only, with no interpolated frames. Retiming error is at most 0.000009 seconds. See retiming.json. Source recording is outputs/SS-player-material-detail/material-player-live.mov in the working evidence directory. It was rotated counterclockwise and cropped to the actual 2112×978 renderer view. The detail crop is 400×650 at (880,250).

The retained interval is 55.5–56.4 seconds of the recording. It is a short steady-movement excerpt, not a full-cycle/contact/seam acceptance package. Start/middle/end images were inspected; continuous normal-speed perceptual acceptance is not claimed.

## Entry/exit gap remains open

OBSERVED: A white fallback appears before movement. check.png preserves the earlier cut that exposed it; check-final.png shows the chosen steady-movement cut. Trimming does not fix the defect or supply idle coverage.

The isolated review library in AppTests/DisplayedPlaybackTests.swift:testSharedProjectedPlayerTraversal contains player_move and six camera clips, but no player_idle. SharedTraversalScene starts with the simulation's idle snapshot, then moves for 75 ticks and stops through tick 90. SpriteLibrary intentionally returns no texture for unsupported clips; its admission contract forbids substituting another clip or direction. Consequently a passing movement-coverage test does not establish a complete player transition.

Next: author/register the missing neutral and transition coverage for the exact projected facing; preserve narrower stance, opposing arm swing, material detail and low knee recovery. Verify entry, all movement frames, exit, repeated 16→1 boundaries and Reduced Motion in the real renderer. Keep missing facings/actions and visual acceptance open. Do not mask the gap with a movement-frame-as-idle substitution or change production fallback policy to make the review look complete.

Player completion precedes the enemy production pipeline. The enemy pipeline remains deferred under SS-specs issue 65, with equivalent design detail and urban street-theater character requirements.

No production art, gameplay, source timing or test assertions were changed to produce this evidence. No device acceptance is claimed.
