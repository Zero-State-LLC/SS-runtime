# Final Camera surface-only pass

## Coordinator closeout, November16 09:02UTC

**Second preview NOT RECOMMENDED, both changed-method attempts exhausted.** See `COORDINATOR-REVIEW.md` for actual visual findings and independently exercised browser controls. No third pass, source admission or scene integration.

Coordinator retained the original3.14.7-versus3.14.5 manifest failure, then corrected only its environment comparison. The immutable author manifest is now SHA256-pinned; a regenerated manifest must truthfully name the running Python version and match every other field exactly. All other exports remain byte-exact. Two extra regressions reject false interpreter reporting and Pillow/reference/file-hash/extra-field drift. No source or pixel output changed.

All16tests passed on Python3.14.7 (30.805s) and3.11.15 (32.707s). A standalone copy containing only `attempt-02/` and `test_final.py`, with no repository or historical sibling, passed all16tests in32.166s. It also exercises the immutable author-manifest pin. Logs are `coordinator-system.log`, `coordinator-py311.log`, and `coordinator-standalone.log`. The following worker report describes its earlier14test author-environment validation; the coordinator evidence supersedes any pending verdict or cross-version caveat below.

Final bounded pass authorized by the coordinator at 08:47 UTC, November 16, 2026, following the first proposal's **NOT RECOMMENDED** verdict. The first proposal, its initial technical failure and both preceding procedural attempts are preserved. No third pass is undertaken.

## Actual preview and honest verdict

Open **`index-final.html`** or **`attempt-02/comparison-color.png`**. The latter compares unchanged benchmark / rejected surface pass 01 / final surface pass 02, with exact native/half source previews. The actual final image was sent to the coordinator at 08:52:11 UTC, before final documentation.

Worker assessment: green bands, hard highlight discs and abrupt plate shading are reduced. The material now has finer, short, separately authored dark-charcoal marks and softer individual brush edges. **It still looks cleaner/smoother and less weathered than the reference. Finished benchmark fidelity is not established, and the worker does not recommend acceptance.** Final coordinator verdict is separate and pending at this handoff. Technical passing checks are not an art score.

## Final source and constraints

- `surfaces-final.py`: **100 individually authored paint surfaces**, replacing the first proposal's 90. Each has explicit path, color, width, opacity and optional brush-edge feather, 0.15–0.9 source pixels.
- `geometry.json`: exact frozen first-proposal geometry/model. All 16 component contours, canvas, root, scale, landmarks and hidden probes are unchanged. No geometry/camera/proportion redesign in this pass.
- `build.py`: ordinary path painting and alpha composition. Brush feather applies only to the alpha edge of its explicitly authored path before clipping to its complete component. There is no random placement, procedural noise, material generator, spatial palette ramp, global image tint or raster overlay.
- `attempt-02/layers/`: **132 RGBA layers**: 100 paint layers plus complete underpaint and complete-component exports for each of 16 parts.
- `attempt-02/camera-surfaces.svg`: independent named geometry/paint paths, with per-mark soft-edge filters where authored. SVG rasterization is not claimed identical to Pillow.
- `attempt-02/source/`: complete standalone replay source, frozen geometry and exact input copies.

Real RGBA and zero RGB beneath alpha-zero are tested for every layer and export. Authored root stays (46,427). Uniform x/y scale stays 96/418, producing 42×104 padded native and 21×52 half canvases. These are source inspection sizes, not executed SpriteKit captures or a newly selected game zoom.

## Rebuild and self-contained tests

From repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 docs/review/camera-surface-authored-20261116/build.py
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 -W error docs/review/camera-surface-authored-20261116/test_final.py
```

For a portable verification package, copy **`attempt-02/` and `test_final.py` together** into another directory, then run that test file. The final tests need only those files and installed Pillow. The final archived renderer finds its bundled `source/inputs/`, not a repository root, neighboring attempt or spec marker. An alternate artifact location can be provided with `CAMERA_FINAL_ROOT`.

To replay source alone, copy `attempt-02/source/`, then run its `build.py --source surfaces.py --output <new-directory>` with an explicit interpreter. The source archive includes `geometry.json` plus exact unchanged reference, rejected first-surface preview and earlier procedural preview copies. Input raster files are used only by the comparison board. A test forbids all raster reads in the actual source renderer.

Observed build/test interpreter: `/usr/local/bin/python3`, Python 3.14.5, Pillow 12.3.0. Exact manifest replay includes observed tool metadata, so cross-version runs may produce honest metadata differences even if pixels agree. The first proposal's Python PATH mismatch remains documented in its original failed log.

### Actual results

**14 final-source tests passed in 29.070s**, retained in `attempt-02-tests.log`. They cover:

1. Complete archived CLI byte replay of outputs, layers, SVG, comparisons, source and manifest.
2. Manifest hashes and hard-pinned reference hash.
3. Pinned bundled original/prior preview input bytes.
4. Every output/layer has real alpha, nonempty authored paint and zero RGB at alpha-zero.
5. Five painted hidden overlaps and a missing-underpaint negative check.
6. Actual collar removal reveals painted pole without modifying distant pixels.
7. A specific paint-color edit changes local pixels, not alpha, root or distant geometry.
8. Source renderer reads no raster inputs.
9. Exact uniform native/half transforms and grayscale conversion.
10. All named editable SVG paint paths correspond to the 100-surface census.
11. Exact first-proposal contour/landmark/root/scale preservation and **pixel-identical alpha** despite changed material RGB.
12. A detached source-only copy replays successfully while an audit hook rejects reads back into the original packet, then reproduces final master/native/half/comparison/manifest bytes.

**Separate historical audit: 2 tests passed in 0.154s**, retained in `history-audit-final.log`, using the unchanged first-proposal test file. This explicitly verifies the original benchmark, first-surface manifest/artifacts and both earlier procedural manifests/artifacts. No external audit was silently skipped or merged into the standalone claim. First-surface manifest still hashes to `4110a4f369b9c0817950fd6887b0b6cc97df6e1c789d466c4e838651ee93aaf1`.

**Actual Brave at 08:55:05 UTC:** all 3 canonical PNGs loaded at 890×550 / 42×104 / 21×52; 16 component and 100 paint-surface controls hid/restored; specific color/opacity edits preserved the selected path and reset restored authored values; grayscale and root toggles restored; no horizontal overflow.

## Scope and stop

Only `docs/review/camera-surface-authored-20261116/` was edited by this pass. No original image, previous attempt bytes, runtime/App/AppTests/CI/shared documents, production assets, states/clips or native execution. No commits or push. The existing full-Swift-suite stop remains respected. Coordinator owns the final visual verdict and publication. **No third art pass, acceptance, state expansion or integration is claimed or undertaken.**
