# Evidence names

Read 2026-11-05 from `ReleaseEvidenceStore` on `ef68565`. No filename was changed.

The export paths, the `QA_DAMAGE` lines, and the three-success bundle stay in [retest-checklist.md](retest-checklist.md). The 512-record log and the QA flag stay in [damage-log-2026-11-05.md](damage-log-2026-11-05.md). Gate C on the device-run record stays in [frame-times-2026-11-05.md](frame-times-2026-11-05.md). The playtest objects stay in [playtest-load-2026-11-05.md](playtest-load-2026-11-05.md).

The store uses the Application Support subdirectory `ReleaseEvidence`. A device run is written atomically as `device-run-<class>-<count>.json`. The class is `deviceClass` with each space replaced by a dash and then lowercased. The count is `consecutiveCompleteRuns`. The bytes are `evidence.canonical().serialize()`.

A release candidate is `release-candidate-<digest>.json`. The digest is the first 12 characters of `peakDensityDigest`, the sha256 hex of the peak report's canonical JSON. `PlaytestSessions` is created under `ReleaseEvidence`. `exportReleaseCandidateWithBundledPlaytests` loads that directory, writes the candidate, then writes the expansion-gate file. That file is `expansion-gate-<decision>.json`, with the decision's raw value lowercased.

`makeDeviceRunEvidence` calls `DeviceRunEvidence.performanceFloor` with the device class, the consecutive count, `frameTime.passesGateC()`, the memory-warning count, the thermal state, the resident bytes, and the atlas bytes. The session passes nil for the atlas bytes.

This does not write a file during ordinary play.
