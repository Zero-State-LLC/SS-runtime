# Asset intake

Read 2026-11-05 from `AssetIntake.validate` on `ef68565`. No file was hashed.

The catalog refusal stays in [catalog-gate-2026-11-05.md](catalog-gate-2026-11-05.md).

`PNGHeader.parse` returns nil when the data is shorter than 26 bytes, the first 8 bytes are not the PNG signature, bytes 12 through 15 are not `IHDR`, or the width or height is below 1. Width is the big-endian integer at bytes 16 through 19. Height is the big-endian integer at bytes 20 through 23. The color type is byte 25.

A runtime path that starts with `ArtSources/` appends `artSourcesInRuntimePath`. An accepted record with an empty runtime path appends `acceptedWithoutFile`. An accepted `.png` path that fails the delivery grammar appends `invalidDeliveryName`. A delivery name ends in `.png`, has an `@` in the stem, a scale of digits that starts at 1 through 9 and ends in `x`, and at least two `_` parts. The first character is lowercase or a digit. Each part is non-empty and uses letters and digits.

Records whose source starts with `ArtSources/` are read under the evidence root. A missing file appends `missingEvidenceFile`. A size at or below 0 appends `emptyFile`. A recorded sha256 that already belongs to another asset id appends `duplicateHash`. The file bytes are not hashed. A `.png` whose header does not parse appends `emptyFile`. Recorded dimensions that differ from the header append `dimensionMismatch`. A recorded color space other than `sRGB` appends `colorSpace`. Color type 4 or 6 with recorded alpha `opaque` appends `colorSpace`.

Regular files under `ArtSources/legacy-evidence`, other than `README.md`, append `undeclaredEvidenceFile` when that relative path is not one of the declared sources.

This does not admit an asset.
