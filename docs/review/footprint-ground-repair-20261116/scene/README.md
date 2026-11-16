# V8 isolated footprint / ground comparison

Status: **actual native2321 retry imported and independently verified at23:25UTC**: one passed test, six captures/eighteen images, exact loaded/fresh-built executable agreement and nine complete V7 baseline RGBA matches. Coordinator's final visual review is `../REVIEW-FINAL.md`: overall benchmark NOT MET, owner review required. Current frozen Swift/input hashes and preserved native2317 preparation are in `ISSUE253-RETRY.md`. Final reviewed source hashes remain in `BINDING.md`. Worker preparation was not native evidence.
Owner authorization: `intent/2026-11-16-footprint-ground-consistency.md` approved November16 22:59:05UTC.
Task/contract references: BP-001/007/012, T1045. V7 remains rejected and immutable.

## Exact comparison

Fixture: `AppTests/FootprintGroundSceneTests.swift`, version
`source-scene-footprint-008-ground-plan`. Compilation conditions:
`DEBUG SS_SOURCE_SCENE_REVIEW SS_FOOTPRINT_GROUND_REVIEW` plus existing renderer test support.
One exact test: `SSRuntimeTests/FootprintGroundSceneTests/testQuietSouthNeutralOrdinaryScene`.
Observed xcresult identifier must be `FootprintGroundSceneTests/testQuietSouthNeutralOrdinaryScene()`.

Both arms preserve all nine V7 prepared source bytes, five building registrations,
all other actor registrations, Camera root/field, Player root, 24 solids, 18 upright
nodes, center `[684,724]`, production HUD/controls and zooms 1/1.25/1.4. Attachment
arm `control` means **BASELINE_V7_CANDIDATE**, not the original V7 control arm.
Candidate means **CANDIDATE_V8_SHARED_GROUND_PLAN**. Only the new ground raster and
exact plan-authorized decorative prop roots differ. Prop local/world depths remain
frozen. Final depth ranks are recomputed from unchanged solid envelopes and planned
prop roots using the same geometry-derived algorithm, never a visibility boost.

Immutable baseline record SHA256:
`9728f0a030020dff0caad52e8d3791be092a3b6ada8b5ffd845ee9d370785889`.
Importer and retained validator require all nine new baseline images to match the
V7 candidate full RGBA pixel arrays exactly, not merely a small sampled region.

## Actual contact versus authority

The old `groundFootprints` records remain for exact V7 correspondence. They are not
reinterpreted as actual contact. New `visibleBuildingContacts` are independent:
all five native actor canvases intersecting the retained crop require actual z=0
mesh vertices, source pixels, source hashes, native sprite-to-scene and ground-to-scene
conversions, and explicit in-crop flags. Kiosk chamfer contact is a five-vertex contour.
Its virtual blocked corner is not an actual contact landmark. Occlusion and offcrop
vertices are not falsely claimed visible pixels. This is a conservative canvas census,
not alpha-derived collision or occlusion certification.

All fourteen building envelopes receive plan semantic validation. The nine offcrop
legacy raster buildings retain explicitly unknown actual contacts, never inferred
from image bounds. Every visible building must have known contact source geometry.
The plan semantic validator independently checks whole-envelope foundation coverage,
sidewalk/curb boundaries, preserved authority, actual source geometry and prop clearance.
The binder also replays the reviewed source in a temporary directory and byte-compares
rendered ground, semantic material IDs and editable SVG to the recommended outputs.

`groundPlanWitness` measures the actual single patch's projected arena corners,
size/anchor/depth/visibility and exact source hash. `propPlanWitnesses` measure actual
roots and projected roots. Their contact/shadow limits are explicitly labeled baked
candidate-plan limits, not measured alpha envelopes of unchanged prop sprites.
The retained tree/newsbox sprite root is the front/base bottom, not the physical trunk
center. In particular, the plan's tree contact radius8 is not the full tree-grate radius.
Coordinator's separate `../prop-base-clearance.json` and `../verify_prop_bases.py`
check conservative source-image base regions against all24solids and compatible sidewalk.
Those raster-region checks are distinct from the planned new baked shadow disk.

