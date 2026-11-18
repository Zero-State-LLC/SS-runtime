# Independent validation, November18 2026

## Confirmed before publication

- Re-fetched exact failed CI44016077111 at0c20990. Preserved raw job JSON and failed log. Original V9 audit independently reproduced seven tests with one error on GameScene, exit1.
- Exhaustive original receipt comparison:1766 protected files,1761 identical and exactly5 changed, no missing files. Exact hashes and implementation provenance are enforced by the new verifier, not a blanket directory exception.
- `swift test --filter 'AcceptedGateCensusTests|GateVerificationTests|SHA256ParityTests|PresentationSocketOrderingTests'`: exit0, **19 tests in4suites**, raw `swift-focused.log`. This is focused qualification, not a newly executed full native or host suite.
- All eight unchanged current-checkout V9 commands following the historical preservation checks: exit0. **25 first-source +13 final-source +5 runner +46 scene tests**. Retained native verifier reports6captures/18images, baseline checker compares9full RGBA images. Evidence gallery reports54actual images,96selections and238rejected mutations. Loader reports144selections and869missing-dependency cases rejected. Raw `current-v9-checks.log`. This is retained-evidence validation, not a new native/browser run or visual acceptance.
- Downstream CI steps:7playback-trace tests,2spec-parity isolation tests, and actual contract/fixture parity against pinned SS-specs `b1ed874e1e8eb0e61b2174b9093201e9a61e1a4b` all pass, exit0. Raw `post-v9-ci-tail.log`. These do not resolve the historical playback237 issue.
- Existing runtime wiring guard:5tests pass. Workflow YAML parses and spec-parity checkout has `fetch-depth:0`; historical verifier itself does not fetch.
- Independent code review requested additional census and executable-mode protections before publication, beyond the first22-test implementation checkpoint. Final worker run passed **31 new guard tests in126.917s** (`tests-02.log`), and the combined integration passed (`integration-03.log`). Current guard checks1768paths (original1766plus2exact authorized additions), approved modes, HEAD/index/worktree consistency and rejection of new unapproved protected files. Historical export independently checks11432Git blobs before running the unchanged seven historical tests and original audit. Earlier implementation evidence remains retained, not overwritten. Coordinator independently reviewed the code and verified source SHA256 identities before the separate export run.

## Publication validation

The final new guard and the literal affected workflow step must pass in an isolated staged-only export before publication. `validate_export.sh` creates a local temporary commit object and standalone temporary repository using read-only local object alternates, then checks out only indexed files. It does not alter the source branch or include unrelated untracked art. Ruby's existing YAML parser extracts the actual CI step rather than maintaining a substitute command list. Historical/current guards, unchanged V9 checks and downstream CI checks run there. The owned scratch export is retained for inspection.

Final independent export completed **exit0 at22:21UTC**, duration363.64seconds. Snapshot `8c757f1b321d2909afbc978b2d3c8aae73075f1e`, indexed tree `3adb30fc965982da8c77a4dc4faf0d5cceef16f9`, base `1e8cbfef9a39d10277a19026d2a6debe4446cd4d`, retained directory `$JCODE_SCRATCH_DIR/ss-preservation-export.yeNt3X`. Raw complete output: `tracked-export-validation.log`.

The literal CI step passed31new guard tests (116.792s), the original7historical tests and original1766-file audit after11432-file historical export verification, then all89current V9 Python tests and unchanged retained-native/pixel/gallery checks. Downstream5runtime-wiring +7trace +2isolation tests and real pinned contract parity also passed. Thus141Python tests ran in this export across the affected step and downstream checks. These are not additional distinct tests beyond the named earlier executions. Export ended with clean tracked/untracked Git status. No unrelated untracked art was present.

`validated-source-sha256.txt` binds both new scripts and CI YAML. Coordinator checked those hashes again after export. Final publication adds only completed documentation/log records to this verified code/configuration. No current/future remote CI success is implied. Trail's lexical census warning and raw-log whitespace preflight are explicitly dispositioned in `TRAIL-CHECK.md`, not reported as passing checks.

## Preservation and acceptance

No App, Sources, AppTests or old V9 packet bytes are changed by this repair. Original V9 audit/test/receipt remain frozen. Existing six untracked art/work-order paths remain untouched. Issue262 remains open and In Progress on Project27. No merge, auto-merge, release, issue closure, new source-art attempt or physical/human acceptance. Visual benchmark remains NOT MET.
