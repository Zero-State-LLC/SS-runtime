# Publication verification, November17 03:10UTC

The finished flat source/native comparison and preserved-material textured source are separate from the ongoing Debug playable integration. The latter remains under `native/playable/` and is deliberately excluded from this publication slice. No canonical assets, neighboring buildings, gameplay, acceptance or release authority changed.

## Observed results

- Original checkout:19source tests and15native-adapter tests passed exit0 at03:02UTC. Independently,12textured tests and7actual retained-evidence regressions passed at02:55UTC. Raw coordinator logs retained alongside this document.
- Original `output/` and `reproduction/`: `diff -qr` exited0 at03:02UTC. Filesystem allocated-block differences were not byte differences.
- Staged-only export of11869tracked/indexed files under `$JCODE_SCRATCH_DIR/ss-kiosk-staged-export-20261117-0303`:19source and15adapter tests passed. This export excludes unrelated untracked packets and all in-progress App/playable changes.
- The first export command then failed the retained suite's positive case because `native/test_retained.py` requires its local ignored DerivedData test executable. This was a real exit1, preserved in `staged-export-attempt01.log`. It is not a missing source dependency or a native test assertion failure. The suite is native-product-dependent, not a portable clean-checkout test.
- Corrected invocation used the existing documented `native/retained.py capture-01 --test-executable ORIGINAL_PRESERVED_BUILD_PRODUCT` interface against the staged-only sources/capture and the original binary. It passed strict source/receipt/loaded-binary/authority/pixel checks:6captures,18images,3outside-kiosk-canvas pair comparisons. Expected/loaded executable SHA256 remains `45d02db24f86d132536e2bd46ff2b9b63d82bcd8817a21e9f90b77135ac8efff`. This is explicitly an external native-build prerequisite, not a fresh checkout containing that binary.
- The remaining staged-only12textured tests passed exit0. No validator, expected image, native receipt or test assertion was edited to obtain success. No native rerun was made.

## Whitespace check disposition

Unrestricted `git diff --cached --check` reported whitespace inside preserved raw compiler logs, a captured diff and the Trail progress log. Those artifacts remain byte-exact rather than being cosmetically rewritten. The source/document check excluding only `*.log` and `*.diff` exited0. Do not report the unrestricted check as passing.

## Visual verdict

Coordinator inspected all six native half-scale frames and the textured source comparison. See `COORDINATOR-REVIEW.md`. Lower crown is worth opt-in live review, but horizontal adjacency and raised-base reading remain unresolved. The flat fixture is not textured playable evidence. Benchmark NOT MET, no owner art acceptance or production admission.
