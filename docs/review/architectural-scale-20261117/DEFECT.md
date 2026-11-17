## Review-tool defect: source proxy stretches square ground texture into rectangular arena

BP-001/007/012, T1045. Scoped to the new architectural proportion review packet, not the shipping renderer.

Coordinator actual-image review at2026-11-17 01:25UTC found the initial source proxy changed apparent paving: black apron regions and a small-paver patch differed from retained V9. Initial12source checks passed, so their self-recomposition oracle did not independently validate texture-coordinate authority.

Cause: initial `docs/review/architectural-scale-20261117/source/build.py:234-244` used the ground witness sprite size2304x1536 as the texture domain. The retained producer `AppTests/BlockedBaseCurbSceneTests.swift:308-313` uses square source registration/tileUnits2304 and clips to the2304x1536arena. Clipping is not texture compression.

Related framing defect: initial standalone current/proposed view PNGs added a30px header, departing from704:326. Scene labels belong outside the scene frame.

Required repair: preserve first failed renderer/output/logs, use exact square source UV domain, add independent world-point UV and raw-frame dimension regressions, retain the identical single proposed geometry, inspect corrected images at all three zooms and validate from tracked-only export. No changed authority, aesthetic retry, native execution, old-file edit or weaker assertion. Do not close automatically or infer art acceptance.
