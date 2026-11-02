# Enemy sprites against the body radius

Measured 2026-11-02 from the runtime asset bytes and `combat-content-009` on `31345cd`. No new frame was added. No sheet was made. This is evidence for issue #117 row 3. It does not admit a character and it does not change a medal.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`WorldRenderer.spriteBox` draws each of these five roles at 64×64. Every one of their clips in `clip-metadata-001` has anchor (32, 56) in that box. `SpriteLibrary.anchorPoint` turns that into SpriteKit (0.5, 8/64). The body circle is centered on the entity, which is that anchor, and its radius is the `combat-content-009` value below. The circle is in the same units as the 64×64 draw: one image pixel is one world unit when the frame's canvas is 64×64.

Every measured frame of these five roles has canvas 64×64.

The south idle cycle is the four `idle_s` frames. The span line gives the smallest and largest width, and the smallest and largest height, across every frame of that role. Those four numbers are not one frame.

## Fog Analytics Cloud

Role `fogAnalyticsCloud`. Body radius 18. Diameter 36. 96 frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_idle_s_01@1x.png` | x 3–58, y 15–49 | 56×35 | `53f9a0fadce98a33747b6b6d3e0377503396b7e8db5c682646ad096b6e1cc8ce` |
| `actor_fogAnalyticsCloud_idle_s_02@1x.png` | x 4–58, y 8–60 | 55×53 | `b1650b45e42da3ef7647344729abb0fc6539200ac71ea9731b7a3408c04d405e` |
| `actor_fogAnalyticsCloud_idle_s_03@1x.png` | x 7–59, y 13–54 | 53×42 | `e2a33d09bec5b94852b59ecab01db528dbd5cded354de0d0d882df5a397f7047` |
| `actor_fogAnalyticsCloud_idle_s_04@1x.png` | x 6–51, y 15–49 | 46×35 | `f582903f2d8fe59985cea80b72e86806a9548a6558d06e0f08e05b725251e706` |

Across every frame, nontransparent width runs 32–64 and height runs 23–54.

## Cable Car Correlator

Role `cableCarCorrelator`. Body radius 20. Diameter 40. 108 frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_idle_s_01@1x.png` | x 13–61, y 12–55 | 49×44 | `0e76845684606c8adaef68376e3e8fc8ada402e963950988064b72ef04fb0740` |
| `actor_cableCarCorrelator_idle_s_02@1x.png` | x 13–57, y 6–63 | 45×58 | `d115de8cfaa20e6ca5508fd2485f773f27f273ff87bc37404174f2f0e3175138` |
| `actor_cableCarCorrelator_idle_s_03@1x.png` | x 1–62, y 6–62 | 62×57 | `5a8086c344d586430f487c456bec1425e4e6050d934162596dffc1fa3f9511e3` |
| `actor_cableCarCorrelator_idle_s_04@1x.png` | x 13–62, y 15–55 | 50×41 | `8fa0292e31cc1892904617bcf30fc3ed6b196e1568f05a2e0dd58a5f1f6f5e8b` |

Across every frame, nontransparent width runs 39–64 and height runs 11–60.

## Sutro Signal Witch

Role `sutroSignalWitch`. Body radius 18. Diameter 36. 96 frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_idle_s_01@1x.png` | x 32–63, y 14–55 | 32×42 | `1538447add8f01c7e6e4fb9269ac350134e02d45a2ecdaf1456363dccc2e0e80` |
| `actor_sutroSignalWitch_idle_s_02@1x.png` | x 0–62, y 14–63 | 63×50 | `3ddb1b182e470b630c36dbe241b1fef52fe87a50dc44d0c81f7e19fbfc33d703` |
| `actor_sutroSignalWitch_idle_s_03@1x.png` | x 18–54, y 15–60 | 37×46 | `98f94b5fb63c88ba5facb72096373e93a9a1bb6a08e7a58035c846fd77c1c864` |
| `actor_sutroSignalWitch_idle_s_04@1x.png` | x 16–60, y 14–55 | 45×42 | `91c1d668808a63f80284368207e908511d8ae317c460fcab62c638abec0b4263` |

Across every frame, nontransparent width runs 23–64 and height runs 9–58.

## Autonomous Informant

Role `autonomousInformant`. Body radius 16. Diameter 32. 72 frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_idle_s_01@1x.png` | x 3–57, y 6–55 | 55×50 | `b97e19a99574e39adb26c0e34c8de911d447f1ee686b89b893a78266513e7d3c` |
| `actor_autonomousInformant_idle_s_02@1x.png` | x 13–54, y 9–55 | 42×47 | `5cc8f64f3741540711124be14772946c73638cc5daa7a953e78c2d0b8d835666` |
| `actor_autonomousInformant_idle_s_03@1x.png` | x 12–48, y 11–55 | 37×45 | `b2dd39f70924cbd16647545864da7fb528dabbda7fd08665edec6ae94f4e7e75` |
| `actor_autonomousInformant_idle_s_04@1x.png` | x 8–60, y 10–55 | 53×46 | `e8a1783e6c407e7c3e1a8e66455c9f818dba0a1b9ff320168cf43dd27a95c3a7` |

Across every frame, nontransparent width runs 24–64 and height runs 17–56.

## Victorian Vendor

Role `victorianVendor`. Body radius 22. Diameter 44. 96 frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_idle_s_01@1x.png` | x 10–62, y 14–57 | 53×44 | `a11ffe530b21e518451503972da4b1591f260b73d6bfbe95541e73dae9f48a82` |
| `actor_victorianVendor_idle_s_02@1x.png` | x 4–61, y 2–62 | 58×61 | `429f3f655e0fa6b7fe77957238246df448ea46fc4ecf181e3eba4886491fb18b` |
| `actor_victorianVendor_idle_s_03@1x.png` | x 8–59, y 13–60 | 52×48 | `19416e86a08b1b4e86fd2a95061eda93f0c0b134ea048f6d45d5def6f03b3894` |
| `actor_victorianVendor_idle_s_04@1x.png` | x 8–61, y 9–56 | 54×48 | `195b6ad21812e3d47f55936c2d59236563e813c8e028bfaec6df12d8e2186ab3` |

Across every frame, nontransparent width runs 30–64 and height runs 16–62.
