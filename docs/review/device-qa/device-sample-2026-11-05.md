# Device sample

Read 2026-11-05 from `DeviceTelemetrySample.capture` on `ef68565`. No thermal label was changed.

The baseline phone sentence stays in [retest-checklist.md](retest-checklist.md). Frame percentiles stay in [frame-times-2026-11-05.md](frame-times-2026-11-05.md). The file that stores this sample stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md). Which outcomes are finished stays in [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md).

`hardwareModel` is the `utsname` machine bytes up to the first zero. `capture` reads `resident_size` through `task_info` with `MACH_TASK_BASIC_INFO`. A result other than `KERN_SUCCESS` stores 0. The thermal label is `nominal`, `fair`, `serious`, `critical`, or `unknown`. The memory-warning count is the integer passed in.

`RunInstrumentation.noteMemoryWarning` adds one to that count. `recordSimulation` stores the first sample as the peak. A later sample replaces the peak when its `totalLive` is greater. `totalLive` is cameras, enemies, projectiles, mines, and the civic pool, added. A sample whose outcome is not `playing` replaces `terminalTelemetry`, including the upgrade choice. `evidence` uses schema `run-instrumentation-001` and carries the frame summary, `capture` of the warning count, the peak, and the terminal sample. `reset` clears the frame collector, the warning count, and both snapshots.

This does not label a phone.
