# Coordinator review: subtle phase variation

Observed November 16, 2026, 02:39 through 02:55 UTC. Status: verified source proposal, not visual acceptance or native-variation evidence.

## Actual change

The same authored source is reassembled with phase/stance-dependent transfer and recovery easing and a small support-foot lift change. No random frame jitter, raster warp or changed neutral arrival. Measured profiles span transfer skew -0.096137 to 0.091264, recovery skew -0.068448 to 0.072103, and lift 2.804486 to 3.201729 source units instead of a fixed 3. These are proposal parameters, not quality thresholds.

Every new phase has 13 pixel-different RGBA poses, 182 changed poses overall. The largest sampled coordinate differences from baseline are hip 0.052016, knee 0.291912 and toe 0.453766 source units. Unchanged contact-boundary poses and endpoints are intentional. The original phase5/13 samples and all34 PNGs are byte-preserved. The entry and neutral remain pixel-identical for every phase; neutral still begins at 0.375 seconds.

## Independent verification

- Read the generator, checkpoint orchestration, baseline validators, export and comparison control code. All seven baseline dependency locks were independently compared with git commit `15be1316d3817604e751664d5167f1649db2fc6b`.
- Ran 19 source regressions, 22 artifact/provenance mutation regressions, and eight actual-exported-script browser-control harness cases. All passed. Also sampled 70 phase/strength geometry paths and 140 monotone easing traces, with zero-strength exact baseline equality for all14 new phases. The latter is supplemental sampling, not a substitute for visual review.
- `verify_packet.py --source-root` checked all272 frames,32 endpoint provenance records,544 leg/pose rows, original5/13 preservation and rehashed all1,012 original input files. No contact, limb, reach or endpoint guard was relaxed.
- Independently reran the existing source audit against this new packet:32 actual endpoint comparisons and294 exact encoded timestamps passed. Normal/quarter source movies contain147 frames each at128/32fps, with0.375s/1.5s neutral boundaries. These are encoded comparison clocks, not measured live playback.
- Rechecked unchanged baseline native evidence:238 poses/227 source-and-configuration files still verify. No new native result is claimed for the variation.

## Actual browser checks

Brave loaded544 baseline/candidate images on each comparison page at384x416. Normal and hidden quarter-speed pages reached ready state. For each of16 phases, manual poses0/8/12/16 kept both image paths synchronized:64 checks per page,128 total. Changing phase preserved the selected pose. Normal page had no horizontal overflow at the inspected viewport; a screenshot showed complete artwork and explicit baseline/proposal labels. The normal play control entered playing/Pause state through its actual DOM click handler. Background-tab throttling means this is not a cadence measurement.

The browser handoff service returned credential401, so checks continued using the existing direct browser bridge without asking for login or changing providers. An initial open before HTML export existed was retried after export. Neither was treated as an artwork defect or successful validation.

## Owner review and limits

Open `artifacts/normal-speed.html` and separate `artifacts/quarter-speed.html`. The phase selector changes both columns together. Review whether the small rhythm/lift differences improve naturalness, especially phase7/15 landings. Numeric and source checks do not decide visual acceptance.

No production App/Sources/assets/input/mapping/specification-pin edits, merges or admission. Four-facing/family, shared-scene, live-cadence and physical-device gates remain open. Historical runtime#237 remains open with its16-pose assertion unchanged. The twice-capped local full Swift suite was not restarted.
