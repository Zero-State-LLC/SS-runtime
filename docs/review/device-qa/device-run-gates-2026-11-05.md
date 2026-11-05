# Device-run gates

Read 2026-11-05 from `DeviceRunEvidence.gateResults` on `ef68565`. No gate was changed.

The filename stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md). Gate C's thresholds stay in [frame-times-2026-11-05.md](frame-times-2026-11-05.md). The phone sample stays in [device-sample-2026-11-05.md](device-sample-2026-11-05.md). The streak stays in [run-streak-2026-11-05.md](run-streak-2026-11-05.md). The three-success bundle stays in [retest-checklist.md](retest-checklist.md).

The schema is `device-run-evidence-001`. The task id is `T905`. `performanceFloor` counts a thermal state of `serious` or `critical` as one event, and every other string as zero. Its device-class parameter defaults to the string `iPhone 12`. The session call passes `hardwareModel`.

`C-001` passes when the consecutive count is at least 3, frame time passes Gate C, memory warnings are 0, and thermal events are 0. `C-002`, `C-003`, `C-004`, `C-005`, and `C-006` pass when frame time passes Gate C. `C-007` passes when thermal events are 0. The source on each record is `deviceCapture`.

`settledD021Ceilings` returns nil unless both resident bytes and atlas bytes are present. When both are present it returns the simulation ceilings after `withDeviceProfiling`. The session passes nil for the atlas bytes. The detached task returns before `exportReleaseCandidateWithBundledPlaytests` when those settled ceilings are nil.

This does not label a phone.
