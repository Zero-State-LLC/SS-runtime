# BP-007 real-renderer projection comparison

Runtime parent 89800ef; spec c773f960ee8f53ac429828767fcd09f4da0d7cb3. CAPTURED / NOT_ACCEPTED. This experiment changes only the benchmark test, not shipping rendering or gameplay.

GameScene, WorldRenderer, SpriteKit and the existing HUD render the same isolated sample. Ground nodes are rotated 45 degrees then vertically compressed by 0.5 about the fixed center. Five named upright sprites (player, camera, building, newsbox, tree) retain their vertical form and use projected roots. Native output is 2112x978 pixels for 704x326 logical units. Candidate settings are zoom1 and sqrt(2) equal-ground-area zoom. The latter uniformly enlarges upright art as well. This is a still fixture with no enemies, attacks or input conversion; it is not a complete production projection implementation.

## Visual review

OBSERVED: diagonal paving better agrees with the oblique building edges than the unprojected paving. The rendered field is transformed with ground geometry. The same five upright images are not flattened into the ground.

FAILED: the unchanged bottom-center building placement is not registered to the projected collider; the magenta footprint falls across the front apron and nearby ground. Aligning the painted sidewalk edge alone would still not establish wall collision. The newsbox becomes obscured by the building. Equal-area zoom crops the building roof, camera and tree and increases HUD overlap. No framing candidate is accepted. Existing fixed layer ordering is not a validated occlusion solution.

Next source/renderer work must register the authored wall-contact polygon to projected authoritative corners, with explicit upright root placement. For an oblique square, the near corner is a projected world corner, not automatically the projected midpoint of the old south edge. Ground apron remains separate. Compare layering and camera center only after that contact registration, then run front/rear/corner traversal and legal encounter tests. Never move the collider to fit this still.

## Validation

Xcode Test-SSRuntime-2026.10.14_11-26-38--0700.xcresult: Passed, 87 tests, zero failures/skips (89 executions with dynamic cases). iPhone17Pro simulator, iOS26.5. The test checks SpriteKit node conversion against the analytic projection, uniformly scaled player canvas dimensions and unchanged HUD camera scale. These checks prove transformation mechanics, not visual correctness. Initial test assertion incorrectly expected unscaled SKSpriteNode.size after zoom; recorded as SS-runtime issue121, then corrected to exact expected Float-scaled dimensions. Other 84 Swift Testing tests passed on both runs.

Raw exported capture manifest and images are retained in capture/. No physical-device run or production asset admission occurred. Comparison plate labels are added outside the captures; images are reduced to704x326 using Lanczos for the plate.
