# Supported neutral renderer comparison

Test-only bounded-proportion movement and matching held neutral for projected front/world-w alias. Startup world-e remains unsupported and is asserted missing. Production art unchanged.

Initial run 2026-10-19 13:37:24: one test, six failures, one outline texture readback per traversal. The new neutral image was loaded but omitted from outline preparation. Repair adds it to the existing image-based preparation loop; the zero-readback assertion remains unchanged. Focused retry pending. GitHub publication pending connectivity; retain this defect record.

Retry passed: one focused test, zero failures, 19.239 seconds; six variants retain 16 movement frames and supported world-w idle texture through tick 90. Initial world-e missing sprite remains explicit. Neutral is included in image-based outline preparation; zero playback readbacks verified. The 66 targeted Clip tests also passed. This is not full-app validation or visual transition acceptance.
