# Resolution-aware outline implementation — #124

BP-007 at specs 439739ea146af57ecc10762d1d55b1fe66331efd. Functional resolution/placement repair; **not final art or device-performance acceptance**.

## Changes

OutlineTextures resamples source alpha to the actor's logical canvas before the existing one-pixel dilation and faction dash rule. Original colour textures remain untouched. The mask is rounded to nearest logical pixels, avoiding cache changes caused by SpriteKit Float geometry roundoff. Padding and anchor mapping use mask dimensions, never SKTexture.size() as a proxy for source pixels.

WorldRenderer recovers the unscaled local canvas from the sprite size and scale because the child outline inherits its parent's scale. An initial zoom capture exposed double scaling despite passing unit tests; the corrected implementation and new fractional/nonuniform-scale regression remove that mismatch. All final captures come from the corrected run. Invalid/nonfinite sizes or unsupported sources hide stale outlines; supported replacement frames restore the appropriate cached texture.

The cache distinguishes source identity, logical mask geometry and faction. Successful and failed entries share a bounded LRU list, retaining source identity only until eviction. Limits are 128 entries and 4 MiB of accounted outline RGBA payload. The source-image guard is 1024 pixels per dimension; mask dimensions are bounded to 256 per dimension. These are engineering bounds for this implementation, not measured safe device budgets. Cache misses generate a new mask; hits do not reread the source image.

## Verification

- Full core suite: 773 tests in 109 suites passed in 445.099 seconds. Core code was unchanged by the subsequent app-only scale correction.
- Final simulator result: Test-SSRuntime-2026.10.14_17-05-40--0700.xcresult; 96 executions, action succeeded. Includes 90 Swift Testing tests, four XCTest cases and two additional parameter executions.
- Four new regression tests prove byte-identical outlines for equivalent 64/256/384 silhouettes at logical 64; both Player and enemy treatment; cache identity/geometry/faction distinctions and churn bounds; invalid and over-limit inputs; current-frame replacement, asymmetric margins/noncentral anchors, invalid-frame hiding and restoration in both motion settings. Scaled-parent coverage includes 1.5×1.25 and fractional 1.1×1.3.
- Original unbroken/dashed outline test remains unchanged and passes. No assertion was weakened.
- Eight actual-renderer captures exported at 2112×978 and inspected in the native-size comparison plate. The closer front capture was also inspected separately at full resolution. The outline now hugs each candidate instead of disappearing or being enlarged twice.
- One pre-existing unnecessary-try compiler warning in EnvironmentLibrary remains.

## Memory and visual limits

For the tested 64×64 logical mask, the explicit source-mask RGBA array has 16,384 bytes and its padded 66×66 output payload has 17,424 bytes. These are payload accounting values, not process peak or GPU residency measurements. At the maximum 256×256 mask, those two arrays total 528,400 bytes; CoreGraphics/SpriteKit copies, decoded input images and allocator overhead are additional. The cache's retainedMaskBytes counter is verified under count- and byte-limited churn; it does not account for shared source textures or SpriteKit GPU allocation. Source references are count-bounded, but device residency and hot-cache churn still require profiling before high-resolution family admission.

Nearest logical-mask sampling produces visible stair steps at enlarged inspection size and can lose sub-logical-pixel features. The current Player silhouette remains distinguishable at native size, but the specified comparison with a density-aware/supersampled alternative and thin-feature coverage is still open. Keep #124 open for that comparison and memory/performance evidence. The sharp white faction treatment is existing specification policy; it is not a new art-style approval.

No new character art is admitted, no gameplay geometry or active clip metadata changed, and no physical-device test occurred. Broader benchmark environment, framing, animation and source-master work remains open.
