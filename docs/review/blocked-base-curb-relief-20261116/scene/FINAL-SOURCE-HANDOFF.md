# Final-source scene handoff, November17 2026 00:15UTC

Supersedes only the first-source binding instructions in `HANDOFF.md`. Original handoff and all logs remain retained.

## Final-only admission

`scene/supplement_binding.py` now binds only `source/attempt-02/manifest.json`, pinned SHA256
`5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891`.
`SOURCE_ROOT` identifies the entire `source/` tree, while `SOURCE` identifies its final `attempt-02/` directory. Coordinator evidence is forbidden anywhere under `SOURCE_ROOT`, including first-attempt snapshots, original source files and final outputs. All prior scope/path/symlink/source/geometry/semantic/replay checks remain in force.

The final manifest requires attempt2/maximumAttempts2, no source self-recommendation and no native-evidence claim. Every frozen first-attempt dependency is independently rehashed. Final geometry bytes and all non-image sprite registration fields must match the first attempt. Source replay and all53 alpha comparisons use the exact final source validator. The first source cannot substitute for the final manifest or image source. No source files were modified.

## Checks actually run

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/review/blocked-base-curb-relief-20261116/scene -p 'test_*.py' -v`

**46 tests passed in22.771seconds**, raw `tests-attempt02-integration.log`.
The suite includes final source replay, independent geometry and semantic checks, first-manifest/image substitution, self-evidence under four source locations, rehashed final manifest pin mutation, dependency mutation even when replay is cached, frozen first dependency mutation and all prior41scene checks.

Frozen Swift fixture is unchanged:
`AppTests/BlockedBaseCurbSceneTests.swift`
SHA256 `a0dbdc1d30a1ea5a950001b2348434038a45c367ad1f42934151442755621638`.
Hash independently fetched after the final suite. No Swift edit, build or native execution occurred in this follow-up.

Changed this follow-up: `supplement_binding.py`, `test_binding.py`, `test_native.py`, `README.md`, `RUN-NATIVE.md`, this handoff and new test log, all inside scene/ only.

Coordinator still owns the actual review and exact recommendation file, bind/prepare, serialized fresh build/native execution, import and visual/gallery checks. This worker created no recommendation or preparation and performed no commit. One source correction is consumed. No third aesthetic attempt is permitted.
