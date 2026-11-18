# One paving corner: bounded source proposal

Authority: accepted source-to-scene continuation, slice6, BP-001/007/012/T1045.
No production, collision, walkable bounds, native scene or art admission changes.

## Delivered

- 64 distinct mixtures of the retained revision02 material, arranged into an
  eight-slab supertile rather than repeating the original four-slab stain unit.
- Opposite edges match exactly. Joint blending narrows from3 to1.5 source pixels.
- One authored rounded curb/road boundary with rails/crossing and explicit
  drain, tactile-panel and manhole positions in `source.json`.
- Top-down and offline midpoint ground-plane previews, a2x2 repeat sheet and
  exact grayscale output. Decorative details have no gameplay authority.

The input is the tracked `paving-repeat-repair-20261116/revision02` PNG, verified
against its retained hash. `source.json`, `build.py` and `manifest.json` bind
parameters, builder bytes, source mixtures and export bytes. No untracked
first-sample packet or external absolute path is needed to rebuild.

## Coordinator review

Actual repeat and corner images were inspected at08:25 and08:32UTC. The broad
four-slab stain/frame is no longer the repeated unit and the joints are less
heavy. The rounded corner and three authored street details are visible.
Recommended only as a bounded material/layout input for a future isolated
scene comparison. It is NOT a benchmark-faithful finished environment: road
wear is sparse, curb depth is only painted on a ground plane, and finite
supertile repetition still exists. Uprights, HUD and fields are absent here.
No source-only preview can certify ordinary whole-scene composition.

## Verification

```sh
python3 -B docs/review/paving-corner-review-20261116/build.py
python3 -B -W error::ResourceWarning docs/review/paving-corner-review-20261116/test_source.py
```

Seven tests passed in4.024s at08:28UTC. They cover exact rebuild/export hashes,
changed-input rejection,64unique slab mixtures, matching edges/narrow joints,
authored curb join/feature-side placement, alpha/grayscale and honest status.
These are technical facts, not aesthetic scores. `tests-0828.log` retains output.
`index.html` displays704x352 and352x176 offline previews and the1024-square repeat
with aspect preserved and grayscale toggle. They are not device measurements.

The earlier unfinished `paving-context-source-20261116` packet is unchanged.
This packet adapts its source algorithm into a separate complete review proposal.
