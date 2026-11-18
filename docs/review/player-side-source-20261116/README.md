# East/west neutral first source samples, PROPOSED

Slice 4 of the owner-approved ten-slice plan (2026-11-16 03:10:28 UTC). Contract IDs: BP-002, BP-007, BP-012, T1045. These are first samples only. No four-facing fidelity, native/simulator capture, animation, production or admission is claimed.

## Deliverables

- `east/east-neutral.png`, `west/west-neutral.png`: 384 x 416 RGBA.
- `east/layers/`, `west/layers/`: 13 editable full-canvas layers each, listed bottom to top in the extension JSON.
- `east/components/`, `west/components/`: exact RGBA crops from the generated sheets.
- `east/east-extension.json`, `west/west-extension.json`: bindings, transforms, hashes and provenance.
- `four-facing-source.png`, `-native.png` (64 x 69 each), `-half.png` (32 x 35 each), `-grayscale.png`: comparison strip, not a finished family. Panels left to right: historical original south (unchanged, slim legs, not the baggy-south proposal), proposed east, proposed active north, proposed west.
- `index.html`: gallery of the views above.

## Method

`assemble.py` crops each authored extraction region of a generated component sheet to its actual alpha bounds. It saves those crops byte-for-byte, scales each one uniformly by 0.4 (the same as the active north sample) and places it with a hand-authored translation. It does no mirroring, rotation, warping, repainting or threshold cleanup. The flat assembled guide on each sheet was only looked at, never composited. I first tried automatic template matching to place parts. It misregistered them badly, so I discarded it.

Three west joins and one east join touch through thin opaque bridges rather than alpha gaps. Each is separated by a straight authored cut row, listed in `cutSplits`.

## Anatomy and equipment

- East faces screen right with anatomical right near. West faces screen left with anatomical left near. In both, near limbs draw over far limbs.
- East and west come from two different generated sheets. No component hash is shared, and neither image is a mirror of the other.
- The satchel binds to `right_hip` in both. The thigh with the cloth patch is anatomical left, matching the south.
- The trousers keep the baggy volume the owner prefers.

## Provenance

- East sheet: `1794799249061-ig_07cd661172aa2162016afa765bdbe887d0b785d913c0ab2a20.png`.
- West sheet: `1794799386977-ig_07cd661172aa2162016afa76e6fc2087d0a633b2f0fce6aa30.png`. Its boots were repaired by the coordinator to face screen left.

Copies and metadata are in `source/`. All side paint, including hidden surfaces, is native-image-generation output from the coordinator. It is not original master paint. Read-only inputs: the original south frame, the original `body-rig.json` and the active north (`0a6e15bd…4fbb`). Their hashes are in `inputs.json`.

## Verification

The packet is portable. `source/` holds the seven immutable inputs: the original south, the original rig, the active north, and both generated sheets with their metadata. `assemble.py` reads only those copies and refuses to build if any differs from the SHA-256 hard-coded in `PINNED`. External originals are provenance only. `--refresh-from-originals` re-copies them after checking the same pins.

```sh
P=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
$P -B -W error::ResourceWarning assemble.py
$P -B -W error::ResourceWarning test_source.py
# optional, in the original workspace only: external originals still match the pins
SIDE_FULL_AUDIT=1 $P -B -W error::ResourceWarning test_source.py
```

Nine portable guards cover:

- a rebuild that reproduces pinned output hashes `4be91d1d…` (east) and `9d06aa54…` (west);
- pinned input and local-copy hashes;
- exact component RGBA identity and uniform 0.4 transforms;
- 13 unique layers that recompose each output exactly;
- distinct, non-mirrored facings;
- near/far anatomical binding and draw order;
- hood-top and root registration;
- gallery strips matching the packet-local south and north;
- PROPOSED labels.

The tenth test is the optional external audit. It is skipped by default. It also fails in a relocated copy by design, because the relocated copy cannot reach the original workspace or the sibling north packet.

## Visual inspection and blockers

At source, native and grayscale size, both sides read as distinct side-on facings, with no floating limb or duplicated part. I did not check joint range, contacts or animation.

Open blockers before any four-facing fidelity claim:

1. **Satchel placement:** in the south, the satchel sits at the front of the right hip. The generated sides and the north put it at the back of the hip. In east the bag is on the near hip but draws behind the torso at the rear edge. Its depth is unresolved, so the tests do not assert it.
2. **Coat tails:** the generated tails are broad, flat panels. The near tails read larger and stiffer than the south coat.
3. **Camera elevation:** the side views look closer to eye level than the south's downward view. The elevated view is not proven.
4. **Placement:** translations are authored by hand, not measured from shared 3D anatomy. The rig bindings are semantic only.
5. **Boots:** shin and boot remain one part, with no separate boot or heel/toe control.
6. **Baggy south not integrated:** a separate baggy-south proposal is published in `docs/review/player-baggy-south-source-20261116/`. It is not integrated into this strip and not accepted. The strip's south is the historical original.

## Independent coordinator review, November16 04:35UTC

All10 checks passed with the optional external-original audit enabled. A fresh relocated copy passed9 checks and explicitly skipped only that external audit, with ResourceWarnings treated as errors. Actual Brave loaded all8 gallery images and preserved exact native256x69 and half128x35 strip dimensions. Wide source plates scroll within their sections, with no page horizontal overflow.

Visual inspection confirms that the satchel changes from front to rear hip and that coat/material and elevation differences remain unresolved. The gallery is explicitly a mixed-status comparison with historical original south, not a finished common four-facing family. Do not use these checks to authorize native family expansion, animation or admission.

Owner fidelity review remains required. This packet changes no production/runtime behavior and grants no animation or admission permission.
