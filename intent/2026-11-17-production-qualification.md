# Runtime production qualification repair

Date: 2026-11-17
Status: accepted scope under the owner's 2026-11-17T01:55:50Z execution directive

## Authority and outcome

Implement routine, reversible engineering repairs under existing accepted requirements. The owner explicitly authorized CI/test defects and release-qualification work, not merges, releases, deployment, paid asset jobs or invented acceptance. Applicable T902/T907/T908, BP-001 through BP-006 and existing CI parity requirements.

1. Runtime #256: reproduce the macOS temporary-root alias failure; execute the frozen review suite under an isolated canonical scratch root. Keep strict assembly/supplement symlink rejection, missing-file assertions, all captured bytes and failure history intact. Prove child failures remain failures.
2. Runtime #257: enumerate all120 gates in pinned SS-specs acceptance.md, including A-013A, D-022 through D-024 and E-021. A missing gate must prevent expansion, and a failed gate must fail expansion. Do not mark newly enumerated gates passed or replace missing device/human evidence.

3. Measured hashing cost: the retained actual Debug process sample at02:39UTC attributes215samples to canonical SHA256 hex generation. Use the system SHA256 implementation where available, retain the portable algorithm and exact lowercase output, and test both against fixed vectors and padding/binary/UTF8 boundaries. No simulation serialization, digest identity, timing, replay schema or acceptance threshold changes. Isolated host microbenchmarks do not establish an FPS improvement or resolve playback237/traversal259.

No gameplay, ruleset, arena, content, replay schema, artwork or contract payload changes. The canonical asset catalog remains authoritative. Owner's camera-adjacent-building-only correction remains in force. Latest accepted specification must be checked before any later gameplay change. Existing separate receipt-adoption PRs retain specification-first order.

## Verification

Retain reproduced red cases, real affected test execution, strict path negative cases, Swift gate regressions and current host qualification. Publish implementation and evidence to existing review PR236 without merging. Report simulator and physical-device evidence separately. Expansion remains NOT_COMPUTABLE unless the actual accepted gates are met.
