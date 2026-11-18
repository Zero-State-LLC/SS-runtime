# Runtime #260: deterministic presentation socket ordering

Authorized by coordinator2026-11-17 03:20UTC after issue260 was opened. Separate from kiosk art wiring. Only production change is `PresentationSnapshot.swift`: sort encounter dictionary keys using existing `utf8LessThan`, then flatten each unchanged authored array and retain elite/boss suffix. No arena, spawn selection, simulation, digest, asset, or native assertion change.

## Red/green proof

Command: `swift test --scratch-path docs/review/kiosk-only-geometry-20261117/.swift-build --filter PresentationSocketOrderingTests`.

- `socket-red-0320.log`: initial compilation failure because GameSession is app-only. Corrected the new core test to use independently initialized Simulation instances. This is not behavioral red evidence.
- `socket-red-0321.log`:4tests executed,33failed expectations. Exact UTF8-key order failed,24insertion-history full snapshot equalities failed, and8independent-session snapshot equalities failed. Bundled canonical-order case happened to pass under that process's random dictionary order. Digest and authored-array checks passed.
- `socket-green-0321.log`: unchanged4regression tests all pass after production key-order repair, exit0. Coverage includes exact bundled order, UTF8 keys, intra-encounter authored order, elite/boss suffix,24dictionary rebuild histories,8independent simulations, full snapshot equality and unchanged authoritative digests.

Original native0314failure remains immutable, including summary and exact `tests-0314-differing-arrays.txt`. Native test source SHA256 remains `fc2f903d2f8c9cadbff3cdd425a607b50e77b2b86d5a9225acf67b29ae01efa6`.

Fresh Debug rebuild succeeded (`build-debug-socket-0322.log`), then exact8test native execution succeeded, exit0. Actual `tests-0322-summary.json` reports total8, passed8, failed0, skipped0. Full `tests-0322.xcresult` and raw log retained. Simulator slot released to coordinator at03:23UTC.

`build-hashes-0323.txt` records all owned source files, app executable, Debug implementation dylib and test bundle. Core source SHA256 `5cac8af2877bdf71751ca93d66eea82050e015036535dd54148653ff2120d022`; new regression test SHA256 `6ecaeb4e2bfb479bf46e22169cf007d8d8a148711adf2bab5967f960b4bb47bb`. App executable SHA256 `b71e6003ba50951745215b866243ce3c9d3497afd6887c9ba68be9382b024aad`; Debug dylib SHA256 `2cf0e8f900436e5ca592dfc63671c958cc64e7b9fdb04caa7bbd2c08906a15f3`. Native test source and compiled test bundle are unchanged from0314.

No shared-tree commit by this worker, as instructed. Coordinator owns independent review, publication and current/candidate actual app captures using README launch commands. No art acceptance or broader qualification claim. Release exclusion proof precedes this presentation-only core fix, not a fresh post-fix Release build claim.
