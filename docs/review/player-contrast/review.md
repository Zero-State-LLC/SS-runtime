# Painted Player contrast comparison — BP-010

Status: REVIEWED quiet-scene diagnostic; production selection remains open.

Runtime adopts specification c075b21e9e70828b032f7f319a712c179450b4f9 in all four pin locations. Exact local parity passes for every bundled contract and fixture. Gameplay versions, source art, active clip delivery and normal rendering remain unchanged. Runtime base b693cad plus the pin/capture change produces this review.

## Method

The existing shared-scene XCTest captures all four painted neutral facings at both existing projection zooms. Each pair holds texture, root, anchor, HUD, backdrop and source shadow fixed. The finer 3× outline is the 100% control. Additional 50%, 25% and 0% values change only the Player outline node's alpha, inside a scoped block that restores it even if capture throws. The test asserts unchanged Player root/texture and other child-node opacities, then verifies restoration. No production opacity control, user setting or enemy contrast change was introduced.

Result Test-SSRuntime-2026.10.14_17-35-35--0700.xcresult: succeeded, 97 test executions, one pre-existing warning. This includes 91 Swift Testing tests and four XCTest cases with two additional parameter executions. Capture test passed in 44.864 seconds. Simulator: iPhone 17 Pro, CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Viewport 704×326 logical, captures 2112×978 pixels. The static composition is the existing review snapshot; it is not a legal encounter or a performance benchmark.

Thirty-two original captures are in renderer/. Comparison plates crop original pixels without resizing; derived grayscale uses Pillow luminance conversion. South half-scale images are Lanczos resizes of the full scene. These derived views are review aids, not new engine captures. The source/export provenance is unchanged from the painted-player and finer-outline reviews.

## Observations

The closer colour plate, unchanged-zoom grayscale plate and full closer south/no-border scene were inspected. On this pale paving, all four neutral silhouettes remain distinguishable without the added border. Removing it better integrates the hood/coat/boots with the painted style. At 25%, the border is less dominant but still adds a light rim; at 100%, it clearly reads as a separate graphic treatment. These are visual judgments on this backdrop, not user acceptance or a measured visibility score.

No claim of complete grounding follows: the existing broad shadow and registered still poses do not demonstrate planted-foot contact. The building, paving and cropped Camera in the closer view remain unresolved benchmark composition issues. The no-border result is a promising comparison candidate, not an admitted art family.

## Remaining acceptance

BP-010 still requires dark asphalt, building shadow, busy props, fog, movement/reversal, damage versus steady-state cues, legal dense combat, Camera fields, occlusion and Reduced Motion evidence. There are no enemies in these diagnostic views, so grayscale here cannot prove faction discrimination. Half-scale derivatives exist but have not received a complete observer review. No optional accessibility mode or context-sensitive outline has been designed or implemented.

Recommendation: carry the no-added-border candidate into the darker-backdrop and legal-encounter comparison, retaining 25% as a fallback comparator. Do not change shipping D-094 until that comparison supports the chosen treatment and coordinated spec/runtime changes. Full core regression: 773 tests in 109 suites passed in 465.129 seconds. No physical-device testing occurred.
