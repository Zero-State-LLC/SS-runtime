# Canonical identity02, runtime#245

**Corrected second preview, source-only, awaiting coordinator review.** Coordinator09:47UTC directed that canonical original-neutral identity takes precedence over the inherited baggy upper composition. This is an exact source-compositing repair, not a new aesthetic approach or a tolerance waiver. BP-002/007/012, T1045 remain the source-work context.

First pilot and all34original packet files remain byte-identical, including its renderer, source copies, strict tests, exported preview and red log. `pilot01-immutable-inventory.json` and `preservation.log` record that audit. This entire derivative is isolated under `canonical-identity-02/`; nothing outside the assigned Player packet was edited. No source originals, shared handoff, CI, Swift, production, commit or push changes.

## Explicit source-authority rule

`identity-policy.json` pins the canonical original frame SHA256 `2076f61c8d3b92a49d842f16eb6a043662dda84953f549a77884344cc3f1cb8e` and both the explicit ownership mask and derivative.

The mask is derived from source ownership, never from final-image difference selection:

1. All pixels with positive alpha in the exact copied upper source layer.
2. Union positive-alpha canonical original pixels above row200, where garment panels have not yet begun.

This declares22,664owned pixels. `canonical-upper-derivative.png` contains exact original-frame RGBA at those pixels and zero outside. `render.py` assigns all four channels directly at owned pixels after rendering the unchanged garment panels. It does **not** alpha-composite the derivative. Thus original alpha254 remains254 rather than being forced back to255 by accumulated alpha-over. The two earlier diagnostic coordinates(125,119)/(123,124) now exactly match original RGBA.

The new whole-image requirement is precise:

- **Inside declared ownership:** every output RGBA byte equals the canonical original.
- **Outside declared ownership:** every output RGBA byte equals the tracked baggy target in the neutral pilot.
- The actual complete image must equal this independently predicted composition.
- The exact changed-pixel mask must equal `ownership AND(original != baggy)`. No blanket tolerance or unconstrained changed region is allowed.

Result:198pixels changed, all inside ownership. These comprise the157reported pixels above y200 plus41lower upper-source edge pixels. Nothing outside ownership changes. Output SHA256: `b32bfcba5ac7cee383715d5f0b918e53b2e7be56634886754ab82357431d6ed4`.

## Preserved editability and limits

`garment_renderer.py` is an exact copy of pilot01's source renderer, not another knee-shell attempt. `garment.json` retains the same140editable front-panel vertices,192triangles, independent per-vertex UV coordinates, material ownership and ground root(192,336). Source component images are exact copies, with original git commit/path/hash provenance in `source-provenance.json`. Only explicit identity policy/status fields were added to the model.

Actual geometry/UV mutation tests still alter the garment and preserve unrelated parts. Canonical upper ownership remains protected. There is still no recovered hidden texture, rear/side cloth, volume, animation, scene capture or family expansion. No repainting, imagegen or other paid service was used for this exact-byte repair.

## Tests and portable replay

```sh
P=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
D=docs/review/player-garment-correspondence-20261116/canonical-identity-02
"$P" -B "$D/render.py"
"$P" -B -W error::ResourceWarning "$D/test_correction.py"
"$P" -B "$D/verify_preservation.py" --pilot-root docs/review/player-garment-correspondence-20261116
```

All16tests passed in0.968s on Python3.11.15 (`tests.log`). A separate standalone copy with no repository siblings passed all16again in1.272s (`standalone-tests.log`). The core replay also succeeds with both the flattened baggy target and pilot01 comparison removed. Canonical original-frame input is required only for its declared identity ownership, not garment material recovery. Full exporter replay compares corrected PNG, comparison PNG/SVG and build metadata bytes exactly.

The original `test_identity_upper_bytes` method is inherited unchanged from the exact retained test file and now passes. Boot/contact, alpha sampling, geometry/UV mutations and unknown-version/degenerate-triangle tests are also inherited unchanged. The former whole-target equality test is explicitly replaced by the stricter two-authority composition rule above. Source ownership support now explicitly includes the canonical mask.

New tests prove the original pilot still exactly matches the old baggy target and still fails the **actual original strict identity assertion**. This is a negative-control regression, not marking the current identity requirement as expected-failure. Other tests reject mask or derivative mutations even when their file hashes are updated, verify all partial-alpha bytes, demonstrate alpha-over would fail, and preserve exact native/half SVG aspect.

`prepare.py` is a one-time provenance/derivative constructor and refuses to overwrite an existing policy. Ordinary replay uses the fully self-contained copies here. `verify_preservation.py` separately requires a real original-pilot path and fails if it is missing, rather than falsely reporting external originals unchanged.

## Corrected preview and real gallery check

The corrected second preview was reported09:49UTC before further work. `comparison.png` retains source-size original/pilot01/corrected views. `comparison.svg` supplies exact fractional native64x69.333333 and half32x34.666667 image dimensions. `index.html` uses intrinsic384:416 aspect with height:auto, never64x69 or32x35 distortion.

Actual Brave verification09:50UTC loaded all9images. Source size measured384x416. Browser layout quantized native to64x69.328125 and half to32x34.6640625 CSS pixels, consistent with fractional layout rounding rather than manually changed aspect. No page horizontal overflow. All9images switched to grayscale(1) and restored to none, checkbox off. `browser-evidence.json` records these actual values. Earlier undefined bridge results were resolved by an explicit script return, without switching services. This is browser-gallery evidence, not a native application capture or visual acceptance.

Worker inspection of the actual corrected comparison finds the baggy silhouette, patch proportions and boots unchanged. Canonical edge-byte restoration is too small to establish a new aesthetic verdict. Coordinator review is still required. No third visual attempt or family/scene admission is inferred from the green correction tests.
