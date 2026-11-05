# Catalog gate

Read 2026-11-05 from `AssetCatalogLoader.decodeAndValidate` on `ef68565`. No asset was admitted.

The visual refusal stays in [visual-gate-2026-11-05.md](visual-gate-2026-11-05.md). The clip refusal stays in [clip-gate-2026-11-05.md](clip-gate-2026-11-05.md). The specification pin stays in [replay-identity-2026-11-04.md](replay-identity-2026-11-04.md).

The catalog schema is `asset-catalog-001`. `legacyRepository`, `legacyCommit`, and `specificationCommit` must equal `LegacyEvidence.repository`, `LegacyEvidence.commit`, and `ContractVersions.specificationCommit`. The catalog keys are exactly `schemaVersion`, `legacyRepository`, `legacyCommit`, `specificationCommit`, and `entries`. Each entry's keys are exactly `admissionDecision` and `record`. An unexpected key throws `unexpectedKey`.

A record uses schema `asset-record-001`. It must carry `schemaVersion`, `assetId`, `kind`, `productionStatus`, `runtimeRequired`, `provenance`, `license`, `source`, `runtimePath`, `sha256`, `dimensions`, `colorSpace`, `alpha`, and `ownerContract`. `notes` may be present and is not required. The asset id must match `^[a-z0-9][a-zA-Z0-9_]*$` over the whole string. A sha256 that is present must match `^[0-9a-f]{64}$`. A repeated asset id throws `duplicateAssetId`.

An `accepted` record needs a non-empty source, runtime path, sha256, and license. `excluded`, `rejected`, and `sfCandidate` refuse `runtimeRequired`. `originalAccepted` requires status `accepted`, provenance `projectOriginal`, `runtimeRequired`, and a non-empty path and sha256. `adaptedAdmitted` requires status `accepted`, provenance `adaptedLegacy`, `runtimeRequired`, and a source that starts with `legacy://`. `plannedOriginal` requires status `planned`, provenance `projectOriginal`, `runtimeRequired`, and a nil source, runtime path, and sha256. A runtime-required record whose provenance is not `projectOriginal`, and whose decision is neither `adaptedAdmitted` nor `originalAccepted`, is refused. A runtime path that starts with `ArtSources/` is refused.

The presentation JSON must carry `requiredAssetIds`, `audioEventIds`, and `musicAssetIds`. Each id in those three arrays must be covered by `plannedOriginal`, `adaptedAdmitted`, or `originalAccepted`.

This does not admit an asset.
