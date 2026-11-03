# Catalog digests and shipped PNG bytes

Measured 2026-11-03 from the runtime asset bytes on `279dc63`. No file was replaced.

The asset catalog has 1030 records whose `runtimePath` is a PNG. Each names one file in `RuntimeAssets`, and every PNG in that directory is named once. Catalog width and height match the PNG header on all 1030.

918 records are `originalAccepted`. On each of them, the catalog `sha256` is the file bytes.

112 records are `adaptedAdmitted`. On each of them, the catalog `sha256` is not the file bytes. Every one of those notes says the digest is the one at the frozen commit. The files are the resampled player hurt, defeat, extraction, idle, and move frames, and the resampled camera frames. There are 62 distinct file digests and 62 distinct catalog digests. A catalog digest is shared by more than one file exactly when those files share a file digest. That is the copied player directions, plus the two camera pairs already named in the camera bounds note: hit frame 02 with criticalEnter frame 01, and destroyedIdle frame 02 with fieldOff frame 01.

| File | Catalog sha256 | File sha256 |
|---|---|---|
| `actor_camera_criticalEnter_none_01@1x.png` | `edb8ba06ca9be58b95a4c32c5db9b6da5706ddb4929897674cc6e93e7c606e18` | `fdcd36cdcbd3a63f7ed809e978e5279dcb5873e45739e9b5c2c9eea98cc958d9` |
| `actor_camera_criticalEnter_none_02@1x.png` | `d55dce8a76c56ffeb089245de490e76d2381cc4a8c9fb8542f689f04f1f5130f` | `2578299b517e62aa9f1734aa915f156c133ef577939a54d0bbfcac6dec405308` |
| `actor_camera_criticalEnter_none_03@1x.png` | `57dc2d1efee7ce9aaa4dc988e4f58765d330cf1c53859750a0b1efa654249aff` | `d77261682a4da0061f1a0b66bfe5610bf9e20121faa869627533753a49da0875` |
| `actor_camera_destroy_none_01@1x.png` | `11d69415c28c0bcc372dbe265e2f813adaa2836d382fdb29d70a037da93ac739` | `df332805bfc2492049d634ef6d008ae80686a258cd45ef86951aaacd18d47e52` |
| `actor_camera_destroy_none_02@1x.png` | `06b3bf10d60279866e3ba58943d3751b544f1daa73a84876b73b5a3172ed3791` | `1360b22b542a32abc9424c37e6ced0c8b236bc7c65cd27d51be15f045d8faa3f` |
| `actor_camera_destroy_none_03@1x.png` | `588f083a89b853e0456d160b0614f1004abd002ab680f121130bf1f1ec7f91c5` | `4f7832c2e4e154ab8e8c18d21bc71a90d58ba0dc1ede98e0c32031753c4ef4ac` |
| `actor_camera_destroy_none_04@1x.png` | `7d9eb285b8bea11a992fbfd5189cce51e9a502b919ba52a379ff5018df63cefa` | `f23aa4adcfc7acb0d3207bf37df53e050daf6a3eaf76a7ee1be2aa6e8c48fc52` |
| `actor_camera_destroyedIdle_none_01@1x.png` | `e4c587dc81fcf26bd0ccf93a2363039c2dadd4544590be803f765d8da5ca4cc0` | `9822d27f6699726461c6447505e34bedaed60cf53b9a4420a7ff7671c500f680` |
| `actor_camera_destroyedIdle_none_02@1x.png` | `f05abb64f479d5599156aae4dbbc1eeb28c8f4e8643cae2b8bd2744c005eb3c1` | `9d79cb23a274c309834eb2733e6b56a4a402316e248f79998ad19fdec3007c00` |
| `actor_camera_fieldOff_none_01@1x.png` | `f05abb64f479d5599156aae4dbbc1eeb28c8f4e8643cae2b8bd2744c005eb3c1` | `9d79cb23a274c309834eb2733e6b56a4a402316e248f79998ad19fdec3007c00` |
| `actor_camera_hit_none_01@1x.png` | `9526f447106cfcda00684b5265fa7d14bb869230e1e9ad097713acc06cb0e556` | `13dfd8a833bd12123ff257595af36fcd70071bf6a0dcec5774ebcd8bb6ba8d86` |
| `actor_camera_hit_none_02@1x.png` | `edb8ba06ca9be58b95a4c32c5db9b6da5706ddb4929897674cc6e93e7c606e18` | `fdcd36cdcbd3a63f7ed809e978e5279dcb5873e45739e9b5c2c9eea98cc958d9` |
| `actor_camera_operationalIdle_none_01@1x.png` | `04fb5f757d173ff256b84bb5648a4105cd10470673165dc2b3761ab161303981` | `1f0d6ef053e915666a6c3613e28255cc509b51ac18d7336dd127eb6b458c415d` |
| `actor_camera_operationalIdle_none_02@1x.png` | `890b8488079eb07755113e6921ee7765f5a0b7aa219b2b129d2da40e444349d6` | `5d9b16e6384df500fee96982797e156ff15345cdf645ee4b338151dc7e79ceec` |
| `actor_camera_operationalIdle_none_03@1x.png` | `eb7822d8b0e24bfc9be176e2d9bfa62faf2bf9a341fb949861b3e140bc0853a5` | `1866a81a7e5973a81737839a84a3fcfdbb714fc2366922835c0869045de37663` |
| `actor_camera_operationalIdle_none_04@1x.png` | `d05ae788a8149171c73399b6a62aa879c3108e64af1c1cbda735d2040afb7ad8` | `c81ae71c64a0c6eeebbd65981b33d0df4a79fb1c7cbedb2cd230caf440a05a93` |
| `actor_player_defeat_e_01@1x.png` | `3cc4bd6a0967ea7dc818051e6633a0959055b74147111d8d7be3333368cbd390` | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_e_02@1x.png` | `56ad49e029bbd20af9c3d2a63129ae39a9bc1e19c1de3a31ae4d88e172cff0d4` | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_e_03@1x.png` | `0b1d5694986127c10104f6e153acc381f823bdd15ca14ab987c97b0b3329d9f3` | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_e_04@1x.png` | `6df713ab1fdb63b56e6da166f400db26f8de8cc437830fe49b14988f348a5967` | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_e_05@1x.png` | `49f1b95a1e66b83fbc4aa0f2ce4c16371db4fca3cc300c6096679d75184986c9` | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_defeat_n_01@1x.png` | `3cc4bd6a0967ea7dc818051e6633a0959055b74147111d8d7be3333368cbd390` | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_n_02@1x.png` | `56ad49e029bbd20af9c3d2a63129ae39a9bc1e19c1de3a31ae4d88e172cff0d4` | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_n_03@1x.png` | `0b1d5694986127c10104f6e153acc381f823bdd15ca14ab987c97b0b3329d9f3` | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_n_04@1x.png` | `6df713ab1fdb63b56e6da166f400db26f8de8cc437830fe49b14988f348a5967` | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_n_05@1x.png` | `49f1b95a1e66b83fbc4aa0f2ce4c16371db4fca3cc300c6096679d75184986c9` | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_defeat_s_01@1x.png` | `3cc4bd6a0967ea7dc818051e6633a0959055b74147111d8d7be3333368cbd390` | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_s_02@1x.png` | `56ad49e029bbd20af9c3d2a63129ae39a9bc1e19c1de3a31ae4d88e172cff0d4` | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_s_03@1x.png` | `0b1d5694986127c10104f6e153acc381f823bdd15ca14ab987c97b0b3329d9f3` | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_s_04@1x.png` | `6df713ab1fdb63b56e6da166f400db26f8de8cc437830fe49b14988f348a5967` | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_s_05@1x.png` | `49f1b95a1e66b83fbc4aa0f2ce4c16371db4fca3cc300c6096679d75184986c9` | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_defeat_w_01@1x.png` | `3cc4bd6a0967ea7dc818051e6633a0959055b74147111d8d7be3333368cbd390` | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_w_02@1x.png` | `56ad49e029bbd20af9c3d2a63129ae39a9bc1e19c1de3a31ae4d88e172cff0d4` | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_w_03@1x.png` | `0b1d5694986127c10104f6e153acc381f823bdd15ca14ab987c97b0b3329d9f3` | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_w_04@1x.png` | `6df713ab1fdb63b56e6da166f400db26f8de8cc437830fe49b14988f348a5967` | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_w_05@1x.png` | `49f1b95a1e66b83fbc4aa0f2ce4c16371db4fca3cc300c6096679d75184986c9` | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_extraction_e_01@1x.png` | `06999375a208f4b085f2753494a3b80341b018ace8cae077c8767e6a6ba0a72b` | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_e_02@1x.png` | `70d852bf8d2a646d81d2c1068b2713d8e4b375ac159e79136bd90b145ea4e269` | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_e_03@1x.png` | `ab5666d69aeca5427c944723e61a82ba9ac8b722307583d21ba13777ee6c5b36` | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_e_04@1x.png` | `d2e8a39c76dc1653f37847406c30731230bef53601518413ae7590162e0d7f26` | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_e_05@1x.png` | `1b1f61346a89924f5b041e9650a91235f270aef09de9168a023ebf272e7b3205` | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_e_06@1x.png` | `b8fe92739d9aeffd0cec4acd88f68781c3c8c0729b9c3e8b94afb40042b2aba1` | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_e_07@1x.png` | `dad29857df474ed33f5f2f37b60f184d56b2ed05cdd1495079843faa8a26b4f3` | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_e_08@1x.png` | `442855223fd86bba00d46f6eeb6c7a99b044d76b79d4e594f9b88a16ccee6436` | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_extraction_n_01@1x.png` | `06999375a208f4b085f2753494a3b80341b018ace8cae077c8767e6a6ba0a72b` | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_n_02@1x.png` | `70d852bf8d2a646d81d2c1068b2713d8e4b375ac159e79136bd90b145ea4e269` | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_n_03@1x.png` | `ab5666d69aeca5427c944723e61a82ba9ac8b722307583d21ba13777ee6c5b36` | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_n_04@1x.png` | `d2e8a39c76dc1653f37847406c30731230bef53601518413ae7590162e0d7f26` | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_n_05@1x.png` | `1b1f61346a89924f5b041e9650a91235f270aef09de9168a023ebf272e7b3205` | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_n_06@1x.png` | `b8fe92739d9aeffd0cec4acd88f68781c3c8c0729b9c3e8b94afb40042b2aba1` | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_n_07@1x.png` | `dad29857df474ed33f5f2f37b60f184d56b2ed05cdd1495079843faa8a26b4f3` | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_n_08@1x.png` | `442855223fd86bba00d46f6eeb6c7a99b044d76b79d4e594f9b88a16ccee6436` | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_extraction_s_01@1x.png` | `06999375a208f4b085f2753494a3b80341b018ace8cae077c8767e6a6ba0a72b` | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_s_02@1x.png` | `70d852bf8d2a646d81d2c1068b2713d8e4b375ac159e79136bd90b145ea4e269` | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_s_03@1x.png` | `ab5666d69aeca5427c944723e61a82ba9ac8b722307583d21ba13777ee6c5b36` | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_s_04@1x.png` | `d2e8a39c76dc1653f37847406c30731230bef53601518413ae7590162e0d7f26` | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_s_05@1x.png` | `1b1f61346a89924f5b041e9650a91235f270aef09de9168a023ebf272e7b3205` | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_s_06@1x.png` | `b8fe92739d9aeffd0cec4acd88f68781c3c8c0729b9c3e8b94afb40042b2aba1` | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_s_07@1x.png` | `dad29857df474ed33f5f2f37b60f184d56b2ed05cdd1495079843faa8a26b4f3` | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_s_08@1x.png` | `442855223fd86bba00d46f6eeb6c7a99b044d76b79d4e594f9b88a16ccee6436` | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_extraction_w_01@1x.png` | `06999375a208f4b085f2753494a3b80341b018ace8cae077c8767e6a6ba0a72b` | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_w_02@1x.png` | `70d852bf8d2a646d81d2c1068b2713d8e4b375ac159e79136bd90b145ea4e269` | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_w_03@1x.png` | `ab5666d69aeca5427c944723e61a82ba9ac8b722307583d21ba13777ee6c5b36` | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_w_04@1x.png` | `d2e8a39c76dc1653f37847406c30731230bef53601518413ae7590162e0d7f26` | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_w_05@1x.png` | `1b1f61346a89924f5b041e9650a91235f270aef09de9168a023ebf272e7b3205` | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_w_06@1x.png` | `b8fe92739d9aeffd0cec4acd88f68781c3c8c0729b9c3e8b94afb40042b2aba1` | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_w_07@1x.png` | `dad29857df474ed33f5f2f37b60f184d56b2ed05cdd1495079843faa8a26b4f3` | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_w_08@1x.png` | `442855223fd86bba00d46f6eeb6c7a99b044d76b79d4e594f9b88a16ccee6436` | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_hurt_e_01@1x.png` | `f28f6e3245a681d9bcc21740fdb4a6035139f59d1f5edb994c080c94361c6e1e` | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_e_02@1x.png` | `f6f489bea9af04a97b38d96ac93ed0fab1f955a2b23a64664fd9338e537ff73a` | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_e_03@1x.png` | `c335639f08bd7a9e1dcb5e5f14734fd633abddeeeb3186946f0f120d8952ff1b` | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_hurt_n_01@1x.png` | `f28f6e3245a681d9bcc21740fdb4a6035139f59d1f5edb994c080c94361c6e1e` | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_n_02@1x.png` | `f6f489bea9af04a97b38d96ac93ed0fab1f955a2b23a64664fd9338e537ff73a` | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_n_03@1x.png` | `c335639f08bd7a9e1dcb5e5f14734fd633abddeeeb3186946f0f120d8952ff1b` | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_hurt_s_01@1x.png` | `f28f6e3245a681d9bcc21740fdb4a6035139f59d1f5edb994c080c94361c6e1e` | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_s_02@1x.png` | `f6f489bea9af04a97b38d96ac93ed0fab1f955a2b23a64664fd9338e537ff73a` | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_s_03@1x.png` | `c335639f08bd7a9e1dcb5e5f14734fd633abddeeeb3186946f0f120d8952ff1b` | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_hurt_w_01@1x.png` | `f28f6e3245a681d9bcc21740fdb4a6035139f59d1f5edb994c080c94361c6e1e` | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_w_02@1x.png` | `f6f489bea9af04a97b38d96ac93ed0fab1f955a2b23a64664fd9338e537ff73a` | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_w_03@1x.png` | `c335639f08bd7a9e1dcb5e5f14734fd633abddeeeb3186946f0f120d8952ff1b` | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_idle_e_01@1x.png` | `ed971b8f43cff93891b4d4b88f81c9367cf9a13ed0c6fdbb3fa8b215011b0541` | `975f700e74ddd28f2e257bd2295c4d0d20da87c2d1faba953d1d4d76b84701cf` |
| `actor_player_idle_e_02@1x.png` | `0b847a6801d43114507b9193dd87e6b54287280ed1cd4728bd11bd30d0787334` | `b6b800fd691f83e84f0c4e34d394742746b4cb98756fcca36f9c2fe7824e040e` |
| `actor_player_idle_n_01@1x.png` | `3acf235879759156fb0a8241a2c4e2a43a1956280cf8b894f2a4b057e4c4655d` | `bb98b4a578f27e4f0a6397a18555b9dfaacf6d548aff69fd56b1f87a24e4af68` |
| `actor_player_idle_n_02@1x.png` | `f4f6cd82f6353bd5e96f8bac2991b571879994111f51907dcc0796f02a9c02c0` | `02e7f6c940fd251ca9f68e4739662b849605f404558894af3fc4602fef035405` |
| `actor_player_idle_s_01@1x.png` | `2a2027efac24614e8da808191319e71003d5eeeb54349948efa0fca1dac88f25` | `f45ca16776f7e4b4475ef8f7cbe7791abbb4b371f24902b600c5d8468a8dd6f4` |
| `actor_player_idle_s_02@1x.png` | `80939dcb502a9e6188ff7259b242674e26be75f0a170ea6ef07195dba7660c03` | `c33085f91166079e3e4fd4df74cb8cd092d7df72520ad14f5a134073db2a198d` |
| `actor_player_idle_w_01@1x.png` | `559a7d1da9175a3cf566a2d6543e6cbec4ef864059b2a119ffe0423a9a4da34d` | `fac6c5c0aa66ee89a8fffa4b66b4f2a48ade5dcf254bda6653a1b39c69058bf7` |
| `actor_player_idle_w_02@1x.png` | `b7a5d6e58328bcad0e5a6ab7c82a65748c625994f7c5a105f0d446fac78d2ad9` | `ad5131c0740aea4c50da6347da469c08cc9c5a88b67d442e876eba61616e1340` |
| `actor_player_move_e_01@1x.png` | `099e4e7566baa5de38561e6b89eedc3ef9058ca62cc4213cff91762043054578` | `1210a72673d5ec47714d87872060d24b50c3cf11c59642c2a1440afe704cb187` |
| `actor_player_move_e_02@1x.png` | `571af3eac638dd665790eb801391e5698abd21b6369de7c2eb3b6b17b2d82144` | `6ae447827bac42856968121534960fdee3a015a745afa9e64f50a7bc71f53ac0` |
| `actor_player_move_e_03@1x.png` | `4b8243807a576451cc21d3394c92867c08bb739173c5d770efa5de674e5348d6` | `8cac33c80e9dc632336c94bb8e3665e77ebcb077ad04dca4b7a584b9371c6579` |
| `actor_player_move_e_04@1x.png` | `e319426426a4477e16c87d2ac61ddb8e61d2d4232e6356c400103802f620d3a4` | `0ae84b0c1b3b073237a0e25cff7efe2dc8d90e7a43ff2d6f9ee4a4d8b0b548c7` |
| `actor_player_move_e_05@1x.png` | `1e8d62eb88e0ab012702cfd13fbd56e4556dd78b6725ca43a6d028ec1b168e88` | `a40853d90aeb8f7c6115665bb0e937547024a70b050b1d73249938c68a782b96` |
| `actor_player_move_e_06@1x.png` | `6c079503928d884dd5c5688583764a59dfb0d8de112f6899f039d61b61ee71ea` | `debcff3670732fae5c3d4de6ff83af84425dc4cf07c479c34f247713f0110649` |
| `actor_player_move_n_01@1x.png` | `85d47858f560aef235f0a51e659fe3eb8669233a718f3f5c9b2f44146e502340` | `d7596bcdaadad0ce988b8d4ef0711c1b7b60989f2af2ccf8b050cb67ba8b44be` |
| `actor_player_move_n_02@1x.png` | `810e18cf52aa53d89ce9512f7bab3d082a11df6d612dbcf56164807fe585f3f2` | `a509561d27cd95ff91166c4efaaf6172fcd218e89e6028fd47a84b808bdc1a0e` |
| `actor_player_move_n_03@1x.png` | `252446046286cc79b1eab45180ee910d698f82004c1ffc893b7dc15093a07fe4` | `0ef93179d3b849d03dacef7653ab8e2e7cd9f3c32cf32404301d9c02cbfa2f32` |
| `actor_player_move_n_04@1x.png` | `61e98e069b090f8fc29c68072e0417be127c0ce6c4f3513cf747e66a0ed572dd` | `b9b377d918c507e2304e0e5fbaff3123aeceb08a640f5354c09ce8d430d2799f` |
| `actor_player_move_n_05@1x.png` | `a419c9aa463853ab00ca7ce38a9113a7d05ac418341c5f7684a1866e9d9d88a8` | `eaad2e44b2141f37e4459685bf9d9580011619de2609662f2f958dee08b47989` |
| `actor_player_move_n_06@1x.png` | `3598c3c9baeeb13914376b7d8e23581e93bad4b35158cfa568dd8d389c1aa4ed` | `449a1c7e3fb6a7b35b14d5edfef2696447103f8cc6d7aa211bc3751f6e6ce411` |
| `actor_player_move_s_01@1x.png` | `d2f64f5248fe88d3b307451f7f6fae76a62961ecd45d4b13ee2f47c6d80ab262` | `7b3434af45c8bea2a987866f7041ae0299a65899f54e7c17d5012642f37d0108` |
| `actor_player_move_s_02@1x.png` | `0f4e2877dadd9e3c44a7ba837afee32e5284f26ecbf35a7447519b36dacbccaf` | `6257de74f3c8ab9fc5430ace985a3bf665b65aef5ba94901c8ce780791b03f30` |
| `actor_player_move_s_03@1x.png` | `7653dadf35b936b9d545ca37cd291cb6e225d45e26da5a31cd80217f0b21001a` | `8e511f29a5958398187407d6a737582c37b63e553312076600ae0129eabb7c91` |
| `actor_player_move_s_04@1x.png` | `d0f3635a48d1d2c44b36bac9a3a8bfaf174e3931c9ea89f88b9e8b1bd87816d0` | `0f11180150cb50ff04bb98a5cf56f2bd32eab4ea96cf21c6d463fc6ecd65fd1f` |
| `actor_player_move_s_05@1x.png` | `5dd4b5409731c616a52b2b91177c10fc7436657e18f465edad4b7194617dc7e2` | `afefdcd696e92623b6359e3f6347476a3282116ba8f803cdb06b28472444c45e` |
| `actor_player_move_s_06@1x.png` | `836c5a6d7c6a07e3b426a619787cd6ae3fd14be89c08c277a152f91decde0fa9` | `cda6a276f78ba1e330b95e3995ca5efc72df940e45475ad9c51b14de2978e67e` |
| `actor_player_move_w_01@1x.png` | `74fdccdca7dca4180b6c45201ed3a0b893bb78e04230d0bbd23eaef382ec91e9` | `cb50d35b35964d68843826eedb3dd2ce7b6f2ab256345b17a00abf89950131c9` |
| `actor_player_move_w_02@1x.png` | `7f13884e9bb52a75fc74281a03c1087470ae863bd43cd51b9ca1a022743d49a2` | `2a93d4dfda2bf7b41db652ce7dd582e03d6a01fc692f811c17faa70b85770b31` |
| `actor_player_move_w_03@1x.png` | `4bb77a96e1fc54922cbe98c5864aff8406efa5f5a929d23bcbed28f919b72d4c` | `e0c4d978ba0fa6feeb323c0536ec894fd44dea55dc46cd6563df662fceea6c31` |
| `actor_player_move_w_04@1x.png` | `5c49a8bddbb10485196c5c8c891a8b07aebc981612e83790a09e80ea55201482` | `99923af83a012a8a7c753c274b16317611947a7c4ced9c7f89af87091c0c1823` |
| `actor_player_move_w_05@1x.png` | `c21f4df2adfab24d6f3e7e1c10db5071b9647d88e51708e0dd4c105985143cb4` | `126e090ef493566fdfbb831ecf8bc96d10d2b170150d5b15cb0d67cb6f829801` |
| `actor_player_move_w_06@1x.png` | `75a97de3ea51283f3ce28d249ae422a25317965df5ddd957259addeddf12586f` | `8f4c79748a7ed6806c275c280786cf18da631f216c699947e3a2527f303fef2d` |

270 rejected sprite records and 117 excluded sprite records have no `runtimePath`. Two records are `sfCandidate` and in review, `legacy_san_francisco_decal_damp_asphalt_01` and `legacy_san_francisco_prop_av_shell_01`, and neither has a `runtimePath`. This note does not admit them. It does not close #131.

