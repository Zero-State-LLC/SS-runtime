---
title: Validate review packets without unpublished siblings or path aliases
author: Jcode
date: 2026-11-16
branch: qa/bp001-projection-decision-20261116
id: l-review-portability-20261116
scope: repo
status: active
src: agent
touches:
  - "docs/review/existing-art-traversal-20261116/"
  - "docs/review/whole-scene-benchmark-20261116/"
  - "docs/review/camera-surface-authored-20261116/"
  - "docs/review/stone-surface-authored-20261116/"
---

## Decided
- Validate published review evidence in a clean tracked export or standalone packet. Local untracked sibling assets must not satisfy published coverage claims. Explicitly report unpublished evidence as NOT CAPTURED rather than weakening missing-evidence guards.
- Canonicalize temporary fixture roots before comparing them with resolved attachment paths. Test both valid root symlink aliases and real outward symlink escapes. Keep containment assertions intact.
- Replayed manifests must truthfully name the running interpreter. When that field legitimately changes, compare every other field exactly and keep all other export bytes exact. Separately pin the retained author manifest.

## Tried and ruled out
- A whole-scene coverage row referenced an unpublished enemy-source directory and failed clean CI (#242).
- Traversal fixtures mixed unresolved temporary roots with resolved paths on macOS (#244). An explicit symlink alias reproduced the old failure; a default local root did not. The repair retained escape rejection and passed the exact repair-head spec-parity job.
- Camera replay on Python 3.14.7 differed from the author manifest's 3.14.5 metadata. Do not ignore the whole manifest or falsify the interpreter. Focused guards reject all non-interpreter changes.

## Evidence
- docs/review/whole-scene-benchmark-20261116/PARITY-REPAIR.md
- docs/review/existing-art-traversal-20261116/CI-ALIAS-REPAIR.md
- docs/review/existing-art-traversal-20261116/ci-repair-parity-success.json
- docs/review/camera-surface-authored-20261116/test_final.py
- docs/review/camera-surface-authored-20261116/COORDINATOR-REVIEW.md
- docs/review/stone-surface-authored-20261116/verify_clean_copy.py
