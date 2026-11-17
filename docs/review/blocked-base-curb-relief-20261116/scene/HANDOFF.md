# Scene-worker handoff, November16 2026 23:59UTC

BP-001/007/012 T1045. Approved V9 scene-only implementation is ready for coordinator
review. No source recommendation, assembly/preparation, native capture, build,
simulator operation, xcodegen, unfiltered Swift, historical edit, commit or push
was performed by this worker.

## Exact checked fixture

`AppTests/BlockedBaseCurbSceneTests.swift`
SHA256 `a0dbdc1d30a1ea5a950001b2348434038a45c367ad1f42934151442755621638`.

## Validation actually performed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/review/blocked-base-curb-relief-20261116/scene -p 'test_*.py' -v`: **41 passed**,17.434seconds. Raw `tests-path-guards.log`.
- `swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW -D SS_BLOCKED_BASE_CURB_REVIEW AppTests/BlockedBaseCurbSceneTests.swift`: exit0 after the final fixture edit. **Parse only**, not typecheck/build/native execution.
- Original V8 `expected_input` and `validate_records` against actual retained V8 records: exit0, `v8-contract.log`. Replay writes only temporary scratch outputs. Historical V8 sources/records were not changed.
- Source replay and independent source/geometry/cell/registration checks pass for53 supplemental sprites. Exact source/immutable hashes are rechecked by binder. All9 baseline RGBA negative cases pass, each rejects a one-pixel mutation.
- Earlier31/38/40test logs retained. No failed native attempt was consumed or removed.

## Files changed

Only new `AppTests/BlockedBaseCurbSceneTests.swift` and this new `scene/`:
`native.py`, `supplement_binding.py`, `retained.py`, `test_native.py`,
`test_binding.py`, `README.md`, `RUN-NATIVE.md`, this handoff and validation logs.
Unrelated source/gallery/coordinator files are not scene-worker changes.

## Next coordinator actions

1. Review actual final source preview and author the separate exact final coordinator recommendation. Envelope/API is in `README.md`. Test synthetic recommendations are in-memory protocol fixtures, not admission authority. Source preview's pending label is historical source provenance, not coordinator admission.
2. Bind and prepare only after that recommendation. Confirm source/fixture freeze before a fresh build. `RUN-NATIVE.md` contains coordinator-only serialized instructions.
3. Build/typecheck and run exactly `BlockedBaseCurbSceneTests/testQuietSouthNeutralOrdinaryScene` with `SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW SS_BLOCKED_BASE_CURB_REVIEW`.
4. Import against that actual fresh-built executable without rebuilding. Require1passed test,6captures,18images,9complete V8 candidate baseline RGBA matches, loaded/build hash equality, actual source XYZ witnesses,18old plus53candidate-only supplements, joint geometry-derived depth and all retained V8 semantics.
5. Inspect actual three-zoom native/half/grayscale images and exercise the gallery/browser/tracked export. Those remain coordinator responsibilities, not source-test claims.

Scene only cannot certify visual obstruction, fidelity, owner acceptance, actual
native rendering, production admission or physical devices. At most one bounded
source correction and one final native comparison remain governed by the approved
contract. Preserve all attempts. No automatic extra aesthetic retry is authorized.

Trail context savings this worker turn: approximately1,434,576tokens.
