---
title: Historical preservation receipts need a separate current-change boundary
author: Daniel
date: 2026-11-18
branch: qa/bp001-projection-decision-20261116
id: l-0d06871a
scope: repo
status: active
src: agent
touches:
  - ".github/workflows/ci.yml"
---

## Decided
Keep a completed review packet's original receipt and audit unchanged. Verify that historical claim against its exact published Git snapshot, then independently enforce current protected bytes with only exact provenance-bound transitions for later approved work. A historical pass must never be labeled current-head success.

## Tried and ruled out
Running the frozen V9 no-runtime-change audit against the later live-projection head fails honestly on App/GameScene.swift. The exhaustive receipt comparison found five later authorized changes among1766 paths, including gate census, hashing and snapshot ordering. Regenerating the receipt or excluding App/ and Sources/ would conceal arbitrary drift and destroy the original evidence, so neither is a repair.

## In the code
Original receipt and checks: docs/review/blocked-base-curb-relief-20261116/{protected-files.json,audit.py,test_audit.py}. Integration point: .github/workflows/ci.yml, Verify bounded base and curb comparison without admission. New boundary: scripts/verify_v9_preservation.py, scripts/test_v9_preservation.py. Failure evidence: docs/review/preservation-scope-20261118/ci44016077111-failed.log, issue262. Scope: intent/2026-11-18-preservation-verification-scope.md.

## Watch out
Git-backed historical verification needs pinned objects and ancestry. Supply them explicitly in CI, do not make the verifier fetch. Keep staged/index checks as well as worktree checks so restored bytes cannot hide a staged violation. None of these checks establishes art, physical-device or release acceptance.
