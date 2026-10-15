# Finer outline sampling — BP-007 / defect #124

Status: REVIEWED comparison, production selection pending.

Specification: 439739ea146af57ecc10762d1d55b1fe66331efd. Runtime base: 87810490e2eb676126ca46128e7ca04998244fa5 plus the local five-file sampling comparison change. Ordinary rendering remains at samplingScale=1; the DEBUG benchmark seam explicitly requests 3 for each comparison capture and then restores the normal callback.

The mask uses three samples per logical pixel while keeping one logical unit of dilation. Padding becomes three mask pixels; faction dash coordinates divide by three. Cache identity includes sampling scale because identical mask dimensions can represent different logical sizes/padding. The source image limit, bounded mask dimensions, cache count/byte limits, sprite geometry, anchors and faction colours remain unchanged. Unsupported scale or oversized masks return nil; there is no implicit fallback or production-wide switch.

## Visual evidence

Sixteen actual SpriteKit captures cover baseline/finer masks, four facings, and the existing two zooms. Test result: Test-SSRuntime-2026.10.14_17-24-13--0700.xcresult, iPhone 17 Pro simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3. All 97 executions passed (91 Swift Testing cases, four XCTest cases and two additional parameter executions); one existing compiler warning. Capture summary is in renderer/capture-summary.json. Original full captures are 2112×978 for the 704×326 logical viewport.

The comparison plate crops without rescaling the actual captures. All eight pairs were inspected, plus the closer south full scene. The finer mask visibly reduces stepped edges around hood, coat, hands and boots without moving the character. This is evidence for the four neutral candidate poses only. No thin-feature stress fixture, animated silhouette run, hostile dash visual comparison, dense encounter or device profile was captured in this change.

The new regression proves the same logical ring/dash pattern for an aligned rectangular silhouette, bounded byte retention, distinct cache identity when mask dimensions coincide but logical scale differs, and invalid/over-budget sample rejection. Earlier source-density, scaled-parent placement, replacement-frame, Reduced Motion and baseline dash tests also pass. Their prior scaled-parent/current-frame tests exercise the default sampling scale; the captures add visual 3× placement evidence, not a complete replacement for 3× animation coverage.

## Cost and decision

At logical 64×64, baseline uses a 64×64 mask and 66×66 output; finer uses 192×192 and 198×198. Accounted output RGBA rises from 17,424 to 156,816 bytes (9×). The explicit input-mask and output arrays total 304,272 bytes at 3×; source decoding, CoreGraphics/SpriteKit copies and GPU allocations are additional and unmeasured. A 4 MiB cache fits 26 finer outputs before its byte bound; 64 unique movement frames would exceed that bound. This is a potential cache-churn problem, not a measured frame-time result. Larger actors can exceed the existing 256-per-dimension mask guard at 3×, so a global default change would be unsafe without an explicit bounded sampling policy and coverage.

PROPOSED: retain the finer comparison path and use its visible edge quality as the target. Before selecting it for production, measure animated multi-actor misses/evictions and CPU cost, evaluate a bounded density policy for larger canvases, and compare thin silhouettes and enemy dashes in motion. Keep #124 open. Do not increase the cache budget based on theoretical bytes alone.

The scene still has unresolved benchmark art/composition issues: bright plaza paving, building treatment, clipped camera at closer framing, and no accepted locomotion. These captures do not admit the character family, finish the shared benchmark, or authorize physical-device testing.

## Final verification and design feedback

Full core suite: 773 tests in 109 suites passed in 492.997 seconds. No core behavior changed. The user questioned the glowing player outline in this comparison. The retained high-contrast border reads like a sticker/glow against the painted benchmark; smoother sampling does not resolve that design mismatch. Treat border strength/treatment as an open researched readability decision, comparing subtler contrast/shadow treatments at native size and in dense encounters before amending the existing faction contract. Do not equate this technical outline result with user approval of the white border.
