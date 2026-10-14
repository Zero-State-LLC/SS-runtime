# Hooded body source pilot — revision 4 review

2026-10-14. **Not admitted as benchmark artwork.** This is an editable source experiment, not a SpriteKit scene capture or a device-test result.

The existing controlled-character-source specification requires a costume master that preserves the approved urban hooded reference; it explicitly rejects a mannequin as acceptance. This review applies that requirement without changing the target.

## Work and evidence

- Hosted project: https://higgsfield.ai/3d-jutsu/e428d4b6-3697-4c74-ae65-78764240abde
- Revision 4, successful mutation `ss-body-silhouette-02`; Blender artifact ETag `57ec8a5bbd7f10f8b21c91e393d7191f`, 1,565,340 bytes; GLB ETag `a8925e04314176649b7eab965694c05c`, 400,196 bytes. These are service ETags, not local SHA hashes.
- 26 editable body objects bound to the existing rig. Hood contour changed from oval to tapered; continuous weighted sleeves replace separate upper/lower arm masses. Meshes parented to the rig; debug proxies removed from export.
- Successful query `ss-body-refined-review-01` rendered frames 1 and 4 at 384 × 384. Both images were visually inspected in the browser, using the same saved camera and light setup.
- Rest artifact `4679ca5cf2b713413f848d03d6185427`; peak artifact `a028deedd7fc1db344af2c38d5314db9`. Exact operation metadata is retained in scene-evidence.json.

## Visual result

Sleeves now read as continuous shapes, and the hood opening has a more tapered contour. The peak sample visibly bends the knees with the boots near their original image locations. This two-frame comparison does not prove every intermediate deformation, no foot slip, or world-travel contact.

The candidate fails the benchmark art gate: the torso and trousers remain smooth mannequin-like masses; knees look like separate oval attachments; hands lack readable construction; the coat lacks convincing fabric thickness, seams and folds. The front strap ends abruptly and has no authored rear continuity. Dark flat materials lose internal separation. Four-direction identity and hidden surfaces have not been reviewed. Increasing export resolution would preserve these defects, not resolve them.

## Required next work

1. Correct garment construction and continuous leg anatomy in the editable master before adding texture detail. Preserve the approved hood, coat length, practical boots and restrained asymmetric equipment; do not introduce fantasy ornament.
2. Author strap continuity and hidden costume surfaces, then inspect all four neutral rotations with one camera and light setup. Actual projection still needs comparison with the real shared renderer scene.
3. Review first, peak, intermediate and final deformation samples, including garment intersections. Then pass the specified south locomotion and world-travel gates before expanding animation families.
4. Export at measured native/zoom pixel density only after shape and costume pass. Resolution choice remains selective; this 384px diagnostic render is not a production texture-size decision.

Runtime assets, active clip metadata and gameplay were not changed. No new Swift or device tests were run for this source-art review. Physical-device testing and the shared-renderer benchmark gate remain open.
