# V9 scene adapter, BP-001/007/012 T1045

Approved intent: `intent/2026-11-16-blocked-base-curb-relief.md`.
Only this new `scene/` and `AppTests/BlockedBaseCurbSceneTests.swift` are scene-worker outputs.
No historical bytes, production renderer, source art, spec pin or project configuration were edited.

## Adaptation and authority

ADAPT current `AppTests/FootprintGroundSceneTests.swift:1-748` and
`footprint-ground-repair-20261116/scene/native.py:1-245`, not failed `native2317`.
Retained verification adapts current V8 `scene/retained.py:1-40`.
Native export uses read-only V6 `scene-qa-framing-20261116/native.py:205-253` with private V9 validators.
Old plan/source/authority semantics continue through V8 `expected_input`, including its
source replay. All unchanged V8 assembly keys must exactly equal the actual V8 assembly.
The exact float-backed ground check remains `CGFloat(Float(0.1))`, with an independent
negative test rejecting double `0.1` in a V9 capture record.

Fixture `source-scene-base-curb-009-relief`, input `source-scene-native-009`,
records `source-scene-records-009`. Both arms retain V8 candidate ground, props, sources,
registrations, authority, framing, controls and all 18 existing actors.
Roles: `BASELINE_V8_CANDIDATE` and `CANDIDATE_V9_BASE_CURB_RELIEF`.
Actual V8 record SHA: `f7a8e0119307305fa4cfd15281871f1c852787d3f6c1ba3d0bc2342c421bf762`.

## Supplemental source API

Only source-owned `source/attempt-02/manifest.json`, schema `blocked-base-curb-source-009`,
attempt2/maximumAttempts2, supplies `sprites`, `files`, `baselineFiles` and
`firstAttemptFiles`. See `source/attempt-02/API.md`.
The final manifest is pinned to
`5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891`.
The first `source/manifest.json` remains immutable historical evidence and cannot
substitute for the final source. Final file dependencies resolve from `source/attempt-02/`.
All first-attempt files are independently rehashed, geometry remains byte-identical,
and every non-image sprite registration field must exactly equal its first source.
The binder independently reconstructs bounded prism faces, actual Z0 contact contours,
centroid roots, D108 XYZ registration, height and bounds. Every curb half-world cell
must equal existing V8 semantic material2, without duplicates or omissions in the
approved source region. Props retain conservative contact/shadow clearance.
Final `source/attempt-02/test_source.verify_manifest(path=..., replay=True)` must additionally pass,
including final replay and all53 first/final alpha comparisons.
All source files and immutable dependencies are rehashed on every validation, with
only replay cached for an exact dependency/recommendation envelope.

Normalized fixture supplement fields:

```text
role, nodeName='supplement-'+role, file=role+'.png', sha256,
registration={canvasPixels,rootPixelsTopLeft,worldPosition,drawSizeWorld},
verticesWorldXYZ, verticesPixelsTopLeft, footprintWorld=[minX,minY,maxX,maxY]
```

The present source has 53 supplemental pieces: one base and 52 small curb prisms.
Candidate census is separately reported as 18 existing actors plus 53 supplements,
71 presentation uprights. Control has 18 plus zero. Supplements never masquerade as
existing actors. Native extraction independently enumerates supplemental nodes.
Both cohorts share the unchanged `SceneQAReviewDepth.order` algorithm. New nodes
start with original local/world Z zero, then geometry determines joint order. The
old cohort's rank/Z may change only as that unchanged algorithm incorporates real
new footprints. No visibility boost, billboard height invention or lifted ground image.
Actual native `SKNode.convert` witnesses compare every new source pixel landmark
against ground-chain world XY plus explicit world Z scaled by zoom.

## Final recommendation gate

Scene preparation waits for a separate coordinator-authored recommendation over the
exact final manifest. Source's `FINAL_CORRECTION_PENDING_COORDINATOR` status is not admission and
is not rewritten by the scene worker. A missing, pending, rejected, wrong-scope or
source-worker recommendation fails closed. The final coordinator's exact-hash
recommendation is the admission decision, independent of source self-description.

Envelope consumed by `native.py bind --recommendations PATH`:

```text
schema: blocked-base-curb-recommendations-009
manifest: {path: repository-relative source/attempt-02/manifest.json, sha256: pinned final hash}
dependencies: [{path: repository-relative source file, sha256: hash}, ...]
recommendation:
  reviewerRole: coordinator
  decision: recommended
  scope: isolated-ordinary-scene
  manifestSHA256: exact final manifest hash
  evidence: {path: coordinator review outside ALL source/ descendants, sha256: exact review hash}
```

Dependencies must exactly enumerate `manifest.files` in sorted filename order,
converted to repository-relative paths. No path aliases, traversal or symlinks.
Do not use the unit tests' synthetic in-memory recommendation fixture as art authority.
The tests write no recommendation, assembly, preparation or native evidence.

## Commands and limitations

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/review/blocked-base-curb-relief-20261116/scene -p 'test_*.py' -v
swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW -D SS_BLOCKED_BASE_CURB_REVIEW AppTests/BlockedBaseCurbSceneTests.swift
```

Swift validation here is **parse only**, not typechecking, building or native execution.
Coordinator-only capture instructions are in `RUN-NATIVE.md`.
Import requires exactly one passed selected test, six captures, eighteen images,
nine complete baseline RGBA matches to actual V8 candidate, exact loaded/fresh-built
executable equality and full old/new source and semantic witnesses.
Retained verification is never a new native-run claim.

The first preview and one bounded source correction are now preserved. Only the final
native comparison remains. No third source attempt is allowed. Preserve every failed attempt. No additional art
retry, unfiltered Swift, production admission, owner acceptance, physical-device
certification, merge or issue closure is granted by these checks.
