# V6 fixed-control-safe framing fixture

Final coordinator result: native2122 passed one test with six captures/eighteen images and exact loaded/build hash agreement. Corrected 39-test framing suite, retained evidence and actual-browser checks pass. See `REVIEW-FINAL.md` for final verification, retained failures and the still-NOT-MET visual verdict. The worker's earlier checkpoints below remain historical.

Authorized by `DIAGNOSIS.md` under the existing bounded QA repair pass. This is the second quiet scene comparison, not source acceptance, production admission, motion/encounter evidence or physical-device certification.

## Scope and files

`AppTests/SceneQAFramingTests.swift` adapts the immutable v5 `SceneQARepairTests.swift`. The only presentation change is the view center `[736,672]` to `[684,724]`, for both arms at zooms 1, 1.25 and 1.4. Source bytes, actor/world roots, authority, solids, fields, contour/contact treatment, geometry depth and control layout stay unchanged. No v5 file is rewritten.

- `native.py`: exact v6 preparation, import and framing guards. Explicit v6 schemas/version are required before copies are checked by the untouched strict v5 validator. Original records and v5 module globals are never rewritten. All non-framing actor registrations, source hashes and contact/ground treatments must also match the SHA-pinned actual v5 record.
- `retained.py`: uses the exact existing retained byte/image/provenance checker through private function globals pointing to the v6 adapter. It does not attest a new native run.
- `test_native.py`: synthetic v6 records, overlap/clipping/control mutation checks, strict-version separation, exact source preparation, and the read-only v5 Camera/stick overlap witness.
- `test_retained.py`: synthetic rasters and rehashed record-forgery tests. These are deliberately not screenshots or native evidence.

Fixture version: `source-scene-qa-006-control-framing`. Input schema: `source-scene-native-006`. Record schema: `source-scene-records-006`. Preparation directory: `native-inputs-v6`. Selected native identity: `SceneQAFramingTests/testQuietSouthNeutralOrdinaryScene()`. The original `source-scene-*` attachment names, six captures and eighteen images are retained.

## Measurement contract

Each capture adds `framing` with `coordinateSystem: logical-crop-top-left-704x326`, zero safe-area insets, exactly three `visibleControls`, and exactly two `actorCanvasBounds`. Every rectangle is `[left,top,width,height]` in logical crop units, not physical PNG pixels.

The harness reads actual `control_stick_base`, `control_dodge` and `control_pause` SKShapeNodes. It transforms each actual path bounding box plus half the actual stroke width into the logical crop. It checks ancestor visibility, matches the path against the actual `ControlLayout`, confirms the stick knob and dodge/pause labels are contained, and checks controls are in-crop. The broad invisible movement activation zone is never substituted for visible geometry. The Python oracle independently reproduces the fixed integer HUD reference/center-anchor mapping from `HUDLayout.swift:98-173` and `HUDAnchor.swift:26-57`. `HUDRenderer.swift:611-699` explicitly sets stick/dodge stroke widths to `2*704/896`, while pause retains its default `1` point stroke.

Issue250 corrects only the Python per-role stroke oracle. Before correction, the independent synthetic default-pause regression failed with `Visible control stroke changed`, while the malicious scaled-pause regression failed because that mutation was accepted. The corrected oracle must accept default pause width `1` and reject scaled pause width `2*704/896`, even when its bounds are changed consistently. Stroke tolerances and all other guards remain unchanged. Frozen Swift, prepared inputs, native2122 result bytes and `import-2122.log` are preserved for coordinator reimport of the same result.

At 21:25 UTC on November 16, 2026, `python3 -m unittest discover -s docs/review/scene-qa-framing-20261116 -p test_native.py -k issue250 -v` demonstrated both failures before the correction. After correction, `python3 -m unittest discover -s docs/review/scene-qa-framing-20261116 -p 'test_*.py' -v` passed all 39 tests. This is portable regression evidence, not a native reimport claim.

Player/Camera canvas bounds are measured from all four registered local corners after projection. They must be completely in-crop and nonoverlapping every visible control at every zoom, in both arms. Python independently derives the same bounds from the already-validated projected roots, sizes, scales and anchors. This checks full canvas rectangles, not alpha occupied bounds, not arbitrary visibility scores, and not the position of the root alone.

The historical red witness uses **actual v5 actor registration/projection records**, with **analytically reconstructed** fixed control geometry. V5 did not record actual control rectangles, so the witness is not mislabeled as a historical measurement. Its zoom-1.4 candidate Camera/stick overlap must remain rejected. No v5 screenshot or record is changed to make that witness green.

## Commands

Run from the repository root. Binding and preparation both refuse to overwrite existing outputs:

```sh
python3 docs/review/scene-qa-framing-20261116/native.py bind
python3 docs/review/scene-qa-framing-20261116/native.py prepare
python3 -m unittest discover -s docs/review/scene-qa-framing-20261116 -p 'test_*.py' -v
swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW AppTests/SceneQAFramingTests.swift
```

The last command is syntax parsing only, not typechecking, building or native execution. Coordinator owns the existing serialized native workflow and selects only the exact v6 test identity above. After that run, with real paths supplied by the coordinator:

```sh
python3 docs/review/scene-qa-framing-20261116/native.py import --xcresult "$RESULT" --output "$FRESH_CAPTURE" --test-executable "$BUILT_TEST_EXECUTABLE"
python3 docs/review/scene-qa-framing-20261116/retained.py "$FRESH_CAPTURE"
python3 docs/review/scene-qa-repair-20261116/qa.py --capture "$FRESH_CAPTURE" --prepared docs/review/scene-qa-framing-20261116/native-inputs-v6
```

The unchanged v5 pixel probe remains a separate required check. A framing pass does not replace pixel probes, actual image inspection or owner acceptance.

## Validation observed November 16, 2026, 21:17 UTC

All 37 portable tests passed. Swift syntax parsing passed. The v5 importer, retained verifier and actual v5 record SHA256 values matched their pre-change values. No native run, simulator, project generation, commit, or acceptance claim was made by the implementation worker. Native typechecking and actual v6 capture remain coordinator work.
