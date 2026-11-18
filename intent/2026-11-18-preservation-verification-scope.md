# Preservation verification scope repair

Date: 2026-11-18
Status: accepted bounded continuation of issue #262, user instruction at 22:02:58 UTC.

## Outcome and authority

Restore honest CI verification after later authorized runtime engineering changed bytes protected by the earlier V9 comparison's historical receipt. This implements the next work order in docs/handoff/NEXT.md. Existing production-qualification authority permits reversible CI/test-defect repair, not weakening tests to force green.

## Contract

- Preserve original V9 audit, tests, receipt, source art, captures and all failed evidence byte-for-byte.
- Run its unchanged historical audit and negative tests against an isolated, exact historical snapshot. Identify that result as historical, not current-head qualification.
- Independently check current protected files against the original receipt plus only exact, provenance-bound transitions for the five inventoried changed paths. No broad path exemptions or replacement of the original receipt.
- Bind each transition to its original digest, final digest and exact implementation commit. Reject unauthorized drift, missing files, symlinks, altered receipt, altered historical verifier and invalid transition provenance. Test rejection behavior and propagation of subprocess failures.
- Keep the rest of the V9 source, scene, retained-native, baseline-pixel and gallery checks on the current checkout, unchanged. CI needs available pinned historical objects without a hidden network fetch in the validator.
- Use only tracked snapshot inputs for publication validation, never depend on unrelated untracked art.

## Scope

New verifier, negative tests and new evidence packet, narrow CI wiring, intent and handoff. No App, Sources, original tests/receipts/art or product behavior changes. Current-tree verification is strict byte/provenance qualification, not re-certification of gameplay or visuals. Historical #237/#259 failures and original #261 red evidence remain preserved. No merge, issue closure, release, paid action, automatic polling chain or visual/device/human acceptance.

## Acceptance

Reproduce the original failure. Enumerate all 1766 original protected paths and all five differences with authority references. Prove original historical tests and audit pass at the exact frozen snapshot, while current unapproved bytes and malformed transition metadata fail. Run complete affected CI step against a tracked export, inspect the final diff, publish to existing PR236 and query only its exact resulting head. Report remote pending/failure accurately.
