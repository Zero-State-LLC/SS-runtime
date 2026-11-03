# Standard-enemy hurt and defeat in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `c603aeb`. No new frame was added. No sheet was made. Frame 01 in these directions stays in [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md). The south frames stay in [enemy-south-hurt-defeat-rest-2026-11-03.md](enemy-south-hurt-defeat-rest-2026-11-03.md). The anchor stays the one in the enemy note: (32, 56).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

The five standard enemies are `fogAnalyticsCloud`, `cableCarCorrelator`, `sutroSignalWitch`, `autonomousInformant`, and `victorianVendor`. Every frame below has canvas 64×64. The table is hurt frames 02–03 and defeat frames 02–06 in north, east, and west: 105 files. This does not close #131 or #132.

## Fog Analytics Cloud

Clip `fogAnalyticsCloud_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_hurt_n_02@1x.png` | x 7–63, y 11–53 | 57×43 | `37a2310d9046ec90def9d3ff343373ac24ad2c8a69c165a42ae6c5205855bb19` |
| `actor_fogAnalyticsCloud_hurt_e_02@1x.png` | x 11–58, y 10–57 | 48×48 | `50e0f649b19ede1e230bdd4f50e2377803a40855f0f278d75b7516c073b4b113` |
| `actor_fogAnalyticsCloud_hurt_w_02@1x.png` | x 5–52, y 10–57 | 48×48 | `f3c9eb44d94f6e5359e9afab2051c03f41158888aa7d7e9cb9d5f4336537d9e9` |
| `actor_fogAnalyticsCloud_hurt_n_03@1x.png` | x 0–58, y 11–56 | 59×46 | `35f956b6ae496097c725fecd17d4c609f44d357ec39c7c72b02ff371603fb1e3` |
| `actor_fogAnalyticsCloud_hurt_e_03@1x.png` | x 0–58, y 13–56 | 59×44 | `de01c6c03e672d17808a2ed78f6ba635bc1a4afd631cb269e06963c02a166b18` |
| `actor_fogAnalyticsCloud_hurt_w_03@1x.png` | x 5–63, y 13–56 | 59×44 | `217abaca49dda089ee93bdeb21e027da68126cadd9dc1634c37194067a45f626` |

Clip `fogAnalyticsCloud_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_fogAnalyticsCloud_defeat_n_02@1x.png` | x 0–63, y 15–56 | 64×42 | `c3ac85bc7b3d98b409eeb2680761afc2bccdd16a9148f4cafdf0ea397faceb1d` |
| `actor_fogAnalyticsCloud_defeat_e_02@1x.png` | x 6–60, y 19–47 | 55×29 | `312dc3b423152985c59cbe5ee51bb39ce29f3ffcfb837442fb08e52195def7fb` |
| `actor_fogAnalyticsCloud_defeat_w_02@1x.png` | x 3–57, y 19–47 | 55×29 | `247fc0180c95b3e665efeae8304590c6c776a010d7e908d3624f5aacf7d21379` |
| `actor_fogAnalyticsCloud_defeat_n_03@1x.png` | x 0–62, y 18–55 | 63×38 | `a0c03cb111b630a26caab61bb95a9d68fb5727721f9ca16a8f444b6d14a2d975` |
| `actor_fogAnalyticsCloud_defeat_e_03@1x.png` | x 4–61, y 20–56 | 58×37 | `8e9218654918e21cf2eea3fb1243f82a61ccf926ee6e4f37d7d3b18b9d4edcb1` |
| `actor_fogAnalyticsCloud_defeat_w_03@1x.png` | x 2–59, y 20–56 | 58×37 | `f70e8080503e7ce76623821fe19b33ce3bb9c2a5a732289036c074c58ed2e069` |
| `actor_fogAnalyticsCloud_defeat_n_04@1x.png` | x 4–60, y 16–46 | 57×31 | `770eb6e8dd584d2cbff280593050cdc1c1acdcd56d3c33557a03561d54896f5e` |
| `actor_fogAnalyticsCloud_defeat_e_04@1x.png` | x 3–62, y 21–55 | 60×35 | `42529745e1c501c8230beb3986b25cd28ad7f36bfee15668f912fedb9268f206` |
| `actor_fogAnalyticsCloud_defeat_w_04@1x.png` | x 1–60, y 21–55 | 60×35 | `8661feac21fdd29a0e8fed94915625bb16a3daa016f1632a3476c44f11c3115a` |
| `actor_fogAnalyticsCloud_defeat_n_05@1x.png` | x 14–61, y 23–45 | 48×23 | `f3d2bcc797fff394e5fd1b606fe600b4c49b564bf65318a853659a8409517172` |
| `actor_fogAnalyticsCloud_defeat_e_05@1x.png` | x 5–56, y 21–58 | 52×38 | `d319a3590bacb8dd616a212cff6e3c178113dfa8ffdee8dd576bbef44f9b0ba1` |
| `actor_fogAnalyticsCloud_defeat_w_05@1x.png` | x 7–58, y 21–58 | 52×38 | `00eaced590229721bc0694d63cb3738b4ad8f80cbe7a08e34fd9923b14f3b7df` |
| `actor_fogAnalyticsCloud_defeat_n_06@1x.png` | x 3–49, y 16–55 | 47×40 | `3b8606cf5da4d3fe80a68a5a429bd43fad14e76344027084cee53a12fac7eb60` |
| `actor_fogAnalyticsCloud_defeat_e_06@1x.png` | x 3–56, y 22–46 | 54×25 | `baf7be6afe31248ed8461e8cd2b9003715b13e7a3d9d8dd4954ff80d908361e1` |
| `actor_fogAnalyticsCloud_defeat_w_06@1x.png` | x 7–60, y 22–46 | 54×25 | `2739bd4934eb0c61ce1a2e14704854c831dfc0e410fccecc2deba9a59194a9e3` |

