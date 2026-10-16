# Boot overlaps and combined source check — BP-002 / BP-008

The twenty-four-layer south source adds two boot overlaps cut from the retained upper-boot leather pixels. Both source rectangles and original layer hashes are recorded in overlap-provenance.json. The reused pixels are concealed by the original opaque parent in neutral. They are a texture overlap, not a newly discovered hidden heel or anatomical model.

The south source now draws the front coat panels and belt/torso before the thighs in compositing order (above the legs in the saved top-to-bottom stack). This corrects the observed source pose where the moving thigh crossed in front of a coat panel. It is an authored south-facing order, not a general solution for all facings or movement phases.

Neutral remains exactly unchanged. Both signs of the small ±8° boot controls were inspected in enlarged comparisons; the visible cut gaps close. One combined pose exercises shoulders, elbows, hips, knees, boots and ±4px cloth deformation together. Six saved diagnostic poses include neutral, the four isolated boot extremes and the combined pose. These are diagnostic holds, not a locomotion animation. The GIF has not been reviewed in the runtime renderer.

Use Python 3 and Pillow with render_source.py, rig.json and source/. Joint angles and cloth offsets can be passed through --angles-file and --deformations-file respectively. diagnostic-poses.json records the comparison inputs. Existing --pose values remain the preceding rig's source poses; use the explicit files for the new combined comparison.

Still required: an authored heel/toe contact model, elevated limb depth/foreshortening, support/flight keys, full gait and four-facing review, actual world-travel comparison and device evidence. A boot seam closing does not establish correct contact or foot rotation. Production resources, timing metadata and gameplay remain unchanged.