## Coordinator recommendation contract

No pending/rejected source is bound or prepared. The coordinator authors a separate
JSON envelope (not created by this worker):

```json
{
  "schema": "footprint-ground-recommendations-008",
  "plan": {"path": "docs/review/footprint-ground-repair-20261116/plan/plan.json", "sha256": "EXACT_SHA256"},
  "manifest": {"path": "docs/review/footprint-ground-repair-20261116/plan/manifest.json", "sha256": "EXACT_SHA256"},
  "validator": {"path": "docs/review/footprint-ground-repair-20261116/plan/test_plan.py", "sha256": "EXACT_SHA256"},
  "recommendation": {
    "reviewerRole": "coordinator",
    "decision": "recommended",
    "scope": "isolated-ordinary-scene",
    "planSHA256": "EXACT_REVIEWED_PLAN_SHA256",
    "sourceSHA256": "EXACT_REVIEWED_GROUND_PNG_SHA256",
    "evidence": {"path": "EXACT_REPO_RELATIVE_COORDINATOR_REVIEW", "sha256": "EXACT_SHA256"}
  }
}
```

Paths and every byte hash are checked, including symlink rejection. All source manifest
files are rehashed every call. Deterministic replay cache keys include the exact binding
and all manifest hashes, never just a filename. Plan/source authority validation is not
optional. Unknown versions, wrong/missing recommendation roles, stale plan/source hashes,
forged authority/props/contacts and unsafe paths fail before preparation writes.
Only source attempts 1 or 2 can be bound, and recommendation remains separately required.
For the final material correction, immutable `plan.json` intentionally retains its
geometry-origin attempt1 label. Manifest/materials attempt2 must bind that exact same
plan and semantic raster as `attempt-01/`, while recursively preserving every old file.
The adapter resolves the reviewed sibling material module only in memory, writes replay
outputs only under a temporary directory, and compares all13 generated final outputs.
Retained paving/original material inputs are separately hashed and recorded as dependencies.

## Dependencies and commands

Read-only dependencies: immutable V7 scene, kiosk and context source/evidence packets,
the inherited V6/V5/V4 source dependency chain, production baseline resources and the
new sibling `../plan/` packet. Portable scripts require Python3 with Pillow. The source
correction may introduce additional explicitly manifest-bound retained material inputs.
No packages are installed by these scripts. Temporary replay uses `JCODE_SCRATCH_DIR`
when configured.

```sh
python3 -m unittest discover -s docs/review/footprint-ground-repair-20261116/scene -p 'test_*.py' -v
swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW -D SS_FOOTPRINT_GROUND_REVIEW AppTests/FootprintGroundSceneTests.swift
python3 docs/review/footprint-ground-repair-20261116/scene/native.py bind --recommendations /absolute/coordinator-recommendations.json
python3 docs/review/footprint-ground-repair-20261116/scene/native.py prepare
```

See `RUN-NATIVE.md` for exact coordinator-only build/capture/import commands. No native
build, simulator run, project generation, commit, push or unfiltered Swift test was
performed by this worker. Swift parsing does not certify typechecking or execution.
Portable tests use explicitly synthetic temporary records and must not be published as
native captures. Import requires exactly one passed test, zero failures/skips, six
captures/eighteen images, nineteen exact attachments, and the actually loaded executable
SHA matching a separately supplied fresh build artifact.

Retained checking without `--test-executable` certifies only agreement of preserved
import provenance, not a new build rehash. Fully coordinated replacement of every
unkeyed hash/trust anchor cannot be authenticated by hashes alone. Preserve actual
xcresult/build artifacts independently. Passing registration/semantic/provenance tests
does not establish visual fidelity, owner acceptance, physical certification or gameplay
admission. Final ordinary-view visual review remains coordinator/owner work.