## Cable Car Correlator

Clip `cableCarCorrelator_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_hurt_n_02@1x.png` | x 3–52, y 7–56 | 50×50 | `1cf70dfe9aef3d5a972f818c95b0e2040815c3cbc64003ca8013b3ffca095315` |
| `actor_cableCarCorrelator_hurt_e_02@1x.png` | x 6–58, y 16–63 | 53×48 | `eed17b93da206041a9c5e99277dc4133c5e2fc79f3555a29c32172bbe6141119` |
| `actor_cableCarCorrelator_hurt_w_02@1x.png` | x 5–57, y 16–63 | 53×48 | `e340944e4f6b027b767da9486fe827f5107b95fbc0a70b8cfc7e3b5c57569215` |
| `actor_cableCarCorrelator_hurt_n_03@1x.png` | x 10–48, y 10–56 | 39×47 | `f35a048810cfaae74f277ceed8e8c84dab734084b8c618b22e268b28d7e3e4da` |
| `actor_cableCarCorrelator_hurt_e_03@1x.png` | x 3–58, y 21–63 | 56×43 | `1f654921368ef562a45c9da951d39bab7b20b009d91442c21ed363e3f374211e` |
| `actor_cableCarCorrelator_hurt_w_03@1x.png` | x 5–60, y 21–63 | 56×43 | `4d83df932e2c1a9917aee6571f420e978b7ba65cb586d10ba2a228fb1143a8ef` |

