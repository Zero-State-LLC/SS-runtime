# Building diagnosis and acceptance checklist

## Observed input

Owner feedback at 2026-11-16 22:10 UTC: buildings are out of perspective and architectural detail is insufficient. The coordinator inspected the actual retained v6 z100 native image and the full immutable benchmark at 22:13 and 22:16 UTC. Neither inspection is an acceptance verdict.

## Bounded causes, not a global camera rewrite

1. The kiosk source already projects `(x-y)/sqrt(2)` and `(x+y)/(2*sqrt(2))` with vertical height. Its basis matches the D108 ground. Replacing that basis would introduce a new defect. The shortcomings are the relation of painted relief to real surfaces, flat parapet/cornice/entry treatment, and architectural massing at scene scale.
2. Context sprites use `App/WorldRenderer.swift:746-769`: the unprojected collision rectangle width and height are used directly as sprite dimensions, with default centered anchor. V6 extracts those sprites as uprights but retains their source sizing/anchor (`AppTests/SceneQAFramingTests.swift:260-305`). The actual v6 record has residential-north size384x192/root320,864 and civic-west192x384/root832,960. These are collision dimensions, not measurements of the painted asset's projected footprint. Explicit source geometry and contact registration are missing. This observation applies to the isolated D108 comparison, not a claim that the production renderer's current top-down contract has changed.
3. Enlarging low-resolution context sprites cannot recover absent detail. The review needs coherent source panels and explicit architectural geometry, not sharpening or extra random grime. The existing independently painted atlas is a legitimate reusable material input. The benchmark must not become a texture atlas.

## Acceptance checks for this work order

- Keep v6 capture and every previous source byte unchanged.
- Derive each proposed building's canvas, source root and uniform draw scale from editable projected geometry. Document local and world footprint landmarks and test their forward projection independently.
- Keep canonical solid footprints, Camera field/root, Player root, view center, controls and non-building source/treatment unchanged. No hidden surrounding buildings and no arbitrary depth overrides.
- Inspect first source sample at native and half logical scale, then at most one aesthetic correction. Distinguish painted relief from actual geometry.
- Capture both v6-style baseline and building-only candidate in the actual native fixture at1x/1.25x/1.4x. Verify one selected test, six captures/eighteen images and actual loaded executable against the fresh build.
- Recheck Camera visibility, Player outline/contact, ground coverage and control-safe framing after buildings change. Inspect the actual images, not just geometry tests.
- Publish a new review gallery that fails closed on missing/bad evidence, preserves full benchmark aspect and supports native/half/grayscale views. No aesthetic acceptance is inferred from the hash verifier.

Motion, encounters, production admission, merge, physical certification and issue closure remain outside this authorization.
