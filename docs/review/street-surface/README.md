# Shared street-surface comparison — BP-001/BP-005/BP-007

Spec d602775; runtime parent e4b668d. The spec was deepened before runtime changes, with matching plan/task/acceptance clauses. All 22 bundled JSON contracts/fixtures match that spec commit, with the catalog's adopted specificationCommit field. Ruleset, arena, content and replay identities remain unchanged.

## Implementation and scope

WorldRenderer's review-art path now supports bounded repeating surface patches and independently placed continuous ground lines. A partial tile uses a texture subrectangle at the same density rather than stretching the full texture. All details belong to the ground layer and therefore share the benchmark ground transform. They are removed with the usual renderer reset. Normal gameplay supplies no review art and receives no patches or lines.

The existing control and registered plain scene are retained. The added street scene uses the existing asphalt and plaza sources, one asphalt rectangle and six placed strips for curb shadow/top and two rail grooves/metal faces. The exact fixture values and source hashes are in source-record.json. The road clears the one fixture building and keeps the placed camera/tree/newsbox on the pedestrian side. This is not the level's authoritative 30-degree rail spine. No crosswalk is drawn because the fixture has no opposite pedestrian landing. Procedural strips remain comparison geometry rather than finished infrastructure artwork.

## Research

[SF Better Streets sidewalk zones](https://sfbetterstreets.org/design-guidelines/sidewalk-zones/index.html) distinguishes frontage, throughway, furnishings and edge functions. [SFMTA historic streetcars](https://www.sfmta.com/getting-around/muni/historic-streetcars) records streetcar track work alongside curbs, crossings and boarding islands. Accessed 2026-10-14. These support the contextual separation; all game-unit dimensions and material values are authored comparison parameters. Existing civic-seam-visual-direction.md §5b already prohibits repeated linear infrastructure in ground tiles.

## Verification

Specification validator passed (23 JSON artifacts, 7 schemas, 33 registered contracts, 55 indexed files). Four ContractVersionsTests/AssetCatalogTests passed with exit 0. The simulator capture checks all 132 road tiles remain within the patch, partial tiles preserve 128px/128-unit density, plain-scene reset removes the curb, projection preserves the building anchor, and simulation digest remains unchanged. Final simulator run Test-SSRuntime-2026.10.14_23-30-18--0700.xcresult: 106 executions, no failures; one existing EnvironmentLibrary nonthrowing-try warning.

## Remaining

This explicitly placed composition is not a legal encounter or live traversal result. Source material variation, final curb/rail art, source-building residuals, Player outline treatment, continuous animation, occlusion, legal/dense encounter integration and device performance remain open. No production style or asset admission is claimed.

## Visual observation

The upper-right street now reads as a continuous asphalt band with two embedded rail indications. The tree, camera and newsbox remain on the pedestrian side. The road edge is still mechanically straight and the paving repeats prominently. Most of the Camera field remains on pale paving; this capture does not satisfy the asphalt field-readability matrix. The current opaque Player border remains conspicuous.
