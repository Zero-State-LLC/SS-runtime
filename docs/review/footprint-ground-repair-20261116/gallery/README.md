# Footprint-ground comparison gallery

Scope: only this new `gallery/` directory. Approved work order: `intent/2026-11-16-footprint-ground-consistency.md`. V7 remains owner-rejected and immutable. The default is now V8, authorized by the coordinator at November 16, 23:28 UTC after real `../scene/native-capture-v8/` evidence was imported and browser review reported. This worker independently passed both `--require-v8` Node suites before handoff. The gallery remains review-only, not accepted, and every load must verify its evidence before displaying captures. No native run, browser run, commit or push is performed by this worker.

## Adaptation and contract

ADAPT, read-only: `docs/review/building-perspective-detail-20261116/gallery/gallery.js:1-225`, `index.html:1-46`, `gallery.css:1-25`, and its two Node test harnesses. Historical bytes are not edited or copied as new native evidence. The original uncropped benchmark remains the shared `stone-painted-facade-20261116/inputs/benchmark.png`.

Exact V8 contract read from Jaguar's `scene/native.py:29-38,141-202`: fixture `source-scene-footprint-008-ground-plan`, record schema `source-scene-records-008`, six ordered `control`/`candidate` captures at 1/1.25/1.4. Internal arms remain those exact strings. Display labels are **baselineV7** and **candidateV8**, with exact roles `BASELINE_V7_CANDIDATE` and `CANDIDATE_V8_SHARED_GROUND_PLAN`.

The loader requires one native test, six records, eighteen PNGs, every image digest and decoded dimensions, importer/record agreement, immutable V7 record SHA256, actual assembly/input/harness/source-image byte hashes, and for V8 actual shared-plan bytes plus all nine frozen V7 source hashes. Loaded binary SHA must agree with expected-build and record SHA; V8 cannot reuse V7's binary. Source filenames cannot escape the review subtree. Missing/corrupt evidence clears the prior display, disables controls and never falls back. All images are verified before any is displayed.

Native/half dimensions are exactly 704×326 / 352×163 logical CSS pixels, independent of capture pixel density. The frame scrolls rather than shrinking images. Grayscale selects retained grayscale capture PNGs; the uncropped original reference uses a reversible CSS filter.

Checksums establish consistency, not independent authenticity of an unsigned importer report. Actual native provenance/semantic validation remains the scene importer's responsibility, with coordinator review required. No visual, production, physical-device or owner acceptance is inferred.

## Validation commands

```sh
node docs/review/footprint-ground-repair-20261116/gallery/test_evidence.js --require-v8
node docs/review/footprint-ground-repair-20261116/gallery/test_loader.js --require-v8
```

Real V8 is now required for handoff. The `--require-v8` option must fail if evidence is absent. The ordinary suites also verify real V8 whenever its verification file exists, rather than silently skipping corrupt/incomplete packets. Explicit regressions assert V8 is selected in both JS and HTML and that a missing default V8 packet still fails closed without falling back to V7.

The Node DOM/network harness is explicitly synthetic. `syntheticV8()` creates only in-memory protocol responses using retained V7 image bytes to exercise version semantics, labels, all 36 controls, dependency deletion and forgery rejection. It never writes a capture, and is not V8 native or browser evidence. Actual retained-file checks now inspect all 36 PNGs across real V7 and V8 packets. The loader exercises 108 selections: 72 using those actual packets and 36 using the explicit synthetic V8 protocol fixture, all within the synthetic DOM harness. Tests additionally reject coherent immutable-record changes, stale V7 binaries, wrong source/plan/role/schema fields, mismatched records/PNGs and every missing fetched dependency.

Coordinator-reported evidence, distinct from this worker's Node checks: the November 16, 23:28 UTC message reports independent fresh-binary validation of six V8 captures/eighteen images/nine exact baseline RGBA matches and actual Brave coverage of 72 selections/96 image displays across V7/V8 with zero sizing, grayscale or count errors. The worker did not execute that browser or independently rerun the native provenance command. These reports do not imply owner acceptance.

Serve the full repository over localhost/HTTPS, not only `docs/review`, because harness and source dependencies are required. The coordinator reported full-repository port 8769 working and review-only port 8768 correctly failing dependency checks. Coordinator follow-up is diff review and any fresh browser confirmation of this default-only change, followed by publication as authorized. No scene or historical packet files were changed by this follow-through.
