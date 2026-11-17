"""#258: exercise checkout lifecycle without a network dependency."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/spec_parity.sh'


class SpecParityIsolationTests(unittest.TestCase):
    def test_parallel_fetch_failures_have_unique_roots_and_preserve_neighbors(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('JCODE_SCRATCH_DIR')) as temp:
            root = Path(temp).resolve()
            scratch = root / 'scratch with spaces'
            scratch.mkdir()
            sentinel = scratch / 'unrelated'
            sentinel.write_text('preserve')
            tools = root / 'bin'
            tools.mkdir()
            fake = tools / 'git'
            fake.write_text('''#!/usr/bin/env python3
import os, sys
from pathlib import Path
args = sys.argv[1:]
if args[0] == 'init':
    path = Path(args[-1])
    assert path.is_dir()
    with open(os.environ['PARITY_CALLS'], 'a') as log:
        log.write(str(path) + '\\n')
if 'fetch' in args:
    raise SystemExit(23)
''')
            fake.chmod(0o755)
            calls = root / 'calls'
            env = dict(os.environ, JCODE_SCRATCH_DIR=str(scratch),
                       PATH=str(tools) + os.pathsep + os.environ['PATH'], PARITY_CALLS=str(calls))
            processes = [subprocess.Popen(['bash', str(SCRIPT)], cwd=ROOT, env=env,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                         for _ in range(2)]
            for process in processes:
                stdout, stderr = process.communicate(timeout=20)
                self.assertEqual(process.returncode, 23, stdout + stderr)
            paths = [Path(value) for value in calls.read_text().splitlines()]
            self.assertEqual(len(paths), 2)
            self.assertNotEqual(paths[0], paths[1])
            for path in paths:
                self.assertEqual(path.parent, scratch)
                self.assertFalse(path.exists())
            self.assertEqual(sentinel.read_text(), 'preserve')
            self.assertEqual(list(scratch.iterdir()), [sentinel])

    def test_shared_checkout_and_global_delete_are_absent(self):
        source = SCRIPT.read_text()
        self.assertNotIn('/tmp/spec-parity-check', source)
        self.assertIn('mktemp -d', source)
        self.assertIn('cmp -s "$bundled" "$spec"', source)
        self.assertIn('find contracts fixtures', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
