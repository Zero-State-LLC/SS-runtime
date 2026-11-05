# Expansion gate

Read 2026-11-05 from `ExpansionGateEvaluator.evaluate` on `ef68565`. No decision string was changed.

The written filename stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md). The three-success bundle stays in [retest-checklist.md](retest-checklist.md).

`passed` is `EXPANSION_GATE_PASSED`. `failed` is `EXPANSION_GATE_FAILED`. `notComputable` is `EXPANSION_GATE_NOT_COMPUTABLE`. An open severity-one count above 0, or an open severity-two count above 0, returns `failed`. While `d013Settled` is false, or `d021Settled` is false, the result is `notComputable`.

The required families are `GateRegistry.functional`, `determinism`, `stability`, `visual`, `arena`, `accessibility`, and `playtest`. A missing required id returns `notComputable`. A required result whose `passed` is false returns `failed`. Every required result `passed` returns `passed`. Any other shape returns `notComputable`.

`defaultInputsFromRegistry` marks each `GateRegistry.evidence` entry whose kind is `automatedTest` as passed, and sets both settled flags false, so that input evaluates `notComputable`. `ExpansionGateReporter.evaluate` stores the decision `ReleaseCandidateEvidenceCollector.collect` computed, the open counts, the settled flags, the linked automated count, the pending count, and the sha256 of that candidate's canonical JSON. The report schema is `expansion-gate-report-001`.

This does not close T908.
