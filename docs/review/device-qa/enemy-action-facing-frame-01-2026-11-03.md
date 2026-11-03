# Non-idle enemy frame 01 in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `8366209`. No new frame was added. No sheet was made. South frame 01 of these states stays in [south-state-frame-01-2026-11-03.md](south-state-frame-01-2026-11-03.md). Idle frame 01 in north, east, and west stays in [enemy-idle-frame-01-2026-11-03.md](enemy-idle-frame-01-2026-11-03.md).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`WorldRenderer.spriteBox` draws each of these five roles at 64×64. The anchor stays the one in the enemy note: (32, 56). Every frame below has canvas 64×64. Radii stay the values in the enemy note. This does not close #131 or #132, and it does not prove a live cycle.

The table is the non-idle states already measured for south: 25 clips, 75 files. Anticipate and commit keep their shipped file names (`pulse`, `charge`, `cast`, `pursuit`, `throw`, and the matching commit names). The informant has no move clip in this set. The cable car has a recover clip. The elite is not in this note.

## Fog Analytics Cloud

Clip `fogAnalyticsCloud_move`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_move_n_01@1x.png` | x 3–61, y 19–57 | 59×39 | `72f0ee199521d07f577c4d76aea02d8a179f1e73b8ec7a10c27f9c2af499111f` |
| `actor_fogAnalyticsCloud_move_e_01@1x.png` | x 6–59, y 21–61 | 54×41 | `2de5491e1ecb8332985bd6cbdea8306688e30ea6ac78932a96d218fc77020ed4` |
| `actor_fogAnalyticsCloud_move_w_01@1x.png` | x 4–57, y 21–61 | 54×41 | `3f94d943966fc92a196ed205b872d2836d30b4bccf32c32fecf7e187394d9b72` |

Clip `fogAnalyticsCloud_anticipate`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_pulse_n_01@1x.png` | x 2–62, y 6–56 | 61×51 | `b5c725fa82709d3b3645a774bf9a3d397a24358122c7d39c88ae77fe558ebb20` |
| `actor_fogAnalyticsCloud_pulse_e_01@1x.png` | x 15–49, y 5–51 | 35×47 | `d8de246693783fc66c57b67d0a2311bf769dadf054d184dedb38198ee7905639` |
| `actor_fogAnalyticsCloud_pulse_w_01@1x.png` | x 14–48, y 5–51 | 35×47 | `6f4d31449633aee736615ebb52ada7300331c4b45bcb27f5626f881cfe10e4a3` |

Clip `fogAnalyticsCloud_commit`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_pulseCommit_n_01@1x.png` | x 6–63, y 9–58 | 58×50 | `abe9c5a9efc0be8cde795684e386d482fe1e1b1829e675400e14363d93e93550` |
| `actor_fogAnalyticsCloud_pulseCommit_e_01@1x.png` | x 12–57, y 4–50 | 46×47 | `e3d0383a42d9ea22435def6886f62a25e521dc401128f7017aa8ef5d010067e7` |
| `actor_fogAnalyticsCloud_pulseCommit_w_01@1x.png` | x 5–50, y 4–50 | 46×47 | `96d0479b9aef746dedb2ef9b27c6861e166ffa9be81773bcf57b7d7593d35d5c` |

Clip `fogAnalyticsCloud_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_hurt_n_01@1x.png` | x 7–58, y 11–55 | 52×45 | `360d32ac110c4aba10f3fa832b2fe1e44535fe71074569d7c7bb8d3768ab8178` |
| `actor_fogAnalyticsCloud_hurt_e_01@1x.png` | x 10–52, y 13–56 | 43×44 | `23e9c8da154013f00dc606afe856303bcd265d694d5fe0bc7aeae46b144933cf` |
| `actor_fogAnalyticsCloud_hurt_w_01@1x.png` | x 11–53, y 13–56 | 43×44 | `a2afd0c4ad9035a8a9a9fe02d0f8ba8935bcc7a2787d5ed4f08fb127fe3a9e48` |

Clip `fogAnalyticsCloud_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_defeat_n_01@1x.png` | x 6–63, y 17–47 | 58×31 | `39f5af3c8eb1a09a313e00c72a00476a0c4742a828c8383faf8af733a293f519` |
| `actor_fogAnalyticsCloud_defeat_e_01@1x.png` | x 8–59, y 18–51 | 52×34 | `565c8f46898e7d7e85bde233f7b133595d397241ee1ea135c439447b799e37cb` |
| `actor_fogAnalyticsCloud_defeat_w_01@1x.png` | x 4–55, y 18–51 | 52×34 | `98e49dc443241db86b1be441a21499c8057f57910b020dbe8bc8f21b7ef6dc5d` |

## Cable Car Correlator

Clip `cableCarCorrelator_move`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_move_n_01@1x.png` | x 11–58, y 4–58 | 48×55 | `cdfda4e07ffc944e397b5e12d02cb4d32f0a18057adeccf9cfe024c3165cf095` |
| `actor_cableCarCorrelator_move_e_01@1x.png` | x 3–62, y 39–63 | 60×25 | `f7e0f496f67daf380f8d3815b331fefdef160a58319522148c65655f56860a61` |
| `actor_cableCarCorrelator_move_w_01@1x.png` | x 1–60, y 39–63 | 60×25 | `f28e33bcc34a487b4a513e2ee97eb97524f90b9632705742c80b4258642d719d` |

