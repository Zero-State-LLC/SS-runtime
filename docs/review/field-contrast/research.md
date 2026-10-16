# Camera field contrast research and comparison

Specification: SS-specs d859658dc4029a3453c247c9b0d792229c1130fc, BP-001/BP-010, D-104 / T1045–T1046. The accepted visual-coherence intent covers this repair; no new gameplay or setting is introduced.

Observed baseline: ecac1ef shared-scene grayscale captures lose much of the pale field fill against paving. Geometry tests do not establish visibility.

Primary guidance checked 2026-10-14:
- Microsoft XAG 102: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102 supports borders and discusses dark/light outline examples for cues on changing backdrops.
- Microsoft XAG 103: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103 calls for non-colour signifiers and distinguishes simulated filters from user testing.
- W3C G209: https://www.w3.org/WAI/WCAG21/Techniques/general/G209 describes contrasting boundaries between adjoining graphical regions. Its web criterion is not adopted as a blanket game-playability score.

Authored comparison parameters: control retains existing field fill and clear stroke; dark uses gray 0.08 at width 1.5 logical world units; paired uses gray 0.08 at width 3 with gray 0.95 at width 1 on the same clipped path. These are candidate parameters, not research-derived constants or approved production values. Solid-clipped paths, origin, heading, fills and authority stay fixed. Shape thickness extends around the centreline visually and does not expand the simulation field.

Review-only controls are excluded from Release. Both standard and Captain paths use the helper, and field removal deletes child contours with their parent. Tests exercise exact path equality, reuse, no child growth, restoration to control, destruction and reset. Quiet shared-scene captures compare all three styles at all four standard-camera integrity states with the actual GameScene/HUD. Further backdrop/encounter/motion-mode evidence remains required before selection.
