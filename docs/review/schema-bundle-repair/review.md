# BP-003 pinned-schema packaging repair

OBSERVED: runtime 7c0f062 omitted contracts/clip-metadata-002.schema.json present at its specification pin 56a5a5da1d87491d23df86731cc01a5acd868d26. Exact git-object comparison found one missing file and no other shared-file drift after applying the documented asset-catalog specificationCommit exception.

Defect recorded before repair: https://github.com/Zero-State-LLC/SS-runtime/issues/123

The repair copies that exact pinned schema into Sources/SurveillanceCore/Resources/contracts. It changes no active registry, clip metadata, assets, specification pin or gameplay identity. The parity guard was not modified.

Validation:
- Existing scripts/spec_parity.sh passed, including both-direction file inclusion and byte comparison. A process-local Git URL rewrite fetched the exact pin from the local SS-specs Git repository instead of GitHub; this is local parity evidence, not remote CI evidence.
- Swift test filter ClipMetadataV2Tests|Contract|LegacyAdmissionTests: 51 tests in 12 suites passed in 3.486 seconds.
- git diff --check passed.

## Remaining coordinated switch

Current-state discovery used the indexed graph, followed by exact current-file search because graph results hit the 500-match cap. These are live dependencies, not a proposed expansion of scope:

1. SS-specs: active versions.json clipMetadata entry; new active metadata payload; catalog ownerContract references; active README index; validator/migration checker inputs; timing design status and plan/tasks/acceptance. Retain the old representation as an explicitly historical compatibility fixture rather than silently converting migration tests into tests against themselves.
2. Runtime: ContractVersions.clipMetadata; ClipCatalog.bundled and ClipFrameLibrary.bundled resource lookup; RuntimeBundleFilter reachable-frame input; bundled metadata and catalog owner references; all four spec-pin sources. Preserve animation/gameplay identities during mechanical conversion.
3. Export/admission: admit_original_art.py and admit_legacy_assets.py contain hard-coded v1 resource and owner references. They must follow the active contract without granting admission to unreviewed art. convert_clip_timing.py remains a v1 input converter by design.
4. Tests: current v1 conversion fixtures and strict malformed-v1 checks must remain independently exercised. Active-delivery assertions in DaemonClipTests, StandardEnemyClipProjectionTests and ClipMetadataTests still require framesPerSecond and need exact timing expectations. This is a planned version migration, not permission to weaken assertions.
5. Run complete spec validation, bidirectional parity, core replay tests and iOS playback tests after the coordinated switch. Existing passing arithmetic and export checks alone do not prove active resource reachability or renderer behavior.

OPEN: the active switch and benchmark art/rendering work remain incomplete. This packaging repair removes a real parity failure; it does not admit v2 clips or establish benchmark visual quality. Physical-device testing remains deferred until the requested renderer/art review.
