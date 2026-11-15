---
title: Green receipt suites do not prove pinned schema conformance
author: Daniel
date: 2026-11-15
branch: qa/2026-11-15
id: l-f624fc82
scope: repo
status: active
src: agent
---

## Decided
- Validate the actual archived run JSON against the bundled pinned schema independently of passing receipt unit suites. CombatAuthorityReceiptTests explicitly assert extractionArmed and reject nested extraction, so their green result cannot establish schema conformance.
- Escalate the contract/test contradiction instead of changing schema, tests, fixtures or pins to force green, as AGENTS.md requires.
## In the code:
- Sources/SurveillanceCore/Events/RunReceipt.swift:108-151 emits extractionArmed, root camera summary fields and a string upgrade.
- Sources/SurveillanceCore/Resources/contracts/run-receipt-001.schema.json requires extraction, rejects unknown root properties and permits only object/null upgrade.
- Tests/SurveillanceCoreTests/CombatAuthorityReceiptTests.swift:25-27 has conflicting shape assertions.
- docs/review/qa-2026-11-15/validate-live-receipt.py independently reproduces all three errors with the archived receipt.
