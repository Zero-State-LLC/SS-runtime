# Actual upgrade scroll and touch interaction

Slice10 of the approved source-to-scene continuation. Review-only host of the unchanged production `App/UpgradeSelectionView.swift` and its real model. No production files or signing configuration changed.

## Native result

Dedicated SE3 simulator84297C74-033E-408F-9622-D36BFF32F74E, iOS26.5, landscape667x375 points. The08:36 run `ss-upgrade-ui-0836.xcresult` passed3tests,0failures,0skips, with54.318s test execution. Raw exported summary, exact identities,12attachments and their export manifest are under `capture/`; native log is retained. Records attest actual XCUI swipes/taps and callback observations:

- Default large: Signal Jammer selected index0 exactly once,0swipes.
- Accessibility3: Ghost Step initially not hittable,2actual swipes, selected index2 exactly once.
- Accessibility5: same required scroll and exactly-once result.
- Scrolling did not select. Production model disabled the selected button after submission. Accessible choice label was nonempty and recorded.

These are real interactions in an isolated production-view host, not copied or simulated selection logic. They do **not** prove full-game pause/resume, physical-device behavior, VoiceOver navigation/speech, every upgrade or every viewport. A button becoming hittable does not prove every line of its long description was read. No blanket accessibility compliance or visual acceptance claim.

## Screenshot failure preserved (#243)

The first08:31 native run passed interactions, but `app.screenshot()` produced misoriented/cropped landscape window captures with large blank padding. Coordinator rejected those images as layout evidence. All original attachments, result files and test source remain under `attempts/01-window-capture/`.

Changed only capture API to `XCUIScreen.main.screenshot()` and reran the same3interaction assertions. Corrected raw PNGs retain750x1334 pixel storage and EXIF orientation; orientation-aware display is1334x750. Do not rotate/recompress the retained evidence bytes. Coordinator inspected default and accessibility5 before/reachable images: the artificial padding/right crop is gone. Large text still requires vertical scrolling by design. The gallery honors EXIF, displays667x375 logical and333.5x187.5 half dimensions. Actual Brave08:44 loaded all9images, verified both dimensions, grayscale restoration and no horizontal page overflow.

## Portable verification

```sh
python3 -B -W error::ResourceWarning docs/review/upgrade-interaction-20261116/verify.py
python3 -B -W error::ResourceWarning docs/review/upgrade-interaction-20261116/test_evidence.py
```

Six retained-evidence tests passed at08:43. They reject zero/wrong tests, altered result counts, false scroll/selection/scope claims, changed image bytes, path escapes, and the old capture method. `build_gallery.py` seals newly imported bytes and generates HTML; it is not an independent source-of-truth validator and must not be used to bless altered evidence. The recorded inventory binds retained export bytes, not execution-source hashes. Native test log/result identities and source are retained, but no cryptographic executed-source attestation is claimed.

## Reproduce native run

Generate this isolated `project.yml` with XcodeGen, then select the3UITests through its `SSUpgradeReview` scheme on the dedicated simulator, with a fresh result bundle, `-parallel-testing-enabled NO CODE_SIGNING_ALLOWED=NO`. No dependency installation needed. The local package supplies SurveillanceCore. Serialize native execution and preserve failed artifacts. No unfiltered local Swift retry is authorized.

Physical signing remains a separate gate. #243 remains open for integration review; this evidence records a bounded harness capture repair, not a production UI change or issue closure.