Clip `cableCarCorrelator_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_cableCarCorrelator_defeat_n_02@1x.png` | x 13–58, y 19–58 | 46×40 | `17acd359ae49e809d17a21649a588b492748a13220849572466c6e9c27499afd` |
| `actor_cableCarCorrelator_defeat_e_02@1x.png` | x 0–63, y 25–63 | 64×39 | `b0a36903eae33b6ba02b4434ad2ebec2a3057473574cb61cbb241a89a0c16603` |
| `actor_cableCarCorrelator_defeat_w_02@1x.png` | x 0–63, y 25–63 | 64×39 | `8f6a21291c7e188763d843ba74be23058158016e853360273953c67abf58ec3a` |
| `actor_cableCarCorrelator_defeat_n_03@1x.png` | x 10–62, y 23–62 | 53×40 | `5cd943642ec9bde13ca16d6c05478278068ab8d9ad9ad587c8a772d8e7f38d5e` |
| `actor_cableCarCorrelator_defeat_e_03@1x.png` | x 5–62, y 38–55 | 58×18 | `48a74c954ebc280674f77030a6144bf8314536732bba098339a6279964f2695f` |
| `actor_cableCarCorrelator_defeat_w_03@1x.png` | x 1–58, y 38–55 | 58×18 | `e7cbc448b82f84bc9643cbbcd0c92bda36a36a4eabfe9e40a2f30fcc45002bad` |
| `actor_cableCarCorrelator_defeat_n_04@1x.png` | x 3–60, y 27–62 | 58×36 | `6eebaca6a54ee1129e094645c98eff616abb9df4486f31ed579a2b3dbacce01a` |
| `actor_cableCarCorrelator_defeat_e_04@1x.png` | x 4–63, y 40–62 | 60×23 | `213c82802b6fdcdb97ae85f04e6225fdbf1a870ec029d94d4d793b62bb80de9c` |
| `actor_cableCarCorrelator_defeat_w_04@1x.png` | x 0–59, y 40–62 | 60×23 | `e0714568cda91768fc843113073a37a796052af4b56b109ec4348dea94732e69` |
| `actor_cableCarCorrelator_defeat_n_05@1x.png` | x 5–59, y 22–63 | 55×42 | `4b84d91c9e93608570706edecfb189805de499032e5f5a1c6394c00eaa695e0c` |
| `actor_cableCarCorrelator_defeat_e_05@1x.png` | x 5–62, y 44–56 | 58×13 | `f28de3b1a7dfe1f0c3d26f8a2c86c56fc41d3f1b8acb8eda97e98d3f5bc6336c` |
| `actor_cableCarCorrelator_defeat_w_05@1x.png` | x 1–58, y 44–56 | 58×13 | `08a468ebd25f3ee0bd8b613837f397b5b8c8b082d22f0f4238133e073e382c63` |
| `actor_cableCarCorrelator_defeat_n_06@1x.png` | x 12–59, y 33–55 | 48×23 | `20786f58aeac8cbc4eb91f15159e98a4b4766e6c7cb98151c14f9f6745fb869a` |
| `actor_cableCarCorrelator_defeat_e_06@1x.png` | x 4–58, y 45–55 | 55×11 | `e65ba2207584181af2d8f595a0a5f37d3bdf342c1de17b50e57f96634e50c769` |
| `actor_cableCarCorrelator_defeat_w_06@1x.png` | x 5–59, y 45–55 | 55×11 | `08a482b0b5ae1d653ce4ef938d69855253d94e9ac2484d911590afc726ca86dc` |

## Sutro Signal Witch

Clip `sutroSignalWitch_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_hurt_n_02@1x.png` | x 16–57, y 7–56 | 42×50 | `cfc5a48ce3acf009fb348cd967f1bbe65ab34ba73e84a18d2eefa18d8cd37b78` |
| `actor_sutroSignalWitch_hurt_e_02@1x.png` | x 0–57, y 3–55 | 58×53 | `146bf9c03c5a561bc0fb8bcc15e4e4fb606f548177223ea122fcdb20e3d0e5a0` |
| `actor_sutroSignalWitch_hurt_w_02@1x.png` | x 6–63, y 3–55 | 58×53 | `ba3a3a38944c87a7ad8953201149f172b37e19b87bf58acb1f82eecbdaec06d7` |
| `actor_sutroSignalWitch_hurt_n_03@1x.png` | x 6–50, y 5–56 | 45×52 | `1c2a19091bfa6b1f7f9d3a296f87fb512724acac3328222b7d91f4014d54d6b2` |
| `actor_sutroSignalWitch_hurt_e_03@1x.png` | x 16–58, y 3–55 | 43×53 | `0f3fb9fd756368281f4d90a9b47068b69636960e33ed81f38797e29cdc9f60e1` |
| `actor_sutroSignalWitch_hurt_w_03@1x.png` | x 5–47, y 3–55 | 43×53 | `444f03993c7b977e0338150c1f7b3b1635a9dfa9a1fb1f7b8f4e09ff589c1aaa` |