Clip `cableCarCorrelator_anticipate`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_charge_n_01@1x.png` | x 11–62, y 3–55 | 52×53 | `1acdb4292765ebaffdc378d1dfc9ac0250ea3bbaf20d7b8d1f25f17dfe6ddd20` |
| `actor_cableCarCorrelator_charge_e_01@1x.png` | x 4–58, y 7–55 | 55×49 | `2a65b806d2578677530a722a1f5d5704b0eab0f4adec9d8a6a1e26edb01df641` |
| `actor_cableCarCorrelator_charge_w_01@1x.png` | x 5–59, y 7–55 | 55×49 | `4a53e35821657273d593fca1e8cd11a325d206f8722dee7885823f5b6f1d1985` |

Clip `cableCarCorrelator_commit`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_chargeCommit_n_01@1x.png` | x 19–61, y 4–60 | 43×57 | `f945c3f51105ea1d2f5694227284f73c43aca22d2cf0e38de51697736fbb3bd5` |
| `actor_cableCarCorrelator_chargeCommit_e_01@1x.png` | x 5–59, y 9–55 | 55×47 | `951a6667f1426aee24a1196ff914d09b633556d7fd853c7ae52fd38a8e16a172` |
| `actor_cableCarCorrelator_chargeCommit_w_01@1x.png` | x 4–58, y 9–55 | 55×47 | `ce51f9fe068cfb97a7489386c843f2a67ecb56c1040b0c4eca9bea4b126a8c82` |

Clip `cableCarCorrelator_recover`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_recover_n_01@1x.png` | x 16–62, y 8–56 | 47×49 | `3b4dd8e8418be3bda4237041955ebba0c393d29ea4daedcd234cd1d9f6d34a48` |
| `actor_cableCarCorrelator_recover_e_01@1x.png` | x 7–59, y 22–62 | 53×41 | `19c6a795a1162bdd20dd898f37b3040b43fa6c1d9cd8516c56cb54c25b7b7ddd` |
| `actor_cableCarCorrelator_recover_w_01@1x.png` | x 4–56, y 22–62 | 53×41 | `9f1de1f0e4b97e28a4c5b700f30b10db8e2253169294bc3ce3b4269785a7665f` |

Clip `cableCarCorrelator_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_hurt_n_01@1x.png` | x 16–56, y 1–56 | 41×56 | `8fdc7d9752eee77fe732004ee1d260c765ac8c858c3d883f10530ff9aefa764d` |
| `actor_cableCarCorrelator_hurt_e_01@1x.png` | x 8–62, y 22–63 | 55×42 | `8d537a4e110e7bcd4168214410e38c7ac4cab678fc49e23c297c221115ed2812` |
| `actor_cableCarCorrelator_hurt_w_01@1x.png` | x 1–55, y 22–63 | 55×42 | `8fdaa5f3d47f974952170d312baf8497bab0daada55d25c541feb29e44b8dbf7` |

Clip `cableCarCorrelator_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_defeat_n_01@1x.png` | x 13–56, y 16–63 | 44×48 | `1eeadc014b50e7feaa310d76cf271a2338a24cef2819891353de2132b6ed4f37` |
| `actor_cableCarCorrelator_defeat_e_01@1x.png` | x 6–63, y 38–63 | 58×26 | `d990787895c9478817365983f599655544870ccb5f275a35d3adbc85693156e2` |
| `actor_cableCarCorrelator_defeat_w_01@1x.png` | x 0–57, y 38–63 | 58×26 | `e18364c3f161bc28cb1352bb035d245e95a2160503f7467d06292459cacd1c0f` |

## Sutro Signal Witch

Clip `sutroSignalWitch_move`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_move_n_01@1x.png` | x 16–55, y 15–55 | 40×41 | `c6791af034c31b048240829097fb15a2bca9c25e9f21a239be48503c9b4ae74a` |
| `actor_sutroSignalWitch_move_e_01@1x.png` | x 8–59, y 20–63 | 52×44 | `160bdb401303513d38a264bfeedcb10675625e5a646a315a27f88bc424b7dd26` |
| `actor_sutroSignalWitch_move_w_01@1x.png` | x 4–55, y 20–63 | 52×44 | `8b5dfac4fedc47f36a79174c00751389b279d2f97f89a4c6d14e349743d61d7a` |

