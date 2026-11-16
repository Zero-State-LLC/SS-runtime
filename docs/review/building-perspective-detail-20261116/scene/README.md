# V7 isolated building scene fixture

Status: **actual v7 native capture imported and independently verified at22:38-22:39UTC**.
`native-run-2237.log` passed exactly one selected test. `native-capture-v7/` contains
six actual captures/eighteen images with the loaded executable matching the separately
rehashed fresh build. See `../REVIEW-FINAL.md`: perspective/detail improved, overall
benchmark NOT MET. `BINDING.md` records the earlier22:37 preparation checkpoint.
Portable tests themselves create no native evidence. The worker mapped coordinator
recommendations without independently recommending source art.
Authorization: `intent/2026-11-16-building-perspective-detail.md`, BP-001/007/012, T1045.

## Scope and exact native selection

New fixture: `AppTests/BuildingPerspectiveSceneTests.swift`.
Required compilation conditions: `DEBUG SS_SOURCE_SCENE_REVIEW SS_BUILDING_PERSPECTIVE_REVIEW`.
Selected Xcode test ID:
`SSRuntimeTests/BuildingPerspectiveSceneTests/testQuietSouthNeutralOrdinaryScene`.
Observed xcresult identity must be
`BuildingPerspectiveSceneTests/testQuietSouthNeutralOrdinaryScene()`.
Fixture version: `source-scene-building-007-perspective-detail`.

The old attachment arm identifier `control` is retained for importer compatibility,
but its recorded meaning is **BASELINE_V6_CANDIDATE**, not old control art. Both arms
use v6 candidate Player, Camera, paving, props, outline/shadow and ground treatments.
Only the candidate kiosk and context solids 01, 02, 04 and 05 receive new images and
explicit size/anchor registrations. All roots, original depths, geometry-derived
ordering, 24 solids, field, HUD/controls, center `[684,724]`, zooms 1/1.25/1.4 and all
other nodes remain unchanged. Dynamic authoritative census retains 18 uprights,
including every backed context node, without concealment.

Read-only v6 `native-capture-v6/source-scene-records.json` is SHA-pinned at
`1cc28f757fb6e9e7ed6e53843c745bcb63f8adc42a2eef6413362582eac4930d`.
Every immutable capture/actor/inventory field compares independently to its v6
**candidate** row. Nothing rewrites v6 records into claimed v7 evidence.

Each capture records all 14 building-image hashes, explicit registration in the
actor/inventory rows, and four actual ground-transform vertices per building.
The five replacement buildings additionally measure source-pixel-to-node-to-scene
vertices and require agreement with the projected authoritative footprints to .002
logical points. Existing source correspondences are explicitly labeled
`authority-only-baseline-source-not-rederived`, not falsely claimed repaired.
Thirteen baseline runtime building image SHA pins were independently checked against
committed HEAD bytes. V6 did not measure those hashes, so this is not retroactive
v6 attestation.

## Coordinator source binding schema

Coordinator authors a JSON document outside this worker's files unless ownership is
explicitly handed over:

```json
{
  "schema": "building-perspective-recommendations-007",
  "sources": ["five source objects, see below"],
  "buildings": ["five building objects, see below"]
}
```

Both arrays must use order `kiosk`, `context-01`, `context-02`, `context-04`,
`context-05`. Each source object:

```json
{
  "role": "kiosk",
  "status": "recommended",
  "image": {"path": "repo-relative exact reviewed PNG", "sha256": "exact SHA256"},
  "registration": {
    "canvasPixels": [1024, 1024],
    "rootPixelsTopLeft": [512, 512],
    "worldPosition": [512, 640],
    "drawSizeWorld": [256, 256]
  },
  "dependencies": [
    {"path": "repo-relative editable source manifest", "sha256": "exact SHA256"},
    {"path": "repo-relative explicit source registration", "sha256": "exact SHA256"}
  ],
  "recommendation": {
    "reviewerRole": "coordinator",
    "decision": "recommended",
    "scope": "isolated-ordinary-scene",
    "sourceSHA256": "exact reviewed image SHA256",
    "evidence": {"path": "repo-relative coordinator visual review", "sha256": "exact SHA256"}
  }
}
```

The numeric example above is illustrative schema only, **not a valid recommended
registration**. Use the source author's actual geometry-derived values. Include all
editable/geometry/material/export manifests needed to preserve the source audit in
`dependencies`. Paths and every byte hash are checked, including internal symlinks.

Each building object has exactly `role`, `solidID`, `nodeName`, and
`groundPixelsTopLeft`. The latter is four `[x,y]` pairs in original image pixels,
ordered authoritative corners **min/min, max/min, max/max, min/max**. Kiosk world root
is `[512,640]`. Context roots are the original authoritative solid centers, not a
new composition placement. SpriteKit anchor is
`[rootX/canvasWidth, 1-rootY/canvasHeight]`.

The binder independently checks each source ground pixel against D108:
`((worldX-rootX)-(worldY-rootY))/sqrt(2)` and
`((worldX-rootX)+(worldY-rootY))/(2*sqrt(2))`, before writing any preparation.

## Commands

From the repository root, with a Python interpreter providing Pillow:

```sh
python3 -m unittest discover -s docs/review/building-perspective-detail-20261116/scene -p 'test_*.py' -v
swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW -D SS_BUILDING_PERSPECTIVE_REVIEW AppTests/BuildingPerspectiveSceneTests.swift
python3 docs/review/building-perspective-detail-20261116/scene/native.py bind --recommendations /absolute/coordinator-recommendations.json
python3 docs/review/building-perspective-detail-20261116/scene/native.py prepare
```

Only coordinator may perform the serialized native build/capture. No simulator,
project generation, full Swift test run, commit or push was performed by this worker.
After that actual single-test run, before rebuilding the test executable:

```sh
python3 docs/review/building-perspective-detail-20261116/scene/native.py import --xcresult /absolute/result.xcresult --output docs/review/building-perspective-detail-20261116/scene/native-capture-v7 --test-executable /absolute/build/SSRuntimeTests.xctest/SSRuntimeTests
python3 docs/review/building-perspective-detail-20261116/scene/retained.py docs/review/building-perspective-detail-20261116/scene/native-capture-v7 --test-executable /absolute/build/SSRuntimeTests.xctest/SSRuntimeTests
```

Import requires exactly one passed test, no skipped/failed/expected failures, six
captures, eighteen images, exact export test identity and nineteen export attachments,
and the actual runtime loaded executable SHA matching the separately supplied built
product. Source-file SHA is explicitly not binary attestation. Retained checking
without `--test-executable` only checks agreement of preserved import provenance,
not a fresh build rehash. Fully coordinated malicious replacement of every file and
trust anchor cannot be authenticated by unkeyed hashes alone. Preserve actual xcresult
and build artifacts as the independent provenance source.

Unknown versions, missing/unreviewed/rehashed sources, stale v6 binary, forged authority,
actor/depth/framing/ground witnesses, missing images, and rehashed export manifests fail
closed. Portable tests use only in-memory or temporary explicitly synthetic mocks and
must never be presented as native evidence. Technical passing does not establish
visual acceptance, source fidelity, family animation or physical-device certification.
