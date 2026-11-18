# Issue 262 implementation evidence

Worker scope: only the two new `scripts/*v9_preservation.py` files and new evidence in this directory. No worker commit. Coordinator owns CI, approved intent, independent review, handoff and publication. No Swift, simulator, remote build, fetch or worktree was run by this implementation.

## Two explicit scopes

1. `CURRENT_HEAD`: retain the original raw receipt SHA256 `5086e2f19bda1f88b72e9854dc05ca652b5049f72c07de65e130fec96b874baa`. Verify every one of its 1,766 paths. Exactly 1,761 retain their original hashes. Exactly five require the final hashes in the explicit transition chains embedded in `verify_v9_preservation.py`. No path is exempted. Also protect the original audit, its test and receipt. Match protected bytes to both HEAD blobs and index entries, rejecting a staged change concealed by restored working bytes.
2. `HISTORICAL_ONLY`: export the full exact tree at `6c3be49c0322874a7c037d4e0b29495e311a6c3a` to a temporary external scratch directory. Validate the commit identity and ancestry, enumerate its tree, reject links/devices/traversal/duplicate and case/Unicode aliases, and compare every exported regular file to its Git blob ID. Require complete file-set equality, so export-ignore or export-subst cannot silently omit/change historical content. Run the unchanged full `test_audit.py`, followed by unchanged `audit.py verify`, each in a separate subprocess. Child failure remains failure. No old bytes are overlaid into the caller checkout, and historical success explicitly makes no current-head claim.

The default combined scope is the explicit CLI action `all`; there is no automatic remote fetch. The original audit remains correctly red when directly run against current App/Sources.

## Provenance map

Exact full commit IDs and before/after SHA256 values live in the new verifier, with a pinned policy fingerprint. Every source transition is checked against both the exact authorization commit and its first parent. Consecutive App transitions must chain exactly from the original receipt. All commits must be ancestors of current HEAD, and authorization commits must descend from the historical V9 commit. Evidence documents are read from the exact commit, not mutable current files; their SHA256 values are emitted in the result.

| Original receipt path | Exact authorization sequence | Accepted intent and retained review |
|---|---|---|
| `App/GameScene.swift` | `8449f6d09932e5c977f495c66135a12b18554232`, then `bb874117fc53fabbc66c7925ee4eb519c2afbcef` | Production qualification directive, kiosk coordinator recommendation/actual playable review; then approved live projection intent and live projection coordinator review |
| `App/WorldRenderer.swift` | Same two commits | Same bounded Debug-only scopes and reviews |
| `Sources/SurveillanceCore/Contracts/GateRegistry.swift` | `0aa395145de56852722256590f8b74cf7fd17118` | Production qualification intent, issue257 gate census and retained red/green review in production execution README |
| `Sources/SurveillanceCore/Determinism/SHA256.swift` | `4294f737e20ff50900faa572768902c51fdca94e` | Production qualification hashing clause and HASH-PERFORMANCE review |
| `Sources/SurveillanceCore/Presentation/PresentationSnapshot.swift` | `fed8a3d18067c226376d9779f42bbc194dffcdab` | Production qualification umbrella and explicit issue260 coordinator authorization in SOCKET-ORDERING-REPAIR.md |

This binds the documented authorization record, not independent cryptographic proof of human approval. Repository policy/code review remains the trust boundary. It does not authorize any later source change, new artwork, acceptance, merge or release.

## CLI and coordinator integration

```sh
# Use a preexisting external scratch directory. On CI, create one under RUNNER_TEMP.
export JCODE_SCRATCH_DIR=/absolute/canonical/external/scratch
python3 -B -W error::ResourceWarning scripts/test_v9_preservation.py
python3 -B -W error::ResourceWarning scripts/verify_v9_preservation.py all --scratch-dir "$JCODE_SCRATCH_DIR"
# Diagnostic scopes, never describe historical-only as current-head validation:
python3 -B -W error::ResourceWarning scripts/verify_v9_preservation.py current
python3 -B -W error::ResourceWarning scripts/verify_v9_preservation.py historical --scratch-dir "$JCODE_SCRATCH_DIR"
```

