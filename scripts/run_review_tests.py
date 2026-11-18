"""Run frozen review tests with a canonical scratch root, preserving path guards."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def run(arguments, environment=None):
    env = dict(os.environ if environment is None else environment)
    base = Path(env.get('JCODE_SCRATCH_DIR') or tempfile.gettempdir()).resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix='ss-review-', dir=base) as temporary:
        root = str(Path(temporary).resolve(strict=True))
        env.update(JCODE_SCRATCH_DIR=root, TMPDIR=root, TEMP=root, TMP=root)
        return subprocess.run([sys.executable, *arguments], env=env, check=False).returncode


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('usage: run_review_tests.py <python arguments>')
    raise SystemExit(run(sys.argv[1:]))
