# Retained boot material transfer — source candidate

Status: source-material experiment, below benchmark art quality; not admitted.

The high-resolution lead-leg source and its existing uniform registration supply the laced tongue patch. material.py maps it exclusively onto the forward shaft tongue, removing the procedural lace ribbons so the two are not doubled. The heel, sides and outsole do not receive that patch. All 32 boot poses use the same source zones and ownership recipe.

The first render repeated a small swatch per face, producing stripes and excessive baked highlights. rejected-repeated-swatches.png preserves that failed result. The revised mapping derives coordinates from shared source vertices so adjacent faces share coordinates, then normalizes non-tongue swatches to explicitly authored palette values with 18% residual color variation. Those colors and normalization are source-experiment choices, not recovered hidden-surface detail or a new art-direction decision. The original raw source is retained unchanged.

The revised surface sheet and assembled contact comparison were inspected. They avoid the conspicuous repeated stripes, but the faceted boot shape, simple shaft and weak material depth do not meet the approved benchmark. The rear material is authored from a generic swatch, not the original unseen heel. This is not finished paint, and it must not be presented as a complete character animation. Further work needs a continuous sculpted boot/ankle shape, meaningful seams/sole construction, and full-body costume/depth review.

Authority: existing SS-specs d602775 controlled-character-source.md/BP-002/BP-008, which permits authored hidden surfaces but does not accept proxy geometry as final art. No active renderer, runtime resource, gameplay or spec pin changes.

Reproduce: Python 3 + NumPy + Pillow, run material.py. Exact source image, registration, retained contact, inherited scripts, 16 pose samples, 32 rendered boots and material ownership records are archived. Script completed exit 0 and verified exactly one laced-source face per boot. This checks assignment, not all-angle final-art quality. Latest core validation remains 773 tests / 109 suites; no repeat runtime/device test for this source-only experiment.