Clip `sutroSignalWitch_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_sutroSignalWitch_defeat_n_02@1x.png` | x 4–49, y 4–54 | 46×51 | `b5d70320af18f6e4717a386e94a76133a78ae2a6d47ad0cb669893205bf54220` |
| `actor_sutroSignalWitch_defeat_e_02@1x.png` | x 10–58, y 25–61 | 49×37 | `dc64bcf65d84b204e8272731a28bb7661f35b2bce65b13a14de761de5bf4963c` |
| `actor_sutroSignalWitch_defeat_w_02@1x.png` | x 5–53, y 25–61 | 49×37 | `205c7aeacb2153348d5d979f284bfb91ee550c99561379cb71ada0a151009626` |
| `actor_sutroSignalWitch_defeat_n_03@1x.png` | x 3–51, y 5–54 | 49×50 | `30dc160740dffd103e255f159a33a1411be225702d0eb387145b6c0af1b623d8` |
| `actor_sutroSignalWitch_defeat_e_03@1x.png` | x 9–62, y 18–63 | 54×46 | `a11dc6341c46e64963aefe913883174c078b1d89bfc0679d75e0ed66ed98d55f` |
| `actor_sutroSignalWitch_defeat_w_03@1x.png` | x 1–54, y 18–63 | 54×46 | `79080842be8ad94aed9e9ca4b8aabd5622905c64723a105db26de129c3643b03` |
| `actor_sutroSignalWitch_defeat_n_04@1x.png` | x 1–63, y 21–54 | 63×34 | `c0cc4c225a2881957c690f4df73b4e0c67d9a175ae48b612634a3d98818693fd` |
| `actor_sutroSignalWitch_defeat_e_04@1x.png` | x 7–63, y 22–56 | 57×35 | `268abb954cf0519e3271e04e28066530308a2c19e39637cc28c1cc6e05badabc` |
| `actor_sutroSignalWitch_defeat_w_04@1x.png` | x 0–56, y 22–56 | 57×35 | `039eaa214120eedb23cbd0478b7e2bc503f6114c7bf4e4d7494f5df6ad803fb9` |
| `actor_sutroSignalWitch_defeat_n_05@1x.png` | x 0–63, y 28–55 | 64×28 | `d796644cf9b57abbaa8bc5cd1615d3378f72a469ef18870c19787ced02764422` |
| `actor_sutroSignalWitch_defeat_e_05@1x.png` | x 6–62, y 45–56 | 57×12 | `5c57fad9d6d4bb3aaa36496313c201563f7c7c7dd335e119edc7e53d4ac6081c` |
| `actor_sutroSignalWitch_defeat_w_05@1x.png` | x 1–57, y 45–56 | 57×12 | `38f09d4ad20e630b6fe8a50d4ee6c31784f425de90ed3e63f9fbacf0e8193f59` |
| `actor_sutroSignalWitch_defeat_n_06@1x.png` | x 0–58, y 38–56 | 59×19 | `0ff35af352bf4ac7d006150ae84c0f8c39b052d9d1ed47c454fb3dc80ed86807` |
| `actor_sutroSignalWitch_defeat_e_06@1x.png` | x 5–60, y 48–56 | 56×9 | `aa89f87927b77e618aa91dbe18cabcdad2dacd448d2370fafb954b517ae1737f` |
| `actor_sutroSignalWitch_defeat_w_06@1x.png` | x 3–58, y 48–56 | 56×9 | `a95041f545afb3ea2c2bd005b13d67aa09a766333690921b8f44253a7ad2147a` |

## Autonomous Informant

Clip `autonomousInformant_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_hurt_n_02@1x.png` | x 10–51, y 9–59 | 42×51 | `99509bcf8238502512a394cd2e7c7658e16251cec61a6e920e6d914582bf5278` |
| `actor_autonomousInformant_hurt_e_02@1x.png` | x 6–58, y 12–63 | 53×52 | `762a08ae2ea2be724bbb1a0f1230c653107d5f7b7ddf191b935a5b3d02a243f6` |
| `actor_autonomousInformant_hurt_w_02@1x.png` | x 5–57, y 12–63 | 53×52 | `5a333322b99763820d1babf2b5d97883107c78f682a334998196fdf697124ba4` |
| `actor_autonomousInformant_hurt_n_03@1x.png` | x 6–49, y 7–55 | 44×49 | `11aff0db345331e330faa2693195c2f55d5432742bb57964738a9114cbdc37c6` |
| `actor_autonomousInformant_hurt_e_03@1x.png` | x 7–51, y 18–55 | 45×38 | `e5f89e7054593bc692557adf4622c036abb68edffddb5eab5806edaa9d678ad5` |
| `actor_autonomousInformant_hurt_w_03@1x.png` | x 12–56, y 18–55 | 45×38 | `43e978d1e2e2ea44284993c4c28a2cbedf9ef09b4949fb628b22eb5def41d884` |