Clip `sutroSignalWitch_anticipate`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_cast_n_01@1x.png` | x 10–47, y 2–56 | 38×55 | `93afc62761837c1501290b46e5a9f2b587bd25c1bd15b079ec614231780dfbc0` |
| `actor_sutroSignalWitch_cast_e_01@1x.png` | x 18–49, y 14–51 | 32×38 | `36e1ccfea9aac113fe9b57a6d34cc4c1d468307ef8f4746df88b2e3d6d66887b` |
| `actor_sutroSignalWitch_cast_w_01@1x.png` | x 14–45, y 14–51 | 32×38 | `a8ddd1feaa8ab378ebd920404ac4fc13707f1545acc80f1c36ef336fa45ead1d` |

Clip `sutroSignalWitch_commit`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_castCommit_n_01@1x.png` | x 27–55, y 9–56 | 29×48 | `9c366175d936553663d94305c7cd3468f3b22535ede84a8d2214be5d9fc2b194` |
| `actor_sutroSignalWitch_castCommit_e_01@1x.png` | x 9–59, y 0–55 | 51×56 | `eaeb8f917319116fa42760673b69ad87ac9f81291049ecd603239ecb49faf905` |
| `actor_sutroSignalWitch_castCommit_w_01@1x.png` | x 4–56, y 0–55 | 53×56 | `1ee469f20cb6a2380ed252e1ee3fe65249ce8fe6693b8819427bb454a211efeb` |

Clip `sutroSignalWitch_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_hurt_n_01@1x.png` | x 12–62, y 6–56 | 51×51 | `4c042c7069af7cc8219387e483c5a38c6a7f3a4d65e3e64470d1b6d1d117302c` |
| `actor_sutroSignalWitch_hurt_e_01@1x.png` | x 6–53, y 3–55 | 48×53 | `175c5037944b7dc0eb61e11e9b92598c538f9bb1dc6f5655e89b26dbada9f141` |
| `actor_sutroSignalWitch_hurt_w_01@1x.png` | x 10–57, y 3–55 | 48×53 | `d272d59e1f7ca26e9494d8ea6543d0f80e0ac2f7ddf60d9ab6e3a414fb9f57ff` |

Clip `sutroSignalWitch_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_defeat_n_01@1x.png` | x 6–51, y 8–60 | 46×53 | `b6d2ee9ad8f719a797704c9a21ab725b873e9b415e963fbfd4a81fb88d2419f3` |
| `actor_sutroSignalWitch_defeat_e_01@1x.png` | x 8–54, y 9–63 | 47×55 | `ba863d67affa10c15d9a2bd1137d12b9fe41174e3732bb8a4c090632570b3dde` |
| `actor_sutroSignalWitch_defeat_w_01@1x.png` | x 9–55, y 9–63 | 47×55 | `13927f987f9ffe76c16d658296208392070d10a44ecb08f60d396235c654f89a` |

## Autonomous Informant

Clip `autonomousInformant_anticipate`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_pursuit_n_01@1x.png` | x 28–56, y 8–53 | 29×46 | `272fd2844d660cbed52992880cb4faad4a5f11f0ffd01d8eaa98c4eb2559ca1a` |
| `actor_autonomousInformant_pursuit_e_01@1x.png` | x 11–52, y 0–44 | 42×45 | `227623f1155040d362164c92d7c72ab8b76be676b11763a685ad86ab6d8e21c7` |
| `actor_autonomousInformant_pursuit_w_01@1x.png` | x 11–52, y 0–44 | 42×45 | `6d41595fa0ce0782333399d22f890ef4a649f73c33ae953c22a47744c6a3a496` |

Clip `autonomousInformant_commit`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_pursuitCommit_n_01@1x.png` | x 30–56, y 13–55 | 27×43 | `e33fd39484122e389d411df41dffdb4c316734d220be25ab2ad76017fbd4fd8a` |
| `actor_autonomousInformant_pursuitCommit_e_01@1x.png` | x 5–59, y 7–52 | 55×46 | `87bfb7aa061b75a5ec2c19012e85e888a75824290613ef1ed9e551cf62df4cf1` |
| `actor_autonomousInformant_pursuitCommit_w_01@1x.png` | x 4–58, y 7–52 | 55×46 | `87e45ca15c8c31cc34f2561918856de6322f4807cad538120ca7e58cdd1cdc5b` |

