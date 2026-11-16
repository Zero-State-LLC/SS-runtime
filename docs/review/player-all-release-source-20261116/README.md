# Player south all-release source continuation

Status: SOURCE CHECKS PASS, ALL 14 NEW PHASES REMAIN PROPOSED. Coordinator verified browser readiness and the separate static native packet at `../player-all-release-native-20261116/`. Ready for owner contact and weight-transfer review. No visual acceptance, admission, shipping change or live-cadence claim.

## Scope and gate

Owner selected midpoint at 2026-11-16 01:39 UTC. The coordinator explicitly confirmed the committed projection decision and authorized generation at 01:47:34 UTC. The specification decision commit is `167171d89f9dfdad550e1b3b95510fc84514d0b1`, followed by pushed `6df5bd6`. This packet does not change projection, gameplay, shipping artwork, the specification pin or prior evidence.

Implementation ownership is limited to this new directory. Original recovered source remains read-only. New phases remain PROPOSED pending visual review. Native/browser review belongs to the coordinator.

## Read-only feasibility observations

- Original editable workspace: the parameterized source root must contain `SS-player-bounded-proportions`, `SS-player-bounded-neutral`, and `SS-player-settle-prototype`.
- Existing runtime recipe: `docs/review/player-settle-prototype/build_source.py`, lines 6–14 (two-bone IK/foot construction), 23–44 (two-stage contact path and geometry guards), and 46–52 (unchanged-paint assembly adaptation).
- Recovered phase-05 and phase-13 samples exactly equal the corresponding frozen runtime pose JSON. All four recovered entry/neutral RGBA comparisons are exact.
- Actual contact metadata selects the support foot before considering toe height. When neither foot is planted, select the lower source toe. In particular, phases 7/8 select left and 15/16 select right, unlike a hardcoded half-cycle split.
- Preliminary calculations of the inherited two-stage construction for all 16 phases find maximum hip-to-ankle reach 26.516910336699222, under the existing strict 27-unit sum of 12.5/14.5 segment lengths. Maximum knee-minus-hip height is -2.849415335891731. These are feasibility facts, not visual acceptance thresholds.
- Existing offline interpreter `/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python` has NumPy 2.4.6 and Pillow 12.3.0. Local ffmpeg exists. No dependency installation or external service is needed.

## Review entry points and measured result

- `artifacts/normal-speed.html` and separate `artifacts/quarter-speed.html`: all 16 phases, full-size 384×416 source frames, pause/manual pose controls, and per-phase contact-plate links.
- `artifacts/normal-speed.mp4` and `artifacts/quarter-speed.mp4`: encoded source-only all-phase grid, 147 frames each at 128 and 32 fps. All 294 integer presentation timestamps exactly match their rational clocks. Neutral starts 0.375 and 1.5 seconds after release respectively. These are generated comparisons, not actual live cadence.
- `artifacts/phase-NN/frames/00.png` through `16.png`: 272 RGBA frames, 238 new and 34 byte-preserved 5/13 frames. Each phase has 17 distinct RGBA poses. `samples.json` contains the editable source coordinates. The original 5/13 source JSON bytes are also preserved.
- `artifacts/phase-NN/contact-plate.png`: 16 contact plates showing poses 0, 1, 8, 9, 15 and 16 with exact timing/contact labels.
- `artifacts/manifest.json`, `geometry-contact-checks.json`, `input-inventory.json` and `audit.json`: machine-readable provenance, measurements and checks.

All 32 entry/neutral pixel comparisons pass exactly. All 1,012 files in the three original source trees match their pre-build SHA-256 inventory. Across 544 leg/pose records: upper length is 12.499999999999996–12.500000000000004, lower length 14.499999999999995–14.500000000000007, hip/ankle reach 16.769474534517247–26.516910336699222, minimum toe/heel heights are both 0, and maximum knee-minus-hip height is -2.849415335891731. Maximum contact-interval toe drift is exactly 0, with no simultaneous horizontal movement of both toes.

