# Playtest gates

Read 2026-11-05 from `PlaytestEvidence.gateResults` on `ef68565`. No gate count was changed.

The file load stays in [playtest-load-2026-11-05.md](playtest-load-2026-11-05.md). The directory stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md).

The schema is `playtest-evidence-001`. For `T903`, `G-001` passes when the session count is at least 5 and at least 4 sessions completed onboarding without instruction. `G-002` passes when the session count is at least 5 and at least 4 sessions described exposure correctly. For `T904`, `G-004` passes when the session count is at least 5 and at least 3 sessions began a voluntary replay. Any other task id returns an empty list. The source on each of those records is `playtest`.

The canonical session stores `competentRunDurationMinutes` as the integer of `rounded()`, or null when the minutes are absent.

This does not close T903 or T904.
