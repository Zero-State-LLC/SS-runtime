# Additional UI and playback evidence, November17

These results were executed earlier in this production-ownership session and their xcresult summaries were fetched again at02:58/03:03UTC before publication. They are not post-hash-optimization runs.

## SE-sized upgrade interaction

`upgrade-ui-summary.json`:3passed,0failed,0skipped on iPhoneSE3 simulator, iOS26.5. Original local result: `$JCODE_SCRATCH_DIR/ss-production-upgrade-20261117-0223.xcresult`.

`upgrade-accessibility5-record.json` records the actual isolated production upgrade view at667x375landscape points and accessibility5Dynamic Type. Ghost Step was initially not hittable, became reachable after two swipes, and selection returned `selected=2;count=1`. Its accessibility label includes the mobility/surveillance description and explicit absence of damage immunity. Capture used XCUIScreen, not the previously problematic cropped app screenshot path.

This is actual UI interaction with the production view in an isolated host, not a complete game journey. The record explicitly says `gameResumeVerified:false`, `voiceOverSession:false` and `physicalDevice:false`. No VoiceOver listening, real-device accessibility or post-selection game resumption claim follows.

## Playback237 diagnostic rerun

`playback237-summary.json`:1passed,0failed,0skipped on iPhone17Pro simulator, iOS26.5. Original local result: `$JCODE_SCRATCH_DIR/ss-production-playback237-20261117-0226.xcresult`.

`playback237-traces.log` retains timing-gap diagnostics and an observed pose list0...15with no missing poses for the displayed trace. Individual timing gaps remain visible. A successful local rerun does not erase the historical intermittent15/16failure or establish its root cause. Issue237 remains unresolved. This result predates the canonical-hash optimization, so it is not evidence that optimization fixed playback.

## Full application captures

`full-app/title-raw.png`, `boss-seeded-raw.png` and `extraction-seeded-victory-raw.png` retain actual full-application simulator images from earlier in this session. Their names disclose seeded scenarios. Seeded boss/extraction states are diagnostic shortcuts, not a complete legal run, first-time onboarding, voluntary replay or proof of encounter fairness. They do not establish acceptance of the benchmark, coherent asset families, audio rights/listening, physical-device ceilings or release readiness.

All owner art, physical-device, external playtest, merge, release and deployment gates remain in force.
