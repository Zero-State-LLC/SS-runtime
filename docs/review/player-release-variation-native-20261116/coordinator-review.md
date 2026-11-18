# Coordinator verification

Verified November 16, 2026 at 03:38–03:40 UTC.

- Read the new texture provenance, paired capture and interruption/Reduced Motion assertions in `AppTests/ReleaseVariationSourceTests.swift:16-163` and fail-closed import/verification at `scripts/import_release_variation_native.py:33-142`.
- Independently fetched the actual xcresult summary from `ss-releasevariation-native-20261116-0313.xcresult`: Passed, 3 total/passed tests, 0 failed/skipped/expected failures, iPhone17 Pro simulator, iOS26.5, arm64.
- Independently ran resource preparation in verify-only mode and the native packet verifier: 476 poses, 442 source/configuration files, 28 exact paired endpoints, 182 changed native intermediate poses. Live cadence remains false.
- Independently reran all29 parser/actual-capture regressions: passed in43.608s, no skips. Full verification task exited0 in63.6s.
- Actual Brave gallery checked all14 phase options at poses0/8/12/16 using the page's change/input handlers:56 paired selections, both576x432 images decoded at each selection, synchronized labels, no horizontal overflow at the current viewport. Left open at phase07/pose08. This is gallery interaction, not native playback cadence or mobile-viewport proof.
- Browser handoff service returned credential401, so the same task continued with direct bridge actions as instructed. Initial async invocation syntax was rejected before QA ran; corrected invocation returned the above result. Neither is counted as an application failure.
- Added verification and regression commands to the existing spec-parity CI job. Production App/Sources/Assets, project settings, baseline source/native packets and the frozen variation packet remain untouched by this slice.

Verdict: native source-selection comparison and tested lifecycle behaviors are verified for this exact packet. Visual naturalness, midpoint shared traversal, continuous contact, live cadence and physical-device acceptance remain open. Issue237 remains open with its16-pose assertion unchanged. No new production or merge permission.
