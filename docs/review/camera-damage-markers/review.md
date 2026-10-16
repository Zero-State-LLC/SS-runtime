# Camera damage-stage markers — BP-004

Specification: SS-specs d640197ffc13b051882df5178d18035a4e0898e4.

The shipping WorldRenderer now shows one ivory notch on a dark backing at camera integrity 2, two at integrity 1, and none at integrity 3 or 0. This is damage-stage information, distinct from the targeted HUD remaining-integrity slots. Markers follow the camera ground anchor, do not animate under Reduced Motion, reuse their node across damage states, and clear when the camera is removed or destroyed. Captain emitters use a separate rendering path.

## Evidence

Xcode result Test-SSRuntime-2026.10.14_10-57-31--0700.xcresult: Passed, 87 tests, zero failures or skips; 89 executions including dynamic parameters. iPhone 17 Pro simulator, iOS 26.5. Includes cameraDamageNotchesPersistAndClearWithIntegrity and benchmark captures. Four targeted ContractVersionsTests / AssetCatalogTests also passed. Local exact pinned parity passed for all 21 contract/fixture JSON files, with only the documented catalog specificationCommit exception. No physical-device testing performed.

comparison.png contains four actual renderer captures reduced from 2112x978 to 704x326 logical size. comparison-grayscale.png uses the same captures. Visual inspection confirms the one/two notches remain distinguishable in grayscale at this review size. This is an initial sizing candidate, not accessibility acceptance or a dense-combat visibility result.

## Remaining benchmark gaps

Camera art is still four state candidates, not the six required animation clips. Pole pixels are not identical across source states. Damage art alone remains subtle. Character directional anatomy and full gait loops remain unaccepted. Building ground registration, environmental scale, repeated paving, contact shadows and legal/dense encounter evidence remain open. Increasing texture resolution cannot correct those composition or motion problems. Review candidates remain test-bundle assets; no production art admission is claimed.
