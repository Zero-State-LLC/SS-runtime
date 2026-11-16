# Final bounded QA review, November 16, 2026, 21:29 UTC

**Technical QA repair verified. Overall benchmark fidelity remains NOT MET. No owner acceptance or production admission.**

## What changed

V5 repairs the diagnosed Camera/kiosk ordering with authoritative footprint constraints, removes only the candidate Player's separate pale faction outline, registers its existing soft shadow to the foot root, and extends the same authored ground context across the arena without the finite patch boundary. V5 remains published as `671c659a0f23af6dfa8ed0cefb57c2673f361979` and its original captures remain unchanged.

V6 changes only the view center from `[736,672]` to `[684,724]`. The constant coordinate sum keeps vertical framing unchanged. It does not move the Player, Camera, stone, props, controls or fields. Exact source hashes, registrations, depth ranks, shadow treatments, all 24 solids and Camera field parameters are checked against preserved v5 evidence.

## Native and portable evidence

- Native2122 executed exactly one selected test with zero failures/skips, producing six captures and eighteen PNGs. Strict import succeeded after correcting the independent pause-stroke oracle, not after changing the native run.
- Actual loaded and freshly built executable SHA256 agree: `4bc45a685a0098b91cd6210829a92c60276db9d1fc6635c3c23b49753c52e7f4`. `native-capture-v6/verification.json` records both exact paths and hashes.
- Every full Player/Camera canvas stays in the 704x326 logical crop and outside actual visible stick/dodge/pause graphics in both arms at all three zooms. Candidate Camera-to-stick horizontal clearance is about 82.73, 55.36 and 38.93 logical units at zoom 1, 1.25 and 1.4. The smallest control-arm clearance is 12.78. This is a fixed quiet fixture, not adaptive gameplay framing.
- The unchanged pixel probe passes all three candidate zooms: zero registered Camera silhouette covered by the kiosk, zero sampled pale Player exterior pixels, Camera core matches about 93.74%, 97.75% and 95.54%. These are bounded diagnostics, not a perceptual quality score.
- Independent suites passed 41 v5 QA, 13 compiled depth, 9 ground, 75 historical scene and 39 corrected framing checks. Original 37-check framing output remains preserved and is not silently relabeled as the corrected suite.
- The final staged-only clean export independently passed all 39 corrected framing tests, both v5/v6 retained verifiers and both gallery suites at 21:29 UTC. It contains no unrelated unpublished editable-master/family/enemy directories. See `clean-export-final-2129.log`.
- The Node evidence suite validates all 54 actual v4/v5/v6 images and 72 selections, with 22 rejection cases plus 15 synthetic v6 mutations. The separate asynchronous loader suite rejects absent/corrupt/mismatched evidence without fallback. Synthetic loader data is not native evidence.
- Actual Brave checked 162 control combinations and 216 image displays across all three versions, zooms, paired/single arms, exact native/half logical sizing and grayscale on/off restoration. The full unchanged benchmark image retained its 1672x941 intrinsic aspect. No page-level horizontal overflow. Before import, v6 correctly showed HTTP404, no capture images and disabled controls. See `browser-check-2128.json`.

## Failed attempts retained

1. Native2120 said success but executed zero tests. Runner diagnostics prove it loaded the retired v4 executable from a `Dead/` application container, not the current installed build. A single non-erasing dedicated-simulator restart recovered correct execution. `REJECTED-2120.md` preserves the evidence. Issue #241 remains open because the underlying cache-retention mechanism is not fixed.
2. The first native2122 import correctly failed against an incorrect verifier expectation: pause uses default stroke1, while stick/dodge explicitly use scaled stroke. Issue #250 records the oracle defect. The correction is per-role and retains the same tolerance, native fixture, captures, required control positions and mutation rejection. `import-2122.log` and `import-2126-corrected-oracle.log` preserve both outcomes.
3. The first v5 clean export lacked the required tracking context and was rejected. A real independently indexed clean export passed without altering validators or source bytes. The browser's first grayscale probe assumed a CSS filter rather than captured grayscale PNG selection, and one timer-polling probe exceeded its tool budget. Event-driven checks corrected the harness, not the gallery.

## Actual visual verdict

The coordinator inspected the actual v6 zoom1 and zoom1.4 candidate PNGs and the unchanged approved benchmark, not only hashes or thumbnails.

**Improved:** Camera is no longer painted behind the kiosk and no longer overlaps the movement graphic. Player has no pale halo. The broad finite-paving material switch is gone. Player/Camera/control separation is visibly clearer.

**Still not benchmark-equivalent:** the building mass, roof crop and scene composition differ substantially; Camera and garment forms/material treatment remain source-fidelity compromises; the Player's static pose and contact shadow do not reproduce the benchmark's grounded walking silhouette; paving and road are more regular, flatter and less weathered, with sparse contextual wear. Surrounding structures are still retained and stylistically inconsistent. The visible authoritative field and fixed production HUD remain diagnostic overlays, not benchmark composition. Passing this repair is not a coherent accepted world, full family, motion or encounter sample.

## Gate

This closes the bounded QA comparison, not the visual acceptance decision. Owner review of v6 is required before another source/layout aesthetic pass or motion/encounter expansion. No production code/assets, gameplay collision/field authority, specification pin, physical-device certification, merge or issue closure was changed. No unfiltered Swift retry or automatic CI polling chain was started. Remote CI for each publication head must be assessed separately from local evidence.
