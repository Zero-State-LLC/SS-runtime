# Cable recover frames in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `df637da`. No new frame was added. Frame 01 in these directions stays in [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md). South frames 02–03 stay in [enemy-south-action-rest-2026-11-03.md](enemy-south-action-rest-2026-11-03.md). The anchor stays the one in the enemy note: (32, 56).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`cableCarCorrelator_recover` is frames 02–03. Every frame below has canvas 64×64. The table is those frames in north, east, and west: 6 files. This does not close #131 or #132.

## Recover

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_recover_n_02@1x.png` | x 3–63, y 8–56 | 61×49 | `af7bc1d849b48c7650ceb998f7d81f57b31008db1049a2fa2c08d046680fc20f` |
| `actor_cableCarCorrelator_recover_e_02@1x.png` | x 4–61, y 17–62 | 58×46 | `f14f9fc2d1389bce04953bcf6b51474751a1d84943a8cad4eb844eb4307134f4` |
| `actor_cableCarCorrelator_recover_w_02@1x.png` | x 2–59, y 17–62 | 58×46 | `b4396d2b042510faa575ce490048889b0f3812df14e059f9f1819ffdbb059e02` |
| `actor_cableCarCorrelator_recover_n_03@1x.png` | x 0–39, y 8–56 | 40×49 | `71ea56b9a4e30fa3f1382fd941c89b379e13ac1f2400817ad2c2fbf41bc70e8e` |
| `actor_cableCarCorrelator_recover_e_03@1x.png` | x 6–57, y 23–63 | 52×41 | `f17ed7c59f2ec0ca9a6e6c6ee3b5618c0c20d01f381edf73bec31312ddaa05c9` |
| `actor_cableCarCorrelator_recover_w_03@1x.png` | x 6–57, y 23–63 | 52×41 | `69a102abf82e39b74b1dd63ec20d18d336403f31fca5be4e6fda662db6921df8` |
