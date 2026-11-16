# Whole-game visual acceptance contract

Status: coordinator implementation checklist derived from the approved benchmark and the owner's November 16, 2026 overall-scene clarification. This is not new gameplay authority, a changed benchmark, or owner acceptance of a candidate.

## Fixed target and boundaries

The unchanged `../bp001-decision-20261116/street-corner-approved-concept.png` is the visual authority. The alternate midpoint concept and generated candidates are not replacement targets. The selected midpoint describes +45-degree ground rotation followed by half-height scaling, with upright source art attached to projected roots. It does not select a new source-camera elevation, final zoom, collision footprint or production policy.

Use the pinned specifications, BP-001/005/007/008/012, the approved ten-slice intent and the existing production/admission/merge gates. Preserve the simulation, input, authoritative Camera geometry, source originals and phases 5/13. A quiet scene with manually selected contents is a composition fixture, not a legal encounter or proof of the complete game.

## Scene-wide visual requirements

| Dimension | Required read from the original benchmark | Current observed mismatch | Evidence needed before recommending acceptance |
|---|---|---|---|
| Composition | A coherent street corner with architecture, narrow pavement and darker road, rather than a uniformly tiled plaza | Road placement improves in the diagnostic, but the full composition still differs | Ordinary full-scene comparison at all retained zooms, with framing differences disclosed |
| Architecture | Low stone facade, charcoal recesses, restrained trim and corner entry | Existing saturated two-storey facade has different proportions and materials | New source in the real renderer, explicit wall-base registration and unchanged collision overlay |
| Ground | Muted grey pavement with broad wear, readable curb and embedded street detail | Beige repeat dominates, uniform tile motif remains visible | Repeated texture preview and native scene, both close and distant framing |
| Palette and materials | Grey/charcoal structure, subdued warm stone, small amber/cyan accents | Broad turquoise/orange areas and beige ground compete with actors | Native and grayscale full scenes. Histograms are diagnostic only, not an aesthetic pass |
| Scale and perspective | Actors, building doors, props and Camera read as sharing one physical world | Camera, building and actor proportions do not yet form a coherent scene | Same-scale scene plus landmark/footprint records, not isolated sprite thumbnails |
| Ground contact | Feet, pole base, walls and props visibly rest on their registered surfaces | Missing or weak contact shading, uncertain source registration | Normal-speed movement, planted-contact observations, stills at front/rear/corners |
| Contours and visual emphasis | Thin dark source edges, detail remains subordinate to actor/action read | Bright Player border, strong field edges and large HUD compete with artwork | Ordinary HUD/field-on gameplay. Any alternate treatment is a separate labelled comparison, not a production change |
| Lighting | Shared overhead-left source lighting and consistent contact cues | Sources have inconsistent baked lighting and absent contact shadows | Source review and integrated scene. No baked screenshot shadow is evidence of a reusable shadow system |
| Motion and depth | Stable identity, ground contact and readable occlusion through movement/combat | Static captures do not demonstrate these | Live scene recording with frame/state evidence, traversal and projectile/contact checks |
| UI and accessibility | Gameplay remains legible with actual controls and required accessibility settings | Staging can hide the very overlays that need evaluation | Ordinary interface first, plus accessibility states and supported viewports |

These requirements are qualitative review criteria. No invented numerical tolerance or similarity score may convert an obvious mismatch into acceptance. Composition comparison across different aspect ratios must preserve aspect ratio and disclose cropping. Never stretch the reference to force a match.

## Order of work

1. Keep the original benchmark and every retained control immutable.
2. Use the existing-asset diagnostic to establish which changes actually affect the complete scene. Do not call a road-layout adjustment a completed visual correction.
3. Repair source assets against the fixed reference. Before native substitution, record actual dimensions, provenance, wall-contact/ground landmarks, explicit anchor, uniform scale, correspondence and residuals. Unknown hidden corners remain unknown. Prompted coordinates and alpha bounds are not measured wall geometry.
4. Integrate one complete representative scene in test-only resources. Ordinary HUD/field-on presentation is the primary view. Staged art-only presentation is secondary and lists every suppression.
5. Review that scene in motion, through occlusion and a crowded legal encounter, before expanding rejected source families into states or animation.
6. Extend the coverage matrix across all existing environment and enemy roles, Camera integrity/field-off states, combat cues, interface states, viewport sizes and accessibility modes. Reuse a verified style basis rather than independently inventing each asset.
7. Admit only explicitly approved coverage. Record uncovered combinations and unresolved defects. A quiet fixture cannot mark the rest of the game complete.

## Acceptance record per coverage row

Every row must identify the exact source/configuration hashes, fixture or legal replay, viewport, camera/zoom, rendered state and evidence path. Record four independent statuses:

- **Technical evidence:** missing, failed, or verified, with the actual command/result.
- **Coordinator visual review:** not reviewed, mismatch, or recommended, with concrete observations.
- **Owner acceptance:** not requested, pending, rejected, or explicitly accepted, with the applicable decision.
- **Production admission:** not requested, blocked, or explicitly admitted under the repository's existing gates.

Never infer the later statuses from the earlier ones. Automation checks evidence integrity, coverage and regressions. It does not certify visual fidelity.

## Regression and delivery gate

Before presenting a candidate, the coordinator reviews the entire ordinary scene against the unchanged benchmark at native and half scale, in color and grayscale, and reviews motion for any affected animation/contact/depth behavior. Keep an explicit mismatch list with owner and next action. Preserve failed runs and rejected artwork. Require the actual affected checks to pass without reducing assertions, relabelling missed poses as expected, hiding overlays, or substituting static exports for live cadence.

Issue237 remains the live playback 16-pose failure investigation. Issue238 concerns the separate review-harness fixed-time clamp. Passing a different head or a static capture does not close either automatically.

## Current gate

The first whole-scene packet contains 36 static quiet plates and a technically verified composition comparison. It does not meet the visual target. Building, paving material, contact shadows and ordinary overlay prominence remain open. The generated stone-building first sample is source work only until its actual footprint and registration are verified. No complete-game acceptance or production readiness is claimed.
