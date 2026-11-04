# Daily flavour

Read 2026-11-04 from `DailyFlavour` on `30a2cc6`. The look was not changed.

The flavour uses the salt-0 mix of the same day key as the daily seed. Grade is bits 0–7 mod 4: `CLEAR`, `OVERCAST`, `GOLDEN HOUR`, `NIGHT SHIFT`. Fog percent is bits 8–15 mod 3, choosing 80, 100, or 120. The headline is bits 16–23 mod 12, in this order: `FOG ADVISORY IN EFFECT`, `NEW CAMERAS APPROVED OVERNIGHT`, `CIVIC SEAM REOPENS AFTER REVIEW`, `TEMPORARY ORDER EXTENDED`, `QUIET HOURS ENFORCED`, `TRANSIT PATROL DOUBLED`, `INDEPENDENT REVIEW SCHEDULED`, `PUBLIC SAFETY NOTICE POSTED`, `NETWORK MAINTENANCE TONIGHT`, `PHOENIX STEPS LIGHTS RESTORED`, `CURFEW RUMOURS DENIED`, `OBSERVATION WEEK BEGINS`. The title detail is the grade, a middle dot, and `FOG N%`.

Clear draws no grade overlay. Overcast multiplies by `(0.78, 0.82, 0.86)` at alpha 1. Golden hour alpha-blends `(1.0, 0.62, 0.25)` at alpha 0.14. Night shift multiplies by `(0.42, 0.47, 0.66)` at alpha 1. The overlay sits above the ground and below actors, telegraphs, camera fields, and outlines. The fight thinning in [fog-thinning-2026-11-04.md](fog-thinning-2026-11-04.md) multiplies after this percent. The flavour does not enter the digest or the receipt.
