# Final bounded source correction validation

November16,2026 local / November17 00:03UTC. BP-001/007/012,T1045.

## Scope and preserved evidence

Exactly one material correction authorized by `../../SOURCE-REVIEW-01.md`. All99frozen first-attempt files, including complete source snapshot, original manifest and rejected previews, match their recorded hashes. All194baseline/provenance dependencies match. The original geometry remains byte-identical. Every non-image field of all53registrations and every source alpha array remains identical to attempt01. Heights18/3, roots, contacts, bounds, source canvas/anchor/draw size, semantic18,880curb pixels and prop clearance are unchanged.

Material-only edits are in `materials.json` and `replay.py`: broad36world staggered masonry courses, retained plain stone crop and lighter/desaturated low-contrast mineral curb. Exact adaptation and UV sampler transform are documented in `ADAPT.md`. No ground or existing actor edits.

## Commands observed

From `source/attempt-02/`:

- `PYTHONDONTWRITEBYTECODE=1 python3 author.py`: froze original source and authored separate correction controls.
- `PYTHONDONTWRITEBYTECODE=1 python3 replay.py --out output`: rendered sole correction,53sources.
- `PYTHONDONTWRITEBYTECODE=1 python3 preview.py`: generated final3zoom full/half/grayscale contexts, detailed base/curb and full uncropped benchmark comparison.
- `PYTHONDONTWRITEBYTECODE=1 python3 freeze.py`: froze81final source files, manifest SHA256 `5b0943d029eadaf00d4e2d039dbeeda3e3353241c7881f28dd370c3295ab1891`.
- `PYTHONDONTWRITEBYTECODE=1 python3 test_source.py`: **13tests PASS**,12.664seconds. Includes19mutation cases and full source plus full preview byte-identical replay. Log `tests-final.log` SHA256 `db83d3c85e21e548857f4fc659c627d641410874ced8a131b00839e140e35b63`.
- `PYTHONDONTWRITEBYTECODE=1 python3 ../test_source.py`: **25preserved first tests PASS**,2.277seconds, including first-source replay. Output in `tests-preserved-first.log`, not written over old log.
- Independent `verify_manifest()`: PASS,99firstfiles unchanged, geometry bytes identical and all53registrations/alpha identical.

A Pillow deprecation warning about `Image.getdata` is retained in the final log. It does not alter outputs or the passing replay result. No claim of future Pillow compatibility is made.

## Synthetic ordering evidence and honest remaining limitation

Final preview uses the retained portable world-footprint depth oracle over71items. Only registered alpha silhouettes of9known actors ranked in front may occlude relief. The preview records exact source hashes, all ordering constraints, actor roots/anchors/sizes, each sprite's occluders, raw/visible pixel counts and alpha hashes. No hand-painted hide mask. Nine legacy actor silhouettes remain unknown and are verified not to overlap any relief at all3zooms. Their actual mesh contacts are not invented.

With this honest retained ordering, the kiosk/stair sprite covers the upper part of the supplemental base. That result is intentionally displayed and reported, not repaired by a visibility boost. The source worker inspected the final detail and zoom1.4half preview for evidence coherence, not to issue a source recommendation. Coordinator received all final preview paths before tests finished. Final source API and exact hash were sent directly to the scene worker's full session identity.

No third art attempt is authorized or performed. Exact-hash source recommendation and visual/native verdict remain coordinator-only. No native/build, production change, historical overwrite, commit or push by this worker.

Trail context calls saved approximately73,242tokens this correction turn (tool estimates).
