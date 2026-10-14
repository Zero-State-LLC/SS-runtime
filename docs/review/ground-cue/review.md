# BP-009 combined occlusion cue comparison

Runtime parentc5b5037; adopted spec00ce027209e6c233bcdd35295f35f0b9bfb9bbe5. Candidate only, not shipping treatment.

The revised contract requires understandable Player ground position and solid boundary during occlusion, lifecycle restoration, static Reduced Motion readability, and continuous/encounter evidence before acceptance. Runtime pin and all21contract/fixture files match this exact spec commit except documented catalog specificationCommit. No gameplay identity change.

The real SpriteKit test compares0.35architecture opacity alone with the same opacity plus an ivory projected footprint and a black-backed ivory Player contact ring. The ring uses the authoritative18-unit collision radius and the same ground projection; it is elliptical in the captured view. Test verifies the cue has no actions. Rear contacts are manually selected test cases, not a production eligibility classifier. This does not establish Reduced Motion integration, lifecycle behavior or multi-occluder correctness.

OBSERVED: the outline makes the occupied ground region explicit and the contact ring locates the feet. Visual review still finds the whole white polygon too diagnostic for the intended street scene; the translucent building and high projected rear position can remain ambiguous. Do not declare visual acceptance. Next comparison should preserve the useful ground information with a less intrusive boundary/material treatment and continuous entry/exit before a production choice.

Validation: Test-SSRuntime-2026.10.14_12-10-27--0700.xcresult Passed87tests (89executions including dynamic cases), zero failures/skips, iPhone17Pro simulatoriOS26.5. Four targeted ContractVersionsTests/AssetCatalogTests passed. Spec validator passed. No physical-device test. Natural screenshots are actual renderer captures; comparison labels and grayscale conversion are postprocessing only.

Apple's node-property propagation documentation supports separate opacity and drawing-order handling: https://developer.apple.com/documentation/spritekit/about-node-property-propagation (accessed2026-10-14). The precise cue style/opacity is an SS experiment, not an Apple recommendation.
