# Boss sprites against the body radius

Measured 2026-11-03 from the runtime asset bytes on `c700b82`. No new frame was added. This note is `algorithmicModerate` only. It does not change D-118 path search, and it does not change the boss step of 120 in `IsolatedKernel`.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`combat-content-009` gives this boss radius 30 and base speed 96. `WorldRenderer.spriteBox` draws the role at 96×96. Every clip of this role in `clip-metadata-001` has anchor (48, 84) in that box. `SpriteLibrary.anchorPoint` turns that into SpriteKit (0.5, 12/96). The body circle is centered on the entity, which is that anchor.

This role has no idle clip. The states are `safetyRationale`, `narrowTailoring`, `temporaryOrder`, `independentReview`, `phaseTransition`, `stagger`, and `defeat`. The table is south frame 01 of each state.

Every measured frame has canvas 96×96. There are 172 frames. Across every frame, nontransparent width runs 35–88 and height runs 39–88.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_algorithmicModerate_safetyRationale_s_01@1x.png` | x 13–90, y 0–87 | 78×88 | `832d937f36bb9f6c1ebe8ca7d4925142da6f82c5afc39aaa34b93d6a105a1ac0` |
| `actor_algorithmicModerate_narrowTailoring_s_01@1x.png` | x 11–85, y 0–87 | 75×88 | `dc9c3e0f617b0a0e7645d413eb61ca31c1a0cc1cd89df301ae38c7567d9fcac0` |
| `actor_algorithmicModerate_temporaryOrder_s_01@1x.png` | x 12–91, y 28–83 | 80×56 | `6aed0d8fdf29de26a5e70c92a5733a9e0b46f79c8a167e2556c62546c67a4ba7` |
| `actor_algorithmicModerate_independentReview_s_01@1x.png` | x 4–91, y 0–87 | 88×88 | `677fc767408cee1851a309a07e9d02ddf2aa74df0848dbdedb986ad126a8ea68` |
| `actor_algorithmicModerate_phaseTransition_s_01@1x.png` | x 19–80, y 0–87 | 62×88 | `992c9c1932ef4995db7d914baaeb8ca34df45efc82612abae08dab909b56cba1` |
| `actor_algorithmicModerate_stagger_s_01@1x.png` | x 42–91, y 31–83 | 50×53 | `f51c4615bcfc7682b87fd06d281ca2921da423e39a671c18fa84ea011efe7afa` |
| `actor_algorithmicModerate_defeat_s_01@1x.png` | x 9–85, y 0–87 | 77×88 | `f06739049fe24fded4aa913afcc1b318c3cf8d7f5a68890ab0f0af6d92817744` |
