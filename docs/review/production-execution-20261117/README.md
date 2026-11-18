# Production execution, November 17, 2026

Authority: owner execution directive at01:55:50Z, broader presentation correction approval at03:40:46Z, and docs/board/all-PR maintenance request at04:04UTC. No merge, release, deployment, paid asset generation or new gameplay contract authorized. This packet records implementation and qualification, not release acceptance.

Latest reconciliation: `../../handoff/PR-RECONCILIATION-20261117.md` inventories all nine open runtime/specs/legacy PRs. Project27 now tracks259/260/261 as well as prior cards. Implemented-but-unmerged repairs remain In Progress, not Done. Specs63's two documentation review findings are repaired atc226085; all acceptance and merge gates remain.

## Live reconnaissance

- OBSERVED runtime working head at intake: `979a928a376c0f5e0e1e89c1c8a798d67afad6d8`, PR236, branch `qa/bp001-projection-decision-20261116`. Remote runtime main `df8473713a3d37aeca05d4e1110f979f197b9ceb`.
- OBSERVED accepted specification main: `983a4ca3427bd8a9d30056bccf356fe0f715312e`. Runtime pin: `b1ed874e1e8eb0e61b2174b9093201e9a61e1a4b`, rules014/content009/arena004. Newer main contains specification clarifications and audit work. Do not infer contract adoption from branch publication.
- OBSERVED open specsPR115 at354c1f4 and runtimePR235 atdcf073c are the separate receipt stream. SpecsPR92 and runtimePR167 concern the Vendor mine. Do not overwrite their work. PR236 has no review threads at intake.
- OBSERVED GitHub Project27 contains benchmark work, open237/238 and device/family gates. Board historical status is not art acceptance. One Mind `agent-context` was pulled ff-only; its SS handoff is dated October30 and is stale relative to live repositories. Its existing unrelated local change was untouched.
- OBSERVED CI43988671605 at6c3be49: deterministic core, Debug, Release and device-sitting jobs passed. Spec-parity failed inside the review suite before the actual byte-parity step. Therefore neither a Debug failure nor a contract mismatch is established by that run. Older intermittent playback237 remains unresolved.
- OBSERVED Xcode26.5 / Swift6.3.2 available. Booted iPhone17Pro simulator. A paired physical iPhone17Pro is visible; no physical run performed. This is not the iPhone12 floor, and D-020 equivalence remains pending.

## Execution backlog

| Priority | Repo / item | Required implementation and acceptance | Verification / evidence | Dependency / status |
|---|---|---|---|---|
| P1 | runtime256 | Canonical isolated temp root for frozen tests; retain real symlink rejection and child failures | `scripts/test_review_test_runner.py`, actual46-test scene suite and retained capture verifier | Implemented, locally verified |
| P1 | runtime257, T902/T908 | Include all120 accepted gates, missing gates block expansion | Swift negative cases for A-013A/D-022/D-023/D-024/E-021; exact census | Implemented;25tests pass after4red tests/18assertions |
| P1 | runtime/spec parity258 | Verify exact pinned bundled contract bytes using isolated checkout | `scripts/spec_parity.sh`,2lifecycle regressions | Actual pinned parity passes; latest-main adoption remains separate |
| P1 | Canonical hash CPU cost | Preserve all digest bytes while removing measured portable-hash/formatting overhead on Apple platforms |23focused hash/determinism/replay tests pass; host Release isolated hash-to-hex14.38x–37.61x faster in five-round measurement, not an FPS claim | Implemented; bounded host partitions and native traversal passed, final Release built. Physical/FPS acceptance remains missing; see HASH-PERFORMANCE.md |
| P1 | runtime260 | Stable presentation socket identity independent of Dictionary traversal |4red/green regressions,21independent affected tests, unchanged8native review tests | Fixed and pushed fed8a3d; no simulation/spawn-selection change, issue remains open pending merge |
| P1 | runtime237 | Explain and fix intermittent15/16 live-pose observation without weakening assertion or changing authored timing | Preserved trace diagnosis, focused native reproduction | Actual focused rerun1test passed with all16poses in retained trace; intermittent historical defect remains unresolved. See UI-PLAYBACK-ADDENDUM.md |
| P1 | runtime133 / T1045 | Correct only Camera-adjacent kiosk geometry/spacing; keep neighbors as reference | Actual runtime three-zoom comparison, authoritatively fixed footprints/actors | Z-only flat native comparison verified:6captures/18images. Broader Debug-only live midpoint correction approved03:40UTC. Native0407 passes18/18 including8unchanged kiosk tests after documented probe-owner repair261. Actual current/candidate app inspected04:09-04:10UTC: MIDPOINT/NOT ACCEPTED visible, foundation/contact/scale deficiencies remain. Benchmark NOT MET, no owner art acceptance |
| P1 | runtime134 / specs65 | Complete coherent reviewed asset families before admission | Existing canonical catalog, source/provenance and native playback evidence | Partial/rejected family evidence, not production-ready |
| P1 | T901/T905/T406 | Device replay and three consecutive complete iPhone12 runs; measured ceilings | Actual device captures and performance telemetry | iPhone12 and D-020/D-021 decisions missing |
| P1 | T903/T904 | Onboarding and voluntary replay with at least5 external participants | Named participant records, comprehension/replay outcomes | External participants required |
| P2 | audio / T606 | Playback and listening QA, rights verification | Existing audio manifests and device listening record | No listening evidence from this session |
| P2 | accessibility / F | VoiceOver, Dynamic Type, handedness and44pt controls in actual UI | Existing app suites plus SE-sized native captures | Debug input/terminal checks and Release input checks pass; actual VoiceOver/SE capture coverage remains separate |
| P2 | store / release | Privacy/metadata and TestFlight preparation evidence | Existing privacy tests and release documentation | No release authorization |
| P3 | expansion | No additional level/platform/content systems | Existing expansion evaluator | NOT_COMPUTABLE |

