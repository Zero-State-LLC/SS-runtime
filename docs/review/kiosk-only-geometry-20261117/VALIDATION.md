# Validation and handoff

2026-11-17. Implementing worker validation, not coordinator art acceptance. Source-only packet, no simulator execution. Inherited subscription route used, no paid external calls. No commit, merge, release or deploy.

## Executed checks

1. `PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/build.py` passed. Three comparison zooms1/1.25/1.4,54output files including manifest. Log: `build-initial.log`.
2. Same builder with `--out docs/review/kiosk-only-geometry-20261117/reproduction` passed. `diff -qr docs/review/kiosk-only-geometry-20261117/output docs/review/kiosk-only-geometry-20261117/reproduction` exited0 with no differences. All54files, including manifest, reproduce byte-for-byte. Log: `reproduction.log`. This is the same frozen candidate, not another aesthetic attempt.
3. `PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/export_editable.py` passed. Original indexed mesh6330vertices,1582faces, face/UV arrays exact, candidate vertices match rendered proxy face-for-face. Log: `editable-validation.log`.
4. `PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/test_packet.py` passed19tests in15.568s. Log: `tests-final.log`. Initial16-test run also passed, retained in `tests-initial.log`.
5. `swift test --scratch-path docs/review/kiosk-only-geometry-20261117/.swift-build --filter 'CameraMountSolidTests|CameraHousingArtTests|EnvironmentContractTests'` passed8Swift Testing tests in3suites. Log: `swift-focused.log`. XCTest's zero-test preamble is not the Swift Testing result. No unfiltered suite or simulator run. Build products remain ignored inside this owned directory.
6. `git diff --exit-code` and `git diff --cached --exit-code` both exited0 at02:17UTC. No tracked source, output, manifest, App, Tests, specification or shared handoff file was edited by this worker. Starting unrelated untracked packets were not edited. This is not a claim of a global byte audit of those unrelated untracked files.
7. Actual `comparison-z100.png`, `comparison-z125.png`, `comparison-z140.png` viewed through image tool. Observations and remaining artistic uncertainty are in `README.md`. Coordinator still must inspect them independently.

## Exact hashes

| Artifact | SHA256 |
|---|---|
| `output/manifest.json` | `ea13512b2db1cf0975c7daf386c38ce3aa5a1eb0ffc6c1f5da4a4f6bdbb67b1d` |
| `editable/manifest.json` | `463ab0139b2316dfe935812cca5aad64c114db8682c76900268d36638d1c110a` |
| `editable/candidate-indexed-mesh.json` | `e24272946eada65ed0b365ba5462f007bb7a5f9117e4d67e158b78c47d1d55ec` |
| `output/current-geometry.json` | `b412eb583bc10bbe2c1e3bcb412a29ee41293258b7016faa1459726228848760` |
| `output/proposed-geometry.json` | `5d5bc2df18f7f1fa4ad7ed00b15bd31f194454ed5393246e05f5213715f07871` |
| `output/comparison-z100.png` | `d5e153bd679be32611bd493c7dad52d52d93df23112c346e38a310ce7da0f945` |
| `output/comparison-z125.png` | `49310b342f6fa9d71d6e3e32bcfe06f583839395dd13161dd97b592d1e3bef6e` |
| `output/comparison-z140.png` | `0bd1d42febd4a11b733a07287126f2190b447ee4172708ac6ed3b36ee52dffb2` |
| Imported prior `source/build.py` | `220750cc0576f3314852dcf306661c066ec0499ff0d48a0caa9d1bd325bda3f3` |

Both manifests enumerate exact source and output paths. `packet-files.sha256` provides the full delivered file inventory except ignored Swift products and itself.

## What the tests establish

- Current geometry matches original extraction. Every neighbor dictionary remains exact. Only the kiosk reuses the old proposal. The broad earlier neighbor proposal is explicitly rejected as an identity match.
- All kiosk vertices retain XY. Ground contacts, chamfer, world roots and all authority footprints remain unchanged. Topology, material, footprint, root, contact, neighbor Z, kiosk XY and undeclared Z mutations are rejected.
- Full V9 authority record matches exactly, including actors, Camera field, solids, depth order/constraints, controls authority, framing, ground witness and supplements. Mutation checks reject changed authority.
- Every retained layer hash is independently reconstructed for both arms. All six frames independently recomposite byte-for-byte from the exact ground, retained layers and kiosk layer in V9 order.
- Frame differences lie entirely within the union of current/candidate kiosk alpha masks. No outside-kiosk pixel changes are allowed. This permits only changed kiosk occlusion of unchanged background layers.
- Original full benchmark and native-reference RGBA bytes remain exact. Native screenshots never supply source-proxy background pixels.
- Semantic doorway faces independently verify threshold/head/clearance, roof heights and measured crown. Plan distances and Player visual reference are checked. Editable mesh UV/height/XY/Z mutations are rejected.
- Existing output overwrite is rejected before writing. Exact deterministic replay is asserted, not inferred from visually similar images.

## Failures and limits retained

No render, export or test assertion failed in this packet. The initial16-test and final19-test logs are retained rather than overwritten. A tool-call schema rejection occurred at02:15:17UTC because an edit boolean was null (`invalid type: null, expected a boolean`), before any file mutation. It was reissued with explicitfalse and succeeded. The isolated Swift build emitted existing non-throwing-try warnings and a60-second no-output watchdog notice while compiling, then completed successfully. Neither is hidden as a test pass or represented as a source defect.

At02:18:21UTC a final whole-tree `git diff --exit-code` returned1 after concurrent changes appeared in `FACTS.md` and `docs/handoff/NEXT.md`, updating production authorization and qualification status. Those files are outside this worker's ownership and were not touched or restored. The chained inventory command stopped before writing inventory, then inventory generation was reissued independently. The02:17UTC zero-diff result is historical, not a claim that the shared tree remains clean. This is expected shared-worktree activity, not a packet-test failure.

Prior architectural packet's failed ground-UV and face-normal attempts remain untouched. This packet imports its final hash-pinned corrected adapter, not those failed variants. No shared tests, assertions or fixtures were weakened.

## Coordinator decision still required

Review the three actual images, especially crown/entry relationship against the unchanged Camera and northern residential wall. The fixed broad footprint, zero-gap northern corner and blocked-base landing reading remain unresolved. UVs are retained for editability, but textured detail under compressed Z has not been validated. No acceptance, benchmark completion or native integration is claimed. If selected for further work, preserve every neighbor source/geometry/registration and carry these gates forward.

Trail context saved approximately1,436,933tokens across this turn's three graph calls. Graph automatically refreshed its local cache when asked after new source files appeared. No manual graph/shared-file edits were made.
