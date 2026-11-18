# V9 supplemental source API, first attempt

Status: pending coordinator recommendation. BP-001/007/012, T1045.

`manifest.json`: schema `blocked-base-curb-source-009`, attempt 1, status `FIRST_PREVIEW_PENDING_COORDINATOR`, `files` map of source-relative path to SHA256, `baselineFiles` map of repo-relative immutable V8 inputs to SHA256, `sprites` array.

Each sprite: `id`, `kind` (`blocked-base` or `curb-relief`), `image` {path, sha256} (path repository-relative), `registration` {canvasPixels, rootPixelsTopLeft, worldPosition, drawSizeWorld}, `pixelsPerWorldUnit` (4), `contactWorldXYZ` (ordered actual z0 contact polygon), `heightWorld`, `worldBoundsXYZ` {min,max}, `geometryLandmarks` [{worldXYZ, sourcePixelsTopLeft}], `geometryFile` (source-relative `geometry.json`), `geometryID`. Images are upright RGBA, preprojected at fixed D108: u=(x-y)/sqrt(2), v=(x+y)/(2sqrt(2))+z. Root is actual ground-contact centroid. Anchor=(rootU/width,1-rootV/height), draw size=canvas/4. No lift of ground textures or depth boost. Use retained geometry-depth ordering with root/footprint witnesses, not an overlay maximum zPosition. Extra nodes are supplemental presentation, not part of 18 actor census.

`geometry.json`: schema `blocked-base-curb-geometry-009`, `sprites` with id/kind/worldPosition/contactLocal/heightWorld/faces. Faces are explicit local XYZ vertices, normal, UV, material. Base is exact chamfer triangle [512,640],[551,640],[512,679], solid masonry height 18, entirely within blocked envelope. Curbs are small rectangular extrusions height 3, derived from existing semantic-ID=2 pixels (no boundary movement). Material/source provenance is in `ADAPT.md` and `materials.json`.

`replay.py --out DIR` deterministically regenerates sprites and registration without modifying prior outputs. `test_source.py` exposes `validate(geometry, registrations=None)` plus `verify_manifest(path=HERE/'manifest.json', replay=False)` for scene binding. Scene must independently require a coordinator-authored exact-hash recommendation. This worker never emits a recommendation.

First preview uses actual retained V8 candidate native images as context with registered source overlays, explicitly synthetic and not native depth proof. Three zooms, detail and full uncropped benchmark. All generated first-attempt outputs live under `attempt-01/`, immutable after generation. No second aesthetic pass without bounded coordinator instruction.
