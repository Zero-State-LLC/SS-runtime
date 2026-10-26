# Aaron continuation — 2026-10-25

Continue from this checkpoint in **Zero-State-LLC/SS-runtime** and **Zero-State-LLC/SS-specs**, not the archived Surveillance-Survivor repos. Project: https://github.com/orgs/Zero-State-LLC/projects/27.

## Keep

Hooded urban street-theater Player, narrower stance, arm swing, detailed knees and boots; accepted 0.375-second settle timing. Owner said the shown deterministic release5/13 transition looked right visually. This is bounded visual acceptance, not acceptance of other facings/actions or device performance. Candidate art remains test-only; production metadata and spec pin have not migrated.

## What is implemented

Player source/neutral and two source-backed settle sequences; review-only fractional presentation clock with rewind/cancellation/Reduced Motion handling; full-window aspect-fit review host; Camera-post ordering/opacity and exterior-ground coverage experiments. Source, tests, research and failed experiments are preserved. `docs/review/aaron-package/` contains the editable bounded source directories and separate normal/quarter-speed review pages/videos. Open the HTML locally; there is no dependency on the former localhost server. Archived reports can reference original workspace outputs/ paths; do not interpret those as portable files.

## Validation at handoff

Historical 2026-10-19 evidence: core 779 tests/110 suites; 442 source-backed interruption cases; four deterministic exports with167 frames each; Standard release5/13 observes17/17 settle poses; Reduced Motion observes none. Gated live test passed91.942s including operator waits. Latest handoff checks and PR CI are recorded separately, not substituted for visual or physical-device acceptance.

The obsolete manual recording wrapper/buttons were removed from automatic XCTest discovery for handoff: they waited up to600s for a human and would hang CI. `testMidpointFractionalClockLiveReview`, lifecycle/source coverage and deterministic export tests remain unchanged. Do not resume OBS setup or recorder debugging by default: the owner found it disproportionate. No recording is required to continue source/coverage work. Live smoothness is still unverified; resolve it on device before release/admission. Earlier recorder-dependent next-step notes are historical, not the current priority.

## Next work, in order

1. Finish the Player: remaining release phases, four genuinely distinct elevated facings, then movement/action/reaction coverage from the same editable source. Do not relabel the front-source diagonal pilot as directional art. Preserve current approved visual qualities; dimensions, amplitude and hidden surfaces remain proposed.
2. Integrate and review the shared scene: hooded Player, one municipal Camera family with its own complete-device sheets, building, props, ground and authoritative field/collision geometry. Review quiet and dense encounters, overlap/edges, camera3→2→1→0 persistent states, and Reduced Motion.
3. Check normal-speed feel and performance on iPhone; capture only the evidence needed to diagnose visible failures. Complete D-020/D-021 device/performance decisions, remaining combat/upgrade feedback and full QA. No green unit test proves smoothness or benchmark art quality.
4. Admit complete reviewed families with coordinated metadata, catalog/provenance, resources and spec-pin reconciliation. Enemy production remains deferred until the Player is a usable template; retain all existing cast and weapon/upgrade obligations.

## Capture evidence caveat

The Simulator movie has zero backwards encoded PTS but seven duplicate PTS values. FFmpeg best-effort estimates switch to DTS after a duplicate; the apparent reversal is not proof of a game hitch. Neither this movie nor deterministic exports establish live cadence. See `docs/review/player-settle-timing/live-clock-diagnosis.md`. Preserve failures; no further recorder project is a prerequisite for Aaron's source work.

## Reproduce

Runtime: `swift test` (on this sandbox host, `swift test --disable-sandbox` was needed); `xcodegen generate`, then SSRuntime scheme / SSRuntimeTests on an iPhone simulator. CI runs Debug and Release app tests with SS_RENDERER_TEST_SUPPORT. Specs: `python3 scripts/validate_specs.py`. Start with SPEC_BASELINE.md and the specs benchmark-production.md current checkpoint. Review artifacts are evidence, not shipping resources.
