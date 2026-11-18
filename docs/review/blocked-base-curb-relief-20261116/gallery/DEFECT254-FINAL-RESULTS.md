# Defect 254 final publication results

Final run completed 2026-11-17 at 00:29:08 UTC, exit 0. Gallery implementation is frozen for coordinator browser/export follow-through.

Commands:

```sh
node docs/review/blocked-base-curb-relief-20261116/gallery/test_evidence.js --require-v9
node docs/review/blocked-base-curb-relief-20261116/gallery/test_loader.js --require-v9
```

Evidence result: PASS, actualVersions=3, actualImages=54, selections=96, rejectedMutations=238, syntheticV9Protocol=true, v9NativeEvidence=true, browserEvidence=false.

Loader result: PASS, missingV9=true, mismatchedCaptureRejected=true, corruptedPNGRejected=true, corruptedRecordRejected=true, missingDependenciesRejected=true, missingDependencyCases=869, sourceForgeryRejected=true, binaryForgeryRejected=true, noFallback=true, actualVersions=3, syntheticV9Loader=true, selections=144, browserEvidence=false, nativeRun=false.

Exact final logs: `defect254-publication-final-evidence.log`, `defect254-publication-final-loader.log`. Both include actual retained V9 records, not only synthetic protocol data. Missing default V9 is independently exercised with valid V8 available and must issue only the two V9 initial requests, keep controls disabled, produce no images or object URLs, and never fall back. Earlier unavailable-real-evidence required-mode failures remain retained separately.

Changed implementation/documentation: `gallery.js`, `test_helpers.js`, `test_evidence.js`, `test_loader.js`, `index.html`, `README.md`, `DEFECT254-VALIDATION.md`, this receipt and preserved test logs. Source attempts, historical packets, scene and native bytes remain untouched by this task. No build, browser, commit or push performed. Node results do not satisfy browser or owner acceptance. Coordinator authorization alone changed the review default to V9. Overall benchmark NOT MET, V8 and V9 unaccepted, no third source attempt.
