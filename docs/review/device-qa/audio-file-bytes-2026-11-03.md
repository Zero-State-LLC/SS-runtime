# Shipped audio files

Measured 2026-11-03 from the runtime asset bytes on `9d4656c`. No file was replaced.

`AssetCatalog.deliveredAudioPaths` is the set `AudioEngine` plays. A record is in that set when admission is `adaptedAdmitted` or `originalAccepted`, production status is `accepted`, and kind is `audio` or `music`. The mapped file is `runtimePath`. `AVAudioPlayer` reads that file.

The `sha256` stored on each catalog record is the PCM source at the frozen commit. It is not the digest of the m4a. For all 43 playable records, that catalog digest differs from the file digest below.

Every file is AAC, 2 channels, 48000 Hz. Frames are the valid AAC frames reported by `afinfo`. Seconds are those frames divided by 48000, printed to six places. That print matches `afinfo`'s estimated duration. The sha256 is of the file bytes. No two files share a digest.

Music beds set `numberOfLoops` to -1, and so does `ambience_civic_seam`. The seconds column is the file. A loop does not end at that time.

Forty-three playable records use these 34 files. Sixty-eight other audio or music records are rejected or excluded, and each has no `runtimePath`.

| File | Seconds | Frames | sha256 |
|---|---:|---:|---|
| `agi_attack_burst.m4a` | 0.680000 | 32640 | `dae61dcd5fbf1618b705e373d3b2c725db5e83d0fa8528909484e6a938f92431` |
| `amb_san_francisco_city_identity_loop.m4a` | 29.272021 | 1405057 | `932103ddd5ca61f8bcc62744477018c96ac6e16e767a1345e2ec581706304db9` |
| `amb_shared_gated_serenity_loop.m4a` | 29.153688 | 1399377 | `ecdee42337d9b24e781cc4519a7035bb43fe5ca44d8b7cfe295efb13862b3bbe` |
| `amb_shared_retail_security_zone_loop.m4a` | 59.041542 | 2833994 | `9e68d87c5ac86f87afd0a5eab54670b31ef6ced42e2cfc2c80e80e8abc570d02` |
| `amb_shared_smart_downtown_loop.m4a` | 44.089208 | 2116282 | `4696e04e60378cc5538acbbca958ca190f53647387d280ec002fcf08487eb18b` |
| `mech_autocannon.m4a` | 0.800000 | 38400 | `b4c4a7790ef8067401645c147e024433c960e2095b447a6c6a05765c6a2141fb` |
| `music_atlanta_boss_phase_1_loop.m4a` | 87.846667 | 4216640 | `49539451cc20ba009c83ca2a86439d05028edd219e89e8e988935a8e5adda435` |
| `music_atlanta_boss_phase_2_loop.m4a` | 54.566667 | 2619200 | `aa22afad45512a0b2ec15b7a67796611543b7d7bb4227b83c73270a0b7bf7ae7` |
| `music_atlanta_boss_phase_3_loop.m4a` | 58.833333 | 2824000 | `23c70579cdf6b2a950645379aa9012d3216ed6892276c7dc3ee9a159fed9808b` |
| `music_atlanta_boss_phase_4_loop.m4a` | 114.300000 | 5486400 | `c2f331d200aea88a997a30d4698e7c28093b9c7f292a46604571eb5c5f444aa5` |
| `music_san_francisco_boss_loop.m4a` | 37.100000 | 1780800 | `656d335d4266b4a4a783d4c544284883b79271710edd58ea5c911a4e6b915416` |
| `music_san_francisco_run_loop.m4a` | 54.100000 | 2596800 | `79dbc9ef4a7cc661ea461e4f8fe6a3cc0a59adfd6731d6a1633109d1ac25b2f5` |
| `sfx_blind_spot_field_loop.m4a` | 14.980000 | 719040 | `afe16aaf2e28b10da961432737ad6d7fd4c284323a3af0add2095c68a1af8e7b` |
| `sfx_boss_activated.m4a` | 3.560000 | 170880 | `f0210341658802dbc12514055d6505bfde0f89e4fc96156115cb597cfb63bcde` |
| `sfx_build_synergy_changed.m4a` | 0.879979 | 42239 | `f35dac08761c964b30beef3ca5d19f2809c20297c69c6da3eb7f44269a800c79` |
| `sfx_camera_scan_sweep.m4a` | 1.000000 | 48000 | `dce8d670f24c559272f49f808d5958a9cb47e40cddaa86311f6ea72355b1f5db` |
| `sfx_city_state_changed.m4a` | 0.844812 | 40551 | `83a1b7550b56854e6c20a8eece586807d8165ef1d85c5d96f38100f6295fbe5a` |
| `sfx_coordination_changed.m4a` | 0.879875 | 42234 | `f8cc83e7a8065fda0a9ff668208a7b31299f6aa4f4257609033f6a447f6cb1ea` |
| `sfx_countermeasure_hit.m4a` | 0.480000 | 23040 | `eb966133e409f74043984ad4b31b54d1e4687de89c52bd16a7dfbda38b0c625b` |
| `sfx_director_decision.m4a` | 0.625625 | 30030 | `26f31acd487bb8f60e10855d4c3b896fe9f6b0f01b0d17e872f906ddd5de5c72` |
| `sfx_extraction_completed.m4a` | 4.480000 | 215040 | `beca0f7a298207b9af1c0df3bb7ecb37b0466a399b6dd9fde3cf1349ccc4fb04` |
| `sfx_extraction_opened.m4a` | 2.759021 | 132433 | `3277708e0e8b5ce7b5491eac2a87fd3491e3afd5bd1fa2961acd30fbea0fe055` |
| `sfx_interactable_activate.m4a` | 0.630917 | 30284 | `baf5a07b2e4d09774ce9fce1b25a71ab0cece0584d9fee055b914524abcaf564` |
| `sfx_los_angeles_private_network_persist.m4a` | 2.480000 | 119040 | `55ab982e7fb71b7d0b60c2b3386a06b2d19ab95ef0b1182500e872060d02cc00` |
| `sfx_louisville_map_redaction.m4a` | 0.999979 | 47999 | `5cf76782ca53ec2b1bc1c64b48b0bdbe920b83311e3e606e683604458d12ab46` |
| `sfx_lpr_destroyed.m4a` | 1.279917 | 61436 | `2900a633507e944aa619022ba5d2d27ee2d00b198b390bdfe983ba8311b12fd5` |
| `sfx_player_damaged.m4a` | 0.800000 | 38400 | `72196290cc62ec7b6f0a73fc1b78c8e54cb8d8d7b819a86de7436712850e1c06` |
| `sfx_player_defeated.m4a` | 2.679958 | 128638 | `4650d4136fa07c11e65a4cfa5e1ff509db2933e64d2044698ee2e00c48bbef93` |
| `sfx_san_francisco_hidden_sensor_fog.m4a` | 0.982333 | 47152 | `0c2d557cf274ffc70959b36c04e01ebd79252eb50155f7a830586dd8460544ac` |
| `sfx_suspicion_tier_up.m4a` | 0.354104 | 16997 | `e99343d9d9aa47ac603070f72af9bdaba4761018fd1058f1d81c6ad88cfb2e39` |
| `sfx_upgrade_selected.m4a` | 0.800000 | 38400 | `ae21e1545b84b195fcb873972632aa7fa92c0eea43ae037545d8763ecae7f893` |
| `sfx_weapon_fire.m4a` | 0.350000 | 16800 | `6aedc1f9dfb720dde24496f93899a1af0e009d9f7c94cace1a9faee53a260f71` |
| `stinger_atlanta_final_blind_spot.m4a` | 9.999562 | 479979 | `e7d718a5ccadc375cef73d16536078e5a402fd09d59b44fcbda1ff2c0fe584a5` |
| `trace_warning.m4a` | 0.480000 | 23040 | `30172b8fc8233e7da46b1a5b164fdf64700dcd499764b333f6c2ab704ab4593f` |

