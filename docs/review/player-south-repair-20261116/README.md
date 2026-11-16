# South anterior-shell repair: source-only, not recommended

Authority: accepted `intent/2026-11-16-source-to-scene-continuation.md`, slices3/4,
BP-002/007/012 and T1045. The old source packet and all recovered originals
remain unchanged. This new packet contains a copied editable source with a
bounded geometry/material repair, not production art.

## Actual change and visual verdict

The old knee cover was smaller than the surrounding enlarged trouser surfaces
and disappeared in the shared source depth buffer. The new kneepad is a complete
ellipsoidal shell positioned anterior to the knee with independently authored
width, height and thickness. It still competes in the same per-pixel depth buffer.
No foreground bitmap overlay or screen mask forces it visible. Diagnostic
`editable/parts/*-visible-knee.png` records pixels surviving lower-body depth
and the final upper-body composite.

Attempt01 restores kneepad visibility but retains blocky mapped thigh paint.
It is preserved under `attempt-01/`. The second/current sample adds bilinear
premultiplied source-material sampling over complete cloth underpaint. Source
paint is unchanged, and this is not postprocessing the character export.

Coordinator inspected both actual comparisons at08:23 and08:26UTC. Kneepads
are visibly present. The second sample smooths sampling blocks, but the thigh
patch is widened/foreshortened and cloth folds still do not match the preferred
baggy neutral. **NOT RECOMMENDED. No other facing or native scene integration.**
Two bounded repair previews are retained. Stop this source method here. A next
method must explicitly re-author garment surface/UV correspondence and preserve
the patch proportions, rather than tune the same sampling or shell parameters.

## Reproduction and evidence

```sh
P=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
"$P" -B docs/review/player-south-repair-20261116/build_south.py
"$P" -B -W error::ResourceWarning docs/review/player-south-repair-20261116/test_south.py
```

Ten tests passed in58.243s at08:26UTC, including exact rebuilt pixels, unchanged
identity/upper region, fixed leg lengths and foot contacts, actual final knee
coverage, alpha, source ownership, alpha-correct bilinear sampling, and a build
with the external-original path deliberately unavailable. Technical success is
not an aesthetic pass. `tests-0825.log` retains that output.

Rebuilds use tracked `aaron-package/SS-player-bounded-neutral` and the tracked
baggy comparison only. The baggy bitmap is never a geometry/material input.
The optional external-original audit checks1001 original entries, including
34 release05/13 frames and the benchmark when those originals are present.
If absent, only that audit is explicitly unavailable; the build and portable
source checks still run. The missing originals are never reported unchanged.
The supplied immutable inventory is not regenerated to bless new input bytes.

`attempt-01` is retained evidence plus the changed model/thigh/builder snapshot,
not a standalone complete project. Run the current packet for the second sample.
No simulation, input, collision, timing, animation or native run changed. The
upper body is still layered recovered paint, not a rotatable four-facing master.
The0.375s settle and original releases05/13 remain immutable and unexercised here.
