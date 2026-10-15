# Full GameScene playback evidence — BP-008

The simulator rerun passed 100 test executions with zero failures. Both displayed-playback tests passed. The existing EnvironmentLibrary.swift:108 nonthrowing `try` warning remains.

The DEBUG-only observer records actual SpriteKit texture identity after actions, authoritative Q8 position, rendered position, camera position and viewport. The full GameScene uses ordinary touch steering and normal scene callbacks. Four renderer images are linked to their observations. These show the existing admitted art, not the revised benchmark candidate. The visible white player outline remains unresolved.

Full-scene capture: 90 observations, ticks 1–90, four images. See summary.json for measured display duration and distinct texture count. Synchronous image extraction adds substantial overhead; this is not a performance measurement or physical-device validation. Timing divergence needs a separate nonintrusive comparison before drawing conclusions.

The initial run failed the isolated recorder's >10-observation assertion: 90 simulation ticks finished with only nine display callbacks. Defect https://github.com/Zero-State-LLC/SS-runtime/issues/126 was filed before repair. The recorder now continues normal simulation until both at least 90 ticks and 11 observations exist; the assertion and timeout are unchanged. The rerun recorded 11 observations through tick 99. Initial failure evidence is retained in the user-facing outputs/SS-full-scene-playback/initial directory.

The last core-only run passed 773 tests across 109 suites; core sources have not changed since that run. This rerun validates the app/test-only changes. No production asset, gameplay, spec pin, or physical-device build was changed. Revised character/camera art, full motion/contact matrix, benchmark composition and contrast acceptance remain open.
