# BP-001 projection decision packet

Prepared November 16, 2026. **Owner choice UNRECORDED. No shipping mapping or art changes.**

Open [the offline gallery](index.html). It needs only this checkout, no server, account or network. Concept illustrations are separated from actual-renderer evidence. The existing 24 plates are reused rather than duplicating 31 MB: every byte matches fresh attachments exported from the successful November 15/16 full native Debug run.

## Decision requested

**Research update: keep the approved visual benchmark fixed and compare a faithful original-reference renderer candidate against midpoint before choosing.** The existing shipping control is not that missing candidate. The [decision research](research.md) supersedes the earlier recommendation to choose midpoint now and specifies the smallest discriminating trial, risks and primary sources. No trial is implemented or owner choice inferred.

- **A: shipping-ground control.** Current ground mapping, with the same candidate art as B. This is **not** a faithful numerical reconstruction of the approved original-reference concept's projection.
- **B: midpoint candidate.** Existing +45-degree ground rotation followed by half-height scaling, with upright actors and building art at projected roots.
- The two concept references are unchanged SS-specs illustrations, not runtime screenshots, geometry proof or a controlled same-art pair.

A response selecting midpoint authorizes recording that visual basis in SS-specs `decisions.md` under BP-001/D-108. It does not authorize shipping a partial transform. Alternatively, request a faithful original-reference renderer candidate before selecting. This packet does not pretend that the shipping control closes the original-reference-candidate requirement. No art-admission or parent production task is marked Done.

## What the comparison actually holds constant

| Property | Quiet street | Legal-input encounter |
|---|---|---|
| Renderer | Existing GameScene, SpriteKit and HUD | Same |
| Snapshot | Controlled modified street fixture | Unedited command-driven seed-1 Ghost Step snapshot |
| Camera/attack | Integrity-3 Camera, paired field | Tick 4976, seven enemies, eight Cameras, one projectile; fixture requires a nearby hostile projectile and live Camera field |
| Art | Same constrained building registration and upright candidates | Same production building art, `registerServiceBuilding: false`, same painted Player/municipal Camera candidates |
| Settings | Paired field treatment, normal motion | Paired field treatment, normal motion |
| Derivatives | Natural and magenta-solid/cyan-body overlay, each native/half/grayscale | Same |

Encounter digest remains `d96494f03b4ade6a6a6dc02961ffd1dc73c5e1f2a86a029ca6dcd22d207162f5`. Both treatments use one paused snapshot, not two separately staged encounters. Quiet fixture is composition evidence, not legal-play evidence. Cropping and apparent threat coverage differ under projection, which is part of this comparison, not a reason to remove actors.

## Provenance and limits

- Viewport **704×326 points**, display scale **3**, native **2112×978 pixels**, half sheet **1056×489 pixels**. Half means half of native pixels, not a newly measured physical phone display.
- Xcode 26.5 (17F42), iPhone 17 Pro Simulator, iOS 26.5 (23F77), Debug. Full xcresult reports 166 logical tests passed, zero failures/skips.
- Local result: `ss-receipt-v2-20261115/app-Debug.xcresult` under the host scratch directory. Attachments came from `BenchmarkCaptureTests/testCaptureCompleteCameraCandidatesInSharedScene()` and `BenchmarkCaptureTests/testCaptureCameraFieldsInReplayableEncounter()`.
- Runtime base `df8473713a3d37aeca05d4e1110f979f197b9ceb`, with a receipt-repair working-tree overlay at capture time. This is **not a clean capture commit**. Four exact capture-source SHA-256 hashes are recorded. These App/fixture files are unchanged between that base and receipt repair head `dcf073c0`.
- [Capture provenance](capture-provenance.json) records all 24 fresh attachment timestamps, source hashes, plate hashes and concept hashes. [Verification](verification.json) records successful fresh-byte comparisons. [Browser workflow evidence](browser-verification.json) records all six rendition/geometry combinations loading the expected images and dimensions.
- Source: `AppTests/BenchmarkCaptureTests.swift:777–852` for the legal-input pair, `:1023–1340` for the shared street pair, and the existing review projection helpers. No fixture, rendering code, gameplay, contract or input mapping changed for this packet.

**Unproved:** live eight-direction facing/input integration, movement and ground contact, front/rear/corner occlusion, moving attack visibility, dense encounter, physical device and final family admission. Midpoint world-south reads down-right. Screen-relative input needs the inverse mapping while preserving analog magnitude and authoritative world speed. Do not relabel a front-facing source as world-south or normalize away foreshortening.

## BP-011 palette findings

Method: existing `scripts/palette_conformance.py`, 8-bit sRGB, box downsample to width 300, non-linearized Rec.709 weighted luminance, max-minus-min chroma and nearest section-10 palette colour. Exclude **top 240 native pixel rows (80 viewport points)** from all four runtime natural plates, covering upper HUD/status labels. Lower translucent touch controls remain in every sample. Reference is uncropped. No Civic Plaza lightness allowance is applied. Overlays and grayscale derivatives are diagnostic views, not separate palette measurements.

| Plate | Mean luminance | Mean chroma | Proposed band |
|---|---:|---:|---|
| Approved concept reference | 85.2 | 11.4 | Reference |
| Quiet A | 126.8 | 25.2 | Both flagged |
| Quiet B | 127.2 | 25.7 | Both flagged |
| Encounter A | 94.4 | 12.8 | Within band |
| Encounter B | 99.3 | 16.0 | Within band |

The quiet street is lighter and more chromatic than the reference in **both** treatments. Projection does not resolve that palette drift. Flags request review, not rejection, and within-band is not owner acceptance. The full nearest-colour shares are in [the report](palette-report.json). Nearest-colour share is not semantic material segmentation.

## Repeat the checks

Requires Python 3 and Pillow, already used by the existing palette tool. From runtime root:

```sh
python3 scripts/verify_bp001_decision.py
python3 scripts/test_bp001_decision.py
# Optional: also compare fresh xcresult exports, each directory retaining manifest.json.
python3 scripts/verify_bp001_decision.py --capture-root "$JCODE_SCRATCH_DIR/ss-bp001-20261116"
```

Reproduce palette output:

```sh
python3 scripts/palette_conformance.py \
  docs/review/bp001-same-art-pair/BP001-quiet-street-current.png \
  docs/review/bp001-same-art-pair/BP001-quiet-street-midpoint.png \
  docs/review/bp001-same-art-pair/BP001-encounter-current.png \
  docs/review/bp001-same-art-pair/BP001-encounter-projected-100-same-art.png \
  --reference docs/review/bp001-decision-20261116/street-corner-approved-concept.png \
  --exclude-top 240
```

Recommended next authorization is the isolated faithful original-reference comparison trial described in [the research](research.md), without further family source detail. The owner projection record must precede the approved breadth-first family slices. Preserve the approved 0.375-second Player settle timing. Do not resume recorder/OBS work or create more source detail before that record.
