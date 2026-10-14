# BP-003 reproducible timing export

OBSERVED: the runtime now has `scripts/convert_clip_timing.py`, a mechanical v1-to-v2 candidate exporter. It reads the pinned target schema explicitly, validates before writing stdout, rejects duplicate JSON keys and mixed representations, and leaves active resources untouched. Requires Python and jsonschema. It does not admit art or replace runtime semantic validation.

Run from SS-runtime:

```sh
python3 scripts/convert_clip_timing.py Sources/SurveillanceCore/Resources/contracts/clip-metadata-001.json --schema ../SS-specs/contracts/clip-metadata-002.schema.json > /tmp/clip-metadata-002.candidate.json
python3 scripts/test_clip_timing_export.py --schema ../SS-specs/contracts/clip-metadata-002.schema.json
```

Use a separate output path: shell redirection truncates its destination before the converter starts. Do not redirect onto the source.

OBSERVED: two export tests passed. Complete round-trip comparison preserved all non-timing fields, full frame order, anchors, events, cancellation rules and loop flags across 59 clips. All 218 facing selections retained exact rational duration and 60 Hz lifetime. Two CLI runs emitted identical bytes. Eighteen invalid inputs (including boolean/fractional fps, mixed timing, unknown fields, invalid/duplicate/empty facings, duplicate JSON keys, wrong version and malformed JSON) emitted no candidate.

OBSERVED: eight focused Swift timing/decoder tests passed in 0.428 seconds. No Swift, bundled resources, gameplay identities or specification pin changed in this step. This is not a new full-core or simulator run; the preceding renderer integration evidence remains in `docs/review/v2-renderer-integration`.

The source specification is 56a5a5da1d87491d23df86731cc01a5acd868d26, `animation-timing-migration.md` under BP-003. This implements its existing export/round-trip requirement without new design choices. Source, schema and candidate SHA-256 values are in hashes.json.

OPEN: coordinated active-resource/version/catalog/export admission; benchmark-quality source animation; camera family completion; projection/occlusion and encounter acceptance; native visual review and physical-device performance. A mechanically valid export does not establish visual quality. Active clip delivery remains v1.
