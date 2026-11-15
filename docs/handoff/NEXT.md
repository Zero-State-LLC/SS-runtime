# SS QA handoff

Updated: 2026-11-15 23:01 UTC.

## Request and authority

User requested QA on SS. This pass records evidence and defects, not release approval. Previous explicit merge approvals applied to earlier audit PRs, not this new evidence branch. Do not merge this PR, bypass review, change branch protection, weaken assertions or move a product pin without the required approval.

## Result

QA run is complete with a contract defect. See `docs/review/qa-2026-11-15.md` and its sibling evidence directory. Tested runtime `df8473713a3d37aeca05d4e1110f979f197b9ceb`, current specs `983a4ca3427bd8a9d30056bccf356fe0f715312e`, runtime authority pin `b1ed874e1e8eb0e61b2174b9093201e9a61e1a4b`.

- Full deterministic core: 850 tests in 123 suites pass, exit 0. Camera placement 9 and fairness 1 pass separately.
- Separately enabled headless daily sitting: all four pinned profiles pass, exit 0. This is a UTC 2026-11-02 fixture, not a phone playtest.
- Native Debug: 166 logical tests / 169 parameter-expanded executions, zero failures/skips. Native Release: 124 / 127, zero failures/skips. Both `TEST SUCCEEDED`, exit 0.
- Specs validators, Python export/palette/audit regressions and pinned payload parity pass.
- Clean SE simulator: title, Settings, largest accessibility text scrolling, Start, pause, verified Home/foreground requiring Resume, and successful DEBUG legal-input full run observed.
- Real archived receipt FAILS its pinned schema with three errors. Independent reproduction is committed and intentionally exits 1.

## Open defect and next work order

Runtime **#233**: archived run receipt fails pinned schema while receipt suites pass. The root camera summary fields are forbidden by `additionalProperties:false`, objectives omit required `extraction`, and an upgrade string violates object/null type. Existing receipt assertions explicitly expect some of the conflicting output. No tests, fixtures, gameplay, schema, pin or CI was changed to force green.

**Gate:** obtain the authoritative product/contract decision for reconciling schema, serializer and tests. Then implement the accepted shape/migration and real serialized-receipt schema coverage. Do not silently patch schema or tests based on this receipt alone. The QA evidence PR requires owner review and separate merge approval.

## Evidence and remaining acceptance

Selected captures, actual archived receipt, extracted xcresult summaries and headless log are in the evidence directory. Full local raw logs and xcresult bundles: `/Users/appliedalchemylabs/.jcode/scratch/ss-qa-20261115/`.

Physical iPhone is unavailable. D-020/D-021 device measurements, interruptions on hardware, touch feel, VoiceOver usability, three consecutive phone runs, twenty manual restarts, owner art admission and independent playtests remain unverified. Runtime #135 remains open. Three long opt-in sweeps remain explicitly unrun, as listed in the QA report. This work does not close Gates A–G, T903/T904 or the expansion gate.
