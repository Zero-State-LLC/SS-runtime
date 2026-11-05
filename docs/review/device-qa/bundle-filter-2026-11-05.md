# Bundle filter

Read 2026-11-05 from `RuntimeBundleFilter.project` on `ef68565`. No asset was added.

The admission shapes stay in [catalog-gate-2026-11-05.md](catalog-gate-2026-11-05.md). The clip frame ids stay in [clip-gate-2026-11-05.md](clip-gate-2026-11-05.md).

`reachableAssetIds` is the presentation contract's `requiredAssetIds`, `audioEventIds`, and `musicAssetIds`, plus `environmentAssetIds` when that array is present. It also includes every `frameIds` entry in `clip-metadata-001`. An absent environment array contributes nothing.

An entry is bundle-eligible when its decision is `plannedOriginal`, `adaptedAdmitted`, or `originalAccepted`, it is runtime-required, its id is reachable, and its runtime path does not start with `ArtSources/`. `project` sorts the eligible ids and the excluded ids.

`validate` appends `duplicateBundleAsset` for a repeated eligible id. An ineligible entry whose decision is outside those three, and which has a runtime path or is runtime-required, appends `legacyEvidenceInBundle`. That same entry appends `nonSanFranciscoInBundle` when the id contains `_atlanta_` or the decision is `excluded`, and a runtime path is present. A runtime-required entry in the three decisions whose id is not reachable appends `unreachableRuntimeRequired`. A runtime path that starts with `ArtSources/` appends `sourceEvidenceInBundle`.

`PresentationAssetRegistry.bundled` stores that projection's ids, and copies the three presentation arrays from `presentation-assets-003`. `require` throws `unreachable` when the id is not in the bundle list.

This does not admit an asset.
