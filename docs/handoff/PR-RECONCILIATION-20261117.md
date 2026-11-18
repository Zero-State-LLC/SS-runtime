# All-PR reconciliation, November 17, 2026

Owner request: update docs, board and handle all PRs, 04:04 UTC. Inventory fetched from GitHub at04:04-04:08UTC, covering SS-runtime, SS-specs and the frozen legacy Surveillance-Survivor repository. This is maintenance and disposition, not merge authorization. Main heads remain runtime `df8473713a3d37aeca05d4e1110f979f197b9ceb` and specs `983a4ca3427bd8a9d30056bccf356fe0f715312e`.

## Nine open PRs

| Repository / PR | Exact head inspected | Verified state | Disposition / remaining gate |
|---|---|---|---|
| SS-runtime #236 | b3c87c388b8d215f99fc2888b36241790e0b65f4 at intake | Five CI jobs queued in run44012617661, no review threads | Replace stale V8 description with current scope and evidence. Publish docs/preservation checkpoint separately from unfinished live-projection code. Broader presentation correction authorized, art remains NOT ACCEPTED. Exact new-head CI must be fetched separately. |
| SS-runtime #235 | dcf073c0f4ffd64d810d20eb476c14be82d25d9c | Five checks SUCCESS, mergeable, no review threads | Ready for owner review only. Depends on specs #115 first, then explicit runtime merge approval. Do not close receipt defects #233/specs #114 on branch evidence. |
| SS-runtime #234 | e10bb4969498c081229b996b5feae23c9eeb1be2 | Five checks SUCCESS, mergeable, no review threads | QA evidence remains separate and valid for its recorded heads. Keep intentional archived-receipt failure and physical/human limitations. Await owner merge approval. |
| SS-runtime #167 | 4a525f1791257760a00c6054cec2c36f5832f221 | Four historical checks SUCCESS, APPROVED, targets feat/d120-shell-copy | Parent #166 merged November2. Main comparison diverged:3ahead/58behind,12changed paths. Do not blindly retarget or merge historical stack and reintroduce shell/pin changes. Requires isolated rebase/patch reconciliation against accepted D-121 and owner merge authorization. D-122 remains proposed in specs #92. |
| SS-specs #115 | 354c1f4bcc7a485ad4fc5d7d7ac8c77c3180165f at intake | Validate SUCCESS, REVIEW_REQUIRED, mergeable, no review threads | Update canonical docs/kanban and handoff only. Retain receipt candidate contract pin194ded9 and specification-first adoption order. Owner code-owner review and merge gate remain. |
| SS-specs #92 | 9ea2a365a9c0cc3e58a746ddf62ee20d23b4c4d3 | Historical Validate SUCCESS, APPROVED, CONFLICTING;4ahead/20behind | Record actual conflict and missing T1060 review plates. Do not silently select product semantics while resolving conflicts across decisions/tasks/visual requirements. Owner D-122 decision and current-main conflict reconciliation precede merge. |
| SS-specs #63 | f129911ea3d12fb7e0070b505fadb372c1575080 at intake, repaired c2260857251d826f80c0455a5b6d8534834dff19 | Two unresolved review findings found and fixed. Local validator passes21JSON/6schemas/33contracts/49indexed files. New-head Validate running at04:08UTC | Published narrow documentation repair: NOT_COMPUTABLE listening claims and separate runtime-file question preserving distinct existing asset IDs. Both review threads replied to and resolved. Draft intent, listening, provenance/licence and owner acceptance gates unchanged. |
| Surveillance-Survivor #25 | 60565c6b203dc3c47bb254f3daffc90dab621fb1 | Two historical failures, REVIEW_REQUIRED, mergeable | Actual job annotations say jobs never started because account payments/spending limit blocked execution. This is not a compiler/test failure. No billing change or blind rerun. Frozen legacy maintenance and merge require owner decision. |
| Surveillance-Survivor #24 | b926da811ae47c96ef46f0c7c0a817cbbe9065f5 | Two historical checks SUCCESS, REVIEW_REQUIRED, mergeable | Historical roadmap-only maintenance, not reboot release evidence. Keep separate from canonical specs/runtime board. Frozen legacy/owner merge gate remains. |

All seven runtime/specs PRs and both legacy PRs were inspected for review threads. Only specs #63 had unresolved threads; both were addressed without changing product behavior. No PR, issue, branch or historical evidence was deleted or closed. No merge, auto-merge, approval, release, paid action or protection bypass is authorized by this maintenance request.

## Current engineering checkpoint

Runtime local commit `a00b184` records the live-action probe defect and strengthens the frozen-path guard against a staged change concealed by restored worktree bytes. Six isolated Git tests pass, with actual11876protected files unchanged. The 03:50 native projection run is17passed/1failed, zero skips. Failure is the test-owned root action being cleared by the existing Player clip transition, not an established runtime animation defect. Frozen source, result bundle and logs are retained. Runtime issue #261 now tracks it. Native retry0407 subsequently passed18/18,0skips. Coordinator independently matched all8source/product hashes, inspected current/candidate live-app frames and default restoration, and verified final Release exclusion across1032PNGs. See `../review/live-world-projection-20261117/COORDINATOR-REVIEW.md`.

Live projection implementation is cleared for Debug-only review publication after the native retry, independent review, real-app inspection and Release exclusion checks. No visual acceptance is claimed. Only the Camera-adjacent kiosk was authorized for source geometry correction. Neighbor designs and all authoritative geometry remain frozen. Earlier no-broader-projection stop was superseded by owner approval at03:40UTC, not by art acceptance.

## Board policy

Project27 is the canonical cross-repository benchmark board. Preserve historical runtime#131 Done/CLOSED and specs#65 InProgress/CLOSED without treating either as new family acceptance. Runtime#132/#133 stay InProgress. #134/#135 stay Todo behind family/device/human gates. Implemented-but-unmerged repairs #238/#256/#257/#258/#260 are InProgress, not Done. Unresolved intermittent #237 and capture timeout #259 stay Todo. New test-instrumentation #261 is InProgress. No issue lifecycle change follows from a board edit.

## Publication follow-through, 04:14UTC

Specs docs published6ae68db with10consistency tests and full validation passing, unchanged contracts/fixtures/specification bytes. Specs63 exact repaired headc226085 passed remote Validate44015043483 and both review threads are resolved. Maintenance comments posted to runtime234/235/167 and specs115/92/63. Legacy25 comment attempt was rejected because Surveillance-Survivor is archived/read-only; `gh repo view` independently confirms `isArchived:true`. Legacy24/25 dispositions therefore remain in these canonical docs, not falsely reported as remote comments. No unarchive or closure attempted.

Project27 overview was updated and read back byte-for-byte against `BOARD-20261117.md`;14cards and all intended statuses were independently fetched. Runtime133/261 received current evidence comments. Final runtime publication and exact-head CI are recorded in NEXT.md.
