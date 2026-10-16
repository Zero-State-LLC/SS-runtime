# BP-008 live cadence comparison

Status: app suite passed 112 named tests / 114 executions, zero failures or skips. Result bundle: Test-SSRuntime-2026.10.15_17-53-06--0700.xcresult.

The test-only PlayerCandidateScene accumulates actual post-collision displacement per simulation tick and selects the corresponding source texture before action evaluation. Original cadence remains the control. Both use identical source PNGs, legal travel route, projection and logical size; no production renderer or simulation changes.

Matrix: full/half/quarter input × normal/Reduced Motion × original cadence/distance phase. Duration increases at partial input to preserve route distance and repeated cycles. Candidate attachment repetition 20; control 21.

Experiment stride 120 source units is derived from the candidate's support trajectory, not admitted production metadata. First eligible movement starts at zero, zero travel holds phase, and non-move/unsupported facing resets the segment. Actual travel is accumulated per tick rather than from a rendered-position chord. These interruption semantics remain proposed.

Still required: stop/start, collision stop, wall slide, reversal, dodge and pause/resume; separate normal/quarter-speed visual review. No production adoption or benchmark closure.

## Live evidence

All twelve control/candidate × input × motion-mode captures observed all 16 frames. Normal-mode candidate support-point range: full 2.75, half 3.50, quarter 3.50 logical pixels. Matching original-cadence controls: full 0.75–4.50, half 6.25, quarter 8.25–9.25. The candidate used eight support intervals at each input; controls produced eight/sixteen/thirty-two. Do not equate lower cadence with validated walk appearance.

Reduced Motion candidate ranges were full 1.75–2.75, half 2.50–3.25, quarter 3.00–3.50. Sampling cadence affects observed extrema; these are projected authored points, not pixel-tracked feet. Raw post-action records and contact-observations.json retain the observations.

Timing is not accepted: candidate p95 reaches 40.09 ms and maximum 53.19 ms. The core run had finished, but test-order/host effects remain uncontrolled. No sustained frame-rate claim.

Production behavior remains unchanged. The comparison does not close BP-008, other facings, interruption behavior, visual review, the shared scene or device acceptance.
