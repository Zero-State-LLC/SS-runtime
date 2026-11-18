# Camera surface-authored proposal, new method

## Current outcome, November16 09:00UTC

**Both changed-method surface previews are NOT RECOMMENDED. No third visual pass or scene integration.** Current final images are `index-final.html` and `attempt-02/comparison-color.png`; see `FINAL.md` and `COORDINATOR-REVIEW.md`. Supported portable verification is `python3 -B -W error::ResourceWarning test_final.py`. The final source archive contains all required input bytes. `test_source.py` and earlier archived entrypoints are historical checks with dependencies on the original local unpublished packets, not the supported portable verification route. They are preserved, not silently skipped or presented as clean-tree passing.

Coordinator corrected only replay-manifest environment comparison: retain the author manifest under a fixed SHA256, require a fresh replay to report its actual running Python version, and compare all other manifest fields exactly. Every other export remains byte-exact. False runtime version and non-environment hash/metadata mutations are explicitly rejected. Source/rendered pixels and prior attempt bytes are unchanged.

The following text describes the retained first proposal and its original review, not the current outcome.

Authorized by `intent/2026-11-16-source-to-scene-continuation.md`, owner approval November 16, 2026 08:19:29.555 UTC. Slice 2, BP-001 through BP-012 / T1045. Only this new directory is changed by this worker. No commits/push, production/shared/runtime/native/state/clip work or source acceptance.

## Start with actual images

Open `index.html` or `attempt-01/comparison-color.png`. The plate compares the **unchanged benchmark**, prior rejected procedural attempt 02, and the new source at equal source scale, plus actual native/half views. First new-method image was sent to the coordinator at 08:25:43 UTC before paperwork. The initially deficient build is retained as `attempt-01-initial/`, with its actual source and images.

**Worker visual assessment, not an acceptance:** the bracket now has a curved fillet, separately painted thickness/underside and cylindrical neck. The hood contour is shallower/narrower. Finial, pole and base have individually authored surfaces rather than a shared extrusion shader. However, the result still looks too clean, green and hard-edged compared with the weathered charcoal/cream benchmark. Finished fidelity is not established. Coordinator verdict is requested before spending another visual iteration or expanding scope.

This is the **first visual proposal of the changed method**, with a separately preserved technical repair of its clipped hood shadow. No second artistic revision has been undertaken. At most two failed visual attempts of this method are allowed.

## What genuinely changed

`surfaces.py` directly authors 16 complete closed parts and **90 individually named paint surfaces**. Each surface has editable contour/stroke geometry, color, stroke width and opacity. These are explicit paths with authored coordinates, not procedural noise, randomized weathering, shared spatial color ramps or a recolored old raster. Every named surface exports separately under `attempt-01/layers/`, alongside complete underpaint and component images. There are 122 RGBA layer images in this attempt.

The renderer performs ordinary cubic-path rasterization, clipping, alpha composition and fixed supersampling. Its contour sampler is adapted from `docs/review/camera-editable-master-20261116/build.py:18-53`; the old procedural material generator and all old raster pixels are excluded from `render()`. Prior raster artwork enters the comparison board only. `camera-surfaces.svg` exposes named geometry and paint paths without an embedded image. SVG rasterization is an inspection convenience, not claimed pixel-identical to Pillow.

The installed `~/.claude/skills/create-game-assets/SKILL.md` and `references/art-direction.md` were read directly after the registered skill loader could not find that installed skill. Applied constraints: unchanged benchmark identity, ordinary narrow pole silhouette, charcoal iron/cream enamel/black glass/tiny cyan roles, upper-left light, thin broken edges and restrained detail. No generation provider, new dependency or paid service was used.

## Geometry, hidden paint and scale

Ground root is authored **(46,427)** on a **180×450** canvas. It is not inferred from alpha bounds, collision or Camera field data. Other landmarks are explicitly reauthored for this geometry in `surfaces.py`, and are not presented as measurements of the original benchmark. Complete pole continues beneath collars/bracket, dome beneath hood, foot beneath plinth and hood beneath neck. Five actual overlaps and a collar-removal render are checked. The neck overlap falls on an antialiased edge: over-alpha is 252 in the first proposal, while authored underpaint is 255. No claim of fully authored future damage/animation surfaces follows.

Uniform x/y scaling is **96/418**, retaining the previous 96 nominal design-height convention. Transparent canvas padding produces **42×104** pixels at native source-preview scale and **21×52** at half. Native here means source inspection size, not an executed SpriteKit capture. No new world registration or zoom choice is made.

## Rebuild and verification

Pin the interpreter explicitly because this machine's background-shell PATH selected a different installed Python:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 docs/review/camera-surface-authored-20261116/build.py
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 -W error docs/review/camera-surface-authored-20261116/test_source.py
```

The complete renderer/source is archived in `attempt-01/source/`. Rebuild it to a **new output directory** with its own `build.py --source .../surfaces.py --output ...`; no top-level mutable source dependency is needed. Hashes and observed interpreter/Pillow versions are recorded in `attempt-01/manifest.json`.

Actual corrected result: **12 tests passed in 14.436 seconds**, retained in `attempt-01-tests.log`. Tests verify full archived-CLI byte rebuild including source, layers, SVG, comparisons and manifest; pinned original benchmark hash; both old attempt manifests and every listed artifact unchanged; real alpha and zero RGB beneath zero alpha for every layer/output; all 90 surfaces nonempty; five hidden-underpaint overlaps; missing-underpaint negative; actual collar removal; one named paint edit that changes pixels but no geometry/alpha/root; source render forbidden from reading raster images; exact uniform native/half transforms; named SVG/census coverage; unchanged reference-window pixels; exact grayscale conversion. Technical checks do not score or override visual quality.

Actual Brave verification at **08:30:38 UTC**: all 3 canonical PNGs loaded, 890×550 plate, 42×104 native and 21×52 half, no horizontal overflow. All 16 component controls and 90 surface controls hid/restored correctly. One actual surface color/opacity change preserved its geometry, then reset restored source values. Grayscale and ground-root controls restored. Existing browser handoff service returned HTTP401, so the existing browser bridge completed checks directly, without credential changes or paid-provider substitution.

## Honest first failure and repair

`attempt-01-initial-tests.log` is retained with **two failures**, not overwritten:

1. Exact manifest rebuild found Python 3.14.5 versus 3.14.7 metadata. Foreground and background PATHs selected different installed interpreters. Explicit `/usr/local/bin/python3` aligned build and validation. No comparison assertion was removed.
2. `hood--rim_under_shadow.png` was fully transparent because its authored path lay outside the hood contour. The source shadow path was corrected into the actual hood lip. The first source/images remain in `attempt-01-initial/`. The nonempty-layer assertion is unchanged.

This was an implementation/command repair, not a test weakening or a claimed visual success. No repeated unfiltered Swift suite was run, per the standing stop and assigned source-only scope.

## Immutable authority and handoff gate

Original benchmark SHA-256: `49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb`.

Old procedural attempt manifests were pinned before this lane and remain verified:

- attempt 01: `0097c829d1dee2d0dd0b98c5b0f126ac40cce6e7c4c015f3a762144176a65dde`
- attempt 02: `eee5365461132b98a7badf2cbf74e9ee4a4530345b2982c44cf0e56d8525dc59`

Coordinator must give the actual visual verdict before further expansion. No source recommendation, owner acceptance or production admission is inferred from this technically verified implementation.
