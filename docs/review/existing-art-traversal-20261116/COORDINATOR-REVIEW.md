# Coordinator existing-art review, November 16, 2026

Scope: accepted benchmark-faithful-scene slices8–10, BP-001–BP-012 / T1045. This is existing-art diagnostic coverage, not completion of the coherent repaired scene.

## Native and portable evidence

- Traversal actual `0659.xcresult`: independently queried one passed test, zero failed/skipped. Retained52 screenshots,824 callback rows,51 selected-texture images and1073 resource bindings. Both normal/Reduced Motion arms and their separate replay terminate at the same digest. Independent portable execution at07:10–07:11UTC passed22 tests, including real-evidence mutations and gallery integrity. The earlier ambiguous-point compilation and incorrect raw-Q8 comparison attempts remain preserved. #239 remains open for integration review.
- Viewport actual `0653.xcresult`: independently queried one passed test, zero failed/skipped. Ten retained captures. Independent portable execution passed7 tests. Scene safe-area inputs are synthetic. UIKit host/window bounds are separately recorded from requested capture-canvas bounds. No physical device, spoken accessibility, focus order or interactive scroll/reachability validation is claimed.
- Encounter actual `0710.xcresult`: one passed test in71.885s. Coordinator independently exported and validated the actual v2 ledger,9 screenshots,1073 resources, replay and crop/node records. Camera integrity0–3, destruction, dense, entity death, field occlusion, hostile projectiles and mines are observed. Player damage and telegraphs are NOT observed. Earlier0649 and0701 captures remain inadequate/rejected for corrected framing. Portable pre-import run passed23 reader/gallery regressions, including rejection of both old attempts. Corrected retained-packet validation at07:17UTC passed28 reader/gallery/actual-packet tests, including five new real-evidence and loaded-path regressions. These verify the retained result, not future runner installations.

## Executed-bundle mismatch

07:01 had passed while executing a retired v1 bundle. Exact runner diagnostics and readable old-binary hash established that its loaded path differed from the current installed v2 path. One non-erasing restart of the dedicated simulator preceded the07:10 retry. The retry's actual loaded binary hashes to `cb8a0f252bb2bb46bca16c808eba373569f31fcfe1d4640bef487016c91e5504`, matching the corrected compiled binary. The mechanism retaining the old container is unproven. See encounter `attempts/02-0701-old-schema/LOADED-BUNDLE-DIAGNOSIS.md` and runtime#241. No test assertions were weakened and no production fix is inferred.

## Actual browser checks

At07:12–07:13UTC, actual Brave exercised all52 traversal images across native, half and grayscale modes:156 image/size checks passed. Logical output sizes were704x326 and352x163; grayscale computed to `grayscale(1)`, and no page horizontal overflow occurred. Reference remains its original aspect ratio. An initial hidden-tab/image-readiness check timed out. Activating the tab and explicitly enabling eager image loading for the browser probe completed every selection. This probe adjustment is not a runtime or source-art change. The Jev handoff returned a provider401, so direct browser actions completed the checks without changing credentials/providers.

The viewport gallery loaded all10 captures. Both button-controlled scales were exercised: all10 at1x and all10 at0.5x, no page horizontal overflow. This tests the review gallery, not native device scaling or game interaction.

The corrected encounter gallery was also checked in actual Brave at07:17UTC: all18 image elements (nine captures at two sizes) loaded at704x326 or352x163 from1408x652 PNGs. Grayscale toggled to `grayscale(1)` and restored to `none`; no horizontal overflow occurred.

## Visual observations and limits

Coordinator inspected the actual corrected dense tick459 PNG: Player is centered, two enemy drones and a projectile are visibly in frame, rather than inferred only from simulation membership. Existing building cutouts, pavement, different actor styles, white outlines and prominent ordinary HUD remain inconsistent with the approved whole-scene benchmark. Passing crop/node checks do not resolve those deficits.

The actual SE accessibility3 upgrade PNG displays the heading and upper first card, with remaining content outside the captured viewport. Static evidence cannot establish that scrolling reaches all options or that VoiceOver selection works. Do not mark accessibility acceptance complete on this basis.

Traversal midpoint plates are reversible post-action stills using selected textures, not live midpoint camera behavior or comprehensive visible-pixel occlusion proof. No16-pose, full-family, performance or scanout claim follows.

## Gates

Whole-scene benchmark: NOT MET. Building registration, coherent editable Player family and faithful editable Camera source remain blocked. No detailed state/clip expansion, production art/HUD/input/collision/field change, shipping pin change, receipt adoption, issue closure or merge permission. Paired-device discovery and signing identities did not supply a configured team/provisioning profile, so no physical installation or acceptance is claimed. #237 remains unrelated and open.
