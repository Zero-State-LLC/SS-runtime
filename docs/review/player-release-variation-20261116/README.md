# Player south release variation proposal

Owner direction at **2026-11-16 02:36:26 UTC**: add slight phase variation for more dynamic motion. This is a new isolated source proposal, not admission of that visual quality. Baseline `15be1316d3817604e751664d5167f1649db2fc6b` is immutable.

## Scope and current state

Only this packet is authored. Original inputs, the published all-release packet, App/AppTests/native evidence, spec pin and handoff are unchanged by this worker. Original releases05/13 are never regenerated. Publication is coordinator-owned. No external service, new worker or remote rendering was used.

Completed source-only proposal: **272 ordered RGBA frames**, comprising238 rendered frames and34 byte-preserved05/13 frames. All32 entry/neutral pixel comparisons and1,012 reopened original-file hashes pass. The14 new phases each differ from baseline in13 intermediate RGBA poses (2–7 and9–15),182 changed images total. Pose1 touchdown and pose8 transfer boundary remain fixed, as do all entry/neutral pixels. All seven two-phase render invocations completed in121.8–146.8s with no cap hit, generation failure or guard relaxation. See `execution.md` and `verification.json`.

## Source design and adaptation decision

ADAPT: baseline `build_source.py:103-131` supplies source trajectory structure. Reuse its existing `support_side`, `foot`, `solve`, `validate`, `render_phase`, `completed_work`, `endpoint_checks`, inventory and hashing APIs directly. Source paint/boot/assembly stays in that API, not copied into another rendering implementation. Its provenance in turn cites `player-settle-prototype/build_source.py:6-52` and the recovered bounded master. `baseline-lock.json` binds seven dependencies to bytes independently checked with `git show 15be131:<path>`. `artifacts/implementation.json` binds the new generator at preparation time. Any drift prevents checkpoint reuse and publication.

For each non-preserved phase:

- Choose the actual authored contact, otherwise the lower authored toe, using the unchanged fail-closed baseline selector.
- Let `stance = tanh((otherToeZ - supportToeZ)/8)` and `angle = 2π(phase-1)/16 + sideOffset`, where sideOffset is+0.25 for left support and−0.25 for right support.
- Set `scale = strength*(0.75+0.25*stance)`, transfer skew `a = 0.12*sin(angle)*scale`, recovery skew `−0.75*a`, and lift `3+0.25*cos(angle)*scale` source units.
- Replace only the two source progress easings with `smooth(t+a*t*(1-t))` and the support recovery arc coefficient with that phase's lift. No per-frame jitter, randomness, costume changes, mirrored assets, bitmap deformation or new body-paint warp.
- Hip/weight transfer and free-foot placement remain the first stage (poses1–8). Planted support stays fixed until pose8. The original support recovers during poses9–16 while the other contact stays fixed. The same authored world-contact offset is retained.
- Entry is copied exactly. All17 poses retain3/128s holds, neutral begins48/128s=0.375s. Preserved05/13 source files keep their historical internal timing fields; manifest timing is authoritative.

The proposed parameter domain is easing skew±0.12, lift3±0.25 and strength[0,1]. These are design choices, **not invented visual quality thresholds**. Actual new-phase transfer skews are−0.0961372485 through+0.0912638923. Actual lifts are2.8044860291 through3.2017288492 source units. Complete values are `artifacts/profiles.json`.

The easing composition is a polynomial and continuous with zero endpoint slope. With `g=t+a*t*(1-t)`, `g'=1+a*(1-2t)≥0.88` on[0,1], and `smooth'(g)=6g(1-g)≥0`. Thus no reversal or overshoot occurs over the continuous easing domain, not just the17 samples. This does **not** certify continuous swept geometry: the inherited limb/ground/contact checks operate on authored discrete poses.

Strength0 returns the exact baseline generator result, including byte-identical serialized source samples for all14 phases. The same renderer/recipe API is used. No separate zero-strength render is claimed as newly measured pixel evidence. Original05/13 bypass variation entirely and preserve source/PNG bytes.

## Reproduce without changing originals

Existing local environment used: Python with NumPy+Pillow at `/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python`. Node runs the browser-code harness. ffmpeg/ffprobe are local `/opt/homebrew/bin` binaries. No installation or service needed.

From repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
P=docs/review/player-release-variation-20261116
SOURCE=/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs

# Portable source regression, existing exact fixtures in immutable baseline packet.
"$PY" "$P/test_variation.py"

