# Issue 262: historical preservation and current qualification

## Original failure

Exact PR236 head `0c20990c8a6334b6c93d42db0336fc4cf2ab62f9`, CI run `44016077111`, completed with Debug, Release, swift and device-sitting jobs successful and spec-parity failed. The failing step was **Verify bounded base and curb comparison without admission**. Its unchanged V9 audit ran seven tests with one error: `Protected bytes changed: App/GameScene.swift`.

Retained raw evidence: `ci44016077111.json`, `ci44016077111-failed.log` and `original-audit-red.log`. Reproduced locally on November18 before any repair. The failure is real divergence from a historical byte snapshot, not evidence that those later authorized changes should be rolled back. Prior #237/#259 failures and original #261 red evidence are not reclassified or removed.

## Exhaustive receipt inventory

The V9 receipt protects **1766** paths, pinned to `404d6b2bac5beeceeab4068d33c24dd5a001430c`. At intake, **1761** still have identical bytes and **five** differ. No receipt path is missing.

| Protected path | Later implementation commits | Authority / evidence |
|---|---|---|
| `App/GameScene.swift` | `8449f6d`, `bb87411` | Production-execution directive and approved `intent/2026-11-17-live-world-projection.md`, kiosk playable and live-projection coordinator reviews |
| `App/WorldRenderer.swift` | `8449f6d`, `bb87411` | Same presentation-only authority and reviews, no neighbor source-art redesign |
| `Sources/SurveillanceCore/Contracts/GateRegistry.swift` | `0aa3951` | `intent/2026-11-17-production-qualification.md`, #257, all120 accepted gates rather than the incomplete census |
| `Sources/SurveillanceCore/Determinism/SHA256.swift` | `4294f73` | Same production intent, measured hashing subsection and `production-execution-20261117/HASH-PERFORMANCE.md`, byte-identical digest requirement |
| `Sources/SurveillanceCore/Presentation/PresentationSnapshot.swift` | `fed8a3d` | #260 and `kiosk-only-geometry-20261117/native/playable/SOCKET-ORDERING-REPAIR.md`, existing UTF8 key order with authored arrays preserved |

The later App additions `KioskPlayableReview.swift` and `LiveWorldProjection.swift` were not present in the historical receipt. They are not historical frozen files. Do not confuse their absence from that receipt with a grant for arbitrary future additions.

## Decision

The historical audit is correct for its original scope. Its current CI invocation is not: it applies the old no-runtime-change work-order boundary to a branch containing subsequent authorized runtime work. Keep the old receipt, audit, tests and old failure exactly as they are. Separate historical reproduction from current qualification, with exact provenance-bound transitions instead of broad exclusions.

The historical result must explicitly identify the exact exported commit. The current result must enforce every original protected path, reject all unlisted changes and bind the five exceptions to original and final hashes and exact original implementation commits. Historical script/test identities must also be verified so executing an altered oracle cannot conceal drift. Failure in either scope must fail CI.

The remaining V9 source, scene, retained capture, baseline RGBA and gallery checks continue against the current checkout. No simulator capture is regenerated. No source art, runtime implementation, protected tests or old expected hashes are changed by this repair.

## Boundary

Scope: `intent/2026-11-18-preservation-verification-scope.md`. CI repair is not art acceptance, gameplay requalification, physical-device certification, merge, release or issue closure. Visual benchmark remains **NOT MET**. This packet records evidence and does not erase the earlier red result.
