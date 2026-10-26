# Shared distance-phase comparison

BP-008 isolated comparison, not production admission. One south/front source is aliased to the projected diagonal; initial east idle remains unsupported. Direct-stop held neutral is unchanged; this run does not adopt proposed0.375s settling.

Twelve variants: three target input magnitudes × fixed-time/distance phase × Standard/Reduced Motion. Full uses raw diagonal components32767 for75 movement ticks; half11585/150; quarter5792/300, then15 held-idle ticks. Actual travel299.96795483148 world units in each route (floating accumulation differences below1e-9). Every pair has identical command stream and independently verified simulation trace/digest.

Initial test passed:1 test,12 variants,0 failures,62.017s. All16 observed movement poses in every variant; backed supported idle restored; projected geometry and registration assertions retained; zero outline readbacks. Art/production metadata and gameplay unchanged. Labeled native recording run passed: 1 test, 12 variants, 0 failures, 63.974s; all 16 movement poses observed in each renderer trace. Original traversal/preparation-clock regression also passed: 1 test, 6 variants, 0 failures, 21.109s.

Evidence: initial-run-inputs.json, result.json, coverage.json, attachments/. Recording coverage is verified in recording-coverage.json; default regression result is default-regression-result.json. Video boundary inspection found capture gaps and mismatches between wall-time offsets and visible variant captions. Do not publish the planned six trimmed comparisons from those offsets. Re-establish boundaries from visible captions and verify capture continuity, or recapture individual variants before separate normal/quarter-speed review. Missing observations may not be filled by retiming or treated as source evidence. Sole-pixel contact review, collision/wall-slide/reversal shared comparison, remaining facings and production/device gates remain open.

## Presentation-timestamp export correction

The initial decoder-estimated boundary analysis was invalid: 2,480 frame timestamps diverged by up to6.88s. Source frame PTS matches sorted packet PTS. Decode using documented `-fflags +igndts` restores correspondence to visible captions without synthesizing frames. See timestamp-investigation.md and timestamp-diagnosis.json.

Six Standard Motion pairs exported at normal and quarter speed. Per-pair frame counts84/77/76/148/263/198 match source packets in the explicit trim windows. Normal relative source timing error ≤1µs; quarter versus source×4 ≤3µs (rounded timestamps); quarter versus normal×4 ≤1µs. Verification artifacts are copied here. Source packet timing and captured pixels are preserved; no claim of recovered frames.

Review: outputs/SS-shared-distance-review/normal-speed.html and quarter-speed.html (workspace outputs, outside repo). Active capture gaps up to135ms remain; quarter-input distance candidate ends before complete held-idle review. This recording supports comparison only, not final cadence/contact acceptance. Further clean native capture and sole/ground contact inspection remain required. No timing/policy or production-family adoption.

Final endpoint images inspected: each of six clips starts and ends in the intended game scene with the player visible. Unsupported initial placeholder and trailing menu were trimmed, without changing the retained timing. One overwrite attempt timed out; re-export to temporary files succeeded and final source-PTS checks passed. Earlier verification was superseded by the final copied JSON.

## Complete playback regression after shared harness changes

2026-10-19:22 tests passed, zero failures, zero skips; result bundle elapsed433.235s. iPhone17 Pro simulator, iOS26.5 build23F77. Archived bundle: `work/shared-distance-full-suite.xcresult`; summary and test tree: full-suite-result.json and full-suite-tests.json. Input inventory full-suite-inputs.json was rechecked after completion: all recorded App/AppTests source and fixture hashes unchanged.

The Mac locked during the latter tests. Saved session logs showed continued progress; the finalized xcresult confirms completion. This is an automated regression pass, not an unlocked visual review or device performance result. No assertions or fixtures were edited during the run. Native visual checks still require unlock.

Capture/callback timing investigation: capture-versus-callbacks.md and recording-callback-cadence.json distinguish recorder gaps from renderer callbacks without claiming physical presentation or selecting a new acceptance budget.