# Reproduce into a new directory within this owned packet.
OUT="$P/reproduction"
"$PY" "$P/variation.py" prepare --source-root "$SOURCE" --output "$OUT"
# Each command is independently bounded to two phases. Do not launch one monolithic job.
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 1 2
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 3 4
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 6 7
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 8 9
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 10 11
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 12 14
"$PY" "$P/variation.py" batch --source-root "$SOURCE" --output "$OUT" --phases 15 16
"$PY" "$P/variation.py" publish --source-root "$SOURCE" --output "$OUT"
"$PY" "$P/export_comparison.py" --source-root "$SOURCE" --output "$OUT"
```

Each of the first four batches was launched with a240s execution cap. At02:47:33 UTC the coordinator explicitly allowed two disjoint two-phase batches concurrently (four rendering processes), with each task under five minutes. Later batches use a300s cap. No invocation contains more than two phases. A repeated completed batch verifies source samples, copied masters, boot/material/assembly recipes, frame order, all17 distinct decoded RGBA hashes and exact endpoint pixels before reuse. Incomplete checkpoints are rejected, never silently overwritten. Keep interrupted work for diagnosis. Source root is parameterized, must not overlap output, and all1,012 original input hashes are checked before/after each batch. The final manifest appears only after every phase passes. These paths can be served by the coordinator's existing local review server.

## Verify delivered packet

```bash
export PYTHONDONTWRITEBYTECODE=1
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
P=docs/review/player-release-variation-20261116
"$PY" "$P/verify_packet.py"
# Optional: reopen all original masters, rehash1,012 files.
"$PY" "$P/verify_packet.py" --source-root /Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs
"$PY" "$P/test_variation.py"
"$PY" "$P/test_artifacts.py"
node "$P/test_comparison.js"
# Local-only checkpoint regressions require rendered private .work and original masters.
"$PY" "$P/test_checkpoints.py" --source-root /Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs
swift test --skip-build --filter ClipTimingTests
```

Portable verification never reopens original masters: it verifies baseline sample/frame hashes before comparison, requires exact variation identity, owner timestamp and native-false status, binds all1,012 original inventory records to immutable baseline provenance, verifies272 ordered PNG hashes/decoded RGBA,32 original entry/neutral endpoints,34 preserved05/13 hashes, exact timing, deterministic regenerated source trajectories and544 geometry records. It also requires measured pixel differences in each of the14 new phases and none in05/13 or endpoints. Full original-root checks happen during prepare/batches/publication and `export_comparison.py`'s inherited audit. No native-assets option is supplied because existing baseline native captures are **historical baseline only**, not variation evidence.

Reviews: `artifacts/normal-speed.html` and separate `quarter-speed.html` show selected-phase baseline/candidate with one shared phase/pose/time state. They preload544 source images and expose manual readiness with complete/natural dimensions plus load/error events before requesting animation. They do not wait for decode or a visible RAF callback. `normal-allphases.html` and `quarter-allphases.html` show all candidate phases. `contact-overview.png` plus16 full-resolution per-phase contact plates cover0,1,8,9,15,16. Encoded source videos use the inherited exact-PTS timeline. Gallery loops, entry holds and neutral holds are review scaffolding, never proof of live cadence.

## Verified results

- 19/19 portable source tests (`source-tests.log`): repeatability, exact zero-variation baseline serialization, phase/stance specificity, continuous monotone easing/domain limits, timing, contacts, limbs, input preservation and tamper rejection.
- 22/22 actual-artifact tests (`artifact-tests.log`):272 files/order/hashes, baseline sample provenance, whole original inventory, exact variation identity/owner/native-false, no baseline relabeling, preserved5/13, endpoint origin, geometry/profile/source tampering and lifted status.
- 7/7 local checkpoint tests (`checkpoint-tests.log`), plus actual validated pair reuse in `checkpoint-reuse.log`. No source rerender on reuse.
- 8/8 comparison-code harness cases (`comparison-tests.log`): both speeds, cached/delayed images and two error paths, no decode/RAF dependency, all272 phase/pose selections synchronized. This is not a real-browser or live-cadence test.
- 5/5 existing ClipTimingTests (`swift-timing-tests.log`). No full-suite claim.
- 2 encoded source movies,147 exact integer presentation timestamps each at timebase1/16384, normal128fps/quarter32fps. Neutral after release0.375s/1.5s. `artifacts/audit.json` records the measured checks.

Numerical observations across544 leg/pose records, not new acceptance thresholds:

| Observation | Measured value |
|---|---:|
| Reach range |16.7694745345–26.5169103367 source units|
| Maximum upper/lower length error |5.3291e-15 /7.1054e-15|
| Minimum sampled toe/heel height |0 /0|
| Maximum knee-minus-hip height |−2.8494153359|
| Maximum adjacent knee step |2.4374536878|
| Maximum baseline-to-variation hip/knee/toe displacement |0.0520160218 /0.2919123091 /0.4537660209|
| Maximum planted toe drift |0|
| Simultaneous horizontal movement of both toes |none|

`artifacts/comparison.json` records per-phase coordinate differences and changed pixel poses. `artifacts/geometry-contact-checks.json` records all measured rows and exact contact intervals. Original airborne entry touchdown is retained, not hidden by new easing. No native variation was captured.

## Limits and review gate

All new variation phases remain **PROPOSED**, pending owner visual review. Coordinator source/browser checks are recorded in [coordinator-review.md](coordinator-review.md); no new native variation was captured. Sampled toe/heel clearance is not full-sole or continuous collision certification. Numerical knee/limb/contact observations are not visual acceptance. Lower-foot switches and inherited airborne entry touchdown, notably phases07/15, remain explicit review concerns. No new native capture, shared-scene, physical-device, live cadence, shipping behavior or gameplay claim is made.

The bounded Swift invocation is the permitted local timing check. The repository's twice-capped unfiltered suite is not restarted and is not claimed complete. Its XCTest shim reports0 tests before Swift Testing actually executes5 ClipTimingTests, recorded in `swift-timing-tests.log`.