## Release evidence matrix

This is a status index into existing acceptance.md and runtime collectors, not a new gate system. Test names or manifests alone never establish a pass.

| Gate | Current evidence / exact checks | Result and missing evidence |
|---|---|---|
| A Functional | `GateVerificationTests`, Camera/Extraction/Objective suites, native input/terminal suites | Historical CI success plus fresh850core/9placement/1fairness partitions and27Debug/25Release tests; see QUALIFICATION.md. Complete player journey not yet qualified here |
| B Determinism | CI core, Camera fairness/placement, replay matrix; pinned parity | Host/simulator evidence only; supported physical matrix remains missing |
| C Stability/performance | Existing FrameTimeCollector, PeakDensityProfiler, device-sitting harness | NOT_COMPUTABLE for iPhone12 percentiles/thermal and measured D-021 ceilings |
| D Visual assets | Canonical `Sources/SurveillanceCore/Resources/contracts/asset-catalog-001.json`, RuntimeAssets/provenance, benchmark packets | Benchmark NOT MET. No new art admission. Kiosk-only correction applies. Generated proxies are not native captures |
| E Arena/fairness | CameraFairnessTests, CameraPlacementTests, ArenaReachabilityTests, traversal captures | Preserve8of18 deterministic stationary Cameras and optional Network Blackout; visible contact/footprint acceptance incomplete |
| F Accessibility | TerminalAccessibilityTests, TouchControllerTests, DevicePresentationRegressionTests | Automated coverage does not replace actual VoiceOver/handedness/comprehension evidence |
| G Playtest | Existing PlaytestEvidence collector; T903/T904 | NOT_RUN per accepted task table; at least5 external participants required |

D-013 decision is ACCEPTED: immutable legacy freeze at3b20d88. This is distinct from visual acceptance gate D-013 (Civic Seam recognition). D-020 and D-021 decisions remain DECISION_PENDING, distinct from similarly numbered visual gates. T903/T904/T905 are NOT_RUN in live accepted tasks. Expansion remains NOT_COMPUTABLE, not passed by the existence of evidence collectors.

## Implemented slices:257 and258

Pinned acceptance.md has120gates. The old registry omitted A-013A,D-022,D-023,D-024,E-021 and the expansion evaluator inherited that omission. Four new tests produced18failed assertions before correction, including false PASS for every missing/failed omitted gate. Corrected registry and old count test now match the accepted census. All25tests across6release-evidence/gate suites pass, including ten complete-run simulations. Newly enumerated gates remain unmapped/pending, not automatically passed. No authoritative simulation identity changed.

Parity258 now uses an invocation-owned mktemp checkout and EXIT cleanup rather than deleting `/tmp/spec-parity-check`. Two subprocess regression checks prove distinct roots for overlapping fetch failures, exit23 preservation, cleanup, paths with spaces and untouched neighboring files. These mocked lifecycle tests are not byte-parity evidence. Separately, the actual script fetched pinnedb1ed874 and reported every bundled contract/fixture byte-matches. The bidirectional comparison and single catalog-pin exception remain unchanged.

## Implemented slice:256

Cause: `test_pending_no_outputs` passes an unresolved temporary path to a deliberately strict assembly-path guard. Under a symlinked temp base, the guard correctly rejects the alias before the test reaches the missing-file assertion. A canonical local temp path hid the problem.

An explicit symlinked scratch base reproduced the exact CI exception. New runner creates a per-process canonical temporary directory and forwards Python arguments and child exit status. It does not resolve user-supplied assembly paths or alter evidence validators. This preserves frozen test/source bytes and their audit hashes. Five regressions pass, including the original failure before wrapping and success after wrapping, genuine assembly-symlink rejection, canonical isolation, exit7 propagation and CI wiring. The full affected suite passes46tests. Retained V9 checker passes6captures/18images/9baseline comparisons;1766protected files remain unchanged. No fresh native or physical evidence claimed.
