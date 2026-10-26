# Fixed-reservation moving-camera review

Focused test `testMovingCameraFixedReservationReview` passed, 1 test / 0 failures. Result: Test-SSRuntime-2026.10.16_11-26-25--0700.xcresult, iPhone 17 Pro iOS 26.5 Simulator.

Seed 1 normal autopilot commands; presentation warm-up ticks 4061–4180, then 60 captures at ticks 4181–4299, every two simulation ticks. Each capture asserts unchanged authoritative digest, SpriteKit player canvas containment in the fixed reservation, and no current HUD overlap. All 60 pass. 1x, right-handed, standard HUD, all captions. Fixed bounds derive offline from the prior 50-state pilot; not production future-state knowledge.

Normal video: 30 capture frames/sec, two seconds. Quarter video: 7.5 capture frames/sec, eight seconds. Videos deliberately reset at loop boundary. These are tick-sampled SpriteKit renders with paused SKActions and neutral facing player poses, not continuous display-cadence evidence, locomotion approval or device performance.

The first run lacked pre-roll and showed up to 55.30 points of focus displacement per two ticks; it was rejected as a cold-camera comparison. The warmed run peaks at 12.65 points per two ticks. This is a measured delta, not a researched acceptance threshold or proof that remaining motion is correct.

Visual findings remain open: player overlaps the camera post/housing; black boundary areas are exposed; legacy enemies/buildings differ in scale/style; diagnostic outlines remain. Current HUD containment does not establish threat readability beneath controls. Next: continuous playback with Q8 positions, reversals and dodges, correlate focus deltas with commands, review normal/Reduced Motion and all HUD layouts, resolve depth and boundary dressing before device acceptance.
