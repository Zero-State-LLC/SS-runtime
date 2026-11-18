# Quiet native source comparison gallery

Serve `index.html` over the coordinator's localhost/HTTPS server. WebCrypto and fetch require that route, not `file://`.

## Capture selection and acceptance boundary

The explicit capture selector defaults to **1040**, never to historical1030 or1020:

| Selection | Exact root | Required fixture version | Label after valid evidence loads |
| --- | --- | --- | --- |
| 1040 | `../native-capture-1040/` | `source-scene-continuation-004-depth-order` | corrected harness, owner acceptance not granted |
| 1030 | `../native-capture-1030/` | `source-scene-continuation-003-upright-census` | historical visual failure: issue248 |
| 1020 | `../native-capture-1020/` | `source-scene-continuation-002-three-zooms` | historical visual failure: issue247 |

Missing1040 displays pending/error with disabled comparison controls and no images. It NEVER falls back to1030 or1020. Changing capture immediately removes previous images, labels and evidence links. Unsupported selections, mismatched fixture versions and stale asynchronous loads cannot display another capture. Raw1020 and1030 packets are untouched. The1030 upright fix exposed background-building insertion-order occlusion over the kiosk, recorded as issue248. The1040 fixture is the final bounded depth-only correction, not new source aesthetic work or visual approval.

Each selected root supplies `source-scene-records.json`, `verification.json`, and eighteen PNGs named `source-scene-{control|candidate}-ordinary-z{100|125|140}{-native|-half|-grayscale}.png`. Evidence links update only after all checks pass. The unchanged full benchmark is `../../stone-painted-facade-20261116/inputs/benchmark.png`.

## Evidence and display checks

Before enabling controls the viewer checks exact status/version, one reported native test, six ordered captures, eighteen images, static one-frame source scope, false owner/device/animation acceptance flags, preparation/harness/executable bindings, ordinary HUD/control/field flags and unchanged authority. It hashes record bytes and every PNG, matches importer hashes, and checks native PNG dimensions. This is not independent re-execution or complete importer validation.

Zoom, paired/control/candidate, native/half and grayscale remain available after verification. Images display at704×326 or352×163 CSS logical pixels, independent of capture density. Narrow image viewports scroll without shrinking. Grayscale uses the existing full-density grayscale file at the selected logical size. The benchmark fits uniformly without cropping.

## Final depth-selector validation, November16 10:29UTC

```sh
python3 -W error docs/review/scene-source-assembly-20261116/gallery/test_gallery.py
node docs/review/scene-source-assembly-20261116/gallery/test_contract.js
node docs/review/scene-source-assembly-20261116/gallery/test_loader.js
```

- Eight HTML/CSS/path checks passed.
- Real historical1020 contract: six records, eighteen PNG hashes/dimensions,24 display selections and12 rejected mutations passed.
- Offline loader with DOM/network doubles: deliberately missing1040, historical-to-missing1040 switching, real1020 and1030 with issue247/248 labels, wrong-version substitution, invalid selector and stale-load isolation passed.
- Real1040 is absent and explicitly reported **PENDING, not certified**. Once its directory exists the same loader test checks actual records and all eighteen PNG hashes/dimensions, and fails on incomplete or invalid evidence. No historical packet is substituted.
- `tests-depth-selector.log` retains this run. Earlier logs remain historical evidence, not current capture approval.

**No browser run or visual acceptance is claimed.** DOM doubles are not browser rendering evidence. Only `gallery/` files changed. No source art, raw capture packets or production files were modified. No Swift/native run was launched, consistent with the coordinator's serialized native slot and existing unfiltered-Swift stop condition.
