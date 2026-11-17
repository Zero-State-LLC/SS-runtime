# Coordinator validation and actual playable review, November17 2026

Verdict: **Debug-only live projection verified within the tested scope. Visual benchmark NOT MET, art NOT ACCEPTED.**

## Independent validation

Coordinator read the actual0407 xcresult summary:18tests,18passed,0failed,0skipped. It includes10new projection tests and8unchanged kiosk tests. Reviewed App adapter/wiring, analytic geometry/input/parity/lifecycle tests and the exact probe-only correction diff. All8entries in `source-build-hashes-0408.txt` independently pass SHA256 comparison. The original0350run17/18 and exact executed source are preserved. Runtime#261 tracks the root-owned test probe cleared by intentional existing clip replacement. The child-owned probe retains all prior assertions and adds a retained-parent assertion. This is not a runtime animation-policy change.

Coordinator reran all6scope guard tests and actual11876protected-file verification successfully. The guard independently checks index and worktree so restored bytes cannot conceal staged authority/test/art edits. Worker reran focused Swift10tests/3suites at0407. This is not a fresh full unfiltered host or Release test-suite result.

Final built Release product independently passes the original kiosk exclusion checker: executable SHA256 `2297733e9e6dcb23b2c792095d0ebb0a21f444df15a6a8852e348db7a554f69a`,1032PNG files inspected, all3review image hashes absent. Coordinator additionally checked actual `nm -j` and `strings` output for absent `LiveWorldProjection`, `SSKioskProjection`, `live-midpoint`, `KioskPlayableReview` and `SSKioskReview`. Retained JSON: `release-coordinator-0411.json`. Source-only conditional compilation is not the exclusion oracle.

## Actual app inspection

Coordinator installed the fresh Debug product with dylib SHA256 `a9e8d87abf61f63750d2a63e8d045f983af45e97267eaf29990cd07981fdd347` on simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Both launches use ordinary initial state and existing legal `-SSAutopilot run`, with `-SSMute`, the validated existing kiosk resource path, selected arm and `-SSKioskProjection midpoint`. No scenario seed or actor repositioning was used.

- Candidate process46740 launched04:09UTC. Raw `candidate-live-0409.png` captured04:09:49UTC.
- Current process48392 launched04:09UTC. Raw `current-live-0410.png` captured04:10:13UTC.
- Default process50303 launched04:10UTC with only `-SSMute`. Raw `default-restored-0410.png` captured04:10:51UTC shows settled ordinary title, no review badge.

All3raw1206x2622PNGs were visually inspected without rotation, cropping, compositing or enhancement. Landscape content is stored in the simulator's portrait-shaped raw image. Current/candidate show correct arm plus MIDPOINT/NOT ACCEPTED, ordinary HUD/controls and live actors. These asynchronous frames are neither matched-tick comparisons nor pixel-parity proof. Continuous update/action behavior is established by the actual SKView native callback test, not by still screenshots.

The ground now presents diagonally with upright actor/building artwork. Large dark foundation areas remain visible, neighbor source scales differ substantially, the kiosk dominates the frontage, and raster sources/contact contours do not consistently correspond to the projected foundations. Current-arm frame shows Player overlap with the small neighboring building. Preserve that evidence as a depth/contact limitation, not a claim that actors should be relocated. HUD remains fixed; retained controls may overlay the large architecture. These screenshots do not establish coherent whole-scene architecture, collision readability, ideal framing or art acceptance. Do not hide foundations or modify neighboring source art to conceal deficits.

## Publication boundary

This reversible opt-in adapter can be published for review, not admitted as shipping presentation. Default/Release remain unchanged. No source-art, simulation/collision, authoritative roots, contract/pin or acceptance threshold was changed. Next art/contact/depth decisions, physical performance, external playtests and owner merge/release remain separate gates. All prior failures and unrelated untracked art packets must be retained.
