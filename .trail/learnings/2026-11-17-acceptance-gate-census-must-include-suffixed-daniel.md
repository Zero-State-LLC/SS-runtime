---
title: Acceptance gate census must include suffixed and later adopted gates
author: Daniel
date: 2026-11-17
branch: qa/bp001-projection-decision-20261116
id: l-38a770fe
scope: repo
status: active
src: agent
touches:
  - ".github/workflows/ci.yml"
  - Sources/SurveillanceCore/Contracts/GateRegistry.swift
  - Tests/SurveillanceCoreTests/GateVerificationTests.swift
  - docs/handoff/NEXT.md
  - docs/review/production-execution-20261117/README.md
  - scripts/spec_parity.sh
---

## Decided
Release qualification must enumerate every accepted gate, including letter-suffixed IDs. Count-only tests inherited an obsolete115-gate census and allowed false PASS when five accepted gates were absent or failed. Test exact accepted membership and each missing/failed gate.
## In the code:
Sources/SurveillanceCore/Contracts/GateRegistry.swift now includes A-013A,D-022,D-023,D-024,E-021. Tests/SurveillanceCoreTests/AcceptedGateCensusTests.swift records the red-to-green cases. ExpansionGateEvaluator uses these families, so omissions propagate into release decisions. These tests do not constitute visual/device acceptance.
