# Captain housing frames

Measured 2026-11-03 from the runtime asset bytes on `df637da`. No new frame was added. The five municipal housings stay in [camera-frame-bounds-2026-11-02.md](camera-frame-bounds-2026-11-02.md).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0. A piece is a 4-connected group of at least 20 such pixels. Smaller groups are specks.

`WorldRenderer` draws each `captainHousings` entry at 64×96. The PNG canvas is 64×96, so the draw size matches the canvas. That loop does not set `anchorPoint`, so the sprite keeps SpriteKit's center, `(0.5, 0.5)`. The position is the emitter point. `civic-seam-arena-004` has three emitters: `captain-emitter-01` at (1888, 832), `captain-emitter-02` at (2208, 832), and `captain-emitter-03` at (2048, 448). The emitter whose Temporary Order field is live uses `env_camera_captain_active`. The others use `env_camera_captain_idle`. When no field is live, all three use the idle file.

Each file below is one piece. Neither file has a speck.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `env_camera_captain_idle@1x.png` | 64×96 | x 3–59, y 3–90 | 57×88 | `e6b0e11b0ba1a447585e027a0720de7a11ea7e04b8e882fcf1423b72597ba15c` |
| `env_camera_captain_active@1x.png` | 64×96 | x 4–59, y 3–90 | 56×88 | `4ceb2e9d7b6ed3669f929c62789fec5e0fe9f5b924ae6030d67c66e82c7596e1` |

This does not move an emitter, and it does not close T1046.
