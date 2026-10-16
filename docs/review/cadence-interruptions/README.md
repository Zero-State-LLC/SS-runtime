# Candidate interruption guard

Fixed a test-only cadence experiment defect: base movement could remain selected in the snapshot while the renderer presented an event reaction. The candidate now overrides only the renderer-selected `player_move|s` clip. Other selected clips reset the experimental movement segment and retain their texture/actions. Production rendering and simulation are unchanged.

Fresh Xcode result Test-SSRuntime-2026.10.15_18-13-54--0700: 113 named tests / 115 executions passed, zero failures or skips. `testDistanceCandidatePreservesSelectedInterruptions()` passed and checks idle, dodge, defeat, completion, north-facing movement and a west-facing hurt event layered over south movement, in normal and Reduced Motion. It also checks resumed south movement becomes eligible.

Scope: actual renderer selection/texture/action preservation using explicit presentation fixtures. This is not a live physical collision-stop, wall-slide, reversal, pause or dodge-command sequence. Those scenarios, visual acceptance and performance profiling remain open. Earlier south-only recordings are still useful art evidence but do not validate the new interruption guard.

Timing findings and raw derivation are in timing-findings.md / timing-analysis.json. Nine-tick catch-up batches appear in the earlier recorded run; the initiating delay is unproven. No simulation ticks were removed and no acceptance assertion weakened.
