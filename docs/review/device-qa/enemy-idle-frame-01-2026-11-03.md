# Enemy idle frame 01 in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `8c37807`. No new frame was added. No sheet was made. The south idle cycles stay in [enemy-sprite-bounds-2026-11-02.md](enemy-sprite-bounds-2026-11-02.md).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`WorldRenderer.spriteBox` draws each of these five roles at 64×64. The anchor stays the one in the enemy note: (32, 56). Every frame below has canvas 64×64. This does not close #131 or #132.

## Fog Analytics Cloud

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_idle_n_01@1x.png` | x 8–59, y 17–60 | 52×44 | `aa9fb4fb264f4e55ad67c0904862007095120d9736f69fe2f4c2112a1bd0731e` |
| `actor_fogAnalyticsCloud_idle_e_01@1x.png` | x 3–62, y 9–55 | 60×47 | `8fd5c9547680ce2691d2fcfb0f89de2581297b0edbb808a416b575d8b109eb6e` |
| `actor_fogAnalyticsCloud_idle_w_01@1x.png` | x 1–60, y 9–55 | 60×47 | `2e745df503837f2de520845b92bb9baf0bb9dcd8d83e897f141a695dc091a248` |

## Cable Car Correlator

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_idle_n_01@1x.png` | x 2–53, y 5–56 | 52×52 | `4ba6914c1124f17e28c464adb8e12c10e8330ac363a08ae9404e55dbbf4c60d1` |
| `actor_cableCarCorrelator_idle_e_01@1x.png` | x 4–62, y 36–63 | 59×28 | `c220b2d09fcdec323c24f383215ecb81587841ee605da06d72e5aedb07543ea8` |
| `actor_cableCarCorrelator_idle_w_01@1x.png` | x 1–59, y 36–63 | 59×28 | `2a1ce3e0ea2d49c285568f28720d2f8bb6dbe3633933a6bb469b87e47697ac46` |

## Sutro Signal Witch

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_idle_n_01@1x.png` | x 7–58, y 14–63 | 52×50 | `da3a346e9ff682fbeb4314417bed1820d21d4d1b0688877e893fb2b1f02eb312` |
| `actor_sutroSignalWitch_idle_e_01@1x.png` | x 11–62, y 12–62 | 52×51 | `5d623a2d158e7c65b379d1be45cdec43827bd4bb02383fc10bd81a493fc8caf5` |
| `actor_sutroSignalWitch_idle_w_01@1x.png` | x 1–52, y 12–62 | 52×51 | `2d28e29f4b0ce1331649ce5727b96999c537a85ab4ec0f561a5baab71ada5f4d` |

## Autonomous Informant

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_idle_n_01@1x.png` | x 18–50, y 11–56 | 33×46 | `a36c807d9597e6d203c6add880b7864d78e193d0166a24bfe8b3f54bba375bf2` |
| `actor_autonomousInformant_idle_e_01@1x.png` | x 3–60, y 27–61 | 58×35 | `77375a406009f3cf3d0f8d898d22eabe3c88a85bd3c351912114bb02ee667a72` |
| `actor_autonomousInformant_idle_w_01@1x.png` | x 3–60, y 27–61 | 58×35 | `33364994a595da724528c02489d07c562f9f846a75bdaab179d319dc89847328` |

## Victorian Vendor

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_idle_n_01@1x.png` | x 13–56, y 17–60 | 44×44 | `a973d488db8e006bb8e7ea5a2f641fe51a815b2089cd646044251a0184709992` |
| `actor_victorianVendor_idle_e_01@1x.png` | x 6–62, y 4–60 | 57×57 | `380dfdd679a3e3e019a0d01856620e33ae009b817201311de09b4732a498df74` |
| `actor_victorianVendor_idle_w_01@1x.png` | x 1–57, y 4–60 | 57×57 | `6340cce0fec0309c00796b70fb0fda410509073160e039bfbd04ee66edf5214f` |
