# Rejected 21:20 native execution

Xcode reported `TEST SUCCEEDED` but the selected v6 identity executed zero tests. The strict importer returned exit 2 (`Wrong exact v6 test identity`) and created no capture packet. This is not successful evidence.

The build log confirms compilation of `SceneQAFramingTests.swift`. Exported runner diagnostics then identify the loaded test bundle under `Library/Caches/com.apple.containermanagerd/Dead/temp.HQD4Dv/C87EB2CB-EA4F-42CA-B4AE-F3B2241D6E5D/`, rather than the newly installed application container. Preserved files:

- `native-run-2120.log`
- `zero-tests-2120-summary.json`
- `rejected-zero-tests-2120.log`
- `stale-loaded-bundle-2120.log`
- `stale-binary-hashes-2121.txt`

The loaded retired executable hashes to `f61ad09650b403b926caf38937f925cb773107a7f8d8baece3f2e1c8e39b4af2`, matching the earlier v4 test build. The currently installed executable and fresh build both hash to `4bc45a685a0098b91cd6210829a92c60276db9d1fc6635c3c23b49753c52e7f4`. This proves stale-bundle selection, not a missing v6 compilation. The underlying simulator/cache retention mechanism remains unproven, as in issue #241.

At 21:22 UTC the coordinator performed one non-erasing shutdown/boot of the dedicated simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3 before a single bounded retry. No source, selector, image, assertion or expected test count was relaxed. The first app-container lookup used an incorrect guessed identifier and failed without mutation. The corrected identifier was read from `project.yml`: `com.zer0state.surveillancesurvivor`.

A retry is admissible only if exactly one selected test executes, all six capture records/eighteen PNGs validate, and the actual loaded executable matches the fresh build. Neither Xcode's process exit 0 nor the nominal success banner suffices. Issue #241 remains open.