Clip `autonomousInformant_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_defeat_n_02@1x.png` | x 0–52, y 15–56 | 53×42 | `28d668bb7a1d67d07e2eef5db9aa9272829c29cee27854cc2973292f23ccca78` |
| `actor_autonomousInformant_defeat_e_02@1x.png` | x 10–63, y 28–56 | 54×29 | `544ff2e5d827bf2074034f0cbb7134a4b719565d686f3dcf6ec0494315fa3b4a` |
| `actor_autonomousInformant_defeat_w_02@1x.png` | x 0–53, y 28–56 | 54×29 | `471de7d4a12e1e44cd15666d6b096fa1544f33bc797e865fea7b78d421525137` |
| `actor_autonomousInformant_defeat_n_03@1x.png` | x 1–53, y 17–59 | 53×43 | `f7d89179738e7f4ddf6bee107f5d1762343ad768762707c486688a51f42a46f9` |
| `actor_autonomousInformant_defeat_e_03@1x.png` | x 3–58, y 36–56 | 56×21 | `d4c91c012311d88c319657aed18f2c117e0d77ae49e63b91da063537e75def09` |
| `actor_autonomousInformant_defeat_w_03@1x.png` | x 5–60, y 36–56 | 56×21 | `9c4f0742346cbf76c12571fd93271f416d4bc51fa15061781e6106bfa8818083` |
| `actor_autonomousInformant_defeat_n_04@1x.png` | x 7–52, y 16–55 | 46×40 | `e07b06f17b054053be07bcbe60c2d75d8de3a4d47f801c5e18b09aa523ce99f2` |
| `actor_autonomousInformant_defeat_e_04@1x.png` | x 4–63, y 40–56 | 60×17 | `87777304f4d65f38f22524a21d0d1a3594eb4f0918d0cbe85f659788a0629d32` |
| `actor_autonomousInformant_defeat_w_04@1x.png` | x 0–59, y 40–56 | 60×17 | `96f2ec3b42fcf47dda4c31adf6f2f3e0106f63225a6937fa7b698558de3c0249` |
| `actor_autonomousInformant_defeat_n_05@1x.png` | x 0–63, y 21–62 | 64×42 | `6d5554696ff8e1c623b98fd4026d579f92ecb0fdbe412707875313af93e7aca6` |
| `actor_autonomousInformant_defeat_e_05@1x.png` | x 0–63, y 36–56 | 64×21 | `368cf6c3cebd831072d5b6ef44369281a7f1dbb0c583859bafa558bd1a3990f9` |
| `actor_autonomousInformant_defeat_w_05@1x.png` | x 0–63, y 36–56 | 64×21 | `610d9a8cb2b04423d82348e01247d0f2c31a0fbceae232300cd2ccfcfe446a65` |
| `actor_autonomousInformant_defeat_n_06@1x.png` | x 0–63, y 34–56 | 64×23 | `3f31da4b32bf0436596f64bb1873ec7200961ecb07ac71c643c25d54a21cfd39` |
| `actor_autonomousInformant_defeat_e_06@1x.png` | x 0–57, y 39–56 | 58×18 | `1f916b7515ad58fcc6a9fc89652b2f526bedae11665d23bb718abe9de6336f36` |
| `actor_autonomousInformant_defeat_w_06@1x.png` | x 6–63, y 39–56 | 58×18 | `fc44ac0f145436ac97eeac81f8b86605a8989ddb55877253cd3cc46e6e53b19c` |

## Victorian Vendor

