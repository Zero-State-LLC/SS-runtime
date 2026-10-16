# BP-003 exact timing migration prerequisite: unified validation

Runtime base: 451a457. Spec pin: 00ce027209e6c233bcdd35295f35f0b9bfb9bbe5, animation-timing-migration.md and BP-003. This change does not admit v2 metadata or new animation art.

## Defects corrected

Frame delivery previously parsed a subset of clip JSON independently of ClipCatalogLoader. It ignored schema identity, unknown timing keys and several semantic constraints. An exporter could add timing while leaving fps, causing delivery to accept and ignore the authored durations even though the clip validator rejected the same data. Delivery now consumes the validated catalog.

The catalog integer helper fell back to NSNumber.intValue, truncating fractions and coercing booleans. Exact integer conversion now rejects fractions, boolean values and values outside Int range. Loop flags require actual JSON booleans; anchor objects require exactly x and y.

Delivery previously inferred a facing from equal-sized consecutive slices. The catalog selected facing tokens from authored frame IDs. A valid interleaved order therefore made the two readers disagree. Delivery now preserves authored order while selecting the declared facing token, matching the catalog.

## Verification scope

New regression cases cover malformed timing/scalars through both loaders, preservation of every bundled clip's fields and facing frame lists, and interleaved facing membership/order and timing. Existing original-art backing, alignment and exact timing tests remain in place. No fixture digest, catalog, spec pin, content/ruleset identity or production art changes.

## Remaining migration

The v2 schema, full parallel frameUnits delivery, facing-specific duration selection, version registry/export/resource migration and renderer pause/interruption tests remain required. Rejecting an unsupported timing key is a prerequisite, not v2 support. Complete source cycles and visual/device acceptance remain open.

Validation: the full core run passed 766 tests in 108 suites (348.388 seconds) after unified parsing/scalar validation. The final facing-selection change and its additional regression were then validated by 39 focused tests across ClipMetadataTests, ClipTimingTests, OriginalArtTests and ClipAlignmentTests (3.529 seconds). The full suite was not rerun after that final facing-selection change. No iOS test run occurred for this change; the renderer APIs and bundled valid v1 data are unchanged.

Commands: `swift test --disable-sandbox --cache-path ../swift-cache --config-path ../swift-config --security-path ../swift-security`, followed by the same command with `--filter 'ClipMetadataTests|ClipTimingTests|OriginalArtTests|ClipAlignmentTests'`.