Additional observations, not acceptance thresholds: knee interior angles span 76.3925670148764–158.22999164431022 degrees, maximum adjacent knee displacement is 2.4374536877849438 source units, and maximum first-hold support-toe drop is 0.48522630501013897 units. In particular, phases 7/15 deserve visual inspection of the larger landing drop.

Validation: 26/26 portable source regressions, 31/31 full source/artifact regressions, and 5/5 existing `ClipTimingTests` using `swift test --skip-build --filter ClipTimingTests`. Both HTML files have 16 ordered phase cards, 53 existing file references each and syntax-checked inline JavaScript. This is not browser execution. Logs are `portable-source-tests.log`, `artifact-tests.log`, and `swift-clip-timing-tests.log`.

## Deliverable boundaries

A parameterized, offline CLI, original-input hash inventory, new per-phase source JSON and RGBA frames, contact/geometry facts, and meaningful geometry/contact/order/endpoint regression tests. Preserve original 5/13 source and frame bytes. Use 17 poses with 3/128-second holds and the neutral pose beginning at 48/128 = 0.375 seconds. Historical source timing fields in preserved 5/13 must not be rewritten. Playback timing belongs in an explicit separate manifest.

Publish normal and separate quarter-speed source-only review and per-phase/contact plates only after all geometry, contact and exact endpoint checks pass. Generated frames never establish actual live cadence, SpriteKit behavior, natural motion, full-sole contact or visual acceptance. Failed checks remain failures, with one diagnosed retry and no lowered guard.

## Reproduce offline

Use an existing Python environment containing NumPy and Pillow, plus local ffmpeg/ffprobe. The run here uses NumPy 2.4.6 and Pillow 12.3.0. No service or dependency installation is part of these commands. Choose a fresh output directory outside the source root. Run from this packet directory:

```bash
PY=/path/to/existing/python
SOURCE=/path/to/recovered/outputs
OUT=/path/to/fresh/player-release-artifacts
PYTHONDONTWRITEBYTECODE=1 "$PY" test_source.py --source-root "$SOURCE"
PYTHONDONTWRITEBYTECODE=1 "$PY" build_source.py --source-root "$SOURCE" --output "$OUT" --jobs 4
PYTHONDONTWRITEBYTECODE=1 "$PY" test_source.py --source-root "$SOURCE" --artifacts "$OUT"
PYTHONDONTWRITEBYTECODE=1 "$PY" export_review.py --artifacts "$OUT"
PYTHONDONTWRITEBYTECODE=1 "$PY" audit.py --source-root "$SOURCE" --artifacts "$OUT"
```

The original rig, paint, boot geometry, material recipes and all input files are inventoried by relative-path SHA-256 before and after generation. Temporary source/boot assemblies live under the output's `.work/`, never under the originals. Existing recipe patch anchors are checked exactly and fail closed if upstream assembly changes. The generator refuses to overwrite a completed output directory or overlap the input root.

If a tool execution cap interrupts a build, rerun the same build command with `--resume`. Completed checkpoints must validate the source masters, recipes, source samples, exact assembly adaptation and all 17 ordered distinct RGBA frame records before reuse. Incomplete phase directories are preserved separately and only those phases rerender. Final geometry/contact/endpoint/inventory guards are never bypassed. See `execution.md` for the actual capped invocation and successful 126.9-second bounded continuation.

### Portable source checks

```bash
PYTHONDONTWRITEBYTECODE=1 "$PY" test_source.py --source-root fixtures
```

`fixtures/` is an exact, small, hash-checked subset of the recovered source samples and assembly template, copied by `prepare_fixtures.py`. It is not a synthetic replacement or a full render master. Its provenance lists every source-relative path and hash. These 26 portable tests cover geometry, actual support selection, contacts, ordering, timing, endpoint mutation rejection and preservation. Full rendering, actual endpoint artifact comparisons and the 1,012-file input audit still require the complete original source root.

## Portable artifact and native-asset checks

