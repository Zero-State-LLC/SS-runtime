# Actual playable review, November 17 2026

Status: **DIAGNOSTIC ONLY. Visual benchmark NOT MET.** No production admission, art acceptance, or release qualification.

## Execution

Coordinator installed the freshly rebuilt Debug app on iPhone17Pro simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Launches used the README's explicit local resource path and `-SSMute -SSAutopilot run`, first current (process4586,03:26:48UTC), then candidate (process6147,03:27:16UTC). This is the existing legal-command pilot from ordinary initial state, not a scenario seed or Player repositioning. Both visible yellow status labels read KIOSK REVIEW with their correct arm and NOT ACCEPTED.

Raw simctl screenshots are retained unchanged:

- `current-live-0326.png`, capture03:26:56UTC.
- `current-live-0327.png`, capture03:27:15UTC.
- `candidate-live-0327.png`, capture03:27:33UTC.
- `default-restored-0327.png` was captured too early and contains the black launch transition, not usable restoration proof. It is retained rather than replaced.
- `default-restored-0331.png`, after the final default relaunch (process22181), shows the settled ordinary title screen with no review badge.

The simulator's raw image orientation is portrait-shaped1206x2622 with landscape app content. These files have not been rotated, cropped, composited or enhanced. Exact simulation ticks were not instrumented for these screenshots. They are asynchronous live observations, not matched-time/current-candidate pixel comparisons. Default restoration is additionally covered by the selected native tests.

## Visual finding and scope boundary

The current early frame shows ordinary movement/HUD and explicit current review status, not an isolated full kiosk comparison. The candidate frame shows the kiosk with existing Camera and actor art in the live world. The already-projected kiosk texture contrasts visibly with the retained rectangular foundation and neighboring live presentation. Dark rectangular foundation regions remain visible, and this is not the coherent V9 source-scene projection. The earlier flat/native exact geometry packet remains the appropriate controlled geometry comparison.

This integration proves an explicit reversible review route, not a repaired playable visual composition. Do not suppress the foundation, move Camera/Player, replace neighboring buildings, or apply whole-world reprojection to make the screenshot look accepted. A broader presentation/projection decision is an owner gate. All gameplay authority and original frozen comparison evidence remain unchanged.

## Engineering evidence

The initial native8-test run failed one full-snapshot assertion despite matching authoritative digests. Issue260 identified randomized dictionary traversal of spawn sockets. The production repair preserves authored within-encounter order and sorts only presentation traversal keys. Four core red/green regressions and the exact unchanged8native tests pass after fresh Debug build. Coordinator independently reran21socket/hash/reinforcement tests, all passed. See `SOCKET-ORDERING-REPAIR.md` and the retained native summaries, logs and source/product hashes. This is not a relaxed test oracle or art approval.

Final existing-art native traversal passed one unchanged test, exit0. The original strict importer verified2arms,52scene images,824post-action rows,50selected textures and1073resource bindings. Human-named exact exported bytes and original attachment manifest are in `traversal-final-retained/`. This fixture deliberately starts at a test position and is separate from the ordinary-start legal-pilot screenshots above. It does not establish performance, full-pose acceptance or resolution of historical issue259.

The post-socket-fix Release build completed exit0 in196seconds. `check_release.py` verified executable SHA256 `ed6edcaae1f7ac64501175c366e0876afb5a2d4399e6fe1ef08a0a86f10d3431`, absent review symbols/launch/schema bytes and absent review image hashes across1032bundledPNG files. See `release-final-exclusion.json`. This final build supersedes the earlier source-version-specific exclusion check, but is not a new Release test-suite or physical-device result.