Clip `autonomousInformant_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_hurt_n_01@1x.png` | x 24–59, y 6–55 | 36×50 | `cc2b36318dfa5d742e2f85b9e3da1ac4a824f5effc464d21dcf3da735374bd3c` |
| `actor_autonomousInformant_hurt_e_01@1x.png` | x 24–62, y 12–60 | 39×49 | `f110906fd2cee83c2dab081e090c26be0ac1e4ed9a8b20e03a7aeed7e143e66b` |
| `actor_autonomousInformant_hurt_w_01@1x.png` | x 1–39, y 12–60 | 39×49 | `a38b28bf48bd5b8696a1dd1c6b8900be4815040efae19730334a3b99a8d366d8` |

Clip `autonomousInformant_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_defeat_n_01@1x.png` | x 9–51, y 17–60 | 43×44 | `9e0e7b2dc5268ad4654e4b4c0dc89be9bd7a8d3c797aee01d0b777dd1635f36a` |
| `actor_autonomousInformant_defeat_e_01@1x.png` | x 5–62, y 25–56 | 58×32 | `be70d8369fc41cbbd0517ee1ffdcfbcb3cd090445fb38147d5a6b04c213d0040` |
| `actor_autonomousInformant_defeat_w_01@1x.png` | x 1–58, y 25–56 | 58×32 | `f0233e5de8a1068cb3cdbef4f1cd515865ea0a4d2ad1cd9b1209b8fc818309a8` |

## Victorian Vendor

Clip `victorianVendor_move`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_move_n_01@1x.png` | x 4–58, y 20–61 | 55×42 | `eea1634f6dfbbfbf3c2a482b5c72016705ad5be3d438cbf247dafeae3c8652df` |
| `actor_victorianVendor_move_e_01@1x.png` | x 10–62, y 9–63 | 53×55 | `4f370b6e3168ed2bb28feb2d85bf4857ab45a658d03368054cae18bf98828987` |
| `actor_victorianVendor_move_w_01@1x.png` | x 1–53, y 9–63 | 53×55 | `28eb8efcf4bd11be7619b833a343fb7bd402dcf4ece22441573536c069b592f8` |

Clip `victorianVendor_anticipate`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_throw_n_01@1x.png` | x 6–63, y 8–55 | 58×48 | `de036eab2c67770844995bfda4e28981f4e99996bb3b6a4deac6cc06bc247300` |
| `actor_victorianVendor_throw_e_01@1x.png` | x 15–45, y 3–46 | 31×44 | `e3cae282753bc1b51376e65366b1ffc423b4127fb0bd841a23d4368cebff4a99` |
| `actor_victorianVendor_throw_w_01@1x.png` | x 17–47, y 3–46 | 31×44 | `33bba207b32d980faecd6f0ec17489a207aab65fa7f43038dd1da4cba9df4cce` |

Clip `victorianVendor_commit`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_throwCommit_n_01@1x.png` | x 27–56, y 15–55 | 30×41 | `ef3f172270f3a1a7aaed13160faec85e953e53011eac0985b9031fa8c217bafd` |
| `actor_victorianVendor_throwCommit_e_01@1x.png` | x 12–54, y 0–52 | 43×53 | `53b3fea998589b297a78db0f6aa4528fbe53cd2aaa66f75d73b29b9312733d9a` |
| `actor_victorianVendor_throwCommit_w_01@1x.png` | x 8–50, y 0–52 | 43×53 | `70d12c57476e427f83a1306848aa15196d0d709acb4c5ddf3dd839d8123e40fe` |

Clip `victorianVendor_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_hurt_n_01@1x.png` | x 6–56, y 8–59 | 51×52 | `002fa8c50bb7fbaffbe174abbd37214e0f015885df80e604147e7c5adfbf1a65` |
| `actor_victorianVendor_hurt_e_01@1x.png` | x 6–62, y 5–55 | 57×51 | `f7e44c123f4576b45df5bdd3c1144d35ef6862cd5ae39852f217bdfa66519a1b` |
| `actor_victorianVendor_hurt_w_01@1x.png` | x 1–57, y 5–55 | 57×51 | `e7e743a26cfae820ce8267228f11f2d4c4cd20d5516dbf27fb3b1b4b7726e214` |

Clip `victorianVendor_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_defeat_n_01@1x.png` | x 13–56, y 7–54 | 44×48 | `e8a250242a167b0754f31e907d86c8cad5b2250de7561156d66af4022f7c0590` |
| `actor_victorianVendor_defeat_e_01@1x.png` | x 5–61, y 6–55 | 57×50 | `554c7057ed28a77fd10eaa0834718b19c4987a660e2c2b7302796a4127fb69d9` |
| `actor_victorianVendor_defeat_w_01@1x.png` | x 2–58, y 6–55 | 57×50 | `d870f0eec5433f2dbf4fc4f0e5736cfea0196b36604d8b4a1b9917b8ae9fef6e` |
