# Issue248: final bounded depth-order correction

Coordinator opened runtime248 before authorizing this correction at10:28 UTC. Actual1030 restored upright geometry but background civic art still occluded the kiosk through inherited shared solid-layer Z and insertion order. This is a distinct fixture defect, not source fidelity acceptance. No additional source aesthetic changes are made.

## Immutable1030 attempt

`attempt-1030-before-depth-order/` preserves exact executedv3 Swift, native.py, assemble.py, both owned test files, assembly.json, NATIVE.md, native-inputs-v3 and every native-capture-1030 record/image/verification file. Originals remain at their existing paths. `attempt-1030-sha256.txt` inventories every copied byte. Readback verified all hashes, identical original capture/preparation bytes, and archived Swift SHA equality with actual1030 source-read metadata. Both1020 and1030 archived importers remain available; tests run their historical `validate_records` entry points on actual historical records and prove the current importer rejects those old schemas.

## Exact adapted rule

ADAPT only the ordering portion of `App/BenchmarkReviewArt.swift:215-223`, not its subsequent Camera alpha modification. The new harness does not call `orderActors` or assign alpha.

1. Retain revision3's full independent upright inventory and exact environment census.
2. Before extraction, measure original world depth by summing each node's local Z and ancestor Z up to the scene. Keep original local Z separately.
3. After projection extraction, sort **all** uprights back-to-front by projected world-root Y descending, then stable sprite name ascending for equal Y.
4. Set unique Z as `originalMaximumWorldDepth + rank / uprightCount * 0.5`, confined to `[originalMaximumWorldDepth, originalMaximumWorldDepth + 0.5)`.
5. Record `depthOrder`, `depthBase`, `depthBand`, each actor's `depthRank`, `actualZ`, `originalWorldDepth` and `originalLocalZ`. Native assertions check ordering, uniqueness and the bounded band.
6. Restore original parent, position and local Z in `defer`, installed before extraction so failure paths also restore them. Assert restored local Z after each capture.

Textures, source roots, sizes, anchors, scales, alpha, HUD, controls, field geometry,24solids and authority digest are not changed. No object is hidden or removed to fix overlap. The importer independently derives expected root order from world coordinates, checks stable ties, exact ranks and actual bounded Z, while retaining every revision3 census/registration/basis guard.

## New boundary and preparation

Fixture `source-scene-continuation-004-depth-order`, input schema `source-scene-native-004`, records schema `source-scene-records-004`. Fresh inputs reside in `native-inputs-v4`; v3 inputs remain immutable. Preparation succeeded, receipt `preparation-depth-v4.json`.

Harness source SHA256: `4d3d75665af922014f6643a5b5d8f9f676f303043fc85fae1a5aefbbec2a6854`.
Prepared JSON SHA256: `2dcfaf2490f544a53e0a2cc2157b09ad287282a55f737ea5f8d655be77602612`.
These are not a new loaded executable hash or corrected native capture claim.

## Validation and handoff

62 explicit owned tests passed5.880s, including background-in-front, equal-depth, wrong-rank/order, name-tie drift, out-of-band/base/original-depth mutations, historical1030 preservation, and unchanged revision3 guards. Both Swift frontend parse modes passed: DEBUG with and without SS_SOURCE_SCENE_REVIEW. Output: `tests-depth-v4-initial.log`. Final rerun after documentation updates passed **62tests in7.002s**, retained in `tests-depth-v4-final.log`. A fresh `expected_input()` comparison and all four prepared PNG hashes matched. Scoped `git diff --check` passed.

Only the requested suites were run:

```sh
PYTHONPATH=docs/review/scene-source-assembly-20261116 python3 -B -W error::ResourceWarning -m unittest test_assembly test_native -v
```

Coordinator-owned `retained.py` and `test_retained.py` were neither edited nor run. No native command, production/CI change, commit or push was made. `NATIVE.md` names the1040 result/output and selected `testQuietSouthNeutralOrdinaryScene` with both explicit review flags. Inputs are already prepared; rerunning prepare intentionally refuses overwrite. Coordinator code review, native1040 import/retained verification and actual visual inspection are the remaining gate. Source fidelity is still not accepted.
