# The candidate the collector builds

Read 2026-11-05 from `ReleaseCandidateEvidenceCollector.collect` on `ef68565`. No ceiling was settled. The decision stays in [expansion-gate-2026-11-05.md](expansion-gate-2026-11-05.md). The identity and the pin stay in [replay-identity-2026-11-04.md](replay-identity-2026-11-04.md). The file name stays in [evidence-names-2026-11-05.md](evidence-names-2026-11-05.md). The profile stays in [peak-density-2026-11-05.md](peak-density-2026-11-05.md). The ceiling statuses stay in [ceiling-status-2026-11-05.md](ceiling-status-2026-11-05.md). The triple run stays in [replay-matrix-2026-11-05.md](replay-matrix-2026-11-05.md). The gate spans stay in [gate-spans-2026-11-05.md](gate-spans-2026-11-05.md).

The evidence schema is `release-candidate-evidence-001`.

`DefectRegistry.tracked` is empty. `openSeverityOneDefects` and `openSeverityTwoDefects` count open records of those severities, so both are 0. Its canonical object uses schema `defect-registry-001` and stores those two counts plus the tracked records. A missing task reference is null.

`Options` uses those registry counts when the caller passes nil. `d013Settled` defaults false. The playtest list and the device list default empty. `d021DeviceProfiling` defaults nil.

`collect` profiles, then builds ceilings with `D021Ceilings.fromSimulation`. A supplied device value replaces that object. It stores each loaded replay-matrix entry's triple-run digest. For each upgrade it makes a simulation at seed 1, runs `testing_completeRunSuccess`, and stores `terminalDigest`, or `digest()` when that is nil.

Gate results start as each automated evidence id with `passed` true. Playtest results and device results are appended. The linked automated ids are the automated evidence ids, sorted. The pending ids are the required families minus the supplied ids, sorted.

The record stores `ContractVersions.specificationCommit`, `ReplayIdentity.current`, those maps, the linked ids, the pending ids, the decision, the open counts, `d013Settled`, whether the ceilings are settled, the sha256 of the peak canonical JSON, and the ceilings.

Ordinary play does not call `collect`.

This does not close T905 or T908.
