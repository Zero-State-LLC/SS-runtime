# Failed attempt 02: incorrect test root mapping

Runtime issue #239 remains open. This is a test-harness contract mismatch, not an established production defect.

The centrally executed 0654 xcresult reports 1 failed, 0 passed and 0 skipped tests. Native log reports 1,408 failures, all XCTAssertEqualWithAccuracy at executed Swift lines 155/156. No other error lines or timeout were found in that log. Test duration was 53.653 seconds. The command wrapper logged exit zero, but XCTest reported TEST FAILED and coordinator reported xcodebuild exit 65. The summary, rather than wrapper success, controls admission.

Exact executed Swift SHA256: `66a9d5feeca9c19d3ed900292ee1125816b29d410c71b819f0a6867d433c451b`.
Result path: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-traversal-20261116-0654.xcresult`.
Retained: exact executed source, native.log, summary.json, tests.json, and 105 exported attachments with original export manifest. Failed captures are history only and must not enter the active packet.

Production `PresentationSnapshot.swift:200-211` projects Q8 coordinates using `unitsTruncated`. `Q8.swift:16-18` divides signed integer raw coordinates by 256, truncating toward zero. The rejected test incorrectly demanded fractional Q8 world coordinates equal rendered integer coordinates. The correction asserts two separate exact mappings: snapshot integers equal authoritative unitsTruncated, and observed renderer roots equal snapshot integers. Raw authority, snapshot integer roots and observed rendered roots are recorded separately. Screenshot projection reconstruction starts from snapshot roots, not fractional authority. No production behavior, tolerance relaxation or visual acceptance threshold changes.
