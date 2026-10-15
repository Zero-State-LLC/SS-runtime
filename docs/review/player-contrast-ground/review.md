# BP-010 darker-ground comparison

Status: REVIEWED static backdrop diagnostic; production selection remains open.

Runtime base ee9331b plus the darker-ground capture test; spec c075b21e9e70828b032f7f319a712c179450b4f9. The fixture uses the existing projected shared scene at closer zoom, replacing only nodes whose texture is the review paving with bundled asphalt/service textures. Four facings × two surfaces × 100%/25%/0% Player border produces 24 original captures. Ground textures and border alpha are restored and asserted afterward. Root and Player texture remain fixed. No production rendering behavior changed.

Simulator result Test-SSRuntime-2026.10.14_18-02-51--0700.xcresult completed successfully: 97 executions, one existing warning. The capture case passed in 40.442 seconds; 91 Swift Testing tests passed in 37.247 seconds, alongside four XCTest cases and two extra parameter executions. iPhone 17 Pro simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3, viewport 704×326 logical, 2112×978 captures. The prior core run for this unchanged capture edit passed 773 tests in 109 suites in 346.800 seconds; it was not restarted after unlock.

Source hashes/dimensions match the catalog as recorded in surface-provenance.json. The colour asphalt plate and grayscale service plate were inspected across all facings. Without the added border, the hood, coat and boots remain distinguishable on these static backgrounds and the character integrates better with the painted scene. The 25% contour adds some separation but retains a light rim. This is an observer judgment from these captures, not user approval, a quantitative accessibility pass or proof of visibility during gameplay.

The comparison plates crop actual renderer pixels without resizing. Grayscale is a derived Pillow luminance view, not an engine filter. This test substitutes surface materials in the existing composition; it does not move the player through real zone transitions or establish legal encounter state. Existing transition decorations remain in the scene. No enemy faction-discrimination claim follows from a scene without enemies.

Keep no-border and 25% candidates for the remaining movement, fog, dark shadow, occlusion and legal dense-combat matrix. The quiet scene does not settle damage readability or faction identity. Source animation and environment registration gates also remain open. Normal play retains the current contrast contract. No physical-device test occurred.
