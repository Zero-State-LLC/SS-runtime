# Camera raster-material pilot 01

**Review only. NOT RECOMMENDED for source acceptance or scene integration.**

Open `pilot-01/comparison.png` or `index.html`. This is the single first visual attempt under `intent/2026-11-16-scene-method-approval.md`. No second visual is authorized by this packet. Coordinator inspection must happen before another attempt.

## Actual inspection

- Supplied independent material: **1254 × 1254 RGB**, not the prompt's requested 1024 square. PNG has no embedded metadata. Exact separate provider JSON records OpenAI image generation, `action=generate`, actual `size=1254x1254`, opaque output and the full material-only prompt. Original PNG and JSON are copied byte-for-byte under `inputs/`.
- Material inspection: near-neutral dark cast iron with restrained grain and sparse warm-grey chips. No benchmark crop supplies any material pixels.
- First rendered comparison inspected November 16, 2026 at 09:36 UTC. Native pole, finial and rings are **too dark and insufficiently separated**. Texture variation is largely lost at native/half. Pale hood still reads smoothly shaded rather than benchmark brushwork. Narrower contour hypotheses are visible, but fidelity is not established. This is not an acceptance recommendation.
- Only one visual source configuration was rendered for review. Mutation checks render temporary in-memory diagnostic variants, do not publish alternate visual proposals, and do not constitute a second art attempt.

## Editable master, not a flat cutout

The master is **`model.json` + `inputs/iron.png` + `replay.py`**, not `camera-master.png`. Sixteen complete separately rendered components remain ordered, individually hideable and editable. `pilot-01/components/` contains complete component previews, including occluded material. They are outputs, not dependencies of the master.

Each part has an editable cubic-path `contour`, `[scaleX,scaleY,translateX,translateY]` construction transform, `uv=[u,v,width,height]` window in actual material pixels, RGB `tint`, `texture_strength`, continuous `shading`, named broad-face gain regions, outline and `visible` flag. Reorder `parts` to change draw order. UV samples are exported under `pilot-01/uv-samples/`. UV axes map the selected material window across the transformed part's bounds. Face paths are clipped by the complete component mask. Edit the material image with a real image editor or generation tool if needed. This renderer never redraws or synthesizes the material source.

Iron luminance supplies the only irregularity. Continuous cosine lighting and explicit broad-face gains supply editable illumination, not procedural noise or dab generation. Cream enamel uses a **tinted/attenuated iron microstructure approximation**, not independently authored enamel. Glass likewise shares the source with a dark tint, while the lens has zero texture strength. This material-role mismatch remains a disclosed limitation. No additional service, image-generation request or installation was performed.

### Explicit contour/proportion hypotheses

| Component | Difference from tracked construction geometry |
|---|---|
| Hood, glass, cyan lens | 0.95 X / 0.85 Y about (116,118), together |
| Bracket | New narrower plate/return contour, not a raster squeeze |
| Bracket neck | 0.88 X / 0.84 Y about (117,76) |
| Foot, plinth, socket, ankle | 0.92 X / 0.90 Y about (46,432) |
| Finial | 0.94 uniform about (45,29) |
| Pole | Original construction contour/axis retained |

These are hand-authored visual hypotheses against the unchanged full original, not measured collision/field geometry or registered production landmarks. Original reference bytes are immutable. The comparison-only crop `(889,19,1069,469)` is never read by `render()` and never used as the master or material. The full original is also shown with uniform-fit rounding.

## Provenance and reuse decision

`provenance.json` contains byte counts, actual image dimensions/modes, hashes and original paths for **every local input**. Five construction/control/background files are exact `git show` copies at `e90b2361bcd80f4a15dd5c39335b2fc69f7be993`. Generated material PNG/JSON are supplied inputs, not claimed to exist at that commit.

**ADAPT:** retained `inputs/prior-build.py` lines 32–59 documents the cubic sampler algorithm used by `replay.py`. `inputs/prior-geometry.json` supplies complete contours and a few broad construction face paths. Prior flat pigments and scratch/dab paths are not rendered. Exact prior code is retained for citation only, never imported. Rejected prior master and original full reference are comparison controls only. Tracked muted paving is only an offline background context, not acceptance of paving or a completed ordinary runtime scene. No untracked sibling packet is read.

## Replay and tests

Requires Python 3 and existing Pillow. Verified here with Python **3.14.5** and Pillow recorded in `pilot-01/manifest.json`. From any working directory:

```sh
python3 /path/to/camera-raster-material-20261116/replay.py --out /path/to/new-replay
python3 /path/to/camera-raster-material-20261116/verify.py
python3 -W error::ResourceWarning /path/to/camera-raster-material-20261116/test_pilot.py
```

For edits, copy `model.json`, change desired fields, then pass `--model /path/to/edited-model.json --out /path/to/diagnostic`. Do not overwrite `pilot-01`. `author.py` is the one-time recorded construction step, not the normal replay entrypoint: rerunning it replaces manual model edits.

**Actual result: 11 tests passed in 8.875 seconds with all warnings treated as errors**, final output `tests-strict.log`. Earlier runs are preserved in `tests.log` and `tests-final.log`. The verifier also passed with `python3 -W error verify.py`. Tests cover actual material metadata, UV-only component change, shading-only component change, contour change, hidden pole under removed ring, render reading only independent material, bad schema/status/UV/path rejection, standalone replay without repository/siblings, input/output corruption detection, explicit correction parameters, and editable broad-face gain. Standalone replay reproduced **all 38 PNG exports and the manifest byte-for-byte** using the same interpreter. A changed interpreter version must truthfully change manifest environment metadata, so exact manifest identity is only claimed for this environment.

Source canvas 180 × 450, inherited scale 96/418, rounded native canvas **42 × 104**, half **21 × 52**. The 352 × 200 ordinary paving-background context is an offline compositing diagnostic with no manufactured HUD, field or shadow. It is **not** a native runtime capture, complete scene, production registration, contact proof or acceptance evidence.

## Ownership and gate

Only this new packet was changed. No shared handoff, CI, production, commit, push or Swift run. Technical reproduction, visual quality, owner acceptance and production admission remain separate. At 09:40 UTC the coordinator directed preservation of this pilot and paused further illumination samples pending a separately generated complete painted-component sheet. No second preview exists. Existing source and issue gates remain untouched.