The follow-up fixes only review readiness and validation. No source frames or source poses were regenerated. `verify_artifacts.py` needs Python and Pillow, not NumPy, original masters or a browser. It verifies the exact 272-file family, phase/pose order, file and decoded-RGBA hashes, exact timing, canonical paths, five fixture provenance hashes, archived endpoint hashes and all 34 preserved 5/13 frame hashes. Archived provenance is not described as freshly reopening the original source trees.

Run from the runtime repository root with the existing local environment used for this packet:

```bash
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
PACKET=docs/review/player-all-release-source-20261116
PYTHONDONTWRITEBYTECODE=1 "$PY" "$PACKET/verify_artifacts.py"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$PACKET/verify_artifacts.py" --native-assets AppTests/BenchmarkAssets
PYTHONDONTWRITEBYTECODE=1 "$PY" "$PACKET/test_artifact_verifier.py"
node "$PACKET/test_readiness.js"
```

The Python path can be replaced by any existing Pillow-enabled interpreter. `--artifacts` and `--fixtures` can override the portable packet locations. When supplied, `--native-assets` must exist and contain exactly the 210 expected `player-allrelease-*` intermediate PNGs for the 14 proposed phases. Each intermediate must match source bytes exactly. The 28 movement-entry/neutral endpoint comparisons require decoded RGBA equality, not identical PNG metadata. Missing paths, extras, mismatches and malformed manifests fail rather than skip. Without the option, the result explicitly reports `nativeAssets: null`, not a native pass.

Follow-up results: **20/20 portable verifier regressions**, **8/8 readiness regressions**, and the actual `AppTests/BenchmarkAssets` verification all pass. Results are in `artifact-verifier-tests.log`, `readiness-tests.log`, `portable-artifact-verification.json` and `portable-native-verification.json`. The source-only encoded PTS and original input audit were rerun after review regeneration and still pass.

Review readiness now uses cached-image `complete` plus 384×416 natural dimensions, with `onload`/`onerror` for pending images. It never awaits `decode()`. The pages expose `data-review-ready="true"`, enabled manual controls and an explicit ready message before requesting the first animation callback. The regression harness executes the actual generated script with RAF callbacks suppressed, covering cached success, delayed success, broken cached images and load errors at both speeds. This harness is not a browser or cadence claim. At 02:22 UTC the coordinator additionally reported successful real-Brave checks: normal ready with all 272 images and manual pose 16, quarter ready while hidden with all 272 images and manual pose 8. No live-cadence acceptance follows.

## Contact and timing semantics

Support selection is source-backed, not phase-hardcoded. Preserve any initial planted toe and its authored `contactWorld` offset while holding the stationary root. If airborne, land the actual lower toe at pose 1. Hold that toe's horizontal position through pose 8 while the other foot settles to neutral. Hold the other toe at neutral through pose 16 while the first foot makes the inherited 3-unit-lift step to neutral. No consecutive samples move both toes horizontally. Original 5/13 are never regenerated.

Contact intervals use zero-based pose indices and half-open timing intervals. A pose-1 through pose-8 contact occupies `[3/128, 27/128)` seconds. The other foot's pose-8 through pose-16 contact occupies `[24/128, 51/128)` within this source clip. Both feet overlap in contact at pose 8. Contact continues in the held neutral afterward, but this packet does not implement that runtime state. Planted-entry phases extend the first interval back to zero.

All 17 poses have 3/128-second holds. Pose 16 is the neutral and starts at 48/128 = 0.375 seconds. Total coverage including its first hold is 51/128 seconds, not 0.375 seconds. The review adds explicitly labeled entry and neutral pauses outside that sequence. Original 5/13 historical `settleSeconds` fields remain byte-preserved and are not used for playback.

Geometry checks cover authored sampled segment lengths, reachable hip/ankle targets, toe/heel ground clearance, knee-below-hip bounds and contact intervals. Knee angles, adjacent knee steps and entry-to-landing toe drop are numerical facts, not invented acceptance thresholds. Neither continuous swept clearance nor full-sole stability is established. Source paint/material/front-layer and faceted-geometry limitations are inherited unchanged.
