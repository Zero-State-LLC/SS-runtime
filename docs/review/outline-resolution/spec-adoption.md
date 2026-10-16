# BP-007 outline resolution clarification

Specs commit: 439739ea146af57ecc10762d1d55b1fe66331efd. Runtime adopts the exact pin in all four existing locations. No outline algorithm or production asset is changed in this adoption.

Observed defect: runtime #124, https://github.com/Zero-State-LLC/SS-runtime/issues/124. The real-renderer 384px candidate loses its outline after normal refresh because the current source budget is 256×256. Source-pixel stroke generation also couples visible thickness to texture density.

The specification now requires consistent equal-framing faction stroke/dashes, explicit pixel/logical-mask/anchor dimensions, current-frame outline synchronization, stale-output removal and bounded measured memory/cache behavior. The plan proposes a bounded logical-mask comparison against density-aware source masks; no algorithm or numeric memory budget is claimed as externally proven or device-validated.

Research: Apple documents SKTexture.size() in points, cgImage/filtering as separate texture APIs, and texture retention while referenced. Sources: https://developer.apple.com/documentation/spritekit/sktexture/size() and https://developer.apple.com/documentation/spritekit/sktexture . These support separating storage and draw dimensions; SS's visual policy and proposed implementation are identified as project decisions in the spec.

Validation: specs validator passes (23 JSON artifacts, 7 schemas, 33 registered contracts, 55 indexed files). Timing migration validator passes (59 clips, 218 facing selections, 14 malformed cases, 5 exact vectors). Seven focused runtime pin/timing tests pass. The actual scripts/spec_parity.sh passes against the exact local SS-specs commit through a process-local git URL rewrite. This is not a remote CI result. The prior full core and simulator results remain in the painted renderer review; they were not rerun for this pin-only adoption.

Next implementation must resolve #124 and pass the new 64/256/384 same-size, anchor, frame-change, Reduced Motion, unsupported-input and cache-churn checks, with native/zoom captures. No high-resolution family admission, artwork acceptance or physical-device testing is authorized by this evidence alone; the user's existing production scope and review gate remain unchanged.