## Playable records

Three records are `originalAccepted`: `boss_telegraph_independentReview`, `boss_telegraph_narrowTailoring`, and `boss_telegraph_safetyRationale`. The other forty are `adaptedAdmitted`. Five files back more than one record.

| Asset id | Kind | File |
|---|---|---|
| `ambience_civic_seam` | music | `amb_san_francisco_city_identity_loop.m4a` |
| `boss_defeated` | audio | `stinger_atlanta_final_blind_spot.m4a` |
| `boss_phase_civilLiberties` | audio | `sfx_boss_activated.m4a` |
| `boss_phase_independentReview` | audio | `sfx_boss_activated.m4a` |
| `boss_phase_publicSafety` | audio | `sfx_boss_activated.m4a` |
| `boss_phase_temporarySafeguard` | audio | `sfx_boss_activated.m4a` |
| `boss_telegraph_independentReview` | audio | `agi_attack_burst.m4a` |
| `boss_telegraph_narrowTailoring` | audio | `mech_autocannon.m4a` |
| `boss_telegraph_safetyRationale` | audio | `trace_warning.m4a` |
| `boss_telegraph_temporaryOrder` | audio | `sfx_camera_scan_sweep.m4a` |
| `camera_critical` | audio | `sfx_city_state_changed.m4a` |
| `camera_destroy` | audio | `sfx_lpr_destroyed.m4a` |
| `camera_field_off` | audio | `sfx_blind_spot_field_loop.m4a` |
| `camera_hit_01` | audio | `sfx_countermeasure_hit.m4a` |
| `camera_hit_02` | audio | `sfx_camera_scan_sweep.m4a` |
| `camera_network_tamper` | audio | `sfx_coordination_changed.m4a` |
| `daemon_dash` | audio | `sfx_louisville_map_redaction.m4a` |
| `daemon_query` | audio | `sfx_director_decision.m4a` |
| `exposure_state_up` | audio | `sfx_suspicion_tier_up.m4a` |
| `extraction_armed` | audio | `sfx_extraction_opened.m4a` |
| `extraction_reset` | audio | `sfx_los_angeles_private_network_persist.m4a` |
| `extraction_tick` | audio | `sfx_interactable_activate.m4a` |
| `impact_enemy` | audio | `sfx_countermeasure_hit.m4a` |
| `lockdown_enter` | audio | `sfx_boss_activated.m4a` |
| `music_boss` | music | `music_san_francisco_boss_loop.m4a` |
| `music_boss_civilLiberties` | music | `music_atlanta_boss_phase_2_loop.m4a` |
| `music_boss_independentReview` | music | `music_atlanta_boss_phase_4_loop.m4a` |
| `music_boss_publicSafety` | music | `music_atlanta_boss_phase_1_loop.m4a` |
| `music_boss_temporarySafeguard` | music | `music_atlanta_boss_phase_3_loop.m4a` |
| `music_explore` | music | `music_san_francisco_run_loop.m4a` |
| `music_extraction` | music | `amb_shared_smart_downtown_loop.m4a` |
| `music_lockdown` | music | `amb_shared_retail_security_zone_loop.m4a` |
| `music_observed` | music | `music_san_francisco_run_loop.m4a` |
| `music_terminal` | music | `amb_shared_gated_serenity_loop.m4a` |
| `network_blackout` | audio | `sfx_build_synergy_changed.m4a` |
| `player_damage` | audio | `sfx_player_damaged.m4a` |
| `player_death` | audio | `sfx_player_defeated.m4a` |
| `player_dodge` | audio | `sfx_san_francisco_hidden_sensor_fog.m4a` |
| `run_success` | audio | `sfx_extraction_completed.m4a` |
| `upgrade_selected_ghostStep` | audio | `sfx_upgrade_selected.m4a` |
| `upgrade_selected_ricochetPulse` | audio | `sfx_upgrade_selected.m4a` |
| `upgrade_selected_signalJammer` | audio | `sfx_upgrade_selected.m4a` |
| `weapon_civic_pulse` | audio | `sfx_weapon_fire.m4a` |

This does not change a cue, a bus, or a file. It does not regenerate audio. Specs #63 stays open.
