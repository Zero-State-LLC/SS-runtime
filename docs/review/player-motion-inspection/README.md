# Narrow stance + arm swing: source inspection

Reviewed 2026-10-15. Source: SS-player-motion-refined, archived at runtime 718b392; test-only renderer integration 88e79e8. Current specs: d602775. User prefers this revision. This review preserves that direction; proportions, motion amplitudes and hidden surfaces remain proposed.

## Separate speed passes

**Normal, 0.5-second cycle:** selected the normal-speed browser mode and inspected successive playback samples at the large and 64px sampling views. The narrower silhouette and opposing hand positions remain readable. The hands are subtle; boots and moving leg highlights draw more attention than the arms. The small view loses calf and lace detail. This is sampled browser playback, not continuous video analysis or measured browser frame pacing. It does not establish real-renderer contact.

**Quarter, 2-second cycle:** separately selected quarter-speed mode and inspected playback, all 16 exported poses, enlarged lower-body keys and isolated boot surfaces. The slower inspection exposes the cup-like knee pads, repeated soft calf folds, flat shafts against bright toe caps and limited arm deformation. These defects are easier to inspect slowly; slow playback is not a substitute for the normal-speed pass.

## Findings

| Item | Observed evidence | Disposition |
|---|---|---|
| Knee-pad orientation | Pads stay at the knee region rather than migrating to a heel/back surface. Their upper edge opens into a dark crescent in frames 1/12/16, while other poses look like rounded caps. The bright thigh patch above is distinct from the knee pad. | Needs refinement: preserve a consistent pad form and front-facing placement through knee flexion; do not hide the problem by moving the joint. |
| Heel/tongue ownership | The isolated front/rear renders show laces on the forward tongue and plain rear heel material. The raised foot often hides the tongue in this facing. | Correct in inspected front/rear keys. Side and other-facing ownership remains unproven; do not claim complete 360-degree validation. |
| Calf/boot detail | Calf folds repeat as broad soft bands. The boot shaft is flat brown while the toe is sharply bright and mottled. Cuff-to-boot transitions read abruptly, especially frames 4/12. | Highest material-polish priority. Preserve retained leather/cloth influence while making detail scale and light treatment coherent. |
| Coat overlap | No obvious exposed cut gap or torn coat contour in the 16 south frames. Tail edges remain attached. The tails retain a flat overlaid appearance beside the lifting thigh. | Keep the silhouette; improve depth/overlap. Hidden coat/leg intersections are not proven by these front views. |
| Arm motion | Hands alternate vertically in opposition; shoulder attachments remain stable in the sampled poses. This is visibly more useful than the earlier symmetric outward spread. The torso stays rigid and forearm deformation remains mostly projected length change. | Keep the restrained amplitude as a candidate; polish elbow/glove articulation without widening the stance or adding exaggerated swing. |
| 16→1 seam | Inspected 15/16/1/2 together and stepped 16→1 with previous-frame onion skin. No whole-character lateral reset or exceptional texture jump was evident. Leg/hip vertical motion remains visible across this interval. | Provisionally continuous as a source sequence, not final gait acceptance. Continuous-source derivative and displayed contact are separate gates. |

## Seam diagnostic

The 16→1 whole-canvas mean absolute RGB difference is 4.57549 on the composited review background. Internal transitions range from 2.81175 to 6.37205. This says only that the seam is not the largest pixel change in the cycle. Background area affects this metric; it is not a perceptual score, smoothness threshold or acceptance test. Exact per-transition data is in transition-diagnostics.json.

## Next repair order

1. Refine pad form and calf/cuff/boot material continuity on this retained narrow-stance source.
2. Polish elbow/glove articulation and coat depth without discarding the user-preferred motion direction.
3. Repeat the two-speed and seam inspection, then perform the unobstructed renderer measurement with image extraction outside the measured interval.

No numeric dimensions/amplitudes or unknown surfaces are approved by this review. Full four-facing work, complete real-renderer travel/contact, shared benchmark scene, encounters and device acceptance remain open. No new gameplay behavior or spec acceptance threshold is introduced.
