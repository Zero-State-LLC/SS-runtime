#!/usr/bin/env python3
"""Verify this presentation-only correction leaves frozen authority/art/tests intact.

Uses Git's tracked-byte/mode comparison, not source-directory counts or mtimes.
Unrelated untracked work is neither inspected nor deleted.
"""
import json
from pathlib import Path
import subprocess

BASE = "2baaeb1765c1df0618b79c1af826f40139d4d793"
ROOT = Path(__file__).resolve().parents[3]
PROTECTED = ["Sources/", "Tests/", "RuntimeAssets/", "AppTests/", "docs/review/"]
EXCLUDED = ["docs/review/live-world-projection-20261117/",
            "docs/review/production-execution-20261117/README.md"]
PATHS = PROTECTED + [":(exclude)" + path for path in EXCLUDED]


def verify(root=ROOT, base=BASE):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])
    tracked = git("ls-tree", "-r", "--name-only", "-z", base, "--", *PROTECTED).split(b"\0")
    tracked = [p for p in tracked if p and not any(p.decode().startswith(e) for e in EXCLUDED)]
    if not tracked:
        raise ValueError("No frozen files found")
    # --diff-filter excludes additions: a new test is allowed, editing/removing an old test is not.
    changed = git("diff", "--no-ext-diff", "--name-only", "--diff-filter=CDMRTUXB", "-z", base, "--", *PATHS)
    paths = [p.decode() for p in changed.split(b"\0") if p]
    added = git("diff", "--no-ext-diff", "--name-only", "--diff-filter=A", "-z", base, "--", *PATHS)
    paths += [p.decode() for p in added.split(b"\0") if p and not p.startswith(b"AppTests/")]
    if paths:
        raise ValueError("Frozen authority/art/test bytes or modes changed: " + ", ".join(paths))
    return {"status": "FROZEN_AUTHORITY_ART_TESTS_UNCHANGED_NOT_VISUAL_ACCEPTANCE",
            "base": base, "trackedProtectedFiles": len(tracked), "paths": PROTECTED, "excluded": EXCLUDED}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
