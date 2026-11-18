# First source validation and handoff

November16,2026 23:55UTC. BP-001/007/012, T1045.

## Observed commands and results

- `PYTHONDONTWRITEBYTECODE=1 python3 source/author.py`: authored53supplemental sprites,52curb rectangles, one blocked triangular base. Source only.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/replay.py --out source/attempt-01`: succeeded once. New PNGs and exact registrations, no historical modifications.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/preview.py`: one first preview produced. Three retained zooms1/1.25/1.4, each full/half/grayscale, detailed base/curb crop and full uncropped benchmark comparison.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/freeze.py`: froze80source files. Manifest SHA256 `49939b540e47b6c87a777e940a60add957c12013fbb1c6237f9794f8b32aa5e6`.
- `PYTHONDONTWRITEBYTECODE=1 python3 source/test_source.py`: **25tests passed**,1.965seconds. `tests-first.log` preserves complete output.20geometry/registration mutations,5manifest corruptions and4unsafe paths rejected. Existing-output overwrite rejected.
- Independent `test_source.verify_manifest(replay=True)`: **PASS**, second source replay byte-identical,187immutable baseline/retained dependencies match,18,880existing semantic curb pixels covered exactly without overlap,53supplemental sprite registrations validated.

## Integration handoff

`manifest.json` schema `blocked-base-curb-source-009`; full field contract in `API.md`. Each sprite has repository-relative PNG path and hash, canvas/source anchor/world root/world draw size, contact polygon XYZ, real height, geometry XYZ bounds and source-pixel witnesses. Base root[525,653], exact triangle contacts[512,640,0],[551,640,0],[512,679,0], height18. Curbs height3. Source geometry and material controls are editable, but first outputs remain immutable.

Scene worker received this API before implementation and final exact manifest hash after tests. Use retained geometry depth without a visibility boost. In particular, the new base's contact centroid differs from the kiosk's virtual-corner root, and their bounding footprints overlap. Actual native ordering must be inspected, not inferred from source overlays.

First image locations are in `README.md`; coordinator received them before test completion. This worker inspected the detail and full benchmark plate only to verify evidence presence and layout, not to issue a source recommendation. No second aesthetic attempt was made. Coordinator must provide exact bounded correction if desired, or recommend exact hashes separately. Source manifest deliberately remains pending regardless of test outcome.

No historical edit, production change, native execution, Swift build, commit or push. Source-only delegation leaves project/native tests to the coordinator. The nine historical offcrop actual mesh contacts remain unknown.

Trail orientation/context calls saved approximately1,354,607tokens this turn (tool estimates).
