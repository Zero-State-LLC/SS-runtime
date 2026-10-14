# Painted character source comparison

2026-10-14. **Neutral source study; not an editable layered master, animation family, or runtime admission.**

The procedural body pilot in runtime 1a1a061 failed the approved art benchmark despite improved geometry. This comparison uses the approved shared street reference directly, through the built-in image-generation tool. Prompts are preserved in prompts.md. The second generation corrects equipment continuity: anatomical right-hip pouch, left-shoulder-to-right-hip strap. The first candidate swapped the pouch's physical side in the rear view and displayed it prominently on both profiles.

## Inspected result

The corrected source has distinct front, rear, right-facing and left-facing views. The rear now places the pouch on viewer right, matching anatomical right; the left-facing view no longer shows a near-side pouch. Coat seams, gloves, boots and material treatment are substantially closer to the approved reference than the procedural mannequin. This is an aesthetic comparison, not a claim of user acceptance.

The reference's rough painted edges and restrained palette are better represented. Fine details compress heavily at the 64px logical preview, though hood, coat opening and boots remain identifiable. Side views still need comparison with the real renderer's ground projection: a generated claim of a fixed camera angle is not a calibrated projection. Body proportions and boot landmarks have not been measured for cross-view consistency. The expanded pouches/straps and both shoulder patches must also be checked against the final character identity contract rather than silently becoming new gameplay equipment.

## Export evidence

- Original corrected source: 1536 × 1024 RGBA, preserved as source.png.
- Deterministic alpha cleanup explicitly authorized by the user: alpha ≤32 becomes zero, ≥240 opaque, linear between; RGB unchanged. Original remains available for comparison.
- Four 384 × 384 candidate previews, all using one factor 312/459. No per-facing size stretching or bitmap mirroring.
- Manual approximate ground roots registered to (192,336), corresponding to logical (32,56) at 64px. These are preview annotations, not verified foot-contact measurements.
- Source and export SHA-256 hashes, source rectangles, roots and alpha bounds in exports.json; reproducible recipe in export.py.
- Registered plate visually inspected at large and 64px size. All four exported alpha bounds remain inside their canvases; no canvas-edge clipping detected. This does not rule out anatomical/source clipping.

## Production gate remains open

This sheet demonstrates a more promising material treatment, but four flattened drawings are not the editable source required by BP-002. Next, construct separately editable hood/torso/coat-tail/arm/hand/leg/boot layers with explicitly painted hidden overlaps, preserve equipment side, and test one restrained deformation before committing to a full locomotion family. Simply cutting the visible image into pieces would leave missing hidden surfaces; stretching a whole bitmap would not satisfy the spec.

Keep the existing rig as a pose/contact reference. Compare the layered result in the actual SpriteKit benchmark scene at native and zoom sizes, then validate world-travel contact and the required distinct frames. Do not replace active runtime resources or claim animation/device acceptance from this still-image study.

No Swift tests were needed or run for this source-only comparison. Runtime art, active metadata and physical-device testing remain unchanged.
