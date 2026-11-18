# Source validation, November16 2026 20:52UTC

Status: SOURCE READY FOR COORDINATOR'S ISOLATED REVIEW INTEGRATION, NOT OWNER ACCEPTED.

- Python3.14.5, Pillow12.3.0, macOS. Nine portable tests passed in18.693s. `tests.log` preserves the actual command output.
- Standalone `build.py --probe v4` returned1. All three real v4 inverse crops exceed the finite rectangle. `v4-coverage-red.json` preserves the exact corners and failures.
- Standalone `build.py --probe fixed` returned0. `fixed-coverage-green.json` preserves the same corners and complete arena coverage.
- Complete source rebuild matched the manifest and every generated PNG SHA256. All seven pinned input digests remained exact before/after. Original paving directories show no git modifications.
- Every pixel in original corner-topdown.png matches the corresponding arena interior. Four independent original-context strip evaluations across every old finite edge match exactly. This proves no new rectangular patch seam, while retaining legitimate curb/joint transitions.
- Square texture adapter exact arena crop passed. Native bottom-left UV behavior follows the existing renderer implementation but has not been exercised by this worker.
- Visually inspected `diagnostic-preview.png` directly: paving and asphalt continue across the red former boundary without the old material switch. Curb, rails, crossing, drain and tactile panel retain the same geometry. Source repetition and fine road grain remain evident. This is an offline ground-only assessment, not a verdict on the ordinary complete scene or benchmark equivalence.

## Preserved implementation failure

First run passed8/9 checks. Deterministic manifest comparison rejected Python tuples from `inverse()` versus JSON lists read from disk. The generator now constructs JSON-native lists before returning its coverage records. No test, fixture, original source, visual parameter or assertion was changed. `attempt01-json-type-failure.log` and `attempt01-manifest.json` retain that failed attempt. All three output PNG hashes are identical before/after this metadata-only correction. This remains bounded visual sample01, not a second aesthetic revision.

## Final source SHA256

- `ground-arena.png`: `870428dbbc76bcf9e7a6b5de594285d06427dc1a71b590bb28cd3a7a1fc06fb3`
- `ground-patch-square.png`: `f4a3f542d8879b036c1a1979ab5fa03356b69350181fb526e190098982191dac`
- `diagnostic-preview.png`: `83f45a1b2f3f7d585f490fefec6ad25cf36f95a43c1ff595713ee6d2dbbeda5f`

No native/Swift runs, benchmark reads/copies, shared CI/handoff edits or commits were performed. Coordinator owns capture and integration evidence. Native texture filtering/orientation, memory performance, all other scene deficits and owner acceptance remain open.