Clip `victorianVendor_hurt`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_hurt_n_02@1x.png` | x 17–49, y 8–55 | 33×48 | `a80bf9c4304a78c46ecc4771a4ba7f22bfbe9c32c96bc4d49da35b193533a5b1` |
| `actor_victorianVendor_hurt_e_02@1x.png` | x 0–52, y 10–55 | 53×46 | `43ee43890d972b1249f8d0ea2228f0163f2c11f086fb4a8a81df7d5079dff52f` |
| `actor_victorianVendor_hurt_w_02@1x.png` | x 11–63, y 10–55 | 53×46 | `07ad3a1199473fd6405b9893f56c0b0074832541700686dbfcb973a221b18f09` |
| `actor_victorianVendor_hurt_n_03@1x.png` | x 17–55, y 10–55 | 39×46 | `adb55c4ba18374985bb23c7a566a577455ebaed7f7d794544e0795a25d94fde8` |
| `actor_victorianVendor_hurt_e_03@1x.png` | x 0–61, y 6–55 | 62×50 | `3e276688c77a8415f3d9aa57932ba854df82ef28c27dde5ecf88651c4b0941c0` |
| `actor_victorianVendor_hurt_w_03@1x.png` | x 2–63, y 6–55 | 62×50 | `1ec6a7c9d0f2b54b29dd475eba611c5e4bbfa7e37285fa79c2c723f85291535c` |

Clip `victorianVendor_defeat`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_defeat_n_02@1x.png` | x 13–57, y 13–61 | 45×49 | `6add602f1787dbd868964bf31f8b8a55c8d35fda7efdfde8e599f3f8a7f0a45f` |
| `actor_victorianVendor_defeat_e_02@1x.png` | x 3–63, y 18–58 | 61×41 | `a2c0b37c3beacbc5a031071fa91da2f880e1e7e52a0a8c225463104ec86f6a22` |
| `actor_victorianVendor_defeat_w_02@1x.png` | x 0–60, y 18–58 | 61×41 | `ea7d8ca867158e8a3e58fb473cd3b17ca4b6b0d2200bb4c7e6feef50d6e12980` |
| `actor_victorianVendor_defeat_n_03@1x.png` | x 5–59, y 14–54 | 55×41 | `ea07b6bd9000b7ae934d5f75101311be7f688ba5176c7bc9d2611c36fa245d41` |
| `actor_victorianVendor_defeat_e_03@1x.png` | x 6–62, y 27–60 | 57×34 | `3d8da82cf94858247da22baec8c667541dae97b1f573fca8a6a8963c9bd7efc8` |
| `actor_victorianVendor_defeat_w_03@1x.png` | x 1–57, y 27–60 | 57×34 | `d6e2b15cb461e85221ec522f55befb7a7c9307c875144c33896b90da1e52b07a` |
| `actor_victorianVendor_defeat_n_04@1x.png` | x 1–63, y 18–63 | 63×46 | `3303e9b920dcceb158e958f7b1da168938327993d19ef97276cc259b90416fed` |
| `actor_victorianVendor_defeat_e_04@1x.png` | x 4–63, y 23–62 | 60×40 | `1523fd8a7106312d9581da88b7215aaf81688302264fa7f131bb02f56644be25` |
| `actor_victorianVendor_defeat_w_04@1x.png` | x 0–59, y 23–62 | 60×40 | `3a6eb469a8f8d76055c5e753f32c06a5382e2b04fe4067dda3dc19d3b8b0353c` |
| `actor_victorianVendor_defeat_n_05@1x.png` | x 2–63, y 28–54 | 62×27 | `8c9fd89612cda3fa9f674d1aa1cd71a687614cfffda68c40cc8f1086b8decde3` |
| `actor_victorianVendor_defeat_e_05@1x.png` | x 3–63, y 25–55 | 61×31 | `a4c593f366c3c43ffebce1e4f048b46bae761865a7a16f7a2fba989e44b11d22` |
| `actor_victorianVendor_defeat_w_05@1x.png` | x 0–60, y 25–55 | 61×31 | `52f51b1506e3c729494ff3c8ee72c269552dcebd06a1e1beb851b4803f8074e4` |
| `actor_victorianVendor_defeat_n_06@1x.png` | x 0–60, y 28–59 | 61×32 | `27c72ef4730fa781c7055f0b3c7e86c52e7a67327ac5e8697fb9cbcfb11c3370` |
| `actor_victorianVendor_defeat_e_06@1x.png` | x 0–58, y 40–55 | 59×16 | `10eba70cdb8944293f6340a1c6bac875f49a7642f17f6b8b537b852bbb5058c7` |
| `actor_victorianVendor_defeat_w_06@1x.png` | x 5–63, y 40–55 | 59×16 | `ebcefee5372190972862f89c4749db2c43a090c895ff40202b0392c2c9dae21e` |