Dependencies: Git, Python 3.9+ and Pillow for the original tests. No new package or tool dependency. Python/Git/Pillow are existing repository CI dependencies. Tests use local read-only Git object alternates in a separate temporary repository, not a worktree or clone/fetch, and copy only the protected files. Tests never create a commit or modify caller Git objects/index/files.

Recommended CI fetch strategy: `actions/checkout` with `fetch-depth: 0` for the reviewed branch. For an existing shallow checkout, the coordinator may separately run `git fetch --unshallow origin` before validation. The verifier itself never fetches. A shallow checkout with all required pinned commits, first parents and ancestry already available is sufficient. Missing commits, broken ancestry or missing tree/blob data fail with explicit fetch guidance. Partial/promisor clones are rejected before object operations that could lazy-fetch; Git replacement refs and environment redirection are disabled.

## Actual execution at implementation checkpoint

- Head: `1e8cbfef9a39d10277a19026d2a6debe4446cd4d`.
- `original-current-red.log`: unchanged original seven tests run against current checkout, exit1, one error `Protected bytes changed: App/GameScene.swift`. This preserves the real failure, not a simulated substitute.
- `integration-01.log`: first new integration attempt exited1 because the initial preflight rejected all shallow repositories. Diagnosis proved both historical and receipt-reference commits are actual ancestors locally. The blanket rejection was replaced with exact required-object/parent/ancestry validation. No history metadata was edited in the caller checkout and no fetch was performed.
- `integration-02.log`: combined verifier exit0. Current scope checks all1,766 paths (1,761 original, five exact transitions). Historical export verifies all11,432 tracked files. Original seven historical tests pass, then original audit reports1,766 protected files unchanged. Export automatically removed after execution.
- `git log -- docs/review/blocked-base-curb-relief-20261116` ends at6c3be49; `git diff --name-only 6c3be49 HEAD -- docs/review/blocked-base-curb-relief-20261116` is empty. The pinned publication already contains the final gallery fix/default. Its retained VALIDATION.md documents both final gallery suites. This worker did not rerun browser/native/gallery checks and does not relabel their historical evidence as new execution.

## Coordinator review follow-through: census and modes

The first22-test checkpoint above did not close the protected namespace or bind mode changes to an approved snapshot. Coordinator requested this explicit extension, rather than interpreting byte checks as proof of either property. Initial logs remain unchanged.

The hardened current scope pins approved commit `0c20990c8a6334b6c93d42db0336fc4cf2ab62f9`. Its protected tracked census must equal the original1,766 receipt paths plus only `App/KioskPlayableReview.swift` and `App/LiveWorldProjection.swift`, for1,768 total. Both new files have explicit SHA256 values verified at their exact authorization commits8449f6d/bb87411 and at0c20990. The original receipt still reports1,766 paths and is not replaced or enlarged. Separate output fields report the1,768 current census and two approved added files.

HEAD and index must have exactly that protected census. Nonignored untracked protected additions are rejected too. Every protected file and frozen audit/test/receipt must match the approved snapshot's Git blob identity and executable mode, not merely agree with an arbitrary later HEAD. The actual worktree must have the approved executable state. Restoring the worktree cannot hide staged mode changes. Current scope rejects new HEAD modes even if HEAD and index agree. Test fixtures use `copy2` to preserve mode rather than silently normalizing it.

Additional regressions cover added-file byte/missing/alias failures, source mismatches at each approval stage, extra/missing HEAD entries, unauthorized staged and untracked additions, changed approved census/policy, worktree executable changes and staged-mode drift. Final runs are retained separately: `tests-02.log` exited0 with **31 tests passed in126.917s**; `integration-03.log` exited0 at HEAD1e8cbfe with approved current census1,768, original receipt1,766, two added files, and the unchanged historical7tests/audit1,766 after full11,432-file export verification. No prior log was overwritten.

New guard test execution: `python3 -B -W error::ResourceWarning scripts/test_v9_preservation.py` exited0, **22 tests passed in59.419s**, retained in `tests-01.log`. Coverage includes all five unauthorized source mutations, immutable file/missing/alias cases, receipt/audit/test drift, rollback to historical App bytes, policy changes, source-at-authorization mismatch, staged tampering, broken history, unsafe archive extraction and child-failure cleanup. Any fault injection is confined to new verifier dependencies, never the frozen audit or frozen test semantics.
