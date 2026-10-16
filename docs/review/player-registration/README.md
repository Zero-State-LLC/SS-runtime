# Revised player registration preflight — BP-002/BP-007/BP-008

Status: integration finding and numerical prediction, NOT a real-renderer capture or art admission.

Authority inspected: runtime 718b392, specs d602775. WorldRenderer.playClip assigns the normal 64×64 player sprite box and passes actor positions through unchanged. SpriteLibrary.anchorPoint divides contract anchors by logical box size. The static benchmark-art path also removes actions each render, so it cannot be reused as a moving playback proof. DisplayedPlaybackTests provides the correct post-action observation boundary but currently measures admitted art.

The revised source is 384×416 with ground root (192,336). At a proposed 6 source pixels per logical unit, preserve aspect with draw size 64×69⅓ and SpriteKit anchor (0.5, 0.1923076923). Fitting into 64×64 compresses vertical dimensions by 7.6923%. This scale is a controlled comparison parameter, not an accepted production size.

The source projects its forward ground coordinate at 0.5 and height at sqrt(0.75). For nominal 240-unit/s travel, sampled support poses cancel motion under that same projected mapping. Applying their local foot offsets to an unprojected actor root instead predicts 11.25 logical units of residual across the sampled 0.09375-second support span. This is NOT measured runtime slip. Exact zero in the consistent mathematical mapping is also NOT a displayed contact result: collisions, fixed-point positions, texture holds, action phase, real camera motion and render timing remain absent.

Required next capture: use the exact 16 revised source frames; preserve aspect/root; retain live SpriteKit actions; record actual selected texture after actions alongside authoritative and rendered position. Apply the chosen world-to-view mapping consistently to actor roots, ground and geometry. Do not squash the finished elevated character or change controller speed. Use explicit test-only candidate loading, not production metadata admission. The static composition fixture remains separate. Cardinal/diagonal, partial input, collision, reversal and interruption evidence remains open under BP-008.

This exposes an implementation prerequisite already required by the pinned specs; no new visual projection or gameplay rule is adopted. check.py and samples.json reproduce registration.json. No runtime code or production assets changed in this review.
