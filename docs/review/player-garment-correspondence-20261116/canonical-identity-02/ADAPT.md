# ADAPT record for canonical identity02

Decision: COPY_EXACT the Player pilot01 renderer and regression implementation into a self-contained derivative, then compose canonical source-owned identity in a new wrapper. Authority: coordinator09:47UTC, runtime#245. No old inflated knee-shell source is imported.

| Destination | Exact source citation | SHA256 | Change |
| --- | --- | --- | --- |
| `garment_renderer.py` | `docs/review/player-garment-correspondence-20261116/render.py:1-113` | `1b87036da2ef2500bc4dda9932d130d5e6c7af292c0c87caf037d5806c707726` | None. Called by the new wrapper for front-mesh composition only. |
| `pilot01-test_correspondence.py` | `docs/review/player-garment-correspondence-20261116/test_correspondence.py:1-126` | `60ca72105cc68f947279b12baeb0878cbd5bed0f699daa3a9a2fa6218a8fade3` | None. Strict original identity method inherited unchanged. New subclass documents the explicit source-authority composition rule and adds mutation checks. |
| `inputs/**` | Exact tracked paths and commits in `source-provenance.json` | Per-file pinned | None. |
| `pilot01.png`, `pilot01-tests.log` | Parent `south-neutral.png`, `tests.log` | Per-file pinned in `pilot01-immutable-inventory.json` | None. |
| `canonical-upper-derivative.png` | Exact canonical frame under declared source ownership in `identity-policy.json` | Pinned in policy | New separately identified derivative. Exact RGBA assignment, no repainting or alpha-over. |

All dependencies required for rendering and regression execution are copied inside this directory. Parent paths above are provenance citations, not runtime imports. The original pilot preservation audit is intentionally separate from standalone rendering.
