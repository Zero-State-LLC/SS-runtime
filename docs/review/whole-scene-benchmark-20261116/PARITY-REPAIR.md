# Spec-parity publication defect, November 16, 2026

Issue: SS-runtime #242. Scope: review-gallery publication only.

## Cause and retained failure

Both run `43823194651` at `d152e6d380aed98ff098538cfcc6836b73bc85f8`
and run `43823296806` at `e64ccd2f86d507dfb9c8022e038cbabc055b1be8`
failed the whole-scene gallery setup in spec-parity. Their completed job logs
identify the same assertion in `build_gallery.py:46`:

```text
AssertionError: enemy-role-first-samples-20261116
```

The coverage matrix claimed this local first-sample directory as captured
source evidence. It was untracked, absent from `git ls-tree -r HEAD`, and
therefore absent from CI. The original builder fails with exactly that assertion
in a `git archive HEAD` export. Local directory existence had masked a
publication error, not a specification-pin or bundled-contract mismatch.

## Correction

The enemy row remains visible but now explicitly says NOT CAPTURED in this
published packet and identifies the first-sample work as unpublished. No local
source packet is imported or granted acceptance. The existing missing-evidence
assertion and its negative test remain unchanged. An additional regression
requires this unpublished row to carry no captured status or evidence link.
The generated coverage matrix is updated from the builder.

## Validation method

Create an isolated export of the pre-fix tracked HEAD with `git archive`, then
copy only the changed builder, coverage matrix and gallery test into it. Do not
copy any untracked directory. Run the exact four commands in CI's
`Test whole-scene diagnostic evidence without visual admission` step and the
following portable blocked-source, existing-art and retained-playback checks.

The initial test invocation used system Python without NumPy and failed to
import. That environment failure is not a product failure or a successful test.
Validation uses the existing video-use Python 3.11 environment with NumPy 2.4.6,
Pillow 12.3.0 and SciPy 1.17.1, matching the CI dependency versions. CI uses
Python 3.12, so local results do not certify the remote job.

The original remote logs and before/after local output are retained under the
session scratch directory as `ci-43823194651-spec-parity.log`,
`ci-43823296806-spec-parity.log`, `parity-build-before-0802.log`,
`parity-gallery-before-0802.log`, and `parity-clean-after-0802.log`.

## Validation results, 08:08 UTC

The clean-export command completed with exit 0. The exact affected CI step
passed 15 baseline/gallery, 7 paving, 13 bound-input and 5 Camera-source tests
(40 total). Previously skipped follow-through also passed: 5 stone-registration
tests, 107 Player-family assertions, both paving verifiers, 22 traversal tests,
7 viewport tests, 28 encounter tests and 7 retained-playback tests. These are
technical evidence checks, not source or visual acceptance. `git diff --check`
passed. The new test and original missing-evidence negative test both ran.

## Boundaries

No capture pixels, production code, input, collision, field geometry, shipping
assets, specification pin or admission records change. No unfiltered Swift
retry. Issues #237/#239/#240/#241 remain separate. Source, physical-device,
visual-acceptance and merge gates remain closed. Remote CI must be checked at
the repair commit before claiming it passes.
