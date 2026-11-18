# Final Camera padding correction

**Technical completeness correction only. No aesthetic retry or source acceptance.**

Final comparison: `final/comparison.png`. Final source: `final/camera-master.png`. Registration: `final/registration.json`. Original first painted preview, model, renderer, source audit and tests are preserved byte-for-byte in `control/`, with local raw inputs so its original tests remain executable. The parent preview and mapped-material pilot are unchanged.

## Authorized change

Per coordinator instruction November16,2026 at09:58 UTC:

- Source canvas `[180,450]` → **`[204,450]`**, adding12 source pixels on each horizontal side.
- Every layer origin translates **`[+12,0]`**.
- Source root `[46,427]` → **`[58,427]`**.
- All source crops, actual RGBA pixels, per-layer uniform scales, visibility, draw order, role descriptions and logical scale remain identical.

`author.py` records exactly those model edits. `replay.py` imports the **unchanged archived renderer** from `control/replay.py` and passes the corrected model plus packet-local inputs. It regenerates from original complete source layers, not by placing the clipped old composite in a bigger canvas. No recoloring, contour adjustment, smoothing, new shading, source redraw, UV change or nonuniform fitting.

## Actual completeness results

The first control still has maximum border alpha **215** and retains `antialiasPaddingSatisfied=false`. Its original failure regression remains intact.

The corrected master, all three transformed layers, native raster and half raster have **maximum outer-border alpha0**. The final test asserts this, rather than merely reporting a warning.

- **35 previously clipped left-fringe pixels restored**, total alpha57.
- **79,650 old pixels**, source columns3–179 across all450rows, are byte-identical after the integer+12X translation. This check also passes independently for every layer.
- Only old columns0–2 differ. Those columns were affected by the old canvas clipping the three-source-pixel LANCZOS filter support. Their changes restore that support, not new artwork.
- Exact original source-layer PNG bytes and all six raw input files remain unchanged.
- A negative test proves that merely pasting the old clipped image into a larger canvas is rejected because it does not restore the fringe.

`final/padding-evidence.json` records those observations. No prior failure evidence was overwritten or softened.

## Scene registration

Use the full source master, not a nonuniform fit of the rounded native preview:

| Field | Verified value |
|---|---|
| Source canvas | 204 × 450 |
| Root, top-left source pixels | `[58,427]` |
| Uniform logical/world draw scale | `96/418 = 0.22966507177033493` |
| Exact logical draw size | `[46.85167464114833,103.34928229665071]` |
| Sprite anchor, bottom-left normalized | `[0.28431372549019607,0.05111111111111111]` |
| Native preview raster | 47 × 104 |
| Half preview raster | 24 × 52 |
| Source SHA256 | `1343507b7517cd2a4848810b14aca88644677f35266ec8299dcbbf8347ef5ab1` |

The root-relative mapping is `worldDelta = (sourceX - 58, 427 - sourceY) × (96/418)`. Translating both source content and root by12X preserves the original mapping. Tests check representative local points on every component to12decimal places. No absolute world position, collision, field or gameplay truth is inferred. This is inherited review-source registration, not production admission.

The new path, hash, root, dimensions, exact logical size and anchor were sent to the scene worker and coordinator at10:01 UTC after tests passed.

## Replay and verification

Python3 plus existing Pillow only:

```sh
python3 -W error /path/to/padded-final/replay.py --out /path/to/new-replay
python3 -W error /path/to/padded-final/test_padding.py
python3 -W error /path/to/padded-final/test_control_supported.py
```

**Supported result after interpreter-metadata repair:15 padding tests passed on both Python3.14.7 (2.533seconds) and Python3.11.15 (2.359seconds)**, all warnings treated as errors. Logs: `tests-python3147.log` and `tests-python31115.log`. Each suite also executes all **12 control checks** through `test_control_supported.py`, which explicitly replaces only the archived interpreter-equality comparison. No skips. Original control tests and author manifests remain immutable. Coverage includes exact model delta, preserved red control, actual final border transparency, source-pixel and cropped-layer identity, restored fringe, unchanged root-relative mapping, registration/hash agreement, rejection of unauthorized shape/scale changes, and clean standalone replay.

Standalone copies reproduce **all15 final exports byte-for-byte**. Regenerated manifest `python` must exactly equal the running `sys.version.split()[0]`; every other field, including Pillow and all source/output hashes, must equal the retained author record. Both retained author manifests are separately SHA256-pinned in `manifest_compare.py`. Mutation guards reject false interpreter, changed Pillow/status/output hash map/acceptance fields, missing or additional fields, and altered author bytes. The15exports are12PNGs and3JSONrecords. No retained artwork, model, renderer or final manifest was regenerated for this test-only correction.

The original coordinator3.14.7 failure log and original test files are retained under `history/interpreter-metadata/`. The direct archived `control/test_assembly.py` is historical, with its original author-interpreter byte-equality assumption. Use the supported runner above for cross-interpreter validation. The earlier same-interpreter result remains in `tests.log`.

Exact supported coordinator commands:

```sh
/opt/homebrew/bin/python3 -W error docs/review/camera-raster-material-20261116/painted-assembly/padded-final/test_padding.py
/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python3.11 -W error docs/review/camera-raster-material-20261116/painted-assembly/padded-final/test_padding.py
```

Actual final comparison inspected at10:01 UTC. Wider generated base and native highlight stippling are unchanged visual observations. Three neutral editable raster layers remain three layers, not a sixteen-part/full3D source or inferred pan-frame family. Offline paving background is not a native scene capture. No new owner/source/production acceptance, commits, shared edits, CI changes or Swift runs. Stop after this verified technical correction.
