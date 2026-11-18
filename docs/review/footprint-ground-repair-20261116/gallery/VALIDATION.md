# Gallery worker validation, November 16, 2026

## V8 default follow-through, 23:28-23:29 UTC

Coordinator authorized the gallery-only V8 default after reporting a real import and actual browser success. This worker first ran the evidence suite with `--require-v8` successfully, then changed only gallery JS/HTML/default regressions and documentation. Missing/corrupt evidence handling remains unchanged.

Commands rerun after the default change:

```sh
node docs/review/footprint-ground-repair-20261116/gallery/test_evidence.js --require-v8
node docs/review/footprint-ground-repair-20261116/gallery/test_loader.js --require-v8
```

Both exited 0. Evidence suite: 2 actual versions, 36 PNGs, 48 selections, 79 rejected mutations, real V8 evidence present. Loader suite: 2 actual versions plus explicit synthetic V8 protocol responses, 108 selections, all missing/corrupt/source/binary forgery checks passing. Its `missingV8:true` output denotes the simulated missing-V8 rejection test, not absent retained V8 evidence. The DOM/network harness remains synthetic and neither suite constitutes actual browser execution. Explicit regressions now require V8 in both JS and HTML and verify the missing default V8 fails closed.

Separately, the coordinator's 23:28 UTC message reports a fresh-binary retained check passing six V8 captures/eighteen images/nine baseline RGBA matches, plus actual Brave passing 72 selections/96 image displays across V7/V8 with zero sizing, grayscale or count errors. Those are coordinator-reported results, not browser/native commands executed by this worker. No post-default-switch actual browser run is claimed here.

V8 is now the review-only default, not accepted. V7 remains immutable. No scene changes, native/Swift retry, browser execution, commit or push by this worker.

## Historical initial implementation validation, 23:07 UTC

Commands run from repository root:

```sh
node docs/review/footprint-ground-repair-20261116/gallery/test_evidence.js
node docs/review/footprint-ground-repair-20261116/gallery/test_loader.js
```

Observed results:

- Evidence suite PASS: 1 actual capture version (immutable V7), 18 actual PNGs, 24 image selections, 48 rejected mutations. Explicit synthetic V8 protocol test passes. V8 native evidence: false. Browser evidence: false.
- Loader suite PASS: 72 control selections across actual V7 data and explicitly synthetic in-memory V8 data. Missing dependencies, mismatched version, corrupt PNG/records/source, incoherent binary hashes, coherently stale V7 binary and coherently rewritten immutable records all rejected. No fallback. Browser/native run: false.
- Both commands with `--require-v8` returned exit 1 with `Actual v8 evidence required`, checked with Node `spawnSync` assertions. This is the expected missing-real-evidence gate, not a passing native capture.
- `git diff --exit-code -- docs/review/building-perspective-detail-20261116` returned exit 0. No old tracked packet bytes changed.

At this earlier checkpoint no Swift/native retry, browser execution, commit or push occurred. Standing handoff forbids unfiltered Swift retries after prior timeouts. V7 was then the default and real V8 was absent. The later evidence-backed default change is recorded above. No visual acceptance is claimed.
