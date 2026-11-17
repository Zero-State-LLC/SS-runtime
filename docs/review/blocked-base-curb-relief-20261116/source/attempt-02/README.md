# V9 sole material correction, attempt02

BP-001/007/012,T1045. Authorized by `../../SOURCE-REVIEW-01.md`. Final source only, no third aesthetic pass.

The complete first source, original manifest, rejected previews and snapshot remain immutable. This directory adds one material correction: broader staggered masonry courses using retained plain stone, lighter/desaturated low-contrast mineral-gray curb. All geometry bytes,53registrations, contacts, roots, heights18/3, semantic coverage and PNG alpha arrays are unchanged. No old source, paving, production or authoritative topology edit.

The final synthetic compositor uses retained world-footprint depth and exact registered actor alpha, rather than drawing every new sprite over native context. Per-sprite evidence in `output/preview/preview-metadata.json` binds occluders and visibility to the actual joint order. The retained kiosk/stair sprite is ahead of the overlapping base. That consequence is displayed honestly, not masked away or depth-boosted. Native inspection still required.

Review images: `output/preview/base-curb-detail.png`, `context-z100.png`, `context-z125.png`, `context-z140.png`, corresponding half/grayscale, and `full-benchmark-comparison.png`. All are synthetic source preview, not native evidence or acceptance.

Validation from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_source.py
PYTHONDONTWRITEBYTECODE=1 python3 replay.py --out "$JCODE_SCRATCH_DIR/v9-final-independent-replay"
```

Existing outputs refuse overwrites. `manifest.json` and `API.md` define the final interface. Recommendation remains coordinator-only and pending. No native/build, commit or push by source worker.
