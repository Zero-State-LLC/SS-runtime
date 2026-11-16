# Ordinary-scene source assembly preparation

## Final result, November16 10:47UTC

Actual final native evidence and the gallery are now available. Read `REVIEW-FINAL.md` first: **overall visual result NOT MET**, with owner scene review required before expansion. Successful result1041 is retained in `native-capture-1040/` (the gallery packet label). One native test, six captures, eighteen images and matching loaded/fresh-build executable hashes are verified. All75portable scene guards,8gallery structure checks and both JavaScript suites pass. Actual browser verification exercised36display combinations. No owner acceptance, production admission, motion/encounter expansion or physical certification follows.

The preparation checkpoints below are historical and do not supersede this final verdict.

**Current issue248 / revision4:**1030's upright geometry passed, but actual review found shared-depth/insertion-order occlusion. Exact1030 code and evidence are preserved. All uprights now receive stable back-to-front projected-root ranks in a bounded original-depth band, without Camera alpha changes. `native-inputs-v4` is prepared; see `DEPTH-ORDER.md`. Final1040 native capture and visual inspection remain coordinator-owned. Source fidelity is not accepted.

**Issue247 update:** coordinator capture1020 exposed omitted environment-upright projection despite passing old technical checks. It is preserved, not accepted. Revision3 now inventories and extracts the complete existing upright cohort, with exact importer census and uniform-basis guards. See `UPRIGHT-CENSUS.md`. Fresh `native-inputs-v3` is prepared; corrected native capture remains coordinator-owned after review. Original1020 evidence and original `native-inputs` remain unchanged.

**Final source recommendations are bound. Strict tracked-dependency validation and native preparation are required before capture. No scene image, native scene capture, visual acceptance or production integration is delivered.**

Authorized by `intent/2026-11-16-scene-method-approval.md` (09:31 UTC).
Initial preparation was confined to this directory. The 09:47 UTC continuation
also authorizes the new `AppTests/SourceSceneContinuationTests.swift`, documented
in `NATIVE.md` with the exact coordinator-owned command. BP-001/007/012/T1045 remain review context,
not permission to change collision, fields, source admission or production.

## Runnable preparation

Python 3.10+ and Pillow (already used by the tracked paving packet) are required.
From the repository root:

```sh
python3 -B docs/review/scene-source-assembly-20261116/assemble.py --root .
python3 -B -W error::ResourceWarning docs/review/scene-source-assembly-20261116/test_assembly.py
```

Verifier exit codes: **0** ready for offline assembly only, **2** valid preparation
but required inputs blocked, **1** invalid dependency/registration/admission.
The preserved `assembly-pending-v2.json` returns 2 with the historical Camera, Player
and stone reasons. The current manifest binds the final recommended sources and
actual placement probe1014. It still rejects any untracked or changed dependency.
No render occurs during a check. A rejected or pending record must have null image,
registration and recommendation, so it cannot smuggle an old fallback into a scene.
All four roles are mandatory even if a caller deletes a source entry.

After strict dependency validation succeeds:

```sh
python3 -B docs/review/scene-source-assembly-20261116/assemble.py --root . --render "$JCODE_SCRATCH_DIR/ordinary-source-review.svg"
```

This command creates an output only if all tracked dependency checks pass. It creates a new
self-contained SVG with embedded source PNG bytes and a visible offline/not-accepted
label. It never overwrites prior output. It is a source-composition tool, **not**
SpriteKit, native/half inspection, encounter evidence or the completed ordinary game
scene. No HUD, collision, targeting, Camera fields, damage state or motion is invented.
The viewport is an explicit review framing proposal, not a gameplay authority.

## Exact source and registration

`assembly.json` binds actual paving image bytes, its source recipe, builder, material
input, output manifest and existing coordinator review. Paths are repository-relative,
not machine-specific. Every dependency must exist, be tracked and match SHA256.
Absolute paths, parent traversal, dot aliases and symlink dependencies are rejected.
The repository root itself may be a filesystem alias, as on macOS.

The actual paving canvas is 1152 x 1152. Its source-space root is `(0,1152)`
(top-left pixel convention), world position `(448,384)`, and world draw size
`576 x 576`, exactly transcribed from the tracked 2 pixels/world-unit source recipe.
Only its existing bounded material/layout recommendation is transcribed, not a new
review or whole-environment acceptance. No dependency references any untracked
`paving-context-source`, Player family or editable-master packet.

A future admitted source needs:

1. Tracked PNG path and exact hash, with actual canvas dimensions.
2. Explicit source root, positive world draw size, world placement, coordinate
   convention, and ground/upright kind. No alpha bounds infer the root or geometry.
3. Coordinator `recommended` record for the correct scope, binding both source hash
   and SHA256 of canonical registration JSON (`sort_keys=True`, compact separators).
4. Hash-pinned, tracked coordinator review evidence. Changing placement, root, size,
   source or verdict invalidates the prior binding. Owner acceptance is neither
   required nor substituted for coordinator recommendation.

The verifier checks the consistency of records, not a reviewer's identity or the
truth of prose. Coordinator publication/review remains the trust boundary. A person
can rewrite an entire unsigned packet, so hashes are not a signature or art quality
proof. No automated check may manufacture a recommendation.

