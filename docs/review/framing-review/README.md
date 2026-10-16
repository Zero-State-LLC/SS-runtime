# Closer street framing — focused renderer comparison

Actual SpriteKit captures at 1×, 1.25× and 1.4×. HUD remains at 1×; world sizes, player registration and authority unchanged. Exact run Test-SSRuntime-2026.10.15_21-16-00--0700: one selected test passed, no failures. Selected via test navigator context menu Run, not Cmd+U. The Xcode AX tree omitted that context menu; screenshot plus Down/Return selected the visible first Run item. This is the verified fast path for subsequent focused captures.

Visual review: 1.25× retains the building base and municipal camera while giving the player more presence. 1.4× crops the building base and loses more ground context. Recommend 1.25× for moving encounter comparison, not production adoption. Full field, offscreen threats, occlusion and input coverage are unproven. Alpha height is calculated from unchanged source bounds/draw mapping; it is not pixel-tracked visibility evidence. The crossing falls outside these closer crops and needs composition reconsideration.

The temporary SSBenchmarkReview scheme and project.yml addition were removed because UI activation was not verified; the existing full scheme remains unchanged. Scene-specific Run is verified by the one-test xcresult.