## Existing contracts used, located through Trail

- `docs/review/paving-corner-review-20261116/build.py:77-92` defines image rows as
  decreasing world Y, world bounds and pixel density. `:145-154` records the D-108
  orthographic midpoint ground transform, `(x-y)/sqrt(2), (x+y)/(2sqrt(2))`.
- `docs/review/paving-corner-review-20261116/source.json` is the actual bounded
  paving registration/layout source. Its README's Coordinator review limits scope.
- `AppTests/AllReleaseSourceTests.swift:52-104` demonstrates exact source textures,
  fixed logical size and source top-left root converted to a SpriteKit anchor.
  This packet uses the same explicit root/size principle, not those rejected art bytes.
- `docs/review/service-building-repair/register_source.py:18-29` retains explicit
  source-pixel/world scaling and ground-anchor registration independent of collision.
- `docs/review/camera-midpoint-source-20261116/build.py:82-137` distinguishes upright
  art at a projected root from ground-plane projection and source-only evidence from
  native evidence. This is registration precedent only, never Camera art admission.

Uprights stay upright at projected roots. Ground rows reverse world Y. Depth ordering
is stable by projected root depth then role. None of these operations reads or changes
game collision/field data. This is a small isolated adapter, not a new runtime schema.

## Portability

A preparation export is allowed even while scene rendering is blocked:

```sh
python3 -B docs/review/scene-source-assembly-20261116/assemble.py --root . --export "$JCODE_SCRATCH_DIR/scene-preparation-export"
python3 -B "$JCODE_SCRATCH_DIR/scene-preparation-export/assemble.py" --root "$JCODE_SCRATCH_DIR/scene-preparation-export"
```

Use a new export destination. Export
copies only declared checked dependencies, manifest and assembler, retaining their
relative paths. `tracked-inputs.json` records the originating Git HEAD and exact bytes
checked against Git's index membership. The manifest and assembler are preparation
files, not falsely claimed to have been committed. Offline validation requires each
referenced dependency to appear in that receipt and match it. This makes replay
independent of the original checkout or neighboring unpublished work. The receipt is
an unsigned export record, not evidence that all bytes equal HEAD or a native capture.
This exports **assembly inputs**, not every unrelated paving gallery output.

## Blocking inputs and distinct verdicts

| Role | Current state | Required next input |
| --- | --- | --- |
| Paving | Bounded coordinator recommendation | Retain exact layout/material scope, whole-scene verdict still pending |
| Camera | Final padded master recommended, hash1343507b... | Bound root58,427, uniform96/418, actual seed1 Camera id3 at496,672 |
| Player | Canonical-identity-02 recommended for quiet south-neutral | Bound root192,336, uniform1/6, presentation-only placement736,654 |
| Stone | Final changed-method composite recommended, hash5b575160... | Bound root500,1160, uniform0.2, world512,640, original128x128 collision retained |

Scene visual verdict, owner verdict, native verdict and production verdict are all
pending/unestablished. No source acceptance is inferred from passing technical tests.
Motion and encounter expansion remain gated by owner scene review. #237/#239/#240/#241
remain distinct. No commits, pushes, CI/shared handoff, production or specification-pin
changes are made. The authorized native continuation adds only the new AppTests file
and packet-native preparation/importer. See `NATIVE.md` for its unexecuted build/run gate.
The v2 native fixture requires exactly three zooms per ordinary arm (six records,
eighteen images), exact fixtureVersion, world/projected roots, and actual loaded test
executable SHA/path separately from the current Swift source-read hash.
Both native methods are compiled only with `DEBUG && SS_SOURCE_SCENE_REVIEW`, so
ordinary CI does not discover checkout-only review tests. `NATIVE.md` also provides
a source-free seed-1 placement probe command to read actual Camera/solid authority
before assigning source world placements. No guessed socket is treated as a selected Camera.

## Focused tests

`test_assembly.py` labels generated PNGs, review text and SVGs **SYNTHETIC** and removes
them with temporary directories. Positive rendering tests prove mechanics only.
They cover required-role census, source and evidence mutation, coordinator versus
owner gates, stale registration/source binding, malformed geometry, untracked/missing
files, traversal/symlink rejection, root alias handling, source-root mapping, output
preservation and receipt membership/hash enforcement. Real paving preparation is
also exported and checked in a separate process without Git in the export root.
The historical pending export remains blocked and emits no scene. A separate final-binding
regression verifies the current real source/root/scale records and portable export without
rendering. `assembly-pending-v2.json` preserves the actual pre-binding manifest so existing
negative assertions remain unchanged. `blockers-v2.json` is historical and is not rewritten.
No fake native evidence exists. See `BINDING.md` for the actual placement provenance.

### Recorded run, November 16 09:38 UTC

`tests.log` retains **25 passing tests in 5.497 seconds**, Python 3.14.5 and
Pillow 12.3.0. `blockers.json` is the actual real-manifest check output, exit 2.
Positive renders were temporary synthetic fixtures only. No real scene SVG exists.
Swift/native tests were not run in the initial isolated phase. The subsequent
09:47-authorized native harness has syntax-only validation, not a native run.
